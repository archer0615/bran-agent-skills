# Architecture

## Boundary

`skills/` 提供可重用的 capability；`orchestrator/`（未來 runtime）負責 workflow coordination、state、persistence、provider adapter 與 gate enforcement。Phase 01 文件放在 `references/orchestrator/`，不建立 runtime。

## Roles

| Role | Responsibilities | Must not do |
|---|---|---|
| Planner | inspect repo, define scope, decompose tasks, acceptance criteria, dependencies, risk and next executable task | modify target repo |
| Executor | read Task, inspect, make minimum changes, run checks, emit evidence | expand scope or self-approve |
| Reviewer | compare Goal/Task/criteria/diff/evidence/rules and decide | silently edit code |
| Human | approve material risk, resolve ambiguity, override or abort | be bypassed by an automatic retry |

## Components

1. **Controller** owns state transitions, limits, locking and recovery.
2. **Artifact store** persists versioned JSON documents and run metadata.
3. **Planner / Executor / Reviewer providers** are replaceable adapters; contracts do not depend on a model or vendor.
4. **Repository adapter** reads instructions, Git status/diff and verification commands without assuming a specific project.
5. **Gate evaluator** blocks destructive, security-sensitive or externally visible actions until human approval.

## Target repository state

The preferred future layout is:

```text
.orchestrator/
  state.json                 # committed checkpoint, no secrets
  current-plan.json          # committed plan snapshot
  tasks/<task-id>.json       # committed task contracts/results
  runs/<run-id>/              # local or ignored evidence/logs
```

`.orchestrator/` belongs to the target repository so work can resume on another machine. Runtime logs, prompts containing sensitive context, tokens and large command output stay local/ignored. A `repository_revision` and artifact `schema_version` make stale state detectable. Concurrent writers require a lock; a revision mismatch stops with `BLOCKED` rather than overwriting state.

## Context bundle

Authoritative: target `AGENTS.md`, current Goal/Plan/Task, current state, Git revision/diff, and persisted execution/review artifacts. Optional: relevant files, prior failed attempts, and compact project notes. Stale context is any artifact whose revision, task id, or schema version no longer matches; it is excluded or triggers re-inspection. Each provider receives only the minimum bundle: instructions → goal → plan → task → relevant context → prior result → review findings.

## Multi-repository rule

The same controller must accept an explicit target path/repository identity. No project names, commands, language, branch or directory are hard-coded. Project-local rules override generic defaults; missing project-specific verification is reported as unverified, not invented.
