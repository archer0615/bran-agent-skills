"""Persisted, single-use human gate approvals."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


STATUSES = {"PENDING", "APPROVED", "REJECTED", "EXPIRED", "CANCELLED"}


class GateValidationError(RuntimeError):
    pass


class GateStore:
    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path(self, gate_id: str) -> Path:
        if not gate_id or Path(gate_id).name != gate_id or gate_id in {".", ".."}:
            raise GateValidationError("invalid gate id")
        return self.directory / f"{gate_id}.json"

    def create(self, *, goal_id: str, plan_id: str | None, task_id: str, repository_revision: str, scope: list[str], reason: str, actor: str = "system", expires_in_seconds: int = 3600) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        gate = {"schema_version": "1.0", "gate_id": uuid.uuid4().hex, "goal_id": goal_id, "plan_id": plan_id, "task_id": task_id, "repository_revision": repository_revision, "status": "PENDING", "actor": actor, "reason": reason[:500], "created_at": now.isoformat(), "decided_at": None, "expires_at": (now + timedelta(seconds=expires_in_seconds)).isoformat(), "scope": list(scope)}
        self._path(gate["gate_id"]).write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return gate

    def get(self, gate_id: str) -> dict[str, Any]:
        path = self._path(gate_id)
        if not path.exists():
            raise GateValidationError("gate not found")
        gate = json.loads(path.read_text(encoding="utf-8"))
        if gate.get("schema_version") != "1.0" or gate.get("status") not in STATUSES:
            raise GateValidationError("invalid gate artifact")
        return gate

    def list(self) -> list[dict[str, Any]]:
        return [self.get(path.stem) for path in sorted(self.directory.glob("*.json"))]

    def decide(self, gate_id: str, status: str, *, actor: str, reason: str = "") -> dict[str, Any]:
        if status not in {"APPROVED", "REJECTED", "CANCELLED"}:
            raise GateValidationError("invalid decision")
        gate = self.get(gate_id)
        if gate["status"] != "PENDING":
            raise GateValidationError("gate already decided or expired")
        if datetime.fromisoformat(gate["expires_at"]) <= datetime.now(timezone.utc):
            gate["status"] = "EXPIRED"
            self._path(gate_id).write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")
            raise GateValidationError("gate expired")
        gate.update({"status": status, "actor": actor, "reason": reason[:500], "decided_at": datetime.now(timezone.utc).isoformat()})
        self._path(gate_id).write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return gate

    def validate_approval(self, gate_id: str, *, task_id: str, repository_revision: str, scope: list[str]) -> dict[str, Any]:
        gate = self.get(gate_id)
        if gate["status"] != "APPROVED" or gate.get("task_id") != task_id or gate.get("repository_revision") != repository_revision or gate.get("scope") != list(scope):
            raise GateValidationError("approval does not match task, revision or scope")
        if datetime.fromisoformat(gate["expires_at"]) <= datetime.now(timezone.utc):
            raise GateValidationError("approval expired")
        gate["status"] = "CANCELLED"
        self._path(gate_id).write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return gate

