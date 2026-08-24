---
name: quality-gate
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when reviewing whether an artifact or change is ready to deliver.
---

# Quality Gate

## Use when

Use this skill before delivering an artifact, implementation, documentation change, or configuration update when readiness must be judged against scope, quality, safety, and evidence.

## Inputs

- Required: Final artifact or change, acceptance criteria, project rules, and verification evidence.
- Optional: Risk classification, reviewer requirements, baseline, release constraints, and known limitations.
- Preconditions: Work is reviewable; incomplete work must be marked not ready.
- Missing information: Classify missing evidence as unverified and do not approve by assumption.
- Output artifact: Ready/not-ready decision with evidence, gaps, risks, owners, and follow-up.

## Procedure

1. Read the request, acceptance criteria, project instructions, changed files, diff, and verification results.
2. Check scope and completeness: every requested outcome is addressed, unrelated changes are excluded, and documentation or configuration is consistent with the implementation.
3. Check correctness and compatibility using targeted tests, static inspection, build results, and existing conventions appropriate to the change.
4. Check safety: secrets and personal data are absent, security-sensitive behavior is reviewed, destructive or irreversible actions are authorized, and failure handling is explicit.
5. Check maintainability: names, structure, duplication, error handling, and operational notes are consistent with the repository.
6. Classify findings by severity and impact. Block delivery for unresolved critical correctness, security, data, compatibility, or acceptance failures.
7. Re-run the final relevant verification after any correction, then issue a ready or not-ready decision with evidence.

## Decision rules

- Use repository instructions and explicit acceptance criteria as the primary authority.
- Treat warnings as delivery concerns when they affect correctness, security, compatibility, or future operation.
- Do not approve a change because a single check passed when required checks were skipped or blocked.
- Distinguish defects from optional improvements; do not expand the requested scope during the gate.
- Never expose secret values or claim verification that was not performed.
- Own the final ready/not-ready judgment; consume `implementation-validator` evidence rather than duplicating its test procedure.
- Return failed criteria and required corrective checks to the implementation owner or `implementation-validator`.

## Verification

- Scope, correctness, compatibility, safety, maintainability, and documentation have been reviewed as applicable.
- All blocking findings are resolved or explicitly escalated.
- Final evidence corresponds to the final file state.
- The readiness decision and remaining limitations are unambiguous.

## Output

Return a quality-gate report with readiness decision, reviewed scope, verification evidence, findings by severity, unresolved limitations, and required follow-up actions.

