"""Append-only, redacted transition event persistence."""

from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


_SECRET = re.compile(r"(?i)(api[_-]?key|token|password|secret|authorization)=([^\s,]+)")


def _safe(value: Any) -> Any:
    if isinstance(value, str):
        return _SECRET.sub(r"\1=[REDACTED]", value)[:500]
    if isinstance(value, Mapping):
        return {str(k): _safe(v) for k, v in value.items() if str(k).lower() not in {"prompt", "stdout", "stderr", "environment", "env"}}
    if isinstance(value, (list, tuple)):
        return [_safe(v) for v in value]
    return value


class TransitionLog:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def append(self, *, from_state: str, to_state: str, actor: str, reason: str, context: Mapping[str, Any]) -> dict[str, Any]:
        event = {"event_id": uuid.uuid4().hex, "timestamp": datetime.now(timezone.utc).isoformat(), "from": from_state, "to": to_state, "actor": actor, "reason": _safe(reason), "goal_id": context.get("goal_id"), "plan_id": context.get("plan_id"), "task_id": context.get("task_id"), "repository_revision": context.get("repository_revision")}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        return event

    def list(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line]

