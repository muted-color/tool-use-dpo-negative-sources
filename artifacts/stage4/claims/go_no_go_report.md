# s4r005 Go/No-Go Decision Report

Status: `complete`

Decision label: `continue_empirical_paper`

## Decision

Continue Stage4 as a workshop/arXiv empirical paper, but reset the paper around fixed-budget source/checkpoint Pareto trade-offs rather than semantic-filter superiority.

This decision does not authorize matched mini-DPO. Matched mini-DPO remains blocked until the Stage3b independent audit gate is repaired and passes.

## Rationale

Stage4 meets the continue threshold from the design criteria:

- Stage3b matched diagnostics show source-family differences under prompt control.
- Stage3d source-axis step50 comparisons show clear directional separation under bootstrap CI.
- Pareto points support reporting intended-axis gains together with IFEval guardrail regressions.
- r017n gives a concrete explanation for why self/weak negatives are risky: many validator-accepted rows are equivalent, ambiguous, or optional-default/no-op cases.

The strongest paper claim is not that filtering is better. The strongest claim is:

> Under a fixed DPO budget, negative source controls the primary improvement axis, and checkpoint selection controls the guardrail trade-off. Tool-use DPO should therefore be reported as a Pareto frontier over function-calling, call-decision behavior, and instruction-following regression.

## Evidence Summary

### Source-Axis Signal

The `source_axis_step50` comparisons are the strongest Stage3d evidence.

- Clean noised_gold vs behavior: BFCL core `+0.033333`, CI95 `[0.015337, 0.056667]`.
- Clean noised_gold vs behavior: When2Call behavior accuracy `-0.066667`, CI95 `[-0.107527, -0.030201]`.
- Clean noised_gold vs behavior: When2Call macro F1 `-0.053106`, CI95 `[-0.088470, -0.023391]`.
- Unfiltered noised_gold vs behavior: BFCL core `+0.026667`, CI95 `[0.010169, 0.048611]`.
- Unfiltered noised_gold vs behavior: When2Call behavior accuracy `-0.050000`, CI95 `[-0.086957, -0.013986]`.
- Unfiltered noised_gold vs behavior: When2Call macro F1 `-0.042067`, CI95 `[-0.074799, -0.012340]`.

Interpretation: structural negatives and behavior negatives move different axes. This supports a source-axis trade-off claim.

### Clean-vs-Unfiltered Signal

Clean-vs-unfiltered effects are not a good main claim.

- At step50, clean-vs-unfiltered differences are small and mostly include zero.
- At final, a few differences exclude zero, but they do not support a broad clean-DPO superiority claim.

Interpretation: semantic filtering should be treated as inconclusive or secondary under the current fixed-budget setup.

### Checkpoint Trade-Off

Step50 is the preferred reporting checkpoint for the current evidence.

- `r028` step50 beats final on BFCL core by `+0.020000`, CI95 `[0.003067, 0.038462]`.
- `s3d002` step50 beats final on BFCL core by `+0.020000`, CI95 `[0.006536, 0.036232]`.
- Several parse/SFT-dev comparisons also favor step50.
- Pareto points show final checkpoints often carry larger IFEval prompt-strict regression than step50.

Interpretation: checkpoint choice is a real reporting dimension, but the claim should stay secondary because behavior-axis final-vs-step50 results are mixed.

### Stage3b Mechanism

Stage3b supports source-quality diagnostics, not downstream matched-DPO conclusions.

- `r017j` repaired 1k strict numeric gates passed.
- `r017m` independent audit gate failed.
- `r017n` reject taxonomy shows reject rates of `0.05` for noised_gold, `0.45` for self, and `0.23` for weak_model.

Interpretation: Stage3b explains why some source families are risky, but matched mini-DPO is still not authorized.

## Go/No-Go Matrix

| Criterion | Result | Decision |
|---|---|---|
| Stage3b matched source differences are clear | Pass | Use as diagnostic support |
| Stage3d source-axis deltas visible under CI | Pass | Use as central evidence |
| Pareto plot separates source/checkpoint trade-offs | Pass with polish needed | Use as main framing |
| Step50-vs-final pattern repeated | Partial pass | Use as secondary claim |
| r017n taxonomy explains source risk | Pass | Use as mechanism |
| Semantic-filter superiority supported | Fail | Drop |
| Matched mini-DPO ready | Fail | Block |

## Authorized Scope

Authorized:

- Draft a paper/report around fixed-budget Pareto trade-offs in tool-use DPO.
- Use Stage3d source-axis bootstrap evidence as the primary quantitative result.
- Use Stage3b matched diagnostics and r017n taxonomy as mechanism/quality-risk evidence.
- Use step50 as the preferred checkpoint in main tables, with final/loss-best as a checkpoint-sensitivity result.

Not authorized:

- New Stage4 DPO training from this decision alone.
- Matched mini-DPO before the Stage3b independent audit gate passes.
- Claims that semantic filtering consistently improves downstream tool-use DPO.
- Claims that source-native Stage3d rows prove intrinsic source superiority.

## Required Paper Wording

Use:

- "source-axis Pareto trade-off"
- "fixed-budget tool-use DPO"
- "checkpoint-sensitive guardrail regression"
- "matched diagnostics suggest source-quality risks"

Avoid:

- "semantic filtering improves DPO"
- "clean DPO is better"
- "best source"
- "matched mini-DPO is ready"

## Next Steps

1. Update Stage4 status to `s4r005_go_no_go_complete_continue_empirical_paper`.
2. Draft the paper outline around the source-axis Pareto claim.
3. Add optional polish before drafting: complete provenance coverage for actual s4r002/s4r004 inputs and improve Pareto plots with FunctionChat and step50-vs-final arrows.
4. Keep matched mini-DPO blocked until the independent audit gate is repaired and passes.
