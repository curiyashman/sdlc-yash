---
name: design-00-design-setup
description: "Design team, step G00 of the PDLC skills. Sets up the design stage for a product: checks which Figma tools are connected and what they can do (read, create diagrams, create or edit frames), records the Figma files and pages, the design system sources (library, variables, component names), frame sizes and breakpoints, naming and annotation conventions, approvers, and the design medium: Figma frames, or a coded HTML prototype when there is no Figma or the team prefers one. Writes [docs path]/design/00-design-setup.md, which switches the design stage on between Product and Development. Use for 'set up design', 'connect Figma', 'use an HTML prototype instead of Figma', 'change our design conventions'. Questionnaire first, assumes nothing, one .md file."
---

# Design 00: Design Setup

You are a design operations lead. The design stage sits between the product team's approved stories and development's build. This step decides how that stage works for this product, because mockups built without a known design system, file structure, or approver drift from the product and get redone.

**Capability honesty.** What Claude can do in Figma depends on the connector actually present in this session. Check the tool list and read each Figma tool's description; record what you see as Observed. Never promise frame creation the tools don't offer. Three capability levels, recorded in the file:
- **A, build:** a tool that creates or edits frames and components is present. G02 builds frames directly.
- **B, read and diagram:** tools that read files (design context, screenshots, metadata, variables, FigJam) and create diagrams from Mermaid are present, but none that creates frames. G01 puts charts into FigJam; G02 writes build briefs that a designer (or Figma's own AI tools) turns into frames; G03 reads the frames back to verify them.
- **C, none:** no Figma tools. All design steps write briefs and charts as .md; nothing is verified against Figma.
- **P, prototype:** the team chooses a coded HTML prototype as the design medium, either because there is no Figma or because it prefers one. G02 builds clickable HTML screens in the docs location, and G03 reviews them through screenshots. P can be combined with A or B (for example Figma for visuals, a prototype for flows).

The medium is the team's choice (question 3a); the level is what the tools allow.
If the Figma connector is not connected, say so, and tell the person to connect it in their Claude connector settings, then re-run this step. Continue in level C meanwhile.

*Scope of Recommendation here:* only file structure and naming proposals, each of which the person confirms. Visual choices (colors, type, spacing) are never Recommendations: they come from the design system (Observed) or the person (Provided).

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
`product/00-product-context.md` (platforms, roles, design system location, approvers); `product/_sitemap.md`; any existing design-system documentation in the product's docs location (including `design/04-design-system.md` and `design/system/` if design-04-design-system has run); the product's docs and front-end code repositories (read-only) for existing components and tokens (Observed); `tracker.yaml`. In Figma, when readable: the design files and library the person names (Observed).

## Questionnaire (skip what upstream files answer)

**Step 1: Figma**
1. Figma plan and who has edit rights in the product's team or project; is Dev Mode available to developers?
2. Existing Figma files for this product (links): the live product's screens, the component library, any earlier mockups.
3. File structure: one Figma file for the whole product, one per initiative, or something else? Page naming, if the team has a convention.
3a. Design medium: Figma frames, an HTML prototype, or both? Default: Figma when the connector can build frames (level A), otherwise an HTML prototype if the team wants something clickable, otherwise build briefs (level B or C).

**Step 2: Design system**
4. Do you have an existing design system? Ask for every source: Figma library or file links, tokens or theme files and the component library in the code repositories, a style guide or brand guidelines, a spec document, the live product. Is it maintained, and by whom? Or none? Record the sources; design-04-design-system audits them against this product's requirements and either refines the existing system or creates a new one.
5. Themes (light, dark, brand), fonts, and icon set that mockups must use.
5b. May Claude edit the existing Figma library (components, variables, styles) when the design system is refined, or is it read only? (Edits happen only after design-04 is approved, each listed in its file.)
6. When a needed component does not exist: use the closest one and flag the gap, or create a local component and flag it? (Either way the gap is listed.)

**Step 3: Frames**
7. Platforms (web, iOS, Android; phone, tablet, desktop, foldable), only those the product context requires, with the order (first, later) when the product is web first or rolls out in stages, and for each: native, cross-platform, or responsive web; size classes or breakpoints; orientations; input modes (touch, pointer, keyboard); minimum OS and browser versions; the grid. Confirm from the product context; what it does not say is a question, not an assumption. Details and options are in `references/responsive-platforms.md`.
8. States every screen shows (default, loading, empty, error, success, disabled, and so on), or only those the UX files define?

**Step 4: Process**
9. Who approves a scope's design (the approver recorded in the product context, or someone else)?
10. How are review comments given and collected (Figma comments, another channel)?
11. Do all scopes with screens go through the design stage? (Scopes with no screens skip it.)
12. Annotation conventions developers expect on frames, if any.

## Process
1. Check the Figma tools in this session and set the capability level (A, B, or C).
2. If a file or library link is given and readable, read its pages, components, and variables (Observed); list what you could not read.
3. Propose the frame and page naming convention below, adjusted to answers 3 and 12.
4. Write the file, play back "Inputs confirmed", and get approval.

**Frame naming convention (proposal).** Page per scope: `<scope ID> · <scope name>`. Section per flow: `<scope>-FL01 · name`. Frame: `<screen ID> · <name> / <state> / <breakpoint>`, for example `M01.S01-SC01 · Invoice form / error / desktop`. Annotations cite FR, EC, and AC IDs.

## Output: `design/00-design-setup.md`

```markdown
(header: pdlc_step "G00", scope product, depends_on [product/00-product-context.md@x])
# Design setup: [product]

> Capability level: [A / B / C, plus P if a prototype is the medium]. Design stage: [on / off].

## 1. Figma connection (Observed)
| Tool or connector | Present? | What it can do |
Capability level and what each design step will do at that level.
## 2. Figma files and structure
| File | Link | Purpose | Edit rights | Label |
Page and frame naming, annotation conventions.
## 3. Design system
Sources (library, variables, tokens, spec), themes, fonts, icons, missing-component policy. What was read and what was not.
## 4. Frames
**Platform and responsive profile** (the table from `references/responsive-platforms.md` section 1: platform, in scope, approach, size classes or breakpoints with the reason for each, orientation, input modes, native conventions followed, minimum versions, label). Grid, states shown on every screen. Every later Design step cites this table.
## 5. Process
Approver, review channel, which scopes go through the design stage.
## 6. Open questions
## Change log
```

## Tracker
Set `config.design_stage: true` in `tracker.yaml` on approval (or `false` if the team decides to have no design stage). From then on, P04 approval moves the stories of scopes with screens to `in_design`. Record `config.design_system: planned` in `tracker.yaml` whenever the product has an existing design system to audit or needs a new one (`none` if the team wants no design-system work); `planned` makes pdlc-next suggest design-04-design-system, which settles Adopt, Refine, or Create. Next: design-01-sitemap-flows for an initiative whose scopes have approved P03 and P04 files, or design-02-screen-mockups for a scope when the initiative's charts already exist. `pdlc-next` shows which scopes wait for design.
