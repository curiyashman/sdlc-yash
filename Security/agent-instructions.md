# Security skill routing (add to the Security team's Claude project, or to CLAUDE.md and AGENTS.md)

## Product configuration (fill in for this product only; anything left blank is asked, never assumed)
- Product name:
- Docs location (repository or store, branch, folder). Chain files go in the docs path, `docs/pdlc/` unless set otherwise:
- Docs path, used below as `[docs path]`:
- Systems and repos authorized for this engagement (filled per engagement in S00):

One project or repository serves one product. To work on another product, use a separate project or fill in its own block.

This project uses the Security skills (sec-00 to sec-05) and pdlc-next when `config.security_stage: true`. Security is **independent**: do not read other teams' PDLC docs for findings.

## Sources and rules
- **Isolation:** read only the engagement scope sheet, authorized code/systems, and your own `security/` files. Do **not** read `product/`, `design/`, `dev/`, `qa/`, or `deploy/` documents for evidence. If you encounter one, skip it and note that you did not use it.
- **Authorization first:** nothing runs against a system until S00 records owner, authorizer, targets, environment, dates, allowed/forbidden methods, and stop contact.
- **Your files** live in `[docs path]/security/<engagement>/`. Append findings to `tracker.yaml` as vulnerability or privacy-gap items with `SF-` IDs; do not fix the system.
- **Hard limits:** see `references/security-methodology.md` — no unauthorized targets, no destructive actions, no real-user data, no exploit or malware development.
- **Lint:** after each run, run the skill's `scripts/pdlc.py lint --fix --root [docs path]` and then `board` where applicable.

## Which skill
| The task | Skill |
|---|---|
| What is next for Security | pdlc-next `--team security` |
| Scope and authorization for an engagement | sec-00-engagement-scope |
| Attack surface map | sec-01-attack-surface |
| Vulnerability assessment | sec-02-vulnerability-assessment |
| Privacy and compliance audit | sec-03-privacy-compliance-audit |
| Audit report and remediation tracking | sec-04-audit-report-remediation |
| Retest and Security Go / No-go | sec-05-retest-signoff |

Order: S00 → S01 → S02/S03 as scoped → S04 → S05. Pick one skill per turn, start with "Using sec-0X-name for [engagement] because [reason].", and name the next step at the end.
