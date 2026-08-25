# Artifact contracts

All artifacts are UTF-8 JSON with `schema_version`, stable ids, ISO-8601 timestamps where applicable, and `additionalProperties: false` in the production schema. JSON is the interchange format; Markdown views may be generated for human review. Contracts are model/provider agnostic and versioned additively.

## Goal

```json
{"schema_version":"1.0","goal_id":"goal-...","objective":"...","repository":{"path":"...","revision":"..."},"constraints":[],"acceptance_criteria":[{"id":"AC-1","text":"...","required":true}],"risk_level":"low|medium|high|critical"}
```

## Plan

```json
{"schema_version":"1.0","plan_id":"plan-...","goal_id":"goal-...","tasks":[{"task_id":"task-...","objective":"...","dependencies":[]}],"sequence":["task-..."],"risks":[],"human_gates":[]}
```

## Task

```json
{"schema_version":"1.0","task_id":"task-...","plan_id":"plan-...","objective":"...","scope":[],"allowed_changes":[],"forbidden_changes":[],"acceptance_criteria":[],"required_verification":[],"dependencies":[],"risk_level":"low|medium|high|critical"}
```

## Execution Result

```json
{"schema_version":"1.0","task_id":"task-...","status":"completed|blocked|failed|aborted","changed_files":[],"commands_run":[{"command":"...","exit_code":0,"summary":"..."}],"verification_results":[],"known_issues":[],"blocked_reason":null,"evidence":[{"kind":"diff|test|build|lint|manual","ref":"..."}]}
```

## Review Result

```json
{"schema_version":"1.0","task_id":"task-...","decision":"PASS|REPLAN|BLOCKED|NEEDS_HUMAN","acceptance_results":[{"criterion_id":"AC-1","result":"pass|fail|unverified","evidence_refs":[]}],"issues":[],"required_corrections":[],"risk_findings":[],"next_action":"finish|replan|block|human"}
```

The Reviewer must reject missing required fields, unverifiable claims, scope violations, and criteria marked `unverified` when required. `evidence.ref` points to a persisted run artifact or exact command record; secrets and credentials are never stored.
