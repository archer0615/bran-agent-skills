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
    retry_base_seconds: float = 0.0
    retry_max_seconds: float = 30.0
    provider_endpoint: str = ""
    provider_model: str = ""
    provider_api_key_env: str = "OPENAI_API_KEY"

    @classmethod
    def from_environment(cls) -> "OrchestratorConfig":
        def integer(name: str, default: int) -> int:
            value = int(os.getenv(name, str(default)))
            if value < 0:
                raise ValueError(f"{name} must be non-negative")
            return value

        def non_negative_float(name: str, default: float) -> float:
            value = float(os.getenv(name, str(default)))
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
            retry_base_seconds=non_negative_float("BRAN_RETRY_BASE_SECONDS", 0.0),
            retry_max_seconds=non_negative_float("BRAN_RETRY_MAX_SECONDS", 30.0),
            provider_endpoint=os.getenv("BRAN_PROVIDER_ENDPOINT", ""),
            provider_model=os.getenv("BRAN_PROVIDER_MODEL", ""),
            provider_api_key_env=os.getenv("BRAN_PROVIDER_API_KEY_ENV", "OPENAI_API_KEY"),
        )
