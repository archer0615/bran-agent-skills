"""Small local CLI using deterministic fake providers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .controller import LoopController
from .providers import FakeExecutor, FakePlanner, FakeReviewer
from .repository import RepositoryAdapter
from .state_store import StateStore


def main(argv: list[str] | None = None) -> int:
    if argv and argv[0] not in {"run", "plan", "status", "resume", "abort"}:
        argv = ["run", *argv]
    parser = argparse.ArgumentParser(prog="bran-agent-orchestrate")
    parser.add_argument("command", choices=["run", "plan", "status", "resume", "abort"], nargs="?", default="run")
    parser.add_argument("repository")
    parser.add_argument("goal", nargs="?")
    parser.add_argument("--approve-human-gate", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.repository).resolve()
    store = StateStore(root / ".orchestrator" / "state.json")
    if args.command == "status":
        print(json.dumps(store.load() or {"state": "NEW"}, ensure_ascii=False))
        return 0
    if args.command == "abort":
        snapshot = RepositoryAdapter(root).inspect()
        store.save({"state": "ABORTED", "reason": "user requested abort"}, repository_revision=snapshot.revision or "unknown")
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
