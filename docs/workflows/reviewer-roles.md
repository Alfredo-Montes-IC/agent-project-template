# Reusable independent reviewer roles

Use these task prompts for a separate subagent or session when the host and user permit delegation. Native project role definitions are included for supported clients; see [agent setup](../agents/README.md). They do not automatically spawn agents or guarantee tool permissions. Supply the objective, exact staged tree or commit range, relevant instructions, acceptance criteria, allowed paths, and verification evidence. Do not include secrets. Reviewers should avoid modifying the author's files; the author fixes findings and requests re-review of material changes. The mandatory adversarial and PR security reviews remain governed by [their workflow](adversarial-review.md).

## Security reviewer

For every code PR, read the general `security-review` skill and any policy actually applicable to the project. Examine the complete base-to-head diff, changed trust boundaries and suspect paths to concrete sinks. Challenge authentication, authorization, tenant isolation, injection, secrets, CI permissions, dependency provenance, and AI tool access where relevant. Report confirmed issues with location, impact, and remediation; distinguish deployment assumptions and policy questions from proven vulnerabilities. Record reviewed base and head, limitations, findings and disposition.

## Verification reviewer

Read the `verification` skill. Challenge acceptance criteria, test selection, realistic failure cases, test isolation, integration coverage, and evidence for the exact change. Run safe checks when authorized and available. Report missing coverage or failures with reproduction and expected behavior; distinguish unrun checks from passing checks.

## Adversarial reviewer

Use the `adversarial-code-reviewer` skill. Independently challenge correctness, requirements, regressions, edge cases, security and tests. A specialist review may contribute evidence, but does not automatically replace the required independent adversarial review. Record identity or session, reviewed revision, findings and outcome. No findings is a report, not proof of absence of defects.

## Migration reviewer

Use the `data-migration` skill and release/recovery workflow when schemas or persistent state change. Challenge compatibility, idempotence, rollout order, data handling, backup evidence and tested restoration. Distinguish reversible steps from irrecoverable ones; do not execute a migration or claim a restore was tested without evidence.

## Accessibility reviewer

Use `accessibility-review` for UI work. Examine keyboard flows, focus, semantics, labels, errors, contrast and responsive behavior, with manual evaluation where tools are insufficient. Report checks not possible in the current environment; automated results alone do not establish accessibility conformance.
