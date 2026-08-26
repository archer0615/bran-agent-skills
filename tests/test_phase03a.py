import json
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from orchestrator.events import TransitionLog
from orchestrator.artifacts import ArtifactStore, ArtifactValidationError
from orchestrator.gates import GateStore, GateValidationError
from orchestrator.retry import action_for, backoff_seconds, classify, wait_before_retry
from orchestrator.state_machine import InvalidTransitionError, StateMachine
from orchestrator.state_store import StateConflictError, StateCorruptionError, StateStore


class Phase03ATests(unittest.TestCase):
    def test_artifacts_are_atomic_confined_and_redacted(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ArtifactStore(Path(directory))
            saved = store.write({"schema_version": "1.0", "run_id": "r1", "environment": {"TOKEN": "secret"}}, artifact_id="r1", kind="run")
            self.assertNotIn("environment", saved)
            self.assertEqual(store.read(artifact_id="r1", kind="run")["run_id"], "r1")
            with self.assertRaises(ArtifactValidationError):
                store.write({"schema_version": "1.0"}, artifact_id="../escape", kind="run")

    def test_artifacts_are_contract_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ArtifactStore(Path(directory))
            with self.assertRaises(ArtifactValidationError):
                store.write({"schema_version": "1.0", "goal_id": "g"}, artifact_id="g", kind="goal")
            with self.assertRaises(ArtifactValidationError):
                store.write({"schema_version": "1.0", "run_id": "r", "task_id": "t", "kind": "execution", "execution": {"schema_version": "1.0"}, "repository_revision": "r"}, artifact_id="r", kind="run")

    def test_transition_validation_and_terminal_fail_closed(self):
        machine = StateMachine()
        machine.transition("NEW", "PLANNING", "Controller", {"goal_id": "g"})
        with self.assertRaises(InvalidTransitionError):
            machine.transition("NEW", "COMPLETED", "Controller", {"goal_id": "g"})
        with self.assertRaises(InvalidTransitionError):
            machine.transition("COMPLETED", "PLANNING", "Controller", {"goal_id": "g"})

    def test_gate_is_bound_and_single_use(self):
        with tempfile.TemporaryDirectory() as directory:
            gates = GateStore(Path(directory))
            gate = gates.create(goal_id="g", plan_id="p", task_id="t", repository_revision="r1", scope=["a.py"], reason="review")
            gates.decide(gate["gate_id"], "APPROVED", actor="human")
            approved = gates.validate_approval(gate["gate_id"], task_id="t", repository_revision="r1", scope=["a.py"])
            self.assertEqual(approved["status"], "CANCELLED")
            with self.assertRaises(GateValidationError):
                gates.validate_approval(gate["gate_id"], task_id="t", repository_revision="r1", scope=["a.py"])

    def test_backup_recovery_and_corrupt_primary(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / "state.json")
            store.save({"state": "NEW"}, repository_revision="r1")
            store.save({"state": "PLANNING"}, repository_revision="r1")
            store.path.write_text("{broken", encoding="utf-8")
            with self.assertRaises(StateCorruptionError):
                store.load()
            restored = store.recover_from_backup(repository_revision="r1")
            self.assertEqual(restored["state"], "NEW")
            self.assertTrue((Path(directory) / "events.jsonl").exists())

    def test_lock_unknown_is_not_deleted_and_event_log_is_redacted(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / "state.json")
            store.lock_path.write_text(json.dumps({"pid": 1}), encoding="utf-8")
            self.assertEqual(store.lock_status(), "unknown")
            with self.assertRaises(StateConflictError):
                store.recover_lock(explicit=True)
            log = TransitionLog(Path(directory) / "events.jsonl")
            log.append(from_state="NEW", to_state="PLANNING", actor="Controller", reason="api_key=secret", context={"environment": {"TOKEN": "secret"}})
            event = log.list()[0]
            self.assertNotIn("secret", json.dumps(event))

    def test_retry_classification_has_bounded_default_actions(self):
        self.assertEqual(classify("environment"), "ENVIRONMENT")
        self.assertEqual(action_for("security"), "human_gate")
        self.assertEqual(action_for("not-known"), "failed")

    def test_retry_backoff_is_bounded_and_injectable(self):
        self.assertEqual(backoff_seconds(0, base_seconds=1, max_seconds=5), 1)
        self.assertEqual(backoff_seconds(4, base_seconds=1, max_seconds=5), 5)
        delays = []
        self.assertEqual(wait_before_retry(2, sleeper=delays.append, base_seconds=1, max_seconds=5), 4)
        self.assertEqual(delays, [4])


if __name__ == "__main__":
    unittest.main()
