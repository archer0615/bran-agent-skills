---
name: prompt-evaluation
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when testing whether a prompt is clear, robust, consistent, and fit for repeated use.
---

# Prompt Evaluation

## Use when

Use this skill when testing whether a prompt is clear, robust, consistent, safe, and fit for repeated use across representative inputs.

## Inputs

- Required: Prompt under test, intended behavior, output contract, and representative inputs.
- Optional: Existing examples, rubric, known failures, language requirements, safety constraints, and baseline version.
- Preconditions: Expected behavior can be observed or the test is explicitly exploratory.
- Missing information: Record unknown criteria and avoid declaring stability until the contract is testable.
- Output artifact: Test matrix, rubric, results, failure classification, regression status, and revision recommendation.

## Procedure

1. Define the prompt’s purpose, target model or workflow, audience, constraints, expected output, and success criteria.
2. Build a representative test set covering normal, boundary, missing-data, ambiguous, adversarial, multilingual, and regression cases.
3. Define an evaluation rubric for correctness, completeness, instruction following, consistency, safety, tone, and format.
4. Run the prompt against the test set and record input, output, rubric result, failure mode, and reproducibility.
5. Identify instruction conflicts, hidden assumptions, leakage risks, overfitting, and unsupported claims.
6. Revise minimally, preserve intended behavior, and re-run the full regression set. Compare against the prior version.

## Decision rules

- Every test case needs expected behavior and an observable criterion; otherwise classify it as exploratory.
- Missing-data, ambiguity, safety, privacy, instruction hierarchy, and format behavior are part of correctness.
- Classify failures as prompt, model, tool, data, or environment related before revising.
- Preserve the output contract and do not overfit to the test set or hide regressions.
- Own test design and regression evidence; hand off a failing or improvable Prompt with test results to `prompt-curator`, then re-run this Skill after changes.
- Do not use this Skill for simple wording cleanup when no behavioral test is required.

## Verification

- Test cases cover representative success and failure conditions.
- Criteria are observable and applied consistently.
- Safety, privacy, instruction hierarchy, and adversarial behavior are reviewed.
- Changes improve or preserve required behavior without hiding regressions.

## Output

Return the evaluation plan, test cases, rubric, results, failure modes, revision diff or recommendation, regression status, assumptions, and unresolved questions. Communicate with the user in Traditional Chinese unless another language is requested.

## Example

For a JSON-output prompt, test a normal request, missing fields, conflicting instructions, injection wording, multilingual input, and a prior regression. Score format compliance and safe handling separately from fluency.

