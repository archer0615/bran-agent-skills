"""Provider-neutral configuration with safe defaults and no secret persistence."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class OrchestratorConfig:
    planner_provider: str = "fake"
    executor_provider: str = "fake"
    reviewer_provider: str = "fake"
    command_timeout_seconds: int = 300
    max_execution_retries: int = 2
    max_plan_revisions: int = 3

    @classmethod
    def from_environment(cls) -> "OrchestratorConfig":
        def integer(name: str, default: int) -> int:
            value = int(os.getenv(name, str(default)))
            if value < 0:
                raise ValueError(f"{name} must be non-negative")
            return value

        return cls(
            planner_provider=os.getenv("BRAN_PLANNER_PROVIDER", "fake"),
            executor_provider=os.getenv("BRAN_EXECUTOR_PROVIDER", "fake"),
            reviewer_provider=os.getenv("BRAN_REVIEWER_PROVIDER", "fake"),
            command_timeout_seconds=integer("BRAN_COMMAND_TIMEOUT_SECONDS", 300),
            max_execution_retries=integer("BRAN_MAX_EXECUTION_RETRIES", 2),
            max_plan_revisions=integer("BRAN_MAX_PLAN_REVISIONS", 3),
        )
