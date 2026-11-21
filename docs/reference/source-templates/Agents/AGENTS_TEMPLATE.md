# Project agent instructions template

This is a drafting aid. Adapt it to the actual project and reconcile it with the root `AGENTS.md`; do not treat placeholders as established facts.

## Project and context

- Purpose and users: [describe the project and intended audience]
- Current stack and runtime: [confirmed technologies, or pending]
- Source boundaries: [actual directories and responsibility of each]
- Relevant documentation: [project brief, architecture and scoped rules]

## Set up and verify

| Activity | Directory | Command | Prerequisites |
|---|---|---|---|
| Setup | [directory] | [verified command] | [requirements] |
| Run | [directory] | [verified command] | [requirements] |
| Lint or type check | [directory] | [verified command] | [requirements] |
| Tests and build | [directory] | [verified commands] | [requirements] |

Mark unknown commands pending; do not guess a package manager, language or runtime. Use the project's `docs/standards/verification.md` as the source for actual checks.

## Engineering and security

- Follow confirmed conventions in `docs/standards/GUIDELINES.md` and scope-specific instructions.
- Validate external input and enforce access at the appropriate boundaries. Protect secrets and private data.
- Keep changes focused, preserve unrelated work, and update architecture decisions when contracts change.
- Add meaningful verification for changed behavior and report checks that could not run.

## Collaboration and delivery

- Follow the project's Git and independent-review workflow, including adversarial review and security review of code PRs.
- Document acceptance criteria, relevant decisions and handoffs. Identify unavailable reviewers and checks as pending.
- Record special rules for each real component in its own scoped instructions and route agents to them through the context map.
