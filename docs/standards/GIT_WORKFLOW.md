# Git workflow

## Branches and integration

| Branch | Purpose | Incoming changes |
|---|---|---|
| `main` | Stable template / production baseline | PR from this repository's `dev` only |
| `dev` | Integration | PR from an allowed task branch |
| `feat/*`, `fix/*`, `docs/*`, `refactor/*`, `test/*`, `chore/*`, `security/*`, `hotfix/*` | One bounded change | Local commits, non-forced pushes |

Create task branches from current `dev`, use lowercase descriptive names, and record the task/issue. Even hotfixes enter via `dev`; do not bypass the stable-branch flow. Use Conventional Commits. Promote through `task -> dev -> main`. Do not write or push directly to `main` or `dev`, delete them, or force-update history. Stage task-owned files only, inspect the diff, and preserve unrelated work.

Run `python3 scripts/bootstrap.py` in every clone to install the [local hooks](../../.githooks/pre-commit). The commit hook checks the exact index snapshot, including shared-skill parity and basic secret hygiene. The push hook inspects destination refs, so `git push origin HEAD:main` is also blocked. Fetch missing history before pushing to an existing branch; unverifiable fast-forwards are rejected. These hooks are not a server-side security boundary.

Code changes require the independent adversarial review in [the review workflow](../workflows/adversarial-review.md) before commit or PR. Record the reviewed revision and outcome in the PR. Repeat review when later changes invalidate it. If an independent reviewer is unavailable, leave the review pending; do not represent self-review as independent or merge as though the gate passed.

Before opening or marking ready a code PR, obtain an independent `security-review` of the complete base-to-head diff and record its result separately. A generic CI pass or local review receipt does not establish that this review occurred. Re-review affected changes if the reviewed diff changes.

Inspect remotes and remote history before publishing. Adding `origin` does not upload files or authenticate the current environment. Never store credentials in Git URLs or documentation.

## Server enforcement

Versioned [main](../../.github/rulesets/main.json) and [dev](../../.github/rulesets/dev.json) rulesets require PRs, resolved review threads, and successful `repository-checks`, `windows-checks`, `python-minimum-checks`, `secret-scan` and `branch-policy` jobs; block deletion and non-fast-forward pushes; and configure no bypass actors. Zero human approving reviews are required for a solo owner working with an agent. Independent agent and security reviews are recorded in PRs; local receipts are self-reported, so do not describe them as an authenticated server review check. No paid reviewer integration is required by this template. Activate only available branch controls and report plan restrictions without inventing enforcement.

The metadata-only `pull_request_target` workflow checks PR routing from the trusted base workflow, without checking out or executing PR code and without using secrets. Repository verification runs separately on PR code with read-only permissions. Initial installation needs reviewed bootstrap PRs before the trusted workflow exists on the base/default branch. Required-check names alone are not a defense against a malicious administrator who can change workflows or settings; add independent review/organization-managed controls when needed. Bootstrap does not activate GitHub settings. Apply and verify them with an authenticated `gh` CLI that has repository administration access:

```bash
python3 scripts/apply_rulesets.py --repo OWNER/REPOSITORY
python3 scripts/apply_rulesets.py --repo OWNER/REPOSITORY --apply
python3 scripts/apply_rulesets.py --repo OWNER/REPOSITORY --check
```

The first command previews only. The apply command updates only named template rulesets and preserves unrelated rulesets. GitHub may require a paid plan for private-repository enforcement. Never change repository visibility or buy a plan to work around that limit without the owner's instruction. Mark protection as pending until GitHub returns active effective rules. A JSON file, a failing workflow after a push, or a proposed ruleset alone does not protect a branch. New repositories made from this template need their own `dev` branch, hook installation, and server settings.

Inspect remotes and remote history before publishing. Never put credentials in Git URLs, files or handoffs. Use [multi-agent isolation](../workflows/multi-agent.md), one writer per file, separate worktrees, and reviewed PRs. Record branch, commit, ownership, check results and unavailable enforcement in the handoff.

## Cleanup after merge

Opening a PR does not delete its source branch. After a task PR is merged into `dev` and its result is promoted by PR into `main`,
the trusted [cleanup workflow](../../.github/workflows/cleanup-branches.yml) deletes the task branch.
Keep both permanent branches after the promotion. Do not enable indiscriminate
auto-deletion that could delete an unprotected `dev` branch.

The cleanup workflow reads GitHub PR metadata without checking out any PR code. It verifies
same-repository ownership, actual merge status, base `dev`, allowed task names, and that the
merged result remains in `dev`. It deletes only a head still matching the PR's reviewed SHA,
using an atomic Git force-with-lease deletion to preserve concurrent commits. No force-update
of history is performed. Local hooks continue blocking manual deletion; the dedicated workflow
is the authorized post-merge cleanup path. It uses the repository-scoped Actions token with
contents write and PR read permissions. It never changes branch protections or visibility.

Initial installation and manual runs inspect at most the newest 100 closed PRs targeting `dev`;
this also cleans up already-merged task branches. Branches with new commits are retained.
Use merge commits for the `dev` to `main` promotion to retain shared ancestry.

The task-head lease cannot prevent an administrator from concurrently rewriting both permanent
branches. Ancestry is verified at check time; this workflow is not a substitute for server
branch protection. Requiring the merged result in both `dev` and `main` reduces accidental loss during
a rewrite of just one permanent branch. `protected: true` alone is not treated as proof
that a protection configuration forbids force pushes.
