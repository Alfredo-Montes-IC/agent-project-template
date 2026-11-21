# Data migration plan: [name]

This is a planning aid. Replace placeholders with verified project facts; mark unknowns and incomplete checks as pending. Do not include secrets or raw sensitive data.

## Scope and state

- Owner, environment, related task or decision:
- Affected data, classification, access and retention requirements:
- Current state, desired state, consumers, dependencies, and expected volume:
- Assumptions and unknowns:

## Compatibility and rollout

- Deployment and migration order; compatibility with old and new readers and writers:
- Batching, time and capacity limits, concurrency, retries, idempotency, and progress tracking:
- How partial failures, duplicate writes, and concurrent updates are handled:
- Preconditions and authorization required before execution:

## Recovery

- Backup location and access owner, restore procedure, and date/result of a restore test:
- Rollback, forward-recovery, or both; impact of writes after migration and any irreversible transformations:
- Stop criteria, incident response, and escalation route:

## Verification and evidence

- Safe test data and environments; expected counts, invariants, and behavior:
- Pre-migration baseline, post-migration reconciliation, permission and application checks:
- Monitoring, completion criteria, results, unresolved risks, and follow-up owner:
