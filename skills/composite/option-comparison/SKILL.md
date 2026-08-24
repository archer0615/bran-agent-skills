---
name: option-comparison
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when comparing products, designs, vendors, or implementation choices against explicit criteria.
---

# Option Comparison

## Use when

Use this skill when comparing products, designs, vendors, tools, or implementation choices against explicit decision criteria.

## Inputs

- Required: Options, decision question, owner, constraints, and comparison criteria.
- Optional: Weights, budget, evidence sources, time horizon, risk tolerance, and pilot constraints.
- Preconditions: At least two realistic options or an explicit baseline can be identified.
- Missing information: Mark unavailable values unknown and state assumptions; do not invent scores.
- Output artifact: Comparable matrix with criteria, evidence, trade-offs, sensitivity, recommendation conditions, and gaps.

## Procedure

1. Clarify the decision, owner, constraints, time horizon, budget, must-haves, and unacceptable risks.
2. Define weighted criteria and the evidence needed to evaluate each option.
3. Gather comparable information, normalize units and assumptions, and identify missing or stale evidence.
4. Build the comparison with facts, estimates, costs, risks, trade-offs, reversibility, and fit.
5. Separate observed facts from judgment and sensitivity to criteria weights.
6. Recommend an option with conditions, mitigations, and the evidence that would change the recommendation.
7. Run a sensitivity check on the highest-impact weights or unknowns and identify whether a small pilot can reduce decision risk.

## Decision rules

- Use identical criteria and scoring definitions for all options.
- A disqualifying constraint overrides a high aggregate score.
- Do not invent missing values; mark them unknown or state estimation assumptions.
- Include total cost, operational burden, exitability, and downside risk where relevant.
- Treat a high score as insufficient when evidence quality is weak or the option violates a must-have.
- Prefer conditional recommendations when the ranking changes under plausible weights or assumptions.
- Own the comparison matrix and normalized criteria; hand off the matrix, evidence gaps, and sensitivity findings to `decision-researcher` for the final decision brief.
- Do not use this Skill alone when the primary need is evidence gathering without comparable options.

## Verification

- Every option is evaluated against the same criteria or differences are explained.
- Material claims have sources or are labeled assumptions.
- Total cost, operational risk, compatibility, and exit or rollback implications are considered where relevant.
- The recommendation is traceable to the comparison and unresolved gaps are explicit.
- Sensitivity, pilot or validation path, and exit criteria are stated when the decision is material.

## Output

Return the comparison, criteria and weights, evidence, assumptions, trade-offs, recommendation with conditions, unresolved questions, and verification criteria. Communicate with the user in Traditional Chinese unless another language is requested.

