---
name: dependency-maintenance
description: Review and update application dependencies, action pins, and scanner versions with provenance, compatibility checks and a recovery plan.
---

# Dependency maintenance

Inspect actual manifests and lockfiles; verify current versions, publisher provenance, advisories and compatibility with official upstream sources. Follow [dependency maintenance](../../../docs/workflows/dependency-maintenance.md). Keep updates focused, regenerate lockfiles using the project's package manager, run relevant checks and obtain the normal adversarial/security reviews. Do not auto-merge updates, invent package versions or assume a scanner proves safety. Record source/date, remaining uncertainty and rollback steps.
