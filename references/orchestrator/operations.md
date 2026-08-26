# Orchestrator operations guide

## Local start

```powershell
python -m orchestrator.cli doctor .
python -m orchestrator.cli plan . "<goal>"
python -m orchestrator.cli run . "<goal>"
python -m orchestrator.cli status .
python -m orchestrator.cli artifacts .
```

The default providers are deterministic fakes. Provider selection is explicit through `BRAN_PLANNER_PROVIDER`, `BRAN_EXECUTOR_PROVIDER`, and `BRAN_REVIEWER_PROVIDER`; credentials are read from the environment and never persisted in artifacts.

## Human gates

Request a gate with `request-gate`, inspect it with `gates`, then use `approve` or `reject`. A gate is bound to task, repository revision and scope, expires, and becomes single-use after validation. Approval never authorizes a different task or revision.

## Recovery

Use `status` to inspect the checkpoint and `resume` to continue a non-terminal run. If a lock is known to be stale, inspect it first and use `recover-lock`; unknown live locks are not removed automatically. A corrupted state must be recovered from its verified backup before continuing.

## Safety

Verification commands are allowlisted against mutating Git and deployment verbs. Output is bounded and redacted. The controller must stop for destructive operations, secrets, production data, protected branches, public API breaks, major upgrades or architecture changes outside task scope.

## Persistence policy

`.orchestrator/` is local runtime state and ignored by Git. Do not commit secrets, raw prompts, environment dumps or unredacted logs. Commit only source, schemas, tests and documentation.
