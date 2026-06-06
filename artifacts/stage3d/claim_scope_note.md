# Stage3d Claim Scope Note

Generated: 2026-06-02T12:51:43+00:00

## Decision

Stage3d supports a narrow claim: high-confidence clean DPO moves the intended source-aligned axis under a 3k equal-example budget. It does not support a general improvement claim, a source-intrinsic ranking claim, or a clean-vs-unfiltered causal claim.

The preferred Stage3d checkpoints are the step 50 adapters, not the final loss-best adapters:

| Run | Preferred adapter | Intended-axis delta | Key remaining guardrail |
|---|---|---:|---:|
| `r028` noised_gold clean | `checkpoint_step_0050` | BFCL core +0.046667 | IFEval prompt strict -0.062500 |
| `r029` behavior clean | `checkpoint_step_0050` | When2Call macro F1 +0.048644 | IFEval prompt strict -0.052083 |

Both runs saturated by step 50. The final step 375 adapters improve DPO eval loss but worsen downstream guardrails. This is evidence that DPO loss best step is not downstream best step for Stage3d.

## Same-Budget Clean-vs-Unfiltered Controls

Both same-budget unfiltered controls are complete: `s3d001` for noised_gold and `s3d002` for behavior. The comparison is now available in `clean_vs_unfiltered_delta.csv`, but it remains source-native rather than prompt/domain matched.

At step 50:

| Source | Clean run | Unfiltered run | Intended-axis clean delta | Intended-axis unfiltered delta | Clean minus unfiltered |
|---|---|---|---:|---:|---:|
| noised_gold | `r028` | `s3d001` | BFCL core +0.046667 | BFCL core +0.043333 | +0.003333 |
| behavior | `r029` | `s3d002` | When2Call macro F1 +0.048644 | When2Call macro F1 +0.043106 | +0.005538 |

Current interpretation: noised_gold clean and unfiltered step-50 results are near-tied, and behavior clean is modestly ahead of behavior unfiltered on the intended behavior axis. This supports at most a narrow same-budget observation, not a broad semantic-filter superiority claim.

## Allowed Claims

- `r028 checkpoint_step_0050` improves structural/tool-call metrics versus `r004`, especially BFCL core and BFCL parallel, with lower guardrail damage than final step 375.
- `r029 checkpoint_step_0050` improves the intended behavior axis versus `r004`, especially When2Call behavior accuracy and macro F1, with lower guardrail damage than final step 375.
- Stage3d clean DPO shows source-aligned effects, with an explicit dataset/task-family confound caveat.
- Early stopping/checkpoint selection is required for defensible downstream interpretation.

## Disallowed Claims

- No general positive clean DPO claim: both preferred checkpoints still exceed the 0.05 IFEval prompt-strict regression threshold or are too close to treat as clean pass.
- No broad clean-vs-unfiltered causal claim: same-budget controls are complete, but rows remain source-native and not prompt/domain matched.
- No full source ranking or intrinsic source superiority claim.
- No claim that behavior and noised_gold are prompt-matched or domain-matched; they are source-native and task-family confounded.
- No claim that Stage3a `r013`/`r014` prove clean-vs-unfiltered effects; those are 5k/625-step contextual baselines.

## Recommended Reporting Sentence

Stage3d clean DPO produces source-aligned improvements under a 3k equal-example budget, but both high-confidence clean sources show instruction-following guardrail regression. Early checkpoint selection at step 50 substantially improves the trade-off versus final-step selection. Same-budget controls show no clear noised_gold semantic-filter advantage and a modest behavior clean advantage on the intended behavior axis, with the prompt/domain matching caveat.
