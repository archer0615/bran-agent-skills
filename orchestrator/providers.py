"""Provider boundaries and deterministic local adapters for Phase 02."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .contracts import validate_artifact


class Planner(Protocol):
    def create_plan(self, goal: dict) -> dict: ...


class Executor(Protocol):
    def execute(self, task: dict) -> dict: ...


class Reviewer(Protocol):
    def review(self, task: dict, execution: dict) -> dict: ...


@dataclass
class FakePlanner:
    task_objective: str | None = None

    def create_plan(self, goal: dict) -> dict:
        task_id = f"{goal['goal_id']}-task-1"
        plan = {
            "schema_version": "1.0", "plan_id": f"{goal['goal_id']}-plan-1",
            "goal_id": goal["goal_id"], "tasks": [{"task_id": task_id, "objective": self.task_objective or goal["objective"], "dependencies": []}],
            "dependencies": [], "sequence": [task_id], "risks": [], "human_gates": [],
        }
        return validate_artifact("plan", plan)


@dataclass
class FakeExecutor:
    status: str = "completed"
    changed_files: tuple[str, ...] = ()

    def execute(self, task: dict) -> dict:
        result = {
            "schema_version": "1.0", "task_id": task["task_id"], "status": self.status,
            "changed_files": list(self.changed_files), "commands_run": [], "verification_results": [],
            "known_issues": [], "blocked_reason": None if self.status == "completed" else "fake status",
            "evidence": [{"kind": "manual", "ref": "fake-executor"}],
        }
        return validate_artifact("execution_result", result)


@dataclass
class FakeReviewer:
    decision: str = "PASS"

    def review(self, task: dict, execution: dict) -> dict:
        result = {
            "schema_version": "1.0", "task_id": task["task_id"], "decision": self.decision,
            "acceptance_results": [{"criterion_id": str(i), "result": "pass" if self.decision == "PASS" else "unverified", "evidence_refs": ["fake-executor"]} for i, _ in enumerate(task.get("acceptance_criteria", []), 1)],
            "issues": [] if self.decision == "PASS" else ["fake reviewer decision"],
            "required_corrections": [] if self.decision == "PASS" else ["replan"],
            "risk_findings": [], "next_action": "finish" if self.decision == "PASS" else "replan",
        }
        return validate_artifact("review_result", result)
