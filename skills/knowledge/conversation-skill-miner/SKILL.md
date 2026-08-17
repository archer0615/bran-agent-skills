---
name: conversation-skill-miner
description: Use to extract reusable procedures or skills from a conversation.
---

# Conversation Skill Miner

## Use when

Use this skill to extract a repeatable procedure, decision rule, prompt pattern, or skill candidate from a conversation or task history.

## Procedure

1. Identify the conversation’s goal, successful outcome, repeated decisions, inputs, constraints, and observable steps.
2. Separate durable procedure from one-off context, personal data, secrets, and unsupported assumptions.
3. Extract trigger conditions, required inputs, decision rules, procedure, exceptions, verification, and output format.
4. Compare the candidate with the existing skill library to detect overlap, conflicts, or a better destination.
5. Draft the smallest reusable skill or recommend against creating one when the pattern is not sufficiently repeatable.
6. Validate the draft against representative cases and preserve the source terminology needed for future use.

## Verification

- The candidate has a clear trigger and reusable outcome.
- One-off details and sensitive information are removed.
- Overlap with existing skills is identified and resolved.
- The procedure can be followed and verified by another agent.

## Output

Return the mined pattern, reusable skill draft or no-create recommendation, overlap analysis, assumptions, source evidence, and validation criteria.

