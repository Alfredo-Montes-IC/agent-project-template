# Context map

Read the [root contract](../../AGENTS.md), inspect the checkout, and load the smallest relevant context set.

## Current state

Uncustomized template. No application, dependency manifest, deployed service, or application test suite exists. Replace this status after initialization.

## Task routing

| Task | Source | Owning paths |
|---|---|---|
| Product scope and acceptance | [Project brief](../product/project-brief.md) | `docs/product/` |
| New project or major stack change | [Project customization](../workflows/project-customization.md) | Shared standards, project docs, and applicable client adapters |
| Design and contracts | [Architecture](../architecture/README.md), accepted decisions | `docs/architecture/` |
| Implementation | Relevant code and scoped instructions; add concrete links after setup | Assigned code boundary |
| Verification | [Verification commands](../standards/verification.md), [engineering standards](../standards/GUIDELINES.md) | Owning component and `scripts/` |
| Git and CI | [Git workflow](../standards/GIT_WORKFLOW.md) | `.github/`, `scripts/` |
| Parallel work | [Multi-agent workflow](../workflows/multi-agent.md), [handoff](../templates/handoff.template.md) | Assigned task paths |
| Security | [Portable security skill](../../.agents/skills/security-review/SKILL.md); applicable project policy | Changed trust boundaries and their controls |
| Agent integrations and permissions | [Integration setup and verification](../agents/integrations.md) | Project integrations and client configuration |
| Reproduce a bug | [Debugging skill](../../.agents/skills/debugging/SKILL.md) | Affected behavior and evidence |
| Choose and report checks | [Verification skill](../../.agents/skills/verification/SKILL.md), [verification commands](../standards/verification.md) | Changed behavior and integration boundaries |
| Code review | [Independent adversarial review](../workflows/adversarial-review.md) | Complete proposed code change |
| Specialist review | [Reusable reviewer roles](../workflows/reviewer-roles.md) | Scoped task evidence and findings |
| Budget and service selection | [Budget planning](../workflows/budget-planning.md), [budget template](../templates/budget.template.md) | Project costs, current pricing evidence and limits |
| Dependencies and secrets | [Dependency maintenance](../workflows/dependency-maintenance.md) | Manifests, workflows, findings and updates |
| Application CI and delivery | [Project CI and configured job inventory](../workflows/project-ci.md), [release/recovery](../workflows/release-recovery.md) | Actual component checks, deployment and recovery |
| Data migration | [Migration template](../templates/migration.template.md) | Affected data, compatibility and verified recovery |
| Additional templates | [Imported source templates](../reference/source-templates/README.md) | Optional references; adapt before use |

## Durable context

Approved specs and accepted ADRs record decisions; code and executable checks establish implemented behavior. Flag contradictions instead of silently assuming one document is current. Templates are drafting aids, not approved contracts.

Store task-specific status in `docs/tasks/` or a linked issue. Keep decisions in architecture records. Add research/archive directories only when needed and keep them outside default task context. Update this map whenever source boundaries change.

## Portable agent workflows

Read [agent setup and shared skills](../agents/README.md) for the task-to-skill map, common working lifecycle, client discovery, local bootstrap, invocation differences, and enforcement limitations. The template includes repository regression checks; no application runtime exists yet.
