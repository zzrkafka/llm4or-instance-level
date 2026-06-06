"""
Heuristic tagging of the both-fail instance set by *formulation challenge type*.

Each instance can carry several tags (multi-label). Tags are keyword/structure
heuristics over the question text -- a first-pass triage to size the challenge
landscape, not a hand-verified gold labeling. The output table is the
"what an instance-level method must handle" checklist.

Usage:
  python mini/tag_hardset.py --hardset mini/hardset_IndustryOR.jsonl
"""
import argparse
import json
import re
from collections import Counter, defaultdict

# tag -> regex (case-insensitive) over the question text
TAGS = {
    "MIN_MAX/MAKESPAN":   r"completion time of the last|makespan|minimi\w*\s+the\s+maximum|the last (task|job)|earliest.*(finish|complete)",
    "ASSIGN/SCHEDULE":    r"\b(assign|schedul\w+|machine|processor|cpu|\bjob\b|shift|roster|sequence)\b",
    "MULTI_PERIOD/TIME":  r"time period|each (hour|day|week|month|year)|\d{1,2}:\d{2}|per (hour|day|week)|over .*(days|weeks|months|periods)",
    "NETWORK/TRANSPORT":  r"\b(warehouse|transport\w*|route|shipping|ship\b|container|distribut\w+|supply|demand|origin|destination)\b",
    "TABLE_DATA":         r"\|.*\|",
    "RATIO/PERCENT":      r"%|percent|at least .* of the|\bratio\b",
    "UNIT_CONVERSION":    r"\bg?hz\b|km/?h|per hour|kwh|frequency|grams? of|per 100",
    "INTEGER/COUNT":      r"\b(integer|whole number|number of|how many)\b",
}


def tag_text(q):
    tags = []
    for name, pat in TAGS.items():
        if re.search(pat, q, re.I):
            tags.append(name)
    return tags or ["UNTAGGED"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hardset", required=True)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.hardset, encoding="utf-8")]
    tag_count = Counter()
    tag_by_mode = defaultdict(Counter)
    for r in rows:
        tags = tag_text(r["en_question"])
        r["tags"] = tags
        for t in tags:
            tag_count[t] += 1
            tag_by_mode[t][r["category_3b"]] += 1

    n = len(rows)
    print(f"both-fail instances: {n}\n")
    print(f"{'challenge tag':<20}{'count':>6}{'pct':>7}   3B-mode (WF/SF/CB)")
    print("-" * 64)
    for t, c in tag_count.most_common():
        m = tag_by_mode[t]
        modes = f"{m.get('WRONG_FORMULATION',0)}/{m.get('SOLVE_FAILED',0)}/{m.get('CODE_BUG',0)}"
        print(f"{t:<20}{c:>6}{c/n*100:>6.0f}%   {modes}")

    # write the tags back alongside the hardset for reuse
    out = args.hardset.replace(".jsonl", "_tagged.jsonl")
    with open(out, "w", encoding="utf-8") as fw:
        for r in rows:
            fw.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nTagged set -> {out}")


if __name__ == "__main__":
    main()
