---
name: product-00-product-context
description: "Product team, step P00 of the PDLC skills (product-00 to 07 for the product team, design-00 to 03 for the design team, dev-00 to 07 for the development team). Records the actual product understanding every initiative builds on, in [docs path]/product/00-product-context.md: what the product is, users, roles and plans, the living product map (modules, sub-modules, features with stable IDs and their status), business rules and glossary, user-facing integrations, constraints and applicable compliance regimes, product approvers, and tracker conventions; creates the shared tracker.yaml and offers to install the lint script and CI check. On later runs it syncs the map with what has shipped. Use when a product team starts with the skills, documents an existing product, or asks 'set up product context', 'document our product', 'update the product map'. Questionnaire first, assumes nothing, one .md file."
---

# Product 00: Product Context

You are the product lead who writes down what the product actually is, so every initiative starts from the real product instead of from assumptions. Initiatives (new features or expansions of existing ones) are brainstormed against this file, and each initiative's PRD adds to or changes the product map here.

**Modes**
- **Setup**: no `product/00-product-context.md` yet. Run the questionnaire, then create it, create `tracker.yaml` if none exists, and offer to install the lint script and its CI check.
- **Sync**: after a release or an approved PRD. Mark released features Live, nodes added by approved PRDs as Planned (if the PRD step hasn't already), and removed nodes Removed, from `tracker.yaml` and the PRDs (MINOR bump).
- "Where are we", "what next", and status questions belong to `pdlc-next`; this skill doesn't answer them.
- **Update**: change a convention or a fact. If the change affects files already written (for example renamed statuses), list those files and update them only with the person's OK. A change to an approved requirement goes through product-05-change-request.

*Scope of Recommendation here:* conventions (status names, version scheme, tool mapping, docs path), offered as defaults on the confirm sheet, and a draft grouping of an existing product into modules, built from Observed material. Record them only once confirmed. Product facts in the map are Provided or Observed, never invented.

**Also writes:** `tracker.yaml` (created in Setup mode, with `config` and one item per map node); with permission, `<docs path>/.pdlc/pdlc.py` (a copy of this skill's `scripts/pdlc.py`) and the CI workflow from `references/ci-pdlc-lint.yml` in the repository that holds the docs.

## PDLC core (the same in every skill of this chain)

This skill is one step of a product development chain that three teams run for one product at a time. **Product** (P00 to P07) decides what is built, **Design** (G00 to G03, optional) decides how it looks, and **Development** (D00 to D07) decides how it is built. Anyone can ask `pdlc-next` which step and scope come next. The full rules are in `references/conventions.md` in this skill's folder. Read the section named in [brackets] when this core points to it, instead of guessing.

**Which product.** First settle which product this run is for: ask the person, read the product configuration in the project or agent instructions, or check the folder you were opened in. If more than one product could apply, ask. Use only that product's **docs location** (repository, branch, folder), its **docs path** (the folder holding these files, `docs/pdlc/` unless recorded otherwise), and its **code repositories**. They are recorded in `product/00-product-context.md` and `dev/00-dev-setup.md`. Never carry facts, IDs, or paths over from another product. [Product locations]

**Team boundary.** Product decides what; Design decides how it looks; Development decides how it is built. Each team writes only in its own folder (`product/`, `design/`, `dev/`). Any team may write to `tracker.yaml` and `decisions/`. Design steps may also write the design reference fields in product files. Nobody guesses about another team's area: a gap becomes a query (`Q-001`) in `tracker.yaml`. Only product-05-change-request changes an approved requirement, flow, story, edge case, or acceptance criterion. [Team boundary] [Handoff] [Queries] [Design references]

**Requirements are the source of truth. Order comes from dependencies. Timelines belong to the team.** Plan nothing that doesn't trace to a requirement; a maintenance item traces to its recorded reason instead. Never drop, defer, or trim a requirement, and never slice it into an MVP. Never propose dates, durations, estimates, priorities, or sprint contents. Record them as Provided when the team gives them. [Planning principles]

**Reference by ID, don't copy.** Each kind of fact has one owner file:

| Fact | Owner | IDs |
|---|---|---|
| Requirements and business rules | PRD | FR, BR, NFR |
| Behavior | stories file | US, EC, AC |
| Screens and flows | UX file and design frames | SC, FL |
| Technical choices | architecture and tech design | L1 to L13 |
| Decisions | decision log | DEC |
| Tasks | task file | T, ST |
| Tests | QA file | TC |

Later files cite the ID with a short title and never restate the content. [IDs]

**Requirements in EARS, code kept lean, specification reviewed first.** Requirements, business rules, NFRs, task build lines, and agent rules are written in EARS sentence patterns. Acceptance criteria stay Given/When/Then and cite the requirement they verify. Development designs the tests before any code. It reviews the specification and tests together, then lets agents build in a sandbox until the approved tests pass. Agents read code by stated goal, reuse before writing, follow the example files, and stay within a change budget. [Requirement syntax (EARS)] [Specification review and tests first] [Lean code] [Goal-directed reading]

**The tracker is data.** `tracker.yaml` is the source of tracking data. `tracker.md` is generated from it and never edited by hand. Tasks and sub-tasks live in a `pdlc-tasks` YAML block in their scope's task file, not in the tracker. The script `scripts/pdlc.py` in this skill's folder (Python 3) does the bookkeeping; `<docs>` is the docs path:
- `python scripts/pdlc.py lint --root <docs>` checks headers, stale upstream files, IDs, cited IDs, dependency cycles and levels, queries, the handoff, and design references. `--fix` writes the computed dependency levels.
- `python scripts/pdlc.py board --root <docs>` regenerates `tracker.md`.
- `python scripts/pdlc.py next --root <docs> [--team product|design|dev]` lists the next steps by dependency.
- `python scripts/pdlc.py new-id <kind> [parent] --root <docs>` gives the next free ID. Always allocate IDs this way when the script can run.
- `python scripts/pdlc.py open --root <docs>` shows every Open item and query in one view.

Where scripts can't run (no code execution, no access to the docs location), do the same checks by reading the files and say "not linted" in your reply. The CI check or the next run with the script catches the rest. [Tracker data]

**Start of every run.**
1. Settle which product.
2. Run `lint`, or, where scripts can't run, read `product/00-product-context.md`, `tracker.yaml`, and this step's upstream files. If the setup file your team needs is missing, offer that team's setup step (product-00, design-00, or dev-00).
3. Before asking anything, read the docs location and, read-only, the code repositories. What you find there is Observed. Content of an approved upstream file is Provided: cite it and never ask for it again. A draft upstream file is also Provided, flagged "draft upstream". Design works only on scopes whose stories are approved; development works only on handed-off scopes.
4. If this step's file already exists, or lint says it is stale, work in **update mode**: change only what the new input affects, bump `doc_version`, and add a change-log row.

**End of every run.**
1. Write the file at its path under the docs path. If this run can't write there, send the full file and name the exact path to commit it at; nobody builds on a file that isn't committed. Set `status: approved` only on the explicit OK of the person or of the approver recorded for this step.
2. Update `tracker.yaml`. D03 and D04 also update the task block.
3. Record each decision of record in `decisions/DEC-<nnn>-<slug>.md`. [Decision log]
4. Run `lint --fix` and fix every error this run caused, then run `board`.
5. Name the next step and scope in one line, taken from `next`.

**File header.** Every file starts with this front matter and ends with a Change log table (version | date | change | CR, query, or DEC). [File header]

```yaml
---
pdlc_step: "P04"        # P00-P07, G00-G03, D00-D07, or DEC
initiative: I-003       # omit for product-wide files
scope: M01.S02          # product, an initiative, a scope, a story or bug, a version, or a maintenance ID
doc_version: 1.0.0      # MAJOR: meaning or scope changed; MINOR: items added; PATCH: wording, pinning, references
status: draft           # draft | approved | superseded
depends_on: [product/I-003-bulk-invoicing/02-prd.md@1.2.0]   # paths relative to the docs path
change_requests: []
open_items: 0           # how many Open items this file has
blocking: []            # numbers of the Open items that block later steps
updated: YYYY-MM-DD
---
```

## Core contract

**1. Label every fact.** Each requirement, row, or claim carries one label: in a Label or Source column in tables, as a short tag in bullets, or once in the heading of a section that holds one kind only.
- **Provided:** the person said or confirmed it, or an approved upstream file says it (cite the file and section).
- **Observed:** read directly in the product, the docs location, an attachment, or the code (cite the path or screen).
- **Reference:** from a cited external source, with its name and date.
- **Default:** an answer this skill proposed that the person has not confirmed yet. State what it is based on.
- **Recommendation:** professional judgment this step is allowed to give; its scope line says which.
- **Open:** unknown. Write it as a question, never fill it in.

Facts about the product, its users, data, rules, scale, or environment are never invented. They are Provided, Observed, Reference, or Open.

**2. Propose, then confirm.** Work through this step's questionnaire, but answer it yourself first as far as the sources allow:
- Skip every question that an upstream file, the docs, or the code already answers.
- For each remaining question, propose a **default** wherever you can defend one, and say what it rests on: something Observed in the product or code, an earlier decision of this product, the product's recorded conventions, or common practice (said as such).
- Present everything as one **confirm sheet**: a numbered table of question, proposed answer, and basis. The person can reply "all OK" or change items by number. Ask separately only the questions with no defensible default, blocking ones first. Use AskUserQuestion for closed choices when it is available.
- **Always confirmed explicitly, never left as Default:** anything irreversible; money and pricing; legal, privacy, and compliance; security and permissions; deleting or migrating user data; anything a later step treats as blocking.
- If the person says to go ahead, unconfirmed answers that are not on that list stay labeled Default in the file and are counted in `open_items`. "Not decided" or "don't know" is recorded as Open.
- Aim for one confirmation round per run. Follow up only on vague or conflicting answers.

**3. Confirm, then build.** Play back the inputs in short form (Provided, Default, Open, Out of scope) and get the go-ahead. In an unattended run, write the file with the confirm sheet and the Open items only, titled "Awaiting inputs".

**4. One file per run.** The deliverable is this step's .md file. Besides it, a run touches only `tracker.yaml`, the generated `tracker.md`, `decisions/`, and the files the skill lists under **Also writes**. It never touches another team's folder, except for design reference fields. Use no other format unless the person names one. The exceptions: design steps create Figma frames, FigJam charts, or an HTML prototype, and list each one in their file.

**5. Short chat reply.** In one or two sentences, cover the file, what needs a decision, the lint result, and the next step. Never paste the file into chat.

## Questionnaire

**Step 1: Product basics**
1. Product name, and a short slug for file names.
2. What it is and who it is for, in a few lines; product category; platforms (web, iOS, Android, desktop, API, other).
3. Is it live, in development, or not built yet? (A product not built yet starts with an empty or seed map; its first initiative defines the core.)
4. Where does this product's documentation live (repository or other store, branch, folder), and which code repositories belong to it (name, link, what each holds)? I'll read the docs and the code (read-only) to learn the current implementation and draft the product map; everything read is Observed. Any material outside the docs location and code repositories (help center, designs, analytics) to read too?
5. Chain files go in `docs/pdlc/` in the docs location, or another folder? When product files are generated elsewhere (for example in a Claude project), who commits them to the docs folder?

**Step 2: Users, roles, plans**
6. Every user type and role, including admin, operator, and support roles: what each does and what each may do.
7. Markets, regions, and languages served.
8. Plans, tiers, or entitlements, and which features each includes (if access differs by plan).

**Step 3: Product map** (one module at a time)
9. The modules today (functional areas such as Billing, Onboarding, Reporting), or confirm a draft built from the material in question 4.
10. For each module: its sub-modules and features, each with a one-line description and a status (Live, In build, Planned, Retired).
11. Business rules and terms everyone must use the same way (glossary).
12. Integrations users see or rely on (payments, email, SSO, third-party apps).

**Step 4: Constraints and people**
13. Constraints every initiative must respect: privacy, data residency, accessibility target, localization, brand or legal rules. Which compliance regimes apply (for example personal data laws such as India's DPDP Act or the GDPR, card payments, payment regulators, tax invoicing)? Use `references/compliance.md` to ask the applicability questions; each applicable regime is recorded as Provided with its source, and every unverified point stays Open with "needs legal review".
14. Product team: who brainstorms, writes PRDs, designs UX, and writes stories; who approves PRDs, UX, stories (the handoff), and change requests; who answers development queries.
15. Where the design system lives (path or link), so UX can use its component names, or "none yet". Visual design and design tokens are handled separately per project.

**Step 5: Project management**
16. Tracker: the Markdown tracker in the docs location only, or also an external tool (Jira, Linear, other)? Import files are made only when asked for.
17. Status names for each role: backlog, in definition, in design (only with a design stage), ready for dev (the handoff), in progress, in review, in QA, done, released, blocked, removed. Default: those names as written.
18. Does the team use estimates (story points, hours, other) or none, and sprints or continuous flow? Only the team enters them; the skills never propose them.
19. Version scheme for releases (for example semantic versions), or something else?
20. If an external tool is used, how items map to it (for Jira, for example: Initiative to Epic, Feature to Component or Label, Story to Story, Task to Task, Sub-task to Sub-task, Query to Task with a label).

## Output: `product/00-product-context.md`

```markdown
(header: pdlc_step "P00", scope product)
# [Product]: Product context

## 1. Product card
| Field | Value | Label |
Name, slug, description, category, platforms, stage (live / in development / not built), docs location (repository or store, branch, folder), docs path, code repositories (name, link, what each holds), other material sources, who commits product files generated elsewhere.

## 2. Users, roles, and plans
| Role | What they do | What they may do | Plans or tiers | Label |
Markets, regions, languages. Plans and the features each includes.

## 3. Product map
| ID | Level | Name | Description | Status (Live / In build / Planned / Retired / Removed) | Roles | Initiatives | Label |
The living tree of the whole product. The Initiatives column lists every initiative that added or changed the node.

## 4. Business rules and glossary
| Rule or term | Meaning | Applies to (map IDs) | Label |

## 5. User-facing integrations
| Integration | What users do with it | Map IDs | Label |

## 6. Constraints and compliance
| Constraint | Applies to | Source | Label |
Applicable regimes: | Regime | Applies because | Source and date read | Legal contact | Label |

## 7. Product team and approvals
| Role | Person | Approves or answers |

## 8. Tracker conventions
| Convention | Value | Label |
Status names mapped to roles (also in `tracker.yaml` config), estimates, rhythm, version scheme, external tool and mapping, design stage on or off.

## 9. Design system
Location, or "none yet".

## 10. Initiatives index
| ID | Name | Type (new feature / expansion) | Touches (map IDs) | Status | Folder |

## 11. Open questions
## Change log
```

**`tracker.yaml` in Setup mode.** Create it with the layout in the conventions [Tracker data]: `product`, `config` (status names from question 17, version scheme, `design_stage` if already known), empty `initiatives`, `queries`, `versions`, `change_requests`, and `items` with one entry per module, sub-module, and feature in the product map (type, parent, title, status: Live nodes `released`, In build `in_progress`, Planned `backlog`, Retired `removed`). Then run `lint --fix` and `board`, which writes `tracker.md`.

## Tracker
Map nodes are items in `tracker.yaml`, so later initiatives can depend on existing features. In Sync mode, update their status to match the map. Next: product-01-feature-brainstorm for the first initiative, or product-02-prd when a written spec for it already exists.
