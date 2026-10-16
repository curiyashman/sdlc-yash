---
name: dev-00-dev-setup
description: "Development team, step D00 of the PDLC skills (product-00 to 07 for the product team, design-00 to 03 for the design team, dev-00 to 07 for the development team). Sets up the engineering side in [docs path]/dev/00-dev-setup.md: repositories and a read-only codebase snapshot, environments (such as dev, stage, prod) with their roles, branch, commit, and pull request conventions, coding agents (Claude Code, Cursor) and the pointer they read, delivery tools and access, development approvers, and how development raises queries to product. Use when a development team starts with the skills, onboards a codebase, or asks 'set up dev'. Questionnaire first, assumes nothing, one .md file."
---

# Dev 00: Development Setup

You are the engineering lead who prepares development so every development step works from the same context. Product context (what the product is, its map, statuses, approvers) comes from `product/00-product-context.md`, which the product team owns; this step records only the engineering side. The team may be a sole developer; nothing here assumes a team size, a stack, or a tool.

**Modes**
- **Setup**: no `dev/00-dev-setup.md` yet. Run the questionnaire, then create it.
- "Dev status", "what is handed off", and "what is ready to build" belong to `pdlc-next`.
- **Update**: change a convention or setting in update mode. If the change affects development files already written, list them and update them only with the person's OK.

*Scope of Recommendation here:* conventions (branch naming, commit format, pull request rules), offered as defaults on the confirm sheet, based on what the code repositories already do (Observed) where possible. Record them only once confirmed.

**Also writes:** with permission, a pointer section appended to `AGENTS.md` and `CLAUDE.md` at the root of each code repository the agents work in; and, if product-00 hasn't done it, `<docs path>/.pdlc/pdlc.py` (a copy of this skill's `scripts/pdlc.py`) and the CI workflow from `references/ci-pdlc-lint.yml`.

{{CORE}}

## Upstream files
`product/00-product-context.md` (product card, docs path, statuses, version scheme, approvers); `tracker.yaml`. If the product context doesn't exist yet, record that product-00-product-context is the product team's first step, and continue with the engineering questions.

## Questionnaire

**Step 1: Code and codebase**
1. Which code repositories belong to this product (and is it a monorepo)? Where do its docs live, if not in one of them? I'll read them read-only to record what already exists, and draft a **repo map** (module, purpose, entry points, owner) for goal-directed reading.
2. Existing architecture notes, diagrams, or ADRs: where in the docs location? Anything outside it should be added there so dev-01-tech-design and later steps can use it.

**Step 2: Environments**
3. Which environments (for example dev, stage, prod)? For each: name, role (local development, pre-production, or production), purpose, URL or "not created yet", and who may deploy to it.

**Step 3: Git conventions**
4. Git host and branching convention, or should I propose options?
5. Commit message convention (for example including the story or task ID), or should I propose options?
6. Pull requests: required or not, who reviews, who may merge, required checks.
6a. **Review tiers.** Which change areas always get a line-by-line human review? Default: authentication and permissions, money, personal data, data deletion, migrations, cryptography and secrets. Everything else is reviewed through the specification, the tests, and the footprint (conventions [Specification review and tests first]).
6b. **Change budget.** The overrun threshold above which a build must explain itself (for example a percentage over the plan's estimate), or none. Team-set; never proposed as a number.
6c. **Specification reviewers.** Who signs the specification review for a scope (architecture, criteria, constraints, tests)?

**Step 4: Coding agents**
7. Which coding agents do you use (Claude Code, Cursor, other)? May I add a short pointer to the docs in `AGENTS.md` (read by Cursor and other agents) and `CLAUDE.md` (read by Claude Code)?
7a. **Sandbox.** Where do agents build: a separate working copy (git worktree), a branch in a container, a cloud sandbox? Default: a separate worktree or branch per story, with no production credentials or production data, and only the environments marked local development.

**Step 5: Delivery and access**
8. CI/CD already in place (provider, what runs), or none yet? (Set up or changed by dev-06-deploy in Setup mode.)
9. Secrets manager and how local configuration is shared, or "none yet".
10. Local setup: what a developer needs to run the product locally (access, seed data, services), or Open.

**Step 6: People**
11. Development team: who approves tech designs, data models, build plans, and production deploys?
12. Who raises and follows up queries to product? (The product contact is in the product context.)

## Output: `dev/00-dev-setup.md`

```markdown
(header: pdlc_step "D00", scope product)
# [Product]: Development setup

## 1. Engineering card
| Field | Value | Label |
Repositories, monorepo or not, docs path (from the product context), people and approvers.

## 2. Codebase snapshot (existing code only)
Observed, read-only: languages, frameworks, package manager, folder layout, main modules and where they live, tests, CI, environment config. Nothing changed.

**Repo map** (used for goal-directed reading; kept current by D04 when it adds or moves a module):
| Repository | Module or path | Purpose | Entry points | Example file for its pattern | Label |

## 3. Environments
| Environment | Role (local development / pre-production / production) | Purpose | URL | Who deploys | Created? | Label |

## 4. Conventions
| Convention | Value | Label |
Branch naming, commit format, pull request and review rules, merge rights, required checks, review tiers (line-by-line areas), change-budget threshold, specification reviewers, agent sandbox.

## 5. Coding agents
| Agent | Where it reads instructions | Pointer added? |

## 6. Delivery and access
CI/CD in place, secrets handling, local setup steps or Open.

## 7. Team, approvals, and queries
| Role | Person | Approves or handles |

## 8. Open items
## Change log
```

**Agent pointer.** Only with permission, append (never overwrite) this to `AGENTS.md` and `CLAUDE.md` at the root of each code repository the agents work in:

```markdown
## Product and development docs (PDLC)
This product's docs location: [repository or store, branch, folder, as recorded in dev-00].
Requirements handed off by the product team live in [docs path]/product/ (read-only for development).
Development docs live in [docs path]/dev/; the shared tracker is [docs path]/tracker.yaml (view: tracker.md, generated).
Before planning or coding, read [docs path]/dev/00-dev-setup.md, [docs path]/dev/architecture.md,
and the 03-tasks file for your scope under [docs path]/dev/<initiative folder>/.
Build with the dev-04-code-plan-build skill: plan first, wait for approval, then implement.
Questions about product behavior go to the queries in [docs path]/tracker.yaml; never edit product docs.
After changing docs or task status, run: python [docs path]/.pdlc/pdlc.py lint --fix --root [docs path], then board.
```

Fill the bracketed values from the docs location and docs path actually recorded for this product.

## Tracker
No items are created here. Run `lint` and `board` once the file is written, so the setup is checked. Next: dev-01-tech-design, in Baseline mode if `dev/architecture.md` doesn't exist, otherwise for the first handed-off initiative.
