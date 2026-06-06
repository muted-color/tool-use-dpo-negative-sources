# Benchmark and Evaluator Notes

This file summarizes values recovered from local artifacts. It does not invent
missing revisions. The machine-readable source of truth is
`manifests/benchmark_manifest.yaml`.

## Frozen Eval Manifest

- Local source: `experiments/exp_02_stage1_target_sft_pilot/artifacts/runs/r002/eval_slice_manifest.jsonl`
- Snapshot metadata: `experiments/exp_02_stage1_target_sft_pilot/artifacts/runs/r002/dataset_snapshot.json`
- Total frozen eval rows in the manifest: `800`
- Public release mode: aggregate metrics plus sanitized per-example outputs

## Evaluation Surfaces

| Surface | Source snapshot | Slice | n | Evaluator/parser | Released per-example artifact |
|---|---|---|---:|---|---|
| BFCL | `gorilla-llm/Berkeley-Function-Calling-Leaderboard@61fc0608cfd831fcfbbaa676ebdfef0ed963eeda` | first 60 each from `BFCL_v3_simple`, `multiple`, `parallel`, `irrelevance`, `live_multiple` | 300 | `stage3d_eval.py` -> `stage1_candidate_eval.py`, `qwen3_tool_call_parser_stage0_policy` | `results/per_example/primary/*_<checkpoint>.csv` rows `task=bfcl` |
| When2Call | `nvidia/When2Call@0582f7749df63a96fdc3070932e83e72396ace53` | config `test`, split `mcq`, 100 each for `tool_call`, `follow_up`, `unable`, 0 `direct_answer` gold rows | 300 | `stage3d_eval.py` -> `stage1_candidate_eval.py` | `results/per_example/primary/*_<checkpoint>.csv` rows `task=when2call` |
| SFT-dev auxiliary | frozen Stage1 SFT-dev split | 351 `tool_call`, 93 `direct_answer`, 30 `follow_up`, 26 `unable` | 500 | `stage3d_eval.py` -> `stage1_candidate_eval.py` | `results/per_example/primary/*_<checkpoint>.csv` rows `task=sft_dev` |
| IFEval-style | `google/IFEval@966cd89545d6b6acfd7638bc708b98261ca58e84` | first 100 raw rows from `ifeval_input_data.jsonl`; 96 prompt-level rows with supported instructions | raw 100 / eval 96 | `stage3d_eval.py` -> `stage1_secondary_eval.py` | `results/per_example/ifeval/*_<checkpoint>.csv` |
| FunctionChat-Bench | `kakao/FunctionChat-Bench@5ddb0b5bb37d6423e1f3381ef693cda811a7847e` | 25 singlecall, 45 dialog, 30 call_decision | 100 | `stage3d_eval.py` -> `stage1_secondary_eval.py` | `results/per_example/functionchat/*_<checkpoint>.csv` |

## Parser and Decoding

- Generation uses deterministic decoding (`do_sample=False`).
- `enable_thinking=false` is recorded in the frozen Stage1 eval config.
- Tool-call parser policy: `qwen3_tool_call_parser_stage0_policy`.
- Parser modes:
  - strict: `strict_tool_call_block`, `strict_full_json`
  - permissive: `permissive_json_substring`
  - failures include `missing_parseable_tool_call`, JSON decode errors, or JSON without a tool-call shape
- `strict_parse_success` is true only for strict parser modes.

## Bootstrap

- Public artifact: `artifacts/stage4/bootstrap/pairwise_bootstrap_ci.csv`
- Recompute command: `python scripts/compute_grouped_bootstrap.py --bootstrap-iterations 1000`
- Unit: `prompt_id`
- Iterations: `1000`
- CI type: percentile
- Seed rule: `20260603 + comparison_metric_index * 97`
- Scope: evaluation-sample uncertainty only; does not include training-seed, DPO stochasticity, or independently resampled data-pool variance.

## Recovered FunctionChat-Bench Snapshot

- Stage1 originally recorded FunctionChat-Bench as `github_main_2026-05-28` because the loader read `https://raw.githubusercontent.com/kakao/FunctionChat-Bench/main/data/*.jsonl` directly.
- A post-hoc GitHub history check matched the frozen 100-row `eval_slice_manifest.jsonl` canonical row hashes against upstream files.
- Matching snapshot: `kakao/FunctionChat-Bench@5ddb0b5bb37d6423e1f3381ef693cda811a7847e`.
- The same selected rows are data-equivalent at `cb32af378a2b94ee84fc4d3cb50302377c7ff679` and `dfa59f64392ffc6373dfb4a336b631c11be3ec5e`; the recorded raw-`main` date resolves to `5ddb0b5bb37d6423e1f3381ef693cda811a7847e`.

## Values Not Recoverable From Current Artifacts

- Separate deterministic eval sampling seed: not recoverable; evaluation uses deterministic decoding and a frozen hash manifest.
