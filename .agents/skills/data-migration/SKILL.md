---
name: data-migration
description: Plan, implement, review, or recover a change to stored data, schema, or persistent state.
---

# Data migration

Use when a change affects stored data, schemas, or persistent state. Prepare a project-specific plan using the [migration template](../../../docs/templates/migration.template.md). Respect the actual project's data classification, access controls, retention, and authorization; do not copy production data into development or logs by default.

1. Identify the affected data and consumers, current and target state, compatibility across deployed versions, dependencies, ownership, and unknowns. Define observable acceptance and stop criteria.
2. Document and test a backup and restore path where applicable. Decide whether rollback is actually possible or whether forward recovery is required, especially after writes or destructive transformations. Never represent an untested backup as a proven recovery.
3. Design workload-appropriate bounded batches, idempotency or safe retries, concurrency controls, progress and reconciliation. Consider partial failure and duplicate or concurrent writes. Prefer staged, backward-compatible changes where feasible.
4. Test using safe representative data and validate counts, invariants, permissions, and application behavior. Record the rollout order, monitoring, failure response and evidence. Pause when prerequisites, recovery, or authorization are unresolved; do not execute irreversible production actions without the required authorization.
