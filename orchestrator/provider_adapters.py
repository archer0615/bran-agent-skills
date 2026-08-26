"""Optional provider adapters. They are explicit and never selected by default."""

from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .security import redact, validate_command


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
