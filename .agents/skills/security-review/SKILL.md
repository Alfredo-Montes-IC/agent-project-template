---
name: security-review
description: Review security when designing, implementing, changing, or reviewing software, infrastructure, automation, or AI integrations.
---

# Software security expert

Use this guidance for security-relevant work, together with the project's actual security policy and requirements. Read the relevant code and configuration before drawing conclusions. This file can be read directly by any coding agent; native skill discovery depends on the host configuration.

1. Identify assets, trust boundaries, entry points, principals, data sensitivity, and relevant deployment assumptions. Trace changed paths to their sinks and check existing controls.
2. Review authentication and authorization, tenant and object isolation, validation and injection, secrets, cryptography and TLS, logging and error exposure, dependencies, CI permissions, infrastructure, and resource limits as applicable. For AI integrations, treat prompts, retrieved content, and tool outputs as untrusted; enforce access and tool permissions outside the model.
3. Prefer narrow, testable controls at the boundary. Add proportionate verification, including negative cases when useful. Check authoritative current sources for versions and external requirements when needed; state what could not be verified.
4. Report findings with location, evidence, realistic impact, and remediation. Separate confirmed issues from assumptions requiring deployment verification and from policy deviations. Do not claim compliance or approval without evidence.
5. Protect secrets and private data. Escalate unresolved security decisions according to the actual project policy; do not invent exceptions, approvals, or certifications.

Use the [review checklist](references/review-checklist.md) where relevant to the component.
