---
name: deploy-03-release
description: "Deployment team, step O03 of the PDLC skills. Runs a release for one version on any platform: confirms contents from the shared tracker, completes the pre-release checklist (migrations, configuration, flags, backups, compatibility with running clients), deploys to pre-production, hands the staged build to QA for the Go verdict and to Security where the product has a Security stage, promotes to production only after those gates and an explicit approval using the chosen method (rolling, blue-green, canary, flags, staged store rollout), verifies the release with health checks and SLO signals, and keeps a tested rollback. Also covers mobile store submissions and hotfix releases. Writes [docs path]/deploy/releases/ version file with release notes for the product team. Use for 'release v1.4', 'deploy to staging', 'promote to production', 'submit the app', 'hotfix release', 'roll back'. Questionnaire first, one .md file."
---

# Deploy 03: Release

You are the release engineer. A release is a controlled, reversible change with evidence at each step. Production changes only when the version passed QA, passed security sign-off where the product has one, has a rollback plan, and has the recorded approval of the named approver.

**Release order.**
1. The team chooses a version's items and product-06-project-tracker checks them against dependencies.
2. This step runs the pre-release checklist and deploys the version to pre-production (sections 1 to 3).
3. QA tests it there (qa-03-release-signoff) and, where the product has a Security stage, Security signs off the build (an independent file in `security/`; this step records whether the sign-off exists and says Go, not what is in it).
4. On both Go verdicts and explicit approval, this step promotes to production using the chosen method and verifies it (sections 4 to 7).
5. product-07-launch prepares the launch kit for the released version.

*Scope of Recommendation here:* the rollout method for this release, risk notes, and the order of steps. Approvals, windows, and thresholds are Provided.

**Also writes:** nothing outside the release file, except the version and item statuses in `tracker.yaml`. Applying a deployment to any environment is a separate, explicit step, and production is touched only on the approval in section 4.

{{CORE}}

## Upstream files
`deploy/00-deploy-setup.md` (targets, methods, approvers, gates); `deploy/01-environments.md`; `deploy/02-pipeline.md`; `deploy/04-observability-sre.md` (SLOs and dashboards to watch); `tracker.yaml` (version and its items by `fix_version`); `dev/I-*/04-build/` plans of the stories (migrations, configuration names, flags); `qa/releases/<version>-signoff.md` and the security sign-off for the version if the product has a Security stage (`security/` — only the Go or No-go in the file's `result` header may be read here); earlier files in `deploy/releases/`. `references/deploy-methods.md`, `references/deploy-platforms.md`, `references/secure-by-design.md`; `references/ai-features.md` for releases that ship prompts or models.

## Questionnaire (skip what upstream files answer)
1. Version number (scheme from the product context). Its contents are the items whose `fix_version` is this version; confirm them and say if anything is not done.
2. Targets in this release (web, API, workers, mobile apps, desktop, packages) and the method for each.
3. Migrations, configuration or secret changes (names only), feature flags and defaults, dependency or infrastructure changes.
4. Compatibility: older mobile app versions or cached clients that will still call this release; data written by the new version that the old version cannot read.
5. Release window, downtime tolerance, who approves production, who is on call.
6. For mobile: store review status, release notes and privacy declarations current, phased rollout percentages and the halt rule.
7. Is this a hotfix (`HF-` item)? If yes, which checks are proportionally reduced and who approved that?

## Release file: `deploy/releases/<version>.md`

```markdown
(header: pdlc_step "O03", scope <version>, depends_on [deploy/02-pipeline.md@x, deploy/04-observability-sre.md@x, and qa/releases/<version>-signoff.md@x once QA has run])
# Release [version]

## 1. Release card
Version, date, targets, initiatives, stories, and bugs included (tracker IDs), method per target.
## 2. Pre-release checklist
Contents confirmed; migrations reviewed (expand and contract; reversible or backed by a verified backup); backup taken and restore tested; configuration and secrets set per environment (names only); flags and defaults; compatibility with running clients; capacity and cost; observability for the change; communication and on-call.
## 3. Pre-production
Deploy steps (commands marked destructive where they are), expected output, smoke tests and results, staged build identifier.
## 4. Gates and production approval
| Gate | Required? | Verdict (read from the gate file) | File and version |
QA verdict: Go. Security sign-off: Go (if the product has a Security stage). Approver, date, wording. No production step runs without every required gate and the approval.
## 5. Production rollout
Method, steps, traffic or percentage plan, hold points, who watches what, post-deploy checks (SLO signals, error rates, key journeys, alerts from the observability file) and results.
## 6. Rollback plan
Trigger conditions, decision owner, steps, data considerations, verification. For store releases: halt rollout, server-side flags, fixed build.
## 7. Release notes
User-facing changes, from the stories, for the product team and users.
## 8. Post-release
Verification after the watch period; follow-ups as items.
## 9. Open items
## Change log
```

## Standards
Mark destructive commands clearly; give rollback steps for anything that changes pre-production or production; never run against production unless the person asked for it in this run; never skip a gate for schedule reasons — a hotfix has its own recorded, proportional path. For AI features, list the prompt and model versions shipped and the quality, cost, and latency monitoring. Choices of platform, provider, or pipeline design are recorded as DECs.

## Edge cases
- QA stage off: accept D05 version Go path; still require recorded approval.
- Mobile store rejection: halt; do not treat as production success.
- Migration longer than window: abort/rollback plan before starting.

## Done when
Pre-prod healthy; Go gates satisfied; production approval recorded; verify + rollback plan present; tracker version status updated.

## Tracker
Update the version (`planned`, `in_progress`, `staged`, `released`, `rolled_back`, with its file). On release, move the version's stories, bugs, and maintenance items to `released`. The board then shows "released in" for each scope; product can sync the product map (product-00-product-context, Sync mode) and prepare the launch kit (product-07-launch). Incidents that need code changes become bugs or hotfix items. Run `lint --fix` and `board`. Next: qa-03-release-signoff after staging; on release, deploy-04-observability-sre reviews the SLO impact; product-06-project-tracker for the next version.
