---
name: release-recovery
description: Plan, verify, or investigate a release, rollback, incident, or recovery of a deployed service.
---

# Release and recovery

Use when work affects an actual deployed service or release. Follow the project-specific [release and recovery workflow](../../../docs/workflows/release-recovery.md), the user's authorization, and the service's operational procedures. Do not invent a deployment platform, recovery target, approval, or command.

1. Identify the intended change, affected environments and data, dependencies, current release, and observable success and failure signals. For externally synchronized hosts such as ChatGPT Sites, check for source divergence before editing or publishing (see `docs/workflows/chatgpt-sites.md`). State unknowns.
2. Define and, where practicable, test the rollout, health checks, stop criteria, rollback or forward recovery, and restore procedure before changing production. Account for data migrations, irreversible actions, and dependencies that may outlive an application rollback.
3. During an incident, first assess and contain the immediate impact. For exposed credentials, arrange revocation or rotation promptly under the applicable authority; do not wait for Git history cleanup. Protect evidence and avoid exposing secret values.
4. Verify recovery using available evidence and report what was done, what remains unknown, and follow-up actions. An agent must not claim that backups, restore, rollback, or deployment succeeded without evidence.
