import tempfile
import unittest
from pathlib import Path

from orchestrator.controller import LoopController
from orchestrator.providers import FakeExecutor, FakePlanner, FakeReviewer
from orchestrator.repository import RepositoryAdapter
from orchestrator.state_store import StateStore


def goal():
    return {"schema_version": "1.0", "goal_id": "g1", "objective": "demo", "repository": {}, "constraints": [], "acceptance_criteria": [], "risk_level": "low"}


class ControllerTests(unittest.TestCase):
    def run_controller(self, reviewer="PASS", executor="completed"):
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        controller = LoopController(RepositoryAdapter(root), StateStore(root / ".orchestrator" / "state.json"), FakePlanner(), FakeExecutor(executor), FakeReviewer(reviewer))
        return directory, controller

    def test_pass_completes(self):
        directory, controller = self.run_controller()
        self.assertEqual(controller.run(goal()).state, "COMPLETED")
        directory.cleanup()

    def test_replan_and_blocked_paths(self):
        directory, controller = self.run_controller("REPLAN")
        controller.max_replans = 0
        self.assertEqual(controller.run(goal()).state, "FAILED")
        directory.cleanup()

    def test_retry_backoff_is_applied_between_attempts(self):
        delays = []
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        controller = LoopController(RepositoryAdapter(root), StateStore(root / ".orchestrator" / "state.json"), FakePlanner(), FakeExecutor("failed"), FakeReviewer(), max_execution_retries=2, retry_base_seconds=1, retry_max_seconds=3, sleeper=delays.append)
        self.assertEqual(controller.run(goal()).state, "FAILED")
        self.assertEqual(delays, [1, 2])
        directory.cleanup()
        directory, controller = self.run_controller(executor="blocked")
        self.assertEqual(controller.run(goal()).state, "BLOCKED")
        directory.cleanup()
