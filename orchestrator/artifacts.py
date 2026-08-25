"""Safe, atomic persistence for the small Phase 03B artifact set."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Mapping


class ArtifactValidationError(ValueError):
    pass


_SAFE_ID = re.compile(r"^[A-Za-z0-9._-]+$")


def _redact(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _redact(v) for k, v in value.items() if str(k).lower() not in {"prompt", "stdout", "stderr", "environment", "env"}}
    if isinstance(value, list):
        return [_redact(v) for v in value]
    if isinstance(value, str):
        return value[:4000]
    return value


class ArtifactStore:
    """Persist only bounded, JSON-safe workflow artifacts below one root."""

    def __init__(self, root: str | os.PathLike[str]) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.tasks = self.root / "tasks"
        self.runs = self.root / "runs"
        self.tasks.mkdir(exist_ok=True)
        self.runs.mkdir(exist_ok=True)

    def _path(self, directory: Path, artifact_id: str, suffix: str = ".json") -> Path:
        if not isinstance(artifact_id, str) or not _SAFE_ID.fullmatch(artifact_id):
            raise ArtifactValidationError("invalid artifact id")
        path = (directory / f"{artifact_id}{suffix}").resolve()
        if self.root not in path.parents:
            raise ArtifactValidationError("artifact path escapes root")
        return path

    def write(self, artifact: Mapping[str, Any], *, artifact_id: str, kind: str) -> dict[str, Any]:
        data = dict(_redact(artifact))
        if data.get("schema_version") != "1.0":
            raise ArtifactValidationError("unsupported schema_version")
        if kind == "goal":
            path = self._path(self.root, artifact_id)
        elif kind == "plan":
            path = self._path(self.root, "current-plan")
        elif kind == "task":
            path = self._path(self.tasks, artifact_id)
        elif kind == "run":
            path = self._path(self.runs, artifact_id)
        else:
            raise ArtifactValidationError(f"unknown artifact kind: {kind}")
        fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return data

    def read(self, *, artifact_id: str, kind: str) -> dict[str, Any]:
        if kind == "goal":
            path = self._path(self.root, artifact_id)
        elif kind == "plan":
            path = self._path(self.root, "current-plan")
        elif kind == "task":
            path = self._path(self.tasks, artifact_id)
        elif kind == "run":
            path = self._path(self.runs, artifact_id)
        else:
            raise ArtifactValidationError(f"unknown artifact kind: {kind}")
        return json.loads(path.read_text(encoding="utf-8"))

    def list_runs(self) -> list[dict[str, Any]]:
        return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(self.runs.glob("*.json"))]

