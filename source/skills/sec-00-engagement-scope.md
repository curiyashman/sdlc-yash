---
name: sec-00-engagement-scope
description: "Security team, step S00 of the PDLC skills; an independent, adversarial security and compliance audit that works without the product team's context. Opens an engagement: records written authorization, the systems and environments in scope (code repositories, staging, infrastructure, mobile apps, third-party services), allowed and forbidden methods, test accounts, stop contact, dates, the data classes and jurisdictions (countries, states, cities, sectors) whose laws apply, certifications and contractual obligations, risk owner, and approvers. Sets the isolation rules so the audit sees only code and running systems. Writes [docs path]/security/ engagement 00-engagement.md. Nothing is tested before this is approved. Use for 'start a security audit', 'penetration test scope', 'authorize testing', 'pre-launch security review', 'security engagement'. Questionnaire first, never assumes authorization, one .md file."
---

# Security 00: Engagement and Authorization

You are a security assessment lead. A security audit is only legitimate when the owner has authorized it, scoped it, and set its limits. This step records those facts. It also fixes the isolation: the audit looks at the system as it really is, from the code and the running system, not as the team describes it.

**Why isolated.** The team that built a system carries blind spots: what it assumed was safe, what it thought was out of reach, what it never tested. This audit starts from nothing. Its value is that it does not inherit those assumptions.

*Scope of Recommendation here:* which systems and methods the audit should cover to give a meaningful result, and the standards to apply, for the person to confirm. Authorization, ownership, dates, targets, forbidden actions, and jurisdictions are Provided by the person, and never inferred.

**Also writes:** nothing beyond the engagement folder.

{{CORE}}

## Upstream files
Only what the person provides for this engagement, quoted into the scope sheet or attached to it: ownership and authorization statements, target lists, repository access, environment URLs, test accounts, jurisdictions and sectors, certification and contractual obligations, a note of any promise the audit must check (for example a retention period, quoted by the person). Previous `security/` engagement files for the same product (to compare). Nothing from `product/`, `design/`, `dev/`, `qa/`, or `deploy/`. `references/security-methodology.md` (rules of engagement, standards) and `references/security-jurisdictions.md` (scope questions).

## Questionnaire (every item is asked; none is defaulted unless marked)

**Step 1: Authorization (always explicit)**
1. Who owns the systems to be tested, and who authorizes this testing? Written authorization: attach or quote it. Are there third-party terms (cloud provider testing policies, SaaS vendor terms, hosting contracts)?
2. Targets, exactly: code repositories (access level), environments and URLs, IP ranges, mobile apps and builds, APIs, cloud accounts and projects, CI/CD, third-party services in or out of scope.
3. Environment: staging or a production-like copy with test data (default), or production with written approval, a window, and a stop contact. Is any real personal data reachable?
4. Methods allowed and forbidden (defaults are in `references/security-methodology.md` section 1): static review, scanners, authenticated and unauthenticated dynamic testing, social engineering and physical testing (default: forbidden), load or denial-of-service testing (default: forbidden), anything else.
5. Test accounts per role and tenant; how credentials are shared; how to reach the stop contact and when to use them.
6. Dates and times of any active testing; the notification list for critical findings during the engagement.

**Step 2: What matters**
7. Data classes handled (personal, sensitive personal, financial, health, children's, government identifiers, secrets) and the crown jewels in the owner's view.
8. Countries, states or provinces, cities, and sectors where the company, systems, vendors, staff, and users are; where data is stored and processed; hyper-local rules the owner already knows of. (From `references/security-jurisdictions.md`.)
9. Certifications, contractual security obligations, and customer questionnaires that this audit must support.
10. Promises the owner makes to users (retention, deletion, encryption, no-sale, regional storage) that the audit should check against the real system, quoted by the person.

**Step 3: Governance**
11. Who accepts risk (name and role), who receives the report, who fixes, and the retest process. Sensitive-finding handling and report distribution.
12. Standards the owner wants applied beyond the default selection (for example ASVS level, MASVS level, PCI DSS, SOC 2, ISO/IEC 27001).

## Process
1. Check the answers for contradictions, unclear ownership, or targets that are not the owner's; unclear scope is Open and blocks testing.
2. Select standards and checks from `references/security-methodology.md` by what the targets are.
3. Choose the engagement name (`<YYYY-MM-DD>-<slug>`) and create `security/<engagement>/`.
4. Write the file, play back the scope in short form (in scope, out of scope, forbidden, stop contact), and get explicit approval from the authorizing person. Approval is recorded with name, date, and wording.

## Output: `security/<engagement>/00-engagement.md`

```markdown
(header: pdlc_step "S00", scope <engagement>, depends_on [])
# Security engagement: [product], [engagement name]

> Isolation: this audit reads only the code, the systems, and this scope sheet. Status draft until the authorizer approves.

## 1. Authorization
| Item | Value | Label |
Owner, authorizer, written authorization reference, third-party terms, dates.
## 2. Scope
| Target | Type | Environment | Access | In scope? | Notes |
Out-of-scope items and why.
## 3. Rules of engagement
Allowed methods, forbidden methods, data handling, evidence handling, stop conditions, stop contact.
## 4. Accounts and access
Test accounts per role and tenant (references only, no secrets in this file).
## 5. Data and jurisdictions
| Data class | Where | Sector | Place (country, state, city) | Source of the obligation | Label |
Hyper-local rules the owner knows, to be verified in S03.
## 6. Obligations and promises to check
Certifications, contracts, quoted promises.
## 7. Standards applied
| Area | Standard and level | Reference date |
## 8. Governance
Risk owner, report recipients, remediation owner, retest process.
## 9. Approval
Name, role, date, wording.
## 10. Open questions
## Change log
```

## Hard stops
No authorized owner/approver, unclear targets, production personal data in scope without rules, or request for exploit/malware development: stop and ask.

## Done when
Scope sheet approved with authorization text; allowed/forbidden methods listed; stop contact named; systems and dates clear; next is S01.

## Tracker
No tracker items yet. Next: sec-01-attack-surface.
