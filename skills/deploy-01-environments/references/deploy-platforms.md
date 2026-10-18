# Deployment platforms and stacks (reference pack for the deploy skills)

Choose the sections that match this product's platforms and stack, as recorded in O00. Nothing here is a default. Versions, services, and flags are **Reference**: check current documentation and record the date. Where a product has several targets (for example a web app and two mobile apps), each target gets its own row in the deployment profile.

## Deployment profile (recorded in O00)
| Target | Platform family | Stack and runtime | Environments | Release method | Rollback method | Owner | Label |
|---|---|---|---|---|---|---|---|

## 1. Web applications and APIs on virtual machines or platform services
Static site or SPA on object storage plus CDN; server apps on VMs, managed app platforms, or PaaS. Ask: region(s) and residency, domains and TLS certificates, CDN and cache invalidation, load balancers and health checks, autoscaling, process manager, OS patching, configuration and secrets, session or state storage, database location and network path, zero-downtime needs.

## 2. Containers and orchestration
Image build (minimal base, non-root, pinned digests, no secrets in layers), registry and retention, vulnerability scanning of images, orchestration (Kubernetes or a managed container service): namespaces, resource requests and limits, probes, rollout strategy, pod disruption budgets, network policies, RBAC, secrets (external secrets manager), ingress and TLS, config maps, horizontal scaling, node patching, cluster upgrades, GitOps or push-based deploy, Helm or manifests, admission policy.

## 3. Serverless and managed services
Functions and event-driven pipelines: packaging, cold-start behavior, concurrency and timeout limits, permissions per function, event source retries and dead-letter queues, idempotency, cost limits and alarms, versions and aliases for rollout, observability for short-lived compute, local emulation versus real-environment testing.

## 4. Mobile apps (iOS and Android)
Build and signing: certificates, provisioning profiles, keystores and their custody; build numbers and versioning; distribution channels (internal testing, beta, staged production); store review requirements (privacy declarations, data safety forms, permission explanations, account deletion rules, content ratings); phased rollout and halting a rollout; forced-update and minimum-version policy; backward compatibility with older app versions for APIs and data; crash reporting; remote configuration and feature flags (store rules limit changing behavior after review); over-the-air update mechanisms only where the store policies and the product's risk allow; rollback means a new build, a halted rollout, and server-side flags, not an instant revert.

## 5. Desktop and on-device software
Installers and updaters, code signing and notarization, update channels, delta updates, telemetry consent, and recovery from failed updates.

## 6. On-premises and private cloud
Hardware or VM baseline, air-gapped or restricted networks, offline packages and mirrors, change windows, customer-managed upgrades, licensing, backup and restore on customer systems, remote support access and its audit.

## 7. Data stores and migrations (all platforms)
Managed versus self-hosted databases, backups and tested restores, point-in-time recovery, replication and failover, schema migrations (see `deploy-methods.md` for expand and contract), data residency, encryption, connection limits, maintenance windows.

## 8. Infrastructure as code and environments
Declarative IaC (for example Terraform, OpenTofu, Pulumi, CloudFormation, Bicep, Ansible) with remote state and locking, modules, environment parity, drift detection, policy checks, plan review before apply, separate accounts or projects per environment, tagging for cost and ownership. Never apply to production from a laptop with long-lived admin keys when a pipeline gate exists.

## 9. CI/CD
Pipeline stages (build, test, scan, package, publish, deploy), required gates (developer tests, QA gate, security gate), artifact promotion across environments without rebuilding, ephemeral and isolated runners, short-lived credentials (workload identity), protected environments and approvals, provenance and signing, SBOM generation, caching, and notifications.

## Environment ladder (typical; rename to the product's terms)
| Environment | Purpose | Data | Who deploys |
|---|---|---|---|
| Local / ephemeral | Developer and agent sandboxes | Synthetic | Developers |
| Integration / QA | Independent QA and automation | Synthetic or masked | Pipeline or Deploy |
| Pre-production | Release candidate, version QA | Near-prod shape, masked | Deploy on release |
| Production | Users | Real | Deploy with approval |

Production data is never copied down without a Provided masking process and owner. Admin interfaces and databases are not public.

## Cross-cutting questions for every target
Regions and residency; TLS and certificate renewal; secrets custody; identity and access (human and machine); backup and restore proof; observability hooks; cost limits; compliance logging retention; rollback path that has been practiced or at least written and reviewed.
