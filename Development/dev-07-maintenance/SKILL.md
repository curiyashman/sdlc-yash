---
name: dev-07-maintenance
description: "Development team, step D07 of the PDLC skills: the route for work that has no product requirement, namely hotfixes, tech debt, dependency and platform upgrades, spikes, and chores. Records one item in [docs path]/dev/maintenance/: what and why, evidence, affected code repositories and product areas, risk, the guarantee that product behavior doesn't change (or a query to product when it would), the approach, tests, and rollback; adds it to tracker.yaml as HF-, TD-, UPG-, SPK-, or CHR- with dependencies. Then the item is built with dev-04, tested with dev-05, and shipped with dev-06; a spike ends in a decision (DEC). Use for 'hotfix', 'production bug, urgent', 'tech debt', 'upgrade React / Node / the database', 'security patch', 'spike on X', 'investigate whether', 'clean up', 'chore'. Questionnaire first, assumes nothing, one .md file."
---

# Dev 07: Maintenance

You are a staff engineer who keeps the product healthy. Not all work starts from a requirement: production breaks, code ages, dependencies need upgrades, and some questions need a time-boxed investigation before anyone can decide. This step gives that work a route, so it is tracked, tested, and traceable like everything else, without inventing product requirements.

**Types**
| Type | ID | For | Ends with |
|---|---|---|---|
| Hotfix | `HF-001` | a production defect that cannot wait for the next version | a patch release (dev-06 Hotfix mode) and the bug's root cause |
| Tech debt | `TD-001` | known shortfalls in code, architecture, tests, or tooling | the change merged and verified, or a DEC to accept it |
| Upgrade | `UPG-001` | dependency, runtime, framework, database, or platform upgrades, including security patches and deprecated AI models | the upgrade released, with the install list updated |
| Spike | `SPK-001` | a time-boxed investigation that answers one question | a DEC with the answer and its evidence |
| Chore | `CHR-001` | operational work with no behavior change (rotate keys, clean up data per policy, rename) | done and recorded |

**Product behavior doesn't change here.** If the fix or change alters anything a user sees or relies on, it is not maintenance alone: raise a query to product (`to: product`). Product answers in its files or through a change request. The maintenance item waits for the answer, or ships only the part that doesn't change behavior. A hotfix that restores the behavior the stories already define is not a behavior change.

*Scope of Recommendation here:* approach, risk rating, test and rollback plan, and, for tech debt, whether to fix now, later, or accept with a DEC. Each cites the evidence. Timelines and priorities are the team's.

**Also writes:** a DEC for a spike's answer or an accepted risk; the install list in `dev/architecture.md` (PATCH bump) for upgrades, with the person's OK.

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
`dev/00-dev-setup.md` (repositories, environments); `dev/architecture.md` (layers, install list); `tracker.yaml` (existing bugs and items); `decisions/`; for a hotfix, the incident file in `dev/releases/` and the stories file that defines the correct behavior; the code repositories (read-only until dev-04).

## Questionnaire (skip what the sources answer)
1. What is it: hotfix, tech debt, upgrade, spike, or chore? In a sentence, what and why now?
2. Evidence: incident, error, logs, metrics, advisory (for example a CVE), deprecation notice with its date, or a team observation. Each with its source.
3. Which code repositories, layers (L1 to L13), and product areas (map IDs, stories) does it touch?
4. Could any user-visible behavior change? If yes, which, and has product been asked?
5. Risk if left as it is, and risk of the change. Use the team's scale or a proposed default (low, medium, high), confirmed.
6. For a spike: the one question it must answer, what counts as an answer, and its time box (team-set).
7. For an upgrade: from and to versions (Reference, cited release notes and dates), breaking changes, and what must be re-tested.
8. For a hotfix: the shortened path the team accepts (for example skip pre-production with a named approver), and what is completed after release (tests, root cause, documents).

## Output: `dev/maintenance/<id>-<slug>.md`

```markdown
(header: pdlc_step "D07", scope <HF/TD/UPG/SPK/CHR ID>, depends_on [the files read, with versions])
# [ID]: [title]

## 1. What and why
Type, evidence (labeled, with sources), affected repositories, layers, and map IDs.
## 2. Behavior guarantee
"No user-visible change", with how it is verified; or the query ID raised to product and what waits for it.
## 3. Approach
For a spike, the question, the method, and the exit condition. Otherwise, the change in requirement form, with no code.
## 4. Risk
| Risk | Rating | Mitigation | Label |
## 5. Tests and verification
Existing tests that must still pass; new tests; for a hotfix, the test that reproduces the defect; for an upgrade, the re-test list.
## 6. Release and rollback
Which version or patch release; the rollback plan; for a hotfix, the shortened path and what is completed after.
## 7. Outcome
Filled at the end: result, DEC ID (spike or accepted risk), PRs, release.
## Change log
```

## Tracker
Add the item to `tracker.yaml` (`pdlc.py new-id hf|td|upg|spk|chr`; type `hotfix`, `tech_debt`, `upgrade`, `spike`, or `chore`; title; status `backlog`; `depends_on`; source this file). Run `lint --fix` and `board`. Next: dev-04-code-plan-build for the item (a spike may need no code), then dev-05-test-qa and dev-06-deploy. A hotfix uses dev-06 Hotfix mode.
