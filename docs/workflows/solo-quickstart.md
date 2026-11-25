# Solo project quickstart

You are the developer. The independent reviewer can be a separate agent session; a second person is not required. The local gate is a reminder, not proof of who reviewed. GitHub enforcement needs an authenticated reviewer integration and active branch rules.

## Create the project

1. Create a new GitHub repository from the template's default branch only, or copy the files into an existing project after reconciling its instructions. If GitHub offers to include all template branches, leave that option off: generated branches have unrelated histories and cannot be merged with one another. See [GitHub's template instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).
2. On GitHub create `dev` **from your new repository's `main`**. The template uses `task -> dev -> main`; creating `dev` from your own `main` gives them shared history. Do not create or overwrite a branch that already exists without inspecting it. GitHub settings, secrets, hooks and branch protections are not copied with the files.
3. Clone your new repository. In the clone, fetch your new `dev`, create a task branch, and initialize the tools. Replace `first-task` with a descriptive lowercase name:

   ```bash
   git fetch origin dev
   git switch -c docs/first-task origin/dev
   python3 scripts/bootstrap.py
   python3 scripts/verify.py
   ```

   On Windows, `py -3` or `python` can replace `python3`. Bootstrap installs local hooks and refuses to replace a different existing hooks path; integrate the existing hooks if that happens. The local hook blocks direct pushes to `main` and `dev` once installed. Creating `dev` on GitHub in step 2 avoids needing to push it through that hook.
4. Follow the [project customization workflow](project-customization.md), including adapting `docs/standards/GUIDELINES.md` to the actual project. Update the brief, architecture, README, context map, verification commands, and client adapters as applicable. Add stack-specific build, tests, CI, dependency and secret management as you select them. The template's own checks do not test your application. Do not put real secrets in files you commit.
5. Create a [budget record](budget-planning.md) for the actual agents, APIs, tools and hosting used. Configure [application CI](project-ci.md) when the stack exists, and apply the recovery/migration/accessibility workflows only where relevant. Routine agent review does not require adding a second human or buying a reviewer service.

## Make and review a change

1. Ask your agent to read `AGENTS.md`, the relevant skill files, and the task. For code changes, request independent adversarial and code standards reviewers alongside any applicable specialists. Work on a task branch, stage the intended files, and run relevant checks.
2. Run `python3 scripts/review_gate.py snapshot`. Give the independent reviewers the staged diff, tree, parent, requirements, and test results. Use `adversarial-code-reviewer` and, for code changes, `code-standards-review`. If your host cannot delegate, use a separate agent session or a human reviewer. Keep unavailable independent reviews pending.
3. Fix blocking findings, restage, rerun checks, and run `python3 scripts/review_gate.py snapshot` again before obtaining re-review of changed content. For a passing review, record the exact new tree and parent from `snapshot`: `python3 scripts/review_gate.py record --tree TREE --parent PARENT --reviewer SESSION --evidence SUMMARY`. Quote arguments containing spaces in your shell. Use `unborn` for a null parent. The receipt is local and unauthenticated; do not include secrets in it.
4. Commit your reviewed change. Before opening or marking ready a code PR, invoke the portable `security-review` skill in an independent reviewer session on the complete base-to-head PR diff. Confirm the code standards review covers the proposed diff. Fix blocking findings and repeat affected reviews after material changes. Record all reviewer sessions, exact revisions, findings and disposition in the PR, and link any governing GitHub issue (`Refs #<n>` on `task -> dev`; `Closes #<n>` or `Fixes #<n>` on `dev -> main` when solved). Push the task branch and open a PR into `dev`. After checks and review, merge to `dev`; promote `dev` to `main` through another PR, reviewing the final promotion diff and checks. Never claim an automated check proves a human or agent reviewed.
5. After promotion, verify the GitHub branch cleanup, confirm solved linked issues closed on `main`, return to local `dev`, and safely delete the matching local task branch using the checks in the [Git workflow](../standards/GIT_WORKFLOW.md). Report retained branches or unavailable cleanup; never delete `dev` or `main`.

## Before relying on GitHub protection

Files in this repository do not activate rules in a new GitHub repository. Configure and verify protection on both `dev` and `main`, using your GitHub plan's available controls; require trusted checks and block direct pushes. If you need GitHub itself to enforce independent AI review, configure an independently authenticated reviewer integration tied to the exact PR head and require its status from the trusted app. Do not mistake the local receipt or the template's current zero-approval rules for that integration. See [GitHub branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule). Until configured and verified, server-side enforcement remains pending.
