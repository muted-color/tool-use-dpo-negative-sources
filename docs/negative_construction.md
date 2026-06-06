# Negative Construction and Filtering

The report compares source-native DPO recipes under a fixed pair and optimizer
budget.

## Sources

- `noised_gold`: structural negatives derived from gold tool calls, including
  wrong function, missing required argument, wrong required argument value, wrong
  call count, or material type/schema errors after canonicalization.
- `behavior`: behavior-oriented negatives for call-decision failures, including
  wrong call, no call, unnecessary follow-up, abstention, or answer-completion
  errors.
- `unfiltered` controls: same-budget source-native controls sampled before the
  high-confidence semantic-clean gate, with trainability-only exclusions.

## Clean Filtering

Rows are retained for clean DPO only when the rejected output is materially worse
than the chosen output under the provided tool schema and expected behavior.

Rows are dropped or quarantined when they are:

- unparsable or schema-invalid in a non-informative way
- equivalent to the chosen output after canonicalization
- acceptable alternatives
- ambiguous under the available schema
- optional/default/no-op differences
- chosen/reference suspect
- not verifiably worse than the chosen output

## Audit Gate

For each active clean source, at least 100 selected rows are audited with an
LLM-assisted holdout gate. The gate requires high accept rate, low
chosen/reference-suspect rate, and no repeated reject-taxonomy bucket dominating
the selected pool. These audits are quality-control gates, not human ground
truth.

