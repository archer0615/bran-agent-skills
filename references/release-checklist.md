# Release Checklist

Use this checklist before publishing a Skill library update.

## Versioning

- Use a patch-level change for documentation-only corrections.
- Use a minor-level change for compatible Skills, routing, or validation additions.
- Use a major-level change for renamed or removed Skills, changed output contracts, or incompatible routing behavior.
- Record the version, date, scope, migration notes, and validation results in `CHANGELOG.md`.

## Pre-release checks

1. Review `git diff` and confirm the scope contains no secrets, personal data, or unrelated files.
2. Run `scripts/validate-skills.ps1`.
3. Run `scripts/validate-scenarios.ps1`.
4. Run `scripts/validate-library.ps1`.
5. Review routing scenarios and update README or handoff documentation when counts or routes change.
6. Record unresolved warnings, compatibility notes, and rollback steps.

## Publication

- Commit with a concise change description.
- Push only the intended branch after local checks pass.
- Confirm the GitHub Actions validation workflow passes.
- Create a release or tag only after review; do not imply a release from a commit alone.
