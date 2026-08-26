"""Explicit provider factory with safe offline defaults."""

from __future__ import annotations

from .config import OrchestratorConfig
from .provider_adapters import CodexCliExecutor, JsonHttpProvider, JsonPlanner, JsonReviewer, ProviderError
from .providers import Executor, FakeExecutor, FakePlanner, FakeReviewer, Planner, Reviewer


def build_providers(config: OrchestratorConfig) -> tuple[Planner, Executor, Reviewer]:
    names = (config.planner_provider, config.executor_provider, config.reviewer_provider)
    if all(name == "fake" for name in names):
        return FakePlanner(), FakeExecutor(), FakeReviewer()
    if config.planner_provider not in {"fake", "openai"} or config.reviewer_provider not in {"fake", "openai"} or config.executor_provider not in {"fake", "codex"}:
        raise ProviderError("unknown provider; supported: fake, openai, codex")
    raise ProviderError("real provider wiring requires explicit role adapter configuration")
