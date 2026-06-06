# Contamination and Overlap Checks

This public artifact records aggregate-only overlap evidence. It intentionally
does not publish raw prompts, tool schemas, full processed DPO pairs, or
generated benchmark text.

## Released Artifact

- `artifacts/stage4/claims/overlap_check_summary.csv`
- `artifacts/stage4/claims/stage1_contamination_report.json`
- `artifacts/stage4/claims/stage2_contamination_report.json`
- `artifacts/stage4/claims/stage3d_train_pool_overlap_report.json`
- `artifacts/stage4/claims/stage3d_train_pool_overlap_summary.csv`

## Scope

- Stage1 SFT-vs-evaluation contamination check: exact hash overlap counts are
  zero for prompt ID, normalized user utterance, normalized tool schema, and
  combined user-plus-schema hashes.
- Stage2 accepted prompt pool after filtering: exact hash overlap counts are
  zero for prompt ID, normalized user utterance, normalized tool schema, and
  combined user-plus-schema hashes. Excluded candidate counts are reported.
- Stage3d final selected DPO train pools for `r028`, `r029`, `s3d001`, and
  `s3d002`: exact hash overlap counts are zero against the frozen eval slice,
  SFT-dev manifest rows, and the full Stage1 SFT manifest.

## Recompute Command

The public command checks the included aggregate reports:

```bash
python scripts/verify_overlap.py
```

The recomputation path requires local private pair artifacts that are not
redistributed:

```bash
python scripts/verify_overlap.py --workspace-root .. --write-artifacts
```

These checks support the paper's hash-based overlap statement. They do not prove
semantic near-duplicate absence, and they do not replace upstream benchmark
license and redistribution constraints.
