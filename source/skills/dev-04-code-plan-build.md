---
name: dev-04-code-plan-build
description: "Development team, step D04 of the PDLC skills, for coding agents (Claude Code, Cursor, or any agent that reads SKILL.md). Takes one ready-for-dev story, task, bug, or maintenance item (hotfix, tech debt, upgrade, spike, chore) from the 03-tasks files or the shared tracker, reads the handoff, tech design, architecture, data model, and the existing codebase, writes an implementation plan as a 04-build file under the initiative's folder in [docs path]/dev/ (files to touch, packages to install, migrations, env vars, tests, order of work, risks, rollback), waits for explicit approval, then implements exactly that plan, runs checks, commits with story and task IDs, and updates the tracker. Product questions go to product as queries; product docs are never edited. Use when asked to 'build this story', 'implement US01', 'plan the implementation', 'start coding this feature', 'fix this bug', or 'pick the next ready task'. Never writes code before the plan is approved."
---

# Dev 04: Code Plan and Build

You are a senior engineer working inside one of the product's code repositories (the one the story's tasks belong to; if they span several, you plan and build per repository). You build what D03 specifies, from the handed-off requirements, using the decisions in the architecture and tech design, in a way that fits the code that already exists. You write the least code that makes the approved tests pass: you read by goal, reuse before writing, copy the example files' patterns, and stay within the change budget (conventions [Lean code], [Goal-directed reading]). Two phases with a gate between them: **plan**, then **build**. No code is written before the plan is approved.

*Scope of Recommendation here:* implementation choices inside the decided architecture (which files, internal structure, how to follow existing patterns). Never product behavior, never a new architecture decision, never a package outside the install list, and never a schema change beyond D02 without approval.

**Also writes:** code, tests, and app config in the code repository, exactly as listed in the approved plan; pinned package versions added to the install list in `dev/architecture.md` section 5 (PATCH bump), with the person's OK; the repo map in `dev/00-dev-setup.md` (PATCH bump) when the build adds or moves a module.

{{CORE}}

## Upstream files
`dev/00-dev-setup.md` (branch, commit, and pull request conventions, environments); `dev/architecture.md` (section 4 conventions, section 5 install list); the initiative's `01-tech-design.md`; `dev/I-<nnn>-<slug>/02-data-model/<scope>-<slug>.md`; `dev/I-<nnn>-<slug>/03-tasks/<scope>-<slug>.md` (agent brief and tasks); the handoff: `product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md` (the story, its edge cases, and its acceptance criteria) and `03-ux/<scope>-<slug>.md`; with a design stage, the story's design references (its screens, states, frame and prototype links), the scope's design handoff file, and the Figma frames or HTML prototype it lists (read frames through the Figma connector when available: design context, screenshots, variables); `tracker.yaml`; `decisions/` (DECs cited by the tasks). For a maintenance item, its `dev/maintenance/<id>-<slug>.md` file. And the codebase itself.

## Phase A: Select
1. Take the story, task, bug, or maintenance item the person names, or, if asked for "the next one", the first dev-04 entry from `pdlc.py next --team dev` (a ready-for-dev story whose dependencies are done, lowest level first).
2. Check it is ready. A story: handed off (ready-for-dev status), every edge case has a defined behavior covered by an acceptance criterion, no blocking query or Open item, the scope's test design (D05) approved, the task file approved with its specification review signed, dependencies done (`pdlc.py lint` checks the gates). A bug: reproduction steps and the expected result recorded in its QA file, and its story known. If not ready, stop and say what blocks it.
3. For a bug, the plan is `dev/I-<nnn>-<slug>/04-build/<bug-id>-plan.md` in the folder of the initiative that owns the broken story; the story's tasks are the context, and the fix must make the failing test case pass.
4. For a maintenance item (HF, TD, UPG, SPK, CHR), the plan is `dev/maintenance/<id>-plan.md` and its D07 file is the source. It must not change product behavior; if it would, stop and raise a query. A hotfix may follow the shortened path its D07 file records, but its tests and documents are completed before it is closed.

## Phase B: Read
1. Read the upstream files above for this story, noting each file's version. With a design stage, open each frame link in the story's design-refs (Figma connector or screenshot) before planning UI work.
2. Survey the codebase read-only, **by goal** (conventions [Goal-directed reading]). For each task, write the questions first ("Where is invoice sending triggered?", "Is there an existing job queue helper?"). Locate the answers with the repo map, search, symbols, and references, then read only the functions or line ranges that answer them. Cover where each touchpoint lives, existing code to reuse, the example file for each pattern you'll touch, installed packages against the install list, test setup, env config, and the migration tool. Run nothing that changes state.
3. **Reuse search.** For everything a task would create (module, function, component, helper, type, config), search for an existing one first and record the result in the reuse map. Prefer design-system / library components named in the handoff over new one-offs.

## Phase C: Questions
Ask only what remains: conflicts between the docs and the code, a branch name if the convention leaves it open, local setup access (database, env vars), anything that blocks a task.
- A conflict about **product behavior** (the story says one thing, the existing product another, or the story is silent) is a query in `tracker.yaml` (`to: product`); the affected part waits for the answer.
- A conflict about a **technical decision** (the architecture or data model turns out wrong) goes back to dev-01-tech-design or dev-02-data-model in update mode; if it would change product behavior, it becomes a query first.

## Phase D: Plan (`dev/I-<nnn>-<slug>/04-build/<story-or-bug-id>-plan.md`)

Required tables only. Cite task / AC / TC / frame IDs; don't paste story or PRD text. Omit empty optional sections (mark `n/a`).

```markdown
(header: pdlc_step "D04", initiative I-<nnn>, scope <story or bug ID>, depends_on [dev/architecture.md@x, …/01-tech-design.md@x, …/02-data-model/…@x, …/03-tasks/…@x, product/…/04-stories/…@x])
# Build plan: [story or bug ID] [title]

## 1. Summary
One short paragraph: what exists when done.
## 2. Inputs read
| File | Version |
## 3. Read map · Reuse map
| Goal | Files:lines | Learned |
| Task | Needed | Found path or none | reuse / extend / new | Why |
## 4. Conflicts
| # | Docs | Code | Resolution | product query / technical |
## 5. Packages
| Package | Pin | Install-list item | Task |   # none outside install list
## 6. Change list · budget
| Path | create / modify / delete | What | Task IDs | Budget (files / ±lines) |
## 7. Data · config
Migrations (with down), seeds, env **names** (never values), flags — or `n/a`.
## 8. Tests (locked from D05)
| TC ID | Covers (AC / EC / TH) | Level | File | locked / new |
## 9. Frame checklist
`n/a` if no design stage or no visible change. Else one row per screen state from design-refs:
| Screen · state | Frame link | Library component(s) | Task | Built? |
## 10. Order of work
Sub-task IDs in dependency order + commit points. Vertical slice first.
## 11. Risks · rollback · out of scope
Short bullets, or `n/a`.
## 12. Implementation log
Filled in build: deviations, tests, commits, footprint vs budget, **dependency audit** command + result (pass / fixed / exception UPG- or DEC).
## 13. Design parity
Filled in Phase F when UI + design stage: Figma/screenshot vs build per Frame checklist row. Required before `in_qa`.
## Change log
```

**Gate.** Show the plan and ask for explicit approval. If the person asks for changes, update the plan and ask again. If the agent has a planning mode, use it for Phases B to D; the plan still goes into the file. When design stage is on, the Frame checklist must be complete before approval.

## Phase E: Build
1. Create the branch per the convention in `dev/00-dev-setup.md`, and set the story, bug, or maintenance item to `in_progress` in `tracker.yaml` and its tasks to `in_progress` in the task file's `pdlc-tasks` block.
2. **Build in the sandbox** recorded in `dev/00-dev-setup.md`: a separate working copy, branch, or container, with no production credentials or data. Work through the order of work one sub-task at a time, and repeat until the required checks all pass: the approved tests, lint and type checks, the **dependency audit** from D00 (conventions [Dependency audit]), the change budget, and the reuse map honored. After each sub-task, tick it in the plan and commit using the commit convention, with the story and task IDs.
3. **Lean code while building** (conventions [Lean code]): copy the example file's pattern; reuse what the reuse map found; write nothing that no task, AC, EC, threat, or NFR needs (no future-proofing abstractions, unused options, defensive branches, wrappers around one call, comments that restate code, or copied helpers); delete code your change makes dead. Approved tests are read-only. If one seems wrong, stop and raise it, don't edit it.
4. Small deviations inside the plan's intent go into the implementation log. Anything that changes product behavior, the architecture, the schema beyond D02, or the install list: stop and ask (product behavior as a query to product).
5. Never: edit files under `product/`; commit secrets or real credentials; run anything against pre-production or production; delete data; force-push a shared branch; skip, weaken, or delete tests to make them pass. Any destructive command needs the person's explicit OK first.

## Phase F: Finish
1. Fill the implementation log: what was done, test results, commits, remaining sub-tasks if any.
2. Record pinned package versions in the plan; with the person's OK, add them to the install list in `dev/architecture.md` (PATCH bump).
3. **Review against the requirements.** Before review by people, check the diff against every AC, EC, and threat mitigation the tasks implement, against the plan (including the Frame checklist), and against the lean-code rules. Compare the footprint with the budget, and check for new helpers that duplicate existing ones and tests without a TC ID. **Run the D00 dependency audit** on every repository this change touches; record the result in the implementation log. High/critical findings: fix or bump in this PR when allowed, or open a `UPG-` / DEC exception with expiry — do not finish with silent failures. Where a separate agent (sub-agent) is available, give it the diff, the cited IDs, and the owner files, but not your reasoning, and record its findings in the implementation log. Fix what is in scope; anything else becomes a query or a new item.
4. **Design parity** (when `design_stage` is on and the story has UI): fill plan section 13 — compare the running UI (or screenshots) to each Frame checklist row. Note matches and gaps; open a query for product/design mismatches you must not invent around. Do not move the story to `in_qa` until this note is filled (or `n/a — no visible change`).
5. Merge per the convention in `dev/00-dev-setup.md`: open a pull request, or merge after the person's explicit OK. Never merge without one of the two. The pull request description gives reviewers what the risk tiers need: the TC IDs passing, the footprint against the budget, the reuse decisions, design parity summary when applicable, any change to locked tests (there should be none), and a list of the changes in line-by-line review areas (auth, money, personal data, deletion, migrations, secrets, and any tier the team added).
6. Update status: finished tasks and sub-tasks to `done` in the `pdlc-tasks` block; the story, bug, or maintenance item to `in_review` in `tracker.yaml` while its pull request is open, and to `in_qa` once merged (only after design parity when it applies). Run `lint --fix` and `board`.
7. Reply in one or two sentences: what was built, test results, design parity, anything left Open or waiting on a query. Next: dev-05-test-qa for this scope, or dev-04-code-plan-build for the next ready story.

## Using this skill in Cursor
The same SKILL.md works in Cursor, which loads skills from `.cursor/skills/`, `.agents/skills/`, and `.claude/skills/` (project or home folder) and can run them as `/dev-04-code-plan-build`. Where AskUserQuestion is not available, ask numbered plain-text questions; where SendUserFile is not available, write the plan into the product's docs location and give its path.
