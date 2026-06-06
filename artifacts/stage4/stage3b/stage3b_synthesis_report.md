# s4r004 Stage3b Matched Diagnostic Synthesis

Status: `complete`

Stage3b is diagnostic evidence, not downstream DPO evidence.

Key interpretation:

- Existing matched diagnostics show source differences under prompt control.
- Repaired 1k strict numeric gates pass in `r017j`.
- The independent audit gate remains failed in `r017m`.
- `r017n` shows many validator-accepted self/weak rows are GPT-5.5-equivalent, ambiguous, or optional-default/no-op cases.
- Therefore matched mini-DPO is still not authorized as a clean downstream experiment.
