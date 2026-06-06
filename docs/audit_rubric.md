# Audit Rubric

## Reject Categories

- `optional_default_noop`: the rejected output differs only by optional/default
  or no-op behavior.
- `acceptable_alternative`: the rejected output is plausibly acceptable under the
  supplied tool schema or behavior policy.
- `equivalent_to_chosen`: chosen and rejected outputs are materially equivalent
  after canonicalization.
- `semantic_ambiguity`: the available prompt/schema does not establish that the
  rejected output is worse.
- `malformed_noninformative`: parse/schema failure does not represent a useful
  DPO negative.
- `chosen_reference_suspect`: the chosen/reference output may itself be wrong.

## LLM-Assisted Audit

The Stage3d clean-pool gates used an external `gpt-5_5-2026-04-23` high judge
for holdout quality control. The recorded request metadata uses JSON response
format, `reasoning_effort=high`, and `max_completion_tokens=4096`; temperature
was not explicitly set by the client for the OpenAI chat-completions request. These
holdout gates are reported for `r026` noised_gold and `r027b` behavior; the
earlier `r027` behavior attempt failed the chosen/reference-suspect gate and is
not the DPO training source.

The Stage3d public manifest records the prompt template versions used by the
audit packets (`stage3d_clean_holdout_v1` and
`stage3d_clean_rescue_adjudication_v1`) and the input packet fields passed to
the judge. The exact prompt template and query date are not redistributed in the
public artifact. The required JSON response keys are `audit_item_id`,
`audit_accept`, `rejected_tool_schema_valid`, `rejected_incorrect`,
`primary_error`, `taxonomy`, `confidence`, and `rationale_short`. A clean pool
gate passes only if the holdout has at least 100 rows, at least 95% audit
acceptance, at most 1% chosen/reference-suspect labels, and no repeated reject
taxonomy bucket above 3%.

The Stage3b matched diagnostic audit uses a two-judge LLM workflow. First,
local `gpt-oss-120b` (`ggml-org/gpt-oss-120b-GGUF`) screens all 300 sampled
matched diagnostic items with `temperature=0`, JSON response format, and
`max_tokens=4096`. Second, external `gpt-5_5-2026-04-23` high adjudicates all
300 items with JSON response format, `reasoning_effort=high`, and
`max_completion_tokens=4096`; temperature was not explicitly set by the client
for the OpenAI chat-completions request. The final labels are the `gpt-5_5-2026-04-23` high
labels.

The audits are not human annotations or human ground truth. They are used to
screen selected pools for semantic validity risks, repeated failure modes, and
chosen/reference defects.

The matched diagnostic audit failed the independent audit gate required for
downstream matched mini-DPO reporting, so matched diagnostics are reported only
as source-quality diagnostics.
