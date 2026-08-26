import os
import tempfile
import unittest
from pathlib import Path

from orchestrator.provider_adapters import CodexCliExecutor, JsonHttpProvider, ProviderError
from orchestrator.schema_validation import SchemaError, validate_schema_file


class AdapterSchemaTests(unittest.TestCase):
    def test_provider_requires_explicit_credential(self):
        with tempfile.TemporaryDirectory():
            os.environ.pop("TEST_PROVIDER_KEY", None)
            with self.assertRaises(ProviderError):
                JsonHttpProvider("https://example.invalid", "model", "TEST_PROVIDER_KEY").request({})

    def test_cli_executor_blocks_mutating_git_command(self):
        executor = CodexCliExecutor(command=("git", "push"))
        with self.assertRaises(Exception):
            executor.execute(Path.cwd(), "x")

    def test_nested_schema_validation(self):
        schema = Path(__file__).parents[1] / "orchestrator" / "schemas" / "approval.schema.json"
        valid = {"schema_version":"1.0","gate_id":"g","goal_id":"g","plan_id":None,"task_id":"t","repository_revision":"r","status":"PENDING","actor":"system","reason":"x","created_at":"now","decided_at":None,"expires_at":"later","scope":[]}
        validate_schema_file(valid, schema)
        valid["unexpected"] = True
        with self.assertRaises(SchemaError):
            validate_schema_file(valid, schema)


if __name__ == "__main__":
    unittest.main()
