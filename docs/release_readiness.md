# Release Readiness

This document summarizes the checks used before linking this repository from the
technical report.

## Artifact Scope

The repository is intended to support artifact-level reproduction of reported
tables, confidence intervals, contamination/overlap checks, and Pareto figures.
It is not a raw data release and does not include model or adapter weights.

## Required Public Checks

Run from the repository root:

```bash
python -m pip install -e '.[dev]'
python scripts/verify_artifacts.py
python scripts/verify_overlap.py
python scripts/reproduce_tables.py
python scripts/reproduce_figures.py
pytest
```

Optional grouped bootstrap recomputation:

```bash
python scripts/compute_grouped_bootstrap.py --bootstrap-iterations 1000
```

## Release Boundary

The public artifact repository includes aggregate results, sanitized per-example
metrics, hashes, manifests, and reproduction scripts. It excludes raw benchmark
prompts, raw generated outputs, full DPO pair files, private audit materials,
credentials, and model/adapter weights.

## Evidence Files

- `configs/artifact_manifest.json`: file sizes and SHA-256 hashes for released
  artifacts.
- `manifests/benchmark_manifest.yaml`: benchmark versions, slices, evaluator
  notes, parser settings, and bootstrap configuration.
- `docs/paper_manifest_summary.md`: paper-ready evaluation surface summary.
- `docs/contamination_overlap.md`: contamination and train-pool overlap scope.
- `docs/redistribution_policy.md`: release boundary and source-specific policy.
