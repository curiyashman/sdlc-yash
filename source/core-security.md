## PDLC core for the Security team (isolated, the same in every security skill)

This skill is one step of the Security team's engagement: **S00** scope and authorization, **S01** attack surface, **S02** vulnerability assessment, **S03** privacy and compliance audit, **S04** audit report and remediation, **S05** retest and sign-off. The team works **independently of the Product, Design, Development, QA, and Deployment teams on purpose**. It looks at the system the way a determined attacker, a malicious insider, and a regulator would, with fresh eyes and no inherited assumptions. The full rules are in `references/conventions.md` (read only the sections on the Security team and the file header).

**Isolation (the rule that makes the audit honest).**
- Read only: the scope sheet in `security/<engagement>/00-engagement.md`, the code repositories and running systems it names, the infrastructure and configuration it authorizes, and the team's own `security/` files.
- Do **not** read `product/`, `design/`, `dev/`, `qa/`, or `deploy/` documents, earlier threat models, architecture notes, or test plans, even if they are present in a repository you are reading. If you find one, skip it, and note in the file that you saw it and did not use it. Findings come from the code and the system, never from what the team says the system does. If a document is the only evidence of an intent (for example a retention promise), the person quotes it into the scope sheet.
- Do not ask the other teams how something works. Ask the person only for scope, access, test accounts, and authorization.

**Which product and engagement.** Settle which product and which engagement this run belongs to (an engagement is one assessment, such as a release, a quarterly audit, or a pre-launch audit). Use only that engagement's scope sheet, systems, and accounts. Never carry facts, IDs, or paths over from another product or engagement. [Product locations]

**Authorization comes first.** Nothing runs against any system until the scope sheet records, in the person's words: who owns the systems, who authorizes the testing, the targets, the environment, the dates, the allowed and forbidden methods, a stop contact, and any third-party terms. The hard limits are in `references/security-methodology.md` section 1. They cannot be waived by this skill: no unauthorized targets, no destructive actions, no real-user data, no exploit or malware development. If authorization is missing or unclear, stop and ask.

**Team boundary.** Security writes only in `security/` and appends its findings to `tracker.yaml` as items (type `vulnerability` or `privacy-gap`, with the `SF-` ID, severity, and a link to the report), without reading other entries. It does not fix the system. Fixes belong to Development (and Deployment for infrastructure); Security reviews them on retest. Only the named risk owner accepts a risk, recorded in `decisions/`. [Team boundary]

**Evidence over opinion.** Every finding rests on evidence from the code or the running system (Observed) or a cited source (Reference). A scanner result is a lead until verified. Findings never contain working exploits; they contain what an attacker could do, how it was shown safely, and how to fix it. Facts about the product, its users, data, rules, scale, or environment are never invented.

**The script.** `scripts/pdlc.py` (Python 3) is used here only for `new-id sf` and for `lint` limited to `security/` files; ignore lint output about other teams' files and do not open them. Where scripts can't run, allocate IDs by reading the highest `SF-` in your own engagement files and say "not linted".

**Start of every run.**
1. Settle the product and engagement; read `security/<engagement>/00-engagement.md` (if S00 is missing, this step must be sec-00).
2. Confirm the authorization and the allowed methods still hold for what this run will do.
3. Read the code and systems in scope (read-only unless the scope sheet allows active testing); what you observe is Observed.
4. If this step's file already exists, or the system changed since it was written, work in **update mode**: change only what the new input affects, bump `doc_version`, and add a change-log row.

**End of every run.**
1. Write the file at its path under the engagement folder. If this run can't write there, send the full file and name the exact path to commit it at. Set `status: approved` only on the explicit OK of the person or the approver recorded in the scope sheet.
2. Append new findings to `tracker.yaml` (items), and record risk acceptances in `decisions/DEC-<nnn>-<slug>.md`.
3. Run `lint` on `security/` files and fix what this run caused.
4. Name the next step in one line: S00 to S01 to S02 to S03 to S04 to S05; retests loop through S04 and S05.

**File header.** Every file starts with this front matter and ends with a Change log table (version | date | change | reason).

```yaml
---
pdlc_step: "S02"        # S00-S05
scope: 2026-10-20-prelaunch   # the engagement folder name under security/
doc_version: 1.0.0      # MAJOR: scope or conclusion changed; MINOR: findings added; PATCH: wording
status: draft           # draft | approved | superseded
depends_on: [security/2026-10-20-prelaunch/00-engagement.md@1.0.0]   # only security files
change_requests: []
open_items: 0           # how many Open items this file has
blocking: []            # numbers of the Open items that block later steps
updated: YYYY-MM-DD
result: ""              # S05 only: "Go" or "No-go"; S04 may carry "3 critical, 5 high"
---
```

## Core contract

**1. Label every fact.** Each requirement, row, or claim carries one label: in a Label or Source column in tables, as a short tag in bullets, or once in the heading of a section that holds one kind only.
- **Provided:** the person said or confirmed it, or an approved upstream file says it (cite the file and section).
- **Observed:** read directly in the product, the docs location, an attachment, or the code (cite the path or screen).
- **Reference:** from a cited external source, with its name and date.
- **Default:** an answer this skill proposed that the person has not confirmed yet. State what it is based on.
- **Recommendation:** professional judgment this step is allowed to give; its scope line says which.
- **Open:** unknown. Write it as a question, never fill it in.

Facts about the product, its users, data, rules, scale, or environment are never invented. They are Provided, Observed, Reference, or Open.

**2. Propose, then confirm.** Work through this step's questionnaire, but answer it yourself first as far as the sources allow:
- Skip every question that an upstream file, the docs, or the code already answers.
- For each remaining question, propose a **default** wherever you can defend one, and say what it rests on: something Observed in the product or code, an earlier decision of this product, the product's recorded conventions, or common practice (said as such).
- Present everything as one **confirm sheet**: a numbered table of question, proposed answer, and basis. The person can reply "all OK" or change items by number. Ask separately only the questions with no defensible default, blocking ones first. Use AskUserQuestion for closed choices when it is available.
- **Always confirmed explicitly, never left as Default:** anything irreversible; money and pricing; legal, privacy, and compliance; security and permissions; deleting or migrating user data; anything a later step treats as blocking.
- If the person says to go ahead, unconfirmed answers that are not on that list stay labeled Default in the file and are counted in `open_items`. "Not decided" or "don't know" is recorded as Open.
- Aim for one confirmation round per run. Follow up only on vague or conflicting answers.

**3. Confirm, then build.** Play back the inputs in short form (Provided, Default, Open, Out of scope) and get the go-ahead. In an unattended run, write the file with the confirm sheet and the Open items only, titled "Awaiting inputs".

**4. One file per run.** The deliverable is this step's .md file in the engagement folder. Besides it, a run touches only the engagement's `evidence/` folder (redacted evidence), `decisions/` for risk-acceptance records, and the line items it appends to `tracker.yaml` (see the team boundary). It never edits the system under test, its code, its configuration, or another team's folder. Use no other format unless the person names one.

**5. Short chat reply.** In one or two sentences, cover the file, what needs a decision, the lint result, and the next step. Never paste the file into chat.
