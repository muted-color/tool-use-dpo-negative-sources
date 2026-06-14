# Reporting Tool-Use DPO Under Fixed Budgets

Artifact repository for the technical report:

**Reporting Tool-Use DPO Under Fixed Budgets: Recipe--Checkpoint Profiles and
Guardrail Trade-offs**

This repository is the public verification package for the report. Its goal is
narrow: make the report's tables, confidence intervals, overlap checks, and
Pareto figures easy to verify from released artifacts.

## At a glance

- Verifies the report tables, confidence intervals, overlap checks, and Pareto
  inputs from released artifacts.
- Supports artifact-level reproduction only.
- Excludes raw benchmark prompts, full DPO pair files, model weights, and
  adapters.
- Keeps internal trace IDs in `docs/evidence_map.md`.

This is not an end-to-end training release. Full DPO retraining and raw
benchmark reconstruction require upstream dataset access, restricted raw
artifacts, and substantial GPU resources, so they are outside the default public
scope.

## What This Repository Verifies

| Report evidence | Purpose | Start here |
|---|---|---|
| Source-axis recipe profile | BFCL and When2Call deltas for clean structural vs behavior-oriented negatives | `artifacts/stage4/bootstrap/pairwise_bootstrap_ci.csv` |
| Clean-vs-unfiltered controls | Same-budget filtering comparison | `artifacts/stage4/bootstrap/pairwise_bootstrap_ci.csv` |
| Checkpoint and guardrail trade-off | IFEval prompt-strict deltas and Pareto inputs | `artifacts/stage4/pareto/`, `artifacts/stage4/bootstrap/ifeval_prompt_strict_bootstrap_ci.csv` |
| Pair-quality diagnostics | LLM-audited source-risk summaries and claim scope | `artifacts/stage4/stage3b/`, `docs/claims_and_limitations.md` |
| Mixed-source appendix ablation | Post-hoc mixed-source sanity check | `artifacts/stage5/mixed_source/` |
| Training-seed stability | Fixed-pair-pool source-axis sign stability | `artifacts/stage6/multiseed/` |
| Direct-answer coverage audit | Public When2Call direct-answer coverage limitation | `artifacts/stage7/direct_answer/`, `docs/direct_answer_coverage.md` |
| Independent pair-pool robustness | One pool-B replicate for the two main clean conditions | `artifacts/stage8/data_sampling/` |

Internal run IDs are retained for traceability only. They are not intended to be
the public claim names; see `docs/evidence_map.md` for the trace mapping.

## What You Can Check

| Check | Status | Command or file |
|---|---:|---|
| Artifact manifest integrity | Pass | `python scripts/verify_artifacts.py` |
| Contamination/overlap release checks | Pass | `python scripts/verify_overlap.py` |
| Table reproduction | Supported | `python scripts/reproduce_tables.py` |
| Figure reproduction | Supported | `python scripts/reproduce_figures.py` |
| Grouped bootstrap recomputation | Supported | `python scripts/compute_grouped_bootstrap.py --bootstrap-iterations 1000` |
| IFEval bootstrap recomputation | Supported | `python scripts/compute_ifeval_bootstrap.py --bootstrap-iterations 1000` |
| Raw/private data exclusion policy | Documented | `docs/redistribution_policy.md` |

## Contents

- Aggregate CSV/JSON results used in the report tables.
- Sanitized per-example evaluation rows: prompt IDs and hashes, metric flags,
  generated-output hashes, and token counts.
- Pairwise and grouped bootstrap summaries.
- Pareto point tables, figure inputs, and regenerated SVG figures.
- Mixed-source appendix ablation summaries.
- Multi-seed source-axis sign-stability summaries.
- Direct-answer coverage audit and auxiliary direct-answer diagnostics.
- Independent pair-pool data-sampling robustness summaries.
- Hash-only contamination and train-pool overlap reports.
- Run inventory, benchmark versions, DPO/evaluation config notes, and recovered
  evaluator/parser details.
- Data access, license, redistribution, reference, and claim-scope notes.
- Small scripts for checking the artifacts and regenerating tables/figures.

## Data Boundary

Raw benchmark data, benchmark prompt text, full processed DPO pairs, raw
generated benchmark outputs, private audit materials, credentials, and
model/adapter weights are not redistributed here. See
`docs/redistribution_policy.md` and `docs/data_availability_statement.md`.

## Quick Start

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

These commands reproduce the released tables, bootstrap summaries, and figure
inputs from the files in this repository.

## Repository Layout

```text
artifacts/   Public aggregate artifacts used by the report
configs/     Run inventory, benchmark notes, and artifact manifest
results/     Sanitized per-example and aggregate evaluation outputs
docs/        Reproduction, data access, and claim-scope documentation
scripts/     Reproduction and verification commands
src/         Python package used by the scripts
tests/       Lightweight smoke tests
```

## Main Commands

```bash
python scripts/verify_artifacts.py
```

Checks the artifact manifest and rejects raw/private files that should not be in
the public release.

```bash
python scripts/verify_overlap.py
```

Checks the released contamination reports and fixed-budget train-pool overlap
summaries. If the private pair artifacts are available locally, they can be
recomputed with:

```bash
python scripts/verify_overlap.py --workspace-root .. --write-artifacts
```

```bash
python scripts/compute_grouped_bootstrap.py --bootstrap-iterations 1000
```

Recomputes grouped bootstrap CIs from sanitized per-example primary evaluation
outputs. The bootstrap unit is `prompt_id`; intervals are percentile CIs.

```bash
python scripts/compute_ifeval_bootstrap.py --bootstrap-iterations 1000
```

Recomputes IFEval prompt-strict CIs from sanitized per-example IFEval outputs.
The denominator excludes zero-supported prompts, matching the paper metric.

```bash
python scripts/reproduce_tables.py
```

Rebuilds compact derived tables from the included aggregate artifacts.

```bash
python scripts/reproduce_figures.py
```

Regenerates the public Pareto SVG from `artifacts/stage4/pareto/pareto_points.csv`.

## Evaluation Outputs

`results/per_example/` contains sanitized per-example evaluation outputs. The
files keep prompt IDs/hashes, metric components, parse/schema flags, behavior
labels, token counts, and generated-output hashes. They do not include prompt
text, tool schemas, generated text, or benchmark raw data.

`results/aggregate/` contains absolute and delta metrics used to trace the
reported point estimates.

`docs/evidence_map.md` maps paper-facing evidence names to public artifact
paths, internal trace IDs, and interpretation boundaries.

## Citation

Use `CITATION.cff` for citation metadata. Dataset and benchmark attribution
notes are in `docs/data_license_table.md` and `docs/data_and_model_access.md`.

## Notes

- Bootstrap intervals use `prompt_id` as the grouped resampling unit with 1000
  iterations.
- The main recipe comparisons are fixed-budget, source-native comparisons. They
  should not be read as source-intrinsic causal rankings.
- `configs/artifact_manifest.json` records file sizes and SHA-256 hashes for the
  released files.
- The pre-release checklist is summarized in `docs/release_readiness.md`.

## Data Availability Statement

Some raw benchmark and training examples cannot be redistributed because of
license and benchmark-integrity constraints. This repository provides the
metadata, sanitized outputs, aggregate metrics, bootstrap artifacts, and figure
scripts needed to verify the reported results.
