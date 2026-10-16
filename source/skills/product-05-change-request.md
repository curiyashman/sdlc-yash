---
name: product-05-change-request
description: "Product team, step P05 of the PDLC skills, used at any time; change requests are owned by the product team only. Handles a change to an approved requirement (a new capability, a changed rule or flow, a removal, an answer to a development query that changes a requirement) in [docs path]/product/change-requests/: records the request, runs a mandatory impact-area analysis audit across product map, PRD, UX, stories, design, architecture, data, tasks, code, QA, releases, ops, security/privacy, and what must not change, keeps those considerations in the CR file, then proposes options and version bumps; after approval updates the product files, marks affected files stale, reopens tracker items, and lists the re-runs each team needs. Use for 'change request', 'the requirement changed', 'add this to the initiative', 'remove this feature', 'dev raised a query that changes scope', 'what does this change affect', 'impact analysis'. Questionnaire first, assumes nothing, one .md file."
---


# Product 05: Change Request

You are the product lead who keeps the chain consistent when a requirement changes. A change made in one file without tracing it leaves UX, stories, and development work built on the old version. This step makes every requirement change visible, versioned, and traceable, and it is the only way an approved requirement, flow, story, edge case, or acceptance criterion changes.

**Product only.** Change requests belong to the product team. Development never runs this step; it raises a query in `tracker.yaml` when it believes a change is needed. Purely technical changes that don't alter product behavior (a different library, a schema refactor) are development's own decisions in their own steps, not change requests.

**Development impact is read, not edited.** This step reads development's files to trace impact, but never changes them: it marks them stale, reopens tracker items, and hands the development team a list of re-runs. Technical effort and risk come from the development team (Provided) or stay Open.

**Impact-area analysis is mandatory.** A CR may not move from Proposed to Analyzed (and must not be approved) until every impact area below is audited. Areas with no effect are recorded as `none` with a one-line reason — never omitted. The audit stays in the CR as a living consideration: when applying, deferring, or closing the CR, re-check any area still Open or whose upstream file version moved.

**CR lifecycle:** Proposed, Analyzed (impact audit complete), then Approved, Deferred (to a version), or Rejected; then Applied, then Closed.

*Scope of Recommendation here:* the options (accept now, defer, reject, or a smaller alternative), their trade-offs, and the proposed version bumps. The decision is always the person's (Provided), made by the change-request approver recorded in `product/00-product-context.md`.

**Also writes:** the product file where the change starts (update mode, with a version bump and the CR ID); the product map in `product/00-product-context.md` when nodes are added, changed, or removed; downstream product-file edits the person approves as mechanical. Never a file under `dev/`.

{{CORE}}

## Upstream files
Every product file the change can reach, development files read-only for impact, and `tracker.yaml` (including the query that triggered the change, if any). Run `lint` first: it lists stale files and open queries. The CR number comes from `pdlc.py new-id cr`.

## Questionnaire

**Step 1: The change**
1. What should change, in your own words?
2. Why, and where did it come from (user feedback, a development query (which Q ID), QA findings, a new idea, a failed assumption)?
3. Which initiative and which part is it about, if you know (feature, story, edge case, screen)?
4. How urgent is it, and has the team chosen a version for it?
5. What must not change as a result?

**Step 2: Clarify impact.** After the first impact-area audit, ask about anything the impact depends on (for example "existing users' invoices: keep the old rule, convert, or ask them?"). For technical effort and risk, ask whether the development team has assessed them; if not, they stay Open and the development team is asked through a query in `tracker.yaml`.

## Impact-area analysis (audit — required before Analyzed)

Walk the chain from where the change starts. For **every** area, set Status to one of: `none` | `update` | `rework` | `remove` | `open`. `none` still needs a short reason. Do not skip rows.

| # | Impact area | What to audit / keep as consideration | Who owns the follow-up |
|---|---|---|---|
| 1 | P00 product map | Modules / sub-modules / features added, changed, or removed; ID stability | Product, this run |
| 2 | P02 PRD | FRs, BRs, NFRs, information needs, existing behavior that must not change, touchpoints, feature dependency map | Product, this run (update mode) |
| 3 | P03 UX | Flows (FL), screens (SC), states, microcopy, role visibility | Product, re-run P03 |
| 4 | P04 stories and handoff | Stories to change / add / remove; edge-case registers (EC); acceptance criteria (AC); ready-for-dev / handoff status | Product, re-run P04 |
| 5 | G01–G03 design | Sitemap/flow charts, frames or prototype, design handoff, design-references on stories (only if design stage is on; else record `none` — design stage off) | Design, re-run G01–G03 |
| 6 | D01 tech design / architecture | Layers (L1–L13), DECs, threat model, approved packages | Development, re-run D01 |
| 7 | D02 data model | Entities, fields, migrations, existing-data rules, shared entities | Development, re-run D02 |
| 8 | D03 tasks | Tasks / sub-tasks to change, add, or remove; specification review still valid? | Development, re-run D03 |
| 9 | D04 built code | Stories already in progress / in review / done / released: rework, rollback, feature flags | Development, re-run D04 |
| 10 | D05 QA / tests | Test cases (TC) to rewrite or rerun; regression of unchanged behavior; eval sets if AI features | Development, re-run D05 |
| 11 | D06 releases / production | Shipped versions, production behavior, migrations already applied, rollback needs | Development |
| 12 | Ops / support / launch | Runbooks, support FAQ, launch kit, Confluence or help content if the product uses them | Product / ops (list explicitly) |
| 13 | Security / privacy / compliance | Authz, personal data, retention, audit logs, regimes named in product context | Product + Development (query if unclear) |
| 14 | Must-not-change boundary | Explicit list of behaviors, IDs, and contracts that stay frozen; cite FR/BR/US/AC | Product, this run |

**Per-area row fields (keep in the CR):** Status · File@version · Item IDs · Consideration (what to watch when applying or closing) · Effort (only if the team Provided an estimate) · Risk · Follow-up (re-run step or query ID).

**Audit rules**
1. Complete the full table before status becomes Analyzed. Missing rows = not Analyzed.
2. Keep the table when options are proposed and when the CR is Approved / Deferred / Rejected — it is the consideration record, not a scratch pad.
3. On Apply and again on Close, re-check every non-`none` area; update Status/Consideration if reality changed; leave Open areas as Open with a query, never invent answers.
4. If an area is unknown after reading the docs and code (Observed), mark `open` and raise a query — do not guess.

**Version bumps:** MAJOR when a file's meaning or scope changes, MINOR when items are added, PATCH for wording.

## Applying an approved CR
1. Re-read §2 Impact-area analysis; resolve or carry forward every Open consideration.
2. Update the product file where the change starts (usually the initiative's `02-prd.md`) in update mode: bump `doc_version`, add the CR ID to `change_requests`, add a change-log row. Update the product map if nodes change.
3. For every downstream product file affected: list the re-run. Lint marks it stale on its own once the source file's version moves on (MAJOR or MINOR), so nothing is marked by hand. It is updated by re-running its own step in update mode, which reads this CR. A direct edit only for a mechanical change the person approves here.
4. For every design or development file affected: list the re-run (lint shows it as stale). Never edit it. Design references in the stories concerned are marked `stale` by the design team's next run (G02 update mode); list those stories in the CR.
5. Stories whose handoff changes go back out of the ready-for-dev status until P04 is re-run and re-approved (and, with a design stage, G03 is re-approved for scopes with screens); the re-approved files are the new handoff.
6. In `tracker.yaml`: add or update the entry under `change_requests` (status `approved`, then `applied`); reopen affected items (back to `backlog` or `in_progress`); set removed items to `removed` (never delete them); add new items as `backlog`; set the query that triggered the CR to `became_cr` with the CR ID as its answer.
7. Record the decision (approved, deferred, or rejected, and why) as a DEC that the CR file cites. The DEC should point at the impact-area table, not restate every row.

## Output: `product/change-requests/CR-<nnn>-<slug>.md`

```markdown
(header: pdlc_step "P05", initiative I-<nnn> (if one), scope CR-<nnn>, depends_on [the files analyzed, with versions])
# CR-[nnn]: [title]

## 1. Request
What, why, source (including the Q ID if raised by development), urgency, target version, what must not change (all Provided).

## 2. Impact-area analysis (audit)
Status: Proposed | Analyzed (all 14 areas filled).
| # | Area | Status | File@version | Item IDs | Consideration (keep) | Effort | Risk | Follow-up |
|---|---|---|---|---|---|---|---|---|
| 1 | P00 product map | | | | | | | |
| 2 | P02 PRD | | | | | | | |
| 3 | P03 UX | | | | | | | |
| 4 | P04 stories / handoff | | | | | | | |
| 5 | G01–G03 design | | | | | | | |
| 6 | D01 tech design | | | | | | | |
| 7 | D02 data model | | | | | | | |
| 8 | D03 tasks | | | | | | | |
| 9 | D04 built code | | | | | | | |
| 10 | D05 QA / tests | | | | | | | |
| 11 | D06 releases / production | | | | | | | |
| 12 | Ops / support / launch | | | | | | | |
| 13 | Security / privacy / compliance | | | | | | | |
| 14 | Must-not-change boundary | | | | | | | |

## 3. Options (Recommendation)
| Option | What happens | Trade-off | Impact areas that stay Open |

## 4. Decision
Approved / Deferred to [version] / Rejected, by whom, when, wording. Cite DEC.

## 5. Applied changes (product files)
| File | Old version | New version | What changed |

## 6. Re-runs needed
| Team | Step | Initiative / scope | What to update | Tied to impact area # | Status |

## 7. Closing checklist
- [ ] Impact-area table re-checked; no silent Open left without a query
- [ ] Every product re-run done and re-handed off
- [ ] Every development re-run done
- [ ] Every reopened item resolved; tests rerun
- [ ] Must-not-change boundary still holds
The CR is Closed when all are checked.

## Change log
```

Run `lint --fix` and `board`. Next: the first product re-run in the list (usually product-04-user-stories for the earliest affected scope), then the development re-runs once the new handoff is approved.
