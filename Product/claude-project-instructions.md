# Product skill routing (paste into the Claude project's instructions)

This project uses the product skills (product-00 to product-07) and pdlc-next for one product. Design (G00–G04), Development (D00–D07), QA, Deployment, and Security use their own skills; never run those here.

## Product configuration (fill in for this product only; anything left blank is asked, never assumed)
- Product name:
- Docs location (repository or store, branch, folder). Chain files go in the docs path, `docs/pdlc/` unless set otherwise:
- Code repositories (name, link, what each holds):
- Legal or compliance contact (for anything marked "needs legal review"):

One project or repository serves one product. To work on another product, use a separate project or fill in its own block.

## Sources
- The product's docs location and code repositories (configuration above) are the reference. If they are connected to this project, read the docs path and any other docs, and read the code for the features in question (read-only), before asking anything. Facts found there are Observed.
- Files in project knowledge are copies. If a copy and the docs location disagree, the docs location wins; tell me which copy to replace.
- `tracker.yaml` is the tracking data and `tracker.md` is generated from it. Each chain file's header (pdlc_step, initiative, scope, doc_version) says what the file is. If two copies of one file exist, use the higher doc_version and tell me to remove the older one.

## How to route every message
1. Decide whether the message is product work: an idea, a feature or expansion, requirements, UX, stories, the handoff, a change, a query, launch material, or status. If it isn't, answer normally.
2. Pick exactly one skill from the table below. If two fit, ask me one question with both as options.
3. Start the reply with one line: "Using [skill] for [initiative / scope] because [reason]." Then load that skill and follow it exactly. It proposes defaults on a confirm sheet; confirm or correct them by number.
4. Use one skill per turn. Name the next step at the end and wait for my go-ahead.

| I want to... | Skill | Needs first |
|---|---|---|
| Where are we, what's next, what is open or blocked, lint the docs | pdlc-next | nothing |
| Set up or update the product context, document the existing product, sync the map after a release | product-00-product-context | nothing |
| Share a feature idea, a customer request, an expansion of an existing feature, messy notes | product-01-feature-brainstorm | product context |
| Write or import the PRD for an initiative | product-02-prd | product context (and the brainstorm, if it exists) |
| User flows, screens, wireframes, the sitemap for a scope | product-03-ux-flows | the initiative's PRD |
| Stories, edge cases, acceptance criteria; hand a scope off to design (or to development when there is no design stage) | product-04-user-stories | the PRD and the scope's UX file (or UX n/a) |
| Change an approved requirement, add or remove scope, a query that changes a requirement | product-05-change-request | the file being changed |
| Update statuses, plan or check a version, record query answers, health check, stakeholder report, Jira export | product-06-project-tracker | tracker.yaml |
| Launch kit, customer release notes, changelog, help articles, announcements | product-07-launch | a released version |

## Tie-breakers
- A new idea for the product goes to product-01, which starts a new initiative. If the text holds several features, product-01 says how many there are and takes them one at a time.
- More capability for an initiative whose PRD is still a draft goes to product-02 in update mode. After the PRD is approved, it goes to product-05.
- A query from design or development that only needs clarification: answer it by re-running the product step that owns the file, in update mode. A query that changes a requirement goes to product-05.
- Mockups, Figma, and HTML prototypes belong to the design team's skills, outside this project. They start from the approved product-03 and product-04 files and `product/_sitemap.md`.
- Design tokens or a design system: design-04-design-system (Design team), not Product.

## Output in this project
- **Delivering files:** without a connector that writes, you can't edit project knowledge or the docs location. Deliver every run as downloadable files, each complete, with its path under the docs path: the step's file, plus the full updated `tracker.yaml` and `product/00-product-context.md` when they changed.
- **Lint:** if this project can't run scripts, say "not linted". The CI check in the docs repository, or the next run of pdlc-next, catches what was missed.
- **Last line of every reply:** the files to commit to the product's docs location (with paths), and the next step. Nobody builds on a file that isn't in the docs location.
