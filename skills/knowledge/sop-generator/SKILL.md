---
name: sop-generator
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when turning a repeatable task or informal know-how into a clear, handoff-ready SOP.
---

# Sop Generator

## Use when

Use this skill when turning a repeatable task or informal know-how into a clear, handoff-ready standard operating procedure.

## Inputs

- Required: Source process or evidence, audience, purpose, scope, inputs, tools, and completion criteria.
- Optional: Owner, frequency, permissions, examples, exceptions, rollback steps, and version history.
- Preconditions: The process is repeatable enough to distinguish confirmed steps from assumptions.
- Missing information: Mark unknown steps and escalation points; do not convert guesses into mandatory procedure.
- Output artifact: Versioned SOP with preconditions, numbered steps, decisions, exceptions, checks, recovery, and ownership.

## Procedure

1. Identify the process purpose, owner, audience, scope, frequency, inputs, tools, preconditions, and completion criteria.
2. Extract the real sequence from source evidence and preserve domain terminology. Mark assumptions instead of silently filling gaps.
3. Write numbered steps with decision points, expected results, exceptions, escalation paths, and rollback or recovery actions where relevant.
4. Add safety, access, data-handling, and approval requirements proportional to the process risk.
5. Include checks at the points where errors can be detected earliest and a final verification that proves completion.
6. Review the SOP with a fresh execution path or representative case; correct ambiguity and record owner, version, and change notes.

## Decision rules

- Preserve actual purpose and constraints; do not turn guesses into mandatory steps.
- Every step needs an observable action or result, and every decision needs a condition and branch.
- Mark approval-required, permission-sensitive, irreversible, and escalation actions explicitly.
- Keep exceptions adjacent to the step where they occur.

## Verification

- Another person can execute the SOP from the document without relying on hidden context.
- Inputs, preconditions, decisions, exceptions, checks, and completion criteria are explicit.
- Assumptions, safety requirements, and escalation paths are visible.
- Terminology and steps match the source process and the final validation case.

## Output

Return the SOP with purpose, scope, owner, inputs, preconditions, steps, decisions, exceptions, checks, completion criteria, version notes, assumptions, and review criteria. Communicate with the user in Traditional Chinese unless another language is requested.

