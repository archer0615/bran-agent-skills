# Codex routing guidance

- Treat the repository `AGENTS.md` as the governing project policy.
- Route from the request and conversation context; do not require users to name a skill.
- Before execution, judge whether the instruction needs optimization. Preserve clear instructions; use `requirement-refinement` only when ambiguity or missing acceptance criteria could change the result.
- Use `personal-ai-task-router` when multiple capabilities may apply.
- Use `existing-project-takeover` for unfamiliar repositories.
- Use `requirement-refinement` when requirements or acceptance criteria are unclear.
- Use `evidence-first-research` when current or external evidence is required.
- Use `implementation-validator` after implementation.
- Use `quality-gate` before delivery.
- Composite skills may coordinate focused skills but must not replace verification.
- Keep skill instructions in English when useful for portability, but respond to the user in Traditional Chinese by default.
- Use Traditional Chinese for questions, progress explanations, verification results, and final answers unless the user requests otherwise.
