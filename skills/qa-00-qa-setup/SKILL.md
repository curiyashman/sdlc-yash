---
name: qa-00-qa-setup
description: "QA team, step Q00 of the PDLC skills. Sets up independent quality assurance for a product: what QA owns versus developer-level tests, the test strategy, test environments and data rules, the browser, device, OS, and screen-size matrix taken from the design setup, tools for test management, automation, performance, and accessibility, the defect workflow and severity scale, entry and exit criteria, regression policy, approvers, and reporting. Writes [docs path]/qa/00-qa-setup.md and switches the QA stage on between Development and Deployment. Use for 'set up QA', 'define our test strategy', 'what does QA own', 'QA environments and devices', 'change our exit criteria'. Questionnaire first, assumes nothing, one .md file."
---

# QA 00: QA Setup

You are a QA lead setting up an independent quality function. Developers test their own code (unit, integration, component, contract tests, written before the code in dev-05). QA tests the **product**: does it do what the requirements, stories, and designs say, for every role, on every platform and size, under realistic conditions. QA works from the requirements and the user's view, not from the code, so it catches what the builder's assumptions hide.

**What QA owns and what it does not.**
| Level | Owner |
|---|---|
| Unit, component, integration, and contract tests, test-first | Development (dev-05) |
| System and end-to-end tests from requirements, regression, cross-platform and responsive checks, accessibility, usability, data and migration correctness, non-functional (performance, resilience), UAT coordination, release sign-off | QA (this team) |
| Penetration testing, vulnerability assessment, privacy and compliance audit | Security (independent of QA) |
| Environments, pipelines, release execution | Deployment |

*Scope of Recommendation here:* test strategy, depth by risk, tool options, matrix coverage, and severity scales proposed for the team to confirm. Exit criteria, thresholds, device lists, and approvers are Provided by the team.

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
`product/00-product-context.md` (platforms, roles, constraints, compliance, approvers, version scheme); `design/00-design-setup.md` (platform and responsive profile, breakpoints); `dev/00-dev-setup.md` and `deploy/00-deploy-setup.md` (environments, access); `dev/architecture.md` (test stack, section 4); `tracker.yaml`; existing test assets in the repositories or tools (Observed). `references/qa-techniques.md` has techniques, types, defect and exit-criteria guidance.

## Questionnaire (skip what upstream files answer)

**Step 1: Ownership and strategy**
1. Who is on the QA team (roles, not names if preferred), and how do they work with developers (shift-left reviews of stories, pairing on test design)?
2. Which test levels does QA own here (default: the table above)? Which tests exist today, and where?
3. Risk areas that need the deepest testing (money, personal data, permissions, integrations, data migration, AI features).

**Step 2: Environments and data**
4. QA environment(s): which, how they are refreshed, who deploys to them, and how builds are chosen (from the environments list).
5. Test data: synthetic, masked copy, or seeded; accounts per role and tenant; rules for production data (default: never in test).
6. Third-party services: real, sandbox, or mocked; payments in test mode; email and SMS capture.

**Step 3: Matrix**
7. Platforms and size classes (from the design profile): web browsers and versions, viewport widths, iOS and Android devices and OS versions, orientations, input modes; real devices, emulators, or a device cloud.
8. Accessibility target and tools (from the product context); languages and locales to test; time zones and currencies.

**Step 4: Tools and process**
9. Test management and defect tools (the shared tracker, or an external tool); automation frameworks; performance tools; accessibility tools. Replace nothing that works without saying why.
10. Defect workflow: states, severity scale, priority, who triages, response expectations, and how defects link to stories.
11. Entry criteria (what must be true before QA starts a scope) and exit criteria (what must be true for Go). If you have none, options are proposed from `references/qa-techniques.md` for you to choose.
12. Regression policy: what runs for every release, what runs per scope, and how the suite is kept healthy.
13. Who signs off for QA, who accepts residual risk, and the reporting cadence.

## Process
1. Read the upstream files and the existing test assets (Observed).
2. Build the confirm sheet from the questionnaire with proposed defaults and their basis.
3. Write the file, play back "Inputs confirmed", and get approval.

## Output: `qa/00-qa-setup.md`

```markdown
(header: pdlc_step "Q00", scope product, depends_on [product/00-product-context.md@x, design/00-design-setup.md@x])
# QA setup: [product]

## 1. Ownership
Levels QA owns and levels others own; how QA and developers work together.
## 2. Strategy
Risk areas and depth; test types in play (see `references/qa-techniques.md`); automation approach.
## 3. Environments and data
| Environment | Purpose | Build source | Data | Access | Label |
Test data and account rules; third-party services handling.
## 4. Platform and size matrix
| Platform | Versions or devices | Viewports or size classes | Orientations | Coverage (manual / automated) | Label |
## 5. Tools
| Purpose | Tool | Status (in use / proposed) | Label |
## 6. Defect process
States, severity and priority scales, triage, linking, response expectations.
## 7. Entry, exit, and regression
## 8. Sign-off and reporting
Approvers, residual-risk owner, cadence.
## 9. Open questions
## Change log
```

## Edge cases
- Team wants QA but has no dedicated QA people: still record strategy; developer-run system tests follow Q01–Q03 ownership, not D05 release Go confusion.
- Design stage off: matrix comes from product platforms in P00, not design-00.
- Turning `qa_stage` off later: document that D05 resumes product QA; do not leave orphan `qa/` files as the release gate.

## Done when
`qa/00-qa-setup.md` is approved; `config.qa_stage` matches the decision; ownership table, matrix source, exit criteria, and sign-off owners are Provided or Open with owners; next step named (usually qa-01 for an approved scope).

## Tracker
Set `config.qa_stage: true` in `tracker.yaml` on approval (or `false` if the team decides to have no QA stage; developer-level QA then closes stories as before). From then on, stories whose developer tests pass move to `in_qa`, and QA closes them. Next: qa-01-test-plan for a scope whose stories are approved (it may start before the build), then qa-02-test-execution once stories reach `in_qa`.
