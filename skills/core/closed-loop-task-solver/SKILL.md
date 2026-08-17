---
name: closed-loop-task-solver
description: Use when a task needs inspect, execute, verify, and correction-loop discipline.
---

# Closed Loop Task Solver

## Use when

Use this skill when a task requires coordinated inspection, implementation or action, verification, and correction until the acceptance criteria are met.

## Procedure

1. Define the objective, scope, constraints, acceptance criteria, and safe stopping condition from the request and repository context.
2. Inspect relevant files, tests, configuration, history, and existing conventions. Record assumptions, risks, and the smallest viable change.
3. Execute only the approved in-scope change, preserving unrelated work and existing compatibility.
4. Verify with the narrowest useful checks, including targeted tests, lint, type-check, build, static inspection, or an equivalent evidence-based check.
5. Compare the observed result with every acceptance criterion. Separate passed checks, failed checks, warnings, and unverified items.
6. If verification fails, identify the direct cause, make the minimum corrective change, and repeat verification. Do not conceal or bypass a failed check.
7. Stop when all criteria pass, or when a genuine external blocker remains. Report the blocker and the evidence needed to continue.

## Decision rules

- Prefer repository evidence over assumptions and external information.
- Keep each correction focused on the verified failure that caused it.
- Do not broaden scope merely because an adjacent improvement is visible.
- Escalate to `implementation-validator` when the main work is complete and only targeted validation remains.
- Escalate to `quality-gate` when readiness, compatibility, security, or delivery completeness requires a final review.
- Never claim completion from an unrun command or from an incomplete acceptance check.

## Verification

- Every acceptance criterion has a matching evidence item or an explicit blocker.
- The final verification was run after the last modification.
- Failed checks are either corrected and re-run or reported as unresolved.
- The final state and changed files are consistent with the requested scope.

## Output

Return the outcome, changed files, verification commands or evidence, remaining limitations, and the next action if blocked.

