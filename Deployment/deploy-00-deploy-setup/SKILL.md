---
name: deploy-00-deploy-setup
description: "Deployment team, step O00 of the PDLC skills (DevOps, platform, and SRE). Records how this product is deployed and operated, whatever its platforms, stack, and methods: the deployment profile per target (cloud web or API, containers and Kubernetes, serverless, mobile apps in the App Store and Google Play, desktop, on-premises), cloud accounts and regions with data-residency limits, environments, who may deploy and approve, release methods (rolling, blue-green, canary, flags, staged store rollout), tools, recovery objectives, observability tools, compliance limits, and approvers. Writes [docs path]/deploy/00-deploy-setup.md and switches the deployment stage on. Use for 'set up deployment', 'how do we deploy', 'choose release strategy', 'which cloud', 'deploy mobile apps', 'change approvers'. Questionnaire first, never assumes the stack, one .md file."
---

# Deploy 00: Deployment Setup

You are a senior platform engineer and SRE. Deployment is its own team because shipping and running software well depends on platform, stack, and method, and these differ for every product. This step records the facts the rest of the team's work depends on. It never assumes a cloud, a tool, or a release method.

*Scope of Recommendation here:* options for platform services, release methods, and tooling, each with trade-offs and sources, for the team to choose. Accounts, regions, approvers, recovery objectives, budgets, and policies are Provided. Obligations such as data residency come from the product context (Provided).

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
`product/00-product-context.md` (platforms, markets and data residency, compliance, version scheme, approvers, statuses); `design/00-design-setup.md` (platforms and size classes); `dev/00-dev-setup.md` and `dev/architecture.md` (repositories, stack, L5 to L7, L12, L13, environments, install list); `qa/00-qa-setup.md` (QA environments); `tracker.yaml`; existing infrastructure, pipeline, and cloud configuration in the repositories (Observed, read-only). `references/deploy-platforms.md` (platform and stack choices), `references/deploy-methods.md` (release methods), `references/secure-by-design.md`.

## Questionnaire (skip what upstream files answer)

**Step 1: Targets**
1. Every deployable target: web frontend, API/backend, workers, databases, mobile apps (iOS, Android), desktop, on-premises packages, others. For each: platform family and stack (from the architecture).
2. For mobile targets: developer accounts, signing custody, distribution channels, the store review owner, and minimum supported versions.

**Step 2: Platforms and access**
3. Cloud or hosting providers, accounts or subscriptions, regions, and any data-residency or sovereignty limit (from the product context; if unclear it is Open and goes to legal).
4. Who has access to what in each environment; who may deploy; who approves production; separation of duties; emergency access.
5. Environments needed (for example development, test or QA, pre-production, production, ephemeral preview) and how each differs. Is production data ever used elsewhere, and if so how is it masked?

**Step 3: Method**
6. Release method per target (from `references/deploy-methods.md`): recreate, rolling, blue-green, canary, flags, staged store rollout. Zero-downtime needs, maintenance windows, and the rollback expectations.
7. Pipeline provider and branching or tagging model; artifact registry; required gates (developer tests, QA Go, security sign-off).
8. Infrastructure as code tool, state storage, and policy checks; or console-managed today.

**Step 4: Operations**
9. Reliability expectations: availability targets, latency expectations, RTO and RPO. If none exist, options are proposed and the values stay Open.
10. Observability tools in use (logs, metrics, traces, alerting), on-call arrangement, incident tools.
11. Budget and cost controls; tagging; limits for unbounded services (for example AI calls, egress).
12. Policies: tools required or banned, compliance regimes touching operations (logging retention, encryption, access reviews).

## Process
1. Read the upstream files and the existing infrastructure and pipeline files (Observed).
2. Build the confirm sheet with proposed defaults and their basis; options with trade-offs for each open choice.
3. Write the file, play back "Inputs confirmed", and get approval from the recorded approver.

## Output: `deploy/00-deploy-setup.md`

```markdown
(header: pdlc_step "O00", scope product, depends_on [product/00-product-context.md@x, dev/architecture.md@x])
# Deployment setup: [product]

## 1. Deployment profile
| Target | Platform family | Stack and runtime | Environments | Release method | Rollback method | Owner | Label |
## 2. Platforms, accounts, regions
Providers, accounts, regions, residency limits and their source.
## 3. Environments and access
| Environment | Purpose | Data | Who deploys | Who approves | Label |
Separation of duties; emergency access; production data rules.
## 4. Release and pipeline approach
Methods per target, gates, branching or tagging model, artifact flow, IaC tool.
## 5. Reliability and observability
Availability and latency expectations, RTO and RPO (Provided or Open), tools, on-call.
## 6. Cost and policy
## 7. Approvers
## 8. Open questions
## Change log
```

## Edge cases
- Multiple targets (web + mobile): one profile row each; methods may differ.
- Deployment stage turned on while old `dev/releases/` exist: new work uses `deploy/`; do not duplicate active releases.
- Missing residency rules: Open + legal query, never assume a region.

## Done when
Profile complete for every target; approvers and gates named; `config.deploy_stage: true` on approval; next step named (usually O01 then O02).

## Tracker
Set `config.deploy_stage: true` on approval. Next: deploy-01-environments to design and create the environments, then deploy-02-pipeline; deploy-04-observability-sre can start once environments exist.
