# bran-agent-skills

Personal AI capability source of truth for Codex.

## Rules

- Inspect before changing; make the smallest correct change.
- Keep skills focused, concise, and independently routable.
- Never commit secrets, personal data, or machine-specific paths.
- Validate skill frontmatter, names, scripts, and links before committing.

Every skill lives at `skills/<name>/SKILL.md`; its `name` must equal the directory name.
