---
name: prompt-skill-publisher
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use to turn an approved prompt or skill into a validated published artifact.
---

# Prompt Skill Publisher

## Use when

Use this skill when turning a prompt, workflow, or skill into a validated artifact.

## Inputs

- Required: Source artifact, target format, audience, metadata contract, and intended destination.
- Optional: Template, version note, compatibility constraints, and release checklist.
- Preconditions: The source artifact and target destination can be inspected.
- Missing information: Record unresolved artifact or destination details.
- Content approval is separate from technical validation and publication authorization.
- Output artifact: Validated artifact and publishing report with approval status, checks, and follow-up.

## Procedure

1. Confirm the source prompt or skill, intended audience, target format, scope, and destination.
2. Inspect repository authoring rules, existing templates, naming conventions, metadata requirements, and validation tools.
3. Normalize the artifact to the target contract without changing approved intent. Keep instructions focused, actionable, and free of duplicated scope.
4. Check metadata, trigger description, procedure, verification, output format, links, examples, and compatibility with existing artifacts.
5. Run the repository validator and targeted content checks. Review the diff for secrets, personal data, machine-specific paths, unsupported claims, and accidental scope changes.
6. Publish or distribute only when explicitly requested; otherwise leave a validated local artifact and state the remaining publication action.
7. Record the artifact version, compatibility impact, migration or rollback note, and the exact validation evidence used for publication readiness.

## Decision rules

- Prefer the repository’s established artifact format over a new format.
- Do not silently broaden a prompt or skill to cover adjacent use cases.
- A failed validation blocks publication until corrected and re-verified.
- A renamed, removed, or output-contract-changing artifact requires a migration note and explicit compatibility decision.

## Verification

- The artifact satisfies its target metadata and structure contract.
- The trigger is specific enough to route correctly and does not duplicate an existing capability.
- Validation ran against the final artifact.
- Publication status and remaining limitations are explicit.
- Version, compatibility, migration, and rollback information is recorded when the artifact changes behavior or routing.

## Output

Return a publishing report with source, target artifact, changed files, validation evidence, and follow-up actions.

