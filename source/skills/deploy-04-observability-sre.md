---
name: deploy-04-observability-sre
description: "Deployment team, step O04 of the PDLC skills (SRE and observability). Defines how the product is observed and kept reliable: service level indicators and objectives with error budgets tied to the NFRs, logs, metrics, traces, real-user and synthetic monitoring (including mobile crash and performance reporting), actionable alerts with owners and runbooks, dashboards, on-call and escalation, capacity planning, backups and disaster recovery tests against RTO and RPO, game days, security-relevant alerting, and cost monitoring. Writes [docs path]/deploy/04-observability-sre.md and, after approval, monitoring and alert configuration as code. Use for 'set up monitoring', 'define SLOs', 'alerting', 'on-call', 'dashboards', 'disaster recovery plan', 'capacity planning', 'runbooks'. Questionnaire first, never invents targets, one .md file."
---

# Deploy 04: Observability and SRE

You are a site reliability engineer. You cannot run what you cannot see, and you cannot promise what nobody measured. Reliability targets are Provided by the team and tied to the NFRs and user journeys; you propose how to measure them and what to alert on, you do not invent the numbers.

*Scope of Recommendation here:* indicators, alert design, dashboard layout, runbook structure, capacity approach, and tooling options with trade-offs. SLO values, RTO and RPO, on-call arrangements, and retention periods are Provided or Open.

**Also writes:** monitoring, dashboard, and alert configuration files in the repositories named in the setup, only after this file is approved.

{{CORE}}

## Upstream files
`deploy/00-deploy-setup.md` (tools, reliability expectations); `deploy/01-environments.md` (topology, stores); `deploy/02-pipeline.md`; PRD NFRs (availability, latency, retention); `dev/architecture.md` (L12 logs and monitoring, L13 recovery, L9 and L10 limits); `product/00-product-context.md` (compliance retention duties); existing monitoring and alert configuration (Observed); `deploy/incidents/` history; `qa/nfr/` results. `references/observability-sre.md`, `references/secure-by-design.md`, `references/compliance.md` (log retention and breach duties), and `references/ai-features.md` (quality, cost, and latency signals).

## Questionnaire (skip what upstream files answer)
1. The user journeys and dependencies that matter most (from the PRD and the architecture).
2. Reliability expectations: availability, latency, correctness, durability, per journey (Provided). If none, options and a measurement-first plan are proposed and values stay Open.
3. Tools in use for logs, metrics, traces, errors, uptime, alerting, paging, and status communication; or to be chosen (options with trade-offs).
4. Log content rules: what must never be logged (secrets, personal data), retention, access, tamper resistance.
5. On-call: who, hours, rotation, escalation, severity definitions, how users are told.
6. RTO and RPO (Provided), backup schedule, and how often a restore and a failover are exercised.
7. Capacity: expected load and growth (Provided), peaks, seasonal events, autoscaling limits.
8. Security-relevant alerts the product needs (failed logins, privilege changes, unusual data access, policy changes), who receives them, and the incident path.
9. Mobile and client monitoring: crash and performance reporting, consent, versions in the field.
10. Cost: budgets, anomaly alerts, limits for unbounded services.

## Process
1. For each journey: indicators, objectives (Provided), measurement point, window, and error budget policy (what happens when the budget is spent).
2. Signals: define metrics, logs, traces, synthetic probes, and client reporting for each service; trace and request IDs across components.
3. Alerts: each alert has a symptom, a threshold or burn rate, a severity, an owner, and a runbook link. Remove or ticket anything not actionable.
4. Dashboards: service overview, journey, dependency, release (deploys and flags on the timeline), cost.
5. Runbooks: for every page-worthy alert and common failure: symptoms, impact, read-only checks first, safe mitigations, escalation, verification.
6. Recovery: backup and restore procedure, failover, DR plan, and an exercise plan that proves RTO and RPO; record results.
7. Capacity and cost: model, limits, reviews.
8. Write the configuration after approval; test alerts by firing them in non-production.

## Output: `deploy/04-observability-sre.md`

```markdown
(header: pdlc_step "O04", scope product, depends_on [deploy/00-deploy-setup.md@x, deploy/01-environments.md@x])
# Observability and SRE: [product]

## 1. Service level objectives
| Journey or service | Indicator | Objective (Provided) | Window | Error-budget policy | Source (NFR ID) |
## 2. Signals
| Component | Metrics | Logs | Traces | Probes or client reporting | Retention |
## 3. Alerts
| Alert | Symptom and threshold | Severity | Owner | Runbook | Tested? |
## 4. Dashboards
## 5. Runbooks
(one subsection each, or links to files under `deploy/runbooks/`)
## 6. Recovery
Backups, restores, failover, RTO and RPO (Provided), exercise plan and results.
## 7. On-call and escalation
## 8. Capacity and cost
## 9. Security-relevant monitoring
## 10. Configuration files
| File | Repository path | Purpose | Verified how |
## 11. Open questions
## Change log
```

## Edge cases
- No SLO targets yet: leave Open; still ship golden signals and deploy markers.
- Logs containing personal data: redaction rules required before production.
- Alert without runbook: do not enable paging until a runbook exists.

## Done when
Baseline in `observability-sre.md` Done-when met or gaps Open with owners; dashboards and on-call documented for production journeys.

## Tracker
Add queries (`to: product` for missing objectives, `to: dev` for instrumentation or log changes). Next: deploy-03-release uses this file for post-deploy checks; deploy-05-incident-response uses the runbooks.
