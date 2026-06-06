"""
Lightweight ORLM-style pipeline for an 8GB laptop GPU.

Replaces the original heavy stack (vLLM + coptpy) with:
  - Inference : a local small model served by Ollama (default: qwen2.5:3b)
  - Solver    : PuLP + CBC (open source, no license)

It mirrors ORLM's eval loop: NL question -> (math model + python code) -> execute -> compare
the optimal objective against the ground-truth answer with 5% tolerance (pass@1, greedy).

Dataset: NL4OPT test set, read OFFLINE from the repo's reference results file
(results/NL4OPT.q2mc_en.ORLM-LLaMA-3-8B/executed.jsonl), so no HF download is needed.

Usage:
  python mini/run_mini.py --n 8
  python mini/run_mini.py --n 245 --model qwen2.5:3b
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time

import requests

# --- PuLP variant of ORLM's q2mc prompt template -----------------------------
TEMPLATE = r"""Below is an operations research question. Build a mathematical model and corresponding python code using `PuLP` that appropriately addresses the question.

Follow these rules for the python code:
- Use the `PuLP` library only.
- Name the LpProblem variable exactly `prob`.
- Call `prob.solve()` to solve it.
- Put the full python code inside a single ```python ... ``` block.

# Question:
{Question}

# Response:
"""

# Runner: executes the model's code in an isolated namespace. If the model's own
# trailing lines crash (small models often write buggy status-print lines AFTER
# solving), the exception is caught but `prob` — already built and solved — is
# preserved, so we can still read the objective. This isolates true formulation
# errors from cosmetic code bugs.
RUNNER = r"""
import sys
from pulp import *
import pulp
g = {}
exec("from pulp import *\nimport pulp\n", g)
src = open(sys.argv[1], encoding="utf-8").read()
try:
    exec(compile(src, "model", "exec"), g)
except Exception as e:
    print("MODEL_CODE_ERROR:", repr(e))
prob = g.get("prob", None)
try:
    print("STATUS:", LpStatus[prob.status])
    print("BEST_OBJECTIVE:", value(prob.objective))
except Exception as e:
    print("SCORER_ERROR:", repr(e))
"""

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# All four ORLM benchmarks are readable offline from the repo's reference result
# files (each has en_question / en_answer). No HF download needed.
BENCHMARKS = {
    "NL4OPT": "NL4OPT.q2mc_en.ORLM-LLaMA-3-8B",
    "IndustryOR": "IndustryOR.q2mc_en.ORLM-LLaMA-3-8B",
    "MAMO_EasyLP": "MAMO.EasyLP.q2mc_en.ORLM-LLaMA-3-8B",
    "MAMO_ComplexLP": "MAMO.ComplexLP.q2mc_en.ORLM-LLaMA-3-8B",
}


def load_dataset(benchmark, limit):
    ref = os.path.join(REPO, "results", BENCHMARKS[benchmark], "executed.jsonl")
    seen = {}
    with open(ref, encoding="utf-8") as f:
        for line in f:
            e = json.loads(line)
            seen.setdefault(e["en_question"], e["en_answer"])
    items = [{"en_question": q, "en_answer": a} for q, a in seen.items()]
    return items[:limit]


def ollama_generate(model, prompt, host="http://localhost:11434"):
    r = requests.post(
        f"{host}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0, "num_predict": 2048},
        },
        timeout=600,
    )
    r.raise_for_status()
    return r.json()["response"]


def extract_code(text):
    start = text.find("```python")
    if start == -1:
        return None
    end = text.find("```", start + len("```python"))
    if end == -1:
        return None
    return text[start + len("```python"):end]


def run_code(script, timeout=120):
    target_dir = os.path.join(REPO, "mini", "_exec")
    os.makedirs(target_dir, exist_ok=True)
    # write the model's code to a sidecar source file, plus a runner that execs it
    src_fh = tempfile.NamedTemporaryFile(delete=False, suffix=".src.py", dir=target_dir, mode="w", encoding="utf-8")
    src_fh.write(script)
    src_path = src_fh.name
    src_fh.close()
    run_fh = tempfile.NamedTemporaryFile(delete=False, suffix=".run.py", dir=target_dir, mode="w", encoding="utf-8")
    run_fh.write(RUNNER)
    run_path = run_fh.name
    run_fh.close()
    try:
        p = subprocess.run([sys.executable, run_path, src_path], text=True, capture_output=True, timeout=timeout)
        out = p.stdout
        err = p.stderr
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT", "Execution Failed: Timeout"
    finally:
        for pth in (src_path, run_path):
            try:
                os.remove(pth)
            except OSError:
                pass

    m = re.search(r"BEST_OBJECTIVE:\s*([^\n]+)", out)
    status_m = re.search(r"STATUS:\s*([^\n]+)", out)
    status = status_m.group(1).strip() if status_m else "?"
    if m is None:
        # show why it failed
        reason = err.strip().splitlines()[-1] if err.strip() else "no BEST_OBJECTIVE printed"
        return None, status, f"Execution Failed: {reason}"
    val = m.group(1).strip()
    if val in ("None", "none", ""):
        return None, status, "Execution Successful but No Objective"
    try:
        return float(val), status, "OK"
    except ValueError:
        return None, status, f"Execution Successful but unparsable objective: {val!r}"


SOLVE_FAIL_STATUS = {"Not Solved", "Infeasible", "Unbounded", "Undefined"}


def is_match(pred, gt, status="?", tol=0.05):
    # Some NL4OPT items are infeasible; their ground truth is the string
    # "No Best Solution". Count a match when the solver also proved no optimum.
    if isinstance(gt, str) and gt.strip() == "No Best Solution":
        return status in SOLVE_FAIL_STATUS
    if pred is None:
        return False
    gt = float(gt)
    if gt == 0:
        return abs(pred) <= tol
    return abs((pred - gt) / gt) <= tol


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", type=str, default="NL4OPT", choices=list(BENCHMARKS))
    ap.add_argument("--n", type=int, default=8, help="number of questions")
    ap.add_argument("--model", type=str, default="qwen2.5:3b")
    ap.add_argument("--save", type=str, default=None)
    args = ap.parse_args()
    if args.save is None:
        args.save = os.path.join(REPO, "mini", f"results_{args.benchmark}.jsonl")

    data = load_dataset(args.benchmark, args.n)
    print(f"Loaded {len(data)} {args.benchmark} questions | model={args.model} | solver=PuLP/CBC\n")

    judges = []
    fw = open(args.save, "w", encoding="utf-8")
    t0 = time.time()
    for i, ex in enumerate(data):
        try:
            prompt = TEMPLATE.replace("{Question}", ex["en_question"].strip())
            gen = ollama_generate(args.model, prompt)
            code = extract_code(gen)
            if code is None:
                pred, status, state = None, "?", "Execution Failed: No code block"
            else:
                pred, status, state = run_code(code)
            ok = is_match(pred, ex["en_answer"], status)
        except Exception as e:
            # never let one bad item kill a long run
            gen, pred, status, state, ok = "", None, "?", f"Harness Error: {e!r}", False
        judges.append(1 if ok else 0)

        mark = "PASS" if ok else "FAIL"
        print(f"[{i+1:>3}/{len(data)}] {mark} | pred={pred} gt={ex['en_answer']} | {status} | {state[:60]}", flush=True)
        fw.write(json.dumps({
            "en_question": ex["en_question"],
            "en_answer": ex["en_answer"],
            "generation": gen,
            "pred": pred,
            "status": status,
            "state": state,
            "correct": ok,
        }, ensure_ascii=False) + "\n")
        fw.flush()
    fw.close()

    acc = sum(judges) / len(judges) if judges else 0.0
    dt = time.time() - t0
    print(f"\n==== pass@1 = {acc:.3f}  ({sum(judges)}/{len(judges)})  |  {dt:.0f}s total, {dt/max(len(judges),1):.1f}s/q ====")
    print(f"Details saved to {args.save}")


if __name__ == "__main__":
    main()
