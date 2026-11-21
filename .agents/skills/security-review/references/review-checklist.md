# Review checklist

Use only categories relevant to the actual component. Build a data-flow or permission argument for each reported issue.

| Boundary | Investigate |
|---|---|
| Authentication | Session lifecycle, token verification and expiry, password reset, CSRF where cookie authentication is used |
| Authorization | Object ownership, tenant separation, server-side role checks, default-deny behavior, privileged actions |
| Input and execution | SQL/command/template injection, unsafe deserialization, untrusted filenames, path traversal, archive extraction |
| Outbound requests | SSRF, redirects and DNS behavior, destination and protocol restrictions, metadata-service access |
| Browser output | Contextual escaping, XSS sinks, unsafe HTML, CSP assumptions, exposure through client bundles |
| Files | Content/type validation, upload limits, storage permissions, executable content, download authorization |
| Secrets and privacy | Credential exposure, sensitive logs, data minimization, authorization of exports and backups |
| Business logic | Replay/idempotency, race conditions, inventory/payment invariants, abuse limits, atomicity |
| Dependencies and delivery | Known vulnerable reachable components, lockfile integrity, workflow permissions, untrusted PR execution |
| Errors and operations | Information disclosure, safe failure, resource exhaustion, observability without sensitive payloads |

Choose severity from realistic impact, attacker prerequisites, and exposure. Do not invent a CVSS score or CVE. For current vulnerability identifiers or framework guidance, verify against authoritative advisories and official documentation.

Reference frameworks: [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), [CWE](https://cwe.mitre.org/), and the actual framework's security documentation. They guide review; they are not a claim of compliance.
