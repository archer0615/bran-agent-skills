# Phase 03 — Provider integration and operational hardening

## Phase 03A completed

Phase 03A completed the offline runtime safety foundation: centralized and validated state transitions, terminal-state enforcement, append-only transition events, persisted single-use human gates, lock metadata with explicit stale/unknown recovery, atomic state backups, corruption detection/recovery, repository revision checks, and persisted bounded retry/replan counters. Deterministic fake-provider tests remain the only execution path.

Remaining Phase 03 work is provider-neutral operational UX and production-like integration described below; real providers remain out of scope until Phase 03B.

## Phase 03B progress

The first Phase 03B increment now persists bounded Goal, current Plan, Task, execution/review Run artifacts under `.orchestrator/`, exposes them through the `artifacts` CLI command, and keeps all writes atomic and path-confined. Real provider adapters remain pending provider selection and explicit integration requirements.

外部 provider 尚未選定，因此 Phase 03 保持 adapter-neutral：先建立 provider configuration、secret redaction、timeouts、approval policy 與可替換 adapter；待 provider 決策後才接 API 或 Codex CLI。

## Planned

- real provider adapters behind existing `Planner`／`Executor`／`Reviewer` protocols
- persisted plan/task/run artifacts and human-readable status views
- lock expiry policy and explicit stale-run recovery
- retry backoff and richer failure classification
- integration tests against provider fakes and repository fixtures

## Non-goals

No automatic commit, push, merge, deploy, production mutation, or unbounded autonomous loop.
