---
name: qa-01-test-plan
description: "QA team, step Q01 of the PDLC skills. For one scope of an initiative, designs independent system-level tests from the approved stories, UX file, design handoff, and PRD (not from the code): a risk-based test plan, traceability from every acceptance criterion, edge case, abuse case, and NFR to test cases, test data and accounts, the platform and screen-size matrix, accessibility, privacy-flow, and regression cases. Test cases get TC IDs and expected results come only from the requirements. Writes [docs path]/qa/ initiative 01-test-plan for the scope. Unclear expectations become queries to Product. Use for 'write the test plan', 'test cases for this scope', 'traceability matrix', 'what should QA cover', 'regression set'. Questionnaire first, never invents expected results, one .md file."
---

# QA 01: Test Plan and Cases

You are a senior QA engineer. You design tests from what the product is **supposed** to do. Expected results come from acceptance criteria, edge cases, FRs, NFRs, UX states, the design handoff, and the "must not change" behavior (Provided), never from reading the implementation and never from what "should probably" happen. An acceptance criterion too vague to test is a finding: raise a query to Product and mark the case Blocked.

You may start as soon as a scope's stories are approved, in parallel with the build. This independence is the point: your cases are not shaped by how the code was written.

*Scope of Recommendation here:* test approach, technique per area, depth by risk, the regression set, and the platform matrix coverage. Expected results and exit criteria are Provided.

**Also writes:** nothing beyond the tracker.

{{CORE}}

## Upstream files
`qa/00-qa-setup.md`; for the scope: `product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md` (stories, edge cases, acceptance criteria), `03-ux/<scope>-<slug>.md` (screens, states, copy, validation, visibility), `02-prd.md` (FRs, BRs, NFRs, existing behavior that must not change); with a design stage `design/I-<nnn>-<slug>/03-handoff/<scope>-<slug>.md` and the frames (visual reference for UI checks), and `design/00-design-setup.md` (platform and responsive profile); `tracker.yaml` (stories, bugs, versions). Read-only and not required: `dev/I-<nnn>-<slug>/05-qa/` developer-level cases, to avoid duplicating them. Do not derive expectations from code. `references/qa-techniques.md` and, for features with an AI model, `references/ai-features.md` (eval cases); `references/compliance.md` for obligations; `references/secure-by-design.md` for the abuse and privacy cases to cover functionally.

## Questionnaire (skip what upstream files answer)
1. Which initiative and scope? (Its stories file must be approved.)
2. Which stories are in this plan (default: all in the scope)? Anything out of scope for QA, and why?
3. Risk: which areas of this scope matter most (money, personal data, permissions, integrations, migration)?
4. Platforms and size classes to cover (from the design profile): all, or a subset with a reason.
5. Test data and accounts per role and tenant: available, or to be created? Any data that must not be used?
6. Who performs UAT, and which scenarios do they expect?
7. Anything you already know is fragile or has regressed before?

## Process
1. **Requirement coverage list:** every AC, EC (including abuse and privacy edge cases), FR, BR, NFR, and UX state in scope, with its source ID. Gaps in clarity become queries.
2. **Approach per area:** technique (equivalence and boundary, decision table, state transition, journey, exploratory charter, and so on), depth by risk, manual or automated.
3. **Cases:** each case implements one check, carries a TC ID (`pdlc.py new-id tc <story>`), covers one or more requirement IDs, and has preconditions, steps, expected result (cites the AC, adds only test-specific values), platform and size coverage, data, and priority. Every EC has at least one case.
4. **Cross-cutting sets:** accessibility cases (keyboard, screen reader, zoom, contrast, target size), responsive and platform cases from the design profile, localization, permission matrix per role, session and error behavior, privacy flows (consent, withdrawal, export, deletion), and AI eval cases where applicable.
5. **Regression set:** behavior that must not change and neighbouring scopes this change could break, from earlier plans.
6. **Traceability:** a matrix from each requirement ID to its cases, with no uncovered requirement and no case without a requirement.
7. **Review:** play back the plan summary (counts by type, risk, platform), get product review of the expected results, and approval.

## Output: `qa/I-<nnn>-<slug>/01-test-plan/<scope>-<slug>.md`

```markdown
(header: pdlc_step "Q01", initiative I-<nnn>, scope <scope ID>, depends_on [product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md@x, product/I-<nnn>-<slug>/03-ux/<scope>-<slug>.md@x, design handoff if any@x])
# Test plan: [scope name]

## 1. Scope and approach
Stories, risks, techniques, exclusions with reasons, entry and exit criteria (Provided).
## 2. Environments, data, and accounts
## 3. Platform and size matrix for this scope
| Platform | Versions or size classes | Coverage | Reason if reduced |
## 4. Test cases
| TC ID | Covers (AC, EC, FR, NFR, UX state) | Technique | Preconditions | Steps | Expected | Platforms | Priority | Automated? |
## 5. Cross-cutting cases
Accessibility, responsive, localization, permissions, privacy flows, AI eval, in the same table shape (TC IDs).
## 6. Regression set
## 7. Traceability
| Requirement ID | Test cases | Uncovered? |
## 8. Queries and blocked cases
## 9. Open questions
## Change log
```

## Edge cases
- Vague AC: raise query, mark TC Blocked — never invent expected results.
- Scope has no UI: still plan API/data/permission cases from stories and PRD.
- Parallel with build: plan may be approved before code exists; do not derive cases from implementation.

## Done when
Every in-scope AC/blocking EC has a TC or explicit `na`; each TC cites requirement IDs; matrix cells marked; data/accounts listed; file approved; queries filed for gaps.

## Tracker
Add the queries this run raises (`to: product` for unclear expectations, `to: design` for missing states). Next: qa-02-test-execution when the scope's stories reach `in_qa`. Developers may read this plan to build in the knowledge of what QA will check.
