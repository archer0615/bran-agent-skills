"""Versioned, atomic persistence for a local orchestrator checkpoint."""

from __future__ import annotations

import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Mapping


class StateValidationError(ValueError):
    """Raised when a persisted state does not satisfy the minimum contract."""


class StateConflictError(RuntimeError):
    """Raised when a state write would overwrite a newer repository revision."""


class StateStore:
    """Persist a single state document without silently overwriting newer state."""

    schema_version = "1.0"

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = Path(path)

    def load(self) -> dict[str, Any] | None:
        if not self.path.exists():
            return None
        with self.path.open("r", encoding="utf-8") as handle:
            state = json.load(handle)
        self._validate(state)
        return state

    @contextmanager
    def lock(self):
        """Acquire a process-level lock; fail instead of clobbering a run."""
        lock_path = self.path.with_suffix(self.path.suffix + ".lock")
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise StateConflictError(f"state lock exists: {lock_path}") from exc
        try:
            os.write(fd, str(os.getpid()).encode("ascii"))
            yield
        finally:
            os.close(fd)
            lock_path.unlink(missing_ok=True)

    def save(
        self,
        state: Mapping[str, Any],
        *,
        repository_revision: str,
        expected_repository_revision: str | None = None,
    ) -> dict[str, Any]:
        """Atomically write state, rejecting stale writers.

        ``expected_repository_revision`` is the revision observed before work
        started. A mismatch means another run has advanced the checkpoint.
        """
        candidate = dict(state)
        candidate["schema_version"] = self.schema_version
        candidate["repository_revision"] = repository_revision
        self._validate(candidate)

        current = self.load()
        if (
            current is not None
            and expected_repository_revision is not None
            and current["repository_revision"] != expected_repository_revision
        ):
            raise StateConflictError(
                "state revision changed from "
                f"{expected_repository_revision!r} to {current['repository_revision']!r}"
            )

        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(
            prefix=f".{self.path.name}.", suffix=".tmp", dir=self.path.parent
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                json.dump(candidate, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return candidate

    @classmethod
    def _validate(cls, state: Any) -> None:
        if not isinstance(state, dict):
            raise StateValidationError("state must be a JSON object")
        if state.get("schema_version") != cls.schema_version:
            raise StateValidationError("unsupported or missing schema_version")
        if not isinstance(state.get("repository_revision"), str) or not state[
            "repository_revision"
        ]:
            raise StateValidationError("repository_revision must be a non-empty string")
        if "state" not in state or not isinstance(state["state"], str):
            raise StateValidationError("state must contain a string 'state' field")
