# Reproduction Guide

## Artifact-Level Reproduction

This is the default public reproduction target. It verifies the reported tables,
confidence intervals, overlap checks, and figures from aggregate and sanitized
artifacts. It does not reconstruct raw benchmark data, regenerate full DPO pair
files, retrain adapters, or rerun the full inference pipeline from raw prompts.

```bash
python -m pip install -e '.[dev]'
python scripts/verify_artifacts.py
python scripts/verify_overlap.py
python scripts/compute_grouped_bootstrap.py --bootstrap-iterations 1000
python scripts/reproduce_tables.py
python scripts/reproduce_figures.py
pytest
```

Generated files are written under `reproduced/`, which is intentionally ignored
by Git.

## Expected Outputs

- `reproduced/tables/source_axis_step50.csv`
- `reproduced/tables/clean_vs_unfiltered_step50.csv`
- `reproduced/tables/pareto_summary.csv`
- `reproduced/tables/absolute_scores.csv`
- `reproduced/tables/budget_accounting.csv`
- `reproduced/tables/functionchat_transfer.csv`
- `reproduced/tables/source_risk.csv`
- `reproduced/figures/pareto_2panel.svg`
- `reproduced/bootstrap/pairwise_bootstrap_ci.csv`

The public overlap command verifies included aggregate reports only. To
recompute those reports from local private pair artifacts, use:

```bash
python scripts/verify_overlap.py --workspace-root .. --write-artifacts
```

## Required Public Commands

Install:

```bash
python -m pip install -e '.[dev]'
```

Verify artifact manifest and release hygiene:

```bash
python scripts/verify_artifacts.py
```

Verify released contamination/overlap reports:

```bash
python scripts/verify_overlap.py
```

Recompute grouped bootstrap from sanitized per-example primary eval outputs:

```bash
python scripts/compute_grouped_bootstrap.py --bootstrap-iterations 1000
```

Reproduce compact tables:

```bash
python scripts/reproduce_tables.py
```

Reproduce Pareto figure:

```bash
python scripts/reproduce_figures.py
```

Run smoke tests:

```bash
pytest
```

## Full Training Path

Full DPO retraining is outside the default public release scope. It requires:

- access to upstream datasets and benchmarks under their own terms
- access to restricted raw artifacts that are not redistributed here
- a CUDA-capable GPU environment
- Qwen3 model access from Hugging Face
- regeneration of source-native pair pools under the documented filters

The included aggregate and sanitized artifacts are sufficient to verify the
technical report's reported tables, bootstrap summaries, overlap checks, and
Pareto figure inputs.
