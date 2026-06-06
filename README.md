# Tool-Use DPO Negative Sources: Reproducibility Artifacts

This repository contains the reproducibility artifacts for the technical report:

**A Fixed-Budget Empirical Study of Tool-Use DPO: Negative Sources, Checkpoints,
and Pareto Trade-offs**

```text
Artifact release: technical-report companion repository
Base model family: Qwen3
Shared SFT reference: r004
Main DPO/control runs: r028, r029, s3d001, s3d002
Primary metrics: BFCL core, When2Call behavior accuracy, When2Call macro F1, IFEval prompt-strict
Main claim: fixed-budget source-native recipe comparison, not source-intrinsic causal ranking
```

The scope is artifact-level reproduction: verifying the report's released
tables, bootstrap summaries, contamination/overlap checks, and Pareto figures
from aggregate and sanitized files.

Full DPO retraining and raw benchmark reconstruction are outside the default
public release scope because they require upstream dataset access, restricted
raw artifacts, and substantial GPU resources. The released scripts and artifacts
are intended to verify the reported results, not to serve as an end-to-end
training pipeline.

## Release Status

| Check | Status | Command or file |
|---|---:|---|
| Artifact manifest integrity | Pass | `python scripts/verify_artifacts.py` |
| Contamination/overlap release checks | Pass | `python scripts/verify_overlap.py` |
| Table reproduction | Supported | `python scripts/reproduce_tables.py` |
| Figure reproduction | Supported | `python scripts/reproduce_figures.py` |
| Grouped bootstrap recomputation | Supported | `python scripts/compute_grouped_bootstrap.py --bootstrap-iterations 1000` |
| Raw/private data exclusion policy | Documented | `docs/redistribution_policy.md` |

## What Is Included

- Aggregate Stage3d and Stage4 CSV/JSON artifacts used by the report tables.
- Sanitized per-example evaluation rows with prompt IDs/hashes, metric flags,
  generated-output hashes, and token counts.
- Pairwise and grouped bootstrap CI summaries.
- Pareto point tables, figure inputs, and regenerated SVG figures.
- Stage1/Stage2 contamination and Stage3d train-pool overlap summaries released
  as hash-only artifacts.
- Run inventory, DPO/evaluation configuration notes, benchmark versions, and
  exact evaluator/parser notes where recoverable from local artifacts.
- License, data access, redistribution, reference verification, and claim-scope
  documentation.
- Release-readiness notes for the report-linked artifact repository.
- Verification scripts for artifact integrity, release hygiene, tables, figures,
  and overlap checks.

## Data Boundary

The repository does not redistribute raw benchmark data, benchmark prompt text,
full processed DPO pair files, raw generated benchmark outputs, private audit
materials, credentials, or model/adapter weights. See
`docs/redistribution_policy.md` and `docs/data_availability_statement.md` for
the source-specific policy.

## Quick Start

```bash
python -m pip install -e '.[dev]'
python scripts/verify_artifacts.py
python scripts/verify_overlap.py
python scripts/compute_grouped_bootstrap.py --bootstrap-iterations 1000
python scripts/reproduce_tables.py
python scripts/reproduce_figures.py
pytest
```

The default reproducibility target is artifact-level reproduction of the report's
numbers and figures. Full DPO retraining is outside the default public release
scope and requires upstream dataset access, restricted raw artifacts, and
substantial GPU resources.

## Repository Layout

```text
artifacts/   Public aggregate artifacts used by the report
configs/     Run inventory, benchmark notes, and artifact manifest
results/     Sanitized per-example and aggregate evaluation outputs
docs/        Reproduction, data access, and claim-scope documentation
scripts/     User-facing reproduction and verification commands
src/         Python package used by the scripts
tests/       Lightweight artifact and script smoke tests
```

## Main Commands

```bash
python scripts/verify_artifacts.py
```

Checks required public artifacts, rejects raw/private/large forbidden files, and
writes a release hygiene summary.

```bash
python scripts/verify_overlap.py
```

Checks the released Stage1/Stage2 contamination reports and Stage3d train-pool
overlap summaries. To recompute from local private pair artifacts, run
`python scripts/verify_overlap.py --workspace-root .. --write-artifacts` from
the repository root.

```bash
python scripts/compute_grouped_bootstrap.py --bootstrap-iterations 1000
```

Recomputes grouped bootstrap CIs from sanitized per-example primary evaluation
outputs. The bootstrap unit is `prompt_id`; intervals are percentile CIs and
reflect evaluation-sample uncertainty only.

```bash
python scripts/reproduce_tables.py
```

Rebuilds compact derived tables from the included aggregate artifacts.

```bash
python scripts/reproduce_figures.py
```

Regenerates the public Pareto SVG from `artifacts/stage4/pareto/pareto_points.csv`.

## Evaluation Outputs

`results/per_example/` contains sanitized per-example evaluation outputs for
artifact-level verification. These files exclude prompt text, tool schemas,
generated text, and benchmark raw data. They retain prompt IDs/hashes, metric
components, correctness flags, parse/schema flags, behavior labels, and generated
output hashes.

`results/aggregate/` contains absolute and delta metrics used to trace the
reported point estimates.

## Citation

Use `CITATION.cff` for citation metadata. Dataset and benchmark attribution rules
are documented in `docs/data_license_table.md` and `docs/data_and_model_access.md`.

## Release Notes for Readers

- The released per-example files are sanitized: they do not include prompt text,
  tool schemas, generated text, or benchmark raw data.
- Bootstrap intervals use `prompt_id` as the grouped resampling unit with 1000
  iterations and percentile confidence intervals.
- Stage3d comparisons are fixed-budget, source-native recipe comparisons. They
  should not be read as source-intrinsic causal rankings.
- This repository verifies released results from sanitized artifacts; it is not
  an end-to-end raw-data preprocessing, DPO training, and inference pipeline.
- The public artifact manifest records file sizes and SHA-256 hashes in
  `configs/artifact_manifest.json`.
- The pre-release checklist is summarized in `docs/release_readiness.md`.

## Data Availability Statement

Due to licensing and redistribution constraints, some raw benchmark and training
examples are not redistributed. This repository provides run-level metadata,
sanitized evaluation outputs, aggregate metrics, bootstrap artifacts, and figure
generation scripts sufficient to verify the reported tables, confidence
intervals, and figures.
