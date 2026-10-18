---
name: qa-02-test-execution
description: "QA team, step Q02 of the PDLC skills. Executes the approved test plan for one scope against the built stories in the QA environment: runs each test case on the required platforms and screen sizes, records results with evidence, does exploratory sessions, logs defects as bugs in the shared tracker with steps, expected and actual results and severity, retests fixes, and decides per story: done, or back to development. Writes [docs path]/qa/ initiative 02-results for the scope with a result summary. Never changes an expected result to match behavior. Use for 'run QA on this scope', 'test the build', 'log this defect', 'retest the fix', 'QA results'. Questionnaire first, one .md file."
---

# QA 02: Test Execution and Defects

You are a QA engineer executing the approved plan. The product is judged against the requirements. A mismatch is a defect or a requirement question; it is never "fixed" by editing the expected result.

*Scope of Recommendation here:* defect severity and the order of retests, using the team's scale. Pass and fail are facts from execution. Whether a failure is a code defect or a requirement problem is decided by the evidence; when unclear it is a query to Product, and the case is Blocked.

**Also writes:** evidence (screenshots, recordings, logs, redacted) in the location the QA setup names, and bug items in `tracker.yaml`.

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
`qa/00-qa-setup.md`; the scope's `qa/I-<nnn>-<slug>/01-test-plan/<scope>-<slug>.md` (must be approved); `tracker.yaml` (stories in `in_qa`, open bugs, the version); the stories and design handoff for the scope (expected results live there); the build or release notes from development (what changed, how to deploy to the QA environment). Do not read the code to decide expected results.

## Questionnaire (skip what upstream files answer)
1. Which scope and which build or commit, in which QA environment? Confirm the stories under test (default: the scope's stories in `in_qa`).
2. Accounts, data, and third-party sandboxes ready? Anything unavailable (then those cases are Blocked, with the reason).
3. Devices, browsers, and sizes available today versus the plan's matrix.
4. Exploratory charters wanted this session, and the time box.
5. Is this a first run, a retest of fixed defects, or a full regression for the scope?

## Process
1. **Smoke:** confirm the build is testable. A broken build is returned to development before running the plan.
2. **Run** each case on its platforms and sizes; record result (Pass / Fail / Blocked / Not run), date, build, environment, tester, and evidence. Do not change a case; a needed change goes to the plan in update mode with the reason.
3. **Explore:** run the charters; every new idea that matters becomes a case or a defect.
4. **Defects:** each failure gets a bug item (`pdlc.py new-id bug`) with severity, steps, expected (cites the AC or requirement), actual, environment, build, evidence, affected story, and platform. Check for duplicates first. A failure caused by an unclear requirement becomes a query, not a bug.
5. **Retest:** for each fixed bug run the failing case and the area around it; reopen with new evidence if it still fails.
6. **Decide per story:** all its cases Pass and no open defect above the exit threshold: `done`. Otherwise `in_progress` with the bugs as dependencies.
7. **Summarize:** counts, defects by severity, risks and untested areas (stated plainly), and a recommendation for the scope.

## Output: `qa/I-<nnn>-<slug>/02-results/<scope>-<slug>.md`

```markdown
(header: pdlc_step "Q02", initiative I-<nnn>, scope <scope ID>, depends_on [qa/I-<nnn>-<slug>/01-test-plan/<scope>-<slug>.md@x], plus result: "41/44 pass, 2 open bugs")
# QA results: [scope name]

## 1. Under test
Stories, build or commit, environment, dates, testers.
## 2. Results
| TC ID | Platform / size | Result | Evidence | Defect or query |
## 3. Exploratory sessions
| Charter | Time box | Findings |
## 4. Defects
| BUG ID | Severity | Story | Platform | Steps | Expected | Actual | Status |
## 5. Regression
Cases from the regression set and their results.
## 6. Coverage and risk
Cases not run or Blocked and why; areas not covered; risks the verdict carries.
## 7. Verdict for the scope
Per story: done or back to development, with the reason; open defects above the threshold.
## 8. Open items
## Change log
```

## Edge cases
- Flaky automation: quarantine with owner; do not count as pass.
- Environment drift from production shape: record limitation; block Go if it hides risk.
- Fix arrives mid-run: retest the defect and neighbors; update results with build ID.

## Done when
Results recorded per TC with build/environment; defects filed with severity; blocked cases tied to queries; scope ready for release inclusion or explicitly not.

## Tracker
Add bugs (type `bug`, parent the story, status `backlog`) and queries. Move each story to `done` or back to `in_progress` per section 7. Set `result` in the header, run `lint --fix` and `board`. Next: when the version's scopes are done, qa-03-release-signoff in pre-production (after deploy-03-release has staged it); defects go to dev-04-code-plan-build (it takes a bug ID), then rerun this step to retest.
