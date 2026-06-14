# Evidence Map

This document is for audit and reproduction tracking. It maps the public
evidence names used in the README and report to released artifacts and internal
trace IDs. The trace IDs are kept to make results auditable, but the public
claim names should follow the report evidence names.

| Report evidence | Public interpretation | Primary artifacts | Trace IDs |
|---|---|---|---|
| Source-axis recipe profile | Clean structural negatives and clean behavior-oriented negatives move different evaluation axes under the same fixed DPO budget. | `artifacts/stage4/bootstrap/pairwise_bootstrap_ci.csv`, `results/aggregate/main_metrics_absolute.csv` | `r028`, `r029` |
| Clean-vs-unfiltered controls | Same-budget unfiltered controls test whether semantic filtering itself gives a broad downstream gain. | `artifacts/stage4/bootstrap/pairwise_bootstrap_ci.csv`, `artifacts/stage3d/clean_vs_unfiltered_delta.csv` | `s3d001`, `s3d002` |
| Checkpoint and guardrail trade-off | Preferred early checkpoints are reported with IFEval prompt-strict guardrail movement rather than only intended-axis gains. | `artifacts/stage4/pareto/pareto_points.csv`, `artifacts/stage4/bootstrap/ifeval_prompt_strict_bootstrap_ci.csv` | `r028`, `r029`, `s3d001`, `s3d002` |
| Pair-quality diagnostics | Rejected-output source quality is audited as diagnostic evidence, not as human ground truth or downstream matched-DPO proof. | `artifacts/stage4/stage3b/`, `docs/audit_rubric.md`, `docs/claims_and_limitations.md` | Diagnostic audit (Stage3b) |
| Mixed-source appendix ablation | A same-budget mixed-source run is included as appendix evidence and does not replace the source-axis profile. | `artifacts/stage5/mixed_source/` | `s5r002` |
| Training-seed stability | Additional seeds check whether the main source-axis sign pattern is stable for fixed pair pools. | `artifacts/stage6/multiseed/` | `s6r002`-`s6r005` |
| Direct-answer coverage audit | Public When2Call labeled configs used here do not expose direct-answer gold rows, so direct-answer behavior remains a limitation. | `artifacts/stage7/direct_answer/`, `docs/direct_answer_coverage.md` | Coverage audit (Stage7) |
| Independent pair-pool robustness | One independently reconstructed pool-B replicate checks whether the main clean source-axis signs persist under pair resampling. | `artifacts/stage8/data_sampling/` | `s8r005`, `s8r006` |

## Scope Boundaries

- The repository supports artifact-level reproduction: tables, confidence
  intervals, overlap checks, and figure inputs.
- It does not redistribute raw benchmark prompts, full generated outputs, full
  DPO pair files, private audit materials, model weights, or adapters.
- Stage and run identifiers are implementation trace keys. They should not be
  read as additional public claims beyond the evidence map above.
- The independent pair-pool robustness evidence supports one scoped replicate
  for the two main clean conditions. It is not broad distribution robustness and
  not a source-intrinsic ranking.
