# ADR-XXXX: [Short Title of Solved Architectural Problem]

* **Status:** [Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-YYYY]
* **Date:** YYYY-MM-DD
* **Authors / Deciders:** [Names of engineering decision makers]
* **Technical Story / Context:** [Link to a project issue or relevant finding]
* **Applicable requirements:** [Project requirements, or pending]

---

## 1. Context and Problem Statement

[Describe the context and problem to solve. What is the business and technical motivation? What are the constraints (e.g., Google Apps Script execution limits, single-threaded V8, spreadsheet concurrency)?]

---

## 2. Decision Drivers

* [Driver 1, e.g., Fail-closed security architecture per SEC-01]
* [Driver 2, e.g., Elimination of client parameter tampering per SEC-02]
* [Driver 3, e.g., Maintenance of sub-second response times on Web App UI]
* [Driver 4, e.g., Zero breaking changes to existing historical spreadsheet rows]

---

## 3. Considered Options

* **Option 1:** [Title of Option 1]
* **Option 2:** [Title of Option 2]
* **Option 3:** [Title of Option 3]

---

## 4. Decision Outcome

**Chosen Option:** **Option X**, because [brief rationale combining technical fitness, security compliance, and organizational standard].

### Positive Consequences
* [Advantage 1, e.g., Strict compile-time type safety via TypeScript]
* [Advantage 2, e.g., Completely eliminates client-side tampering risk]
* [Advantage 3, e.g., Decoupled multi-environment releases between Dev and Prod]

### Negative Consequences / Trade-offs
* [Trade-off 1, e.g., Slightly higher build complexity requiring Clasp and Jest]
* [Trade-off 2, e.g., Developers must run local type-check before pushing]

---

## 5. Pros and Cons of the Options

### Option 1: [Title of Option 1]
* ✅ Good, because [argument a]
* ✅ Good, because [argument b]
* ❌ Bad, because [argument c]

### Option 2: [Title of Option 2]
* ✅ Good, because [argument a]
* ❌ Bad, because [argument b]
* ❌ Bad, because [argument c]

---

## 6. Implementation Notes & Security Verification

* **Affected Components:** [List services, sheets, or frontend templates modified]
* **Audit Finding Remediation:** [Direct mapping to SEC-XX finding if applicable]
* **Verification / Tests:** [How this architectural decision is proven via Jest tests]
