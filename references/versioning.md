# Versioning and compatibility

- The Python orchestrator version is declared in `pyproject.toml`.
- Skill-library content changes are recorded in `CHANGELOG.md`.
- A patch release is for documentation, validation, or backwards-compatible fixes.
- A minor release is for additive Skills, commands, schemas, or provider adapters.
- A major release is required for breaking schema, CLI, installation, or Skill routing changes.
- Schema changes must include migration or compatibility guidance and a regression fixture.
- Runtime `.orchestrator/` state is local data and must not be committed.

Before release, run `scripts/prepare-release.ps1` and complete `references/release-checklist.md`.
