# Multi-agent workflow

This process coordinates developers and coding agents. It does not prescribe a multi-agent architecture for the application.

## Assign

The coordinator defines one atomic task per writer, with objective, allowed paths, required context, dependencies, acceptance criteria, and verification commands. Delegate only when authorized by the active environment or user.

Give shared contracts, manifests, lockfiles, and CI a sole writer. Agree contracts before parallel implementation of dependent components. Reviewers may inspect in parallel without editing writer-owned files.

## Isolate

Use a separate branch and worktree for each writer. Example from an initialized repository:

```powershell
git worktree add ../project-task-101 -b feat/101-first-component dev
git worktree add ../project-task-102 -b feat/102-second-component dev
```

Check that paths and branches are available. Outside-workspace writes may require permission. Keep environment files and dependency installs local to each worktree. Never switch branches beneath another agent. If isolation is unavailable, serialize implementation.

## Integrate

1. Each writer supplies the [handoff](../templates/handoff.template.md), exact check results, changed paths, and unresolved decisions.
2. Review acceptance criteria, contract compatibility, security, and test evidence.
3. Integrate dependency-first through reviewed PRs; resolve conflicts and verify the combined result.
4. Update task status and accepted ADRs. Resume from task/handoff records and recheck current Git state.

Keep status task-scoped to avoid a global progress file that all writers edit. Do not commit transcripts or private information as shared memory.
