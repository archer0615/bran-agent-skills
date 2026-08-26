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


def main(argv: list[str] | None = None) -> int:
    if argv and argv[0] not in {"run", "plan", "status", "resume", "abort", "gates", "approve", "reject", "artifacts", "validate", "doctor"}:
        argv = ["run", *argv]
    parser = argparse.ArgumentParser(prog="bran-agent-orchestrate")
    parser.add_argument("command", choices=["run", "plan", "status", "resume", "abort", "gates", "approve", "reject", "artifacts", "validate", "doctor"], nargs="?", default="run")
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
        print(json.dumps({"runs": artifacts.list_runs(), "state": store.load()}, ensure_ascii=False))
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
    if args.command == "doctor":
        checks = {"repository": root.is_dir(), "orchestrator_directory": (root / ".orchestrator").is_dir(), "verification_commands": discover_commands(root)}
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
    result = LoopController(RepositoryAdapter(root), store, FakePlanner(), FakeExecutor(), FakeReviewer()).run(goal, human_approved=args.approve_human_gate)
    print(json.dumps({"state": result.state, "task_id": result.task_id, "human_reason": result.human_reason}, ensure_ascii=False))
    return 0 if result.state == "COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
