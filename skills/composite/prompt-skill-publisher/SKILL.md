---
name: prompt-skill-publisher
description: Use to turn an approved prompt or skill into a validated published artifact.
---

# Prompt Skill Publisher

## Use when

Use this skill when turning an approved prompt, workflow, or skill into a validated artifact ready for local distribution or an explicitly requested publication step.

## Procedure

1. Confirm the source prompt or skill, intended audience, target format, scope, approval status, and publication destination.
2. Inspect repository authoring rules, existing templates, naming conventions, metadata requirements, and validation tools.
3. Normalize the artifact to the target contract without changing approved intent. Keep instructions focused, actionable, and free of duplicated scope.
4. Check metadata, trigger description, procedure, verification, output format, links, examples, and compatibility with existing artifacts.
5. Run the repository validator and targeted content checks. Review the diff for secrets, personal data, machine-specific paths, unsupported claims, and accidental scope changes.
6. Publish or distribute only when explicitly requested; otherwise leave a validated local artifact and state the remaining publication action.

## Decision rules

- Approval of content is separate from technical validation and publication authorization.
- Prefer the repository’s established artifact format over a new format.
- Do not silently broaden a prompt or skill to cover adjacent use cases.
- A failed validation blocks publication until corrected and re-verified.

## Verification

- The artifact satisfies its target metadata and structure contract.
- The trigger is specific enough to route correctly and does not duplicate an existing capability.
- Validation ran against the final artifact.
- Publication status and remaining limitations are explicit.

## Output

Return a publishing report with source, target artifact, changed files, validation evidence, approval or publication status, and follow-up actions.

