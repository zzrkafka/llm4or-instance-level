# llm4or-instance-level

Toward **instance-level** optimization-model formulation with small, local LLMs.

LLM-for-OR systems today mostly formulate at the **problem level** — recognize a
problem class and apply a class template. This repo provides a lightweight,
fully **offline, license-free** harness that reproduces ORLM's *natural language →
optimization model → solve → score* loop on a single **8 GB laptop GPU**, then
turns the results into evidence for a research question:

> Is the real bottleneck the problem *class*, or the *instance*? This harness
> measures it and isolates the instances that a bigger/fine-tuned model still
> cannot formulate — the target for an instance-level method.

## 1. Why this exists (constraints → design)

The upstream [ORLM](https://github.com/Cardinal-Operations/ORLM) stack needs a
fine-tuned 7B/8B served by vLLM and a licensed `coptpy` solver — neither fits an
8 GB RTX 4060 laptop. We keep ORLM's evaluation protocol but swap the heavy parts:

| Stage | Upstream ORLM | This harness |
|-------|---------------|--------------|
| Model | fine-tuned 7B/8B + vLLM | **Ollama + `qwen2.5:3b`** (4-bit, ~2 GB) |
| Solver | `coptpy` (license) | **PuLP + CBC** (open, no license) |
| Data | HuggingFace download | **offline** from `results/<bench>/executed.jsonl` |
| Scoring | execution-based, 5% tol | identical logic (`eval/execute.py` semantics) |

The prompt template is ORLM's `q2mc_en`, retargeted to PuLP. The model is a
general 3B instruct model (no fine-tuning) — so absolute accuracy is *not*
comparable to ORLM's paper numbers; the goal is the **failure structure**, which
is robust to model choice.

## 2. Harness robustness (so failures reflect modeling, not plumbing)

Small general models emit messy code; without care, cosmetic bugs masquerade as
modeling errors. The executor therefore:

- prepends `from pulp import *` (models often under-import);
- runs the model's code in an **isolated namespace under try/except**, so a buggy
  *post-solve* print line never discards an already-solved `prob`;
- handles the `"No Best Solution"` string ground truth (infeasible instances);
- wraps every item in try/except so one bad instance can't kill a long run.

This is what lets us cleanly separate **WRONG_FORMULATION** / **SOLVE_FAILED**
from mere **CODE_BUG**.

## 3. Setup & usage

The scripts read ORLM's benchmark data from its reference result files, so place
this `mini/` folder inside an [ORLM](https://github.com/Cardinal-Operations/ORLM)
checkout (it expects `../results/<bench>/executed.jsonl`). Then:

```bash
pip install pulp requests          # + Ollama, then: ollama pull qwen2.5:3b

# run a benchmark (NL4OPT | IndustryOR | MAMO_EasyLP | MAMO_ComplexLP)
python mini/run_mini.py --benchmark IndustryOR --n 100 --model qwen2.5:3b

# attribute failures into 4 categories
python mini/analyze.py mini/full_industryor_3b.jsonl

# per-instance contrast: where 3B is wrong but ORLM-8B (reference) is right
python mini/compare.py --benchmark IndustryOR --pred mini/full_industryor_3b.jsonl

# curate the "both-fail" set (3B wrong AND 8B wrong) and tag it by challenge type
python mini/hard_set.py --benchmark IndustryOR --pred mini/full_industryor_3b.jsonl
python mini/tag_hardset.py --hardset mini/hardset_IndustryOR.jsonl
```

## 4. Results (qwen2.5:3b, greedy)

| Benchmark | n | pass@1 | WRONG_FORMULATION | SOLVE_FAILED | CODE_BUG |
|-----------|---|:------:|:---:|:---:|:---:|
| NL4OPT (academic) | 245 | **53.9%** | 23.7% | 20.8% | 1.6% |
| IndustryOR (real-world) | 100 | **12.0%** | 29.0% | 43.0% | 16.0% |

## 5. Findings

1. **The bottleneck is formulation, not code generation.** On NL4OPT, modeling
   errors (WRONG_FORMULATION + SOLVE_FAILED = 44.5%) dwarf pure code bugs (1.6%).

2. **Failure is not predictable from surface problem class.** Splitting NL4OPT by
   presence of ratio/percentage constraints gave 53.7% vs 54.0% — no signal.
   Whether an instance is formulated correctly depends on the *instance*, not its
   nominal class. This argues directly for an instance-level view.

3. **Academic benchmarks overstate capability.** pass@1 collapses 53.9% → 12.0%
   from NL4OPT to real-world IndustryOR; SOLVE_FAILED (infeasible/unbounded
   models) jumps to 43% — a concrete, measurable failure mode to target.

4. **Scale/fine-tuning has a ceiling.** Among 3B failures, the share the
   fine-tuned ORLM-8B *recovers* drops from **76%** (NL4OPT, 86/113) to **33%**
   (IndustryOR, 29/88). The remaining **59 IndustryOR "both-fail" instances** are
   wrong for *both* a small model and a fine-tuned 8B — not solved by "use a
   bigger model", and the genuine target for an instance-level method.

## 6. The both-fail challenge taxonomy (instance-level target list)

59 IndustryOR instances where 3B and ORLM-8B both fail. 3B failure modes within
the set: WRONG_FORMULATION 16 / SOLVE_FAILED 34 / CODE_BUG 9 — i.e. on genuinely
hard instances the dominant symptom is producing an **infeasible/unbounded
model**. Heuristic multi-label tags (counts; 3B mode = WF/SF/CB):

| Challenge tag | share | 3B mode (WF/SF/CB) |
|---------------|:-----:|:---:|
| TABLE_DATA (params in tables) | 56% | 8/23/2 |
| NETWORK/TRANSPORT | 41% | 4/14/6 |
| INTEGER/COUNT | 37% | 4/12/6 |
| MULTI_PERIOD/TIME | 34% | 5/12/3 |
| ASSIGN/SCHEDULE | 15% | 3/5/1 |
| UNIT_CONVERSION | 10% | 1/5/0 |
| RATIO/PERCENT | 10% | 1/5/0 |
| MIN_MAX/MAKESPAN | 2% | 1/0/0 |

Read: hard instances overwhelmingly carry **tabular parameter data** and
**network / multi-period / integer** structure, and the model's failure is
overwhelmingly to emit an unsolvable model — i.e. it mis-maps the instance's
entities/constraints, not merely its syntax.

**Illustrative case (CPU scheduling, both fail):** a makespan (min-max) problem
with parameters in a table that is internally inconsistent ("10 tasks" in prose,
7 in the table) and an implicit unit conversion (time = instructions / frequency).
Correct modeling needs binary assignment + an auxiliary makespan variable
`T ≥ load(j) ∀ machine j`, `min T`. Neither model applied it. This is an
instance-level reasoning failure: structure recognition + messy-data parsing +
implicit conversion, none recoverable by class-template matching.

## 7. Limitations

- 3B + quantization + PuLP swap → absolute accuracy ≠ ORLM paper numbers (by
  design; we study failure structure).
- Section 6 tags are keyword heuristics (a triage), not hand-verified labels.
- "ORLM-8B correct/wrong" uses the repo's stored reference executions.

## 8. File index

| File | Purpose |
|------|---------|
| `mini/run_mini.py` | inference (Ollama) → solve (PuLP/CBC) → score; 4 benchmarks |
| `mini/analyze.py` | 4-way failure attribution |
| `mini/compare.py` | per-instance 3B-wrong vs ORLM-8B-right contrast |
| `mini/hard_set.py` | curate the both-fail set (+ formulations) |
| `mini/tag_hardset.py` | tag the both-fail set by challenge type |
| `mini/full_*_3b.jsonl` | raw run results |
| `mini/hardset_IndustryOR*.{jsonl,md}` | curated both-fail set (the research target) |
| `mini/contrast_*.md` | weak-wrong vs strong-correct formulation pairs |

## Credits

Built on **ORLM** (Cardinal Operations) for the benchmarks (NL4OPT, MAMO,
IndustryOR), the `q2mc` prompt protocol, and the reference 8B formulations used
for contrastive analysis.
