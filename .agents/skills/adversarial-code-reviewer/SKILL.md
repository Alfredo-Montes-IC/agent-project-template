---
name: adversarial-code-reviewer
description: Independently challenge a proposed code change before commit, pull request, or promotion.
---

# Adversarial code reviewer

Use as an independent reviewer of a change authored by a person or another agent. Follow the project's review workflow and host permissions. A role change in the author's own session does not create independence.

Inspect the exact staged diff or commit range, requirements, relevant surrounding code, and test evidence. Actively seek correctness, security, data loss, concurrency, integration, and regression failures. Trace candidate defects to actual code paths and try to disprove them. Do not assume an external control exists without evidence. Inspect tests for meaningful missing cases and run safe relevant checks where available.

Report actionable findings first, with severity, location, evidence, concrete impact, and a suggested correction. Distinguish confirmed defects from unresolved assumptions and state checks not run. If there are no findings, say so explicitly while noting residual risk. Do not approve with unresolved blocking findings. The author fixes findings and requests re-review of material changes; verify the exact final staged tree or commit again.

Record the reviewed revision, reviewer session and findings/disposition in the project's handoff or PR. For the optional local receipt process, follow [the review workflow](../../../docs/workflows/adversarial-review.md). The receipt is not authenticated server-side proof of review.
