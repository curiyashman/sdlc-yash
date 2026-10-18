# QA techniques (reference pack for the qa skills)

QA is an independent view of the product: it tests against the **requirements and the user's experience**, not against how the code was written. Expected results are Provided by the PRD, UX files, stories, and design handoff; an unclear expectation becomes a query and the case is Blocked.

## What QA owns vs Development
| Level | Owner |
|---|---|
| Unit, component, integration, contract | Development (dev-05), before code |
| System / E2E from requirements, regression, cross-platform, accessibility, usability, data/migration correctness, NFR, UAT, release Go | QA (this pack's skills) |
| Penetration / vulnerability / privacy audit attacks | Security (independent) |

Do not duplicate developer-level cases. Read `dev/**/05-qa/` only to avoid overlap.

## Test design techniques
Equivalence partitions and boundary values for every input; decision tables for rules with several conditions; state-transition tests for workflows and statuses; pairwise combinations for configuration spaces; use-case and journey tests along the flows; error guessing from past defects; exploratory sessions with a charter and a time box; negative and misuse tests from the abuse stories; data variations (empty, maximal, special characters, unicode, long text, time zones, daylight-saving changes, currencies, locales, large volumes).

Traceability rule: every TC cites at least one AC, EC, FR, NFR, or "must not change" ID. Every AC and blocking EC in scope has at least one TC (or an explicit `na` with reason).

## Test types to consider per scope (select by risk)
Functional; end-to-end journeys; regression; integration and contract behavior seen from outside; cross-role permissions; data and migration correctness; compatibility (browsers, OS, devices, screen sizes/orientations, app versions); responsive behavior at every breakpoint in the design profile; localization; accessibility (keyboard only, screen reader, zoom/reflow, contrast, target size, text scaling); usability and content; performance and load; resilience (network loss, slow network, retries, interrupted flows, background/resume on mobile); installation and upgrade; offline and sync; notifications and emails; payments in test mode; analytics events; privacy flows (consent, withdrawal, export, deletion); security-adjacent functional checks (roles, session expiry, error messages) without attack testing.

## Risk-based depth
| Risk | Depth |
|---|---|
| Money, personal data, permissions, migrations, auth | Deep: positive, negative, boundary, abuse, multi-role, regression neighbors |
| Core happy path for the release | Full journey + one alternate + one error |
| Low-risk cosmetic or admin-only | Smoke or sample; document reduced coverage |

## Environments and data
Test environments mirror production in shape; test data is synthetic or masked, with accounts per role and tenant; no production personal data. Record the build under test, the environment, and the data set for every run. Third-party services: sandbox or mock unless a Provided reason requires a real integration.

## Matrix
Build the platform and size-class matrix from the design setup (web browsers and viewport widths, iOS and Android devices and OS versions, orientations, input modes). Mark each cell: automated, manual, or not covered, with the reason. Partial coverage needs a named risk owner when it affects a release Go.

## Automation
Automate stable, high-value, repeatable journeys at the UI or API level; keep tests independent, deterministic, and fast; avoid duplicating developer-level tests; quarantine flaky tests with an owner; treat test code as code. Visual comparison only where it adds value. The team's tools come from the setup (Provided).

## Defects
Each defect has: ID, title, severity, priority (the team's scale), environment and build, steps to reproduce, expected, actual, evidence, story or requirement affected, and status. Severity guide: **Critical** blocks core use, loses or corrupts data, or has security or legal impact; **High** breaks a main flow without a workaround; **Medium** breaks a secondary flow or has a workaround; **Low** is cosmetic or minor. Retest every fix and the area around it. Link defects to the story and to the TC that found them.

## Exit criteria and sign-off
Criteria are Provided by the team (for example every acceptance criterion passes, no open critical or high defects, regression passes, NFR thresholds met). Verdicts are **Go** or **No-go** with reasons; conditional Go lists accepted risks with a named approver. Schedule pressure is never a substitute for missing evidence.

## Non-functional testing
Performance and load: workload model from real or Provided usage, ramp profiles, soak runs, thresholds from NFRs (Provided), results per environment, and what the environment cannot prove. Run only in environments built for it. Resilience and recovery checks as agreed with Deployment. Accessibility audit against the confirmed target. Below-threshold NFR results are No-go unless a named owner accepts the risk in writing.

## Common failure modes to watch for
Flaky automation treated as green; expected results copied from the UI instead of from ACs; untested roles; matrix cells silently skipped; production data in QA; release Go without regression of untouched scopes that share code or data.
