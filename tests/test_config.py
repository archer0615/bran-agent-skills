import os
import unittest

from orchestrator.config import OrchestratorConfig
from orchestrator.factory import build_providers
from orchestrator.provider_adapters import ProviderError


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

    def test_factory_defaults_to_fake_and_rejects_unwired_real_provider(self):
        self.assertEqual(len(build_providers(OrchestratorConfig())), 3)
        with self.assertRaises(ProviderError):
            build_providers(OrchestratorConfig(planner_provider="openai"))

    def test_negative_budget_is_rejected(self):
        old = os.environ.get("BRAN_MAX_PLAN_REVISIONS")
        try:
            os.environ["BRAN_MAX_PLAN_REVISIONS"] = "-1"
            with self.assertRaises(ValueError):
                OrchestratorConfig.from_environment()
        finally:
            if old is None:
                os.environ.pop("BRAN_MAX_PLAN_REVISIONS", None)
            else:
                os.environ["BRAN_MAX_PLAN_REVISIONS"] = old

    def test_retry_backoff_settings_are_loaded(self):
        old_base = os.environ.get("BRAN_RETRY_BASE_SECONDS")
        old_max = os.environ.get("BRAN_RETRY_MAX_SECONDS")
        try:
            os.environ["BRAN_RETRY_BASE_SECONDS"] = "1.5"
            os.environ["BRAN_RETRY_MAX_SECONDS"] = "7"
            config = OrchestratorConfig.from_environment()
            self.assertEqual(config.retry_base_seconds, 1.5)
            self.assertEqual(config.retry_max_seconds, 7.0)
        finally:
            for name, old in (("BRAN_RETRY_BASE_SECONDS", old_base), ("BRAN_RETRY_MAX_SECONDS", old_max)):
                if old is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = old


if __name__ == "__main__":
    unittest.main()
