# Project AGENTS.md guide

## Purpose

Use a project-level `AGENTS.md` for rules that are true only for one repository. Keep global behavior in Codex Instructions and shared capabilities in `bran-agent-skills`.

## Sources

Derive project rules from the repository's README, package/build configuration, tests, existing conventions, and explicit owner requirements.

## Recommended sections

- Language and communication
- Technology and package manager
- Development and test commands
- Architecture and naming conventions
- Safety and forbidden operations
- Delivery requirements

## Minimal template

```markdown
# Project instructions

## Language

- Respond in Traditional Chinese.
- Use English for code identifiers and commit messages.

## Workflow

- Read the README and relevant tests before editing.
- Run the project's targeted tests after editing.

## Safety

- Do not commit secrets or modify `.env`.
- Do not deploy, push, or change production data without explicit approval.
```

Do not copy every shared skill or the global system prompt into each project.
