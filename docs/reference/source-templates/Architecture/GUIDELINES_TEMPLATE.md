# Project architecture and engineering guidelines template

This is a drafting aid. Keep the authoritative project guidelines in `docs/standards/GUIDELINES.md` and the actual design in `docs/architecture/README.md`. Populate the sections below with confirmed facts and project-specific decisions; mark unknowns pending.

## Design and boundaries

Describe the system purpose, components, responsibilities, data flows, interfaces, dependencies and trust boundaries. Document accepted decisions and compatibility constraints in architecture records.

## Engineering conventions

Record the actual languages, runtimes, coding style, error handling, logging, dependency and security conventions. Link to component-specific rules where necessary rather than creating conflicting guidance.

## Verification and release

Record real setup, lint, tests, build and health checks in `docs/standards/verification.md`. For deployed systems describe release checks, monitoring, rollback and tested recovery. Specify data migration and compatibility requirements only when applicable.

## Maintenance

Update design and guidelines when behavior or accepted decisions change. Keep secrets out of documentation and do not claim testing or compliance without evidence.
