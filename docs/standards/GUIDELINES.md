# Engineering conventions

Keep these guidelines limited to practices with a clear benefit for correctness, security, reliability, accessibility, or maintainability. Document project-specific standards when the stack and requirements justify them. Keep personal preferences optional and use the project's formatter and linter for mechanical style.

- Prefer simple code and existing patterns. Avoid speculative abstractions and unrelated refactors.
- Use the project's chosen type system and runtime validation at external boundaries.
- Keep components cohesive and dependencies explicit; name source directories for their actual responsibilities.
- Handle failures deliberately and avoid silent exceptions. Mock external services in routine automated checks.
- Select tests for observable behavior and meaningful failure cases. Match coverage to change risk.
- Use clear names and types to express behavior. Write concise, neutral comments for intent, constraints, tradeoffs, or edge cases that the code cannot show. Keep comments accurate as behavior changes and remove comments that merely repeat the code or narrate the edit.
