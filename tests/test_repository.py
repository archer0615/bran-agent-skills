import tempfile
import unittest
from pathlib import Path

from orchestrator.repository import RepositoryAdapter


class RepositoryAdapterTests(unittest.TestCase):
    def test_reads_instructions_and_handles_non_git_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
            (root / "README.md").write_text("# Project\n", encoding="utf-8")

            snapshot = RepositoryAdapter(root).inspect()

            self.assertEqual(snapshot.path, str(root.resolve()))
            self.assertIsNone(snapshot.revision)
            self.assertEqual(snapshot.status, ())
            self.assertEqual(dict(snapshot.instructions)["AGENTS.md"], "# Rules\n")
            self.assertEqual(dict(snapshot.instructions)["README.md"], "# Project\n")

    def test_rejects_missing_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                RepositoryAdapter(Path(directory) / "missing")


if __name__ == "__main__":
    unittest.main()
