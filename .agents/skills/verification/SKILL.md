---
name: verification
description: Select, run, and report appropriate checks for a change or project.
---

# Verification

Read the project verification commands and identify the changed behavior and affected boundaries. Choose available checks that exercise the risk: focused regression and negative cases where useful, then relevant integration, lint, type, build, and security checks. Avoid tests that merely duplicate implementation. Do not invent commands or coverage targets for an unknown stack. For repeatable checks or E2E flows discovered by an agent, save the verified path as a readable, auditable deterministic script or test so future runs require zero model calls and fail loudly when the system changes.

Run checks in the documented environment when possible. Report exact commands, outcomes, and any skipped or unavailable checks. Distinguish the template's own checks from application tests, and rerun affected checks after material fixes. CI success does not replace independent adversarial review or prove compliance.
