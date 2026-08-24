---
name: context-management
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when a task has a long conversation, many files, competing instructions, or risk of losing important context.
---

# Context Management

## Use when

Use this skill when a task has a long conversation, many files, competing instructions, handoffs, or a meaningful risk of losing decisions and evidence.

## Inputs

- Required: Current objective, scope, decisions, evidence, files, status, and next action.
- Optional: Prior handoff, conversation history, blockers, deadlines, and verification logs.
- Preconditions: Task state can be reconstructed from authoritative sources.
- Missing information: Mark facts unknown or unverified; do not fill gaps with transcript inference.
- Output artifact: Compact state or handoff with verified status, open questions, files, evidence, blockers, and resume action.

## Procedure

1. Maintain compact task state with objective, scope, constraints, decisions, open questions, evidence, files, current status, and next action.
2. Prefer authoritative and recent evidence. Record where each important fact came from and distinguish user instructions, repository rules, observed state, assumptions, and recommendations.
3. Summarize before context grows: preserve decisions and unresolved items, remove repetition, and keep exact paths or commands needed to resume work.
4. Reconcile conflicts by authority and recency. Do not silently discard a higher-priority instruction or a newer verified state.
5. At handoff, provide the current objective, completed work, remaining work, blockers, changed files, verification evidence, and the first safe next action.

-
## Decision rules

- Preserve information that affects scope, safety, acceptance, routing, or verification; compress incidental narrative.
- Distinguish planned, attempted, verified, blocked, deferred, and unverified work.
- Resolve conflicts by authority and recency, recording superseded constraints and decisions.
- Treat uncommitted files and user changes as protected context.

## Verification

- Another agent can identify the current objective and next action without rereading the full conversation.
- Decisions, assumptions, evidence, and open questions are clearly separated.
- File paths and verification results match the repository state.
- No secret, personal data, or unnecessary transcript content is retained.

## Output

Return the structured artifact, assumptions, unresolved questions, and concrete verification or review criteria. Communicate with the user in Traditional Chinese unless another language is requested.

