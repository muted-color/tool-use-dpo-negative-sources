# Tool-Use DPO Negative Sources: Artifact Reproducibility

This repository is the public artifact companion for the arXiv technical report
on fixed-budget tool-use DPO negative sources, checkpoints, and Pareto trade-offs.

```text
Paper: A Fixed-Budget Empirical Study of Tool-Use DPO
Version: arXiv v1 / draft-v5-derived artifact packet
Base model family: Qwen3
Shared SFT reference: r004
Main DPO/control runs: r028, r029, s3d001, s3d002
Primary metrics: BFCL core, When2Call behavior accuracy, When2Call macro F1, IFEval prompt-strict
Main claim: fixed-budget source-native recipe comparison, not source-intrinsic causal ranking
```

The manuscript source is maintained separately under the project `paper/`
directory. This repository intentionally contains only the minimal public
artifacts needed to reproduce and verify the report's tables, bootstrap
summaries, and Pareto figures.

## What Is Included

- Aggregate Stage3d and Stage4 CSV/JSON artifacts used by the report.
- Bootstrap CI summaries for source-axis and clean-vs-unfiltered comparisons.
- Pareto point tables and a regenerated SVG figure.
- Contamination/overlap summaries released as aggregate hash-check artifacts.
- Run inventory, DPO/evaluation configuration notes, and benchmark/version notes.
- License, data access, redistribution, and claim-scope documentation.
- Verification scripts that check artifact presence and public-release hygiene.

## What Is Not Included

- The paper LaTeX source, bibliography, or build directory.
- Raw benchmark data or benchmark prompt text.
- Full processed DPO pair files such as `pairs_*.jsonl`.
- Raw per-example generation outputs derived from benchmark prompts.
- Private audit keys, `.env` files, RunPod secrets, API keys, or credentials.
- Model, LoRA, or adapter weights such as `*.safetensors`.

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
numbers and figures. Full DPO retraining is documented as an optional path for
users with the required GPU environment and upstream dataset access.

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

## Data Availability Statement

Due to licensing and redistribution constraints, some raw benchmark and training
examples are not redistributed. This repository provides run-level metadata,
sanitized evaluation outputs, aggregate metrics, bootstrap artifacts, and figure
generation scripts sufficient to verify the reported tables, confidence
intervals, and figures.
