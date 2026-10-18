# QA skill routing (add to the QA team's Claude project, or to CLAUDE.md and AGENTS.md)

## Product configuration (fill in for this product only; anything left blank is asked, never assumed)
- Product name:
- Docs location (repository or store, branch, folder). Chain files go in the docs path, `docs/pdlc/` unless set otherwise:
- Docs path, used below as `[docs path]`:
- Code repositories (name, link, what each holds):

One project or repository serves one product. To work on another product, use a separate project or fill in its own block.

This project uses the QA skills (qa-00 to qa-04) and pdlc-next when `config.qa_stage: true`. Product, Design, Development, Deployment, and Security use their own skills; never run those here except to read their approved files.

## Sources and rules
- **Read-only:** requirements and stories in `[docs path]/product/`, design handoff under `[docs path]/design/` when the design stage is on, developer test designs under `[docs path]/dev/**/05-qa/` (to avoid duplicating them). Expected results come only from requirements — never from reading implementation.
- **Your files** live in `[docs path]/qa/`. Tracking data is `[docs path]/tracker.yaml`.
- **Independence:** system/E2E tests, regression, accessibility/usability at product level, UAT coordination, and release Go / No-go are yours. Unit/integration/contract tests stay with Development (dev-05).
- **Never guess:** unclear acceptance criteria become queries (`to: product`). Do not invent expected results.
- **Lint:** after each run, run the skill's `scripts/pdlc.py lint --fix --root [docs path]` and then `board`.

## Which skill
| The task | Skill |
|---|---|
| What is next for QA, what is blocked or stale | pdlc-next `--team qa` |
| Set up QA strategy, matrix, exit criteria, defect process | qa-00-qa-setup |
| Test plan and cases for a scope (may start once stories are approved) | qa-01-test-plan |
| Execute tests when stories are `in_qa` | qa-02-test-execution |
| Release regression and Go / No-go in pre-production | qa-03-release-signoff |
| Performance, resilience, or other NFR testing | qa-04-nonfunctional-testing |

Order: qa-00 once when the QA stage turns on; qa-01 per scope; qa-02 when stories reach `in_qa`; qa-03 per staged version; qa-04 as needed. Pick one skill per turn, start with "Using qa-0X-name for [scope/version] because [reason].", and name the next step at the end.
