"""Centralized, fail-closed lifecycle transition rules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


STATES = frozenset({
    "NEW", "PLANNING", "READY", "EXECUTING", "VERIFYING", "REVIEWING",
    "REPLAN_REQUIRED", "BLOCKED", "NEEDS_HUMAN", "COMPLETED", "FAILED", "ABORTED",
})
TERMINAL_STATES = frozenset({"COMPLETED", "FAILED", "ABORTED"})


@dataclass(frozen=True)
class Transition:
    from_state: str
    to_state: str
    owner: str
    required_context: tuple[str, ...] = ()
    terminal: bool = False


def _rules() -> tuple[Transition, ...]:
    rows = [
        ("NEW", "PLANNING", "Controller", ("goal_id",)),
        ("PLANNING", "READY", "Planner", ("goal_id", "plan_id", "task_id")),
        ("PLANNING", "NEEDS_HUMAN", "Planner", ("goal_id", "reason")),
        ("READY", "EXECUTING", "Controller", ("task_id",)),
        ("EXECUTING", "VERIFYING", "Executor", ("task_id", "execution_result")),
        ("EXECUTING", "BLOCKED", "Controller", ("task_id", "reason")),
        ("EXECUTING", "NEEDS_HUMAN", "Controller", ("task_id", "reason")),
        ("EXECUTING", "FAILED", "Controller", ("task_id", "reason")),
        ("VERIFYING", "REVIEWING", "Controller", ("task_id", "verification")),
        ("VERIFYING", "EXECUTING", "Controller", ("task_id", "retry")),
        ("VERIFYING", "FAILED", "Controller", ("task_id", "reason")),
        ("REVIEWING", "COMPLETED", "Reviewer", ("task_id", "review")),
        ("REVIEWING", "REPLAN_REQUIRED", "Reviewer", ("task_id", "review")),
        ("REVIEWING", "BLOCKED", "Reviewer", ("task_id", "reason")),
        ("REVIEWING", "NEEDS_HUMAN", "Reviewer", ("task_id", "reason")),
        ("REVIEWING", "FAILED", "Reviewer", ("task_id", "reason")),
        ("REPLAN_REQUIRED", "PLANNING", "Controller", ("goal_id", "plan_revision")),
        ("BLOCKED", "PLANNING", "Controller", ("goal_id", "recovery")),
        ("BLOCKED", "ABORTED", "Human", ("reason",)),
        ("NEEDS_HUMAN", "READY", "Human", ("task_id", "approval")),
        ("NEEDS_HUMAN", "PLANNING", "Human", ("goal_id", "approval")),
        ("NEEDS_HUMAN", "ABORTED", "Human", ("reason",)),
    ]
    rows.extend((state, "ABORTED", "Human", ("reason",)) for state in sorted(STATES - TERMINAL_STATES) if state not in {"BLOCKED", "NEEDS_HUMAN"})
    return tuple(Transition(a, b, c, tuple(d), b in TERMINAL_STATES) for a, b, c, d in rows)


TRANSITIONS = _rules()


class InvalidTransitionError(RuntimeError):
    """Raised for an unknown, unauthorized, stale or incomplete transition."""


class StateMachine:
    transitions = TRANSITIONS

    def transition(self, current_state: str, target_state: str, actor: str, context: Mapping[str, Any]) -> Transition:
        if current_state not in STATES or target_state not in STATES:
            raise InvalidTransitionError("unknown state")
        if current_state in TERMINAL_STATES:
            raise InvalidTransitionError("terminal state cannot transition")
        rule = next((r for r in self.transitions if r.from_state == current_state and r.to_state == target_state), None)
        if rule is None or actor not in {rule.owner, "Controller"}:
            raise InvalidTransitionError(f"transition {current_state}->{target_state} is not allowed for {actor}")
        missing = [key for key in rule.required_context if key not in context or context[key] in (None, "")]
        if missing:
            raise InvalidTransitionError(f"missing transition context: {', '.join(missing)}")
        if context.get("stale_repository"):
            raise InvalidTransitionError("stale repository revision")
        if target_state == "NEEDS_HUMAN":
            approval = context.get("approval")
            if approval is not None and approval.get("status") != "APPROVED":
                raise InvalidTransitionError("human gate approval is not valid")
        return rule
