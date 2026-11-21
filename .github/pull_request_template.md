## What

Describe the resulting behavior in one sentence.

## Why

Explain the concrete problem and relevant issue, if any.

## Changes

- List meaningful changes, including removed or renamed files.
- Record checks actually run, their results, and any limitations.
- Note API/schema/architecture effects and relevant decisions when applicable.

Task branches target `dev`; only this repository's `dev` targets `main`.
Delete the task branch after merging into `dev` and promoting into `main`. Keep `dev` and `main`.

API/schema/architecture effects when applicable, relevant ADRs, and remaining limitations. Confirm the diff excludes unrelated work and credentials.

## Independent adversarial review (code changes)

- Reviewer and independence: <!-- agent/session or person; not the author -->
- Reviewed commit or exact diff: <!-- revision or immutable diff identifier -->
- Findings and disposition: <!-- links or concise evidence; include unresolved items -->
- Outcome: <!-- passed / changes requested / pending; re-review after relevant changes -->

## Security review (code changes)

- Security skill and independent reviewer/session: <!-- security-review; identify reviewer -->
- Reviewed PR base and head SHAs: <!-- full base-to-head diff -->
- Findings, fixes, and remaining uncertainty: <!-- include unavailable checks -->
- Outcome: <!-- passed / changes requested / pending / not applicable, with reason -->
