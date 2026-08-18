---
name: implementation-validator
description: Use after implementation to run targeted checks and report evidence.
---

# Implementation Validator

## Use when

Use this skill after implementation or configuration changes when targeted evidence is needed to determine whether the requested behavior works and whether regressions were introduced.

## Procedure

1. Read the request, acceptance criteria, changed files, project instructions, and available test or build configuration.
2. Inspect the diff and identify the changed execution paths, risk areas, and the smallest checks that cover them.
3. Run checks in increasing cost and scope: static or syntax checks, targeted tests, affected package checks, then broader checks only when justified.
4. Capture the exact command, result, relevant failure output, and environment limitation for every check.
5. Compare results with the acceptance criteria and, when available, the pre-change baseline. Classify findings as pass, introduced failure, pre-existing failure, warning, or unverified.
6. If an introduced failure is found, provide the cause and return the work to the implementation or correction loop. Do not silently modify scope to make a check pass.
7. Classify validation depth as `smoke`, `targeted`, `affected-area`, or `full`; explain why the selected depth is sufficient and what remains outside coverage.

## Decision rules

- Prefer existing project commands and test conventions over invented validation scripts.
- Match validation depth to change risk: behavior, public API, data, security, and build changes require broader evidence.
- Do not treat a successful lint or static check as proof of runtime behavior.
- Do not report a check as passed when it was skipped, blocked, or only inferred.
- Keep secrets, credentials, private data, and machine-specific paths out of evidence.
- Prefer a baseline comparison whenever the repository or prior artifact is available.
- Treat a blocked dependency, unavailable environment, or skipped test as `unverified`, not `pass`.
- Escalate from targeted to broader checks when the change affects public contracts, data, security, or multiple execution paths.

## Verification

- Every acceptance criterion has a corresponding check or an explicit unverified status.
- The final check ran against the final modified state.
- Failures identify whether they were introduced, pre-existing, or caused by the environment.
- The report distinguishes verified behavior from limitations and recommendations.
- Validation depth, baseline, coverage boundary, and failure classification are explicit.

## Output

Return a validation report with scope, changed paths, commands run, results, acceptance-criteria mapping, failures or limitations, and a clear ready/not-ready recommendation.

## Example

For a one-file configuration change, run a syntax or targeted check first. If it changes a public API or data path, expand to affected-area or full validation and compare with the baseline; report any unavailable environment as unverified.

