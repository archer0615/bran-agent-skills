import tempfile
import unittest
from pathlib import Path

from orchestrator.state_store import StateConflictError, StateStore, StateValidationError


class StateStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / ".orchestrator" / "state.json"
        self.store = StateStore(self.path)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def test_save_and_load_round_trip(self) -> None:
        saved = self.store.save({"state": "NEW", "goal_id": "goal-1"}, repository_revision="abc")

        self.assertEqual(saved["schema_version"], "1.0")
        self.assertEqual(self.store.load(), saved)
        self.assertTrue(self.path.exists())

    def test_stale_writer_is_rejected(self) -> None:
        self.store.save({"state": "NEW"}, repository_revision="abc")
        self.store.save(
            {"state": "PLANNING"},
            repository_revision="def",
            expected_repository_revision="abc",
        )

        with self.assertRaises(StateConflictError):
            self.store.save(
                {"state": "READY"},
                repository_revision="ghi",
                expected_repository_revision="abc",
            )

        self.assertEqual(self.store.load()["repository_revision"], "def")

    def test_invalid_state_is_rejected(self) -> None:
        with self.assertRaises(StateValidationError):
            self.store.save({"state": "NEW"}, repository_revision="")


if __name__ == "__main__":
    unittest.main()
