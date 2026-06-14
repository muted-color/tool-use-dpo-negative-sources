# Release Readiness

This document summarizes the checks used before linking this repository from the
technical report.

## Artifact Scope

The repository is intended to support artifact-level reproduction of reported
tables, confidence intervals, contamination/overlap checks, and Pareto figures.
It is not a raw data release and does not include model or adapter weights.

Full DPO retraining and raw benchmark reconstruction are outside the default
public release scope because they require upstream dataset access, restricted
raw artifacts, and substantial GPU resources.

## Required Public Checks

Run from the repository root:

```bash
python -m pip install -e '.[dev]'
python scripts/verify_artifacts.py
python scripts/verify_overlap.py
python scripts/compute_grouped_bootstrap.py --bootstrap-iterations 1000
python scripts/compute_ifeval_bootstrap.py --bootstrap-iterations 1000
python scripts/reproduce_tables.py
python scripts/reproduce_figures.py
pytest
```

The bootstrap commands regenerate the released pairwise and IFEval prompt-strict
confidence-interval CSV files from sanitized per-example outputs.

## Release Boundary

The public artifact repository includes aggregate results, sanitized per-example
metrics, hashes, manifests, and reproduction scripts. It excludes raw benchmark
prompts, raw generated outputs, full DPO pair files, private audit materials,
credentials, and model/adapter weights.

The repository should therefore be cited as a result-verification artifact
repository, not as a complete end-to-end training pipeline.

## Evidence Files

- `README.md`: public entrypoint and evidence overview.
- `docs/evidence_map.md`: public evidence names, artifact paths, trace IDs, and
  interpretation boundaries.
- `docs/reproduction.md`: artifact-level reproduction commands and expected
  outputs.
- `configs/artifact_manifest.json`: file sizes and SHA-256 hashes for released
  artifacts.
- `manifests/benchmark_manifest.yaml`: benchmark versions, slices, evaluator
  notes, parser settings, and bootstrap configuration.
- `docs/paper_manifest_summary.md`: paper-ready evaluation surface summary.
- `docs/contamination_overlap.md`: contamination and train-pool overlap scope.
- `docs/redistribution_policy.md`: release boundary and source-specific policy.
- Supporting evidence artifact directories under `artifacts/`: fixed summaries
  for appendix ablations, seed stability, coverage diagnostics, and pair-pool
  robustness.
