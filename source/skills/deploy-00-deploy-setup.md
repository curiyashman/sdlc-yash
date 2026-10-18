---
name: deploy-00-deploy-setup
description: "Deployment team, step O00 of the PDLC skills (DevOps, platform, and SRE). Records how this product is deployed and operated, whatever its platforms, stack, and methods: the deployment profile per target (cloud web or API, containers and Kubernetes, serverless, mobile apps in the App Store and Google Play, desktop, on-premises), cloud accounts and regions with data-residency limits, environments, who may deploy and approve, release methods (rolling, blue-green, canary, flags, staged store rollout), tools, recovery objectives, observability tools, compliance limits, and approvers. Writes [docs path]/deploy/00-deploy-setup.md and switches the deployment stage on. Use for 'set up deployment', 'how do we deploy', 'choose release strategy', 'which cloud', 'deploy mobile apps', 'change approvers'. Questionnaire first, never assumes the stack, one .md file."
---

# Deploy 00: Deployment Setup

You are a senior platform engineer and SRE. Deployment is its own team because shipping and running software well depends on platform, stack, and method, and these differ for every product. This step records the facts the rest of the team's work depends on. It never assumes a cloud, a tool, or a release method.

*Scope of Recommendation here:* options for platform services, release methods, and tooling, each with trade-offs and sources, for the team to choose. Accounts, regions, approvers, recovery objectives, budgets, and policies are Provided. Obligations such as data residency come from the product context (Provided).

**Also writes:** nothing beyond the tracker.

{{CORE}}

## Upstream files
`product/00-product-context.md` (platforms, markets and data residency, compliance, version scheme, approvers, statuses); `design/00-design-setup.md` (platforms and size classes); `dev/00-dev-setup.md` and `dev/architecture.md` (repositories, stack, L5 to L7, L12, L13, environments, install list); `qa/00-qa-setup.md` (QA environments); `tracker.yaml`; existing infrastructure, pipeline, and cloud configuration in the repositories (Observed, read-only). `references/deploy-platforms.md` (platform and stack choices), `references/deploy-methods.md` (release methods), `references/secure-by-design.md`.

## Questionnaire (skip what upstream files answer)

**Step 1: Targets**
1. Every deployable target: web frontend, API/backend, workers, databases, mobile apps (iOS, Android), desktop, on-premises packages, others. For each: platform family and stack (from the architecture).
2. For mobile targets: developer accounts, signing custody, distribution channels, the store review owner, and minimum supported versions.

**Step 2: Platforms and access**
3. Cloud or hosting providers, accounts or subscriptions, regions, and any data-residency or sovereignty limit (from the product context; if unclear it is Open and goes to legal).
4. Who has access to what in each environment; who may deploy; who approves production; separation of duties; emergency access.
5. Environments needed (for example development, test or QA, pre-production, production, ephemeral preview) and how each differs. Is production data ever used elsewhere, and if so how is it masked?

**Step 3: Method**
6. Release method per target (from `references/deploy-methods.md`): recreate, rolling, blue-green, canary, flags, staged store rollout. Zero-downtime needs, maintenance windows, and the rollback expectations.
7. Pipeline provider and branching or tagging model; artifact registry; required gates (developer tests, QA Go, security sign-off).
8. Infrastructure as code tool, state storage, and policy checks; or console-managed today.

**Step 4: Operations**
9. Reliability expectations: availability targets, latency expectations, RTO and RPO. If none exist, options are proposed and the values stay Open.
10. Observability tools in use (logs, metrics, traces, alerting), on-call arrangement, incident tools.
11. Budget and cost controls; tagging; limits for unbounded services (for example AI calls, egress).
12. Policies: tools required or banned, compliance regimes touching operations (logging retention, encryption, access reviews).

## Process
1. Read the upstream files and the existing infrastructure and pipeline files (Observed).
2. Build the confirm sheet with proposed defaults and their basis; options with trade-offs for each open choice.
3. Write the file, play back "Inputs confirmed", and get approval from the recorded approver.

## Output: `deploy/00-deploy-setup.md`

```markdown
(header: pdlc_step "O00", scope product, depends_on [product/00-product-context.md@x, dev/architecture.md@x])
# Deployment setup: [product]

## 1. Deployment profile
| Target | Platform family | Stack and runtime | Environments | Release method | Rollback method | Owner | Label |
## 2. Platforms, accounts, regions
Providers, accounts, regions, residency limits and their source.
## 3. Environments and access
| Environment | Purpose | Data | Who deploys | Who approves | Label |
Separation of duties; emergency access; production data rules.
## 4. Release and pipeline approach
Methods per target, gates, branching or tagging model, artifact flow, IaC tool.
## 5. Reliability and observability
Availability and latency expectations, RTO and RPO (Provided or Open), tools, on-call.
## 6. Cost and policy
## 7. Approvers
## 8. Open questions
## Change log
```

## Edge cases
- Multiple targets (web + mobile): one profile row each; methods may differ.
- Deployment stage turned on while old `dev/releases/` exist: new work uses `deploy/`; do not duplicate active releases.
- Missing residency rules: Open + legal query, never assume a region.

## Done when
Profile complete for every target; approvers and gates named; `config.deploy_stage: true` on approval; next step named (usually O01 then O02).

## Tracker
Set `config.deploy_stage: true` on approval. Next: deploy-01-environments to design and create the environments, then deploy-02-pipeline; deploy-04-observability-sre can start once environments exist.
