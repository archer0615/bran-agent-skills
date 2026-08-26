"""Small deterministic failure classification and bounded actions."""

from __future__ import annotations

from enum import Enum
from typing import Callable


class FailureClass(str, Enum):
    IMPLEMENTATION = "IMPLEMENTATION"
    VERIFICATION = "VERIFICATION"
    ENVIRONMENT = "ENVIRONMENT"
    REQUIREMENT = "REQUIREMENT"
    ARCHITECTURE = "ARCHITECTURE"
    SECURITY = "SECURITY"
    DEPENDENCY = "DEPENDENCY"
    UNKNOWN = "UNKNOWN"


DEFAULT_ACTION = {FailureClass.IMPLEMENTATION: "retry", FailureClass.VERIFICATION: "retry", FailureClass.ENVIRONMENT: "blocked", FailureClass.REQUIREMENT: "replan", FailureClass.ARCHITECTURE: "human_gate", FailureClass.SECURITY: "human_gate", FailureClass.DEPENDENCY: "blocked", FailureClass.UNKNOWN: "failed"}


def classify(value: str | None) -> FailureClass:
    try:
        return FailureClass(str(value).upper())
    except ValueError:
        return FailureClass.UNKNOWN


def action_for(value: str | None) -> str:
    return DEFAULT_ACTION[classify(value)]


def backoff_seconds(attempt: int, *, base_seconds: float = 0.0, max_seconds: float = 30.0) -> float:
    """Return bounded exponential backoff for a retry attempt.

    The default is zero so local runs stay deterministic; callers can inject a
    sleeper and a positive base when an external provider needs throttling.
    """
    if attempt < 0:
        raise ValueError("attempt must be non-negative")
    if base_seconds < 0 or max_seconds < 0:
        raise ValueError("backoff limits must be non-negative")
    return min(max_seconds, base_seconds * (2 ** attempt))


def wait_before_retry(attempt: int, *, sleeper: Callable[[float], None], base_seconds: float = 0.0, max_seconds: float = 30.0) -> float:
    delay = backoff_seconds(attempt, base_seconds=base_seconds, max_seconds=max_seconds)
    sleeper(delay)
    return delay
