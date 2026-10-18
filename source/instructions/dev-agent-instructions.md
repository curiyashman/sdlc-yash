# Development skill routing (add to CLAUDE.md and AGENTS.md of each code repository of the product)

## Product configuration (fill in for this product only; anything left blank is asked, never assumed)
- Product name:
- Docs location (repository or store, branch, folder). Chain files go in the docs path, `docs/pdlc/` unless set otherwise:
- Docs path, used below as `[docs path]`:
- Code repositories (name, link, what each holds), and which one this is:

One project or repository serves one product. To work on another product, use a separate project or fill in its own block.

## Product and development docs (PDLC)
- **Read-only for development:** requirements handed off by the product team live in `[docs path]/product/`. With a design stage, the scope's design handoff (`[docs path]/design/<initiative folder>/03-handoff/`) and the frames or prototype it lists are the visual reference. Read frames through the Figma connector when it is available.
- **Where development writes:** development docs live in `[docs path]/dev/`, and maintenance items in `[docs path]/dev/maintenance/`. Tracking data is `[docs path]/tracker.yaml`; `tracker.md` is generated from it and never edited by hand. Tasks live in the `pdlc-tasks` blocks of the scope's task file.
- **Read before asking:** read the product's docs location and the relevant code repositories before asking anything. Any doc made elsewhere gets committed to its path under the docs path before anyone relies on it.
- **Build only from handed-off scopes:** their stories have the `ready_for_dev` status in `tracker.yaml`. Work without a requirement (hotfixes, tech debt, upgrades, spikes, chores) goes through dev-07-maintenance.
- **Never guess:** don't guess about product behavior or a screen. Raise a query in `tracker.yaml` (`to: product` or `to: design`). Change requests belong to the product team.
- **Specification first:** a scope is built only after its test design (dev-05) and its specification review (in dev-03) are approved. Build in the sandbox until the approved tests pass. Approved tests are read-only. Read code by goal, reuse before writing, follow the example files in `architecture.md` section 4, and stay within each task's change budget.
- **Cite requirements, don't copy them:** cite requirements by ID (FR, BR, NFR, US, AC, EC) and read their wording in the owner files.
- **After changing docs or task status:** run `python [docs path]/.pdlc/pdlc.py lint --fix --root [docs path]`, then `board`.

## Which skill
| The task | Skill |
|---|---|
| What is ready to build, what's next, what is blocked or stale | pdlc-next |
| Set up dev conventions, repositories, environments, agents, the lint script and CI | dev-00-dev-setup |
| Product-wide architecture, or the tech design and threat model for a handed-off initiative; "is this feasible" | dev-01-tech-design |
| Schema, tables, migrations for a handed-off scope | dev-02-data-model |
| Test design before any code: developer-level cases from criteria, edge cases, threats; failing tests first | dev-05-test-qa (test design) |
| Tasks and sub-tasks for a handed-off scope, and the specification review that gates the build | dev-03-build-tasks |
| Build a story, implement a task, fix a bug, work a maintenance item, "pick the next ready task" | dev-04-code-plan-build (plan first, wait for approval, then build) |
| Developer test results; product QA / release Go only when `qa_stage` is off | dev-05-test-qa |
| Independent system/E2E QA or release Go when `qa_stage` is on | qa-* (not Development) |
| Environments, CI/CD, deploy, release, incidents when `deploy_stage` is off | dev-06-deploy |
| Same when `deploy_stage` is on | deploy-* (not Development) |
| Hotfix, tech debt, upgrade, spike, chore | dev-07-maintenance |

Before planning or coding, read `[docs path]/dev/00-dev-setup.md`, `[docs path]/dev/architecture.md`, and the `03-tasks` file for your scope under `[docs path]/dev/<initiative folder>/`.
