import tempfile
import unittest
from pathlib import Path

from orchestrator.evidence import run_verification
from orchestrator.repository import RepositoryAdapter
from orchestrator.security import SecurityPolicyError


class BaselineDiffTests(unittest.TestCase):
    def test_non_git_baseline_compare_and_patch(self):
        with tempfile.TemporaryDirectory() as directory:
            adapter = RepositoryAdapter(Path(directory))
            baseline = adapter.baseline()
            comparison = adapter.compare(baseline)
            self.assertFalse(comparison["revision_changed"])
            self.assertEqual(adapter.diff_patch(), "")

    def test_verification_rejects_mutating_command(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(SecurityPolicyError):
                run_verification(directory, ["git", "push"])


if __name__ == "__main__":
    unittest.main()
