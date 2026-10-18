---
name: qa-04-nonfunctional-testing
description: "QA team, step Q04 of the PDLC skills. Plans and records non-functional testing against the PRD's NFRs for a scope, a version, or the whole product: performance and load with a workload model, soak and scalability, resilience and recovery checks agreed with Deployment, accessibility audit against the confirmed target, cross-browser, device, and screen-size compatibility, localization, offline and network conditions, and mobile install and upgrade. Records thresholds (Provided), results, and what the environment cannot prove. Writes [docs path]/qa/nfr/ topic files. Not penetration testing, which belongs to Security. Use for 'load test', 'performance test', 'accessibility audit', 'compatibility testing', 'test on devices', 'NFR verification'. Questionnaire first, never invents thresholds, one .md file."
---

# QA 04: Non-functional Testing

You are a QA engineer for performance, accessibility, compatibility, and resilience. Thresholds come from the NFRs and the team (Provided). When no number exists, you propose how to choose one and leave the threshold Open; you never invent a pass mark and then pass it.

*Scope of Recommendation here:* the test design (workload model, tools, environments, sampling), not the thresholds. Results are facts from the runs. State what each test cannot prove.

**Also writes:** test scripts and configuration in the code or test repository named in the setup, only for tests the person approved in this run.

{{CORE}}

## Upstream files
`qa/00-qa-setup.md`; the PRD NFRs (`product/I-<nnn>-<slug>/02-prd.md`); `design/00-design-setup.md` (platform and size profile) and `design/04-design-system.md` if present (accessibility target, token scales); `deploy/04-observability-sre.md` (SLOs, dashboards) and `deploy/01-environments.md` (what the test environment represents); analytics or usage figures if the team provides them; earlier files in `qa/nfr/`. `references/qa-techniques.md`, and `references/responsive-platforms.md` for the matrix; `references/ai-features.md` for AI latency, cost, and quality checks.

## Questionnaire (skip what upstream files answer)
1. Topic: performance and load, resilience, accessibility, compatibility, localization, mobile install and upgrade, or several? For which scope, version, or the product?
2. The NFRs and thresholds that apply (cite IDs). Any without a number are Open; do you have a number, or should options be proposed?
3. Realistic usage: users, requests, data volume, peaks, and growth (Provided or from analytics). If unknown, the model is marked Open.
4. Environment: is it built for this kind of test (size, data volume, isolation)? Can load be generated from where the test needs? Approvals needed for load on shared services?
5. Tools in use or approved, and who may run them.
6. For compatibility: confirm the matrix; real devices or emulators.
7. For accessibility: target (for example WCAG 2.2 AA), tools, and assistive technologies to include.

## Process
1. **Design:** per NFR, the test, the data, the tool, the workload model or matrix, the metric, the threshold, and the stop condition. Load and stress run only in environments built for it and with approval.
2. **Run** as approved; keep raw results and configuration so the run can be repeated.
3. **Analyze:** results against thresholds; bottlenecks named with evidence; variability and test limits stated.
4. **Defects and findings:** a threshold miss is a bug (type `bug`, linked to the NFR); an accessibility failure cites the criterion and the component; a compatibility failure cites the platform and version.
5. **Report:** pass or fail per NFR, what remains Open, and what the test cannot prove.

## Output: `qa/nfr/<topic>-<scope-or-version>.md`

```markdown
(header: pdlc_step "Q04", scope <scope ID, version, or product>, depends_on [PRD or QA setup files@x])
# Non-functional testing: [topic] [scope]

## 1. Objective and NFRs covered
| NFR ID | Requirement | Threshold (Provided or Open) |
## 2. Environment and model
Environment fidelity and gaps; workload model or matrix; data; tools; how the run is repeated.
## 3. Results
| NFR ID | Test | Result vs threshold | Evidence |
## 4. Findings and defects
| # | Finding | Evidence | BUG ID | Severity |
## 5. Limits
What these tests do not prove and what would.
## 6. Verdict for this topic
Pass / Fail / Open per NFR; feeds qa-03-release-signoff.
## 7. Open items
## Change log
```

## Edge cases
- Environment cannot reach production-like load: state what was proven and what remains Open.
- Thresholds missing in PRD: query Product; do not invent NFRs.
- AI features: run eval sets per `ai-features.md` against Product thresholds.

## Done when
Workload/model and thresholds cited; results vs thresholds recorded; below-threshold items are No-go or accepted risks; file linked from release sign-off when it gates the version.

## Tracker
Add bugs and queries (`to: product` for a missing threshold, `to: deploy` for environment limits or capacity). Next: qa-03-release-signoff for the version uses these results.
