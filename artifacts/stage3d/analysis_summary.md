# s3d003 Analysis Summary

Status: `complete`

Generated: 2026-06-02T12:51:43+00:00

Primary package outputs are listed in `analysis_manifest.json`.

Key interpretation:

- `r028` and `r029` both remain `pass_with_tradeoff`.
- `checkpoint_step_0050` is the preferred trade-off candidate for both runs.
- final step 375 is loss-best but not downstream-best under guardrails.
- `r013`/`r014` are included only as contextual 5k unfiltered baselines.
- same-budget clean-vs-unfiltered deltas are available, but remain source-native rather than prompt/domain matched.
