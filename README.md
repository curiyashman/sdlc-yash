# PDLC skills: Product, Design, Development, QA, Deployment, and Security

**39** Agent Skills for a team that builds one or more products. The skills take an idea through requirements, design, build, developer tests, optional independent QA, release/ops, optional security audit, and launch — with a shared tracker and a script that keeps the chain consistent.

- **Product** (`product-00` to `07`) turns ideas for new features, or expansions of existing ones, into requirements and user stories. It also owns change requests, the tracker, and the launch kit. Sets `product_mode` (`greenfield` | `brownfield`).
- **Design** (`design-00` to `04`, optional via `design_stage`) turns approved stories into Figma mockups or an HTML prototype, and can audit/create a design system (G04). Foundations (tokens, core atoms, page shells) gate story-level screens when required.
- **Development** (`dev-00` to `07`) builds, runs developer-level tests, dependency audit (Layer 1), and (when optional stages are off) also owns product QA Go and deploy/incidents. It handles maintenance (hotfixes, tech debt, upgrades, spikes, chores).
- **QA** (`qa-00` to `04`, optional via `qa_stage`) independently checks the product against requirements, including a thin **design parity smoke** when design stage is on, and issues the release Go / No-go.
- **Deployment** (`deploy-00` to `05`, optional via `deploy_stage`) owns environments, pipelines, releases, observability, and incidents (one process path; platform details live in reference packs).
- **Security** (`sec-00` to `05`, optional via `security_stage`) independently scopes, attacks, audits, reports, and retests — isolated from other teams' docs. Leave off for day-to-day work; use for engagements.
- **pdlc-next** (in `Common/`) is the shared entry point. It answers "what next", "where are we", and "what is open" for any team.

**Default for small teams:** leave `qa_stage`, `deploy_stage`, and `security_stage` false. Development keeps D05 (including release Go) and D06 (release/incidents), plus Layer 1 dependency audit. Turn Design on when you have UI; turn other stages on only when that team exists.

Every skill proposes answers for the person to confirm and assumes nothing. Each fact is labeled Provided, Observed, Reference, Default, Recommendation, or Open. Each run delivers one `.md` file. Prefer **cite by ID, don't copy** — thin tables over restated PRD text.

## How it fits together

- **Team boundary.** Product decides what; Design decides how it looks; Development decides how it is built (and tests at developer level); QA decides whether it meets requirements; Deployment decides how it is released and run; Security decides how safe it is from outside. Each team writes only in its own folder (`product/`, `design/`, `dev/`, `qa/`, `deploy/`, `security/`), plus the shared `tracker.yaml` and `decisions/`.
- **Stage flags** in `tracker.yaml` `config`:
  | Flag | Role |
  |---|---|
  | `product_mode` | `greenfield` \| `brownfield` (P00) |
  | `design_stage` | Design team G00–G04 |
  | `design_system` | `planned` \| `adopt` \| `refine` \| `create` \| `none` |
  | `design_system_foundation` | `pending` \| `approved` — Phase 0 before story G02 when system is planned/create/refine |
  | `qa_stage` / `deploy_stage` / `security_stage` | Independent teams when true |

  Do not run both the Dev compat path and the staged path for the same release.
- **Requirements are the single source of truth.** Every initiative covers its full scope; no MVP slicing is applied by default. Order comes only from dependencies (stories drafted Level 0 → N). Timelines, priorities, and estimates belong to the team. Lint blocks `ready_for_dev`+ when upstream stories are not yet handed off.
- **Reference by ID, don't copy.** Each kind of fact has one owner file:

  | Fact | IDs | Owner |
  |---|---|---|
  | Requirements and rules | FR, BR, NFR | PRD |
  | Behavior | US, EC, AC | stories |
  | Screens and flows | SC, FL | UX |
  | Technical choices | L1 to L13, DEC | architecture |
  | Tasks | T, ST | task file |
  | Tests | TC | Dev QA file and/or independent QA plan |

  Every later file cites the ID. The lint script checks that every cited ID exists. Brownfield stories include a **Delta** (what changes vs unchanged AC IDs).
- **The handoff package.** Build from stories + cited PRD/UX — and, with design stage, approved G03 + design-refs frames — not from parallel doc trees alone. With a design stage, product approval moves stories to *in design*; G03 makes them *ready for dev*. Without one, product approval makes them ready for dev directly. Gaps become queries in `tracker.yaml`; only `product-05-change-request` changes an approved requirement.
- **Closed loop with design.** Each story gets a design-references block. UI tasks (D03) cite frame + state; D04 plans include a Frame checklist and a design parity note before `in_qa`. QA runs a thin design parity smoke (not a second G03). Lint reports handed-off stories with missing or stale references.
- **Design foundations first.** When `design_system` is planned/create/refine, finish G04 Phase 0 (foundations, core atoms, page shells) and set `design_system_foundation: approved` before story-level G02. Adopt/none do not block G02.
- **Requirements in EARS.** Functional requirements, business rules, NFRs, task build lines, and agent rules are single EARS sentences. Lint rejects requirement rows that aren't. Acceptance criteria stay Given/When/Then, and each one names the requirement it verifies.
- **Specification first, then sandboxed build.** For each scope: developer-level tests before code (dev-05, test design) → specification review (dev-03) → coding agent builds in a sandbox until locked tests pass (dev-04), including **dependency audit** (npm audit / pip-audit / equivalent from D00). When `qa_stage` is on, independent QA owns system/E2E and the release Go (qa-03).
- **Lean code.** Agents read by stated goal (read map), search before writing (reuse map), copy the example file for each pattern, stay within each task's change budget, write nothing no requirement needs, delete what they replace, and write no test without a test-case ID.
- **Layer 1 security (always on).** Dependency audit while developing and in CI. Full Security engagements (S00–S05) stay optional via `security_stage`.
- **Per product.** The skills name no repository. Each product records its own docs location and code repositories. Every run first settles which product it is for.

## The tracker is data, kept honest by a script

`tracker.yaml` holds initiatives, scopes, items, queries, versions, and change requests. `tracker.md` is generated from it and never edited by hand. Tasks and sub-tasks live in a `pdlc-tasks` YAML block in each scope's task file, so the tracker stays small.

`tools/pdlc.py` (Python 3; PyYAML optional) is bundled in every skill as `scripts/pdlc.py`:

| Command | What it does |
|---|---|
| `lint [--fix]` | Checks EARS rows, TC→criteria mapping, test-design and specification-review gates, headers, stale upstream files, IDs, citations, dependency cycles/levels, query rules, ready-for-dev and design-handoff rules, design references, **upstream-ready story deps**, and the **design foundation gate**. `--fix` writes dep levels. |
| `board` | Regenerates `tracker.md`: summary, initiative board, what next, open items and queries, blocked, stale, items by dependency level, versions, change requests. Shows stage flags. |
| `next [--team product\|design\|dev\|qa\|deploy\|security]` | The exact skill and scope to run next for each team, by dependency level (including foundation-before-G02 when the gate applies). |
| `new-id KIND [PARENT]` | The next free ID: initiative, module, sub-module, feature, story, task, subtask, fr, br, nfr, ec, ac, ev, sc, fl, tc, bug, query, cr, dec, hf, td, upg, spk, or chr. |
| `open` | Every Open item and query in one view. |

Every step ends by running `lint --fix` and `board`. Where scripts can't run, the skill does the checks by reading and says "not linted". The CI check in the product's repository (`references/ci-pdlc-lint.yml`) catches the rest.

## Skills

### Common
| Skill | Use for |
|---|---|
| [pdlc-next](Common/pdlc-next/SKILL.md) | what next, where are we, what is open, blocked, or stale, lint the docs |

### Product (`Product/`)
| Step | Skill | Works on | Output (under the docs path) |
|---|---|---|---|
| P00 | [product-00-product-context](Product/product-00-product-context/SKILL.md) | product | `product/00-product-context.md`, `tracker.yaml` (`product_mode`) |
| P01 | [product-01-feature-brainstorm](Product/product-01-feature-brainstorm/SKILL.md) | one initiative | `product/I-<nnn>-<slug>/01-brainstorm.md` |
| P02 | [product-02-prd](Product/product-02-prd/SKILL.md) | one initiative | `product/I-<nnn>-<slug>/02-prd.md` |
| P03 | [product-03-ux-flows](Product/product-03-ux-flows/SKILL.md) | one scope | `product/I-<nnn>-<slug>/03-ux/<scope>.md`, `product/_sitemap.md` |
| P04 | [product-04-user-stories](Product/product-04-user-stories/SKILL.md) | one scope | `product/I-<nnn>-<slug>/04-stories/<scope>.md` (Level 0→N; brownfield Delta) |
| P05 | [product-05-change-request](Product/product-05-change-request/SKILL.md) | any time | `product/change-requests/CR-<nnn>.md` (mandatory impact-area audit) |
| P06 | [product-06-project-tracker](Product/product-06-project-tracker/SKILL.md) | any time | `tracker.yaml`: statuses, versions, queries, reports, exports |
| P07 | [product-07-launch](Product/product-07-launch/SKILL.md) | one released version | `product/launch/<version>.md` |

### Design (`Design/`, optional — `config.design_stage`)
| Step | Skill | Works on | Output |
|---|---|---|---|
| G00 | [design-00-design-setup](Design/design-00-design-setup/SKILL.md) | product | `design/00-design-setup.md` (Figma capability, or HTML prototype as the medium) |
| G01 | [design-01-sitemap-flows](Design/design-01-sitemap-flows/SKILL.md) | one initiative | `design/I-<nnn>-<slug>/01-sitemap-flows.md` + FigJam charts |
| G02 | [design-02-screen-mockups](Design/design-02-screen-mockups/SKILL.md) | one scope | `design/I-<nnn>-<slug>/02-mockups/<scope>.md` + frames (after foundation gate when it applies) |
| G03 | [design-03-design-handoff](Design/design-03-design-handoff/SKILL.md) | one scope | `design/I-<nnn>-<slug>/03-handoff/<scope>.md` |
| G04 | [design-04-design-system](Design/design-04-design-system/SKILL.md) | product | `design/04-design-system.md`, then `design/system/` (Phase 0 foundations first when Create/Refine) |

### Development (`Development/`)
| Step | Skill | Works on | Output |
|---|---|---|---|
| D00 | [dev-00-dev-setup](Development/dev-00-dev-setup/SKILL.md) | product | `dev/00-dev-setup.md` (incl. dependency-audit command), lint script and CI |
| D01 | [dev-01-tech-design](Development/dev-01-tech-design/SKILL.md) | baseline, then one initiative | `dev/architecture.md`; `dev/I-<nnn>-<slug>/01-tech-design.md` |
| D02 | [dev-02-data-model](Development/dev-02-data-model/SKILL.md) | one handed-off scope | `dev/I-<nnn>-<slug>/02-data-model/<scope>.md` |
| D03 | [dev-03-build-tasks](Development/dev-03-build-tasks/SKILL.md) | one handed-off scope | `dev/I-<nnn>-<slug>/03-tasks/<scope>.md` (UI tasks cite frame + state; vertical slice) |
| D04 | [dev-04-code-plan-build](Development/dev-04-code-plan-build/SKILL.md) | one story, bug, or maintenance item | plan (Frame checklist, dependency audit, design parity) + sandboxed build |
| D05 | [dev-05-test-qa](Development/dev-05-test-qa/SKILL.md) | scope or version | developer tests first; product QA / design parity smoke / release Go when `qa_stage` is off |
| D06 | [dev-06-deploy](Development/dev-06-deploy/SKILL.md) | version or event | release/incident when `deploy_stage` is off; otherwise use Deployment |
| D07 | [dev-07-maintenance](Development/dev-07-maintenance/SKILL.md) | one maintenance item | `dev/maintenance/<id>.md` (HF, TD, UPG from audits, SPK, CHR) |

### QA (`QA/`, optional — `config.qa_stage`)
| Step | Skill | Works on | Output |
|---|---|---|---|
| Q00 | [qa-00-qa-setup](QA/qa-00-qa-setup/SKILL.md) | product | `qa/00-qa-setup.md` |
| Q01 | [qa-01-test-plan](QA/qa-01-test-plan/SKILL.md) | one scope | `qa/I-*/01-test-plan/<scope>.md` (incl. design parity smoke TCs when design on) |
| Q02 | [qa-02-test-execution](QA/qa-02-test-execution/SKILL.md) | one scope | `qa/I-*/02-results/<scope>.md` |
| Q03 | [qa-03-release-signoff](QA/qa-03-release-signoff/SKILL.md) | one version | `qa/releases/<version>-signoff.md` (release Go) |
| Q04 | [qa-04-nonfunctional-testing](QA/qa-04-nonfunctional-testing/SKILL.md) | as needed | `qa/nfr/<slug>.md` |

### Deployment (`Deployment/`, optional — `config.deploy_stage`)
| Step | Skill | Works on | Output |
|---|---|---|---|
| O00 | [deploy-00-deploy-setup](Deployment/deploy-00-deploy-setup/SKILL.md) | product | `deploy/00-deploy-setup.md` |
| O01 | [deploy-01-environments](Deployment/deploy-01-environments/SKILL.md) | product | `deploy/01-environments.md` |
| O02 | [deploy-02-pipeline](Deployment/deploy-02-pipeline/SKILL.md) | product | `deploy/02-pipeline.md` (Layer 1 dependency audit in CI) |
| O03 | [deploy-03-release](Deployment/deploy-03-release/SKILL.md) | one version | `deploy/releases/<version>.md` |
| O04 | [deploy-04-observability-sre](Deployment/deploy-04-observability-sre/SKILL.md) | product | `deploy/04-observability-sre.md` |
| O05 | [deploy-05-incident-response](Deployment/deploy-05-incident-response/SKILL.md) | incident | `deploy/incidents/…` |

### Security (`Security/`, optional — `config.security_stage`)
| Step | Skill | Works on | Output |
|---|---|---|---|
| S00 | [sec-00-engagement-scope](Security/sec-00-engagement-scope/SKILL.md) | engagement | `security/<engagement>/00-engagement.md` |
| S01 | [sec-01-attack-surface](Security/sec-01-attack-surface/SKILL.md) | engagement | `security/<engagement>/01-attack-surface.md` |
| S02 | [sec-02-vulnerability-assessment](Security/sec-02-vulnerability-assessment/SKILL.md) | engagement | `security/<engagement>/02-vulnerabilities.md` |
| S03 | [sec-03-privacy-compliance-audit](Security/sec-03-privacy-compliance-audit/SKILL.md) | engagement | `security/<engagement>/03-privacy-compliance.md` |
| S04 | [sec-04-audit-report-remediation](Security/sec-04-audit-report-remediation/SKILL.md) | engagement | `security/<engagement>/04-report.md` |
| S05 | [sec-05-retest-signoff](Security/sec-05-retest-signoff/SKILL.md) | engagement / version | `security/<engagement>/05-retest-signoff.md` (Security Go) |

Security skills use an isolated core (`source/core-security.md`): findings come from authorized systems and code, not from reading `product/` / `design/` / `dev/` / `qa/` / `deploy/` docs.

**Decision log.** Any step that makes a decision of record writes `decisions/DEC-<nnn>-<slug>.md`. Examples: a scope cut, an architecture choice, a change-request outcome, or a spike's result. Files cite the DEC instead of repeating its reasoning.

**Reference packs**, bundled only in the skills that use them and read only when they apply:
- **`compliance.md`:** checklists for personal data, India's DPDP Act, GDPR, PCI DSS, RBI payments, GST invoicing, communications, and accessibility. These are questions to verify against current official sources, never legal facts.
- **`threat-model.md`:** STRIDE per data flow, used by dev-01.
- **`ai-features.md`:** eval sets owned by Product, prompt and model versioning, guardrails, budgets, eval runs in QA, and monitoring.
- **`secure-by-design.md`:** security considerations for every non-Security team skill (except `pdlc-next`).
- **`qa-techniques.md`**, **`deploy-platforms.md`**, **`deploy-methods.md`**, **`observability-sre.md`**, **`security-methodology.md`**, **`security-jurisdictions.md`:** team-specific packs.
- **`design-system-references.md`**, **`responsive-platforms.md`:** Design / G04 and responsive QA.

## Typical flow
1. **Setup:** Product runs `product-00` once (`product_mode`). Optional: Design (`design-00`, then G04 Phase 0 when needed), QA (`qa-00`), Deployment (`deploy-00`), Security (engagement via `sec-00`). Development runs `dev-00` (record dependency-audit command) and the `dev-01` baseline once.
2. **Per idea:** `product-01`, then `product-02` for the initiative's PRD.
3. **Per scope**, lowest dependency level first:
   - Product: `product-03`, then `product-04` (Level 0→N; brownfield Delta).
   - Design (if on): foundation gate clear → `design-01` → `design-02` → `design-03`.
   - Development: `dev-01` → `dev-02` → `dev-05` (test design) → `dev-03` → `dev-04` (Frame checklist, audit, design parity) → `dev-05` (developer results).
   - QA (if on): `qa-01` after stories approved (incl. design parity smoke TCs); `qa-02` when stories are `in_qa`.
4. **Release:**
   - Stages off: `dev-06` → `dev-05` version Go → `dev-06` promote → `product-07`.
   - Stages on: `deploy-03` stage → `qa-03` Go (+ `sec-05` if Security on) → `deploy-03` promote → `product-07`.
5. **Any time:** `pdlc-next`, `product-05`, `dev-07` (including UPG- from audits), incidents via `deploy-05` or `dev-06`.

## Install (once, at Cursor user root)

Skills are **not** copied into each product repo. Install them once under your Cursor user skills so every product workspace can use them. Each product keeps only its own `docs/pdlc/` (tracker, PRDs, stories, etc.).

```bash
git clone https://github.com/curiyashman/sdlc-yash.git
cd sdlc-yash
python3 source/build.py          # if you edited source/; clone from main is already built
python3 tools/install.py         # → ~/.cursor/skills/  (default: Product + Design + Development + pdlc-next)
python3 tools/install.py --preset full --claude --clean-legacy   # all teams + ~/.claude/skills/
python3 tools/install.py --plugin-local   # also symlink into ~/.cursor/plugins/local/pdlc-skills
```

| Flag | Effect |
|---|---|
| `--preset minimal` | `pdlc-next` + Product + Development |
| `--preset default` | + Design (recommended) |
| `--preset full` | + QA + Deployment + Security |
| `--claude` | also install into `~/.claude/skills/` |
| `--plugin-local` | symlink this repo for Cursor Plugin loading (reload the window after) |
| `--clean-legacy` | remove older competing skill folders from the install targets |
| `--dry-run` | print what would be installed |

**Plugin manifests** (for Cursor Marketplace / Agent Plugins): [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json) and root [`plugin.json`](plugin.json). Logo: [`assets/logo.svg`](assets/logo.svg) (same YP mark as the personal site favicon). Flat skill folders live in [`skills/`](skills/) (generated by `source/build.py`). Submit later at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish).

- **Do not** put these skills in a product's `.cursor/skills/` unless you intentionally pin a fork for that one repo.
- **Claude / Cursor agent instructions** (paste into the product's `CLAUDE.md` / `AGENTS.md`, not into the skills package): [`Product/claude-project-instructions.md`](Product/claude-project-instructions.md), [`Design/agent-instructions.md`](Design/agent-instructions.md), [`Development/agent-instructions.md`](Development/agent-instructions.md), [`QA/agent-instructions.md`](QA/agent-instructions.md), [`Deployment/agent-instructions.md`](Deployment/agent-instructions.md), [`Security/agent-instructions.md`](Security/agent-instructions.md). Or let `dev-00-dev-setup` add the Development pointer, lint script, and CI.

## Editing the skills
Never edit the generated folders (`Common/`, `Product/`, `Design/`, `Development/`, `QA/`, `Deployment/`, `Security/`, `skills/`). Edit `source/` and rebuild. Commit **`skills/`** for the plugin layout; team folders (`Product/`, …) are browse/compat mirrors of the same build — installers use `skills/` or team folders interchangeably:

| File | Holds |
|---|---|
| `source/core.md` | the short core inlined in every non-Security SKILL.md |
| `source/core-security.md` | isolated core inlined in every `sec-*` SKILL.md |
| `source/conventions.md` | the full rules, bundled as `references/conventions.md` |
| `source/skills/<name>.md` | one skill's own content |
| `source/packs/` | the reference packs |
| `source/instructions/` | the project and agent instructions |
| `tools/pdlc.py` | the script |

```bash
python3 source/build.py            # rebuild team folders + skills/
python3 source/build.py --check    # what CI runs: fails if the folders are out of date
python3 -m unittest discover tests # script tests against examples/sample-product
```

`examples/sample-product/` is a small fictional product (Ledgerly) run through the Product/Design/Development path. It is the test fixture for the script and a worked example of the files, the header, `tracker.yaml`, the task blocks, the design references, and a DEC.

## Contributing

This is a **public, maintainer-gated** repo. Forks and pull requests are possible because the repo is public; merges are not open to everyone.

- Direct pushes to `main` are blocked.
- Every PR needs an approving review from a [CODEOWNER](.github/CODEOWNERS) before merge.
- Open an issue (or ask first) before large changes. Unsolicited PRs may be closed.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full rules.
