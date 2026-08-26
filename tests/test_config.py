import os
import unittest

from orchestrator.config import OrchestratorConfig


class ConfigTests(unittest.TestCase):
    def test_defaults_are_offline_and_bounded(self):
        config = OrchestratorConfig.from_environment()
        self.assertEqual(config.planner_provider, "fake")
        self.assertEqual(config.max_plan_revisions, 3)

    def test_environment_overrides_non_secret_settings(self):
        old = os.environ.get("BRAN_MAX_EXECUTION_RETRIES")
        try:
            os.environ["BRAN_MAX_EXECUTION_RETRIES"] = "4"
            self.assertEqual(OrchestratorConfig.from_environment().max_execution_retries, 4)
        finally:
            if old is None:
                os.environ.pop("BRAN_MAX_EXECUTION_RETRIES", None)
            else:
                os.environ["BRAN_MAX_EXECUTION_RETRIES"] = old


if __name__ == "__main__":
    unittest.main()
