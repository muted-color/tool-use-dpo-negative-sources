# model_license_table.md

Stage0에서 실제 model card, license, and local runtime status를 확인해 채운다.

| Role | Candidate | Size | License | Local runtime | Tool-call format risk | Korean capability risk | Status | Notes |
|---|---|---:|---|---|---|---|---|---|
| target base | Qwen/Qwen3-8B-Base | 8B | Apache-2.0 | likely feasible on GB10 120GB UMA; smoke required | base model may need SFT to produce stable tool-call format | unknown; likely enough for secondary OOD check but must measure | preferred | Non-gated HF model, same family as weak candidate |
| target instruct | Qwen/Qwen3-8B | 8B | Apache-2.0 | likely feasible on GB10 120GB UMA; smoke required | instruct/chat formatting may reduce SFT headroom; verify parser/schema validity | unknown; likely stronger multilingual prior than base but must measure | preferred_pilot_pair | Non-gated HF model; use for Base+SFT vs Instruct+light-SFT pilot |
| weak model | Qwen/Qwen3-1.7B-Base + light/same-format tool-use SFT | 1.7B | Apache-2.0 | feasible; smoke required | raw base may be too weak/trivial; light SFT should teach JSON/tool-call format while preserving weak errors | unknown; not used for Korean claims | preferred | Use as weak-model negative generator if difficulty gate passes |
| weak model | Qwen/Qwen3-1.7B | 1.7B | Apache-2.0 | feasible; smoke required | may generate more formatted but less diverse negatives; still needs difficulty gate | unknown; not used for Korean claims | backup | Backup weak generator if weak-base+SFT is unusable |
| target base | Qwen/Qwen2.5-7B | 7B | Apache-2.0 | likely feasible; smoke required | older family but stable HF support | unknown | backup | Non-gated Apache candidate if Qwen3 tooling causes issues |
| target instruct | Qwen/Qwen2.5-7B-Instruct | 7B | Apache-2.0 | likely feasible; smoke required | may be saturated on function-calling format; check headroom | unknown | backup | Pair with Qwen2.5-7B if Qwen3 is not selected |
| weak model | Qwen/Qwen2.5-3B / Qwen2.5-3B-Instruct | 3B | qwen-research / other | feasible; smoke required | license less clean than Qwen3 Apache; difficulty gate still required | unknown | avoid_for_now | Prefer Qwen3-1.7B Apache unless Qwen3 weak generator fails |
| target base/instruct | meta-llama/Llama-3.1-8B / Instruct | 8B | Llama 3.1 Community License; gated manual access | likely feasible after access; smoke required | custom license/access and naming obligations complicate public reproducibility | Korean not listed; likely weaker OOD basis | needs_review | Keep as backup only; gated and non-Apache |
| target base/instruct | google/gemma-2-9b or gemma-3-4b | 4B/9B | Gemma license; gated manual access | likely feasible after access; smoke required | custom license/access; Gemma 3 4B is multimodal pipeline tag | unknown | needs_review | Backup only; size does not match 7B/8B target cleanly |

## Selection Rule

- Prefer one model family for target and weak model if license and runtime allow it.
- Choose Base+SFT if the pilot reaches usable parse/schema validity and leaves DPO headroom.
- Choose Instruct+light-SFT if Base+SFT is unstable or format failures dominate.
- Do not choose an already saturated Instruct checkpoint unless hard behavior/noised negatives still show headroom.

## Current Stage0 Recommendation

- Preferred family: Qwen3, because target and weak candidates are non-gated Apache-2.0 and same-family.
- Pilot target pair: `Qwen/Qwen3-8B-Base` with tool-use SFT versus `Qwen/Qwen3-8B` with light tool-use SFT.
- Preferred weak generator: `Qwen/Qwen3-1.7B-Base` after light/same-format tool-use SFT, with `Qwen/Qwen3-1.7B` as backup.
- Do not use Llama or Gemma as first target unless Qwen3 runtime or tool-call format fails; both add gated/custom-license complexity.

## Tool-Call Format Rule

- Base models are not direct DPO targets. The main DPO target is the selected tool-use SFT checkpoint.
- Main target path: `Qwen/Qwen3-8B-Base -> tool-use SFT -> DPO rejected-source ablation`.
- Backup target path: `Qwen/Qwen3-8B -> light tool-use SFT -> DPO rejected-source ablation`.
- Weak source path: `Qwen/Qwen3-1.7B-Base -> light/same-format tool-use SFT -> weak-model negatives`.
- Fix Qwen3 function-calling serialization before SFT/DPO: tool schema serialization, assistant tool-call format, tool result format, system prompt, stop tokens, parser, and thinking mode.
- Main function-calling runs use `enable_thinking=False` unless a later predeclared ablation changes it.

## Evidence Sources Checked

- `https://huggingface.co/api/models/Qwen/Qwen3-8B-Base`
- `https://huggingface.co/api/models/Qwen/Qwen3-8B`
- `https://huggingface.co/api/models/Qwen/Qwen3-1.7B-Base`
- `https://huggingface.co/api/models/Qwen/Qwen3-1.7B`
- `https://huggingface.co/api/models/Qwen/Qwen2.5-7B`
- `https://huggingface.co/api/models/Qwen/Qwen2.5-7B-Instruct`
- `https://huggingface.co/api/models/Qwen/Qwen2.5-3B`
- `https://huggingface.co/api/models/meta-llama/Llama-3.1-8B`
- `https://huggingface.co/api/models/meta-llama/Llama-3.1-8B-Instruct`
- `https://huggingface.co/api/models/google/gemma-2-9b`
- `https://huggingface.co/api/models/google/gemma-2-9b-it`
- `https://huggingface.co/api/models/google/gemma-3-4b-pt`
- `https://huggingface.co/api/models/google/gemma-3-4b-it`
