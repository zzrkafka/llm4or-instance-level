"""
Per-instance contrastive analysis: where the small local model (3B) got the
formulation WRONG but the stronger ORLM-LLaMA-3-8B reference got it RIGHT.

The repo's results/<bench>/executed.jsonl files contain, for every question, the
ORLM-8B generated math model + coptpy code and its executed objective value.
This script matches them against our 3B run by question text and extracts the
"weak-wrong vs strong-correct" pairs -- the raw material for studying *why* a
formulation fails on a specific instance (the instance-level question).

Usage:
  python mini/compare.py --benchmark NL4OPT --pred mini/full_nl4opt_3b.jsonl
  python mini/compare.py --benchmark IndustryOR --pred mini/full_industryor_3b.jsonl
"""
import argparse
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCHMARKS = {
    "NL4OPT": "NL4OPT.q2mc_en.ORLM-LLaMA-3-8B",
    "IndustryOR": "IndustryOR.q2mc_en.ORLM-LLaMA-3-8B",
    "MAMO_EasyLP": "MAMO.EasyLP.q2mc_en.ORLM-LLaMA-3-8B",
    "MAMO_ComplexLP": "MAMO.ComplexLP.q2mc_en.ORLM-LLaMA-3-8B",
}


def match(sol, ans, tol=0.05):
    if isinstance(ans, str) and ans.strip() == "No Best Solution":
        return sol == "No Best Solution"
    if sol is None or sol == "No Best Solution":
        return False
    try:
        sol = float(sol); ans = float(ans)
    except (TypeError, ValueError):
        return False
    if ans == 0:
        return abs(sol) <= tol
    return abs((sol - ans) / ans) <= tol


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", default="NL4OPT", choices=list(BENCHMARKS))
    ap.add_argument("--pred", required=True, help="our 3B results jsonl")
    ap.add_argument("--out", default=None)
    ap.add_argument("--limit", type=int, default=20, help="max pairs to write")
    args = ap.parse_args()
    if args.out is None:
        args.out = os.path.join(REPO, "mini", f"contrast_{args.benchmark}.md")

    # our 3B run, keyed by question
    mine = {}
    for line in open(args.pred, encoding="utf-8"):
        e = json.loads(line)
        mine[e["en_question"]] = e

    # ORLM-8B reference, keyed by question
    ref_path = os.path.join(REPO, "results", BENCHMARKS[args.benchmark], "executed.jsonl")
    ref = {}
    for line in open(ref_path, encoding="utf-8"):
        e = json.loads(line)
        ref.setdefault(e["en_question"], e)

    pairs = []
    n_my_wrong = 0
    for q, me in mine.items():
        if me.get("correct"):
            continue
        n_my_wrong += 1
        r = ref.get(q)
        if r is None:
            continue
        ref_correct = match(r.get("execution_best_solution"), r.get("en_answer"))
        if ref_correct:
            pairs.append((q, me, r))

    n = len(mine)
    print(f"benchmark={args.benchmark}  questions={n}")
    print(f"3B wrong: {n_my_wrong}")
    print(f"  of which ORLM-8B got RIGHT (recoverable / formulation-gap): {len(pairs)}")
    print(f"  -> these are the instance-level study cases\n")

    with open(args.out, "w", encoding="utf-8") as fw:
        fw.write(f"# Contrastive pairs ({args.benchmark}): 3B wrong vs ORLM-8B correct\n\n")
        fw.write(f"3B wrong: {n_my_wrong} | of which 8B correct: {len(pairs)}\n\n")
        for k, (q, me, r) in enumerate(pairs[: args.limit]):
            fw.write(f"\n## Case {k+1}\n\n")
            fw.write(f"**Ground truth:** {me['en_answer']}  |  **3B answer:** {me.get('pred')} ({me.get('status')})  |  **8B answer:** {r.get('execution_best_solution')}\n\n")
            fw.write(f"### Question\n{q.strip()}\n\n")
            fw.write(f"### 3B formulation (WRONG)\n{me.get('generation','').strip()}\n\n")
            fw.write(f"### ORLM-8B formulation (CORRECT)\n{r.get('en_math_model_coptpy_code','').strip()}\n\n")
            fw.write("---\n")
    print(f"Wrote {min(len(pairs), args.limit)} cases to {args.out}")


if __name__ == "__main__":
    main()
