---
name: human-review-workflow
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when designing a safe human review step for AI-generated or automated outputs.
---

# Human Review Workflow

## Use when

Use this skill when AI-generated or automated output needs a defined human approval, correction, escalation, or rollback step before acceptance or action.

## Inputs

- Required: Automated output, affected decision or action, reviewer authority, approval criteria, and risk level.
- Optional: Evidence requirements, queues, SLAs, audit fields, escalation contacts, and rollback mechanism.
- Preconditions: A human owner can approve, reject, correct, or escalate the output.
- Missing information: Stop action and mark the workflow not ready when authority, evidence, or rollback is undefined.
- Output artifact: Review workflow with gates, roles, decisions, audit trail, escalation, rejection, and rollback paths.

## Procedure

1. Define the output, affected parties, action boundary, reviewer role, authority, and completion state.
2. Set review criteria, required evidence, confidence or uncertainty thresholds, and explicit escalation conditions.
3. Specify how the reviewer inspects, approves, rejects, requests correction, or delegates the decision.
4. Require approval before high-impact, external, irreversible, or security-sensitive actions.
5. Record the decision, reviewer, evidence, timestamp, corrections, exceptions, and audit trail without retaining unnecessary sensitive data.
6. Define rollback, incident handling, and re-review when output or context changes.

## Decision rules

- Require approval before high-impact, irreversible, external, security-sensitive, or legally consequential actions.
- Escalate when evidence is missing or conflicting, uncertainty is below threshold, or the reviewer lacks authority.
- Rejection must stop or quarantine downstream action; correction must preserve the original and record the change.

## Verification

- Reviewer authority and acceptance criteria are unambiguous.
- High-impact and irreversible actions cannot bypass approval.
- Rejection, correction, escalation, audit, and rollback paths are testable.
- Completion requires evidence of the required review.

## Output

Return the workflow, roles, criteria, escalation thresholds, evidence record, rollback path, assumptions, unresolved questions, and verification criteria. Communicate with the user in Traditional Chinese unless another language is requested.

## Example

For an AI-generated financial recommendation that can trigger an external action, quarantine the action until an authorized reviewer confirms evidence, records a decision, or escalates the case; preserve rollback and re-review paths.

