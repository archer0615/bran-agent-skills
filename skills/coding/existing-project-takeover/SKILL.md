---
name: existing-project-takeover
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when taking over an unfamiliar repository or codebase.
---

# Existing Project Takeover

## Use when

Use this skill when taking over an unfamiliar repository, codebase, service, or partially completed change and the existing architecture and conventions must be understood before editing.

## Inputs

- Required: Repository path or workspace and requested investigation or change.
- Optional: Known symptoms, target subsystem, preferred commands, or issue references.
- Preconditions: Repository files can be inspected without changing them.
- Missing information: Build a bounded project overview first; do not guess an implementation target.
- Output artifact: Architecture and workflow summary, risks, evidence, and safe next route.

## Procedure

1. Establish the takeover objective, requested scope, constraints, and definition of done.
2. Inspect repository status and structure, `AGENTS.md` files, README and project documentation, dependency and build configuration, entry points, tests, and relevant history.
3. Identify the architecture, primary execution path, data or state boundaries, external integrations, and conventions that the requested change must preserve.
4. Run the narrowest safe baseline checks available before modifying files. Record existing failures separately from new failures.
5. Map the request to the smallest set of files and tests. Note assumptions, risks, unknowns, and files explicitly kept out of scope.
6. Execute the requested change using existing patterns and preserve unrelated user work.
7. Verify the changed path and compare results with the baseline. If a check fails, isolate whether the cause is pre-existing or introduced, then correct only introduced failures.

## Decision rules

- Treat repository instructions and existing tests as authoritative evidence for local conventions.
- Do not rewrite architecture, upgrade dependencies, or clean unrelated code unless explicitly required.
- Do not infer production behavior from a filename alone; trace the relevant call or data path.
- Inspect secrets and environment references for usage, but never expose or copy secret values.
- If the baseline cannot run, document the exact blocker and use static inspection or narrower checks where safe.

## Verification

- The project structure, instructions, relevant execution path, and affected files are identified.
- Baseline and post-change verification results are distinguished.
- The changed behavior is covered by a targeted check or an explicit limitation.
- No unrelated files or existing user changes were overwritten.

## Output

Return a takeover brief containing project map, relevant conventions, baseline status, affected files, assumptions, risks, implementation result, verification evidence, and remaining blockers.

