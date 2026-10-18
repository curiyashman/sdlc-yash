# PDLC skills: Product, Design, Development, QA, Deployment, and Security

**39** Agent Skills for a team that builds one or more products. The skills take an idea through requirements, design, build, developer tests, optional independent QA, release/ops, optional security audit, and launch — with a shared tracker and a script that keeps the chain consistent.

- **Product** (`product-00` to `07`) turns ideas for new features, or expansions of existing ones, into requirements and user stories. It also owns change requests, the tracker, and the launch kit.
- **Design** (`design-00` to `04`, optional via `design_stage`) turns approved stories into Figma mockups or an HTML prototype, and can audit/create a design system (G04).
- **Development** (`dev-00` to `07`) builds, runs developer-level tests, and (when optional stages are off) also owns product QA Go and deploy/incidents. It handles maintenance (hotfixes, tech debt, upgrades, spikes, chores).
- **QA** (`qa-00` to `04`, optional via `qa_stage`) independently checks the product against requirements and issues the release Go / No-go.
- **Deployment** (`deploy-00` to `05`, optional via `deploy_stage`) owns environments, pipelines, releases, observability, and incidents.
- **Security** (`sec-00` to `05`, optional via `security_stage`) independently scopes, attacks, audits, reports, and retests — isolated from other teams' docs.
- **pdlc-next** (in `Common/`) is the shared entry point. It answers "what next", "where are we", and "what is open" for any team.

**Default for small teams:** leave `qa_stage`, `deploy_stage`, and `security_stage` false. Development keeps D05 (including release Go) and D06 (release/incidents). Turn a stage on only when that team exists.

Every skill proposes answers for the person to confirm and assumes nothing. Each fact is labeled Provided, Observed, Reference, Default, Recommendation, or Open. Each run delivers one `.md` file.

## How it fits together

- **Team boundary.** Product decides what; Design decides how it looks; Development decides how it is built (and tests at developer level); QA decides whether it meets requirements; Deployment decides how it is released and run; Security decides how safe it is from outside. Each team writes only in its own folder (`product/`, `design/`, `dev/`, `qa/`, `deploy/`, `security/`), plus the shared `tracker.yaml` and `decisions/`.
- **Stage flags** in `tracker.yaml` `config`: `design_stage`, `qa_stage`, `deploy_stage`, `security_stage` (default off unless the matching setup file is approved). Do not run both the Dev compat path and the staged path for the same release.
- **Requirements are the single source of truth.** Every initiative covers its full scope; no MVP slicing is applied by default. Order comes only from dependencies, and timelines, priorities, and estimates belong to the team.
- **Reference by ID, don't copy.** Each kind of fact has one owner file:

  | Fact | IDs | Owner |
  |---|---|---|
  | Requirements and rules | FR, BR, NFR | PRD |
  | Behavior | US, EC, AC | stories |
  | Screens and flows | SC, FL | UX |
  | Technical choices | L1 to L13, DEC | architecture |
  | Tasks | T, ST | task file |
  | Tests | TC | Dev QA file and/or independent QA plan |

  Every later file cites the ID. The lint script checks that every cited ID exists.
- **The handoff.** With a design stage, product approval moves a scope's stories to *in design*, and the design handoff (design-03) makes them *ready for dev*. Without one, product approval makes them ready for dev directly. Other teams never guess: gaps become queries in `tracker.yaml`, and only `product-05-change-request` changes an approved requirement (with a mandatory impact-area audit).
- **Closed loop with design.** Each story gets a design-references block with its frames or prototype pages. The UX inventory and the sitemap get links too. Lint reports handed-off stories with missing or stale references.
- **Requirements in EARS.** Functional requirements, business rules, NFRs, task build lines, and agent rules are single EARS sentences ("When [trigger], the [system] shall [response]."). Lint rejects requirement rows that aren't. Acceptance criteria stay Given/When/Then, and each one names the requirement it verifies.
- **Specification first, then sandboxed build.** For each scope, development designs developer-level tests before any code (dev-05, test design). It then signs a specification review in dev-03. Only after that does the coding agent build, in an isolated sandbox, until the approved (and locked) tests pass. When `qa_stage` is on, independent QA owns system/E2E tests and the release Go (qa-03), not D05.
- **Lean code.** Agents read code by stated goal (a read map), search before writing (a reuse map), copy the example file for each pattern (named in `architecture.md`), stay within each task's change budget, write nothing no requirement needs, delete what they replace, and write no test without a test-case ID.
- **Per product.** The skills name no repository. Each product records its own docs location (repository, branch, folder) and code repositories. Every run first settles which product it is for.

## The tracker is data, kept honest by a script

`tracker.yaml` holds initiatives, scopes, items, queries, versions, and change requests. `tracker.md` is generated from it and never edited by hand. Tasks and sub-tasks live in a `pdlc-tasks` YAML block in each scope's task file, so the tracker stays small.

`tools/pdlc.py` (Python 3; PyYAML optional) is bundled in every skill as `scripts/pdlc.py`:

| Command | What it does |
|---|---|
| `lint [--fix]` | Checks EARS requirement rows, test cases mapped to criteria, the test-design and specification-review gates, headers, stale upstream files (MAJOR or MINOR moves), ID format, parents and duplicates, every cited ID, dependency cycles, and dependency levels (`--fix` writes them in place, keeping the file's layout). Also checks query rules, the ready-for-dev and design-handoff rules, design references, and uncommitted files. |
| `board` | Regenerates `tracker.md`: summary, initiative board (derived from file headers), what next, open items and queries, blocked, stale, items by dependency level, versions, change requests. Shows design/qa/deploy/security stage on/off. |
| `next [--team product\|design\|dev\|qa\|deploy\|security]` | The exact skill and scope to run next for each team, by dependency level. Optional teams appear when their stage is on or they have work waiting. |
| `new-id KIND [PARENT]` | The next free ID: initiative, module, sub-module, feature, story, task, subtask, fr, br, nfr, ec, ac, ev, sc, fl, tc, bug, query, cr, dec, hf, td, upg, spk, or chr. |
| `open` | Every Open item and query in one view. |

Every step ends by running `lint --fix` and `board`. Where scripts can't run (for example a Claude project without code execution), the skill does the checks by reading and says "not linted". The CI check in the product's repository (`references/ci-pdlc-lint.yml`) catches the rest.

## Skills

### Common
| Skill | Use for |
|---|---|
| [pdlc-next](Common/pdlc-next/SKILL.md) | what next, where are we, what is open, blocked, or stale, lint the docs |

### Product (`Product/`)
| Step | Skill | Works on | Output (under the docs path) |
|---|---|---|---|
| P00 | [product-00-product-context](Product/product-00-product-context/SKILL.md) | product | `product/00-product-context.md`, `tracker.yaml` |
| P01 | [product-01-feature-brainstorm](Product/product-01-feature-brainstorm/SKILL.md) | one initiative | `product/I-<nnn>-<slug>/01-brainstorm.md` |
| P02 | [product-02-prd](Product/product-02-prd/SKILL.md) | one initiative | `product/I-<nnn>-<slug>/02-prd.md` |
| P03 | [product-03-ux-flows](Product/product-03-ux-flows/SKILL.md) | one scope | `product/I-<nnn>-<slug>/03-ux/<scope>.md`, `product/_sitemap.md` |
| P04 | [product-04-user-stories](Product/product-04-user-stories/SKILL.md) | one scope | `product/I-<nnn>-<slug>/04-stories/<scope>.md` |
| P05 | [product-05-change-request](Product/product-05-change-request/SKILL.md) | any time | `product/change-requests/CR-<nnn>.md` (mandatory impact-area audit) |
| P06 | [product-06-project-tracker](Product/product-06-project-tracker/SKILL.md) | any time | `tracker.yaml`: statuses, versions, queries, reports, exports |
| P07 | [product-07-launch](Product/product-07-launch/SKILL.md) | one released version | `product/launch/<version>.md` |

### Design (`Design/`, optional — `config.design_stage`)
| Step | Skill | Works on | Output |
|---|---|---|---|
| G00 | [design-00-design-setup](Design/design-00-design-setup/SKILL.md) | product | `design/00-design-setup.md` (Figma capability, or HTML prototype as the medium) |
| G01 | [design-01-sitemap-flows](Design/design-01-sitemap-flows/SKILL.md) | one initiative | `design/I-<nnn>-<slug>/01-sitemap-flows.md` + FigJam charts |
| G02 | [design-02-screen-mockups](Design/design-02-screen-mockups/SKILL.md) | one scope | `design/I-<nnn>-<slug>/02-mockups/<scope>.md` + Figma frames or HTML prototype |
| G03 | [design-03-design-handoff](Design/design-03-design-handoff/SKILL.md) | one scope | `design/I-<nnn>-<slug>/03-handoff/<scope>.md` (the design handoff) |
| G04 | [design-04-design-system](Design/design-04-design-system/SKILL.md) | product (optional) | `design/04-design-system.md`, then `design/system/` |

### Development (`Development/`)
| Step | Skill | Works on | Output |
|---|---|---|---|
| D00 | [dev-00-dev-setup](Development/dev-00-dev-setup/SKILL.md) | product | `dev/00-dev-setup.md`, lint script and CI |
| D01 | [dev-01-tech-design](Development/dev-01-tech-design/SKILL.md) | baseline, then one initiative | `dev/architecture.md`; `dev/I-<nnn>-<slug>/01-tech-design.md` (13 layers + threat model) |
| D02 | [dev-02-data-model](Development/dev-02-data-model/SKILL.md) | one handed-off scope | `dev/I-<nnn>-<slug>/02-data-model/<scope>.md` |
| D03 | [dev-03-build-tasks](Development/dev-03-build-tasks/SKILL.md) | one handed-off scope | `dev/I-<nnn>-<slug>/03-tasks/<scope>.md` (`pdlc-tasks` blocks, agent brief, specification review) |
| D04 | [dev-04-code-plan-build](Development/dev-04-code-plan-build/SKILL.md) | one story, bug, or maintenance item | plan (read map, reuse map, budget) + code built in a sandbox until the locked tests pass |
| D05 | [dev-05-test-qa](Development/dev-05-test-qa/SKILL.md) | scope or version | developer tests first; product QA / release Go only when `qa_stage` is off |
| D06 | [dev-06-deploy](Development/dev-06-deploy/SKILL.md) | version or event | release/incident when `deploy_stage` is off; otherwise use Deployment |
| D07 | [dev-07-maintenance](Development/dev-07-maintenance/SKILL.md) | one maintenance item | `dev/maintenance/<id>.md` (HF, TD, UPG, SPK, CHR) |

### QA (`QA/`, optional — `config.qa_stage`)
| Step | Skill | Works on | Output |
|---|---|---|---|
| Q00 | [qa-00-qa-setup](QA/qa-00-qa-setup/SKILL.md) | product | `qa/00-qa-setup.md` |
| Q01 | [qa-01-test-plan](QA/qa-01-test-plan/SKILL.md) | one scope | `qa/I-*/01-test-plan/<scope>.md` |
| Q02 | [qa-02-test-execution](QA/qa-02-test-execution/SKILL.md) | one scope | `qa/I-*/02-results/<scope>.md` |
| Q03 | [qa-03-release-signoff](QA/qa-03-release-signoff/SKILL.md) | one version | `qa/releases/<version>-signoff.md` (release Go) |
| Q04 | [qa-04-nonfunctional-testing](QA/qa-04-nonfunctional-testing/SKILL.md) | as needed | `qa/nfr/<slug>.md` |

### Deployment (`Deployment/`, optional — `config.deploy_stage`)
| Step | Skill | Works on | Output |
|---|---|---|---|
| O00 | [deploy-00-deploy-setup](Deployment/deploy-00-deploy-setup/SKILL.md) | product | `deploy/00-deploy-setup.md` |
| O01 | [deploy-01-environments](Deployment/deploy-01-environments/SKILL.md) | product | `deploy/01-environments.md` |
| O02 | [deploy-02-pipeline](Deployment/deploy-02-pipeline/SKILL.md) | product | `deploy/02-pipeline.md` |
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
1. **Setup:** Product runs `product-00` once. Optional stages: Design (`design-00`, then `design-04` if needed), QA (`qa-00`), Deployment (`deploy-00`), Security (engagement via `sec-00`). Development runs `dev-00` and the `dev-01` baseline once.
2. **Per idea:** `product-01`, then `product-02` for the initiative's PRD.
3. **Per scope**, lowest dependency level first:
   - Product: `product-03`, then `product-04`.
   - Design (if on): `design-01`, then `design-02` and `design-03`.
   - Development: `dev-01` → `dev-02` → `dev-05` (test design) → `dev-03` → `dev-04` → `dev-05` (developer results).
   - QA (if on): `qa-01` can start after stories are approved; `qa-02` when stories are `in_qa`.
4. **Release:**
   - Stages off: `dev-06` → `dev-05` version Go → `dev-06` promote → `product-07`.
   - Stages on: `deploy-03` stage → `qa-03` Go (+ `sec-05` if Security on) → `deploy-03` promote → `product-07`.
5. **Any time:** `pdlc-next`, `product-05`, `dev-07`, incidents via `deploy-05` or `dev-06`.

## Install
```bash
git clone https://github.com/curiyashman/sdlc-yash.git
cd sdlc-yash
# Cursor / Claude Code (user skills)
cp -r Common/* ~/.claude/skills/              # everyone (pdlc-next)
cp -r Product/product-* ~/.claude/skills/     # product team
cp -r Design/design-* ~/.claude/skills/       # design team
cp -r Development/dev-* ~/.claude/skills/     # development team
cp -r QA/qa-* ~/.claude/skills/               # if using QA stage
cp -r Deployment/deploy-* ~/.claude/skills/   # if using Deployment stage
cp -r Security/sec-* ~/.claude/skills/        # if using Security stage
# Or for one Cursor project only:
# mkdir -p .cursor/skills && cp -r Common/* Product/product-* Design/design-* Development/dev-* QA/qa-* Deployment/deploy-* Security/sec-* .cursor/skills/
```
- `~/.claude/skills/` is read by Claude Code, and also by Cursor (all projects). `<repo>/.claude/skills/` covers one project only; Cursor also reads `.cursor/skills/`.
- **Claude projects (product team):** add the Product skills and `pdlc-next`. Fill in [`Product/claude-project-instructions.md`](Product/claude-project-instructions.md).
- **Design / QA / Deployment / Security:** add that team's skills + `pdlc-next`, and the matching [`Design/agent-instructions.md`](Design/agent-instructions.md), [`QA/agent-instructions.md`](QA/agent-instructions.md), [`Deployment/agent-instructions.md`](Deployment/agent-instructions.md), or [`Security/agent-instructions.md`](Security/agent-instructions.md).
- **Coding agents (development team):** fill in [`Development/agent-instructions.md`](Development/agent-instructions.md) in `CLAUDE.md` / `AGENTS.md`. Or let `dev-00-dev-setup` add its pointer, lint script, and CI.
- **Remove older competing skills** where installed: `pdlc-00` to `pdlc-12`, workflow-architect, fullstack-architect, research-driven-prd, prd-to-ux-ui, requirements-to-stories, product-brainstorm, devops-sre-expert, schema-design-interview, design-system-architect / design-system-spec (use G04).

## Editing the skills
Never edit the generated folders (`Common/`, `Product/`, `Design/`, `Development/`, `QA/`, `Deployment/`, `Security/`). Edit `source/` and rebuild:

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
python source/build.py            # rebuild the skill folders
python source/build.py --check    # what CI runs: fails if the folders are out of date
python -m unittest discover tests # script tests against examples/sample-product
```

`examples/sample-product/` is a small fictional product (Ledgerly) run through the Product/Design/Development path. It is the test fixture for the script and a worked example of the files, the header, `tracker.yaml`, the task blocks, the design references, and a DEC.

## Contributing

This is a **public, maintainer-gated** repo. Forks and pull requests are possible because the repo is public; merges are not open to everyone.

- Direct pushes to `main` are blocked.
- Every PR needs an approving review from a [CODEOWNER](.github/CODEOWNERS) before merge.
- Open an issue (or ask first) before large changes. Unsolicited PRs may be closed.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full rules.
