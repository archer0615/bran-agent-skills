"""Bounded Planner → Executor → Reviewer orchestration using safety services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .events import TransitionLog
from .artifacts import ArtifactStore
from .gates import GateStore
from .providers import Executor, Planner, Reviewer
from .repository import RepositoryAdapter
from .state_machine import StateMachine
from .state_store import StateStore


@dataclass
class RunResult:
    state: str
    task_id: str | None
    review: dict | None
    human_reason: str | None = None


class LoopController:
    def __init__(self, repository: RepositoryAdapter, store: StateStore, planner: Planner, executor: Executor, reviewer: Reviewer, *, max_replans: int = 3, max_execution_retries: int = 2) -> None:
        self.repository, self.store = repository, store
        self.planner, self.executor, self.reviewer = planner, executor, reviewer
        self.max_replans, self.max_execution_retries = max_replans, max_execution_retries
        self.machine = StateMachine()
        self.transition_log = TransitionLog(self.store.path.parent / "events.jsonl")
        self.gates = GateStore(self.store.path.parent / "approvals")
        self.artifacts = ArtifactStore(self.store.path.parent)

    def _transition(self, current: str, target: str, *, actor: str, context: dict[str, Any], reason: str, revision: str) -> dict[str, Any]:
        self.machine.transition(current, target, actor, context)
        state = dict(context)
        state.update({"state": target, "reason": reason})
        saved = self.store.save(state, repository_revision=revision, expected_repository_revision=revision if self.store.load() else None)
        self.transition_log.append(from_state=current, to_state=target, actor=actor, reason=reason, context=saved)
        return saved

    def run(self, goal: dict, *, human_approved: bool = False) -> RunResult:
        snapshot = self.repository.inspect()
        revision = snapshot.revision or "unknown"
        state = self.store.load()
        current = state["state"] if state else "NEW"
        if state and state["repository_revision"] != revision:
            return RunResult("BLOCKED", state.get("task_id"), None, "stale repository revision")
        if current in {"COMPLETED", "FAILED", "ABORTED"}:
            return RunResult(current, state.get("task_id") if state else None, None, "terminal state requires a new run")
        if current == "NEEDS_HUMAN" and not human_approved:
            return RunResult(current, state.get("task_id"), None, state.get("reason"))
        if current == "NEEDS_HUMAN" and human_approved:
            gate = self.gates.get(state.get("gate_id", ""))
            if gate["status"] != "APPROVED":
                return RunResult(current, state.get("task_id"), None, "valid persisted approval is required")
        with self.store.lock(run_id=goal.get("goal_id")):
            self.artifacts.write(goal, artifact_id=goal["goal_id"], kind="goal")
            plan_revision = int((state or {}).get("plan_revision", -1)) + 1
            for revision_number in range(plan_revision, self.max_replans + 1):
                context = {"goal_id": goal["goal_id"], "plan_revision": revision_number, "plan_revision_budget": self.max_replans}
                self._transition(current, "PLANNING", actor="Controller", context=context, reason="create or revise plan", revision=revision)
                plan = self.planner.create_plan(goal)
                self.artifacts.write(plan, artifact_id=plan["plan_id"], kind="plan")
                task = dict(plan["tasks"][0])
                task.update({"schema_version": "1.0", "plan_id": plan["plan_id"], "scope": [], "allowed_changes": [], "forbidden_changes": [], "acceptance_criteria": goal.get("acceptance_criteria", []), "required_verification": [], "risk_level": goal["risk_level"]})
                self.artifacts.write(task, artifact_id=task["task_id"], kind="task")
                context.update({"plan_id": plan["plan_id"], "task_id": task["task_id"]})
                self._transition("PLANNING", "READY", actor="Planner", context=context, reason="valid plan and executable task", revision=revision)
                execution = None
                for attempt in range(self.max_execution_retries + 1):
                    context.update({"execution_attempt": attempt, "execution_budget": self.max_execution_retries})
                    self._transition("READY" if attempt == 0 else "VERIFYING", "EXECUTING", actor="Controller", context={**context, "retry": attempt}, reason="execute task", revision=revision)
                    execution = self.executor.execute(task)
                    self.artifacts.write({"schema_version": "1.0", "run_id": f"{task['task_id']}-attempt-{attempt}", "task_id": task["task_id"], "kind": "execution", "execution": execution, "repository_revision": revision}, artifact_id=f"{task['task_id']}-attempt-{attempt}", kind="run")
                    if execution["status"] == "completed":
                        self._transition("EXECUTING", "VERIFYING", actor="Executor", context={**context, "execution_result": execution, "verification": True}, reason="execution result emitted", revision=revision)
                        break
                    if execution["status"] in {"blocked", "aborted"}:
                        target = "BLOCKED" if execution["status"] == "blocked" else "ABORTED"
                        if target == "ABORTED":
                            self._transition("EXECUTING", target, actor="Controller", context={**context, "reason": execution["blocked_reason"] or target}, reason=execution["blocked_reason"] or target, revision=revision)
                        else:
                            self._transition("EXECUTING", target, actor="Controller", context={**context, "reason": execution["blocked_reason"]}, reason=execution["blocked_reason"] or target, revision=revision)
                        return RunResult(target, task["task_id"], None, execution["blocked_reason"])
                    self._transition("EXECUTING", "VERIFYING", actor="Executor", context={**context, "execution_result": execution, "verification": True}, reason="retryable execution result", revision=revision)
                if execution is None or execution["status"] != "completed":
                    self._transition("VERIFYING", "FAILED", actor="Controller", context={**context, "reason": "execution budget exhausted"}, reason="execution budget exhausted", revision=revision)
                    return RunResult("FAILED", task["task_id"], None, "execution budget exhausted")
                review = self.reviewer.review(task, execution)
                self.artifacts.write({"schema_version": "1.0", "run_id": f"{task['task_id']}-review-{revision_number}", "task_id": task["task_id"], "kind": "review", "review": review, "repository_revision": revision}, artifact_id=f"{task['task_id']}-review-{revision_number}", kind="run")
                self._transition("VERIFYING", "REVIEWING", actor="Controller", context={**context, "review": review, "verification": True}, reason="review result emitted", revision=revision)
                if review["decision"] == "PASS":
                    self._transition("REVIEWING", "COMPLETED", actor="Reviewer", context={**context, "review": review}, reason="review passed", revision=revision)
                    return RunResult("COMPLETED", task["task_id"], review)
                if review["decision"] == "REPLAN":
                    if revision_number == self.max_replans:
                        self._transition("REVIEWING", "FAILED", actor="Reviewer", context={**context, "review": review, "reason": "plan revision limit exceeded"}, reason="plan revision limit exceeded", revision=revision)
                        return RunResult("FAILED", task["task_id"], review, "plan revision limit exceeded")
                    self._transition("REVIEWING", "REPLAN_REQUIRED", actor="Reviewer", context={**context, "review": review}, reason="review requires replan", revision=revision)
                    current = "REPLAN_REQUIRED"
                    continue
                target = {"BLOCKED": "BLOCKED", "NEEDS_HUMAN": "NEEDS_HUMAN"}.get(review["decision"], "FAILED")
                if target == "NEEDS_HUMAN":
                    gate = self.gates.create(goal_id=goal["goal_id"], plan_id=plan["plan_id"], task_id=task["task_id"], repository_revision=revision, scope=task.get("scope", []), reason="review requires human decision")
                    context["gate_id"] = gate["gate_id"]
                self._transition("REVIEWING", target, actor="Reviewer", context={**context, "review": review, "reason": review.get("issues", [target])[0] if review.get("issues") else target}, reason=target, revision=revision)
                return RunResult(target, task["task_id"], review)
        raise AssertionError("bounded plan loop did not return")
