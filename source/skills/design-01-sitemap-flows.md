---
name: design-01-sitemap-flows
description: "Design team, step G01 of the PDLC skills. For one initiative, turns the product team's sitemap and user-flow charts (Mermaid in product/_sitemap.md and the 03-ux files) into shared charts in FigJam, checks the charts against the screen tables, and writes the screen design list: every screen to mock up, per scope, with roles, new or changed status, and dependency level. Writes [docs path]/design/ initiative 01-sitemap-flows.md and puts the FigJam links back under the charts in the product files. Use for 'put the sitemap in Figma', 'make the flow charts', 'which screens need design', 'prepare design for this initiative'. Questionnaire first, assumes nothing, one .md file."
---

# Design 01: Sitemap and Flow Charts

You are a design lead preparing an initiative for mockups. The product team defined where screens sit and how users move between them (step P03). Here those charts become shared design artifacts and the list of screens to design, so every mockup starts from the same map and nothing is designed twice or missed.

**You do not redraw the product.** The charts come from the product files. If a chart and its table disagree, or a screen is missing, that is a query to Product, not a fix here.

*Scope of Recommendation here:* only the layout of the shared charts (grouping and arrangement). Screens, transitions, and roles are Provided by the product files.

**Capability check.** Read `design/00-design-setup.md` for the capability level. At level A or B, create the charts in FigJam with the Figma diagram tool (Mermaid in, FigJam diagram out) and record each URL. At level C, no diagrams are created: the Mermaid source in the file is the deliverable, ready to paste into any tool.

**Also writes:** FigJam diagrams in the connected Figma project (levels A and B), and the link line under each chart in its source product file (`product/_sitemap.md` or the `03-ux` file), as described under Design references.

{{CORE}}

## Upstream files
`design/00-design-setup.md`; `product/_sitemap.md` (chart and Screens table); for the initiative: `product/I-<nnn>-<slug>/02-prd.md` (placement), every `03-ux/*.md` (flow charts, screen inventories, touchpoints), and the `04-stories` files (to see which scopes are approved); `tracker.yaml` (dependency levels from `lint`).

## Questionnaire (skip what upstream files answer)
1. Which initiative?
2. Which charts go into FigJam: the sitemap excerpt for this initiative, the flows of every scope, or a list you choose? (Default: the sitemap excerpt and every flow of every scope that has an approved UX file.)
3. Where in Figma: the FigJam file and page, or create a new file in the project from `design/00-design-setup.md`?
4. Should charts show role-specific views separately (one chart per role) or all roles in one chart?
5. Anything in the current charts you already know is wrong or incomplete?

## Process
1. **Collect the charts** from `_sitemap.md` and each UX file, at their versions. Keep the Mermaid source verbatim.
2. **Consistency check:** every node in a chart is a screen in the matching table, every table screen appears in a chart, every edge is a transition in a flow table, every role-restricted screen names its roles. Record each mismatch as a finding; blocking ones become queries to Product.
3. **Create the diagrams** (levels A and B), one per chart, titled with the chart's source (`I-003 sitemap`, `M01.S01-FL01 create invoice`). Record URL and node. If creation fails or the result differs from the source, say so in the file.
4. **Screen design list:** every screen from the initiative's UX inventories, per scope: ID, name, type, New / Changed / Existing, roles, the scope's dependency level, the platforms and size classes it must be designed for (from the G00 profile), and whether its scope's stories are approved (the design stage starts only for approved scopes). Existing screens being changed need a link to the current Figma frame or a screenshot.
5. **Write back:** put each diagram's link on the line under its chart in the source product file (PATCH bump, change-log row), and record the write in section 2 of this file.
6. **Gaps:** screens the PRD placement implies but no UX file defines, scopes without an approved UX file, and charts that can't be built, as queries.

## Output: `design/I-<nnn>-<slug>/01-sitemap-flows.md`

```markdown
(header: pdlc_step "G01", initiative I-<nnn>, scope I-<nnn>, depends_on [design/00-design-setup.md@x, product/_sitemap.md@x, product/I-<nnn>-<slug>/03-ux/<scope>-<slug>.md@x])
# Sitemap and flows: I-[nnn] [name]


## 1. Sources
| File | Version | Status | Label |
## 2. Charts
| Chart | Source (file@version, section) | FigJam link | Link written back (file@new version) | Matches its table? | Label |
### Sitemap (excerpt)
(Mermaid source, verbatim)
### <scope>-FL01 [name]
(Mermaid source, verbatim; one block per chart)
## 3. Screen design list
| Screen ID | Name | Scope | Type | New / Changed / Existing | Roles | Platforms and size classes | Navigation pattern per size class | Dep level | Stories approved? | Current frame (changed screens) | G02 |
## 4. Consistency findings
| # | Finding | Chart / table | Blocking? | Query |
## 5. Touchpoints
## 6. Open questions
## Change log
```

## Tracker
Add the queries this run raises to `tracker.yaml` (`to: product`). Next: design-02-screen-mockups for a scope whose stories are in design, lowest dependency level first.
