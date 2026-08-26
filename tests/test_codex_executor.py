import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from orchestrator.provider_adapters import CodexTaskExecutor


class CodexExecutorTests(unittest.TestCase):
    def test_task_executor_maps_cli_result_to_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            executor = CodexTaskExecutor(directory)
            with patch.object(executor.adapter, "execute", return_value={"status": "completed", "exit_code": 0, "stdout": "ok", "stderr": ""}):
                result = executor.execute({"task_id": "t1", "objective": "do work"})
            self.assertEqual(result["task_id"], "t1")
            self.assertEqual(result["status"], "completed")


if __name__ == "__main__":
    unittest.main()
