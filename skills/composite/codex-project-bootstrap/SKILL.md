---
name: codex-project-bootstrap
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use to initialize Codex guidance and capability links for a project.
---

# Codex Project Bootstrap

## Use when

Use this skill when initializing Codex guidance, project instructions, capability links, or validation conventions for an existing or new project.

## Inputs

- Required: Project repository and existing instructions, configuration, and workflow files.
- Optional: Technology stack, desired Codex behavior, setup constraints, and validation commands.
- Preconditions: The project can be inspected and no external publication is implicitly required.
- Missing information: Derive commands from repository evidence and mark uncertain setup steps as conditional.
- Output artifact: Scoped project guidance, bootstrap changes, validation results, and remaining setup actions.

## Procedure

1. Inspect the project structure, README, package or build configuration, tests, existing `AGENTS.md` files, and repository-specific workflows.
2. Determine whether project-specific guidance is necessary and identify the technology stack, commands, conventions, safety constraints, and expected delivery checks.
3. Create or update only the smallest required guidance files and capability links. Keep project rules separate from global instructions and do not duplicate the full skill library.
4. Preserve existing instructions unless they conflict with verified project behavior or the explicit request. Flag conflicts rather than silently overriding them.
5. Validate file placement, Markdown structure, commands, links, and consistency with the actual project.
6. Perform an idempotence pass: verify that repeating the bootstrap does not duplicate rules, overwrite user content, or create broken links.

## Decision rules

- Do not create `AGENTS.md` when the project has no special rules that need to be recorded.
- Derive commands from project configuration and existing documentation; do not invent package managers or deployment steps.
- Never include secrets, personal data, or machine-specific paths.
- Do not install dependencies, publish, deploy, or change external systems unless explicitly requested.
- Prefer a reversible, additive change; record any required manual migration or platform-specific limitation.
- Treat missing project evidence as a conditional instruction, not permission to invent commands.

## Verification

- Guidance matches the project’s actual stack and workflow.
- Instructions are scoped, non-duplicative, and discoverable from the project root.
- Referenced commands and links are valid or clearly marked as conditional.
- Existing project behavior and user changes remain intact.
- A repeat-run check confirms setup is idempotent or documents the exact limitation.

## Output

Return a bootstrap report with inspected sources, created or changed guidance, assumptions, validation evidence, and remaining setup actions.

