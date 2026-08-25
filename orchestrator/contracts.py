"""Validation for the Phase 02 machine-readable handoff contracts."""

from __future__ import annotations

from typing import Any, Mapping


class ContractValidationError(ValueError):
    """Raised when an artifact does not satisfy its contract."""


_SCHEMAS: dict[str, dict[str, Any]] = {
    "goal": {
        "required": {"schema_version", "goal_id", "objective", "repository", "constraints", "acceptance_criteria", "risk_level"},
        "allowed": {"schema_version", "goal_id", "objective", "repository", "constraints", "acceptance_criteria", "risk_level"},
        "enums": {"risk_level": {"low", "medium", "high", "critical"}},
    },
    "plan": {
        "required": {"schema_version", "plan_id", "goal_id", "tasks", "dependencies", "sequence", "risks", "human_gates"},
        "allowed": {"schema_version", "plan_id", "goal_id", "tasks", "dependencies", "sequence", "risks", "human_gates"},
    },
    "task": {
        "required": {"schema_version", "task_id", "plan_id", "objective", "scope", "allowed_changes", "forbidden_changes", "acceptance_criteria", "required_verification", "dependencies", "risk_level"},
        "allowed": {"schema_version", "task_id", "plan_id", "objective", "scope", "allowed_changes", "forbidden_changes", "acceptance_criteria", "required_verification", "dependencies", "risk_level"},
        "enums": {"risk_level": {"low", "medium", "high", "critical"}},
    },
    "execution_result": {
        "required": {"schema_version", "task_id", "status", "changed_files", "commands_run", "verification_results", "known_issues", "blocked_reason", "evidence"},
        "allowed": {"schema_version", "task_id", "status", "changed_files", "commands_run", "verification_results", "known_issues", "blocked_reason", "evidence"},
        "enums": {"status": {"completed", "blocked", "failed", "aborted"}},
    },
    "review_result": {
        "required": {"schema_version", "task_id", "decision", "acceptance_results", "issues", "required_corrections", "risk_findings", "next_action"},
        "allowed": {"schema_version", "task_id", "decision", "acceptance_results", "issues", "required_corrections", "risk_findings", "next_action"},
        "enums": {"decision": {"PASS", "REPLAN", "BLOCKED", "NEEDS_HUMAN"}},
    },
}


def validate_artifact(kind: str, artifact: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and return an ordinary dict suitable for persistence."""
    if kind not in _SCHEMAS:
        raise ContractValidationError(f"unknown artifact kind: {kind}")
    if not isinstance(artifact, Mapping):
        raise ContractValidationError("artifact must be an object")

    schema = _SCHEMAS[kind]
    actual = set(artifact)
    missing = schema["required"] - actual
    unknown = actual - schema["allowed"]
    if missing:
        raise ContractValidationError(f"missing required fields: {', '.join(sorted(missing))}")
    if unknown:
        raise ContractValidationError(f"unknown fields: {', '.join(sorted(unknown))}")
    if artifact["schema_version"] != "1.0":
        raise ContractValidationError("unsupported schema_version")

    for field, values in schema.get("enums", {}).items():
        if artifact[field] not in values:
            raise ContractValidationError(f"invalid {field}: {artifact[field]!r}")

    for field in ("goal_id", "plan_id", "task_id", "objective"):
        if field in artifact and (not isinstance(artifact[field], str) or not artifact[field]):
            raise ContractValidationError(f"{field} must be a non-empty string")
    return dict(artifact)
