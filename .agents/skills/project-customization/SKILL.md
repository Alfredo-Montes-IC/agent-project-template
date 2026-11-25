---
name: project-customization
description: Initialize or update project-specific guidelines, context, verification, and agent instruction placement using confirmed project facts.
---

# Project customization

Follow [the project customization workflow](../../../docs/workflows/project-customization.md). Inspect existing files, user requirements and code first; preserve existing instructions and decisions. Adapt the canonical `docs/standards/GUIDELINES.md` and other relevant documents instead of copying project-specific reference templates indiscriminately. When an existing ChatGPT Site is used alongside the GitHub repository, identify and document their relationship, source of truth, access assumptions, and sync process via `docs/workflows/chatgpt-sites.md` without committing credentials or private IDs; skip Sites guidance when not used. Mark unverified choices pending, update context routing and client adapters without overwriting user settings, and verify discovery in the clients actually used. Report changes, evidence and unknowns.
