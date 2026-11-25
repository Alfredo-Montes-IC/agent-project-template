## What

Describe the resulting behavior in one sentence.

## Why

Explain the concrete problem and link the governing issue (`Refs #<n>` on `task -> dev`; `Closes #<n>` or `Fixes #<n>` on `dev -> main` when solved).

## Changes

- List meaningful changes, including removed or renamed files.
- Record checks actually run, their results, and any limitations.
- Note API/schema/architecture effects and relevant decisions when applicable.

Task branches target `dev`; only this repository's `dev` targets `main`.
Delete the task branch and verify any solved linked issue closed after merging into `dev` and promoting into `main`. Keep `dev` and `main`.

API/schema/architecture effects when applicable, relevant ADRs, and remaining limitations. Confirm the diff excludes unrelated work and credentials.

## Independent adversarial review (code changes)

- Reviewer and independence: <!-- agent/session or person; not the author -->
- Reviewed commit or exact diff: <!-- revision or immutable diff identifier -->
- Findings and disposition: <!-- links or concise evidence; include unresolved items -->
- Outcome: <!-- passed / changes requested / pending; re-review after relevant changes -->

## Code standards review (code changes)

- Independent reviewer/session: <!-- code-standards-reviewer or independent fallback -->
- Reviewed revision: <!-- staged tree or PR revision covering this change -->
- Findings and disposition: <!-- applicable guideline, code or comment impact, and any unresolved issues -->
- Outcome: <!-- passed / changes requested / pending -->

## Security review (code changes)

- Security skill and independent reviewer/session: <!-- security-review; identify reviewer -->
- Reviewed PR base and head SHAs: <!-- full base-to-head diff -->
- Findings, fixes, and remaining uncertainty: <!-- include unavailable checks -->
- Outcome: <!-- passed / changes requested / pending / not applicable, with reason -->
