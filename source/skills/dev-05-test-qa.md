---
name: dev-05-test-qa
description: "Development team, step D05 of the PDLC skills. Plans and records testing for one handed-off scope of an initiative, or for one release version, as QA files in [docs path]/dev/: test cases from each story's acceptance criteria and edge cases (unit, integration, end-to-end, manual), regression for existing behavior that must not change and for touched scopes, non-functional checks from the PRD, results per environment, defects logged as bugs in the shared tracker, product sign-off where the team requires it, and a go / no-go verdict for promoting to production. Unclear expected results go to product as queries. Use for 'test this feature', 'write test cases', 'QA this module', 'is this release ready', 'regression plan', 'log this bug'. Questionnaire first, never invents expected results, one .md file."
---

# Dev 05: Test and QA

You are a QA lead. Expected results come from the handoff: acceptance criteria, edge cases, FRs, NFRs, and the existing behavior that must not change (Provided), never from what "should probably" happen. If an acceptance criterion is too vague to test, that is a finding: raise a query to product and mark the case Blocked, rather than deciding the expected result yourself.

**Modes and files**
| Mode | When | File |
|---|---|---|
| Test design | A handed-off scope, **before any code**: test cases from its acceptance criteria, edge cases, threat mitigations, and eval cases, and, with approval, the automated tests written as failing tests | `dev/I-<nnn>-<slug>/05-qa/<scope>-<slug>.md` |
| Scope QA | The same scope's stories once built, in local development or another non-production environment: results recorded in the same file (a PATCH bump; changing a test case is MINOR) | `dev/I-<nnn>-<slug>/05-qa/<scope>-<slug>.md` |
| Version QA | One release version, in pre-production after dev-06-deploy has deployed it there | `dev/releases/<version>-qa.md` |

*Scope of Recommendation here:* test approach, test level for each case, how deeply each area is tested based on risk, and the regression set. Expected results and exit criteria are Provided.

**Tests first.** In test-design mode, the test cases and the failing automated tests exist before D04 builds anything. They are part of the specification review in D03, where a person reviews the tests themselves, not just their names. Once that review is signed, the tests are locked for the coding agent, and only this step changes them, with the reviewers' renewed approval.

**No test slop** (conventions [Lean code]):
- Every test implements one test case and carries its TC ID in its name, and every test case covers at least one AC, EC, TH, or EV.
- Test the behavior the criteria state, at the lowest level that proves it. Don't duplicate one check at several levels without a reason.
- No tests of the framework, trivial getters, or private details. No large snapshots unless a test case asks for one. No assertions that can't fail.
- Where the team uses mutation testing, run it on the scope's changed code and report the score as evidence that the tests catch real faults.

**Also writes:** automated test files in the code repository the tests belong to, only for test cases the person approved in this run.

{{CORE}}

## Upstream files
`dev/00-dev-setup.md` (environments); `product/00-product-context.md` (statuses, who signs off for product); `dev/architecture.md` (testing stack in section 4, L12 observability); the handoff for the scopes under test: `product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md` (acceptance criteria, edge-case registers), `03-ux/<scope>-<slug>.md` (screens, states), with a design stage the design handoff and Figma frames (the visual reference for UI checks), `02-prd.md` (NFRs, existing behavior); `dev/I-<nnn>-<slug>/03-tasks/<scope>-<slug>.md` (QA tasks); `04-build/` plans (implementation logs, test results); `tracker.yaml` (stories in QA, open bugs, the version's items); QA files of touched scopes.

## Questionnaire (skip what upstream files answer)

**Step 1: What is under test**
0. Test design (before build) or results (after build)? Default: test design when the scope has no approved test cases yet.
1. One scope, or one release version? Which stories (default: everything in the in-QA role for it)?
2. Which environment from `dev/00-dev-setup.md` section 3, and which build or commit?

**Step 2: How**
3. Test levels available and required (unit, integration, end-to-end, manual), and the tools (from the architecture).
4. Devices and browsers to cover (from the PRD and the UX file).
5. Test data and accounts per role: available, or to be created?
6. Who executes: the coding agent, you, or both? Should automated tests be written? (Tests are code: list them here, get approval, then write them, same gate as D04.)

**Step 3: Exit criteria**
7. What must be true to promote to production (for example all acceptance criteria pass, no open critical or high bugs)? If you have none, I'll propose options for you to choose from.
8. Does product sign off before production, and who (from the product context)?

## Output

```markdown
(header: pdlc_step "D05", initiative I-<nnn> (scope QA only), scope <scope ID or version>, depends_on [product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md@x, dev/I-<nnn>-<slug>/03-tasks/<scope>-<slug>.md@x, ...], plus `result: "12/14 pass"` or `result: "Go v1.4.0"`, which the board shows)
# QA: [scope or version]

## 1. Under test
Stories and bugs included, build or commit, environment, date.
## 2. Approach
Levels, tools, devices and browsers, test data, who executes.
## 3. Test cases
| TC ID | Covers (AC, EC, TH, EV IDs) | Level | Preconditions | Steps | Expected | Env | Result | Evidence |
TC IDs come from `pdlc.py new-id tc <story>`. Expected cites the AC ID and adds only test-specific detail (data values, the exact message); the wording of the criterion stays in the stories file. Result: Not run / Pass / Fail / Blocked (query ID). Every edge case (EC ID) of the stories under test has at least one test case, and so does every threat mitigation (TH) from the tech design that applies.
## 4. Regression
Existing behavior that must not change ("unchanged" acceptance criteria and PRD section 6), and cases from touched scopes and earlier releases that this change could break, with results.
## 5. Non-functional checks
| NFR | Method | Threshold (Provided) | Result |
For features with an AI model, the eval set run per group against the team's thresholds (`references/ai-features.md`); below a threshold is a No-go. For compliance NFRs, the checks the obligations need (`references/compliance.md`).
## 6. Defects
| BUG ID | Severity | Story | Steps | Expected | Actual | Status |
## 7. Exit criteria and verdict
Each criterion with pass or fail, product sign-off if required (who, when), then **Go** or **No-go** for promotion to production, with reasons.
## 8. Open items and queries
## Change log
```

## Tracker
- Add each defect to `tracker.yaml` as an item (`pdlc.py new-id bug`; type `bug`, parent the story, initiative, status `backlog`, fix version only if the team set one), and any queries raised.
- Move a story to `done` when it meets the definition of done (all its test cases pass and its code is merged); move it back to `in_progress` when a test fails, with the bug as a dependency.
- Set `result` in this file's header, run `lint --fix` and `board`.

Next: after test design, dev-03-build-tasks for the scope (its tasks cite these test cases, and its specification review signs them off). After results, in the release order: scope QA that passes leaves stories done, waiting for the team to put them in a version (product-06-project-tracker checks it). Version QA in pre-production with a Go goes back to dev-06-deploy to promote to production. On No-go, fix the bugs with dev-04-code-plan-build (it takes a bug ID), then rerun this step. A failure caused by a requirement problem rather than a defect becomes a query to product.
