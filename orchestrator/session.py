"""Portable session metadata and resume compatibility checks."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path


class ResumeError(RuntimeError):
    pass


@dataclass(frozen=True)
class Session:
    session_id: str
    repository_root: str
    repository_revision: str

    @classmethod
    def start(cls, repository_root: str | Path, repository_revision: str) -> "Session":
        return cls(uuid.uuid4().hex, str(Path(repository_root).resolve()), repository_revision)

    def validate_resume(self, repository_root: str | Path, repository_revision: str) -> None:
        if self.repository_root != str(Path(repository_root).resolve()):
            raise ResumeError("session belongs to another repository")
        if self.repository_revision != repository_revision:
            raise ResumeError("session repository revision is stale")
