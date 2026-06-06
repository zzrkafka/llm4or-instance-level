"""
Failure attribution for mini ORLM runs.

Reads a results jsonl (from run_mini.py) and buckets every question into:
  PASS              - correct answer (within 5% tolerance)
  WRONG_FORMULATION - solved to Optimal but the objective is wrong (genuine modeling error)
  SOLVE_FAILED      - model is runnable but Infeasible/Unbounded/Not Solved (bad constraints)
  CODE_BUG          - no code block / runtime error / objective never produced

The PASS vs WRONG_FORMULATION vs SOLVE_FAILED split is the useful signal:
it separates "the LLM can't write code" from "the LLM picked the wrong formulation",
which is the evidence base for the problem-level vs instance-level discussion.

Usage:
  python mini/analyze.py mini/full_nl4opt_3b.jsonl
"""
import json
import sys
from collections import Counter

SOLVE_FAIL_STATUS = {"Not Solved", "Infeasible", "Unbounded", "Undefined"}


def classify(e):
    if e.get("correct"):
        return "PASS"
    status = (e.get("status") or "?").strip()
    pred = e.get("pred")
    if status == "Optimal" and pred is not None:
        return "WRONG_FORMULATION"
    if status in SOLVE_FAIL_STATUS:
        return "SOLVE_FAILED"
    return "CODE_BUG"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "mini/full_nl4opt_3b.jsonl"
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    buckets = {"PASS": [], "WRONG_FORMULATION": [], "SOLVE_FAILED": [], "CODE_BUG": []}
    for e in rows:
        buckets[classify(e)].append(e)

    n = len(rows)
    print(f"\nFile: {path}")
    print(f"Total questions: {n}\n")
    print(f"{'category':<20}{'count':>7}{'pct':>9}")
    print("-" * 36)
    for cat in ("PASS", "WRONG_FORMULATION", "SOLVE_FAILED", "CODE_BUG"):
        c = len(buckets[cat])
        print(f"{cat:<20}{c:>7}{c/n*100:>8.1f}%")
    print("-" * 36)
    print(f"{'pass@1':<20}{len(buckets['PASS'])/n*100:>15.1f}%\n")

    # show a few concrete examples of the non-PASS categories
    for cat in ("WRONG_FORMULATION", "SOLVE_FAILED", "CODE_BUG"):
        ex = buckets[cat][:3]
        if not ex:
            continue
        print(f"=== examples: {cat} ===")
        for e in ex:
            q = e["en_question"].strip().replace("\n", " ")
            print(f"  pred={e.get('pred')} gt={e.get('en_answer')} status={e.get('status')}")
            print(f"    Q: {q[:130]}...")
            if cat == "CODE_BUG":
                print(f"    state: {str(e.get('state'))[:100]}")
        print()


if __name__ == "__main__":
    main()
