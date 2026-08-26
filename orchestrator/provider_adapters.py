"""Optional provider adapters. They are explicit and never selected by default."""

from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from .security import redact, validate_command
from .contracts import validate_artifact


class ProviderError(RuntimeError):
    pass


@dataclass
class JsonHttpProvider:
    endpoint: str
    model: str
    api_key_env: str = "OPENAI_API_KEY"
    timeout_seconds: int = 120

    def request(self, payload: dict) -> dict:
        token = os.getenv(self.api_key_env)
        if not token:
            raise ProviderError(f"missing provider credential: {self.api_key_env}")
        body = json.dumps({"model": self.model, **payload}).encode("utf-8")
        request = urllib.request.Request(self.endpoint, data=body, method="POST", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise ProviderError(redact(str(exc))) from exc


@dataclass
class CodexCliExecutor:
    command: tuple[str, ...] = ("codex",)
    timeout_seconds: int = 900

    def execute(self, root: str | Path, prompt: str) -> dict:
        command = validate_command([*self.command, prompt])
        try:
            result = subprocess.run(command, cwd=Path(root), capture_output=True, text=True, timeout=self.timeout_seconds, check=False)
        except subprocess.TimeoutExpired as exc:
            raise ProviderError("executor timed out") from exc
        return {"status": "completed" if result.returncode == 0 else "failed", "exit_code": result.returncode, "stdout": redact(result.stdout)[-4000:], "stderr": redact(result.stderr)[-4000:]}


@dataclass
class CodexTaskExecutor:
    """Executor-protocol wrapper around the CLI adapter."""
    root: str | Path
    adapter: CodexCliExecutor = field(default_factory=CodexCliExecutor)

    def execute(self, task: dict) -> dict:
        result = self.adapter.execute(self.root, task["objective"])
        return {"schema_version": "1.0", "task_id": task["task_id"], "status": result["status"], "changed_files": [], "commands_run": [{"command": " ".join(self.adapter.command), "exit_code": result["exit_code"], "summary": result["stderr"] or result["stdout"]}], "verification_results": [], "known_issues": [], "blocked_reason": None if result["status"] == "completed" else "Codex CLI failed", "evidence": [{"kind": "executor", "ref": "codex-cli"}]}


@dataclass
class JsonPlanner:
    provider: JsonHttpProvider

    def create_plan(self, goal: dict) -> dict:
        response = self.provider.request({"input": {"role": "planner", "goal": goal}})
        plan = response.get("plan", response)
        return validate_artifact("plan", plan)


@dataclass
class JsonReviewer:
    provider: JsonHttpProvider

    def review(self, task: dict, execution: dict) -> dict:
        response = self.provider.request({"input": {"role": "reviewer", "task": task, "execution": execution}})
        review = response.get("review", response)
        return validate_artifact("review_result", review)
