---
name: prompt-curator
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use to organize, improve, and version reusable prompts.
---

# Prompt Curator

## Use when

Use this skill to organize, improve, classify, deduplicate, or version reusable prompts without changing their intended behavior.

## Inputs

- Required: Prompt, purpose, trigger, audience, inputs, constraints, output contract, and current version.
- Optional: Examples, test results, related prompts, language requirements, and compatibility notes.
- Preconditions: Intended behavior is known well enough to preserve during revision.
- Missing information: Keep ambiguity visible and request evaluation before claiming reliability.
- Output artifact: Curated Prompt, classification, version note, rationale, overlap findings, and usage guidance.

## Procedure

1. Inventory the prompt’s purpose, trigger, audience, inputs, constraints, output contract, language, and version history.
2. Remove duplication, ambiguity, hidden assumptions, secrets, personal data, and machine-specific details.
3. Preserve intent while improving structure, instruction priority, placeholders, examples, and failure handling.
4. Compare against existing prompts and skills; merge, rename, archive, or retain only with an explicit reason.
5. Test representative, missing-data, boundary, and adversarial inputs. Record regressions and compatibility notes.
6. Assign a stable name and version note, then document the change and recommended usage.

## Decision rules

- Preserve purpose and output contract unless a behavior change is explicitly authorized.
- Keep incompatible audiences, triggers, safety constraints, or acceptance criteria as separate variants.
- Treat examples as non-normative unless required, and do not claim reliability without evaluation evidence.
- Route robustness testing to `prompt-evaluation` and conversation extraction to `conversation-skill-miner`.
- Own organization and minimal revision; return the revised Prompt and regression targets to `prompt-evaluation`.
- Do not claim a revised Prompt is stable until the evaluation loop has run.

## Verification

- The prompt has a clear purpose, trigger, inputs, and output contract.
- It does not duplicate or conflict with an existing capability.
- Sensitive and machine-specific content is absent.
- Representative tests preserve required behavior and expose known limits.

## Output

Return the curated prompt, classification, version note, change rationale, overlap findings, test results, assumptions, and usage guidance.

