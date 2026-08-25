"""Small deterministic failure classification and bounded actions."""

from __future__ import annotations

from enum import Enum


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
