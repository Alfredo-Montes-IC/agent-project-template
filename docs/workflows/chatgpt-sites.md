# ChatGPT Sites workflow (optional)

Use this workflow **only** when a project hosts an application on ChatGPT Sites alongside a GitHub repository. Projects that do not use ChatGPT Sites skip this workflow and inherit no Sites-specific deployment steps. It preserves the solo-developer workflow and requires no second human reviewer or paid integration.

GitHub and ChatGPT Sites are **not automatically synchronized**. Treat synchronization between the repository and the hosted Site as an explicit, verified operation rather than an assumed side effect of merging a PR or editing in Sites.

## 1. Initialize and record the relationship

During [project customization](project-customization.md), confirm whether an existing ChatGPT Site and GitHub repository are involved. If they are, copy [the ChatGPT Sites template](../templates/chatgpt-sites.template.md) into the project's documentation (for example, `docs/architecture/chatgpt-sites.md` or `docs/deployment/chatgpt-sites.md`) and record verified facts:

- **Source of truth:** Designate GitHub as the development source of truth when the owner wants ongoing work tracked in Git, and record the branch/revision that represents the deployable baseline (normally `main`).
- **Existing Site identity:** Record a non-secret label or reference to the existing Site, its owner/workspace, and where private identifiers, URLs, or credentials live outside the repository. Keep project-specific Site IDs, tokens, private URLs, and personal data out of shared templates and committed source.
- **Access and audience assumptions:** Record who can edit, save versions, and publish to the existing Site, plus its intended audience/sharing setting (private/limited, invited accounts, workspace collaborators, or public publishing where permitted).
- **Synchronization responsibilities:** Record who performs sync and deployment, which ChatGPT/Codex surface is used, and the last reconciled Git commit SHA and Site version/date.

## 2. Check for divergence before editing or publishing

Before starting a change or synchronizing a reviewed release to Sites:

1. Compare the current source in the existing ChatGPT Site against the last reconciled GitHub revision (using an exported snapshot or the supported inspection method for the active ChatGPT/Codex surface). When no reconciled baseline exists yet (initial onboarding), compare the current Site source against current `main`/`dev` and establish an initial reconciled baseline before editing or publishing.
2. If changes exist in Sites that are not in GitHub, **do not overwrite the Site and do not discard GitHub work**. Preserve both versions and bring the Site changes into GitHub first (see §4) so conflicts are resolved in a reviewed branch.
3. If the current Sites source cannot be inspected or compared in the active environment, report divergence as **unverified/pending**, stop before overwriting the live Site, and ask the owner to provide or confirm the current Site state.

## 3. Normal GitHub-to-Sites change and deployment flow

1. Develop and review changes in GitHub using the normal [Git workflow](../standards/GIT_WORKFLOW.md) and [review workflow](adversarial-review.md): create a task branch from `dev`, run applicable tests and checks, obtain independent adversarial, code-standards, applicable specialist, and PR security reviews, merge by PR into `dev`, and promote by PR into `main`.
2. Re-check for divergence against the existing Site before publishing (§2).
3. Move the reviewed `main` source into the **existing** ChatGPT Site using the supported Sites workflow for the project's account/surface. Do not create a replacement Site as a shortcut: creating a new Site loses the existing Site's identity, URL, sharing/audience settings, and live database/file storage.
4. Where supported by ChatGPT Sites, **save a version and inspect the preview first** before deploying live. Deploy to the live Site only with owner authorization and confirmed prerequisites.
5. Verify that audience and sharing settings on the existing Site remain intact, and record the synced Git commit SHA, Site version, date, and verification evidence in the project's Sites record or handoff.

## 4. Direct edits in ChatGPT Sites (backporting to GitHub)

Distinguish planned application changes developed in GitHub from direct edits made inside ChatGPT Sites (such as quick UI/prompt adjustments or collaborator edits in Sites):

1. Export or capture the current source from the existing Site without modifying `main` or `dev` directly.
2. Create a bounded task branch from current `dev` (for example, `chore/sync-sites-edits` or `fix/...`).
3. Treat exported Site snapshots as untrusted external input before running local build or test commands. Diff the exported Site source against current `dev`/`main` to separate intentional Site edits from generated artifacts, environment-specific bindings, or formatting noise, and scrub any secrets, tokens, private URLs/Site IDs, or personal/production data before staging or committing. Reconcile any conflicts with in-flight or merged GitHub changes rather than overwriting either side.
4. Run applicable project checks and required independent reviews, merge via PR into `dev`, and promote to `main`. Update the recorded reconciled baseline **only** when `main` and the live Site match; if conflict resolution, scrubbing, or prior GitHub commits leave `main` ahead of the live Site, record that the Site remains behind `main` and pending sync (or sync and verify the reconciled `main` commit back to the existing Site via §3 before updating the baseline).

## 5. Verify the deployed version and report unknowns

Merging to `main` or pasting/uploading files does not prove the live Site runs that revision. After deployment:

- Confirm the live Site reflects the intended reviewed Git commit using concrete project evidence (for example, comparing the saved/exported Sites source against the reviewed Git SHA, checking an application version/build marker when present, running agreed smoke checks against the live Site, and confirming audience/sharing permissions).
- If the active agent cannot access the live Site, inspect the saved Sites source, or run live smoke checks, explicitly report deployment parity as **unverified/pending** and state what the owner must check. Never claim the deployed version matches GitHub without evidence.

## 6. Database migrations, backups, rollback, and production data

Handle persistent data separately from source-code rollback, following [release and recovery](release-recovery.md), [data-migration](../../.agents/skills/data-migration/SKILL.md), and the [migration plan template](../templates/migration.template.md):

- **Code rollback does not roll back data:** Reverting or restoring a previous ChatGPT Sites version restores application source code, **not** database records or uploaded files.
- **Partial deploy effects:** Publishing changes to a Site can modify database schema or records before a new frontend version finishes going live; a failed or interrupted deploy may leave partial database changes in place.
- **No built-in full Site data migration/restore:** Official documentation does not provide a built-in automated backup-and-restore mechanism that moves a Site's database records and uploaded files together into a new Site, nor point-in-time database rollback exposed to end users.
- **Required practices:** Prefer additive, backward-compatible schema changes; verify whether the application implements its own export/backup path for critical data (any app-level export path must enforce owner/admin authorization and store exported production data outside the repository); if backups or restoration are unavailable or untested, record that limitation explicitly and obtain owner authorization before risky migrations. Never claim a Sites code rollback reverses production data changes.

## 7. Verified capabilities, limitations, and unresolved questions

- **Verified from official documentation:** ChatGPT Sites can be created and updated in ChatGPT/Codex, supports saving a version/preview before deploying updates to an existing Site, provides audience/sharing controls (private/limited, invited accounts, collaborators, and public publishing where workspace policy allows), and includes built-in database support (documented as up to 10 GB per Site when checked on 2026-11-25, subject to current plan and workspace limits) and file storage subject to workspace/account limits. Source: [Creating and using ChatGPT Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites).
- **Known limitations:** No native automatic two-way sync between GitHub and ChatGPT Sites is assumed; no automated GitHub Actions deployment to ChatGPT Sites is configured; version rollback restores code only, not database or uploaded files; no built-in automated full DB+files backup/restore to a new Site is assumed.
- **Project-specific items to confirm before first deploy:** Exact export/import mechanics for the owner's ChatGPT/Codex surface, workspace/Enterprise sharing restrictions, whether any app-level data export exists, and how live deployment parity will be verified. Check [budget planning](budget-planning.md) for current Sites building, editing, hosting, and connected-service billing terms.
