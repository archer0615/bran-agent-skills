# bran-agent-skills

This repository is the personal AI capability source of truth for Codex.

## Canonical repository root

- This directory is the canonical working repository for this project.
- Codex tasks for `bran-agent-skills` must use the repository root containing this file as the Git working tree.
- Do not use or synchronize a second clone automatically; if another clone is detected, report the path difference before modifying files.

## Operating model

Follow: `Input → Route → Inspect → Execute → Verify → Correct if required → Output`.

- Classify work as direct, engineering, or high-impact before acting.
- Inspect existing code, tests, configuration, and documentation before external sources.
- Use the narrowest matching skill; use `personal-ai-task-router` when uncertain.
- First judge whether the user's instruction is already actionable. Refine only when ambiguity, missing constraints, or unclear acceptance criteria would materially affect the result.
- Make the minimum correct change and preserve existing architecture and compatibility.
- When verification fails, identify the cause, correct it, and re-run the relevant check.

## Safety

- Never commit secrets, tokens, passwords, certificates, personal data, or machine-specific paths.
- Do not overwrite unrelated user changes or delete unrelated files.
- Do not modify production data or perform destructive database operations.
- Do not commit, push, merge, deploy, release, or rewrite history unless explicitly requested.
- Confirm before irreversible changes or changes affecting security, data compatibility, or public APIs.

## Validation and output

- Prefer targeted build, test, lint, type-check, or static-analysis commands appropriate to the change.
- Do not claim a command succeeded unless it was actually run.
- Report concise `Changed`, `Verified`, and only necessary `Notes` sections.
- Skills may be authored in English for portability, but communicate with the user in Traditional Chinese by default.
- Keep questions, explanations, verification results, and final responses in Traditional Chinese unless the user requests another language.

## Skill contract

Every skill lives at `skills/<category>/<name>/SKILL.md`. Its YAML `name` must equal the skill directory name, and its `description` must clearly state when Codex should use it. Keep skills focused, concise, routable, and free of duplicated scope.
