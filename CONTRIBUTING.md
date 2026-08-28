# Contributing

## Workflow

1. Read `AGENTS.md` and the relevant Skill instructions.
2. Keep changes focused and preserve the provider-neutral boundary.
3. Run the complete validation locally before opening a pull request.
4. Do not commit secrets, machine-specific paths, runtime state, or production data.

## Required checks

```powershell
python -m unittest discover -s tests -v
python -m compileall -q orchestrator tests
./scripts/validate-orchestrator.ps1
./scripts/validate-skills.ps1
./scripts/validate-scenarios.ps1
./scripts/validate-library.ps1
./scripts/validate-powershell.ps1
./scripts/validate-markdown.ps1
./scripts/validate-consistency.ps1
```

The GitHub Actions workflow additionally verifies Python 3.11–3.13 on Ubuntu and Windows and tests the installed package layout.
