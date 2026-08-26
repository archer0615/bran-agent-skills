import tempfile
import unittest
from datetime import datetime, timedelta, timezone
import json
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

    def test_heartbeat_refreshes_owned_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / "state.json")
            with store.lock(expires_in_seconds=1) as metadata:
                before = datetime.fromisoformat(metadata["expires_at"])
                refreshed = store.heartbeat(metadata["lock_id"], expires_in_seconds=60)
                self.assertGreater(datetime.fromisoformat(refreshed["expires_at"]), before)
                self.assertEqual(store.lock_status(), "active")

    def test_expired_lock_requires_explicit_recovery(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / "state.json")
            store.lock_path.parent.mkdir(parents=True, exist_ok=True)
            old = (datetime.now(timezone.utc) - timedelta(seconds=10)).isoformat()
            store.lock_path.write_text(json.dumps({"lock_id":"old","pid":999999,"hostname":"localhost","created_at":old,"heartbeat_at":old,"expires_at":old,"repository":"x","run_id":"r"}), encoding="utf-8")
            self.assertEqual(store.lock_status(), "stale")
            self.assertEqual(store.recover_lock(explicit=True)["action"], "recovered")
