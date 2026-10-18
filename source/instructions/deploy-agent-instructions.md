# Deployment skill routing (add to the platform / SRE team's Claude project, or to CLAUDE.md and AGENTS.md)

## Product configuration (fill in for this product only; anything left blank is asked, never assumed)
- Product name:
- Docs location (repository or store, branch, folder). Chain files go in the docs path, `docs/pdlc/` unless set otherwise:
- Docs path, used below as `[docs path]`:
- Code repositories (name, link, what each holds), including infrastructure repos:

One project or repository serves one product. To work on another product, use a separate project or fill in its own block.

This project uses the Deployment skills (deploy-00 to deploy-05) and pdlc-next when `config.deploy_stage: true`. When the Deployment stage is off, Development uses `dev-06-deploy` instead — do not run both for the same release.

## Sources and rules
- **Read-only:** product context, architecture (L5–L7, L12, L13), build plans for migrations/flags, QA sign-off Go / No-go (result only), Security sign-off Go / No-go when the Security stage is on.
- **Your files** live in `[docs path]/deploy/`. Tracking data is `[docs path]/tracker.yaml`.
- **Gates:** promote to production only after QA Go (qa-03 when QA stage on, else the recorded D05 version Go) and Security Go when the Security stage is on, plus explicit recorded approval.
- **Never invent commands or causes:** cite Observed evidence; mark hypotheses as such.
- **Lint:** after each run, run the skill's `scripts/pdlc.py lint --fix --root [docs path]` and then `board`.

## Which skill
| The task | Skill |
|---|---|
| What is next for Deployment | pdlc-next `--team deploy` |
| Deployment profile, methods, approvers, stage on | deploy-00-deploy-setup |
| Environments design and access | deploy-01-environments |
| CI/CD pipeline and gates | deploy-02-pipeline |
| Release, promote, hotfix, rollback, store submit | deploy-03-release |
| SLOs, dashboards, on-call, observability | deploy-04-observability-sre |
| Incident, outage, post-incident review | deploy-05-incident-response |

Order: deploy-00 once; deploy-01 then deploy-02; deploy-04 when environments exist; deploy-03 per version; deploy-05 when something breaks. Pick one skill per turn, start with "Using deploy-0X-name for [target] because [reason].", and name the next step at the end.
