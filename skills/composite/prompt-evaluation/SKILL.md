---
name: prompt-evaluation
description: Use when testing whether a prompt is clear, robust, consistent, and fit for repeated use.
---

# Prompt Evaluation

## Use when

Use this skill when testing whether a prompt is clear, robust, consistent, safe, and fit for repeated use across representative inputs.

## Procedure

1. Define the prompt’s purpose, target model or workflow, audience, constraints, expected output, and success criteria.
2. Build a representative test set covering normal, boundary, missing-data, ambiguous, adversarial, multilingual, and regression cases.
3. Define an evaluation rubric for correctness, completeness, instruction following, consistency, safety, tone, and format.
4. Run the prompt against the test set and record input, output, rubric result, failure mode, and reproducibility.
5. Identify instruction conflicts, hidden assumptions, leakage risks, overfitting, and unsupported claims.
6. Revise minimally, preserve intended behavior, and re-run the full regression set. Compare against the prior version.

## Verification

- Test cases cover representative success and failure conditions.
- Criteria are observable and applied consistently.
- Safety, privacy, instruction hierarchy, and adversarial behavior are reviewed.
- Changes improve or preserve required behavior without hiding regressions.

## Output

Return the evaluation plan, test cases, rubric, results, failure modes, revision diff or recommendation, regression status, assumptions, and unresolved questions. Communicate with the user in Traditional Chinese unless another language is requested.

