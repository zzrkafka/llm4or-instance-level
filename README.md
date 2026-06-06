# llm4or-instance-level

Toward **instance-level** optimization-model formulation with small, local LLMs.

LLM-for-OR systems today mostly formulate at the **problem level** — recognize a
problem class and apply a class template. This repo provides a lightweight,
fully offline, license-free harness to *measure* where that breaks and to isolate
the instances that a larger / fine-tuned model still cannot formulate — the
target for an instance-level method.

It reproduces the [ORLM](https://github.com/Cardinal-Operations/ORLM) evaluation
loop on a single 8 GB laptop GPU by swapping the heavy parts:

- inference: **Ollama + `qwen2.5:3b`** (4-bit) instead of a fine-tuned 7B/8B on vLLM
- solver: **PuLP + CBC** (open source) instead of licensed `coptpy`
- data: read **offline** from ORLM's reference result files

## Key results (qwen2.5:3b, greedy)

| Benchmark | n | pass@1 | formulation errors | code bugs |
|-----------|---|:------:|:---:|:---:|
| NL4OPT (academic) | 245 | 53.9% | 44.5% | 1.6% |
| IndustryOR (real-world) | 100 | 12.0% | 72.0% | 16.0% |

The bottleneck is **formulation, not code**; failure is **not predictable from
problem class**; and on real-world problems only **33%** of failures are
recovered by the fine-tuned 8B — the remaining **59 "both-fail" instances** are
the genuine instance-level target. Full analysis and the challenge taxonomy are
in [`mini/README.md`](mini/README.md).

## Setup

The scripts read ORLM's benchmark data from its reference result files, so place
this `mini/` folder inside an [ORLM](https://github.com/Cardinal-Operations/ORLM)
checkout (it expects `../results/<bench>/executed.jsonl`). Then:

```bash
pip install pulp requests          # + Ollama with: ollama pull qwen2.5:3b
python mini/run_mini.py --benchmark IndustryOR --n 100
python mini/analyze.py mini/full_industryor_3b.jsonl
python mini/hard_set.py --benchmark IndustryOR --pred mini/full_industryor_3b.jsonl
python mini/tag_hardset.py --hardset mini/hardset_IndustryOR.jsonl
```

## Credits

Built on **ORLM** (Cardinal Operations) for the benchmarks (NL4OPT, MAMO,
IndustryOR), the `q2mc` prompt protocol, and the reference 8B formulations used
for contrastive analysis.
