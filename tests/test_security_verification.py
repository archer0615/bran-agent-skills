import tempfile
import unittest
from pathlib import Path

from orchestrator.security import SecurityPolicyError, confined_path, redact, validate_command
from orchestrator.verification import discover_commands


class SecurityVerificationTests(unittest.TestCase):
    def test_redacts_secrets_and_blocks_mutation(self):
        self.assertNotIn("secret-value", redact("API_KEY=secret-value"))
        with self.assertRaises(SecurityPolicyError):
            validate_command(["git", "push"])

    def test_confined_path_and_verification_discovery(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
            self.assertEqual(discover_commands(root)[0][:3], ["python", "-m", "unittest"])
            self.assertEqual(confined_path(root, "tests"), root / "tests")
            with self.assertRaises(SecurityPolicyError):
                confined_path(root, "../outside")


if __name__ == "__main__":
    unittest.main()
