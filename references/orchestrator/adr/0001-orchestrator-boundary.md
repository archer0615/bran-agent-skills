# ADR 0001 — Keep orchestration separate from reusable Skills

## Status

Accepted for Phase 01.

## Decision

Place the future coordinator under an `orchestrator/` boundary and keep reusable behavior under `skills/`. Keep Phase 01 specifications under `references/orchestrator/`; do not create a giant `orchestrator` Skill.

## Rationale

Skills are routed capabilities with their own contracts and validation. State transitions, persistence, provider adapters, retry budgets and safety gates are workflow concerns that must be deterministic and shared across repositories. Combining them would duplicate existing `requirement-refinement`, `context-management`, `human-review-workflow`, `implementation-validator`, `quality-gate`, `project-tracking`, `codex-project-bootstrap` and `personal-ai-task-router` responsibilities, while making state and approval enforcement implicit.

## Consequences

The controller composes existing Skills through explicit contracts and can serve multiple target repositories. A future runtime introduces a small new boundary and tests, but no existing Skill contract needs to change. Repository-specific instructions remain authoritative at execution time.
