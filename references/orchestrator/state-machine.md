# State machine

## States

`NEW` accepts a Goal. `PLANNING` creates or revises a Plan. `READY` has an executable Task and no unresolved gate. `EXECUTING` runs one Task. `VERIFYING` collects reproducible checks and evidence. `REVIEWING` performs independent review. `REPLAN_REQUIRED` records correctable findings. `BLOCKED` waits for an environment, dependency or external decision. `NEEDS_HUMAN` waits for explicit approval or clarification. `COMPLETED` and `ABORTED` are terminal by user/workflow choice; `FAILED` is terminal for exhausted or non-correctable failure.

## Allowed transitions

| From | To | Owner | Required condition |
|---|---|---|---|
| NEW | PLANNING | Controller | valid Goal |
| PLANNING | READY | Planner/Controller | valid Plan and executable Task |
| PLANNING | NEEDS_HUMAN | Planner | ambiguity or scope/risk decision |
| READY | EXECUTING | Controller | gates clear, lock acquired |
| EXECUTING | VERIFYING | Executor/Controller | execution result emitted |
| EXECUTING | BLOCKED / NEEDS_HUMAN / FAILED | Controller | classified failure or gate |
| VERIFYING | REVIEWING | Controller | evidence recorded, checks complete or explicitly unverified |
| VERIFYING | EXECUTING | Controller | bounded verification retry allowed |
| REVIEWING | COMPLETED | Reviewer/Controller | `PASS`, all criteria pass |
| REVIEWING | REPLAN_REQUIRED | Reviewer/Controller | `REPLAN`, correctable issues |
| REVIEWING | BLOCKED / NEEDS_HUMAN / FAILED | Reviewer/Controller | external block, approval, or non-correctable finding |
| REPLAN_REQUIRED | PLANNING | Controller | revision budget remains |
| BLOCKED / NEEDS_HUMAN | PLANNING / READY / ABORTED | Controller/Human | blocker resolved or user aborts |
| any non-terminal | ABORTED | Human/Controller | explicit abort or safety stop |

Each transition records actor, timestamp, input artifact ids, repository revision, reason, and output state. `COMPLETED`, `FAILED`, and `ABORTED` have no automatic outgoing transition.

## Bounded loop policy

Defaults are configurable per Goal but conservative: maximum 2 execution retries per Task, 3 Plan revisions per Goal, and 1 verification retry per Task. Exhaustion becomes `FAILED` or `NEEDS_HUMAN` when a human can resolve the cause. Implementation defects may retry; requirement ambiguity replans; environment failures block; architecture/security/destructive conflicts escalate; unsupported external dependency failure blocks or aborts. No state may silently loop.
