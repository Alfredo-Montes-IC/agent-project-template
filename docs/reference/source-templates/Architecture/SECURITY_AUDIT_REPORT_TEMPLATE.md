# Application security review report template

**Application and environment:** [name and scope]

**Reviewed revision and date:** [commit or version, date]

**Reviewer:** [name or role]

**Applicable policy and standards:** [verified requirements, or pending]

This template records evidence and findings. It does not establish certification or compliance. Exclude secrets and sensitive personal information.

## 1. Scope and summary

Describe the purpose, systems and data in scope, methods used, assumptions, unavailable evidence and principal risks. List checks run and their outcomes; distinguish confirmed defects from deployment assumptions and policy questions.

## 2. Architecture and trust boundaries

Describe relevant components, entry points, principals, data stores and external integrations. Identify authentication, authorization and other controls with references to actual evidence. Add a diagram where useful.

## 3. Findings

| ID | Finding | Evidence and affected path | Impact and severity | Status |
|---|---|---|---|---|
| [ID] | [Title] | [Location and evidence] | [Impact] | [Open/resolved/pending verification] |

For each finding, record the reproduction or reasoning, affected resource, relevant project requirement if any, proposed remediation, owner and verification evidence. Do not invent exploitability, severity, approvals or standards mappings.

## 4. Remediation and verification

Prioritize findings according to risk and document the proposed fix, its owner, target, checks and outcome. Separate existing issues from changes introduced by the reviewed revision. Re-review material fixes and record unresolved questions.

## 5. Residual risk and handoff

List remaining risk, checks not run, deployment controls requiring verification, decisions and next steps. Any formal sign-off must come from the project's authorized approver and be based on actual evidence.
