# Project development guidelines template

Adapt these prompts to actual project decisions. Keep the maintained guidelines in `docs/standards/GUIDELINES.md`; do not maintain competing client-specific copies. Mark unconfirmed conventions pending.

## Language and style

- Runtime and supported versions: [confirmed versions or pending]
- Formatting, naming and type conventions: [project rules]
- Lint and formatting commands: [verified commands]
- Error handling and logging: [project conventions, redaction and observability]

## Architecture and interfaces

Document real source boundaries, dependency direction, public interfaces, data contracts and applicable architecture decisions. Prefer existing patterns and focused changes.

## Verification

Document actual setup, unit and integration tests, build and deployment checks in `docs/standards/verification.md`. Select regression checks for meaningful behavior and failure cases. Report unavailable checks; do not invent coverage targets or results.

## Security and privacy

Identify actual trust boundaries, authentication and authorization requirements, external input validation, secret management and private-data handling. Use the portable `security-review` skill and policies that actually apply to the project.

## Delivery and recovery

Follow the project's branch, independent adversarial review and security-review workflow. Record compatibility, migration, rollback and recovery requirements when a change affects persistent data or a deployed service.

## Documentation and maintenance

Keep the README, context map, scoped agent instructions, architecture records and relevant operational guidance aligned with observed behavior. Record unknowns and revisit this document when project conventions change.
