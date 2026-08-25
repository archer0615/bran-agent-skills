"""Versioned atomic state persistence, backups and explicit lock recovery."""

from __future__ import annotations

import json
import os
import socket
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

from .state_machine import STATES
from .events import TransitionLog


class StateValidationError(ValueError):
    """Persisted state is malformed or unsupported."""


class StateCorruptionError(StateValidationError):
    """Primary state is corrupt; it was not treated as NEW."""


class StateConflictError(RuntimeError):
    """A concurrent or stale writer/recovery was rejected."""


class StateStore:
    schema_version = "1.0"

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = Path(path)
        self.backup_path = self.path.with_name("state.backup.json")
        self.lock_path = self.path.with_suffix(self.path.suffix + ".lock")

    def load(self) -> dict[str, Any] | None:
        if not self.path.exists():
            return None
        try:
            state = json.loads(self.path.read_text(encoding="utf-8"))
            self._validate(state)
            return state
        except (OSError, json.JSONDecodeError, StateValidationError) as exc:
            raise StateCorruptionError("primary state is corrupt") from exc

    def load_backup(self) -> dict[str, Any] | None:
        if not self.backup_path.exists():
            return None
        try:
            state = json.loads(self.backup_path.read_text(encoding="utf-8"))
            self._validate(state)
            return state
        except (OSError, json.JSONDecodeError, StateValidationError) as exc:
            raise StateCorruptionError("backup state is corrupt") from exc

    def recover_from_backup(self, *, repository_revision: str, expected_repository_revision: str | None = None) -> dict[str, Any]:
        backup = self.load_backup()
        if backup is None:
            raise StateConflictError("no backup available for recovery")
        if backup["repository_revision"] != repository_revision:
            raise StateConflictError("backup repository revision is stale")
        if expected_repository_revision is not None and backup["repository_revision"] != expected_repository_revision:
            raise StateConflictError("backup does not match expected repository revision")
        recovered = dict(backup)
        recovered["repository_revision"] = repository_revision
        self._atomic_write(self.path, recovered)
        TransitionLog(self.path.parent / "events.jsonl").append(from_state=recovered["state"], to_state=recovered["state"], actor="Recovery", reason="state recovered from backup", context=recovered)
        return recovered

    @contextmanager
    def lock(self, *, run_id: str | None = None, expires_in_seconds: int = 3600):
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc)
        metadata = {"lock_id": uuid.uuid4().hex, "pid": os.getpid(), "hostname": socket.gethostname(), "created_at": now.isoformat(), "heartbeat_at": now.isoformat(), "expires_at": (now + timedelta(seconds=expires_in_seconds)).isoformat(), "repository": str(self.path.parent.parent.resolve()), "run_id": run_id or uuid.uuid4().hex}
        try:
            fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise StateConflictError(f"state lock exists: {self.lock_path}") from exc
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(metadata, handle, sort_keys=True)
                handle.write("\n")
            yield metadata
        finally:
            self.lock_path.unlink(missing_ok=True)

    def lock_status(self) -> str:
        if not self.lock_path.exists():
            return "stale"
        try:
            metadata = json.loads(self.lock_path.read_text(encoding="utf-8"))
            required = ("lock_id", "pid", "hostname", "expires_at", "repository", "run_id")
            if not all(key in metadata for key in required):
                return "unknown"
            expired = datetime.fromisoformat(metadata["expires_at"]) <= datetime.now(timezone.utc)
            same_host = metadata["hostname"] == socket.gethostname()
            process_exists = same_host and _process_exists(int(metadata["pid"]))
            return "active" if process_exists and not expired else ("stale" if same_host else "unknown")
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return "unknown"

    def recover_lock(self, *, explicit: bool = False) -> dict[str, str]:
        status = self.lock_status()
        if status != "stale" or not explicit:
            raise StateConflictError(f"lock recovery refused: {status}")
        self.lock_path.unlink(missing_ok=True)
        TransitionLog(self.path.parent / "events.jsonl").append(from_state="LOCKED", to_state="LOCKED", actor="Recovery", reason="stale lock explicitly recovered", context={"repository_revision": None})
        return {"action": "recovered", "status": status}

    def save(self, state: Mapping[str, Any], *, repository_revision: str, expected_repository_revision: str | None = None, make_backup: bool = True) -> dict[str, Any]:
        candidate = dict(state)
        candidate["schema_version"] = self.schema_version
        candidate["repository_revision"] = repository_revision
        self._validate(candidate)
        current = self.load()
        if current is not None and expected_repository_revision is not None and current["repository_revision"] != expected_repository_revision:
            raise StateConflictError(f"state revision changed from {expected_repository_revision!r} to {current['repository_revision']!r}")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if make_backup and current is not None:
            self._atomic_write(self.backup_path, current)
        self._atomic_write(self.path, candidate)
        return candidate

    @staticmethod
    def _atomic_write(path: Path, value: Mapping[str, Any]) -> None:
        fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @classmethod
    def _validate(cls, state: Any) -> None:
        if not isinstance(state, dict):
            raise StateValidationError("state must be a JSON object")
        if state.get("schema_version") != cls.schema_version:
            raise StateValidationError("unsupported or missing schema_version")
        if not isinstance(state.get("repository_revision"), str) or not state["repository_revision"]:
            raise StateValidationError("repository_revision must be a non-empty string")
        if not isinstance(state.get("state"), str) or state["state"] not in STATES:
            raise StateValidationError("state must contain a known state")
        for field in ("goal_id", "plan_id", "task_id"):
            if field in state and (not isinstance(state[field], str) or not state[field]):
                raise StateValidationError(f"{field} must be a non-empty string")


def _process_exists(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except (OSError, ProcessLookupError):
        return False
    return True
