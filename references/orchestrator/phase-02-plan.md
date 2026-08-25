# Phase 02 plan — Local CLI prototype

目標是可恢復、保守、單一 target repository 的 local prototype；不是 autonomous framework。

## Must Have

1. Define `.orchestrator/` persistence, atomic writes, schema version and stale-revision detection.
2. Implement contract validation for Goal/Plan/Task/Execution/Review artifacts.
3. Add provider interfaces and deterministic fake adapters for Planner, Codex Executor and Reviewer.
4. Add a loop controller implementing the state machine and bounded limits.
5. Add repository inspection/diff and verification evidence capture.
6. Add human-gate pause/resume and explicit abort/recovery after interruption.

## Should Have

- A small CLI command accepting target path and goal.
- Dry-run mode, structured logs, Markdown status view, and fixture-based end-to-end tests.
- Real provider adapters behind the same interfaces, enabled explicitly and never by default.

## Later

Remote/shared state, parallel tasks, hosted service, GitHub App/Actions, web UI, automatic PR/merge/deploy, multi-agent scheduling, and advanced policy engines.

## Suggested implementation order

`state persistence → contract validator → repository adapter → planner adapter → executor adapter → reviewer adapter → controller → human gate → recovery → CLI/tests`.

Each increment must preserve the default Git boundary, add focused tests, and demonstrate evidence for both a passing path and blocked/replan/abort paths. Phase 02 should not add a dependency until the standard library and existing repository conventions are insufficient.
