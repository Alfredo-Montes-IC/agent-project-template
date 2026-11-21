# Engineering conventions

- Prefer simple code and existing patterns. Avoid speculative abstractions and unrelated refactors.
- Use the project's chosen type system and runtime validation at external boundaries.
- Keep components cohesive and dependencies explicit; name source directories for their actual responsibilities.
- Handle failures deliberately and avoid silent exceptions. Mock external services in routine automated checks.
- Select tests for observable behavior and meaningful failure cases. Match coverage to change risk.
- Record stack-specific naming, formatting, typing, accessibility, and security conventions here during customization.
- Use lowercase kebab-case for new documentation directories and filenames. Keep ecosystem-mandated names such as `AGENTS.md` and `README.md`.
