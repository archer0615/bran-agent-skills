# bran-agent-skills

Personal AI capability source of truth for Codex: task routing, prompt management, Agent Skills, composite workflows, project bootstrap, and playbook maintenance.

## Layout

- `skills/` — focused and composite Codex skills
- `bootstrap/` — cross-platform installation and synchronization scripts
- `references/` — authoring guidance
- `scripts/` — repository validation utilities

## Install once

Windows PowerShell:

```powershell
.\bootstrap\setup.ps1
```

macOS/Linux:

```sh
./bootstrap/setup.sh core coding research knowledge composite
```

Restart Codex after installation. Existing non-link folders are left untouched.

## Use

Just describe the task. Codex selects the matching skill automatically. You may also name one directly, for example: `請使用 quality-gate 審查這次修改。`

To verify the library on Windows:

```powershell
.\scripts\validate-skills.ps1
```
