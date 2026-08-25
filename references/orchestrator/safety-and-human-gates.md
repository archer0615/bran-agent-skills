# Safety, human gates, and Git policy

## Mandatory human gates

Pause in `NEEDS_HUMAN` before destructive operations, production data mutation, deploy/release, merge to a protected/default branch, secrets or credentials, security-sensitive changes, irreversible migrations, public API compatibility breaks, major dependency upgrades, or architecture changes beyond the Task. The approval records scope, actor, timestamp, decision, expiry/revision and rationale. Approval for one task does not authorize a broader task.

## Git boundary

Default permissions are inspect, modify working tree, run checks and generate diff. `allow_commit`, `allow_push`, `allow_pr`, and `allow_merge` default to `false`; deploy/release is always gated separately. No automatic history rewrite. Dirty unrelated changes are preserved and reported; the controller must not include them in its change set.

## Evidence and review

Every command records exact command, exit code, duration, relevant summary and repository revision. Review requires diff summary, changed files, applicable tests/build/lint/type checks, known issues and unverified items. Executor self-report alone is insufficient. A failed check is not silently converted to PASS.

## Failure handling

Implementation defect → bounded retry; repeated defect → replan. Test failure caused by the change → correct/retry; pre-existing failure → record and human/replan decision. Environment failure or unavailable dependency → `BLOCKED`. Requirement ambiguity → `NEEDS_HUMAN`. Security, destructive, architecture or compatibility conflict → `NEEDS_HUMAN`. Exhausted limits or invalid artifacts → `FAILED`. Explicit user stop → `ABORTED`.

Sensitive prompts, environment values, tokens and raw logs remain local/ignored. State writes are atomic and revision-checked; stale or concurrent state stops safely rather than overwriting another run.
