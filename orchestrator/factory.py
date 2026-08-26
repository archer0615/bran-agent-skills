"""Explicit provider factory with safe offline defaults."""

from __future__ import annotations

from .config import OrchestratorConfig
from .provider_adapters import CodexCliExecutor, CodexTaskExecutor, JsonHttpProvider, JsonPlanner, JsonReviewer, ProviderError
from .providers import Executor, FakeExecutor, FakePlanner, FakeReviewer, Planner, Reviewer


def build_providers(config: OrchestratorConfig) -> tuple[Planner, Executor, Reviewer]:
    names = (config.planner_provider, config.executor_provider, config.reviewer_provider)
    if all(name == "fake" for name in names):
        return FakePlanner(), FakeExecutor(), FakeReviewer()
    if config.planner_provider not in {"fake", "openai"} or config.reviewer_provider not in {"fake", "openai"} or config.executor_provider not in {"fake", "codex"}:
        raise ProviderError("unknown provider; supported: fake, openai, codex")
    if not config.provider_endpoint or not config.provider_model:
        raise ProviderError("real provider requires BRAN_PROVIDER_ENDPOINT and BRAN_PROVIDER_MODEL")
    provider = JsonHttpProvider(config.provider_endpoint, config.provider_model, config.provider_api_key_env)
    planner = JsonPlanner(provider) if config.planner_provider == "openai" else FakePlanner()
    reviewer = JsonReviewer(provider) if config.reviewer_provider == "openai" else FakeReviewer()
    executor = CodexTaskExecutor(".") if config.executor_provider == "codex" else FakeExecutor()
    return planner, executor, reviewer
