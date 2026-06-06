"""
Curate the "both-fail" set: instances where BOTH our small local model (3B) AND
the fine-tuned ORLM-LLaMA-3-8B reference produce a wrong answer.

These are the instances that are NOT fixed by "use a bigger / fine-tuned model",
so they are the genuine target for an instance-level formulation method.

For each instance we record the question, the ground truth, both models' answers,
both models' formulations, and the 3B failure category (WRONG_FORMULATION /
SOLVE_FAILED / CODE_BUG) so the set can be sliced by failure mode.

Outputs:
  mini/hardset_<bench>.jsonl  - machine-readable curated set
  mini/hardset_<bench>.md     - human-readable with both formulations

Usage:
  python mini/hard_set.py --benchmark IndustryOR --pred mini/full_industryor_3b.jsonl
"""
import argparse
import json
import os
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCHMARKS = {
    "NL4OPT": "NL4OPT.q2mc_en.ORLM-LLaMA-3-8B",
    "IndustryOR": "IndustryOR.q2mc_en.ORLM-LLaMA-3-8B",
    "MAMO_EasyLP": "MAMO.EasyLP.q2mc_en.ORLM-LLaMA-3-8B",
    "MAMO_ComplexLP": "MAMO.ComplexLP.q2mc_en.ORLM-LLaMA-3-8B",
}
SOLVE_FAIL_STATUS = {"Not Solved", "Infeasible", "Unbounded", "Undefined"}


def match(sol, ans, tol=0.05):
    if isinstance(ans, str) and ans.strip() == "No Best Solution":
        return sol == "No Best Solution"
    if sol is None or sol == "No Best Solution":
        return False
    try:
        sol = float(sol); ans = float(ans)
    except (TypeError, ValueError):
        return False
    return abs(sol) <= tol if ans == 0 else abs((sol - ans) / ans) <= tol


def category(e):
    if e.get("correct"):
        return "PASS"
    status = (e.get("status") or "?").strip()
    if status == "Optimal" and e.get("pred") is not None:
        return "WRONG_FORMULATION"
    if status in SOLVE_FAIL_STATUS:
        return "SOLVE_FAILED"
    return "CODE_BUG"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", default="IndustryOR", choices=list(BENCHMARKS))
    ap.add_argument("--pred", required=True)
    args = ap.parse_args()

    mine = {}
    for line in open(args.pred, encoding="utf-8"):
        e = json.loads(line)
        mine[e["en_question"]] = e
    ref_path = os.path.join(REPO, "results", BENCHMARKS[args.benchmark], "executed.jsonl")
    ref = {}
    for line in open(ref_path, encoding="utf-8"):
        e = json.loads(line)
        ref.setdefault(e["en_question"], e)

    both_fail = []
    for q, me in mine.items():
        r = ref.get(q)
        if r is None:
            continue
        if me.get("correct"):
            continue
        if match(r.get("execution_best_solution"), r.get("en_answer")):
            continue  # 8B got it right -> not a both-fail case
        both_fail.append((q, me, r))

    cats = Counter(category(me) for _, me, _ in both_fail)
    print(f"benchmark={args.benchmark}  questions={len(mine)}")
    print(f"both-fail (3B wrong AND 8B wrong): {len(both_fail)}")
    print("  3B failure-mode breakdown within both-fail:")
    for c in ("WRONG_FORMULATION", "SOLVE_FAILED", "CODE_BUG"):
        print(f"    {c:<18} {cats.get(c,0)}")

    out_jsonl = os.path.join(REPO, "mini", f"hardset_{args.benchmark}.jsonl")
    out_md = os.path.join(REPO, "mini", f"hardset_{args.benchmark}.md")
    with open(out_jsonl, "w", encoding="utf-8") as fj, open(out_md, "w", encoding="utf-8") as fm:
        fm.write(f"# Both-fail instance set ({args.benchmark})\n\n")
        fm.write(f"{len(both_fail)} instances where BOTH 3B and ORLM-8B are wrong. "
                 f"3B modes: {dict(cats)}\n\n")
        for k, (q, me, r) in enumerate(both_fail):
            cat = category(me)
            fj.write(json.dumps({
                "en_question": q,
                "en_answer": me["en_answer"],
                "pred_3b": me.get("pred"),
                "status_3b": me.get("status"),
                "category_3b": cat,
                "sol_8b": r.get("execution_best_solution"),
                "formulation_3b": me.get("generation", ""),
                "formulation_8b": r.get("en_math_model_coptpy_code", ""),
            }, ensure_ascii=False) + "\n")

            fm.write(f"\n## Case {k+1}  [{cat}]\n\n")
            fm.write(f"**GT:** {me['en_answer']}  |  **3B:** {me.get('pred')} ({me.get('status')})  "
                     f"|  **8B:** {r.get('execution_best_solution')}\n\n")
            fm.write(f"### Question\n{q.strip()}\n\n")
            fm.write(f"### 3B formulation\n{me.get('generation','').strip()}\n\n")
            fm.write(f"### ORLM-8B formulation\n{r.get('en_math_model_coptpy_code','').strip()}\n\n---\n")

    print(f"\nWrote: {out_jsonl}\n       {out_md}")


if __name__ == "__main__":
    main()
