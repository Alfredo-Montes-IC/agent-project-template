# Agent Project Template

A stack-neutral starting point for projects developed by people and coding agents. Includes focused context routing, task ownership, architecture decisions, agent handoffs, GitHub issue/PR templates, and executable repository checks.

This is a workflow template, not an application framework. It does not select a language, provider, database, AI model, or deployment platform.

## Start a project

1. Follow the [solo project quickstart](docs/workflows/solo-quickstart.md) to create a project, initialize `dev` and your first task branch, and install the local hooks. To copy into an existing project, reconcile instructions and files rather than overwriting them.
2. Replace this README with your project's name, purpose, status, and setup steps.
3. Fill in [project brief](docs/product/project-brief.md), [architecture](docs/architecture/README.md), and [verification commands](docs/standards/verification.md). Mark unknown decisions as pending.
   Adapt the canonical [engineering guidelines](docs/standards/GUIDELINES.md) and client instructions using the [project customization workflow](docs/workflows/project-customization.md).
4. Update the [context map](docs/context/README.md) with real source directories and task-relevant documents.
5. Add only the application boundaries you need, such as `src/`, `apps/web/`, `apps/mobile/`, `services/api/`, or `infra/`. Place adapted [scoped instructions](docs/templates/scoped-agents.template.md) in each boundary as `AGENTS.md`.
6. Configure real application lint, type checks, tests, and CI before treating the project as runnable. Template checks validate repository context and guardrail behavior only.
7. Review visibility, license, branch protection, and secret management for your project before publishing it.
8. Make [security guidance](.agents/skills/security-review/SKILL.md) available to each agent and arrange [independent adversarial code review](docs/workflows/adversarial-review.md). Set up branch protection separately if review must be enforced by GitHub.

The quickstart also explains how to use the reviewer when you are the only developer. A separate agent session can review your own code; you do not need another employee. A host that cannot provide an independent reviewer leaves the review gate pending.

## Prompt to start or continue a project

Copy this into your coding agent and replace the bracketed details:

```text
I am working solo on [PROJECT NAME]. The goal is [GOAL].
My current task is [TASK AND EXPECTED RESULT].
Known constraints or stack: [DETAILS, OR "NOT YET DECIDED"].
Existing spending authorization and billing currency: [DETAILS, OR "NOT YET SET"].

Read AGENTS.md, the context map, and relevant scoped instructions. Inspect the
existing project and Git status before changing anything. Preserve existing work.
If this project is new or its stack has changed, follow the project-customization
workflow: adapt the project brief, architecture, GUIDELINES.md, verification
commands, context map, and agent adapters to confirmed facts. Keep unknowns
pending and don't copy organization-specific policy unless it applies.
Use budget-planning to estimate low/expected/high agent, API/tool, CI and hosting
costs, including Sites if used. Verify current prices and allowances; don't assume
an existing subscription includes API usage. Respect my existing spending limits.

Implement the task and run appropriate checks. During coding, ask a separate
adversarial subagent to challenge the implementation when your host permits it.
Before committing, have an independent reviewer inspect the exact staged snapshot,
fix blocking findings, re-review changed content, and record the local receipt.
Before opening or marking ready a code PR, invoke the security-review skill in an
independent reviewer session on the complete PR base-to-head diff. Fix blocking
security findings and repeat affected reviews if the diff changes. Record both
reviews, their revisions, findings, and check results in the PR.

If your host cannot delegate, use a separate agent session or tell me the review
is pending. Do not call self-review independent or invent passing checks. Follow
my authorization, your environment's permissions, and the project's Git workflow.
Report what changed, what was verified, and what remains unresolved.
```

For an existing project, keep its instructions and adjust the prompt to the actual task. Use the [solo quickstart](docs/workflows/solo-quickstart.md) for initial branch and hook setup.

## Run the security skill yourself

The general-purpose security expert is named **`security-review`**. Start with a request such as: “Use `security-review` to examine the complete PR diff and report findings.” In supported clients, you can also use:

| Client | Invocation |
|---|---|
| Codex | Type `$security-review` in your message, or choose it from `/skills`. |
| Claude Code | Type `/security-review` followed by the task. |
| Antigravity | Type `/security-review` where available, or ask for the skill by name. |
| Gemini CLI | Use `/skills list` to check discovery, then ask for `security-review` by name. |
| Grok Build | Type `/security-review` if it is listed, or ask for it by name. |

If a client does not discover it, ask it to read `.agents/skills/security-review/SKILL.md` directly. Check the installed client and [agent setup](docs/agents/README.md), because commands and permissions can differ by version.

## Directory map

```text
AGENTS.md                  Concise shared coding-agent contract
.agents/skills/            Canonical portable skills
.agents/agents/            Antigravity reviewer definitions
.codex/agents/             Codex reviewer definitions
.claude/agents/            Claude Code / Grok Build reviewer definitions
.gemini/agents/            Gemini CLI reviewer definitions
.claude/skills/            Generated Claude-compatible copies
.githooks/                 Local Git policy entry points
docs/context/              Entry point and task routing
docs/product/              Project intent, scope, and success criteria
docs/architecture/         Design and durable decisions
docs/standards/            Engineering and verification conventions
docs/workflows/            Git and multi-agent coordination
docs/tasks/                Durable task state when needed
docs/templates/            Task, handoff, ADR, and scoped-agent templates
scripts/                   Portable Python checks, bootstrap and policy helpers
.github/                   CI, issues, PRs, and instruction adapter
```

Start agents at [AGENTS.md](AGENTS.md), then the [context map](docs/context/README.md). Keep long research documents outside routine context; link relevant sections when assigning a task.

Any agent can read the shared contract and skill files directly. If its host supports native skills or instruction files, configure that host to point to these files; discovery and subagent support differ by product and are not guaranteed by this repository. For agents without native discovery, include the relevant paths in the task prompt. The supplied [source templates](docs/reference/source-templates/README.md) include organization-specific examples that require adaptation.

After bootstrap, the local commit hook requires a receipt for independent review of the staged tree, even when you wrote the code yourself. See the [review workflow](docs/workflows/adversarial-review.md). Local hooks cannot authenticate a reviewer or protect GitHub against bypasses; server enforcement needs an independently authenticated reviewer integration and active rules.

## Operations and project costs

Use [budget-planning](docs/workflows/budget-planning.md) with the [budget template](docs/templates/budget.template.md) for agent/subscription/API/tool costs, CI and hosting, including Sites when used. Keep current price sources and dates, low/expected/high estimates, included allowances and incremental cash cost. A budget document does not enforce provider limits or authorize new spending.

The template includes [dependency maintenance](docs/workflows/dependency-maintenance.md), [application CI setup](docs/workflows/project-ci.md), [release and incident recovery](docs/workflows/release-recovery.md), an optional [ChatGPT Sites workflow](docs/workflows/chatgpt-sites.md) and [Sites template](docs/templates/chatgpt-sites.template.md), and a [migration template](docs/templates/migration.template.md). Use the `migration-reviewer` for data changes and `accessibility-reviewer` for UI work. The configured rulesets keep zero required human approvals for solo work and require CI when activated; agent reviews remain separately recorded evidence.

## Validate the template

Requires Git and Python 3.10+. Initialize local controls and verify from the repository root:

```bash
python3 scripts/bootstrap.py
python3 scripts/verify.py
```

Windows PowerShell alternative:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check-context.ps1
```

The PowerShell wrapper delegates to the same Python checks. On Windows, `py -3` or `python` can replace `python3`. Checks cover context, relative links, skill parity, branch policies and basic secret patterns; they do not verify application behavior or detect every secret.

## License

No distribution license has been selected. Choose one before making this template broadly reusable outside your own projects.

## Shared skills and protected branches

The shared workflows include [security-review](.agents/skills/security-review/SKILL.md). Codex, Antigravity and Gemini CLI use `.agents/skills/`; Claude's `.claude/skills/` is generated from the same source and checked for drift. See [client setup and invocation](docs/agents/README.md). No global/personal skills are installed.

Use [adversarial-code-reviewer](.agents/skills/adversarial-code-reviewer/SKILL.md) for independent review, [debugging](.agents/skills/debugging/SKILL.md) for diagnosing failures, and [verification](.agents/skills/verification/SKILL.md) for choosing checks. For a client without skill discovery, provide the path in your prompt.

Use `task -> dev -> main`. Local bootstrap blocks direct main/dev commits and pushes in that clone. [Git workflow](docs/standards/GIT_WORKFLOW.md) documents CI routing and versioned server rulesets. GitHub settings are not inherited just by copying template files and remain pending until effective rules are verified. Private-repository rulesets may require GitHub Pro.
