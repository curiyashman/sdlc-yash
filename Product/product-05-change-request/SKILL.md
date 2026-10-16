---
name: product-05-change-request
description: "Product team, step P05 of the PDLC skills, used at any time; change requests are owned by the product team only. Handles a change to an approved requirement (a new capability, a changed rule or flow, a removal, an answer to a development query that changes a requirement) in [docs path]/product/change-requests/: records the request, runs a mandatory impact-area analysis audit across product map, PRD, UX, stories, design, architecture, data, tasks, code, QA, releases, ops, security/privacy, and what must not change, keeps those considerations in the CR file, then proposes options and version bumps; after approval updates the product files, marks affected files stale, reopens tracker items, and lists the re-runs each team needs. Use for 'change request', 'the requirement changed', 'add this to the initiative', 'remove this feature', 'dev raised a query that changes scope', 'what does this change affect', 'impact analysis'. Questionnaire first, assumes nothing, one .md file."
---


# Product 05: Change Request

You are the product lead who keeps the chain consistent when a requirement changes. A change made in one file without tracing it leaves UX, stories, and development work built on the old version. This step makes every requirement change visible, versioned, and traceable, and it is the only way an approved requirement, flow, story, edge case, or acceptance criterion changes.

**Product only.** Change requests belong to the product team. Development never runs this step; it raises a query in `tracker.yaml` when it believes a change is needed. Purely technical changes that don't alter product behavior (a different library, a schema refactor) are development's own decisions in their own steps, not change requests.

**Development impact is read, not edited.** This step reads development's files to trace impact, but never changes them: it marks them stale, reopens tracker items, and hands the development team a list of re-runs. Technical effort and risk come from the development team (Provided) or stay Open.

**Impact-area analysis is mandatory.** A CR may not move from Proposed to Analyzed (and must not be approved) until every impact area below is audited. Areas with no effect are recorded as `none` with a one-line reason — never omitted. The audit stays in the CR as a living consideration: when applying, deferring, or closing the CR, re-check any area still Open or whose upstream file version moved.

**CR lifecycle:** Proposed, Analyzed (impact audit complete), then Approved, Deferred (to a version), or Rejected; then Applied, then Closed.

*Scope of Recommendation here:* the options (accept now, defer, reject, or a smaller alternative), their trade-offs, and the proposed version bumps. The decision is always the person's (Provided), made by the change-request approver recorded in `product/00-product-context.md`.

**Also writes:** the product file where the change starts (update mode, with a version bump and the CR ID); the product map in `product/00-product-context.md` when nodes are added, changed, or removed; downstream product-file edits the person approves as mechanical. Never a file under `dev/`.

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

## Upstream files
Every product file the change can reach, development files read-only for impact, and `tracker.yaml` (including the query that triggered the change, if any). Run `lint` first: it lists stale files and open queries. The CR number comes from `pdlc.py new-id cr`.

## Questionnaire

**Step 1: The change**
1. What should change, in your own words?
2. Why, and where did it come from (user feedback, a development query (which Q ID), QA findings, a new idea, a failed assumption)?
3. Which initiative and which part is it about, if you know (feature, story, edge case, screen)?
4. How urgent is it, and has the team chosen a version for it?
5. What must not change as a result?

**Step 2: Clarify impact.** After the first impact-area audit, ask about anything the impact depends on (for example "existing users' invoices: keep the old rule, convert, or ask them?"). For technical effort and risk, ask whether the development team has assessed them; if not, they stay Open and the development team is asked through a query in `tracker.yaml`.

## Impact-area analysis (audit — required before Analyzed)

Walk the chain from where the change starts. For **every** area, set Status to one of: `none` | `update` | `rework` | `remove` | `open`. `none` still needs a short reason. Do not skip rows.

| # | Impact area | What to audit / keep as consideration | Who owns the follow-up |
|---|---|---|---|
| 1 | P00 product map | Modules / sub-modules / features added, changed, or removed; ID stability | Product, this run |
| 2 | P02 PRD | FRs, BRs, NFRs, information needs, existing behavior that must not change, touchpoints, feature dependency map | Product, this run (update mode) |
| 3 | P03 UX | Flows (FL), screens (SC), states, microcopy, role visibility | Product, re-run P03 |
| 4 | P04 stories and handoff | Stories to change / add / remove; edge-case registers (EC); acceptance criteria (AC); ready-for-dev / handoff status | Product, re-run P04 |
| 5 | G01–G03 design | Sitemap/flow charts, frames or prototype, design handoff, design-references on stories (only if design stage is on; else record `none` — design stage off) | Design, re-run G01–G03 |
| 6 | D01 tech design / architecture | Layers (L1–L13), DECs, threat model, approved packages | Development, re-run D01 |
| 7 | D02 data model | Entities, fields, migrations, existing-data rules, shared entities | Development, re-run D02 |
| 8 | D03 tasks | Tasks / sub-tasks to change, add, or remove; specification review still valid? | Development, re-run D03 |
| 9 | D04 built code | Stories already in progress / in review / done / released: rework, rollback, feature flags | Development, re-run D04 |
| 10 | D05 QA / tests | Test cases (TC) to rewrite or rerun; regression of unchanged behavior; eval sets if AI features | Development, re-run D05 |
| 11 | D06 releases / production | Shipped versions, production behavior, migrations already applied, rollback needs | Development |
| 12 | Ops / support / launch | Runbooks, support FAQ, launch kit, Confluence or help content if the product uses them | Product / ops (list explicitly) |
| 13 | Security / privacy / compliance | Authz, personal data, retention, audit logs, regimes named in product context | Product + Development (query if unclear) |
| 14 | Must-not-change boundary | Explicit list of behaviors, IDs, and contracts that stay frozen; cite FR/BR/US/AC | Product, this run |

**Per-area row fields (keep in the CR):** Status · File@version · Item IDs · Consideration (what to watch when applying or closing) · Effort (only if the team Provided an estimate) · Risk · Follow-up (re-run step or query ID).

**Audit rules**
1. Complete the full table before status becomes Analyzed. Missing rows = not Analyzed.
2. Keep the table when options are proposed and when the CR is Approved / Deferred / Rejected — it is the consideration record, not a scratch pad.
3. On Apply and again on Close, re-check every non-`none` area; update Status/Consideration if reality changed; leave Open areas as Open with a query, never invent answers.
4. If an area is unknown after reading the docs and code (Observed), mark `open` and raise a query — do not guess.

**Version bumps:** MAJOR when a file's meaning or scope changes, MINOR when items are added, PATCH for wording.

## Applying an approved CR
1. Re-read §2 Impact-area analysis; resolve or carry forward every Open consideration.
2. Update the product file where the change starts (usually the initiative's `02-prd.md`) in update mode: bump `doc_version`, add the CR ID to `change_requests`, add a change-log row. Update the product map if nodes change.
3. For every downstream product file affected: list the re-run. Lint marks it stale on its own once the source file's version moves on (MAJOR or MINOR), so nothing is marked by hand. It is updated by re-running its own step in update mode, which reads this CR. A direct edit only for a mechanical change the person approves here.
4. For every design or development file affected: list the re-run (lint shows it as stale). Never edit it. Design references in the stories concerned are marked `stale` by the design team's next run (G02 update mode); list those stories in the CR.
5. Stories whose handoff changes go back out of the ready-for-dev status until P04 is re-run and re-approved (and, with a design stage, G03 is re-approved for scopes with screens); the re-approved files are the new handoff.
6. In `tracker.yaml`: add or update the entry under `change_requests` (status `approved`, then `applied`); reopen affected items (back to `backlog` or `in_progress`); set removed items to `removed` (never delete them); add new items as `backlog`; set the query that triggered the CR to `became_cr` with the CR ID as its answer.
7. Record the decision (approved, deferred, or rejected, and why) as a DEC that the CR file cites. The DEC should point at the impact-area table, not restate every row.

## Output: `product/change-requests/CR-<nnn>-<slug>.md`

```markdown
(header: pdlc_step "P05", initiative I-<nnn> (if one), scope CR-<nnn>, depends_on [the files analyzed, with versions])
# CR-[nnn]: [title]

## 1. Request
What, why, source (including the Q ID if raised by development), urgency, target version, what must not change (all Provided).

## 2. Impact-area analysis (audit)
Status: Proposed | Analyzed (all 14 areas filled).
| # | Area | Status | File@version | Item IDs | Consideration (keep) | Effort | Risk | Follow-up |
|---|---|---|---|---|---|---|---|---|
| 1 | P00 product map | | | | | | | |
| 2 | P02 PRD | | | | | | | |
| 3 | P03 UX | | | | | | | |
| 4 | P04 stories / handoff | | | | | | | |
| 5 | G01–G03 design | | | | | | | |
| 6 | D01 tech design | | | | | | | |
| 7 | D02 data model | | | | | | | |
| 8 | D03 tasks | | | | | | | |
| 9 | D04 built code | | | | | | | |
| 10 | D05 QA / tests | | | | | | | |
| 11 | D06 releases / production | | | | | | | |
| 12 | Ops / support / launch | | | | | | | |
| 13 | Security / privacy / compliance | | | | | | | |
| 14 | Must-not-change boundary | | | | | | | |

## 3. Options (Recommendation)
| Option | What happens | Trade-off | Impact areas that stay Open |

## 4. Decision
Approved / Deferred to [version] / Rejected, by whom, when, wording. Cite DEC.

## 5. Applied changes (product files)
| File | Old version | New version | What changed |

## 6. Re-runs needed
| Team | Step | Initiative / scope | What to update | Tied to impact area # | Status |

## 7. Closing checklist
- [ ] Impact-area table re-checked; no silent Open left without a query
- [ ] Every product re-run done and re-handed off
- [ ] Every development re-run done
- [ ] Every reopened item resolved; tests rerun
- [ ] Must-not-change boundary still holds
The CR is Closed when all are checked.

## Change log
```

Run `lint --fix` and `board`. Next: the first product re-run in the list (usually product-04-user-stories for the earliest affected scope), then the development re-runs once the new handoff is approved.
