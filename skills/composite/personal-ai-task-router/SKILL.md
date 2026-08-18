---
name: personal-ai-task-router
description: Use to route a personal AI request to the narrowest matching capability.
---

# Personal Ai Task Router

## Use when

Use this skill when a request may match more than one capability, or when the user does not name a skill and the correct workflow must be selected from the request and repository context.

## Procedure

1. Classify the request as direct, engineering, research, knowledge, composite, or high-impact.
2. Inspect the request, explicit constraints, acceptance criteria, repository instructions, and available files before choosing a route.
3. Select the narrowest capability that fully covers the work. Prefer an existing project-specific workflow over a broad or duplicated capability.
4. If several capabilities are required, order them by dependency: clarify or route first, inspect or research second, execute third, validate last.
5. If the request is actionable, preserve its intent and proceed. Use requirement refinement only when missing information would materially change the result.
6. If no capability is an exact match, choose the closest safe workflow, state the assumption, and keep the result reversible.
7. Hand off the selected route with the objective, relevant context, constraints, expected output, and verification criteria.

## Decision rules

- Use `requirement-refinement` when important requirements, constraints, or acceptance criteria are missing.
- Use `existing-project-takeover` when the task begins with understanding an unfamiliar existing project.
- Use `evidence-first-research` when current, niche, external, or source-backed information is required.
- Use `implementation-validator` after code or configuration changes need targeted verification.
- Use `quality-gate` before delivery when correctness, compatibility, security, or completeness needs a final review.
- Use `closed-loop-task-solver` when the work spans inspect, execute, verify, and correction.
- Do not select a broader composite skill when a narrower skill satisfies the request.
- If two Skills appear to match, prefer the one with the more specific trigger and primary artifact; use the other only when it owns a distinct dependency or review gate.
- Use at most one primary execution owner per workstream; supporting Skills must have an explicit input and handoff output.
- For high-impact, irreversible, external, privacy-sensitive, or security-sensitive work, include governance or human review before execution.
- When route confidence is low, state the competing candidates and the evidence or clarification needed to choose safely.

## Verification

- Confirm the selected capability directly covers the user’s requested outcome.
- Confirm required dependencies and sequencing are explicit.
- Confirm the route includes a concrete verification method.
- Confirm no unsupported status, assumption, or completion claim is introduced.
- Confirm the handoff specifies the next Skill, its input artifact, expected output, and return condition.

## Output

Return the selected capability or ordered capability sequence, the routing reason, rejected alternatives when material, the key assumptions or missing information, the handoff contract, expected output, and verification method.

## Example

For a request to assess whether an AI workflow is ready for external use, route to `evidence-first-research` when current evidence is needed, then `human-review-workflow`, and finish with `quality-gate`. Keep `personal-ai-task-router` as the routing owner rather than duplicating those procedures.

