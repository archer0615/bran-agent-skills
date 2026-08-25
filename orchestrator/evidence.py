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


def run_verification(root: str | Path, command: list[str]) -> CommandEvidence:
    result = subprocess.run(command, cwd=Path(root), check=False, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    return CommandEvidence(" ".join(command), result.returncode, output[-2000:])


def evidence_dict(evidence: CommandEvidence) -> dict:
    return asdict(evidence)
