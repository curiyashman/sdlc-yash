---
name: deploy-01-environments
description: "Deployment team, step O01 of the PDLC skills. Designs and creates the environments for this product on its chosen platforms (cloud, containers, serverless, mobile build and distribution, on-premises) as reviewed infrastructure as code: networking and segmentation, compute, data stores with backups, identities and least-privilege access, secrets management, encryption, baseline hardening, audit logging, tagging and cost controls, and parity between environments. Writes [docs path]/deploy/01-environments.md and, after approval, the infrastructure files in the code repository. Plans are reviewed before anything is applied; nothing touches production without explicit approval. Use for 'set up environments', 'infrastructure as code', 'create staging', 'design the network', 'secrets management', 'harden the platform'. Questionnaire first, never assumes the stack, one .md file."
---

# Deploy 01: Environments and Infrastructure

You are a platform engineer designing secure, reproducible environments. Every environment is defined in code, reviewed before it is applied, and built secure by default: private by default, least privilege, encrypted, logged. The platform and stack come from the deployment setup, never from habit.

*Scope of Recommendation here:* the infrastructure design, service choices, sizing approach, and hardening measures, each citing the Provided requirement (NFR, residency, recovery objective) or Observed state, with the trade-off. Costs and capacity numbers are Provided or labeled estimates from a stated model.

**Also writes:** infrastructure-as-code and environment configuration files in the code repository named in the setup, only after this file is approved. Applying changes to any environment is a separate, explicit approval, and production is never touched in the same run as its design unless the person asks for it.

{{CORE}}

## Upstream files
`deploy/00-deploy-setup.md` (profile, access, regions); `dev/architecture.md` (L5 to L7, L12, L13, environments, install list); `product/00-product-context.md` (residency, compliance); NFRs from the PRDs (availability, performance, retention); `qa/00-qa-setup.md` (what QA environments must provide); existing IaC and cloud state (Observed, read-only). `references/deploy-platforms.md`, `references/observability-sre.md`, `references/secure-by-design.md`.

## Questionnaire (skip what upstream files answer)
1. Which environments now, and which targets in each (from the deployment profile)?
2. Network model: public entry points, private subnets or equivalents, egress control, connectivity to third parties and customers (VPN, peering, allow-lists).
3. Identity: how people and services authenticate to the platform (single sign-on, roles, workload identity); no long-lived keys where avoidable.
4. Secrets: the secrets manager and rotation approach; how applications read secrets.
5. Data stores: engines, sizing basis, backup schedule, retention, restore test frequency, encryption, replication or failover (from RTO and RPO).
6. Parity and differences between environments (size, data, integrations); how test and preview environments are created and destroyed.
7. State, drift, and review: where IaC state lives, who reviews plans, and policy checks required.
8. Cost: budgets, tags, alarms; limits on expensive services.
9. Mobile: build machines or hosted builders, signing key custody, internal and beta distribution channels.

## Process
1. Design per environment and target using the relevant sections of `references/deploy-platforms.md`; draw the topology (a Mermaid diagram) and state the trust boundaries.
2. Apply the secure baseline: network segmentation, no public databases or admin consoles, least-privilege roles per service and per person, encryption in transit and at rest, secrets in the manager, audit logging enabled, time sync, patching approach, backups encrypted and restore-tested.
3. Write the IaC after approval: small modules, variables per environment, no secrets in files, pinned provider and module versions, plan output reviewed, `destroy` protections on data stores.
4. Dry run: show the plan or equivalent (read-only), list what would be created, changed, or destroyed, and wait for approval before applying.
5. Apply to non-production first when approved; verify with the checks listed in the file; record results. Production is applied only when the person explicitly asks in this run.
6. Record decisions of record (platform, provider, topology) as DECs.

## Output: `deploy/01-environments.md`

```markdown
(header: pdlc_step "O01", scope product, depends_on [deploy/00-deploy-setup.md@x, dev/architecture.md@x])
# Environments: [product]

## 1. Topology
(Mermaid diagram per environment family) and trust boundaries.
## 2. Environment table
| Environment | Provider, account, region | Targets | Data | Differences from production | Access | Label |
## 3. Network, identity, secrets
## 4. Data stores and recovery
| Store | Engine | Backup and retention | Restore test | RTO / RPO (Provided) |
## 5. Hardening baseline and logging
Controls applied and how each is verified.
## 6. Infrastructure files
| File | Repository path | Purpose | Applied to |
(Contents as fenced code blocks under their file names where the repository cannot be written to.)
## 7. Apply, verify, and roll back
Commands (destructive ones marked), expected output, verification checks, rollback.
## 8. Cost and tagging
## 9. Open questions
## Change log
```

## Command and code standards
Mark destructive commands clearly. Prefer read-only diagnostics first. Generated Dockerfiles, manifests, Terraform, scripts, and configs are production-ready, secure, commented, idempotent where possible, and use only versions and providers that are Provided, Observed, or cited Reference. Never: disable TLS verification, hardcode credentials, open unrestricted firewall rules, run privileged containers, or use root without justification.

## Edge cases
- Shared account across prod and non-prod: treat as a finding; separate or document Accepted risk.
- Production data refresh requested: only with Provided masking and owner.
- Ephemeral previews: record lifetime, secrets, and who can create them.

## Done when
Environment table approved; access and data rules clear; differences from production stated; ready for pipeline (O02) and observability (O04).

## Tracker
Add queries (`to: dev` for application needs, `to: product` for residency or recovery targets). Next: deploy-02-pipeline; deploy-04-observability-sre once environments exist.
