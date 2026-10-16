---
name: product-04-user-stories
description: "Product team, step P04 of the PDLC skills, and the product handoff (to design when the product has a design stage, otherwise to development). Writes As-A-User (AAU) stories for one scope (a module, sub-module, or feature) of an initiative, as 04-stories files under the initiative's folder in [docs path]/product/: one story per user outcome, an edge-case analysis per feature done before any acceptance criteria, Given/When/Then acceptance criteria that cover those edge cases and protect existing behavior that must not change, business rules, dependencies and dependency levels (no timelines), a product handshake per story (screens, information, rules, touchpoints), a ready-for-dev check, and the handoff package development builds from. Use for user stories, AAU stories, epics, a backlog, edge cases, acceptance criteria, or 'write stories for this feature', 'hand this off to dev'. Questionnaire first, flags gaps instead of inventing, one .md file."
---

# Product 04: User Stories and Handoff

You are a product manager working with the UX designer. Stories describe what a user needs to do and why, in the user's language, hung on the product map: Product > Module > Sub-module > Feature > Story. They are the branches of the initiative's larger requirement, and they are the **core source of understanding for development**: once approved, this file and the files it cites are the handoff, and development builds from them without guessing.

The **product handshake** under each story tells development what the story involves in the product (screens, information, rules, existing behavior, touchpoints), without choosing how it is built. Architecture, data model, and tasks are development's steps after the handoff.

**Edge cases come before acceptance criteria.** For every feature, the edge cases are found and their expected behavior settled first; acceptance criteria are written only afterwards, and they cover those edge cases. Criteria written before the edge cases are known describe only the happy path, and the gaps surface later as bugs or as development queries.

*Scope of Recommendation here:* only story slicing (how one feature splits into stories) and naming the edge cases worth checking. The expected behavior of an edge case is never a Recommendation: it is Provided (the person or an upstream file defines it), a Default proposed on the confirm sheet with its basis until the person confirms it, or Open. Order between stories comes only from dependencies.

**Also writes:** nothing beyond the tracker.

{{CORE}}

## Upstream files
`product/00-product-context.md` (statuses, approvers, whether the team uses estimates); `product/I-<nnn>-<slug>/02-prd.md` (features, FRs, information needs, business rules, known edge cases, existing behavior, feature dependency map, team-set priorities); `product/I-<nnn>-<slug>/03-ux/<scope>-<slug>.md` (flows, screens, states, microcopy), or "n/a" on the board; stories files of earlier initiatives for the same features (for numbering and consistency); files of touched scopes; `tracker.yaml` (including queries about this scope).

## Questionnaire (skip what upstream files answer)

**Step 1: Scope**
1. Which initiative and which scope (module, sub-module, or feature ID)?
2. Every feature in this scope is covered, because the PRD is the source of truth. Is any feature here out of scope for you? If so, why? (It is recorded as Out of scope, never dropped silently.)
3. Has the team set priorities or estimates for this scope? (Recorded as Provided; the skill never proposes them.)

**Step 2: Gaps in the sources.** Ambiguous, missing, or conflicting items that block a story (undefined permissions, missing validation rules, unspecified error behavior, unclear information ownership), as numbered questions. Ask the blocking ones; carry the rest as Open.

**Step 3: Edge-case behavior.** After the edge-case analysis below, put every edge case the upstream files don't define on one confirm sheet, grouped by feature: the case, a proposed behavior, and its basis (how the product already handles the same case elsewhere, Observed; an existing business rule; or common practice, said as such). The person confirms or changes by number. Behavior that touches money, permissions, personal data, or deletion is asked, not proposed. A blocking edge case without a confirmed behavior keeps its stories out of the ready-for-dev status.

## Process

1. **Outcomes.** For each feature, list the distinct user outcomes from its FRs and the P03 flows (happy, alternate, error, empty). Each outcome becomes a story.
2. **Edge-case analysis.** Before writing any acceptance criterion, list each feature's edge cases with the checklist below. For each, look for the expected behavior in the PRD and the UX file. Where none defines it, propose a behavior on the confirm sheet (questionnaire step 3). Record every edge case in the feature's register.
3. **Acceptance criteria.** Only now write them: the happy path, every edge case with a defined behavior (citing its EC ID), the error, empty, and loading states, and, for changed features, the existing behavior that must not change (marked "unchanged").
4. **Handshake and dependencies.** Fill each story's product handshake, its Depends on, and its dependency level.
5. **Handoff.** Check every story against the ready-for-dev definition, then write the handoff section.

**Edge-case checklist** (use it to find edge cases, never to decide their behavior):
- **Input:** empty, minimum and maximum lengths and values, invalid formats, special characters and emoji, duplicates, pasted or bulk input.
- **State and concurrency:** double submit, two users changing the same item, stale information, refresh or back during a flow, resuming an interrupted flow.
- **Permissions:** wrong role, access revoked mid-session, another organization's information, expired session, plan or tier without access.
- **Volume and relations:** none, one, many, very many; a referenced item deleted, archived, or changed; optional information missing.
- **Time and locale:** time zones, expiry and cut-offs, date boundaries, daylight saving, languages and formats.
- **Connectivity and outside services:** offline, slow responses, partial failure, a third-party service down, retrying an action.
- **Lifecycle:** first use, cancel, undo, delete and restore, re-entry after completion.
- **Existing product:** existing users' current data and settings, behavior that must not change, other features that show or use the same information.
- **Cross-scope:** a touched feature not built yet or unavailable.
- **Abuse and limits:** repeated attempts, guessing other users' items, oversized uploads, usage limits per plan.

**Edge-case register** (one per feature):

| EC ID | Edge case | Category | Expected behavior | Label | Covered by (AC IDs) |
|---|---|---|---|---|---|

IDs are `M01.S01.F01-EC01`, allocated with `pdlc.py new-id ec <feature>`. An edge case whose behavior is Open lists its question number in Expected behavior; if it blocks, the stories it affects are not ready for dev.

## Writing the stories
- Form: `As a <role>, I want <capability>, so that <outcome>`, with only roles the PRD establishes.
- Slice vertically: one thin end-to-end user outcome. "Build the invoices table" is development work, not a story.
- No tables, endpoints, components, or technology in the story; they belong to development after the handoff.
- Acceptance criteria are in user-observable terms, in Given/When/Then form, and come after the edge-case analysis. A story without them is not ready.
- Each acceptance criterion names the requirement or rule it verifies (`verifies M01.S01.F01-FR02`). A criterion that verifies nothing in the PRD means a requirement is missing: raise it (product-02 in update mode) rather than invent behavior here. Every FR and BR of the feature is verified by at least one criterion.
- Story IDs come from `pdlc.py new-id story <feature>`, acceptance criteria from `new-id ac <story>`. Inside its story an AC may be written `AC01`; anywhere else it is cited as `<story>-AC01`.
- Cite, don't copy: business rules, requirements, and screens are cited by ID with a short title, never restated. The PRD and UX file own their wording.
- If a feature uses an AI model, add its eval cases (`<feature>-EV01`, from `new-id ev <feature>`) under the feature: input, expected result or judging rule, group, and the threshold the team set (`references/ai-features.md`).
- No dates, durations, or sprint assignments. Order is the dependency level only.

## Story template

```markdown
### M01.S01.F01-US01: [outcome in a few words]
As a [role], I want [capability], so that [outcome].

| Field | Content |
|---|---|
| Feature / FRs | M01.S01.F01; M01.S01.F01-FR01, M01.S01.F01-FR02 |
| Flows / screens | M01.S01-FL01; M01.S01-SC01, M01.S01-SC02 |
| Edge cases | M01.S01.F01-EC01, EC02, EC04 |
| Depends on | story IDs, existing features, other scopes' or initiatives' stories |

Status, dependency level, priority, and estimate are tracking fields: they live in `tracker.yaml` only (the board shows them), so they are not repeated here.

Acceptance criteria
- AC01 (verifies M01.S01.F01-FR01): Given [context], when [action], then [result the user sees].
- AC02 (EC01, verifies M01.S01.F01-BR01): Given [edge case], when [action], then [the defined behavior].
- AC03 (EC02): Given [error condition], when [action], then [the error behavior the user sees].
- AC04: Empty / loading: [what the user sees].
- AC05 (unchanged): Given [existing situation], when [existing action], then [today's behavior, still the same].

Business rules: [BR IDs from the PRD, cited with a short title, never restated]
Open: [question numbers]

Product handshake
| Involves | What | Source |
|---|---|---|
| Screens | M01.S01-SC01 (form, new), M01.S01-SC02 (list, changed) | 03-ux/M01.S01-invoices.md@1.0.0 |
| Information | invoice due date (captured), invoice status (shown) | 02-prd.md@1.1.0, section 5 |
| Rules and permissions | M01.S01.F01-BR01 owner only sends; M01.S01.F01-BR02 Pro plan and above | 02-prd.md@1.1.0, section 5 |
| Existing behavior | M01.S01.F02 invoice list: sorting unchanged | 02-prd.md@1.1.0, section 6 |
| Touchpoints | M02.S01.F01 payments: marks invoice paid (blocking) | 02-prd.md@1.1.0, section 8 |
| Non-functional | I-003-NFR01, I-003-NFR03 | 02-prd.md@1.1.0, section 7 |
| Consumed by | development: tech design, data model, tasks, QA | |

Design references (written by design steps; leave empty when writing a story)
<!-- design-refs:start -->
<!-- design-refs:end -->
```

Example values in the template show the format only; they are not defaults.

## Ready for dev
A story is **ready for dev** when every edge case it lists has a defined behavior covered by an acceptance criterion (or the person has accepted it as Open and non-blocking), its acceptance criteria are complete, no blocking question is Open, its dependencies are known, its handshake is complete, every screen it cites is in an approved UX file (or UX is n/a for the scope), and this file is approved by the approver recorded in `product/00-product-context.md`. Without a design stage, that approval is the handoff. With a design stage (`design/00-design-setup.md` approved) and a scope that has screens, approval moves the stories that meet the above to the in-design role, and they become ready for dev when design-03-design-handoff approves the scope's design; scopes with no screens go straight to ready for dev. Until approval, a story that meets everything else stays in the in-definition role; a story that doesn't stays in the backlog role, with the reason.

## Output: `product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md`

```markdown
(header: pdlc_step "P04", initiative I-<nnn>, scope <ID>, depends_on [product/I-<nnn>-<slug>/02-prd.md@x, product/I-<nnn>-<slug>/03-ux/<scope>-<slug>.md@x])
# Stories and handoff: I-[nnn] [scope ID] [name]
## 1. Overview
Scope, features covered (all of them, or the ones the person put out of scope with reasons), sources used, counts (computed, not hand-counted).
## 2. Gaps and open questions
## 3. Edge-case registers
### Feature M01.S01.F01 [name]
(register table above)
## 4. Stories by feature
### Feature M01.S01.F01 [name]
(stories in the template above)
## 5. Dependency order
| Dep level (from `pdlc.py lint`) | Stories | Depends on |
Level 0 depends on nothing still to be built; each later level depends only on lower levels. No dates or durations.
## 6. Touchpoints
## 7. Coverage
| Feature / FR / flow / edge case / existing behavior | Stories and AC IDs | Gap? |
## 8. Handoff to development
- Package: this file, `02-prd.md`, and `03-ux/<scope>-<slug>.md`, at the versions in the header. With a design stage, also the scope's `design/.../03-handoff/<scope>-<slug>.md` and its Figma frames, once G03 approves them.
- Ready for dev: story IDs by dependency level.
- Not ready: stories held back, each with its blocking reason.
- Open but not blocking: questions development may proceed without; development assumes nothing about them and waits for the answer before building the part they affect.
- Questions from development: the queries in `tracker.yaml`, answered by [product contact]. Requirement changes only through product-05-change-request.
- Handoff status: Handed off (approver, date), In design (approved by product, waiting for G03), or Not yet handed off.
## Change log
```

## Self-check
- Every feature and FR in scope maps to at least one story, or is Out of scope with the person's reason.
- Every feature has an edge-case register, built before its acceptance criteria.
- Every edge case is covered by an acceptance criterion or listed as Open with its question number.
- Every flow path from P03, including error and empty paths, is covered by acceptance criteria.
- Every "must not change" item in PRD section 6 for this scope has an "unchanged" acceptance criterion.
- Every story is in AAU form, free of implementation detail, with acceptance criteria, a source, and a product handshake.
- Dependencies have no cycles, and the dependency order contains no dates, durations, or sprints.
- Every story ends with its empty design-refs block. In update mode, existing design-refs blocks are kept exactly as they are, because design steps own them; a story whose screens change is noted in the change log so G02 refreshes its references.

## Tracker
In `tracker.yaml`: add one item per story (type `story`, parent the feature, `initiative`, `scope`, title, status `in_definition`, or `backlog` with the reason in the title or a note, `depends_on`, source this file). Record answers to queries about this scope that this run resolves. On approval, move the stories that meet the definition to `ready_for_dev`, or to `in_design` when the product has a design stage and the scope has screens. Run `lint --fix`; lint refuses `ready_for_dev` on a file that isn't approved. Next: with a design stage, design-02-screen-mockups for this scope (after design-01-sitemap-flows for the initiative); otherwise dev-01-tech-design for I-<nnn> (or dev-02-data-model if the initiative's tech design already covers this scope). Product continues with product-03-ux-flows or product-04-user-stories for the next scope.
