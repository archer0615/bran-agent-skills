# Skill authoring

Keep each skill narrow and operational. Use YAML frontmatter with `name`, a specific `description`, semantic `version`, lifecycle `status`, and ISO `last_reviewed` date, followed by `Use when`, `Inputs`, `Procedure`, `Verification`, and `Output` sections. Do not include secrets, personal data, or machine-specific paths.

Allowed lifecycle statuses are `active`, `experimental`, `deprecated`, and `retired`. A deprecated or retired Skill must document its replacement or migration path before removal.
