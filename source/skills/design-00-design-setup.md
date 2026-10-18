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

{{CORE}}

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
