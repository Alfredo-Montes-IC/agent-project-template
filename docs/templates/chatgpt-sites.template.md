# ChatGPT Sites deployment and sync record (optional)

Status: draft template. Copy and adapt this file **only** for projects that use ChatGPT Sites alongside GitHub; delete or omit it if the project does not use Sites. Do not commit credentials, tokens, private URLs, raw Site IDs intended to stay private, or personal data.

## 1. Source of truth and repository relationship

- **Development source of truth:** GitHub repository (`dev` for integration, `main` for reviewed release baseline) / other (specify)
- **Hosted target:** Existing ChatGPT Site (non-secret project label; store private Site ID/URL in owner-managed private settings if restricted)
- **Last reconciled baseline:**
  - Git commit SHA (on `main`): `[pending]`
  - ChatGPT Sites saved/deployed version and date: `[pending]`
  - Verified by: `[owner / session, date]`

## 2. Existing Site identity and access assumptions

- **Account / workspace owner:** `[pending]`
- **Who can edit, save versions, and publish in Sites:** `[pending]`
- **Intended audience and sharing mode:** `[private / invited accounts / workspace collaborators / public]`
- **Workspace or policy restrictions (e.g., public publishing disabled):** `[pending / none confirmed]`
- **Supported sync surface (ChatGPT web, desktop, Codex):** `[pending — verify before first sync]`
- **Where private identifiers and secrets are stored:** `[owner-managed private settings / secret store — never in repo]`

## 3. Synchronization and deployment procedure

1. **Divergence check:** How to export or inspect the current Sites source and compare it against the last reconciled Git SHA (or against current `main`/`dev` during initial onboarding before a baseline exists) before editing or publishing: `[pending]`
2. **GitHub review gate:** Standard `task -> dev -> main` PRs with applicable tests and independent reviews recorded in GitHub.
3. **Sync to existing Site:** Exact verified steps to update the **existing** Site (without creating a new Site) from reviewed `main` source: `[pending]`
4. **Preview and publish:** Save a version and review the preview before deploying live; record owner authorization for live publish.

## 4. Direct Site edits backport procedure

- **When direct edits happen in Sites:** Export/capture the Site source, treat it as untrusted external input before running local commands, branch from current `dev`, diff against `dev`/`main`, scrub any secrets, tokens, private URLs/Site IDs, or personal/production data, reconcile conflicts without overwriting either side, run checks and independent reviews, and merge via PR (`task -> dev -> main`). Update §1 as reconciled only once `main` and the live Site match; otherwise note that the Site remains behind `main` and pending sync via §3.

## 5. Deployment verification

- **How to confirm live Site matches reviewed Git SHA:** `[e.g., diff exported/saved Sites source, verify build/version marker, run smoke checks]`
- **Post-deploy smoke checks and audience check:** `[pending]`
- **Unverified / unavailable checks:** Explicitly report deployment parity as pending if the agent cannot inspect the live Site or its deployed source.

## 6. Data, migrations, backups, and rollback boundary

- **Stored data in Sites:** `[built-in database (verify current quota) / uploaded files / external service / none]`
- **Code rollback procedure:** Revert to a previously saved Sites version (restores **code only**, not database records or uploaded files).
- **Migration plan:** Use [the migration template](migration.template.md) for schema or persistent-state changes; prefer backward-compatible changes because publishing can alter database state before frontend deployment completes.
- **Backup / export and restore status:** `[app-level export path with owner/admin authorization and external storage outside Git, plus last tested restore date, or "unavailable / untested — escalate before destructive migrations"]`

## 7. Open questions and limitations

- List any unverified export/import steps, workspace limits, or billing assumptions (see [budget planning](../workflows/budget-planning.md) and [ChatGPT Sites workflow](../workflows/chatgpt-sites.md)).
