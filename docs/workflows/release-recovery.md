# Release, incident, and recovery workflow

Use this workflow when a project operates a deployed service, changes an existing release, or handles an incident. Customize it with real environment owners, authorization, deployment methods, recovery targets, and escalation routes. A template is not evidence that backups, restoration, or rollback work.

## Prepare a release

1. Identify the release and affected environment, data, integrations, prerequisites, compatible versions, and responsible person. Record risks, security implications, and unresolved assumptions.
2. Define checks for release readiness and health, monitoring and stop criteria, an appropriate rollout sequence, and a rollback or forward-recovery strategy. Verify recovery dependencies, including migrations, configuration, secrets, and downstream consumers. Where appropriate, test restoration using a non-production environment and safe data.
3. Obtain any project-required authorization before deployment or irreversible changes. Start only when prerequisites and recovery steps are known; stop or escalate if evidence is missing or the expected state differs.
4. Verify the release using project-specific checks and monitor the result. Record the actual version, environment, checks and results, changes made, and remaining risks. Do not claim a deployment or recovery succeeded without evidence.

## Respond and recover

1. Establish the affected systems, current impact, and immediate containment options. Use read-only diagnosis first when feasible, and follow the applicable incident and authorization procedures. Protect sensitive data and preserve appropriate evidence without copying credentials into tickets, logs, or chat.
2. **For an exposed or potentially compromised credential, arrange prompt revocation or rotation under the applicable authority before Git history cleanup.** Contain access, consider dependent services, use replacement credentials securely, and review available access evidence. Removing a secret from a file or rewriting history does not invalidate copies. Do not make unauthorized external changes or use a suspected compromised credential.
3. Choose rollback, restore, or forward recovery based on actual data state, compatibility and tested options. A code rollback might not reverse a migration or external side effect. Verify backups and restore procedures; if recovery is untested or unavailable, state the limitation and escalate instead of assuming it works.
4. Validate service health, data integrity, and access controls after recovery. Record evidence and uncertainties, then capture root-cause investigation, remediation, verification, and follow-up ownership. Follow applicable incident reporting requirements and avoid inventing approvals or completed controls.

Use the [migration plan template](../templates/migration.template.md) when state changes require a separate data plan. For deployments that support incremental rollout, [Google's SRE release guidance](https://sre.google/workbook/canarying-releases/) describes one way to evaluate a limited release before proceeding.
