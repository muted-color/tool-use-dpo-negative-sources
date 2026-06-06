# data_license_table.md

Stage0에서 실제 라이선스와 재배포 가능 여부를 확인해 채운다.

| Source | Intended use | License | Raw redistribution | Processed redistribution | Benchmark test-use constraint | Citation / attribution | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| BFCL | main English eval | Apache-2.0 | permitted by license, but do not commit benchmark raw data | aggregate metrics and tiny inspected samples only | eval-only; do not train on held-out benchmark prompts; record BFCL version/slice | Gorilla / Berkeley Function Calling Leaderboard attribution | download_script_only | HF dataset `gorilla-llm/Berkeley-Function-Calling-Leaderboard`, non-gated, last checked 2026-05-27 |
| When2Call | behavior eval and behavior prompts | CC-BY-4.0 | permitted with attribution, but do not commit full raw benchmark/train files | aggregate metrics and small audited samples only until Stage1 split is frozen | keep train/test split separation; do not tune on held-out test prompts | NVIDIA When2Call citation / attribution | download_script_only | HF dataset `nvidia/When2Call`, configs include `test`, `train_sft`, `train_pref`, last checked 2026-05-27 |
| FunctionChat-Bench | Korean OOD eval | Apache-2.0 | permitted by license, but do not commit benchmark raw data by default | aggregate metrics and tiny inspected samples only | secondary OOD eval; do not train/tune on benchmark prompts | Kakao FunctionChat-Bench citation / attribution | download_script_only | GitHub repo has Apache-2.0 license; HF API access not public/confirmed, use GitHub as source of truth |
| xLAM / APIGen function-calling 60k | SFT and DPO prompt pool | CC-BY-4.0; gated access acknowledgement | do not commit raw data; require HF access acknowledgement and citation | processed pairs should be download-script-only unless derivative release is separately approved | separate SFT train and DPO prompt pools; contamination check against eval benchmarks | Salesforce xLAM / APIGen citation | download_script_only | HF dataset `Salesforce/xlam-function-calling-60k`, auto-gated, last checked 2026-05-27 |
| ToolACE | SFT and DPO prompt pool | Apache-2.0 | permitted with attribution | processed samples releasable by license, but prefer scripts/hashes for full data | split from eval; check EN/ZH language metadata and tool schema format | ToolACE citation / attribution | releasable | HF dataset `lockon/ToolACE`, non-gated, last checked 2026-05-27 |
| Glaive function-calling v2 | optional SFT source | Apache-2.0 | permitted with attribution | processed samples releasable by license, but optional source needs contamination check | optional only; do not mix before SFT data card freezes source proportions | Glaive AI attribution | releasable | HF dataset `glaiveai/glaive-function-calling-v2`, non-gated, last checked 2026-05-27 |
| IFEval / MT-Bench-style subset | general regression check | IFEval Apache-2.0; MT-Bench judgments CC-BY-4.0 | permitted with license-specific attribution; do not commit full benchmark raw files | aggregate metrics and small inspected samples only | regression check only; not a main tool-use metric | Google IFEval / LMSYS MT-Bench attribution as applicable | download_script_only | Use `google/IFEval` first; MT-Bench-style only if license/citation path is explicit |

## Decision Rule

- `blocked`: cannot use in public-ready work without changing source or scope.
- `download_script_only`: do not commit raw/processed data; provide scripts and hashes.
- `sample_only`: only a small inspected sample can be committed.
- `releasable`: processed data can be included with attribution.

## Evidence Sources Checked

- BFCL: `https://huggingface.co/api/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard`
- When2Call: `https://huggingface.co/api/datasets/nvidia/When2Call`
- FunctionChat-Bench: `https://github.com/kakao/FunctionChat-Bench`
- xLAM / APIGen 60k: `https://huggingface.co/api/datasets/Salesforce/xlam-function-calling-60k`
- ToolACE: `https://huggingface.co/api/datasets/lockon/ToolACE`
- Glaive function-calling v2: `https://huggingface.co/api/datasets/glaiveai/glaive-function-calling-v2`
- IFEval: `https://huggingface.co/api/datasets/google/IFEval`
- MT-Bench human judgments: `https://huggingface.co/api/datasets/lmsys/mt_bench_human_judgments`
