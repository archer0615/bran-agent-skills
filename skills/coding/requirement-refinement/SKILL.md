---
name: requirement-refinement
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when a request needs explicit scope, constraints, and acceptance criteria.
---

# Requirement Refinement

## Use when

Use this skill when a request is ambiguous about scope, constraints, expected behavior, priority, or acceptance criteria, and proceeding without clarification could materially change the result.

## Inputs

- Required: Original request and available project or domain context.
- Optional: Existing behavior, examples, constraints, users, deadline, and known risks.
- Preconditions: Ambiguity could change implementation, cost, safety, or acceptance.
- Missing information: Ask focused questions only for material unknowns; record non-material assumptions.
- Output artifact: Clarified requirements with scope, constraints, acceptance criteria, assumptions, and open questions.

## Procedure

1. Restate the requested outcome in one sentence without adding new scope.
2. Inspect the repository instructions, relevant files, existing behavior, and available evidence before asking questions.
3. Identify only the ambiguities that can change implementation, risk, compatibility, or acceptance. Ignore harmless wording preferences.
4. Convert the request into explicit scope, out-of-scope items, constraints, assumptions, priority, and observable acceptance criteria.
5. Ask the smallest set of focused questions when a material decision cannot be inferred safely. If the task is already actionable, proceed without unnecessary rewording.
6. Resolve answers and repository evidence into a concise implementation-ready brief.

## Decision rules

- Preserve the user’s intent; do not optimize a clear request into a different task.
- Prefer existing project conventions over invented requirements.
- Mark inferred details as assumptions and make them easy to revise.
- Treat security, data loss, public API compatibility, and production impact as material constraints.
- Do not ask the user to manually perform a check that can be inspected or verified through the repository.

## Verification

- The outcome is specific enough to identify what changes and what must remain unchanged.
- Each acceptance criterion is observable and testable.
- Scope boundaries, assumptions, and unresolved decisions are explicit.
- The refined brief does not introduce unsupported technologies, dependencies, or behavior.

## Output

Return the implementation-ready brief with objective, in-scope items, out-of-scope items, constraints, assumptions, acceptance criteria, unresolved questions, and the recommended next skill or action.

