---
name: code-standards-review
description: Independently review changed code against applicable engineering standards, including the clarity and usefulness of code comments.
---

# Code standards review

Read [engineering guidelines](../../../docs/standards/GUIDELINES.md), scoped instructions, and established conventions in nearby code. Review the exact staged diff or PR revision, including the affected callers and tests. Use the [review workflow](../../../docs/workflows/adversarial-review.md) to track the outcome.

Check practices that matter to the change, such as clear names and responsibilities, type safety and validation at boundaries, deliberate failure handling, compatibility, and tests for observable behavior. Defer formatting to the project's configured tools. Explain the concrete impact and cite the relevant rule when one applies. Mark preferences as optional and flag conflicting or unverified guidance for the owner to resolve.

Check that added or changed comments are accurate and useful. Keep explanations of intent, invariants, tradeoffs, edge cases, or public behavior. Flag comments that repeat the code, narrate the editing process, make unsupported claims, or use promotional language. Judge the text by what it communicates.

Report findings in plain, neutral language with file and line, evidence, impact, and a concrete correction. Separate changes needed from optional suggestions. State the reviewed revision, checks not run, and whether any findings remain. Do not edit files.
