"""Small fail-closed safety helpers for local orchestration."""

from __future__ import annotations

import re
from pathlib import Path


class SecurityPolicyError(ValueError):
    pass


_SECRET = re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s,;]+")
_FORBIDDEN = {"commit", "push", "merge", "rebase", "reset", "deploy", "release"}


def redact(text: str) -> str:
    return _SECRET.sub(lambda match: match.group(0).split("=", 1)[0].split(":", 1)[0] + "=[REDACTED]", text)


def validate_command(command: list[str], *, allow_git_mutation: bool = False) -> list[str]:
    if not command or any(not isinstance(part, str) or not part for part in command):
        raise SecurityPolicyError("command must contain non-empty strings")
    lowered = {part.lower() for part in command}
    if not allow_git_mutation and lowered & _FORBIDDEN:
        raise SecurityPolicyError("mutating or deployment command requires explicit approval")
    return list(command)


def confined_path(root: str | Path, candidate: str | Path) -> Path:
    root_path = Path(root).resolve()
    path = Path(candidate)
    resolved = (root_path / path).resolve() if not path.is_absolute() else path.resolve()
    if resolved != root_path and root_path not in resolved.parents:
        raise SecurityPolicyError("path escapes repository root")
    return resolved
