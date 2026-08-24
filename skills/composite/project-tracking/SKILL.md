---
name: project-tracking
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when turning project updates into a concise status report, risk register, or follow-up plan.
---

# Project Tracking

## Use when

Use this skill when turning project updates or repository evidence into a concise status report, risk register, action list, or follow-up plan.

## Inputs

- Required: Current updates, completed work, open work, risks, blockers, and evidence.
- Optional: Owners, deadlines, dependencies, milestones, baseline plan, and previous status report.
- Preconditions: Status claims can be traced to updates or repository evidence.
- Missing information: Label unverified status and assign an owner or follow-up to close the gap.
- Output artifact: Status summary, risk register, action list, dependencies, and next checkpoint.

## Procedure

1. Collect milestones, progress, deliverables, blockers, decisions, dependencies, owners, dates, and status signals from authoritative sources.
2. Separate completed, in progress, pending, blocked, and unknown work. Do not infer progress from silence.
3. Classify each workstream as on track, at risk, or blocked with the evidence and impact.
4. Produce actions with owner, due date or checkpoint, dependency, and completion signal.
5. Maintain a risk register with likelihood, impact, mitigation, trigger, and escalation owner.
6. Identify the next checkpoint and the smallest action that moves blocked or at-risk work forward.
7. For each material risk, record the trigger that changes its status and the evidence needed to close it; do not use activity volume as a progress proxy.

## Decision rules

- Never invent progress, dates, owners, confidence, or resolution.
- A missed dependency, unresolved decision, or acceptance risk can make a milestone at risk.
- Assign actions an owner, checkpoint, and completion signal when known.
- Separate current state from forecast, assumption, and stale information.
- Escalate blockers affecting the critical path, safety, public commitments, or acceptance criteria.
- Keep status reporting separate from detailed execution notes; link evidence rather than copying unverified narrative.

## Verification

- Status claims trace to dated evidence or are explicitly marked unknown.
- Owners, dependencies, risks, and next checkpoints are not invented.
- Blockers include impact and a concrete resolution or escalation path.
- Completed work is distinguished from planned or merely discussed work.
- Every at-risk or blocked item has a next checkpoint, mitigation, or explicit escalation gap.

## Output

Return the status summary, milestone table, actions, risk register, blockers, assumptions, unresolved questions, and next checkpoint. Communicate with the user in Traditional Chinese unless another language is requested.

