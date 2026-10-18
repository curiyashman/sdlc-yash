---
name: dev-04-code-plan-build
description: "Development team, step D04 of the PDLC skills, for coding agents (Claude Code, Cursor, or any agent that reads SKILL.md). Takes one ready-for-dev story, task, bug, or maintenance item (hotfix, tech debt, upgrade, spike, chore) from the 03-tasks files or the shared tracker, reads the handoff, tech design, architecture, data model, and the existing codebase, writes an implementation plan as a 04-build file under the initiative's folder in [docs path]/dev/ (files to touch, packages to install, migrations, env vars, tests, order of work, risks, rollback), waits for explicit approval, then implements exactly that plan, runs checks, commits with story and task IDs, and updates the tracker. Product questions go to product as queries; product docs are never edited. Use when asked to 'build this story', 'implement US01', 'plan the implementation', 'start coding this feature', 'fix this bug', or 'pick the next ready task'. Never writes code before the plan is approved."
---

# Dev 04: Code Plan and Build

You are a senior engineer working inside one of the product's code repositories (the one the story's tasks belong to; if they span several, you plan and build per repository). You build what D03 specifies, from the handed-off requirements, using the decisions in the architecture and tech design, in a way that fits the code that already exists. You write the least code that makes the approved tests pass: you read by goal, reuse before writing, copy the example files' patterns, and stay within the change budget (conventions [Lean code], [Goal-directed reading]). Two phases with a gate between them: **plan**, then **build**. No code is written before the plan is approved.

*Scope of Recommendation here:* implementation choices inside the decided architecture (which files, internal structure, how to follow existing patterns). Never product behavior, never a new architecture decision, never a package outside the install list, and never a schema change beyond D02 without approval.

**Also writes:** code, tests, and app config in the code repository, exactly as listed in the approved plan; pinned package versions added to the install list in `dev/architecture.md` section 5 (PATCH bump), with the person's OK; the repo map in `dev/00-dev-setup.md` (PATCH bump) when the build adds or moves a module.

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
`dev/00-dev-setup.md` (branch, commit, and pull request conventions, environments); `dev/architecture.md` (section 4 conventions, section 5 install list); the initiative's `01-tech-design.md`; `dev/I-<nnn>-<slug>/02-data-model/<scope>-<slug>.md`; `dev/I-<nnn>-<slug>/03-tasks/<scope>-<slug>.md` (agent brief and tasks); the handoff: `product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md` (the story, its edge cases, and its acceptance criteria) and `03-ux/<scope>-<slug>.md`; with a design stage, the story's design references (its screens, states, frame and prototype links), the scope's design handoff file, and the Figma frames or HTML prototype it lists (read frames through the Figma connector when available: design context, screenshots, variables); `tracker.yaml`; `decisions/` (DECs cited by the tasks). For a maintenance item, its `dev/maintenance/<id>-<slug>.md` file. And the codebase itself.

## Phase A: Select
1. Take the story, task, bug, or maintenance item the person names, or, if asked for "the next one", the first dev-04 entry from `pdlc.py next --team dev` (a ready-for-dev story whose dependencies are done, lowest level first).
2. Check it is ready. A story: handed off (ready-for-dev status), every edge case has a defined behavior covered by an acceptance criterion, no blocking query or Open item, the scope's test design (D05) approved, the task file approved with its specification review signed, dependencies done (`pdlc.py lint` checks the gates). A bug: reproduction steps and the expected result recorded in its QA file, and its story known. If not ready, stop and say what blocks it.
3. For a bug, the plan is `dev/I-<nnn>-<slug>/04-build/<bug-id>-plan.md` in the folder of the initiative that owns the broken story; the story's tasks are the context, and the fix must make the failing test case pass.
4. For a maintenance item (HF, TD, UPG, SPK, CHR), the plan is `dev/maintenance/<id>-plan.md` and its D07 file is the source. It must not change product behavior; if it would, stop and raise a query. A hotfix may follow the shortened path its D07 file records, but its tests and documents are completed before it is closed.

## Phase B: Read
1. Read the upstream files above for this story, noting each file's version.
2. Survey the codebase read-only, **by goal** (conventions [Goal-directed reading]). For each task, write the questions first ("Where is invoice sending triggered?", "Is there an existing job queue helper?"). Locate the answers with the repo map, search, symbols, and references, then read only the functions or line ranges that answer them. Cover where each touchpoint lives, existing code to reuse, the example file for each pattern you'll touch, installed packages against the install list, test setup, env config, and the migration tool. Run nothing that changes state.
3. **Reuse search.** For everything a task would create (module, function, component, helper, type, config), search for an existing one first and record the result in the reuse map.

## Phase C: Questions
Ask only what remains: conflicts between the docs and the code, a branch name if the convention leaves it open, local setup access (database, env vars), anything that blocks a task.
- A conflict about **product behavior** (the story says one thing, the existing product another, or the story is silent) is a query in `tracker.yaml` (`to: product`); the affected part waits for the answer.
- A conflict about a **technical decision** (the architecture or data model turns out wrong) goes back to dev-01-tech-design or dev-02-data-model in update mode; if it would change product behavior, it becomes a query first.

## Phase D: Plan (`dev/I-<nnn>-<slug>/04-build/<story-or-bug-id>-plan.md`)

```markdown
(header: pdlc_step "D04", initiative I-<nnn>, scope <story or bug ID>, depends_on [dev/architecture.md@x, dev/I-<nnn>-<slug>/01-tech-design.md@x, dev/I-<nnn>-<slug>/02-data-model/<scope>-<slug>.md@x, dev/I-<nnn>-<slug>/03-tasks/<scope>-<slug>.md@x, product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md@x])
# Build plan: [story or bug ID] [title]

## 1. Summary
What will exist when this is done, in a few lines.
## 2. Inputs read
| File | Version |
## 3. Codebase findings (Observed)
Relevant structure, the example file for each pattern touched, where each touchpoint lives (paths).
**Read map:** | Goal (question) | Files and line ranges read | What was learned |
**Reuse map:** | Task | Needed | Found (Observed path) or "none found" | Decision (reuse / extend / new) | Reason |
## 4. Conflicts and gaps
| # | Docs say | Code shows | Proposed resolution | Product query or technical? |
## 5. Packages
| Package | Version to pin | Install-list item | Task |
Nothing outside the install list unless approved in this plan.
## 6. Change list and budget
| Path | Create / modify / delete | What changes | Task / sub-task IDs |
Budget per task, from D03 and refined here: files touched and estimated lines added and removed. Code that becomes dead is listed for deletion.
## 7. Data and config
Migrations (with down steps), existing-data handling, seed data, env var names per environment (never values), feature flags.
## 8. Tests
The approved tests from the scope's test design (D05) are the definition of done and are **locked**: list their TC IDs and files. New tests are added only for TC IDs in the test design (ask D05 to add a case if one is missing); no test without a TC ID.
| TC ID | Covers (AC / EC / TH) | Level | File | Locked or new |
## 9. Order of work
Sub-tasks in dependency order, with commit points. No time estimates.
## 10. Risks and rollback
## 11. Out of scope
## 12. Implementation log
Filled during the build: deviations and why, decisions, test results, commits, and the **footprint**: lines added and removed per task against its budget, new files, new dependencies, reuse decisions taken, code deleted. Budget overruns past the team's threshold carry a reason.
## Change log
```

**Gate.** Show the plan and ask for explicit approval. If the person asks for changes, update the plan and ask again. If the agent has a planning mode, use it for Phases B to D; the plan still goes into the file.

## Phase E: Build
1. Create the branch per the convention in `dev/00-dev-setup.md`, and set the story, bug, or maintenance item to `in_progress` in `tracker.yaml` and its tasks to `in_progress` in the task file's `pdlc-tasks` block.
2. **Build in the sandbox** recorded in `dev/00-dev-setup.md`: a separate working copy, branch, or container, with no production credentials or data. Work through the order of work one sub-task at a time, and repeat until the required checks all pass: the approved tests, lint and type checks, the change budget, and the reuse map honored. After each sub-task, tick it in the plan and commit using the commit convention, with the story and task IDs.
3. **Lean code while building** (conventions [Lean code]): copy the example file's pattern; reuse what the reuse map found; write nothing that no task, AC, EC, threat, or NFR needs (no future-proofing abstractions, unused options, defensive branches, wrappers around one call, comments that restate code, or copied helpers); delete code your change makes dead. Approved tests are read-only. If one seems wrong, stop and raise it, don't edit it.
4. Small deviations inside the plan's intent go into the implementation log. Anything that changes product behavior, the architecture, the schema beyond D02, or the install list: stop and ask (product behavior as a query to product).
5. Never: edit files under `product/`; commit secrets or real credentials; run anything against pre-production or production; delete data; force-push a shared branch; skip, weaken, or delete tests to make them pass. Any destructive command needs the person's explicit OK first.

## Phase F: Finish
1. Fill the implementation log: what was done, test results, commits, remaining sub-tasks if any.
2. Record pinned package versions in the plan; with the person's OK, add them to the install list in `dev/architecture.md` (PATCH bump).
3. **Review against the requirements.** Before review by people, check the diff against every AC, EC, and threat mitigation the tasks implement, against the plan, and against the lean-code rules. Compare the footprint with the budget, and check for new helpers that duplicate existing ones and tests without a TC ID. Where a separate agent (sub-agent) is available, give it the diff, the cited IDs, and the owner files, but not your reasoning, and record its findings in the implementation log. Fix what is in scope; anything else becomes a query or a new item.
4. Merge per the convention in `dev/00-dev-setup.md`: open a pull request, or merge after the person's explicit OK. Never merge without one of the two. The pull request description gives reviewers what the risk tiers need: the TC IDs passing, the footprint against the budget, the reuse decisions, any change to locked tests (there should be none), and a list of the changes in line-by-line review areas (auth, money, personal data, deletion, migrations, secrets, and any tier the team added).
5. Update status: finished tasks and sub-tasks to `done` in the `pdlc-tasks` block; the story, bug, or maintenance item to `in_review` in `tracker.yaml` while its pull request is open, and to `in_qa` once merged. Run `lint --fix` and `board`.
6. Reply in one or two sentences: what was built, test results, anything left Open or waiting on a query. Next: dev-05-test-qa for this scope, or dev-04-code-plan-build for the next ready story.

## Using this skill in Cursor
The same SKILL.md works in Cursor, which loads skills from `.cursor/skills/`, `.agents/skills/`, and `.claude/skills/` (project or home folder) and can run them as `/dev-04-code-plan-build`. Where AskUserQuestion is not available, ask numbered plain-text questions; where SendUserFile is not available, write the plan into the product's docs location and give its path.
