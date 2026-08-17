---
name: prompt-curator
description: Use to organize, improve, and version reusable prompts.
---

# Prompt Curator

## Use when

Use this skill to organize, improve, classify, deduplicate, or version reusable prompts without changing their intended behavior.

## Procedure

1. Inventory the prompt’s purpose, trigger, audience, inputs, constraints, output contract, language, and version history.
2. Remove duplication, ambiguity, hidden assumptions, secrets, personal data, and machine-specific details.
3. Preserve intent while improving structure, instruction priority, placeholders, examples, and failure handling.
4. Compare against existing prompts and skills; merge, rename, archive, or retain only with an explicit reason.
5. Test representative, missing-data, boundary, and adversarial inputs. Record regressions and compatibility notes.
6. Assign a stable name and version note, then document the change and recommended usage.

## Verification

- The prompt has a clear purpose, trigger, inputs, and output contract.
- It does not duplicate or conflict with an existing capability.
- Sensitive and machine-specific content is absent.
- Representative tests preserve required behavior and expose known limits.

## Output

Return the curated prompt, classification, version note, change rationale, overlap findings, test results, assumptions, and usage guidance.

