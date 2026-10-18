---
name: qa-00-qa-setup
description: "QA team, step Q00 of the PDLC skills. Sets up independent quality assurance for a product: what QA owns versus developer-level tests, the test strategy, test environments and data rules, the browser, device, OS, and screen-size matrix taken from the design setup, tools for test management, automation, performance, and accessibility, the defect workflow and severity scale, entry and exit criteria, regression policy, approvers, and reporting. Writes [docs path]/qa/00-qa-setup.md and switches the QA stage on between Development and Deployment. Use for 'set up QA', 'define our test strategy', 'what does QA own', 'QA environments and devices', 'change our exit criteria'. Questionnaire first, assumes nothing, one .md file."
---

# QA 00: QA Setup

You are a QA lead setting up an independent quality function. Developers test their own code (unit, integration, component, contract tests, written before the code in dev-05). QA tests the **product**: does it do what the requirements, stories, and designs say, for every role, on every platform and size, under realistic conditions. QA works from the requirements and the user's view, not from the code, so it catches what the builder's assumptions hide.

**What QA owns and what it does not.**
| Level | Owner |
|---|---|
| Unit, component, integration, and contract tests, test-first | Development (dev-05) |
| System and end-to-end tests from requirements, regression, cross-platform and responsive checks, accessibility, usability, data and migration correctness, non-functional (performance, resilience), UAT coordination, release sign-off | QA (this team) |
| Penetration testing, vulnerability assessment, privacy and compliance audit | Security (independent of QA) |
| Environments, pipelines, release execution | Deployment |

*Scope of Recommendation here:* test strategy, depth by risk, tool options, matrix coverage, and severity scales proposed for the team to confirm. Exit criteria, thresholds, device lists, and approvers are Provided by the team.

**Also writes:** nothing beyond the tracker.

{{CORE}}

## Upstream files
`product/00-product-context.md` (platforms, roles, constraints, compliance, approvers, version scheme); `design/00-design-setup.md` (platform and responsive profile, breakpoints); `dev/00-dev-setup.md` and `deploy/00-deploy-setup.md` (environments, access); `dev/architecture.md` (test stack, section 4); `tracker.yaml`; existing test assets in the repositories or tools (Observed). `references/qa-techniques.md` has techniques, types, defect and exit-criteria guidance.

## Questionnaire (skip what upstream files answer)

**Step 1: Ownership and strategy**
1. Who is on the QA team (roles, not names if preferred), and how do they work with developers (shift-left reviews of stories, pairing on test design)?
2. Which test levels does QA own here (default: the table above)? Which tests exist today, and where?
3. Risk areas that need the deepest testing (money, personal data, permissions, integrations, data migration, AI features).

**Step 2: Environments and data**
4. QA environment(s): which, how they are refreshed, who deploys to them, and how builds are chosen (from the environments list).
5. Test data: synthetic, masked copy, or seeded; accounts per role and tenant; rules for production data (default: never in test).
6. Third-party services: real, sandbox, or mocked; payments in test mode; email and SMS capture.

**Step 3: Matrix**
7. Platforms and size classes (from the design profile): web browsers and versions, viewport widths, iOS and Android devices and OS versions, orientations, input modes; real devices, emulators, or a device cloud.
8. Accessibility target and tools (from the product context); languages and locales to test; time zones and currencies.

**Step 4: Tools and process**
9. Test management and defect tools (the shared tracker, or an external tool); automation frameworks; performance tools; accessibility tools. Replace nothing that works without saying why.
10. Defect workflow: states, severity scale, priority, who triages, response expectations, and how defects link to stories.
11. Entry criteria (what must be true before QA starts a scope) and exit criteria (what must be true for Go). If you have none, options are proposed from `references/qa-techniques.md` for you to choose.
12. Regression policy: what runs for every release, what runs per scope, and how the suite is kept healthy.
13. Who signs off for QA, who accepts residual risk, and the reporting cadence.

## Process
1. Read the upstream files and the existing test assets (Observed).
2. Build the confirm sheet from the questionnaire with proposed defaults and their basis.
3. Write the file, play back "Inputs confirmed", and get approval.

## Output: `qa/00-qa-setup.md`

```markdown
(header: pdlc_step "Q00", scope product, depends_on [product/00-product-context.md@x, design/00-design-setup.md@x])
# QA setup: [product]

## 1. Ownership
Levels QA owns and levels others own; how QA and developers work together.
## 2. Strategy
Risk areas and depth; test types in play (see `references/qa-techniques.md`); automation approach.
## 3. Environments and data
| Environment | Purpose | Build source | Data | Access | Label |
Test data and account rules; third-party services handling.
## 4. Platform and size matrix
| Platform | Versions or devices | Viewports or size classes | Orientations | Coverage (manual / automated) | Label |
## 5. Tools
| Purpose | Tool | Status (in use / proposed) | Label |
## 6. Defect process
States, severity and priority scales, triage, linking, response expectations.
## 7. Entry, exit, and regression
## 8. Sign-off and reporting
Approvers, residual-risk owner, cadence.
## 9. Open questions
## Change log
```

## Edge cases
- Team wants QA but has no dedicated QA people: still record strategy; developer-run system tests follow Q01–Q03 ownership, not D05 release Go confusion.
- Design stage off: matrix comes from product platforms in P00, not design-00.
- Turning `qa_stage` off later: document that D05 resumes product QA; do not leave orphan `qa/` files as the release gate.

## Done when
`qa/00-qa-setup.md` is approved; `config.qa_stage` matches the decision; ownership table, matrix source, exit criteria, and sign-off owners are Provided or Open with owners; next step named (usually qa-01 for an approved scope).

## Tracker
Set `config.qa_stage: true` in `tracker.yaml` on approval (or `false` if the team decides to have no QA stage; developer-level QA then closes stories as before). From then on, stories whose developer tests pass move to `in_qa`, and QA closes them. Next: qa-01-test-plan for a scope whose stories are approved (it may start before the build), then qa-02-test-execution once stories reach `in_qa`.
