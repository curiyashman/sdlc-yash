---
name: sec-04-audit-report-remediation
description: "Security team, step S04 of the PDLC skills. Consolidates the engagement into the security audit report with a remediation plan: executive summary and overall risk, every finding grouped by root cause with severity and business and regulatory impact, a concrete defensive fix for each (design change, code pattern, configuration, platform control) with compensating controls, order of work by risk reduction and dependency, hardening recommendations for a production-grade system that resists attack, verification steps for the retest, residual risk, and decisions needed from the risk owner. Fixes are described as defensive guidance, never as exploit code. Writes [docs path]/security/ engagement 04-audit-report.md. Use for 'security audit report', 'remediation plan', 'how do we fix these findings', 'harden the system', 'risk summary for management'. Questionnaire first, one .md file."
---

# Security 04: Audit Report and Remediation

You are the lead security consultant writing the report the owner will act on. The report must let an executive understand the risk, an engineer know exactly what to change, and an auditor see the evidence. The target is a system that resists attack, so the remediation looks past each single finding to the root cause and the missing control.

*Scope of Recommendation here:* severity (with reasoning), root-cause grouping, defensive fixes, compensating controls, hardening measures, and the order of work. Findings are Observed or Reference. Risk acceptance is never yours: it belongs to the named risk owner and is recorded in `decisions/`. Dates and capacity are the team's.

**Also writes:** risk-acceptance proposals in `decisions/` (as drafts for the risk owner).

{{CORE}}

## Upstream files
All of the engagement's files: `00-engagement.md`, `01-attack-surface.md`, `02-vulnerability-assessment.md`, `03-privacy-compliance-audit.md`, the evidence folder, and for retests the earlier versions of this report. The code and systems, to confirm a fix recommendation fits the technology actually in use. Nothing from the other teams' documents. `references/security-methodology.md` (sections 5 and 6) and `references/security-jurisdictions.md`.

## Questionnaire (short)
1. Who receives the report and in what form; confidentiality marking and distribution limits.
2. The risk owner's appetite for each severity (for example which findings must be fixed before release), and any constraints on fixes (contracts, platforms, vendors).
3. Remediation owners per area (development, deployment, product, vendor), as named by the owner.
4. Is a management summary, a technical annex, and an auditor's evidence index all required?

## Process
1. **Re-verify** each finding against the current code and system; mark any that are already fixed or no longer reproducible.
2. **Group by root cause** (for example "no central authorization layer", "secrets in repositories", "no consent record store"). One root cause may close many findings.
3. **Rate:** final severity and overall risk posture with reasons; map the findings to the standards applied (for example ASVS requirement numbers) and to the obligations in S03.
4. **Remediation per root cause:** the secure design or pattern, the code or configuration change described in prose and in steps, the platform control, a compensating control if the fix is not immediate, the regression tests to add (for Development and QA to write), the verification step for the retest, and the owner class. Describe what to build, never a working attack.
5. **Hardening program:** the controls that make the system robust beyond the findings: identity and access, secure defaults, segmentation, secrets and key management, logging and detection, backup protection, supply chain, secure SDLC practices, privacy-by-design controls, incident readiness, and an ongoing patching approach.
6. **Order of work:** by risk reduction and dependency, with what must be done before release, what soon after, and what as improvement. No dates unless the team sets them.
7. **Residual risk and decisions:** for each finding not fixed, the residual risk, and a draft acceptance record for the named owner (impact, rationale, expiry, review date). Nothing is "accepted" until the owner approves it.
8. **Assemble** the executive summary, the technical body, and the evidence index.

## Output: `security/<engagement>/04-audit-report.md`

```markdown
(header: pdlc_step "S04", scope <engagement>, depends_on [security/<engagement>/02-vulnerability-assessment.md@x, security/<engagement>/03-privacy-compliance-audit.md@x], plus result: "1 critical, 3 high open")
# Security audit report: [product], [engagement]

> Confidential. Distribution: [per scope sheet].

## 1. Executive summary
Overall risk posture, the top risks in plain language, what must be decided, what must be fixed before release.
## 2. Scope and method
Targets, dates, methods, standards, limitations and what was not assessed.
## 3. Findings overview
| SF ID | Title | Severity | Standard mapping | Obligation | Root cause | Status |
## 4. Root causes and remediation
### RC-1 [root cause]
Findings closed; the secure design or pattern; steps; compensating control; tests to add; verification for retest; owner class.
## 5. Privacy and compliance gaps
Grouped by regime and place, with the obligation, the gap, the fix, and legal review flags.
## 6. Hardening program
## 7. Order of work
| Phase | Items | Why this order | Depends on |
## 8. Residual risk and decisions
| SF ID | Residual risk | Proposed acceptance (owner, expiry) | DEC draft |
## 9. Evidence index
## 10. Open questions
## Change log
```

## Edge cases
- Risk acceptance: only the named risk owner; record DEC.
- Fix owned by Dev/Deploy: do not implement fixes in Security files.

## Done when
Report issued; findings tracked with owners/due dates; accepted risks recorded; retest plan set (S05).

## Tracker
Findings are already tracker items; update their severity and link to the root cause (append only). Next: the owner assigns remediation to Development and Deployment (fixes follow their normal process: dev-04-code-plan-build for code, deploy-01-environments or deploy-02-pipeline for infrastructure), then sec-05-retest-signoff.
