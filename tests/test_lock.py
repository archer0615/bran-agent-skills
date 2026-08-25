import tempfile
import unittest
from pathlib import Path

from orchestrator.state_store import StateConflictError, StateStore


class LockTests(unittest.TestCase):
    def test_second_lock_is_rejected_and_lock_is_released(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / "state.json")
            with store.lock():
                with self.assertRaises(StateConflictError):
                    with store.lock():
                        pass
            with store.lock():
                pass
