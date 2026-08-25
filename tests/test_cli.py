import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.cli import main


class CliTests(unittest.TestCase):
    def test_cli_runs_fake_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main([directory, "demo goal"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue())["state"], "COMPLETED")
            self.assertTrue((Path(directory) / ".orchestrator" / "state.json").exists())
