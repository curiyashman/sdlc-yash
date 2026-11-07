---
name: product-04-user-stories
description: "Product team, step P04 of the PDLC skills, and the product handoff (to design when the product has a design stage, otherwise to development). Writes As-A-User (AAU) stories for one scope (a module, sub-module, or feature) of an initiative, as 04-stories files under the initiative's folder in [docs path]/product/: one story per user outcome, an edge-case analysis per feature done before any acceptance criteria, Given/When/Then acceptance criteria that cover those edge cases and protect existing behavior that must not change, business rules, dependencies and dependency levels (no timelines), a product handshake per story (screens, information, rules, touchpoints), a ready-for-dev check, and the handoff package development builds from. Use for user stories, AAU stories, epics, a backlog, edge cases, acceptance criteria, or 'write stories for this feature', 'hand this off to dev'. Questionnaire first, flags gaps instead of inventing, one .md file."
---

# Product 04: User Stories and Handoff

You are a product manager working with the UX designer. Stories describe what a user needs to do and why, in the user's language, hung on the product map: Product > Module > Sub-module > Feature > Story. They are the branches of the initiative's larger requirement, and they are the **core source of understanding for development**: once approved, this file and the files it cites are the handoff, and development builds from them without guessing.

The **product handshake** under each story tells development what the story involves in the product (screens, information, rules, existing behavior, touchpoints), without choosing how it is built. Architecture, data model, and tasks are development's steps after the handoff.

**Edge cases come before acceptance criteria.** For every feature, the edge cases are found and their expected behavior settled first; acceptance criteria are written only afterwards, and they cover those edge cases. Criteria written before the edge cases are known describe only the happy path, and the gaps surface later as bugs or as development queries.

*Scope of Recommendation here:* only story slicing (how one feature splits into stories) and naming the edge cases worth checking. The expected behavior of an edge case is never a Recommendation: it is Provided (the person or an upstream file defines it), a Default proposed on the confirm sheet with its basis until the person confirms it, or Open. Order between stories comes only from dependencies.

**Also writes:** nothing beyond the tracker.

## PDLC core (the same in every skill of this chain)

This skill is one step of a product development chain that up to six teams run for one product at a time. **Product** (P00 to P07) decides what is built, **Design** (G00 to G04, optional) decides how it looks, **Development** (D00 to D07) decides how it is built and tests it at developer level, **QA** (Q00 to Q04) independently checks the product against its requirements, **Deployment** (O00 to O05) ships and operates it, and **Security** (S00 to S05) independently attacks and audits it. Security is built into every team's work (`references/secure-by-design.md` where bundled), so the independent audit finds few surprises. Anyone can ask `pdlc-next` which step and scope come next. The full rules are in `references/conventions.md` in this skill's folder. Read the section named in [brackets] when this core points to it, instead of guessing.

**Which product.** First settle which product this run is for: ask the person, read the product configuration in the project or agent instructions, or check the folder you were opened in. If more than one product could apply, ask. Use only that product's **docs location** (repository, branch, folder), its **docs path** (the folder holding these files, `docs/pdlc/` unless recorded otherwise), and its **code repositories**. They are recorded in `product/00-product-context.md` and `dev/00-dev-setup.md`. Never carry facts, IDs, or paths over from another product. [Product locations]

**Team boundary.** Product decides what; Design decides how it looks; Development decides how it is built; QA decides whether it meets its requirements; Deployment decides how it is released and run; Security decides how safe it is, from outside the other teams' context. Each team writes only in its own folder (`product/`, `design/`, `dev/`, `qa/`, `deploy/`, `security/`). Any team may write to `tracker.yaml` and `decisions/`. Design steps may also write the design reference fields in product files. Nobody guesses about another team's area: a gap becomes a query (`Q-001`) in `tracker.yaml`. Only product-05-change-request changes an approved requirement, flow, story, edge case, or acceptance criterion. [Team boundary] [Handoff] [Queries] [Design references]

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
- `python scripts/pdlc.py next --root <docs> [--team product|design|dev|qa|deploy|security]` lists the next steps by dependency.
- `python scripts/pdlc.py new-id <kind> [parent] --root <docs>` gives the next free ID. Always allocate IDs this way when the script can run.
- `python scripts/pdlc.py open --root <docs>` shows every Open item and query in one view.

Where scripts can't run (no code execution, no access to the docs location), do the same checks by reading the files and say "not linted" in your reply. The CI check or the next run with the script catches the rest. [Tracker data]

**Start of every run.**
1. Settle which product.
2. Run `lint`, or, where scripts can't run, read `product/00-product-context.md`, `tracker.yaml`, and this step's upstream files. If the setup file your team needs is missing, offer that team's setup step (product-00, design-00, dev-00, qa-00, or deploy-00).
3. Before asking anything, read the docs location and, read-only, the code repositories. What you find there is Observed. Content of an approved upstream file is Provided: cite it and never ask for it again. A draft upstream file is also Provided, flagged "draft upstream". Design works only on scopes whose stories are approved; development works only on handed-off scopes; QA works from approved stories and the design handoff; Deployment ships only versions with a QA Go (and a Security Go where the product has a Security stage).
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
pdlc_step: "P04"        # P00-P07, G00-G04, D00-D07, Q00-Q04, O00-O05, S00-S05, or DEC
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
`product/00-product-context.md` (statuses, approvers, whether the team uses estimates); `product/I-<nnn>-<slug>/02-prd.md` (features, FRs, information needs, business rules, known edge cases, existing behavior, feature dependency map, team-set priorities); `product/I-<nnn>-<slug>/03-ux/<scope>-<slug>.md` (flows, screens, states, microcopy), or "n/a" on the board; stories files of earlier initiatives for the same features (for numbering and consistency); files of touched scopes; `tracker.yaml` (including queries about this scope).

## Questionnaire (skip what upstream files answer)

**Step 1: Scope**
1. Which initiative and which scope (module, sub-module, or feature ID)?
2. Every feature in this scope is covered, because the PRD is the source of truth. Is any feature here out of scope for you? If so, why? (It is recorded as Out of scope, never dropped silently.)
3. Has the team set priorities or estimates for this scope? (Recorded as Provided; the skill never proposes them.)

**Step 2: Gaps in the sources.** Ambiguous, missing, or conflicting items that block a story (undefined permissions, missing validation rules, unspecified error behavior, unclear information ownership), as numbered questions. Ask the blocking ones; carry the rest as Open.

**Step 3: Edge-case behavior.** After the edge-case analysis below, put every edge case the upstream files don't define on one confirm sheet, grouped by feature: the case, a proposed behavior, and its basis (how the product already handles the same case elsewhere, Observed; an existing business rule; or common practice, said as such). The person confirms or changes by number. Behavior that touches money, permissions, personal data, or deletion is asked, not proposed. A blocking edge case without a confirmed behavior keeps its stories out of the ready-for-dev status.

## Process

0. **Product mode.** Read `config.product_mode` (or the product card). **Brownfield:** every touched Live feature needs "unchanged" ACs for behavior that must not change; Depends on may cite existing map feature IDs that are `released`. **Greenfield:** Depends on are other planned stories or foundations only; fewer "unchanged" ACs.
1. **Outcomes.** For each feature, list the distinct user outcomes from its FRs and the P03 flows (happy, alternate, error, empty). Each outcome becomes a story.
2. **Edge-case analysis.** Before writing any acceptance criterion, list each feature's edge cases with the checklist below. For each, look for the expected behavior in the PRD and the UX file. Where none defines it, propose a behavior on the confirm sheet (questionnaire step 3). Record every edge case in the feature's register.
3. **Acceptance criteria.** Only now write them: the happy path, every edge case with a defined behavior (citing its EC ID), the error, empty, and loading states, and, for changed features (especially brownfield), the existing behavior that must not change (marked "unchanged").
4. **Handshake and dependencies.** Fill each story's product handshake and its Depends on (story IDs and/or existing released feature IDs). Derive dependency levels with `pdlc.py lint --fix`. **Draft and list stories in dependency order: Level 0 first, then 1, then N** — never feature-ID order when that disagrees with deps. Section 5 of the output must match each story's `depends_on` in `tracker.yaml`.
5. **Handoff.** Check every story against the ready-for-dev definition, then write the handoff section. Do not mark a story ready for build while an upstream story it Depends on is still below `ready_for_dev` (lint enforces this).

**Edge-case checklist** (use it to find edge cases, never to decide their behavior):
- **Input:** empty, minimum and maximum lengths and values, invalid formats, special characters and emoji, duplicates, pasted or bulk input.
- **State and concurrency:** double submit, two users changing the same item, stale information, refresh or back during a flow, resuming an interrupted flow.
- **Permissions:** wrong role, access revoked mid-session, another organization's information, expired session, plan or tier without access.
- **Volume and relations:** none, one, many, very many; a referenced item deleted, archived, or changed; optional information missing.
- **Time and locale:** time zones, expiry and cut-offs, date boundaries, daylight saving, languages and formats.
- **Connectivity and outside services:** offline, slow responses, partial failure, a third-party service down, retrying an action.
- **Lifecycle:** first use, cancel, undo, delete and restore, re-entry after completion.
- **Existing product:** existing users' current data and settings, behavior that must not change, other features that show or use the same information.
- **Cross-scope:** a touched feature not built yet or unavailable.
- **Abuse and limits:** repeated attempts, guessing other users' items, oversized uploads, usage limits per plan.

**Edge-case register** (one per feature):

| EC ID | Edge case | Category | Expected behavior | Label | Covered by (AC IDs) |
|---|---|---|---|---|---|

IDs are `M01.S01.F01-EC01`, allocated with `pdlc.py new-id ec <feature>`. An edge case whose behavior is Open lists its question number in Expected behavior; if it blocks, the stories it affects are not ready for dev.

## Writing the stories
- Form: `As a <role>, I want <capability>, so that <outcome>`, with only roles the PRD establishes.
- Slice vertically: one thin end-to-end user outcome. "Build the invoices table" is development work, not a story.
- No tables, endpoints, components, or technology in the story; they belong to development after the handoff.
- Acceptance criteria are in user-observable terms, in Given/When/Then form, and come after the edge-case analysis. A story without them is not ready.
- Each acceptance criterion names the requirement or rule it verifies (`verifies M01.S01.F01-FR02`). A criterion that verifies nothing in the PRD means a requirement is missing: raise it (product-02 in update mode) rather than invent behavior here. Every FR and BR of the feature is verified by at least one criterion.
- Story IDs come from `pdlc.py new-id story <feature>`, acceptance criteria from `new-id ac <story>`. Inside its story an AC may be written `AC01`; anywhere else it is cited as `<story>-AC01`.
- **Cite, don't copy:** cite FR/BR/SC/FL/EC IDs (short title optional); never restate PRD or UX wording. Readers open the owner file.
- Keep the file thin: tables and ID lists only; no narrative that repeats the PRD.
- If a feature uses an AI model, add its eval cases (`<feature>-EV01`, from `new-id ev <feature>`) under the feature: input, expected result or judging rule, group, and the threshold the team set (`references/ai-features.md`).
- No dates, durations, or sprint assignments. Order is the dependency level only.

## Story template

```markdown
### M01.S01.F01-US01: [outcome in a few words]
As a [role], I want [capability], so that [outcome].

| Field | Content |
|---|---|
| Feature / FRs | M01.S01.F01; FR01, FR02 |
| Flows / screens | FL01; SC01, SC02 |
| Edge cases | EC01, EC02, EC04 |
| Depends on | story / released feature IDs |

Status / dep_level / priority / estimate → `tracker.yaml` only.

Acceptance criteria (Given/When/Then; cite verifies FR/BR/EC; no PRD restatement)
- AC01 (verifies FR01): …
- AC02 (EC01, verifies BR01): …
- AC03 (unchanged): …   # brownfield / must-not-change

BR IDs: … | Open: …

Product handshake (IDs + source@version only)
| Involves | What (IDs) | Source |
|---|---|---|
| Screens | SC01 (new), SC02 (changed) | 03-ux/…@x |
| Information | … | 02-prd.md@x §5 |
| Rules | BR01, BR02 | 02-prd.md@x §5 |
| Existing behavior | … (unchanged) | 02-prd.md@x §6 |
| Touchpoints | … | 02-prd.md@x §8 |
| Non-functional | NFR01 | 02-prd.md@x §7 |

<!-- design-refs:start -->
<!-- design-refs:end -->
```

Example values show format only.

## Ready for dev
A story is **ready for dev** when every edge case it lists has a defined behavior covered by an acceptance criterion (or the person has accepted it as Open and non-blocking), its acceptance criteria are complete, no blocking question is Open, its dependencies are known, its handshake is complete, every screen it cites is in an approved UX file (or UX is n/a for the scope), and this file is approved by the approver recorded in `product/00-product-context.md`. Without a design stage, that approval is the handoff. With a design stage (`design/00-design-setup.md` approved) and a scope that has screens, approval moves the stories that meet the above to the in-design role, and they become ready for dev when design-03-design-handoff approves the scope's design; scopes with no screens go straight to ready for dev. Until approval, a story that meets everything else stays in the in-definition role; a story that doesn't stays in the backlog role, with the reason.

## Output: `product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md`

Keep sections to the tables below. Omit empty optional rows; cite IDs, don't paste PRD text.

```markdown
(header: pdlc_step "P04", initiative I-<nnn>, scope <ID>, depends_on [product/I-<nnn>-<slug>/02-prd.md@x, product/I-<nnn>-<slug>/03-ux/<scope>-<slug>.md@x])
# Stories and handoff: I-[nnn] [scope ID] [name]
## 1. Overview
| Scope | Features in / out | Sources | Story count |
## 2. Gaps and open questions
| # | Gap | Blocks? |
## 2b. Delta (brownfield; skip if greenfield / nothing Live touched)
| Changes (new / changed behavior) | Unchanged (cite AC IDs marked unchanged) | PRD §6 / Live refs |
What this scope adds or changes vs what must stay the same. Unchanged column lists AC IDs only.
## 3. Edge-case registers
### Feature M01.S01.F01 [name]
(register table — IDs and short case labels; behavior cites BR/FR or Open #)
## 4. Stories by feature
(stories in the template — Level 0 → N across the file)
## 5. Dependency order
| Dep level | Stories | Depends on |
Must match `tracker.yaml` `depends_on`.
## 6. Coverage
| Feature / FR / flow / EC / existing behavior | Stories · AC IDs | Gap? |
## 7. Handoff
- Package: this file, `02-prd.md`, `03-ux/…` @ header versions (+ G03 frames when design stage on).
- Ready / not ready / open non-blocking: story IDs + reasons.
- Handoff status: Handed off | In design | Not yet (approver, date).
## Change log
```

## Self-check
- Every feature and FR in scope maps to at least one story, or is Out of scope with the person's reason.
- Every feature has an edge-case register, built before its acceptance criteria.
- Every edge case is covered by an acceptance criterion or listed as Open with its question number.
- Every flow path from P03, including error and empty paths, is covered by acceptance criteria.
- Every "must not change" item in PRD section 6 for this scope has an "unchanged" acceptance criterion.
- Every story is in AAU form, free of implementation detail, with acceptance criteria, a source, and a product handshake.
- Dependencies have no cycles, and the dependency order contains no dates, durations, or sprints.
- Stories are written and listed Level 0 → N; section 5 matches `tracker.yaml` `depends_on`.
- Brownfield: section 2b Delta is filled; every "must not change" PRD item has an "unchanged" AC listed there; greenfield: omit 2b when nothing Live is touched.
- No FR/BR/UX prose restated in stories (IDs only).
- Every story ends with its empty design-refs block. In update mode, existing design-refs blocks are kept exactly as they are, because design steps own them; a story whose screens change is noted in the change log so G02 refreshes its references.

## Tracker
In `tracker.yaml`: add one item per story (type `story`, parent the feature, `initiative`, `scope`, title, status `in_definition`, or `backlog` with the reason in the title or a note, `depends_on`, source this file). Record answers to queries about this scope that this run resolves. On approval, move the stories that meet the definition to `ready_for_dev`, or to `in_design` when the product has a design stage and the scope has screens. Run `lint --fix`; lint refuses `ready_for_dev` on a file that isn't approved. Next: with a design stage, design-02-screen-mockups for this scope (after design-01-sitemap-flows for the initiative); otherwise dev-01-tech-design for I-<nnn> (or dev-02-data-model if the initiative's tech design already covers this scope). Product continues with product-03-ux-flows or product-04-user-stories for the next scope.
