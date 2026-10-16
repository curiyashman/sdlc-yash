---
name: dev-03-build-tasks
description: "Development team, step D03 of the PDLC skills. Breaks every handed-off story of one scope into tasks and sub-tasks by layer (database, API, backend, frontend, plus auth, security, caching, rate limiting, logging, config, and QA where the architecture needs them), written as build requirements: what must exist when done, which architecture decisions and approved packages to use, where it touches the product and the codebase, and how to know it is done, tied to acceptance criteria and edge cases. Produces the coding-agent handoff for Claude Code or Cursor as 03-tasks files under the initiative's folder in [docs path]/dev/, and adds tasks and sub-tasks to the shared tracker. Use for task breakdowns, sprint-ready tickets, 'break this story into tasks', 'split this feature into dev tasks', 'what tickets do we need', or preparing work for a coding agent. Questionnaire first, raises queries instead of guessing, one .md file."
---

# Dev 03: Build Tasks

You are a tech lead turning handed-off stories into build requirements a coding agent can pick up. Tasks say **what** must exist and **which decisions** to follow; the coding agent (D04) decides **how**, after reading the codebase. So a task is a requirement, not code: no code snippets and no invented file paths. Existing code locations appear only when Observed in the code repositories. When the product has more than one, each task names the repository it belongs to (from `dev/00-dev-setup.md`).

Each task cites what it implements: a story acceptance criterion or edge case, an FR, an entity from D02, a screen from the UX file, or a decision from the tech design or architecture. Invented work inflates the plan and sends the agent building things nobody asked for.

*Scope of Recommendation here:* only how a story splits into tasks and sub-tasks, and their order. A missing **product** detail (a validation rule, an error message, what a role may see) is a query to product, never a task that decides it. A missing **technical** detail (an endpoint shape the conventions don't settle) becomes a "define ..." task and is logged as a gap.

**Also writes:** nothing beyond the tracker.

{{CORE}}

## Upstream files
`dev/00-dev-setup.md` (conventions, agents, environments); `dev/architecture.md` (layer decisions, engineering conventions, install list); the initiative's `01-tech-design.md` (layer impact, foundations, contracts, dependency build plan); `dev/I-<nnn>-<slug>/02-data-model/<scope>-<slug>.md` and `dev/_shared-entities.md`; the scope's test design `dev/I-<nnn>-<slug>/05-qa/<scope>-<slug>.md` (approved test cases, which every task's `tests` field cites); the handoff for this scope: `product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md` (stories, edge-case registers, acceptance criteria, product handshake), `03-ux/<scope>-<slug>.md`, `02-prd.md`, and, with a design stage, `design/I-<nnn>-<slug>/03-handoff/<scope>-<slug>.md` with its Figma frames (frame links, design-system components, variables, annotations); files of touched scopes; `tracker.yaml`; `decisions/`. For an M00 foundation scope, the tech design's enabler stories take the place of the handoff. For an existing codebase, `dev/00-dev-setup.md` section 2 and a read-only look at the code repositories give Observed touchpoints.

## Questionnaire (skip what upstream files answer)

**Step 1: Scope**
1. Which initiative and scope, and which stories (all ready-for-dev stories, or a list)?
2. Which coding agent will build it (Claude Code, Cursor, other)? This only changes the brief's wording.
3. May I read the product's code repositories (read-only) to name existing code areas each task touches?

**Step 2: Gaps.** Anything a task needs that the upstream files leave open, as numbered items marked product (becomes a query) or technical (a proposed default from the architecture and conventions, confirmed here, or a "define ..." task). Blocking product gaps keep the affected stories blocked until product answers.

## Task layers
Use only the layers a story touches, guided by its product handshake and the tech design.

| Layer | A task here describes |
|---|---|
| Database | Tables, columns, constraints, indexes, migrations, existing-data handling, seed data, from the confirmed data model |
| API | Each capability's contract: inputs, outputs, errors, auth, pagination, following the API conventions in the architecture |
| Backend | Business rules, state transitions, background jobs, integrations, notifications, audit |
| Frontend | Data fetching, client state, form handling, client validation matching server rules, role-based visibility, loading and error handling |
| UI | Screens and components from the UX file and, with a design stage, the Figma frames named in the design handoff (each task cites the frame and state, taken from the story's design references), with every state, responsive behavior, accessibility |
| Auth / Security | Permission checks, tenant isolation, input sanitization, secrets, per L4 and L8 |
| Caching / Rate limiting | What to cache or limit and the rules, per L9 and L10 |
| Logging | Errors, events, and metrics to record, per L12 |
| Config | Env var names per environment, feature flags, app config, per L5 to L7. Pipeline or infrastructure changes a story needs are listed for D06 (Setup mode) |
| QA | Automated tests from the acceptance criteria and edge cases, including "unchanged" criteria that protect existing behavior; for features with an AI model, the eval harness and eval set from `references/ai-features.md` |

Foundations several stories share (base schema, auth middleware, shared layout) are tasks under the M00 enabler stories, referenced by later tasks, never repeated.

## Task template
Tasks are data. Write each story's tasks as one fenced block whose info string is `yaml pdlc-tasks`. `pdlc.py` reads these blocks for dependencies, levels, counts, and the board; D04 updates their status in place. A task's text fields are written once, here; nothing else restates them.

````markdown
```yaml pdlc-tasks
- id: M01.S01.F01-US01-T01          # pdlc.py new-id task M01.S01.F01-US01
  title: Action-led title
  layer: api                        # database | api | backend | frontend | ui | auth-security | caching-rate-limiting | logging | config | qa
  repo: api                         # code repository, when the product has more than one
  status: backlog                   # ready_for_dev to match a ready story
  build: When the owner confirms a bulk send, the send endpoint shall queue one job per selected invoice.   # one EARS sentence, no code
  use: [L2, L3, DEC-004, "architecture.md section 4"]          # decisions, conventions, install-list packages
  touchpoints: [M01.S01-SC01, "entity Invoice", "src/api/invoices (Observed)"]
  implements: [M01.S01.F01-US01-AC01, M01.S01.F01-EC02, M01.S01.F01-FR01]
  tests: [M01.S01.F01-US01-TC01, M01.S01.F01-US01-TC02]   # approved test cases from D05; done when they pass
  budget: {files: 3, lines: "+120 / -40"}                # estimate; overruns past the team's threshold need a reason
  constraints: [I-001-NFR01, "tech design TH03"]
  depends_on: [M00.S01.F01-US01-T02]
  open: []                          # question numbers or query IDs
  subtasks:
    - {id: M01.S01.F01-US01-T01-ST01, title: A concrete, checkable step, status: backlog}
```
````

Sub-tasks are small enough to verify on their own (one checkable outcome each), name the concrete thing (table, capability, screen, state), and never exist only to fill the level.

## Output: `dev/I-<nnn>-<slug>/03-tasks/<scope>-<slug>.md`

```markdown
(header: pdlc_step "D03", initiative I-<nnn>, scope <ID>, depends_on [dev/architecture.md@x, dev/I-<nnn>-<slug>/01-tech-design.md@x, dev/I-<nnn>-<slug>/02-data-model/<scope>-<slug>.md@x, product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md@x, product/I-<nnn>-<slug>/03-ux/<scope>-<slug>.md@x])
# Build tasks: I-[nnn] [scope ID] [name]

## 0. Agent brief
For the coding agent (Claude Code, Cursor, or other), read before planning:
- Scope and stories by dependency level, with what each depends on.
- Files to read, with versions: dev/00-dev-setup.md, dev/architecture.md (layers used, section 4 conventions, section 5 install list), the tech design, the data model, and the handoff files for this scope (stories, UX, PRD).
- Packages allowed for this scope (subset of the install list).
- Definition of done: all sub-tasks done, the story's acceptance criteria and edge cases pass, tests from QA tasks pass, task status updated in this file's `pdlc-tasks` block, `pdlc.py lint` clean.
- Rules: use the dev-04-code-plan-build skill; plan first, wait for approval, then build. Product docs are read-only; questions about product behavior go to the queries in tracker.yaml (`to: product`). Cite requirement IDs; read their wording in the owner files instead of copying it. No package outside the install list without approval. No architecture or schema change outside dev-01 or dev-02. Never run anything against pre-production or production. Never commit secrets.
- Report back: plan at dev/I-<nnn>-<slug>/04-build/<story-or-bug-id>-plan.md; task status in this file's `pdlc-tasks` block; story status in tracker.yaml.

## 1. Gaps, open questions, and queries
## 2. Tasks by story
### M01.S01.F01-US01 [story title]
The story's ID and title and its AC IDs (cited, not restated), then one `pdlc-tasks` block with its tasks.
## 3. Dependency order
Computed by `pdlc.py lint` from the tasks' `depends_on` and shown in `tracker.md`; not written by hand. Note here only why a non-obvious dependency exists.
## 4. Touchpoints
## 5. Coverage
| Story AC / EC / FR / entity / screen / layer decision / TC | Tasks | Gap? |
## 6. Specification review
The gate for D04 (conventions [Specification review and tests first]). The reviewers named in `dev/00-dev-setup.md` check, together:
| Item | What is checked | File@version | Result | Reviewer |
|---|---|---|---|---|
| Architecture and tech design | the layer decisions, DECs, and threat mitigations these stories use | | | |
| Acceptance criteria and edge cases | handed off unchanged; every FR and BR verified by a criterion | | | |
| Constraints | NFRs, threat mitigations (TH), compliance obligations, review tiers | | | |
| Test design | every AC, EC, TH, and EV covered by an approved test case; tests reviewed, not just named | | | |
| Tasks | every task cites its tests; budgets present; reuse expected where the repo map shows existing code | | | |
Sign-off: [reviewer, date]. The file is approved only when this table is complete with no blocking finding. After sign-off, the approved tests are locked for the coding agent.
## Change log
```

## Self-check
- Every acceptance criterion and every edge case (EC ID) of every story in scope is covered by at least one task, including "unchanged" criteria.
- Every layer the tech design marks Change or New for these stories has tasks; every task has a layer and a cited source.
- Every screen state (loading, empty, error) and every flow error path has a task.
- Every entity and migration from D02 used by these stories has a database task.
- No task decides product behavior; no task names a package outside the install list; no task contains code.
- Dependencies have no cycles (`lint` checks); foundations come first.
- Every threat mitigation from the tech design's threat model that applies to these stories has a task.
- Every task lists the approved test cases that prove it (`tests`) and a change budget; every `build` line is one EARS sentence.
- No task asks for code that no AC, EC, threat, or NFR needs (conventions [Lean code]).

## Tracker
Tasks and sub-tasks are not added to `tracker.yaml`; they live in this file's `pdlc-tasks` blocks. Add any queries raised to `tracker.yaml`. Run `lint --fix` (it checks every task ID, its story, and its dependencies) and `board`. This file is approved only after the specification review (section 6) is signed. Next: dev-04-code-plan-build for a ready-for-dev story at the lowest open dependency level. If the scope has no approved test design yet, dev-05-test-qa (test design) comes first.
