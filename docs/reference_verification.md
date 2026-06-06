# Reference Verification Records

Last checked: 2026-06-05

This file records bibliography identifiers for `report/stage4_pareto_paper_draft_v5.md`. It is kept outside the paper draft so the public manuscript can keep only the References section.

| Paper or resource | Verified record | Identifier | URL |
|---|---|---|---|
| Direct Preference Optimization | arXiv record | `arXiv:2305.18290` | https://arxiv.org/abs/2305.18290 |
| BFCL technical report | UC Berkeley EECS technical report | `UCB/EECS-2025-184` | https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-184.html |
| BFCL ICML paper / leaderboard | ICML 2025, PMLR 267:48371-48392 | `pmlr-v267-patil25a` | https://proceedings.mlr.press/v267/patil25a.html |
| When2Call | ACL Anthology, NAACL 2025 | `2025.naacl-long.174`, DOI `10.18653/v1/2025.naacl-long.174` | https://aclanthology.org/2025.naacl-long.174/ |
| DiaTool-DPO | ACL Anthology, SIGDIAL 2025 | `2025.sigdial-1.32` | https://aclanthology.org/2025.sigdial-1.32/ |
| API-Bank | ACL Anthology, EMNLP 2023 | `2023.emnlp-main.187`, DOI `10.18653/v1/2023.emnlp-main.187` | https://aclanthology.org/2023.emnlp-main.187/ |
| ToolLLM / ToolBench | OpenReview ICLR 2024 spotlight and arXiv record | `arXiv:2307.16789` | https://openreview.net/forum?id=dHng2O0Jjr, https://arxiv.org/abs/2307.16789 |
| FunctionChat-Bench | arXiv record | `arXiv:2411.14054` | https://arxiv.org/abs/2411.14054 |
| Provably Robust DPO | arXiv record | `arXiv:2403.00409` | https://arxiv.org/abs/2403.00409 |
| What Matters in Data for DPO? | arXiv record | `arXiv:2508.18312` | https://arxiv.org/abs/2508.18312 |

## BFCL Citation Roles

Use Yan (2025) for the UC Berkeley technical-report description of BFCL benchmark components and validation design. Use Patil et al. (2025) for the ICML/PMLR paper and public leaderboard framing.

## FunctionChat-Bench Snapshot Recovery

Stage1 loaded FunctionChat-Bench from `https://raw.githubusercontent.com/kakao/FunctionChat-Bench/main/data/*.jsonl` and recorded the source as `github_main_2026-05-28`.
The exact commit was recovered post hoc by comparing the frozen 100-row `manifests/eval/eval_slice_manifest.jsonl` canonical row hashes against upstream Git history.

- Recovered `main` snapshot: `kakao/FunctionChat-Bench@5ddb0b5bb37d6423e1f3381ef693cda811a7847e`
- Hash match: 100/100 selected rows
- Data-equivalent selected-row commits: `cb32af378a2b94ee84fc4d3cb50302377c7ff679`, `dfa59f64392ffc6373dfb4a336b631c11be3ec5e`
- Non-matching public-release branch example: `723bafbf09e251d9de8f083612f023b4d7a19467` matched 70/100 selected rows
