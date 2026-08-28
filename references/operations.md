# Operations quick reference

The local orchestrator is intentionally offline and provider-neutral by default. Real Planner, Executor, and Reviewer integrations must be explicitly configured and remain behind their interfaces.

```powershell
python -m orchestrator.cli doctor .
python -m orchestrator.cli plan . "<goal>"
python -m orchestrator.cli run . "<goal>"
python -m orchestrator.cli status .
python -m orchestrator.cli artifacts .
```

For a production provider integration, define timeout, retry, error mapping, secret redaction, token/cost accounting, and an offline fallback before enabling it. Never enable automatic commit, push, merge, deploy, or production-data mutation as a provider default.
