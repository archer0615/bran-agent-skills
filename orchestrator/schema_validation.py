"""Dependency-free schema loading and structural validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SchemaError(ValueError):
    pass


def validate_document(document: Any, schema: dict[str, Any], path: str = "$") -> None:
    expected = schema.get("type")
    if expected == "object":
        if not isinstance(document, dict):
            raise SchemaError(f"{path} must be an object")
        required = set(schema.get("required", []))
        missing = required - set(document)
        if missing:
            raise SchemaError(f"{path} missing: {', '.join(sorted(missing))}")
        if schema.get("additionalProperties") is False:
            unknown = set(document) - set(schema.get("properties", {}))
            if unknown:
                raise SchemaError(f"{path} unknown: {', '.join(sorted(unknown))}")
        for key, child in schema.get("properties", {}).items():
            if key in document:
                validate_document(document[key], child, f"{path}.{key}")
    elif expected == "array":
        if not isinstance(document, list):
            raise SchemaError(f"{path} must be an array")
        for index, value in enumerate(document):
            validate_document(value, schema.get("items", {}), f"{path}[{index}]")
    elif expected == "string" and not isinstance(document, str):
        raise SchemaError(f"{path} must be a string")
    elif expected == "boolean" and not isinstance(document, bool):
        raise SchemaError(f"{path} must be a boolean")
    if "const" in schema and document != schema["const"]:
        raise SchemaError(f"{path} must equal {schema['const']!r}")
    if "enum" in schema and document not in schema["enum"]:
        raise SchemaError(f"{path} has invalid value")


def validate_schema_file(document: Any, schema_path: str | Path) -> None:
    validate_document(document, json.loads(Path(schema_path).read_text(encoding="utf-8")))
