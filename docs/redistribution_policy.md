# redistribution_policy.md

## Default Policy

Until licenses are verified, do not commit raw benchmark data, raw training data, generated completions derived from restricted prompts, or full processed DPO pair files.

Allowed during Stage0:

- small local smoke artifacts under `experiments/<exp_id>/artifacts/runs/<run_id>/`
- command provenance
- schemas
- hashes
- aggregate metrics
- manually written notes

Potentially public after review:

- dataset download / preparation scripts
- schema definitions
- synthetic noised-gold generator code
- aggregated tables
- a tiny sample pair file only if each source license allows it

## Required Before Public Release

- `docs/data_license_table.md` has no `todo` rows for used sources.
- `docs/model_license_table.md` has no `todo` rows for used models.
- benchmark test-set use restrictions are reflected in README/report wording.
- every released sample has source attribution and redistribution status.

## Source-Specific Release Rules

| Source | Stage1 release mode | Rule |
|---|---|---|
| BFCL | download_script_only | Use for evaluation only. Do not commit raw benchmark data or full generated outputs derived from benchmark prompts. Release aggregate metrics, hashes, commands, and tiny inspected examples only when needed. |
| When2Call | download_script_only | Keep train/test split separation. Do not commit full raw files. Derived behavior examples require attribution and split provenance. |
| FunctionChat-Bench | download_script_only | Treat as secondary OOD benchmark. Do not train/tune on benchmark prompts. Release aggregate metrics and tiny inspected examples only. |
| xLAM / APIGen function-calling 60k | download_script_only | Auto-gated HF source. Do not commit raw data or full processed DPO pairs. Release preparation scripts, hashes, attribution, and aggregate summaries. |
| ToolACE | releasable_with_review | Apache-2.0 permits redistribution with attribution, but full processed pair release still needs contamination and source-proportion review before public release. |
| Glaive function-calling v2 | releasable_with_review | Apache-2.0 permits redistribution with attribution. Optional SFT source; release only if source inclusion is frozen and contamination checks pass. |
| IFEval / MT-Bench-style subset | download_script_only | Regression check only. Keep benchmark prompts external; release aggregate metrics and scripts. |

## Generated Completion Rule

Generated completions inherit the practical release mode of their prompt source. If a prompt source is `download_script_only`, do not publish full generated completions or full DPO pairs derived from it; publish aggregate metrics, hashes, and small audited examples only when the source license and benchmark integrity allow it.

## Non-Negotiable

- Do not redistribute benchmark test sets by default.
- Do not publish full generated outputs if the source prompt license disallows derivatives.
- Do not hide license uncertainty in appendix; if uncertain, keep data download-script-only.
