import tempfile
import unittest

from orchestrator.evidence import run_verification


class EvidenceTests(unittest.TestCase):
    def test_captures_exit_code_and_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            evidence = run_verification(directory, ["cmd", "/c", "echo", "verified"])
            self.assertEqual(evidence.exit_code, 0)
            self.assertIn("verified", evidence.summary)
