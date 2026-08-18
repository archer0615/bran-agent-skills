# Scenario Test Cases

These cases complement the route-structure validator with concrete inputs, expected outputs, and failure conditions.

## Case 1: Prompt evaluation

- Input: A prompt that must answer in a fixed JSON shape, with missing fields and an instruction-injection example.
- Expected output: `prompt-evaluation` produces a test matrix, rubric, failure classification, and regression recommendation; `prompt-curator` is used only for supported revisions.
- Failure case: Treating one successful example as proof of robustness or following the injected lower-priority instruction.

## Case 2: Human review gate

- Input: An AI-generated financial recommendation that could trigger an external action.
- Expected output: `human-review-workflow` defines reviewer authority, evidence, approval threshold, rejection, escalation, audit, and rollback.
- Failure case: The action can execute without approval or rejection does not quarantine the action.

## Case 3: Unfamiliar repository

- Input: A repository with unknown startup commands and a requested login fix.
- Expected output: `existing-project-takeover` establishes a project map and baseline before implementation; `implementation-validator` reports targeted evidence.
- Failure case: Editing before inspecting instructions or reporting a pre-existing test failure as introduced.

## Case 4: Skill library maintenance

- Input: A library containing two Skills with overlapping triggers and different output owners.
- Expected output: `skill-curator` classifies duplicate versus specialization, recommends one canonical owner, and validates references.
- Failure case: Renaming or deleting a Skill without a compatibility or migration decision.

## Case 5: Context handoff

- Input: A long task interrupted after a failed validation attempt with uncommitted files.
- Expected output: `context-management` records verified, unverified, blocked, files, evidence, next action, and stopping condition.
- Failure case: Treating the checkpoint as proof of success or omitting the uncommitted-change boundary.
