"""Read-only inspection of a target repository."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepositorySnapshot:
    path: str
    revision: str | None
    status: tuple[str, ...]
    diff_stat: str
    instructions: tuple[tuple[str, str], ...]


class RepositoryAdapter:
    """Collect repository context without changing the working tree."""

    instruction_names = ("AGENTS.md", "README.md")

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        if not self.root.is_dir():
            raise ValueError(f"repository path is not a directory: {self.root}")

    def inspect(self) -> RepositorySnapshot:
        revision = self._git_output("rev-parse", "HEAD") or None
        status_output = self._git_output("status", "--short")
        diff_stat = self._git_output("diff", "--stat") or ""
        instructions = tuple(
            (name, (self.root / name).read_text(encoding="utf-8"))
            for name in self.instruction_names
            if (self.root / name).is_file()
        )
        return RepositorySnapshot(
            path=str(self.root),
            revision=revision,
            status=tuple(line for line in status_output.splitlines() if line),
            diff_stat=diff_stat,
            instructions=instructions,
        )

    def diff_patch(self) -> str:
        """Return the current unstaged patch; empty when Git is unavailable."""
        return self._git_output("diff", "--no-ext-diff", "--binary")

    def baseline(self) -> RepositorySnapshot:
        """Capture a named pre-execution snapshot for later comparison."""
        return self.inspect()

    def compare(self, baseline: RepositorySnapshot) -> dict[str, object]:
        current = self.inspect()
        return {
            "revision_changed": baseline.revision != current.revision,
            "status_changed": baseline.status != current.status,
            "diff_stat": current.diff_stat,
            "changed_files": [line[3:] for line in current.status if len(line) > 3],
        }

    def _git_output(self, *arguments: str) -> str:
        try:
            result = subprocess.run(
                ["git", *arguments],
                cwd=self.root,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        except OSError:
            return ""
        if result.returncode != 0:
            return ""
        return result.stdout.strip()
