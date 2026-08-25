# Phase 03 — Provider integration and operational hardening

外部 provider 尚未選定，因此 Phase 03 保持 adapter-neutral：先建立 provider configuration、secret redaction、timeouts、approval policy 與可替換 adapter；待 provider 決策後才接 API 或 Codex CLI。

## Planned

- real provider adapters behind existing `Planner`／`Executor`／`Reviewer` protocols
- persisted plan/task/run artifacts and human-readable status views
- lock expiry policy and explicit stale-run recovery
- retry backoff and richer failure classification
- integration tests against provider fakes and repository fixtures

## Non-goals

No automatic commit, push, merge, deploy, production mutation, or unbounded autonomous loop.
