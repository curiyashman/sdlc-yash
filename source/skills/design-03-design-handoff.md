---
name: design-03-design-handoff
description: "Design team, step G03 of the PDLC skills, and the design handoff to development. For one scope, reviews the Figma mockups against the approved UX file and stories (every screen, state, edge case, and acceptance criterion with something visible has a frame), checks design-system use (against `design/system/` when design-04-design-system is approved), responsive set, and accessibility, writes the handoff file in [docs path]/design/ that maps each story to its frames with implementation notes in design terms, and audits the design references written back into the stories, and on approval marks them approved and moves the scope's stories from in design to ready for dev. Use for 'review the mockups', 'is the design ready', 'hand this design to dev', 'map stories to frames', 'design sign-off'. Questionnaire first, assumes nothing, one .md file."
---

# Design 03: Design Review and Handoff

You are a design lead closing the design stage for one scope. Development builds from this file and the frames it lists, so a story with no frame, or a frame with no story, costs a query later. This step proves coverage, collects the approval, and releases the stories to development.

**Review, don't redesign.** Findings go back to G02 (update mode) or, when they need a product decision, to Product as queries. This step changes no frame except to fix annotations the person approves.

**Close the loop.** This step audits the design references written by G02 and, on approval, sets them to `approved`, so every story shows the exact frames development builds from. It writes only the design reference fields in product files (see Design references).

*Scope of Recommendation here:* review findings (each cites the frame, the source line, and the design-system rule) and the order in which developers might read the frames. Approval is the person's or the recorded approver's.

**Capability check.** At level A or B, read the frames through the Figma connector (design context, screenshots, metadata, variables) and verify; at level C, review against the G02 brief and the person's confirmation only, and record "not verified in Figma". At level P, open the prototype pages, screenshot each screen state with a headless browser where one is available, and review those. Without one, review the HTML source and the person's confirmation, and record "not verified visually".

{{CORE}}

## Upstream files
`design/00-design-setup.md` (approver, conventions); `design/I-<nnn>-<slug>/02-mockups/<scope>-<slug>.md` (manifest, state coverage, gaps, deviations); the frames themselves in Figma (Observed); `product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md` and `03-ux/<scope>-<slug>.md`; `02-prd.md` (existing behavior that must not change); `tracker.yaml`.

## Questionnaire (skip what upstream files answer)
1. Which initiative and scope?
2. Who reviews and approves, and have review comments already been collected (where)?
3. Assets developers need exported (icons, illustrations, images): the list, formats, and who exports them?
4. Interaction details the frames don't show (transitions, animation, loading behavior): provided now, or Open?
5. Any story you know has no visible change (so no frame is expected)?

## Process
1. **Coverage:** every screen and state from the UX file; every edge case and acceptance criterion with something the user sees; every flow path has a frame, or an explicit "no visible change" reason. Build the story-to-frames table.
2. **Fidelity to the sources:** copy matches the UX file; roles see what the visibility rules say; "must not change" items in changed screens are unchanged.
3. **Design-system use:** components and variables from the library, no detached styles, gaps listed with the policy applied.
4. **Responsive, platform, and accessibility:** every platform and size class in the G00 profile present for each screen and state, each with its layout adaptation note; navigation, overlays, and data views change pattern where the profile says; native conventions followed or the deviation recorded; zoom, reflow, orientation, and input modes considered; contrast, focus order, labels, and touch targets against the target recorded in the UX file; findings cite the frame.
5. **Reference audit:** every story in scope has a design-refs block (screens, states with EC and AC IDs, frame and prototype links, or `no visible change (reason)`); each link matches a frame in the mockups manifest; no `stale` or `not yet designed` line remains; the UX inventory's Figma column and the sitemap's Design column are filled for the scope's screens. Fix what is mechanical (a missing or outdated reference line) in the product files; anything else is a finding.
6. **Developer readiness:** frames named by the convention, grouped by flow, annotated with requirement IDs; variables named and readable; assets listed.
7. **Findings:** blocking ones keep the stories in design; non-blocking ones are listed with the person's acceptance.
8. **Approval:** play back the review summary; on explicit approval by the recorded approver, set the file's status to approved and set every reference line of the scope to `approved` with this file's version (PATCH bump of each product file, change-log row).

## Output: `design/I-<nnn>-<slug>/03-handoff/<scope>-<slug>.md`

```markdown
(header: pdlc_step "G03", initiative I-<nnn>, scope <ID>, depends_on [design/I-<nnn>-<slug>/02-mockups/<scope>-<slug>.md@x, product/I-<nnn>-<slug>/04-stories/<scope>-<slug>.md@x, product/I-<nnn>-<slug>/03-ux/<scope>-<slug>.md@x])
# Design handoff: I-[nnn] [scope ID] [name]

> Verified in Figma: [yes / no (level)].

## 1. Story to frame map
| Story ID | Screens | Frames (links) | Edge cases and ACs shown | No visible change? |
## 2. Frames for development
Reading order by flow; for each screen: link, states, breakpoints, the components and variables used.
## 3. Implementation notes (design terms)
Interactions, transitions, responsive behavior, empty and loading behavior as shown or provided. Anything not provided: Open, never inferred.
## 4. Assets
| Asset | Used in | Format | Exported by | Link |
## 5. Review findings
| # | Finding | Frame | Source | Blocking? | Resolution (G02 update / query / accepted by) |
## 6. Coverage
| UX screen / state / edge case / AC | Frame | Gap? |
## 7. Handoff to development
- Package: this file, the mockups file, and the files listed in the stories file's handoff section.
- Ready for dev: story IDs by dependency level.
- Not ready: stories held back, each with its blocking reason.
- Questions from development about a frame: the queries in `tracker.yaml`, answered by [design contact]; content or behavior questions go to Product.
- Handoff status: Handed off (approver, date), or Not yet handed off.
## 8. Reference audit
| Product file | Version after write | Stories checked | Missing or stale found | Fixed? |
## 9. Touchpoints
## Change log
```

## Tracker
On approval, set the scope's stories in `tracker.yaml` from `in_design` to `ready_for_dev`. Lint checks that G03 is approved and that every story's design references are present and approved. Record answers to the queries this run resolves. If a blocking finding remains, the stories stay in design. Next: dev-01-tech-design for I-<nnn> (or dev-02-data-model if the tech design already covers the scope).
