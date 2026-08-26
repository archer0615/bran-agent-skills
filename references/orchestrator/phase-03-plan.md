# Phase 03 — Provider integration and operational hardening

## Phase 03A completed

Phase 03A completed the offline runtime safety foundation: centralized and validated state transitions, terminal-state enforcement, append-only transition events, persisted single-use human gates, lock metadata with explicit stale/unknown recovery, atomic state backups, corruption detection/recovery, repository revision checks, and persisted bounded retry/replan counters. Deterministic fake-provider tests remain the only execution path.

The offline runtime safety foundation is implemented and covered by deterministic tests. Remaining work is limited to production-environment validation and explicitly configured external-provider operation; no provider is enabled by default.

## Phase 03B progress

Phase 03B now persists bounded Goal, current Plan, Task, execution/review Run artifacts under `.orchestrator/`, exposes them through the `artifacts` CLI command, validates artifact contracts at write time, and keeps all writes atomic and path-confined. Provider-neutral JSON HTTP Planner/Reviewer adapters and an explicit Codex CLI Executor adapter are available but remain disabled unless configured.

外部 provider 仍採明確設定才啟用的策略：provider configuration、secret redaction、timeouts、approval policy、JSON HTTP adapters 與 Codex CLI adapter 均已建立；正式 provider endpoint、model 與 credential policy 仍由部署環境決定。

## Planned

- production endpoint compatibility tests using a controlled provider fixture
- persisted plan/task/run artifact migration/versioning beyond schema `1.0`
- retry backoff and richer failure classification for external service outages
- multi-process integration tests for lock ownership and stale-run recovery

## Non-goals

No automatic commit, push, merge, deploy, production mutation, or unbounded autonomous loop.
