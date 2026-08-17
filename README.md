# bran-agent-skills

Personal AI capability source of truth for Codex: task routing, prompt management, Agent Skills, composite workflows, project bootstrap, and playbook maintenance.

## Layout

- `skills/` — focused and composite Codex skills
- `bootstrap/` — cross-platform installation and synchronization scripts
- `references/` — authoring guidance
- `scripts/` — repository validation utilities

## Install

Windows: `./bootstrap/setup.ps1 -Categories core,coding,research,knowledge,composite`

macOS/Linux: `./bootstrap/setup.sh core coding research knowledge composite`

Both installers create links into the Codex skills directory and never replace an existing non-link directory.

## Validate

Run `./scripts/validate-skills.ps1` from PowerShell.
