# Observability and SRE (reference pack for deploy-04 and deploy-05)

## Service level objectives
For each user-facing journey and each critical dependency: an indicator (what is measured), an objective (the target over a window), and an error budget. Targets are **Provided** by the team; otherwise Open. Typical indicators: availability, latency percentiles, correctness or freshness, throughput, durability. Alert on the speed at which the error budget is being spent, not on every blip. Tie each SLO to the NFRs in the PRD.

| Element | Record |
|---|---|
| Journey or dependency | Name and owner |
| SLI | Exact measurement (query or metric) |
| SLO | Target + window |
| Error budget | How burn is calculated |
| Alert | Who is paged, runbook link |

## The signals
- **Metrics:** the golden signals (latency, traffic, errors, saturation) per service, business metrics for key flows, and cost.
- **Logs:** structured, with a request or trace ID; no secrets or personal data; retention and access that match obligations; tamper resistance for audit logs.
- **Traces:** distributed tracing across services and clients where more than one component takes part in a request.
- **Real-user and synthetic monitoring:** critical journeys probed from outside, per region; for mobile, crash and performance reporting with consent.
- **Events and change tracking:** deploys, flag changes, and configuration changes appear on the same timeline as the metrics.

## Alerting
Every alert is actionable, has an owner and a runbook, and has a severity with a response expectation. Page for user-visible, urgent problems; ticket for the rest. Review noisy alerts regularly. Security-relevant alerts (failed logins, privilege changes, unusual data access, policy changes) go to the owners the security process names.

Severity guide (align with incident severity in O05): **SEV1** user-visible outage or data risk; **SEV2** major degradation; **SEV3** limited impact; **SEV4** informational.

## Dashboards
One service overview per service, one per journey, one for dependencies, and one for cost. A dashboard answers a question; remove those that do not. Release dashboards must show the version, flags, and error-budget burn for the journeys in the release.

## On-call and response
Rotation, escalation path, handover, severity definitions, communication channels and templates for users and stakeholders, an incident commander role for serious incidents, and a blameless post-incident review within the team's agreed time, with actions tracked as items.

## Reliability work
Capacity planning and load forecasts; autoscaling tests; graceful degradation and timeouts, retries with backoff, circuit breakers, bulkheads; dependency failure drills; backup and restore tests with recovery time and recovery point objectives (Provided); disaster recovery plan and exercise; chaos or game-day exercises where the team accepts them; toil reduction and automation.

## Runbooks
For every alert and common failure: symptoms, impact, checks (read-only first), safe mitigations, escalation, and verification. Runbooks are versioned files and tested by use. Link each production alert to exactly one runbook.

## Cost
Tagging and budgets per environment and team, anomaly alerts, right-sizing reviews. Unbounded usage (for example AI calls, egress) has limits and alerts. Cost regressions after a release are a deploy finding, not only a finance topic.

## Done when (observability baseline)
SLOs recorded or explicitly Open; golden signals for each production service; structured logs with redaction rules; deploy markers on timelines; on-call and escalation documented; at least one synthetic or RUM check for the top journey; runbooks for SEV1/SEV2 alerts.
