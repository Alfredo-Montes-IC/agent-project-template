---
name: debugging
description: Diagnose a bug, failed test, error, or unexpected behavior using reproducible evidence.
---

# Debugging

1. State the expected and observed behavior. Reproduce safely with the smallest useful input; record environment, exact command, and error without exposing secrets or private data. If reproduction is unavailable, state what is missing.
2. Trace the relevant path and existing controls. Form testable hypotheses, rule out alternatives, and distinguish facts from assumptions. Avoid unrelated refactors and changes that hide the symptom.
3. Implement the smallest effective fix and add or update a meaningful regression check when behavior warrants it. Verify the original failure and nearby behavior; report checks not run.
4. For production data or systems, use read-only diagnosis first and follow the user's authorization and project recovery procedures. Avoid destructive fixes and never invent evidence.
