---
name: decision-researcher
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when a decision needs criteria, evidence, alternatives, and a recommendation.
---

# Decision Researcher

## Use when

Use this skill when a decision needs explicit criteria, evidence, alternatives, trade-offs, and a recommendation rather than a simple factual answer.

## Inputs

- Required: Decision question, decision owner or audience, constraints, and decision horizon.
- Optional: Candidate options, existing evidence, budget, risk tolerance, and deadline.
- Preconditions: Decision criteria can be defined or the missing criteria can be clarified.
- Missing information: Label assumptions and confidence; escalate material high-impact gaps for review.
- Output artifact: Decision brief with criteria, evidence, comparison, recommendation, confidence, risks, and next action.

## Procedure

1. Define the decision, decision owner, deadline, constraints, non-negotiables, and consequences of delay.
2. Establish evaluation criteria and relative importance before comparing alternatives. Separate must-have criteria from preferences.
3. Gather relevant repository evidence first, then current or external evidence when required. Record source, date, confidence, and unresolved gaps.
4. Identify realistic alternatives, including the option to defer or do nothing when relevant.
5. Compare alternatives against the criteria, making assumptions and trade-offs explicit. Distinguish facts, estimates, and judgments.
6. Recommend an option with rationale, risks, mitigations, reversibility, and a concrete next action. State what evidence would change the recommendation.
7. Stress-test the recommendation against the most important uncertain assumption and a plausible downside case before finalizing it.

## Decision rules

- Do not present a preference as an objective fact.
- Use primary or authoritative sources for high-impact, current, or technical claims.
- Avoid false precision when evidence is incomplete; show confidence and sensitivity to assumptions.
- Escalate legal, security, financial, medical, or production-impact questions to appropriate human review.
- Include defer, do-nothing, or reversible experiment options when they are credible alternatives.
- If the recommendation changes under reasonable weights or evidence interpretations, present a conditional recommendation instead of a single winner.
- Use `option-comparison` when the primary missing artifact is a normalized multi-option comparison; own the final recommendation after comparable evidence is available.

## Verification

- Criteria cover the stated decision and are applied consistently to every alternative.
- Material claims have evidence or are labeled as assumptions.
- The recommendation follows from the comparison and includes risks and reversibility.
- Open questions and decision-changing evidence are explicit.
- The recommendation has a confidence level and a stated sensitivity or downside check.

## Output

Return a decision brief with objective, criteria, alternatives, evidence, comparison, recommendation, confidence, risks, unresolved questions, and next action.

