---
name: ai-governance
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use when establishing practical rules, risks, ownership, and review controls for AI use in a team or project.
---

# Ai Governance

## Use when

Use this skill when defining practical governance for AI use, including risk classification, ownership, data handling, oversight, review, and incident response.

## Inputs

- Required: AI use case, users, systems, data, outputs, affected people, and operational context.
- Optional: Existing policy, risk framework, owners, incidents, retention rules, and review cadence.
- Preconditions: The use case and accountable decision owner can be identified.
- Missing information: Mark unknown risk factors and escalate legal, security, or ethical gaps for qualified review.
- Output artifact: Risk classification, control checklist, ownership model, review process, and unresolved questions.

## Procedure

1. Map the AI use cases, users, systems, data types, outputs, affected people, and operational context.
2. Classify impact and risk using data sensitivity, autonomy, scale, reversibility, security, legal exposure, and potential harm.
3. Define controls for access, approved tools, data minimization, retention, human oversight, testing, auditability, and incident response.
4. Assign accountable owners, reviewers, escalation paths, review cadence, and evidence required for continued use.
5. Produce a lightweight policy and control checklist proportional to the risk. Flag legal or regulatory questions for qualified review.

## Decision rules

- Higher-impact, less reversible, more sensitive, and more autonomous uses require stronger controls and human oversight.
- Every control needs an owner, trigger, evidence requirement, and response path.
- Separate policy requirements, factual evidence, risk judgments, and unresolved legal questions.

## Verification

- Each material use case has a risk class, owner, and required controls.
- Sensitive data, access, retention, oversight, and incident handling are addressed.
- Controls are testable and have review evidence or a defined collection method.
- Unresolved legal, ethical, security, and operational questions are explicit.
## Output

Return the structured artifact, assumptions, unresolved questions, and concrete verification or review criteria. Communicate with the user in Traditional Chinese unless another language is requested.

