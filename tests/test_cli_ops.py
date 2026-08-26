import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.cli import main
from orchestrator.evidence import run_verification


class CliOpsTests(unittest.TestCase):
    def test_status_and_validation_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main(["status", directory]), 0)
            self.assertEqual(json.loads(output.getvalue())["state"], "NEW")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["validate", directory]), 0)

    def test_verification_timeout_is_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = run_verification(directory, ["cmd", "/c", "ping", "-n", "3", "127.0.0.1"], timeout_seconds=0.001)
            self.assertEqual(evidence.exit_code, 124)
            self.assertIn("timed out", evidence.summary)


if __name__ == "__main__":
    unittest.main()
