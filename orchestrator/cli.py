"""Small local CLI using deterministic fake providers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .controller import LoopController
from .gates import GateStore, GateValidationError
from .events import TransitionLog
from .state_machine import StateMachine
from .artifacts import ArtifactStore
from .providers import FakeExecutor, FakePlanner, FakeReviewer
from .repository import RepositoryAdapter
from .state_store import StateStore
from .verification import discover_commands
from .config import OrchestratorConfig
from .factory import build_providers


def main(argv: list[str] | None = None) -> int:
    if argv and argv[0] not in {"run", "plan", "status", "resume", "abort", "gates", "approve", "reject", "request-gate", "artifacts", "validate", "doctor", "tasks", "runs", "recover-lock"}:
        argv = ["run", *argv]
    parser = argparse.ArgumentParser(prog="bran-agent-orchestrate")
    parser.add_argument("command", choices=["run", "plan", "status", "resume", "abort", "gates", "approve", "reject", "request-gate", "artifacts", "validate", "doctor", "tasks", "runs", "recover-lock"], nargs="?", default="run")
    parser.add_argument("repository")
    parser.add_argument("goal", nargs="?")
    parser.add_argument("--approve-human-gate", action="store_true")
    parser.add_argument("--gate-id")
    parser.add_argument("--actor", default="human")
    parser.add_argument("--reason", default="")
    args = parser.parse_args(argv)
    root = Path(args.repository).resolve()
    store = StateStore(root / ".orchestrator" / "state.json")
    gates = GateStore(root / ".orchestrator" / "approvals")
    artifacts = ArtifactStore(root / ".orchestrator")
    if args.command == "gates":
        print(json.dumps(gates.list(), ensure_ascii=False))
        return 0
    if args.command == "artifacts":
        print(json.dumps({"runs": artifacts.list_runs(), "tasks": artifacts.list_tasks(), "state": store.load()}, ensure_ascii=False))
        return 0
    if args.command == "runs":
        print(json.dumps(artifacts.list_runs(), ensure_ascii=False))
        return 0
    if args.command == "tasks":
        print(json.dumps(artifacts.list_tasks(), ensure_ascii=False))
        return 0
    if args.command == "recover-lock":
        print(json.dumps(store.recover_lock(explicit=True), ensure_ascii=False))
        return 0
    if args.command in {"approve", "reject"}:
        if not args.gate_id:
            parser.error("--gate-id is required")
        try:
            gate = gates.decide(args.gate_id, "APPROVED" if args.command == "approve" else "REJECTED", actor=args.actor, reason=args.reason)
        except GateValidationError as exc:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
            return 1
        print(json.dumps(gate, ensure_ascii=False))
        return 0
    if args.command == "validate":
        print(json.dumps({"commands": discover_commands(root)}, ensure_ascii=False))
        return 0
    if args.command == "request-gate":
        if not args.gate_id or not args.reason:
            parser.error("--gate-id and --reason are required")
        snapshot = RepositoryAdapter(root).inspect()
        gate = gates.create(goal_id="cli-goal", plan_id=None, task_id=args.gate_id, repository_revision=snapshot.revision or "unknown", scope=[], reason=args.reason)
        print(json.dumps(gate, ensure_ascii=False))
        return 0
    if args.command == "doctor":
        config = OrchestratorConfig.from_environment()
        checks = {"repository": root.is_dir(), "orchestrator_directory": (root / ".orchestrator").is_dir(), "verification_commands": discover_commands(root), "providers": {"planner": config.planner_provider, "executor": config.executor_provider, "reviewer": config.reviewer_provider}}
        print(json.dumps(checks, ensure_ascii=False))
        return 0 if checks["repository"] else 1
    if args.command == "status":
        print(json.dumps(store.load() or {"state": "NEW"}, ensure_ascii=False))
        return 0
    if args.command == "abort":
        snapshot = RepositoryAdapter(root).inspect()
        current = (store.load() or {"state": "NEW"})["state"]
        context = {"reason": "user requested abort", "repository_revision": snapshot.revision or "unknown"}
        StateMachine().transition(current, "ABORTED", "Human", context)
        saved = store.save({**context, "state": "ABORTED"}, repository_revision=snapshot.revision or "unknown")
        TransitionLog(root / ".orchestrator" / "events.jsonl").append(from_state=current, to_state="ABORTED", actor="Human", reason="user requested abort", context=saved)
        return 0
    if not args.goal:
        parser.error("goal is required for run, plan, and resume")
    goal = {"schema_version": "1.0", "goal_id": "cli-goal", "objective": args.goal, "repository": {"path": str(root)}, "constraints": [], "acceptance_criteria": [], "risk_level": "low"}
    if args.command == "plan":
        print(json.dumps(FakePlanner().create_plan(goal), ensure_ascii=False))
        return 0
    try:
        planner, executor, reviewer = build_providers(OrchestratorConfig.from_environment(), repository_root=root)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1
    result = LoopController(RepositoryAdapter(root), store, planner, executor, reviewer).run(goal, human_approved=args.approve_human_gate)
    print(json.dumps({"state": result.state, "task_id": result.task_id, "human_reason": result.human_reason}, ensure_ascii=False))
    return 0 if result.state == "COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
