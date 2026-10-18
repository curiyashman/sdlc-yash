# Design skill routing (add to the design team's Claude project, or to CLAUDE.md and AGENTS.md of the repository you work in)

## Product configuration (fill in for this product only; anything left blank is asked, never assumed)
- Product name:
- Docs location (repository or store, branch, folder). Chain files go in the docs path, `docs/pdlc/` unless set otherwise:
- Docs path, used below as `[docs path]`:
- Code repositories (name, link, what each holds):
- Figma files (links), or "HTML prototype" as the design medium:

One project or repository serves one product. To work on another product, use a separate project or fill in its own block.

This project uses the design skills (design-00 to design-04) and pdlc-next. Product, Development, QA, Deployment, and Security use their own skills; never run those here.

## Sources and rules
- **Product files** in `[docs path]/product/` are read-only here. Design works only on scopes whose stories file (product-04) is approved. A gap in them becomes a query in `[docs path]/tracker.yaml` (`to: product`), never a guess.
- **The one exception to read-only:** you write design references into the product files. These are the frame or prototype links per story (in the marked design-refs block), the Figma column in the UX file, and the Design column in the sitemap. Never edit anything else there. Every screen you create must be referenced from its story.
- **Your files** live in `[docs path]/design/`. Read the product's docs location and the existing Figma files before asking anything. Any file made elsewhere is committed to its path under the docs path before anyone relies on it.
- **Figma:** check which Figma tools are present before promising anything. If the Figma connector isn't connected, say so and ask the person to connect it. With read-only tools, the skills write build briefs instead of frames. With an HTML prototype as the medium, they build clickable pages in the docs location.
- **Lint:** after each run, run the skill's `scripts/pdlc.py lint --fix --root [docs path]` and then `board`. Where scripts can't run, say "not linted".

## Which skill
| The task | Skill |
|---|---|
| What is ready to design, what's next, what is open | pdlc-next |
| Connect Figma, choose Figma or an HTML prototype, record files, design system, conventions, approvers | design-00-design-setup |
| Put the sitemap and flow charts into FigJam, list the screens to design for an initiative | design-01-sitemap-flows |
| Create mockups for a scope in Figma, as an HTML prototype, or as a build brief | design-02-screen-mockups |
| Review mockups against stories, map stories to frames, sign off the design handoff | design-03-design-handoff |
| Take in the existing design system, audit it against the project, then adopt, refine, or create it: tokens, atoms to composite components, patterns, platforms and breakpoints, accessibility matrix, phased plan | design-04-design-system |

Order: design-00 once, design-04 when the product needs a design system (audit and approval before anything is built), design-01 per initiative, then design-02 and design-03 per scope, lowest dependency level first. Pick one skill per turn, start the reply with "Using design-0X-name for [initiative / scope] because [reason].", and name the next step at the end.
