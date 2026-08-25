"""Deterministic bounded Planner → Executor → Reviewer control flow."""

from __future__ import annotations

from dataclasses import dataclass

from .providers import Executor, Planner, Reviewer
from .repository import RepositoryAdapter
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

    def run(self, goal: dict, *, human_approved: bool = False) -> RunResult:
        snapshot = self.repository.inspect()
        state = self.store.load()
        if state and state.get("state") == "NEEDS_HUMAN" and not human_approved:
            return RunResult("NEEDS_HUMAN", state.get("task_id"), None, state.get("reason"))
        for plan_revision in range(self.max_replans + 1):
            self.store.save({"state": "PLANNING", "goal_id": goal["goal_id"], "plan_revision": plan_revision}, repository_revision=snapshot.revision or "unknown")
            plan = self.planner.create_plan(goal)
            task = dict(plan["tasks"][0])
            task.update({"schema_version": "1.0", "plan_id": plan["plan_id"], "scope": [], "allowed_changes": [], "forbidden_changes": [], "acceptance_criteria": goal.get("acceptance_criteria", []), "required_verification": [], "risk_level": goal["risk_level"]})
            execution = None
            for retry in range(self.max_execution_retries + 1):
                self.store.save({"state": "EXECUTING", "goal_id": goal["goal_id"], "task_id": task["task_id"], "execution_retry": retry}, repository_revision=snapshot.revision or "unknown", expected_repository_revision=snapshot.revision or "unknown")
                execution = self.executor.execute(task)
                if execution["status"] == "completed" or execution["status"] in {"blocked", "aborted"}:
                    break
            assert execution is not None
            if execution["status"] != "completed":
                next_state = "BLOCKED" if execution["status"] == "blocked" else execution["status"].upper()
                self.store.save({"state": next_state, "task_id": task["task_id"], "reason": execution["blocked_reason"]}, repository_revision=snapshot.revision or "unknown")
                return RunResult(next_state, task["task_id"], None, execution["blocked_reason"])
            review = self.reviewer.review(task, execution)
            if review["decision"] == "PASS":
                self.store.save({"state": "COMPLETED", "task_id": task["task_id"], "review_decision": "PASS"}, repository_revision=snapshot.revision or "unknown")
                return RunResult("COMPLETED", task["task_id"], review)
            if review["decision"] != "REPLAN":
                next_state = {"BLOCKED": "BLOCKED", "NEEDS_HUMAN": "NEEDS_HUMAN"}.get(review["decision"], "FAILED")
                self.store.save({"state": next_state, "task_id": task["task_id"], "review_decision": review["decision"]}, repository_revision=snapshot.revision or "unknown")
                return RunResult(next_state, task["task_id"], review)
            if plan_revision == self.max_replans:
                self.store.save({"state": "FAILED", "task_id": task["task_id"], "reason": "plan revision limit exceeded"}, repository_revision=snapshot.revision or "unknown")
                return RunResult("FAILED", task["task_id"], review, "plan revision limit exceeded")
        raise AssertionError("bounded plan loop did not return")
