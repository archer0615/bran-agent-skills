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

## Case 6: Direct answer

- Input: A stable, low-risk factual question such as the capital of Japan.
- Expected output: Answer directly without routing to a project workflow or inventing a multi-step Skill sequence.
- Failure case: Invoking research or implementation Skills unnecessarily.

## Case 7: Missing material requirement

- Input: A request to add an export feature without format, scope, permissions, or acceptance criteria.
- Expected output: `requirement-refinement` asks only material questions and returns a clarified requirement.
- Failure case: Silently choosing product behavior or asking irrelevant preference questions.

## Case 8: Research to decision

- Input: A request to compare current database vendors by cost, performance, operations, and exitability.
- Expected output: Current evidence is gathered, options are compared consistently, and `decision-researcher` states conditional recommendation and decision-changing evidence.
- Failure case: Using stale facts, mixing criteria, or presenting preference as fact.

## Case 9: Governed automation

- Input: A request to design AI automation that approves sensitive financial records.
- Expected output: `ai-governance` classifies risk, `human-review-workflow` defines authority and controls, and `quality-gate` blocks unready delivery.
- Failure case: Automation proceeds without oversight, audit, rejection, or rollback.

## Case 10: Failed correction loop

- Input: A code change passes lint but fails an acceptance test and must be corrected before delivery.
- Expected output: Route, inspect, correct, rerun validation, and make a final ready/not-ready decision.
- Failure case: Declaring success from lint alone or skipping revalidation after correction.
