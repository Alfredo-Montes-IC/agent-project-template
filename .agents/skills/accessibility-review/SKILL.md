---
name: accessibility-review
description: Review user interfaces for accessibility when designing, implementing, or testing interactive experiences.
---

# Accessibility review

Use for user-facing interface changes. Inspect the affected flow, actual platform, applicable requirements, and existing design system. Choose checks appropriate to the interface; do not assume a web stack or claim a formal conformance level without a complete evaluation.

For web interfaces, consider the relevant [WCAG guidance](https://www.w3.org/WAI/WCAG22/Understanding/conformance): keyboard access, visible focus and focus order, semantic structure and accessible names, text alternatives, contrast, zoom and responsive layout, error feedback, and motion or timing where relevant. For non-web interfaces, use the platform's accessibility guidance and accessibility APIs.

Combine appropriate automated checks with manual keyboard and assistive-technology testing when available. Report the environment, interaction or page, reproducible barrier, user impact, evidence, and suggested fix. State what was not tested and avoid claiming automated tools alone establish accessibility. Accessibility review supplements the project's verification and independent adversarial review; it does not replace either.
