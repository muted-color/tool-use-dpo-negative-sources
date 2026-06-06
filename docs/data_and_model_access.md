# Data and Model Access

This artifact release follows a download-script-only policy for sources whose
raw or processed redistribution is restricted or benchmark-sensitive.

## Datasets and Benchmarks

- BFCL: evaluation only; release aggregate metrics and hashes, not raw benchmark data.
- When2Call: keep train/test split separation; release aggregate metrics by default.
- FunctionChat-Bench: secondary diagnostic; release aggregate metrics only.
- xLAM/APIGen: gated Hugging Face source; do not publish raw or full processed pairs.
- ToolACE: Apache-2.0, but full processed pair release still requires contamination review.
- IFEval-style sources: guardrail check only; do not commit full prompt sets.

See `data_license_table.md` and `redistribution_policy.md` for the source-specific
rules used by the report.

## Models

The study used Qwen3-family checkpoints and LoRA adapters during local
experimentation. Adapter weights are not included in this GitHub artifact
repository. If model artifacts are later released separately, they should be
hosted in a model repository with SHA256 hashes and license metadata.

