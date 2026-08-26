"""Discover conservative project verification commands."""

from __future__ import annotations

import json
from pathlib import Path

from .security import validate_command


def discover_commands(root: str | Path) -> list[list[str]]:
    root = Path(root)
    commands: list[list[str]] = []
    if (root / "pyproject.toml").exists():
        commands.append(["python", "-m", "unittest", "discover", "-s", "tests"])
    package = root / "package.json"
    if package.exists():
        data = json.loads(package.read_text(encoding="utf-8"))
        for name in ("test", "lint", "typecheck"):
            if name in data.get("scripts", {}):
                commands.append(["npm", "run", name])
    return [validate_command(command) for command in commands]
