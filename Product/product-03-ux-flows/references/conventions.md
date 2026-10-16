# PDLC conventions (reference for every skill of the chain)

This file holds the full rules that the PDLC core in each SKILL.md summarizes. Read the section you need; you don't need to read it all on every run.

## Steps

| Team | Step | Skill | Works on | Writes (under the docs path) |
|---|---|---|---|---|
| Any | – | pdlc-next | product | nothing; regenerates `tracker.md` and answers "what next", "where are we", "what is open" |
| Product | P00 | product-00-product-context | product | `product/00-product-context.md`; creates `tracker.yaml` |
| Product | P01 | product-01-feature-brainstorm | one initiative | `product/I-<nnn>-<slug>/01-brainstorm.md` |
| Product | P02 | product-02-prd | one initiative | `product/I-<nnn>-<slug>/02-prd.md` |
| Product | P03 | product-03-ux-flows | one scope | `product/I-<nnn>-<slug>/03-ux/<scope>-<slug>.md`, `product/_sitemap.md` |
| Product | P04 | product-04-user-stories | one scope | `product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md` |
| Product | P05 | product-05-change-request | any time | `product/change-requests/CR-<nnn>-<slug>.md` |
| Product | P06 | product-06-project-tracker | any time | `tracker.yaml` (versions, sprints, statuses, queries, CRs), exports |
| Product | P07 | product-07-launch | one released version | `product/launch/<version>.md` |
| Design | G00 | design-00-design-setup | product | `design/00-design-setup.md` |
| Design | G01 | design-01-sitemap-flows | one initiative | `design/I-<nnn>-<slug>/01-sitemap-flows.md` + FigJam charts |
| Design | G02 | design-02-screen-mockups | one scope | `design/I-<nnn>-<slug>/02-mockups/<scope>-<slug>.md` + frames or HTML prototype |
| Design | G03 | design-03-design-handoff | one scope | `design/I-<nnn>-<slug>/03-handoff/<scope>-<slug>.md` (the design handoff) |
| Development | D00 | dev-00-dev-setup | product | `dev/00-dev-setup.md` |
| Development | D01 | dev-01-tech-design | baseline, then one initiative | `dev/architecture.md`; `dev/I-<nnn>-<slug>/01-tech-design.md` |
| Development | D02 | dev-02-data-model | one handed-off scope | `dev/I-<nnn>-<slug>/02-data-model/<scope>-<slug>.md`, `dev/_shared-entities.md` |
| Development | D03 | dev-03-build-tasks | one handed-off scope | `dev/I-<nnn>-<slug>/03-tasks/<scope>-<slug>.md` (`pdlc-tasks` blocks and the specification review) |
| Development | D04 | dev-04-code-plan-build | one story, bug, or maintenance item | `dev/I-<nnn>-<slug>/04-build/<id>-plan.md` (or `dev/maintenance/<id>-plan.md`), plus code |
| Development | D05 | dev-05-test-qa | one scope (test design first, results later) or version | `dev/I-<nnn>-<slug>/05-qa/<scope>-<slug>.md` or `dev/releases/<version>-qa.md` |
| Development | D06 | dev-06-deploy | one version or event | `dev/releases/<version-or-event>.md` |
| Development | D07 | dev-07-maintenance | one maintenance item | `dev/maintenance/<id>-<slug>.md` |
| Any | DEC | (written by any step) | one decision | `decisions/DEC-<nnn>-<slug>.md` |

## Flow

- **Product:** P00 once. Then, per initiative, P01 and P02. Then, per scope, P03 and P04.
- **Design** (when the product has a design stage): G00 once. Then G01 per initiative, then G02 and G03 per scope.
- **Development:** D00 and the D01 baseline once. Then D01 per initiative. Per handed-off scope:
  1. D02, the data model.
  2. D05 in test-design mode: test cases written from the acceptance criteria, edge cases, and threats, before any code.
  3. D03, the tasks plus the specification review, which approves the design, criteria, constraints, and tests together.
  4. D04 per story: the agent builds in a sandbox until the approved tests pass.
  5. D05 again, recording results.

**Release order:**
1. The team chooses a version's items, and P06 checks them against dependencies.
2. D06 deploys the version to pre-production.
3. D05 tests it there.
4. D06 promotes it to production on a Go.
5. P07 prepares the launch kit for the released version.

**Any time:**
- P05 handles change requests.
- P06 handles tracking.
- D07 handles maintenance items: hotfixes, tech debt, upgrades, spikes, and chores.
- pdlc-next answers "what next".

## Product locations

The skills name no repository. Every product has its own locations, and every run uses only those of the product it works on.
- **Docs location:** where this product's documentation lives, as a repository (or other store), a branch, and a folder. It can be a docs folder inside a code repository, a separate docs repository, or a path in a monorepo. The folder that holds the chain files is the **docs path**: `docs/pdlc/` unless `product/00-product-context.md` records another.
- **Code repositories:** zero or more per product (for example a web app, an API, a mobile app, infrastructure). They are recorded in `product/00-product-context.md` (name, link, what each holds) and detailed in `dev/00-dev-setup.md`. When a product has more than one, every task, plan, and QA item names the repository it belongs to.
- **Read first:** before asking, read what the docs location already says (existing specs, architecture notes, ADRs, READMEs, earlier chain files). Where it helps, also read the code repositories, read-only, to learn how the product works today. Facts found there are Observed: cite the path, and never ask for them again. Product and design steps read code only to understand current behavior; they never choose implementation.
- **Generated anywhere, kept in the docs location:**
  - A file may be generated anywhere (a laptop, a chat, a Claude project), but it must be committed to its path under the docs path.
  - `depends_on`, tracker sources, and cross-references always use paths relative to the docs path.
  - The other teams build nothing on a file that isn't committed. `pdlc.py` lists such files as "not committed".
- **One product at a time:** facts, IDs, paths, and files of one product are never used for another.

## Team boundary

**Product decides what; Design decides how it looks and is laid out; Development decides how it is built.**
- **Product files** state problems, scope, requirements, business rules, flows, screens, stories, edge cases, and acceptance criteria. They never choose technology, architecture, schema, APIs, or implementation, unless a Provided constraint requires it.
- **Design files and frames** show the screens, states, and visual structure of what Product defined. They never add, drop, or change a feature, role, rule, flow, Product-provided copy, or acceptance criterion, and they never choose technology.
- **Development files** decide architecture, schema, tasks, code, tests, infrastructure, and releases. They never change product behavior, scope, requirements, flows, edge-case behavior, or acceptance criteria.
- **Where each team writes:** in its own folder (`product/`, `design/`, `dev/`). Any team may write to `tracker.yaml` and `decisions/`. The one bounded exception is the design reference fields in product files (see Design references). Product owns the structure of `tracker.yaml`: versions, queries, change requests, and statuses.

## Handoff

A scope is handed off when its stories carry the ready-for-dev status. How a scope gets there depends on whether the product has a design stage:

| Product | Scope | P04 approval moves stories to | Ready for dev when |
|---|---|---|---|
| No design stage | any | ready for dev | at P04 approval |
| Design stage¹ | no screens (P03 is n/a) | ready for dev | at P04 approval |
| Design stage¹ | has screens | in design | the scope's G03 design handoff is approved |

¹ `design/00-design-setup.md` is approved, or `config.design_stage: true` is set in `tracker.yaml`.

**The handoff package:**
- the stories file
- the initiative's `02-prd.md`
- the scope's `03-ux` file
- with a design stage, the scope's `03-handoff` file and the frames or prototype it lists

Development uses the versions pinned in the stories file's header and builds only from handed-off scopes.

## Queries

When design or development finds a gap, conflict, or ambiguity in what it was handed, it never fills it with a guess. It adds a query to `tracker.yaml`:

```yaml
queries:
  - id: Q-004              # pdlc.py new-id query
    question: Can a bulk send mix currencies?
    about: [M01.S02.F01-US02]
    raised_by: D01         # step that raised it
    to: product            # product | design | dev
    blocking: true
    status: open           # open | answered | became_cr
    answer:                # file@version that answers it, or the CR ID
```

- **Blocking queries:** a blocking query moves the stories it is about to the blocked status. Answering it returns them to their previous status.
- **Who answers:** product answers by updating its own file in update mode (PATCH for wording, MINOR for added detail) and recording the answer. When the answer changes a requirement, it goes through a change request.
- **Where questions go:** content and behavior questions go to Product; questions about a frame go to Design; technical questions stay in Development.

## Change requests

Only product-05-change-request changes an approved requirement, flow, story, edge case, or acceptance criterion. Design and development raise a query when they think such a change is needed. Development changes its own technical decisions by re-running its own step in update mode, with the reason in the change log and a DEC entry. If that would change product behavior, it raises a query first.

## Design references

Whatever the design team creates for a product feature is written back to the product files that define it. That way a reader of a story finds its screens and prototype, and a reader of a frame finds its story. Design steps may add and update only these fields in product files, and nothing else:

1. **In each story of the stories file:** a block between `<!-- design-refs:start -->` and `<!-- design-refs:end -->`, with one line per screen the story cites, in this form:
   - Line: `Screen ID · states (AC IDs shown) -> frame or prototype link; prototype FLnn -> link · mockups file@version · draft | approved | stale`
   - A story with no visible change gets `no visible change (reason)`.
   - A story whose screen isn't designed yet gets `not yet designed`.
2. **In the UX file:** the Figma column of the screen inventory, and the link line under each flow chart.
3. **In `product/_sitemap.md`:** the Design column of the Screens table, and the link line under its chart.

**How writes are versioned:** each write is a PATCH bump of the product file with a change-log row "design references (G0x)". Status, approval, and content are unchanged. Product steps in update mode keep these fields exactly as they are.

**Stale references:** a reference is `stale` when its frame was deleted or renamed, or when the story or UX file it sits in changed by a MAJOR or MINOR version. The next G02 run refreshes it. `pdlc.py lint` reports stories that are handed off with missing, stale, or not-yet-designed references.

## Requirement syntax (EARS)

Functional requirements, business rules, non-functional requirements, task build lines, and the rules given to coding agents are written in the Easy Approach to Requirements Syntax (EARS). Each one is a single sentence in one of these patterns:

| Pattern | Form | Use for |
|---|---|---|
| Ubiquitous | The [system] shall [response]. | always true |
| Event-driven | When [trigger], the [system] shall [response]. | a response to an event |
| State-driven | While [state], the [system] shall [response]. | behavior during a state |
| Unwanted behavior | If [unwanted condition], then the [system] shall [response]. | errors, faults, abuse |
| Optional feature | Where [feature or plan is present], the [system] shall [response]. | plans, tiers, configuration |
| Complex | While [state], when [trigger], the [system] shall [response]. | combinations of the above |

- **The [system]** is the product, a named feature, or a named role's view of it. It is never a technology.
- **"shall"** is mandatory; **"shall not"** is a prohibition. Nothing else in the sentence is optional: no "should", "may", "etc.", or "as appropriate".
- **One response per requirement.** If a sentence needs "and" between two responses, split it into two IDs.
- **Measurable words only.** Replace "fast", "easy", and "secure" with what users or the business can check (a number Provided by the team, or Open).
- **Acceptance criteria are not EARS.** They stay in Given/When/Then form, because each one is a test scenario. Each criterion cites the requirement or rule it verifies, for example `AC02 (verifies M01.S02.F01-FR02)`.
- **Lint:** `pdlc.py lint` checks that every FR, BR, and NFR row in a PRD matches an EARS pattern.

## Specification review and tests first

Reviewing every line an agent writes doesn't scale. Development reviews the **specification and the tests** before any code, then lets the coding agent build in an isolated sandbox until the approved tests pass. Line-by-line review is kept for the code where it matters most.

1. **Tests first (D05, test-design mode).** For a handed-off scope, D05 writes the test cases before any build: one or more per acceptance criterion, edge case, applicable threat mitigation (TH), and eval case (EV). Each one has its level and its expected result, citing the IDs it covers. With the person's approval, the automated tests are written as failing tests. A person reviews the tests, not just their names.
2. **Specification review charter (D03).** Before any story is built, the reviewers named in `dev/00-dev-setup.md` approve, together:
   - the architecture and tech-design decisions the stories use
   - the acceptance criteria and edge cases, as handed off
   - the constraints (NFRs, threat mitigations, compliance)
   - the test design, with every criterion covered
   - the tasks and their change budgets

   D03 is approved only when this review is signed. It is the gate for D04.
3. **Sandbox build (D04).** The coding agent works in an isolated working copy, branch, or container, with no production credentials and no access to production data. It iterates until every required check passes: the approved tests, lint and type checks, the change budget, and the reuse map. Approved tests are read-only to the agent. Changing, skipping, or weakening one needs the reviewers' approval again, recorded in the plan.
4. **Risk-tiered human review.** Reviewers don't re-read all generated code. They check:
   - that tests were not weakened
   - every change-budget exception and every new module, helper, or package
   - the reuse map
   - **line by line**, any change touching authentication and permissions, money, personal data, data deletion, migrations, cryptography and secrets, or another tier the team adds in `dev/00-dev-setup.md`
5. **When the tests pass but the behavior is wrong,** the specification or the tests were wrong. The fix goes back to the owning step (a query to product, or a D05 update), not just to the code.

## Lean code

Agents write more code than a task needs because writing is cheaper for them than reading. These rules make lean code checkable:
- **Reuse before writing.** Before creating a module, function, component, or helper, search the code repositories for an existing one. The build plan's **reuse map** lists, per task, what was found (Observed paths) and the decision: reuse, extend, or new, with a reason. "New" is allowed only when the search found nothing suitable.
- **Follow the example files.** `dev/architecture.md` section 4 names one example file per pattern (async style, error handling, data access, validation, logging, components, tests). New code copies the pattern of the example, never a second style. Formatter, linter, and type-check rules in CI enforce what they can.
- **Change budget.** The build plan estimates, per task, the files touched and the size of the change (lines added and removed). An overrun beyond the team's threshold (recorded in `dev/00-dev-setup.md`) needs a written reason in the implementation log, and a reviewer checks it. Skills never invent the threshold.
- **No speculative code.** Every new function, class, branch, parameter, and configuration value traces to a task ID. None of the following unless an acceptance criterion, edge case, threat, or NFR requires it:
  - abstractions "for the future"
  - unused parameters or options
  - defensive branches
  - generic wrappers around one call
  - comments that restate the code
  - copied helpers
- **Delete what you replace.** Code made dead by the change is removed in the same change.
- **No test slop.** Each test implements a test case (TC) and is named with its ID. No tests of the framework, trivial getters, or private details. No large snapshots unless a test case asks for one, and no duplicated tests at several levels without a reason. Mutation testing, where the team uses it, shows whether the tests would catch a real fault.
- **Report the footprint.** The implementation log records lines added and removed, new files, new dependencies, and reuse decisions, so reviewers see the size before reading.

## Goal-directed reading

Agents read code to answer questions, not to digest files. This follows the idea of intent-based context pruning (for example SWE-Pruner, arXiv 2601.16746), applied as a working method rather than a tool:
1. **State the goal first.** Before opening code, write the question, for example "Where is error handling triggered for invoice sends?".
2. **Locate, then read.** Use the repo map in `dev/00-dev-setup.md`, then search (text, symbols, the language server, references). Read only the functions or line ranges the goal needs, plus their direct callers and callees when behavior depends on them.
3. **Keep a read map.** The build plan lists each goal, the files and line ranges read, and what was learned. That way reviewers, and the next run, don't repeat the reading.
4. **Widen deliberately.** Read a whole file only when the goal needs its full structure (for example a module being refactored), and say why.

## Planning principles

- **Built on the actual product.** `product/00-product-context.md` holds the product as it is: users and roles, the product map, business rules, and constraints. Every initiative states what it adds, what it changes, and which existing behavior must not change.
- **Requirements are the single source of truth.**
  - The PRD and the product files built from it decide what exists.
  - For development, the handoff package is the source of truth.
  - Nothing is planned that doesn't trace to a requirement, or, for maintenance items, to a recorded reason.
  - No skill drops, defers, or trims a requirement.
- **Full scope of every initiative.** No MVP, phase, or release slice is applied by default. Leaving something out is the person's decision, recorded as Out of scope with their reason. The team may still put any subset of done items into a version; P06 checks that its dependencies are met.
- **Order comes only from dependencies.** Every plan is a dependency order, expressed as dependency levels:
  - Level 0 depends on nothing that is still to be built.
  - Level n depends only on items at lower levels.
  - Dependencies on existing features and on other initiatives count.
  - Items on the same level have no order between them.
  - `pdlc.py` computes the levels; nobody assigns them by hand.
- **Timelines belong to the team.** No skill proposes dates, durations, deadlines, sprint contents, time-based phases, capacity, estimates, or priorities. When the team provides them, they are recorded as Provided and never change the dependency order.

## Initiatives

An initiative is one new feature or one expansion of existing features, started in P01 (or P02 when a write-up already exists).
- **IDs:** `I-001`, `I-002`, and so on, allocated with `pdlc.py new-id initiative`.
- **Files:** they live in `product/I-<nnn>-<slug>/`, `design/I-<nnn>-<slug>/`, and `dev/I-<nnn>-<slug>/`.
- **Scopes:** an initiative's scopes are listed in `tracker.yaml` under the initiative. The first scope-level run for a scope adds it.

## IDs

IDs are never renumbered or reused; a removed item keeps its ID with the status removed. Allocate every new ID with `pdlc.py new-id`, which reads every file and the tracker. Without the script, find the highest number already used under the same parent and take the next.

| Kind | Form | Owner file | `new-id` kind |
|---|---|---|---|
| Module > sub-module > feature | `M01`, `M01.S01`, `M01.S01.F01` | product map (`00-product-context.md`), PRD placement | module, sub-module, feature |
| Functional requirement | `M01.S01.F01-FR01` | PRD | fr |
| Business rule | `M01.S01.F01-BR01` | PRD | br |
| Non-functional requirement | `I-001-NFR01` | PRD | nfr |
| Story | `M01.S01.F01-US01` | stories file | story |
| Edge case | `M01.S01.F01-EC01` | stories file (feature register) | ec |
| Acceptance criterion | `M01.S01.F01-US01-AC01` (inside its story, `AC01` is enough) | stories file | ac |
| Flow, screen | `<scope>-FL01`, `<scope>-SC01` (scope of the run that created it) | UX file | fl, sc |
| Task, sub-task | `M01.S01.F01-US01-T01`, `...-T01-ST01` | task file (`pdlc-tasks` block) | task, subtask |
| Test case | `M01.S01.F01-US01-TC01` | QA file | tc |
| Initiative | `I-001` | `tracker.yaml` | initiative |
| Query, change request, bug | `Q-001`, `CR-001`, `BUG-001` | `tracker.yaml` | query, cr, bug |
| Decision | `DEC-001` | `decisions/DEC-001-<slug>.md` | dec |
| Hotfix, tech debt, upgrade, spike, chore | `HF-001`, `TD-001`, `UPG-001`, `SPK-001`, `CHR-001` | `tracker.yaml` + `dev/maintenance/` | hf, td, upg, spk, chr |
| Architecture layer | `L1` to `L13` | `dev/architecture.md` | – |

- **M00:** reserved for platform foundations (for example base auth, shared layout, a job runner). Development owns them: D01 defines their sub-modules, features, and enabler stories, and later steps treat them like any scope.
- **Versions:** written in the scheme recorded in `product/00-product-context.md`.

**Reference by ID, don't copy.**
- A later file cites an ID with a short title (`M01.S02.F01-BR01 drafts only`). It never restates the requirement, rule, criterion, or decision.
- Coding agents and testers read the owner file for the wording.
- `pdlc.py lint` checks that every cited FR, BR, NFR, US, EC, AC, SC, FL, TC, Q, CR, BUG, DEC, and maintenance ID exists in its owner file or the tracker.
- The pinned `depends_on` versions show whether that owner file has moved on since.

## Statuses

`tracker.yaml` stores the status of every item as a fixed role key, and `config.statuses` maps each role to the team's own name. `tracker.md` shows the team's names.

| Role key | Meaning |
|---|---|
| `backlog` | known, not yet in definition |
| `in_definition` | product is defining it |
| `in_design` | approved by product, waiting for the design handoff (design stage only) |
| `ready_for_dev` | handed off |
| `in_progress` | |
| `in_review` | pull request open |
| `in_qa` | merged, under test |
| `done` | |
| `released` | |
| `blocked` | |
| `removed` | |

Tracking fields (status, `dep_level`, fix version, priority, estimate) can change without a `doc_version` bump of any file.

## Environments

Environment names come from `dev/00-dev-setup.md`, where each environment is marked local development, pre-production, or production. Skills refer to these roles, never to fixed names.

## Scope units and touchpoints

| Step | Covers |
|---|---|
| P00, G00, D00 | the whole product |
| P01, P02, G01, D01 | one initiative |
| P03, P04, G02, G03, D02, D03 | one scope (a module, sub-module, or feature from the initiative's PRD) |
| D04 | one story, bug, or maintenance item |
| D05 | one scope or one version |
| D06 | one version or event |
| D07 | one maintenance item |
| P07 | one released version |

- **Scope level:** within an initiative, a scope's level is fixed at its first scope-level run and recorded in `tracker.yaml`.
- **No overlaps:** two runs of the same step never cover overlapping scopes of one initiative; extend the existing file instead.
- **Narrower scopes:** a scope inside a scope already handled at a higher level reads the nearest ancestor's file for that step.
- **Steps that don't apply:** a step that doesn't apply to a scope is recorded under the scope in `tracker.yaml` as `na: {P03: "no screens"}`, and later steps don't expect its file.
- **What a scope run reads:** the product-wide files, its initiative's files, its own upstream files, and the files of every scope or existing feature it touches.

Every scope file has a **Touchpoints** section:

| Touches (scope, existing feature, or other initiative) | Direction (needs / provides) | What is shared (information, screen, rule, event, entity, API) | Its status | Blocking? |
|---|---|---|---|---|

A touchpoint into something not yet at this step is Open, marked blocking or not. A blocking "needs" touchpoint is also added to the `depends_on` of the affected items in `tracker.yaml`.

## File header

Every chain file starts with the front matter shown in the core and ends with a Change log table (version | date | change | CR, query, or DEC).

**Version bumps:**

| Bump | When | Effect on later files |
|---|---|---|
| MAJOR | meaning or scope changed | they become stale |
| MINOR | items added | they become stale |
| PATCH | wording, version pinning, design references, query answers that only clarify, recording test results and run evidence | never makes a file stale |

- **`depends_on`:** lists upstream files as `path@version`, with paths relative to the docs path.
- **`open_items` and `blocking`:** count the file's Open items and give the numbers of the blocking ones, so `pdlc.py open` can show them all in one view.
- **`status`:** `approved` only on the explicit OK of the person or the recorded approver. An approved file with blocking Open items is reported by lint.

## Tracker data

`tracker.yaml` (in the docs path) is the source of all tracking data. `pdlc.py board` generates `tracker.md` from it and from the file headers: the summary, initiative board, what next, open items and queries, blocked items, stale files and lint findings, items by dependency level, versions, and change requests. The initiative board is derived, never written by hand. History lives in git and in the change logs, so there is no hand-kept activity log.

```yaml
# tracker.yaml
product: Ledgerly
config:
  design_stage: true            # whether the product has a design stage
  version_scheme: semver
  statuses: {backlog: Backlog, in_definition: In definition, in_design: In design, ready_for_dev: Ready for dev,
             in_progress: In progress, in_review: In review, in_qa: In QA, done: Done, released: Released,
             blocked: Blocked, removed: Removed}
  external_tool:                # e.g. Jira, with the field mapping in product-00 (exports only on request)
initiatives:
  - id: I-001
    title: Bulk invoicing
    slug: bulk-invoicing
    status: in_progress
    scopes:
      - id: M01.S02
        na: {D02: "no data change"}
items:                          # modules, sub-modules, features, stories, bugs, maintenance items
  - {id: M01.S02.F01, type: feature, parent: M01.S02, title: Bulk send, status: in_progress, initiative: [I-001],
     source: product/I-001-bulk-invoicing/02-prd.md}
  - id: M01.S02.F01-US02
    type: story                 # module | sub-module | feature | story | bug | hotfix | tech_debt | upgrade | spike | chore
    parent: M01.S02.F01
    initiative: [I-001]
    scope: M01.S02
    title: Send selected invoices
    status: ready_for_dev       # a role key
    depends_on: [M01.S02.F01-US01]
    dep_level: 1                # written by pdlc.py lint --fix
    fix_version:                # team-set only
    priority:                   # team-set only
    estimate:                   # team-set only
    source: product/I-001-bulk-invoicing/04-stories/M01.S02-bulk-actions.md
queries: []                     # see Queries
versions:
  - {id: v1.4.0, goal: Bulk send, status: planned, file: }   # planned | in_progress | staged | released | rolled_back
sprints: []                     # only if the team uses sprints; every field team-set
change_requests:
  - {id: CR-001, title: , initiative: I-001, status: draft, file: }   # draft | approved | applied | rejected
```

**Tasks and sub-tasks** are not in `tracker.yaml`. D03 writes them in the scope's task file as a fenced block whose info string is `yaml pdlc-tasks`. D04 updates their status there. `pdlc.py` reads them for dependencies, levels, counts, and the board.

````markdown
```yaml pdlc-tasks
- id: M01.S02.F01-US02-T01
  title: Bulk send endpoint and job
  layer: api                    # database | api | backend | frontend | ui | auth | security | caching | rate-limiting | logging | config | qa
  repo: api                     # code repository, when the product has more than one
  status: in_progress
  depends_on: [M01.S02.F01-US01-T01]
  implements: [M01.S02.F01-US02-AC01, M01.S02.F01-US02-AC02]
  subtasks:
    - {id: M01.S02.F01-US02-T01-ST01, title: Skip invoices without email, status: backlog}
```
````

**Definitions the tracker enforces:**
- **Ready for dev (story):**
  - every edge case it lists has a defined behavior covered by an acceptance criterion
  - its acceptance criteria are complete, and no blocking question is Open
  - its dependencies are known and its product handshake is complete
  - the screens it cites are in an approved UX file (or UX is n/a)
  - its stories file is approved
  - with a design stage and screens: the scope's G03 is approved and its design references are present and not stale
- **Definition of done (story):**
  - every task and sub-task is done
  - every test case for its acceptance criteria and edge cases passes (D05)
  - the code is merged and the affected docs are updated
- **A bug's parent** is the story it breaks. A maintenance item's source is its `dev/maintenance/` file.

**CI.** P00 and D00 offer to copy `scripts/pdlc.py` into the docs path (`<docs>/.pdlc/pdlc.py`) and to add the CI workflow from `references/ci-pdlc-lint.yml`. That workflow runs `lint` on every change to the docs path and fails on errors.

## Decision log

A decision of record is one whose reasoning a later reader needs:
- a scope cut or an Out-of-scope choice
- a priority the team sets
- the outcome of a change request
- an architecture or technology choice (an ADR)
- a spike's result
- a design-system rule
- a compliance interpretation
- a trade-off accepted with risk

Any step that makes one writes `decisions/DEC-<nnn>-<slug>.md` (header `pdlc_step: "DEC"`, scope the DEC ID):

```markdown
# DEC-[nnn]: [decision in one line]
Owner: product / design / development. Status: proposed / accepted / superseded by DEC-[nnn].
Context: [what forced the decision, with IDs]
Options considered: [each with its trade-offs]
Decision: [what was chosen] (Label)
Consequences: [what follows, including what becomes harder]
Links: [FR, US, L, CR, Q IDs]
```

- **Citing decisions:** change logs and files cite the DEC ID instead of repeating the reasoning.
- **Changing a decision:** a new DEC supersedes the old one; the old file stays.

## Maintenance items

Work without a product requirement still has a route, through dev-07-maintenance:

| Type | Use for |
|---|---|
| hotfix (`HF-`) | a production defect that cannot wait |
| tech_debt (`TD-`) | known shortfalls in code or architecture |
| upgrade (`UPG-`) | dependency, runtime, or platform upgrades |
| spike (`SPK-`) | a time-boxed investigation that ends in a DEC |
| chore (`CHR-`) | operational tasks with no behavior change |

- **Behavior changes go back to Product.** A maintenance item may not change product behavior. If it would, it raises a query to Product, or Product opens a CR.
- **Hotfixes:** a hotfix may ship before its documents are complete, but it is not closed until its D07 file, its tests, and any product answer are recorded.
- **Execution:** D04, D05, and D06 run maintenance work like a story, with the D07 file as its source.

## Reference packs

Some skills include extra reference files in `references/`. Read one only when it applies:

| Pack | Read when |
|---|---|
| `compliance.md` | the product handles personal data, payments, tax invoices, health or financial records, or operates in a regulated market. These are checklists of questions to verify against current official sources, never legal facts. |
| `threat-model.md` | dev-01 designs an initiative or the baseline, or a change touches authentication, permissions, personal data, payments, or external input. |
| `ai-features.md` | a feature uses AI models, from requirements (behavior, eval set, thresholds) to design, build, test, and operations. |
| `ci-pdlc-lint.yml` | setting up the CI check in a product's repository. |
