"""Structured command evidence capture."""

from __future__ import annotations

import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommandEvidence:
    command: str
    exit_code: int
    summary: str


def run_verification(root: str | Path, command: list[str], *, timeout_seconds: int = 300) -> CommandEvidence:
    try:
        result = subprocess.run(command, cwd=Path(root), check=False, capture_output=True, text=True, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        output = ((exc.stdout or "") + (exc.stderr or "")).strip()
        return CommandEvidence(" ".join(command), 124, (output + "\nverification timed out")[-2000:])
    output = (result.stdout + result.stderr).strip()
    return CommandEvidence(" ".join(command), result.returncode, output[-2000:])


def evidence_dict(evidence: CommandEvidence) -> dict:
    return asdict(evidence)
