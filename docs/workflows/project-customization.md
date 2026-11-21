# Customize a new project

Use this workflow when initializing a project or changing its stack, boundaries, or agent setup. The agent should inspect the existing checkout and user instructions first, then adapt files using observed facts and authorized decisions. Do not invent a stack, commands, architecture, policies, approvals, or tests. Mark unresolved choices as pending and ask only when needed for a decision; preserve existing project instructions and unrelated work. Supplied reference templates are examples, not binding policy.

## Put each kind of information in its owning location

| Source or topic | Canonical destination | What to customize |
|---|---|---|
| Project intent | `README.md`, `docs/product/project-brief.md` | Purpose, audience, scope, setup and confirmed requirements |
| Architecture and ADR examples | `docs/architecture/README.md`, `docs/architecture/decisions/` | Actual boundaries, interfaces, constraints and accepted decisions |
| Both supplied `GUIDELINES_TEMPLATE.md` examples | `docs/standards/GUIDELINES.md` | Reconcile applicable engineering, naming, testing, security and accessibility conventions; mark unknowns pending |
| Real checks and prerequisites | `docs/standards/verification.md` | Commands, directories, expected results and unavailable checks |
| Component-specific instructions | `AGENTS.md` within the applicable component, adapted from `docs/templates/scoped-agents.template.md` | Rules unique to that scope, with links to the shared contract |
| Agent entry points and reusable skills | Root `AGENTS.md`, client adapters, `.agents/skills/` | Keep shared guidance canonical; adjust only clients actually used and sync managed mirrors |
| Context routing | `docs/context/README.md` | Link actual source paths, project docs, scoped rules and applicable skills |
| Task, handoff, audit, issue and PR examples | `docs/templates/`, `.github/`, or a project-specific location | Adapt relevant examples for the project; retain existing workflows and avoid duplicate authoritative copies |

For example, review the two `GUIDELINES_TEMPLATE.md` examples under `docs/reference/source-templates/`, compare them with the actual project and `docs/standards/GUIDELINES.md`, and incorporate only applicable rules into the canonical guidelines. Record real language, formatter, test, security and accessibility conventions where confirmed; leave unknowns pending. Do not copy example cloud, framework or compliance rules wholesale. Link the canonical guidelines from the context map and relevant scoped instructions rather than maintaining separate conflicting versions for each agent.

## Agent placement and discovery

Start with the [client setup](../agents/README.md). Root `AGENTS.md` is the shared contract; `CLAUDE.md`, `.github/copilot-instructions.md`, and the existing Gemini project settings are adapters. Shared skills live under `.agents/skills/`; synchronize the managed Claude mirror with `python3 scripts/sync_skills.py` after modifying a skill. Do not overwrite an existing client's settings or instructions: inspect, preserve and integrate them. Use actual component-level `AGENTS.md` files only where the project has boundaries that need them; route agents to the applicable scopes explicitly rather than assuming every client discovers nested files.

Verify discovery in each installed client and version the project uses. For a client or surface without confirmed automatic discovery, include the root contract, applicable scoped instructions, and relevant skill paths in the task prompt. Do not claim native skill or subagent support based solely on a product name. Keep higher-priority user and host instructions intact.

## Finish and maintain

Run `python3 scripts/sync_skills.py --check`, the relevant project verification, and `git diff --check`. Report what was customized, evidence for stack-specific choices, remaining pending items, and any client discovery or checks not verified. Revisit these files when the project or client configuration changes. This workflow does not activate GitHub rules, install global skills, or establish security compliance.
