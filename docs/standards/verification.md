# Verification commands

## Available now

Requires Git and Python 3.10+. From the repository root:

| Command | Purpose |
|---|---|
| `python3 scripts/bootstrap.py` | Install local hooks and synchronize managed skill copies |
| `python3 scripts/verify.py` | Run the complete portable repository verification suite |
| `python3 scripts/project_checks.py --staged` | Check exact staged context, skill copies and basic credential hygiene |
| `python3 scripts/sync_skills.py --check` | Detect skill mirror drift without writing |
| `python3 -m unittest discover -s tests -v` | Exercise branch routing, hooks, secret redaction and skill parity |
| `git diff --check` | Whitespace errors in edits |
| `python3 scripts/apply_rulesets.py --repo OWNER/REPOSITORY --check` | Verify effective GitHub protections with administration-capable gh authentication |

Windows alternatives: `py -3` or `python`. The existing `scripts/check-context.ps1` delegates to the same portable checker. CI runs Ubuntu checks plus a Windows compatibility job. The scanner checks a bounded set of credential patterns, not arbitrary secrets. Local Markdown links are checked; heading anchors and reference-style links are not.

CI also tests Python 3.10 and runs the pinned Gitleaks scanner on full fetched history and current files on pushes, PRs and a weekly schedule. The local regex scan is a fast preliminary check; neither scanner proves absence of secrets. See [dependency/scanner maintenance](../workflows/dependency-maintenance.md). Configure real application CI through [project CI](../workflows/project-ci.md) and verify new required check names exist before activating the updated rulesets.

## Add during project initialization

For each actual component, record setup, lint/format, type-check, unit/integration test, build, and local-run commands with working directory and prerequisites. Configure CI to run those checks. There is no application stack or application test suite in this template; do not invent npm/Python application commands or report application security certification.

## Report evidence

Record command, working directory, result and limitations in each handoff. Report unavailable checks and pending server protections. Rerun checks after integration when parallel changes can affect each other.
