---
name: ai-playbook-maintainer
description: Use to maintain an AI playbook or capability website from repository truth.
---

# Ai Playbook Maintainer

## Use when

Use this skill when maintaining an AI playbook, capability catalog, documentation site, or routing index whose authoritative content comes from the repository.

## Procedure

1. Identify the repository sources of truth, generated or published surfaces, audience, requested update, and acceptance criteria.
2. Inventory relevant skills, documentation, metadata, links, examples, and navigation. Check for duplicates, stale references, missing entries, and inconsistent naming.
3. Trace each published claim to repository evidence. Do not invent capabilities, statuses, integrations, or roadmap commitments.
4. Apply the smallest synchronized change to the source and any required derived surface, preserving local format and compatibility.
5. Validate frontmatter, links, counts, routing references, examples, and generated output using available repository checks.
6. Review the diff for accidental scope expansion, secrets, personal data, machine-specific paths, and claims unsupported by source files.
7. Record the changed source, affected surfaces, verification evidence, remaining drift, and any manual publication dependency.
8. For a website or catalog update, preview the affected navigation and representative entry before publication; for a repository-only update, validate the source-to-index mapping instead.

## Decision rules

- The repository is authoritative; a playbook or website is a projection of repository truth.
- Prefer updating source files before generated or presentation layers.
- Keep category names, skill names, descriptions, and links consistent across surfaces.
- Treat missing or stale source evidence as a blocker for publishing a claim.
- Do not publish, deploy, or alter external systems unless explicitly requested.
- Treat counts, category labels, and route order as derived claims that must be regenerated or checked from source.
- Keep generated content reproducible; record the generator or manual synchronization step when applicable.

## Verification

- Every updated entry maps to an existing source file or an explicitly documented planned item.
- Navigation, links, metadata, and counts are internally consistent.
- Repository validation passes after the final modification.
- The report distinguishes synchronized changes from external publication still required.
- At least one representative entry and one changed navigation path have been checked, or the limitation is explicit.

## Output

Return a maintenance report with sources of truth, synchronized surfaces, changed files, validation evidence, detected drift, and publication or follow-up actions.

