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

0. **Product mode.** Read `config.product_mode` (or the product card). **Brownfield:** every touched Live feature needs "unchanged" ACs for behavior that must not change; Depends on may cite existing map feature IDs that are `released`. **Greenfield:** Depends on are other planned stories or foundations only; fewer "unchanged" ACs.
1. **Outcomes.** For each feature, list the distinct user outcomes from its FRs and the P03 flows (happy, alternate, error, empty). Each outcome becomes a story.
2. **Edge-case analysis.** Before writing any acceptance criterion, list each feature's edge cases with the checklist below. For each, look for the expected behavior in the PRD and the UX file. Where none defines it, propose a behavior on the confirm sheet (questionnaire step 3). Record every edge case in the feature's register.
3. **Acceptance criteria.** Only now write them: the happy path, every edge case with a defined behavior (citing its EC ID), the error, empty, and loading states, and, for changed features (especially brownfield), the existing behavior that must not change (marked "unchanged").
4. **Handshake and dependencies.** Fill each story's product handshake and its Depends on (story IDs and/or existing released feature IDs). Derive dependency levels with `pdlc.py lint --fix`. **Draft and list stories in dependency order: Level 0 first, then 1, then N** — never feature-ID order when that disagrees with deps. Section 5 of the output must match each story's `depends_on` in `tracker.yaml`.
4b. **Depth (harvest ring).** With the person, tag each story `foundation` | `trunk` | `branch` | `leaf` (conventions [Tree, depth, and versions]). Trunk = happy path; branch = good-to-have; leaf = advanced/deeper. Record in `tracker.yaml` (`depth:`). Depth does not change Depends on or Level; it only guides which stories the team puts in the next `fix_version` (P06). Keep the full tree in the PRD — do not drop branch/leaf from the stories file just to shrink a release.
5. **Handoff.** Check every story against the ready-for-dev definition, then write the handoff section. Do not mark a story ready for build while an upstream story it Depends on is still below `ready_for_dev` (lint enforces this).

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
- **Cite, don't copy:** cite FR/BR/SC/FL/EC IDs (short title optional); never restate PRD or UX wording. Readers open the owner file.
- Keep the file thin: tables and ID lists only; no narrative that repeats the PRD.
- If a feature uses an AI model, add its eval cases (`<feature>-EV01`, from `new-id ev <feature>`) under the feature: input, expected result or judging rule, group, and the threshold the team set (`references/ai-features.md`).
- No dates, durations, or sprint assignments. Order is the dependency level only.

## Story template

```markdown
### M01.S01.F01-US01: [outcome in a few words]
As a [role], I want [capability], so that [outcome].

| Field | Content |
|---|---|
| Feature / FRs | M01.S01.F01; FR01, FR02 |
| Flows / screens | FL01; SC01, SC02 |
| Edge cases | EC01, EC02, EC04 |
| Depends on | story / released feature IDs |

Status / dep_level / depth / fix_version / priority / estimate → `tracker.yaml` only.

Acceptance criteria (Given/When/Then; cite verifies FR/BR/EC; no PRD restatement)
- AC01 (verifies FR01): …
- AC02 (EC01, verifies BR01): …
- AC03 (unchanged): …   # brownfield / must-not-change

BR IDs: … | Open: …

Product handshake (IDs + source@version only)
| Involves | What (IDs) | Source |
|---|---|---|
| Screens | SC01 (new), SC02 (changed) | 03-ux/…@x |
| Information | … | 02-prd.md@x §5 |
| Rules | BR01, BR02 | 02-prd.md@x §5 |
| Existing behavior | … (unchanged) | 02-prd.md@x §6 |
| Touchpoints | … | 02-prd.md@x §8 |
| Non-functional | NFR01 | 02-prd.md@x §7 |

<!-- design-refs:start -->
<!-- design-refs:end -->
```

Example values show format only.

## Ready for dev
A story is **ready for dev** when every edge case it lists has a defined behavior covered by an acceptance criterion (or the person has accepted it as Open and non-blocking), its acceptance criteria are complete, no blocking question is Open, its dependencies are known, its handshake is complete, every screen it cites is in an approved UX file (or UX is n/a for the scope), and this file is approved by the approver recorded in `product/00-product-context.md`. Without a design stage, that approval is the handoff. With a design stage (`design/00-design-setup.md` approved) and a scope that has screens, approval moves the stories that meet the above to the in-design role, and they become ready for dev when design-03-design-handoff approves the scope's design; scopes with no screens go straight to ready for dev. Until approval, a story that meets everything else stays in the in-definition role; a story that doesn't stays in the backlog role, with the reason.

## Output: `product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md`

Keep sections to the tables below. Omit empty optional rows; cite IDs, don't paste PRD text.

```markdown
(header: pdlc_step "P04", initiative I-<nnn>, scope <ID>, depends_on [product/I-<nnn>-<slug>/02-prd.md@x, product/I-<nnn>-<slug>/03-ux/<scope>-<slug>.md@x])
# Stories and handoff: I-[nnn] [scope ID] [name]
## 1. Overview
| Scope | Features in / out | Sources | Story count |
## 2. Gaps and open questions
| # | Gap | Blocks? |
## 2b. Delta (brownfield; skip if greenfield / nothing Live touched)
| Changes (new / changed behavior) | Unchanged (cite AC IDs marked unchanged) | PRD §6 / Live refs |
What this scope adds or changes vs what must stay the same. Unchanged column lists AC IDs only.
## 3. Edge-case registers
### Feature M01.S01.F01 [name]
(register table — IDs and short case labels; behavior cites BR/FR or Open #)
## 4. Stories by feature
(stories in the template — Level 0 → N across the file)
## 5. Dependency order
| Dep level | Stories | Depends on | Depth (foundation / trunk / branch / leaf) |
Must match `tracker.yaml` `depends_on`. Depth is team-set for version cuts; it does not reorder Level.
## 6. Coverage
| Feature / FR / flow / EC / existing behavior | Stories · AC IDs | Gap? |
## 7. Handoff
- Package: this file, `02-prd.md`, `03-ux/…` @ header versions (+ G03 frames when design stage on).
- Ready / not ready / open non-blocking: story IDs + reasons.
- Handoff status: Handed off | In design | Not yet (approver, date).
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
- Stories are written and listed Level 0 → N; section 5 matches `tracker.yaml` `depends_on`.
- Depth tags (foundation / trunk / branch / leaf) are set when the team uses harvest rings; they do not contradict Depends on.
- Brownfield: section 2b Delta is filled; every "must not change" PRD item has an "unchanged" AC listed there; greenfield: omit 2b when nothing Live is touched.
- No FR/BR/UX prose restated in stories (IDs only).
- Every story ends with its empty design-refs block. In update mode, existing design-refs blocks are kept exactly as they are, because design steps own them; a story whose screens change is noted in the change log so G02 refreshes its references.

## Tracker
In `tracker.yaml`: add one item per story (type `story`, parent the feature, `initiative`, `scope`, title, status `in_definition`, or `backlog` with the reason in the title or a note, `depends_on`, `depth` when the team set it, source this file). Record answers to queries about this scope that this run resolves. On approval, move the stories that meet the definition to `ready_for_dev`, or to `in_design` when the product has a design stage and the scope has screens. Run `lint --fix`; lint refuses `ready_for_dev` on a file that isn't approved. Next: with a design stage, design-02-screen-mockups for this scope (after design-01-sitemap-flows for the initiative); otherwise dev-01-tech-design for I-<nnn> (or dev-02-data-model if the initiative's tech design already covers this scope). Product continues with product-03-ux-flows or product-04-user-stories for the next scope. Version assignment (`fix_version`) is P06 — prefer trunk (+ deps) before branch/leaf of the same feature.
