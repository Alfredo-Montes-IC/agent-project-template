# Configure project CI and delivery

The template runs repository verification on Ubuntu, Windows and the declared minimum Python version, plus full-history/current-file secret scanning. These checks test the template scripts and context, not an application. The supplied rulesets require all these checks and trusted branch routing when activated; they retain zero required human approvals for a solo owner working with independent agent reviews.

## What is configured now

The workflow files describe intended GitHub Actions jobs; their presence does not show that Actions is enabled, that jobs have passed, or that rulesets are active in a particular repository. Inspect the actual runs and effective rules before reporting their status.

| Job or automation | Trigger and scope | Evidence and limits |
|---|---|---|
| `repository-checks`, `windows-checks`, `python-minimum-checks` | Pushes and selected PR events | Run the portable verification suite on Ubuntu, Windows, and Python 3.10. The Ubuntu job also checks committed whitespace. These are template checks, not application tests. |
| `secret-scan` | Pushes, PRs, weekly schedule, or manual dispatch | Pinned Gitleaks release with a verified archive checksum scans fetched Git history and current files; findings and scanner failures require investigation. A pass is not proof that no secrets exist. |
| `branch-policy` | Selected PR events through the trusted base workflow | Checks PR routing from metadata without checking out PR code. Its workflow must exist on the relevant base branch; a status alone is not an independent review. |
| `cleanup` | Merged PR close events, a change to its workflow on `main`, or manual dispatch | Attempts deletion only for eligible unchanged task branches after the result is in both `dev` and `main`; it is not an application test or a required review. |
| Dependabot | Weekly | Proposes GitHub Actions updates against `dev`; ordinary checks and reviews still apply. Scanner and application dependencies need their own maintenance. |

The rulesets name the first three verification jobs, `secret-scan`, and `branch-policy` as required checks when effective. Confirm exact job names and successful runs after changing workflows or before requiring a new check. See [Git workflow](../standards/GIT_WORKFLOW.md) for bootstrap and enforcement limits.

## What each project must decide

Application lint, types, tests, builds and smoke checks; dependency and code scanning appropriate to the chosen stack; deployment, observability, rollback and recovery are pending until a real project supplies those requirements. CI cannot verify agent instruction discovery, independently authenticate a reviewer, prove a restore works, or establish accessibility or security compliance by itself. Record manual checks, reviewer evidence and limitations separately. Do not add a deployment job or require a check that has not been created and verified.

During project customization, identify the actual application languages, runtimes, package managers and boundaries. Record each real setup, formatter/linter, type check, unit/integration test, build and smoke command in `docs/standards/verification.md`. Run them locally, then create CI jobs using the same commands and supported runtimes. Add dependency, IaC and code scanning appropriate to the actual stack and repository eligibility. Do not add guessed npm/Python application commands, run checks vacuously, or report success when application CI is still pending. Give stable required jobs no path filter that can silently skip the gate. Keep test data sanitized and isolate external services.

Use read-only token permissions for PR verification, pinned actions, timeouts and bounded concurrency. Do not run untrusted PR code with secrets or under a privileged `pull_request_target` job. CodeQL/dependency-review and native secret push protection may have private-repository plan restrictions; use eligible tools rather than buying a plan or claiming unsupported features are active.

Add deployment only after a real target exists. Define environment, release revision, smoke checks, health criteria, rollback triggers and data compatibility using the [release/recovery workflow](release-recovery.md). Prefer scoped short-lived OIDC credentials where supported; configure the cloud-side trust policy for the exact repository, branch and environment. Keep production secrets out of PR jobs. An environment rule requiring a different human approver can lock out a solo owner: use appropriate available controls and existing spending/deployment authorization. The template does not deploy anything merely because it is copied.

Sources: [GitHub OIDC](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers), [CodeQL private-repository eligibility](https://docs.github.com/en/code-security/reference/code-scanning/troubleshoot-analysis-errors/private-repository-enablement).
