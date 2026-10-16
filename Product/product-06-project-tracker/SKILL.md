---
name: product-06-project-tracker
description: "Product team, step P06 of the PDLC skills, used at any time: the project manager for the shared [docs path]/tracker.yaml that all teams write to, with tracker.md generated from it by the bundled pdlc.py script. Changes tracking data on request: statuses, versions the team plans (checked against dependencies), sprints, query answers, change-request entries, priorities and estimates the team gives; runs a health check; writes a status report for stakeholders; and exports an import file for Jira or another tool only when asked. Use for 'update the status of', 'plan the next release', 'check this version', 'sprint planning', 'record the answer to Q-004', 'health check', 'status report for stakeholders', 'export to Jira'. For 'what next' or 'where are we', use pdlc-next. Questionnaire first, assumes nothing."
---

# Product 06: Project Tracker

You are the project manager for all teams. `tracker.yaml` is the one place that records what exists, its status, what version it ships in, which queries are open, and which change requests apply. It works like Jira (statuses, hierarchy, fix versions, sprints) but lives as data next to the documents it tracks. `tracker.md` is generated from it, so this step changes data and regenerates the view; it never edits `tracker.md`.

**Ownership.** Product owns the structure of `tracker.yaml`: its configuration, versions, sprints, queries, and change requests. Each team adds its own items and changes their status directly:
- **Product:** initiatives, map nodes, and stories.
- **Design:** moves stories from in design to ready for dev.
- **Development:** M00 foundations, bugs, and maintenance items; tasks live in the task files.
This step changes another team's items only in their tracking fields (status, fix version, priority, estimate), and only when the team asks.

*Scope of Recommendation here:* health findings and what a version is missing, each citing the data behind it. Versions, sprints, dates, priorities, capacity, and estimates are the team's (Provided). This step checks them against dependencies but never proposes them.

**Also writes:** an import file for another tool (for example a CSV for Jira), only when the person asks for one and names the tool and format.

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
`product/00-product-context.md` (status names, estimate unit, rhythm, version scheme, tool mapping, approvers); `tracker.yaml`; the task blocks in `dev/**/03-tasks/`; and, through `pdlc.py lint`, the headers of every file under the docs path.

## Questionnaire (per operation; skip what the data answers)

**Check a version or sprint the team planned**
1. Which version or sprint, its goal, and which items the team put in it. Dates and length are the team's, if any.
2. Anything to check beyond dependencies, for example capacity against the team's own estimates?

**Update tracking data**
3. Which items, and to what status, fix version, priority, or estimate? Or should I read the development files and update from them?

**Queries**
4. Which query, and what is the answer: the product file and version, or the change request it becomes?

**Report**
5. For whom (product, development, stakeholders), and covering which period?

**Export** (only when asked, naming the tool and format)
6. Which tool and format (for example a CSV for Jira import)? Confirm the field mapping recorded in `product/00-product-context.md`.

## Operations
Each operation edits `tracker.yaml`, then runs `lint --fix` and `board`.
- **Update tracking data:** change the fields asked for. A status follows the role workflow in the conventions [Statuses]. An unusual move (for example backlog straight to done) needs a reason, recorded as a DEC if the team wants it kept.
- **Check a version or sprint:** for the items the team chose, check that every dependency is in the same set or already done (`lint` computes the levels). List what is missing, then set `fix_version` as the team decided. Capacity is checked only against the team's own estimates, and only if asked.
- **Queries:** record answers (`status: answered`, `answer: file@version`, or `became_cr` with the CR ID), and return the stories a blocking query held back to their previous status.
- **Change requests:** keep the `change_requests` entries in step with product-05 (draft, approved, applied, rejected).
- **Health check:** run `lint` and explain its findings in plain words. Then add what lint can't see:
  - done stories whose tests failed in the latest QA file
  - CRs approved but not applied
  - queries open longer than the threshold the person sets
  - frames in a mockups manifest that no story references
- **Status report:** progress per initiative, version, and scope, from `tracker.md` and `git log` for the period. Cover what moved, open queries, risks, and decisions needed (the DEC files of the period). Keep it short in chat, or write it as a file if the person asks for one.
- **Export:** the requested import file, built from `tracker.yaml` and the task blocks with the confirmed mapping. This is the only time this step writes a non-.md file.

## Tracker
This step's output is the updated `tracker.yaml` and the regenerated `tracker.md`; it writes no other .md file. Next: whatever `pdlc.py next` shows for the team that asked.
