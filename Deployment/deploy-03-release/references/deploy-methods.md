# Release and rollout methods (reference pack for deploy-03 and deploy-05)

Pick a method per target with the team (Provided or Recommendation with the trade-offs). A release file names the method, the trigger for rollback, and how rollback is verified.

| Method | Use when | Watch for | Rollback |
|---|---|---|---|
| Recreate | Downtime is acceptable; simple stateful systems | Outage during the swap | Redeploy the previous version |
| Rolling | Stateless services, many instances | Mixed versions running together; incompatible schema or API | Roll back the batch; confirm health |
| Blue-green | Fast, clean cutover and revert; enough capacity for two stacks | Cost; shared state and database changes; long-lived connections | Switch traffic back |
| Canary / progressive | Risky changes; real traffic validation | Needs good metrics, automatic analysis, and traffic splitting | Stop and shift traffic back |
| Feature flags / dark launch | Decouple deploy from release; per-tenant rollout | Flag debt; flag evaluation as an attack surface; testing both states | Turn the flag off |
| Staged store rollout (mobile) | App-store distribution | Cannot revert installed apps; old versions keep calling the backend | Halt rollout; ship a fixed build; server-side flags |
| Scheduled maintenance window | On-prem, large migrations | Communication, support coverage | Restore from backup per plan |

## Choosing a method (quick guide)
- Prefer **rolling** or **blue-green** for APIs and web backends that must stay up.
- Prefer **canary** when blast radius or unknown risk is high and metrics exist.
- Prefer **flags** when product wants to ship dark or per tenant.
- Prefer **staged store** for mobile; never assume instant rollback of installed apps.
- Prefer **maintenance window** only when expand/contract is impossible and downtime is Accepted.

## Database changes: expand and contract
1. Expand: add new columns, tables, or indexes in a backward-compatible way.
2. Deploy code that works with both the old and the new shape; backfill data in controlled batches.
3. Switch reads and writes to the new shape.
4. Contract: remove the old shape in a later release, after the rollback window has passed.

Migrations are reviewed, tested against production-sized data, reversible or backed by a verified backup, and never combined with an irreversible step in the same release. Record migration order, lock risk, and expected duration in the release file.

## Release safety checklist
Version contents confirmed against the tracker; migrations and their order; configuration and secret changes (names only in the file); feature flags and their defaults; dependency and compatibility with running clients (older mobile versions, cached front ends); capacity and cost; backup taken and restore tested; observability in place for the change (dashboards, alerts, SLO impact); communication plan and on-call coverage; rollback trigger, rollback steps, and who decides; QA verdict and, where the product has a Security stage, the security sign-off.

## Promote gates (when stages are on)
1. Pre-production deploy complete and healthy (O03 sections 1–3).
2. Version status `staged`.
3. QA Go from `qa-03-release-signoff` (or D05 version Go when `qa_stage` is off).
4. Security Go from `sec-05-retest-signoff` when `security_stage` is on (read only the Go/No-go result).
5. Explicit production approval recorded with name, role, and time.
6. Promote with the chosen method; verify health and SLO signals; keep rollback ready.

## Hotfix path
A hotfix still carries a record: the item (`HF-`), the reason, the smallest change, a targeted test, QA and security checks proportional to the risk, an approval, and a rollback plan; the full process is caught up afterwards. Prefer flags or canary when the platform allows.

## Rollback decision rule
Roll back (or halt) when: error budget burn is high, critical user journeys fail, data risk appears, or the named approver calls it. Prefer reversible traffic shifts before irreversible data repairs. After rollback, open or update incidents and defects; do not silently re-promote.
