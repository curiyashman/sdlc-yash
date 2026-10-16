# PDLC skills: Product, Design, and Development

Twenty-one Agent Skills for a team that builds one or more products. The skills take an idea through requirements, design, build, test, release, and launch, with a shared tracker and a script that keeps the chain consistent.

- **Product** (`product-00` to `07`) turns ideas for new features, or expansions of existing ones, into requirements and user stories. It also owns change requests, the tracker, and the launch kit.
- **Design** (`design-00` to `03`, optional) turns approved stories into Figma mockups or an HTML prototype. It writes a reference to every screen back into the stories.
- **Development** (`dev-00` to `07`) builds, tests, and releases what was handed off, and handles maintenance work (hotfixes, tech debt, upgrades, spikes, and chores).
- **pdlc-next** (in `Common/`) is the shared entry point. It answers "what next", "where are we", and "what is open" for any team.

Every skill proposes answers for the person to confirm and assumes nothing. Each fact is labeled Provided, Observed, Reference, Default, Recommendation, or Open. Each run delivers one `.md` file.

## How it fits together

- **Product decides what; Design decides how it looks; Development decides how it is built.** Each team writes only in its own folder (`product/`, `design/`, `dev/`), plus the shared `tracker.yaml` and `decisions/`.
- **Requirements are the single source of truth.** Every initiative covers its full scope; no MVP slicing is applied by default. Order comes only from dependencies, and timelines, priorities, and estimates belong to the team.
- **Reference by ID, don't copy.** Each kind of fact has one owner file:

  | Fact | IDs | Owner |
  |---|---|---|
  | Requirements and rules | FR, BR, NFR | PRD |
  | Behavior | US, EC, AC | stories |
  | Screens and flows | SC, FL | UX |
  | Technical choices | L1 to L13, DEC | architecture |
  | Tasks | T, ST | task file |
  | Tests | TC | QA file |

  Every later file cites the ID. The lint script checks that every cited ID exists.
- **The handoff.** With a design stage, product approval moves a scope's stories to *in design*, and the design handoff (design-03) makes them *ready for dev*. Without one, product approval makes them ready for dev directly. Design and development never guess: gaps become queries in `tracker.yaml`, and only `product-05-change-request` changes an approved requirement.
- **Closed loop with design.** Each story gets a design-references block with its frames or prototype pages. The UX inventory and the sitemap get links too. Lint reports handed-off stories with missing or stale references.
- **Requirements in EARS.** Functional requirements, business rules, NFRs, task build lines, and agent rules are single EARS sentences ("When [trigger], the [system] shall [response]."). Lint rejects requirement rows that aren't. Acceptance criteria stay Given/When/Then, and each one names the requirement it verifies.
- **Specification first, then sandboxed build.** For each scope, development designs the tests before any code (dev-05, test design). It then signs a specification review in dev-03 covering architecture, criteria, constraints, tests, and task budgets. Only after that does the coding agent build, in an isolated sandbox, until the approved (and locked) tests pass. People review the specification, the tests, and the footprint, plus line by line where risk demands it: auth, money, personal data, deletion, migrations, and secrets.
- **Lean code.** Agents read code by stated goal (a read map), search before writing (a reuse map), copy the example file for each pattern (named in `architecture.md`), stay within each task's change budget, write nothing no requirement needs, delete what they replace, and write no test without a test-case ID.
- **Per product.** The skills name no repository. Each product records its own docs location (repository, branch, folder) and code repositories. Every run first settles which product it is for.

## The tracker is data, kept honest by a script

`tracker.yaml` holds initiatives, scopes, items, queries, versions, and change requests. `tracker.md` is generated from it and never edited by hand. Tasks and sub-tasks live in a `pdlc-tasks` YAML block in each scope's task file, so the tracker stays small.

`tools/pdlc.py` (Python 3; PyYAML optional) is bundled in every skill as `scripts/pdlc.py`:

| Command | What it does |
|---|---|
| `lint [--fix]` | Checks EARS requirement rows, test cases mapped to criteria, the test-design and specification-review gates, headers, stale upstream files (MAJOR or MINOR moves), ID format, parents and duplicates, every cited ID, dependency cycles, and dependency levels (`--fix` writes them in place, keeping the file's layout). Also checks query rules, the ready-for-dev and design-handoff rules, design references, and uncommitted files. |
| `board` | Regenerates `tracker.md`: summary, initiative board (derived from file headers), what next, open items and queries, blocked, stale, items by dependency level, versions, change requests. |
| `next [--team product\|design\|dev]` | The exact skill and scope to run next for each team, by dependency level. |
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
| P05 | [product-05-change-request](Product/product-05-change-request/SKILL.md) | any time | `product/change-requests/CR-<nnn>.md` |
| P06 | [product-06-project-tracker](Product/product-06-project-tracker/SKILL.md) | any time | `tracker.yaml`: statuses, versions, queries, reports, exports |
| P07 | [product-07-launch](Product/product-07-launch/SKILL.md) | one released version | `product/launch/<version>.md` |

### Design (`Design/`, optional)
| Step | Skill | Works on | Output |
|---|---|---|---|
| G00 | [design-00-design-setup](Design/design-00-design-setup/SKILL.md) | product | `design/00-design-setup.md` (Figma capability, or HTML prototype as the medium) |
| G01 | [design-01-sitemap-flows](Design/design-01-sitemap-flows/SKILL.md) | one initiative | `design/I-<nnn>-<slug>/01-sitemap-flows.md` + FigJam charts |
| G02 | [design-02-screen-mockups](Design/design-02-screen-mockups/SKILL.md) | one scope | `design/I-<nnn>-<slug>/02-mockups/<scope>.md` + Figma frames or HTML prototype |
| G03 | [design-03-design-handoff](Design/design-03-design-handoff/SKILL.md) | one scope | `design/I-<nnn>-<slug>/03-handoff/<scope>.md` (the design handoff) |

### Development (`Development/`)
| Step | Skill | Works on | Output |
|---|---|---|---|
| D00 | [dev-00-dev-setup](Development/dev-00-dev-setup/SKILL.md) | product | `dev/00-dev-setup.md`, lint script and CI |
| D01 | [dev-01-tech-design](Development/dev-01-tech-design/SKILL.md) | baseline, then one initiative | `dev/architecture.md`; `dev/I-<nnn>-<slug>/01-tech-design.md` (13 layers + threat model) |
| D02 | [dev-02-data-model](Development/dev-02-data-model/SKILL.md) | one handed-off scope | `dev/I-<nnn>-<slug>/02-data-model/<scope>.md` |
| D03 | [dev-03-build-tasks](Development/dev-03-build-tasks/SKILL.md) | one handed-off scope | `dev/I-<nnn>-<slug>/03-tasks/<scope>.md` (`pdlc-tasks` blocks, agent brief, specification review) |
| D04 | [dev-04-code-plan-build](Development/dev-04-code-plan-build/SKILL.md) | one story, bug, or maintenance item | plan (read map, reuse map, budget) + code built in a sandbox until the locked tests pass |
| D05 | [dev-05-test-qa](Development/dev-05-test-qa/SKILL.md) | scope or version | test design before build; results, bugs, go / no-go after |
| D06 | [dev-06-deploy](Development/dev-06-deploy/SKILL.md) | version or event | `dev/releases/<version>.md` (release, hotfix, rollback, incident) |
| D07 | [dev-07-maintenance](Development/dev-07-maintenance/SKILL.md) | one maintenance item | `dev/maintenance/<id>.md` (HF, TD, UPG, SPK, CHR) |

**Decision log.** Any step that makes a decision of record writes `decisions/DEC-<nnn>-<slug>.md`. Examples: a scope cut, an architecture choice, a change-request outcome, or a spike's result. Files cite the DEC instead of repeating its reasoning.

**Reference packs**, bundled only in the skills that use them and read only when they apply:
- **`compliance.md`:** checklists for personal data, India's DPDP Act, GDPR, PCI DSS, RBI payments, GST invoicing, communications, and accessibility. These are questions to verify against current official sources, never legal facts.
- **`threat-model.md`:** STRIDE per data flow, used by dev-01.
- **`ai-features.md`:** eval sets owned by Product, prompt and model versioning, guardrails, budgets, eval runs in QA, and monitoring.

## Typical flow
1. **Setup:** Product runs `product-00` once. Design runs `design-00` if the product has a design stage. Development runs `dev-00` and the `dev-01` baseline once.
2. **Per idea:** `product-01`, which counts the features and takes them one at a time, then `product-02` for the initiative's PRD.
3. **Per scope**, lowest dependency level first:
   - Product: `product-03` (UX and charts), then `product-04` (edge cases first, then stories).
   - Design: `design-01` per initiative, then `design-02` and `design-03` per scope.
   - Development, per scope:
     1. `dev-01` for the initiative, then `dev-02`.
     2. `dev-05` (test design: tests first).
     3. `dev-03` (tasks and the specification review).
     4. `dev-04` per story, in a sandbox until the tests pass.
     5. `dev-05` (results).
4. **Release:**
   1. The team picks a version's items, and `product-06` checks their dependencies.
   2. `dev-06` deploys to pre-production, `dev-05` tests the version there, and `dev-06` promotes it to production on a Go.
   3. `product-07` writes the launch kit, and `product-00` syncs the product map.
5. **Any time:** `pdlc-next` to see what comes next, `product-05` for changes, `dev-07` for maintenance.

## Install
```bash
git clone https://github.com/curiyashman/sdlc-yash.git
cd sdlc-yash
# Claude Code / Cursor (user skills)
cp -r Common/* ~/.claude/skills/         # everyone (pdlc-next)
cp -r Product/product-* ~/.claude/skills/ # product team
cp -r Design/design-* ~/.claude/skills/   # design team
cp -r Development/dev-* ~/.claude/skills/ # development team
# Or for one Cursor project only:
# mkdir -p .cursor/skills && cp -r Common/* Product/product-* Design/design-* Development/dev-* .cursor/skills/
```
- `~/.claude/skills/` is read by Claude Code, and also by Cursor (all projects). `<repo>/.claude/skills/` covers one project only; Cursor also reads `.cursor/skills/`.
- **Claude projects (product team):** add the Product skills and `pdlc-next` to your Claude account. Fill in the configuration block of [`Product/claude-project-instructions.md`](Product/claude-project-instructions.md) and paste it into the project's instructions.
- **Design team:** add the Design skills and `pdlc-next`, and connect the Figma connector (or choose an HTML prototype). Fill in [`Design/agent-instructions.md`](Design/agent-instructions.md) and paste it into the project's instructions or the repository's `CLAUDE.md`.
- **Coding agents (development team):** fill in [`Development/agent-instructions.md`](Development/agent-instructions.md) and add it to `CLAUDE.md` and `AGENTS.md` of each code repository. Or let `dev-00-dev-setup` add its pointer, the lint script, and the CI check.
- **Remove the older skills** where these are installed, so two skills don't compete for the same request: `pdlc-00` to `pdlc-12`, workflow-architect, fullstack-architect, research-driven-prd, prd-to-ux-ui, requirements-to-stories, product-brainstorm, devops-sre-expert, and schema-design-interview. `design-system-spec` stays separate.

## Editing the skills
Never edit the generated folders (`Common/`, `Product/`, `Design/`, `Development/`). Edit `source/` and rebuild:

| File | Holds |
|---|---|
| `source/core.md` | the short core inlined in every SKILL.md |
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

`examples/sample-product/` is a small fictional product (Ledgerly) run through every step. It is the test fixture for the script and a worked example of the files, the header, `tracker.yaml`, the task blocks, the design references, and a DEC.
