"""Writes the sample product used by the tests and as a worked example (fictional product: Ledgerly)."""
import os, sys, textwrap
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample-product", "docs", "pdlc")

def w(rel, fm, body):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    head = "---\n" + textwrap.dedent(fm).strip() + "\n---\n"
    with open(p, "w") as f:
        f.write(head + textwrap.dedent(body).lstrip("\n") + "\n## Change log\n| Version | Date | Change | CR / query / DEC |\n|---|---|---|---|\n| 1.0.0 | 2026-10-01 | Created | |\n")

I = "product/I-001-bulk-invoicing"
w("product/00-product-context.md", """
pdlc_step: "P00"
scope: product
doc_version: 1.1.0
status: approved
depends_on: []
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-01
""", """
# Product context: Ledgerly (fictional sample)
## 1. Product card
Docs location: this folder (sample). Code repositories: web, api (sample). Label: Provided.
## 3. Product map
| ID | Level | Name | Status | Label |
|---|---|---|---|---|
| M01 | Module | Billing | Live | Provided |
| M01.S01 | Sub-module | Invoices | Live | Provided |
| M01.S01.F01 | Feature | Create invoice | Live | Provided |
| M01.S01.F02 | Feature | Invoice list | Live | Provided |
| M01.S02 | Sub-module | Bulk actions | Planned (I-001) | Provided |
| M01.S02.F01 | Feature | Bulk send | Planned (I-001) | Provided |
""")
w(f"{I}/01-brainstorm.md", """
pdlc_step: "P01"
initiative: I-001
scope: I-001
doc_version: 1.0.0
status: approved
depends_on: [product/00-product-context.md@1.1.0]
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-01
""", """
# Brainstorm: I-001 Bulk invoicing
One feature: send many invoices at once from the invoice list (M01.S01.F02). Label: Provided.
""")
w(f"{I}/02-prd.md", """
pdlc_step: "P02"
initiative: I-001
scope: I-001
doc_version: 1.2.0
status: approved
depends_on: [product/00-product-context.md@1.1.0, product/I-001-bulk-invoicing/01-brainstorm.md@1.0.0]
change_requests: []
open_items: 1
blocking: []
updated: 2026-10-02
""", """
# PRD: I-001 Bulk invoicing
## 4. Placement
| ID | Level | Name | Change | Label |
|---|---|---|---|---|
| M01.S02 | Sub-module | Bulk actions | New | Provided |
| M01.S02.F01 | Feature | Bulk send | New | Provided |
| M01.S01.F02 | Feature | Invoice list | Changed | Provided |
## 5. Feature requirements
### M01.S02.F01 Bulk send (New)
| FR ID | Requirement | Label |
|---|---|---|
| M01.S02.F01-FR01 | While the invoice list shows draft invoices, the invoice list shall let the account owner select up to 200 of them. | Provided |
| M01.S02.F01-FR02 | When the account owner confirms a bulk send, the product shall send every selected invoice and show each one's result. | Provided |
Business rules
| BR ID | Rule | Label |
|---|---|---|
| M01.S02.F01-BR01 | If a selected invoice has no customer email, then bulk send shall skip it and list it as not sent. | Provided |
## 7. Non-functional
| I-001-NFR01 | When a bulk send of 200 invoices starts, the product shall finish it within the time the team sets (value Open). | Open |
## 12. Open questions
| 1 | Maximum time users accept for a bulk send? | I-001-NFR01 | No | Product |
""")
w("product/_sitemap.md", """
pdlc_step: "P03"
scope: product
initiative: I-001
doc_version: 1.0.1
status: approved
depends_on: []
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-03
""", """
# Sitemap: Ledgerly
## Chart
```mermaid
flowchart TD
  M01_S01_SC01["M01.S01-SC01 · Invoice list"] -->|"Select"| M01_S02_SC01["M01.S02-SC01 · Bulk send dialog"]
```
FigJam: https://www.figma.com/board/sample (design references, G01)
## Screens
| Screen ID | Name | Status | UX file | Design |
|---|---|---|---|---|
| M01.S01-SC01 | Invoice list | Changed (I-001) | 03-ux/M01.S02-bulk-actions.md | https://www.figma.com/design/sample?node-id=1-2 |
| M01.S02-SC01 | Bulk send dialog | New (I-001) | 03-ux/M01.S02-bulk-actions.md | https://www.figma.com/design/sample?node-id=1-3 |
""")
w(f"{I}/03-ux/M01.S02-bulk-actions.md", """
pdlc_step: "P03"
initiative: I-001
scope: M01.S02
doc_version: 1.0.1
status: approved
depends_on: [product/I-001-bulk-invoicing/02-prd.md@1.2.0]
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-03
""", """
# UX: I-001 M01.S02 Bulk actions
## 3. Flows
### M01.S02-FL01 Send selected invoices (happy path; new)
| Step | Role | Action | System response | Screen |
|---|---|---|---|---|
| 1 | Account owner | Selects drafts | Shows count | M01.S01-SC01 |
| 2 | Account owner | Clicks Send | Opens dialog | M01.S02-SC01 |
## 5. Screen inventory
| Screen ID | Name | New / Changed | Figma (written by design steps) |
|---|---|---|---|
| M01.S01-SC01 | Invoice list | Changed, existing, first documented here | https://www.figma.com/design/sample?node-id=1-2 |
| M01.S02-SC01 | Bulk send dialog | New | https://www.figma.com/design/sample?node-id=1-3 |
Implements M01.S02.F01-FR01 and M01.S02.F01-FR02.
""")
w(f"{I}/04-stories/M01.S02-bulk-actions.md", """
pdlc_step: "P04"
initiative: I-001
scope: M01.S02
doc_version: 1.0.2
status: approved
depends_on: [product/I-001-bulk-invoicing/02-prd.md@1.2.0, product/I-001-bulk-invoicing/03-ux/M01.S02-bulk-actions.md@1.0.1]
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-05
""", """
# Stories and handoff: I-001 M01.S02 Bulk actions
## 3. Edge-case registers
| EC ID | Edge case | Expected behavior | Label |
|---|---|---|---|
| M01.S02.F01-EC01 | An invoice has no customer email | It is skipped and listed as not sent (M01.S02.F01-BR01) | Provided |
## 4. Stories
### M01.S02.F01-US01 Select draft invoices
As an account owner, I want to select many draft invoices, so that I can act on them at once. Implements M01.S02.F01-FR01. Screens M01.S01-SC01.
- M01.S02.F01-US01-AC01 (verifies M01.S02.F01-FR01): Given drafts in the list, when I tick them, then the count of selected invoices shows.
Design references (written by design steps; leave empty when writing a story)
<!-- design-refs:start -->
M01.S01-SC01 · default, selected (M01.S02.F01-US01-AC01) -> https://www.figma.com/design/sample?node-id=1-2; prototype M01.S02-FL01 -> https://www.figma.com/proto/sample · design/I-001-bulk-invoicing/02-mockups/M01.S02-bulk-actions.md@1.0.0 · approved
<!-- design-refs:end -->
### M01.S02.F01-US02 Send selected invoices
As an account owner, I want to send the selected invoices, so that customers get them without one-by-one sending. Implements M01.S02.F01-FR02, M01.S02.F01-BR01. Screens M01.S02-SC01. Depends on M01.S02.F01-US01.
- M01.S02.F01-US02-AC01 (verifies M01.S02.F01-FR02): Given selected drafts, when I confirm, then each invoice shows sent or not sent.
- M01.S02.F01-US02-AC02 (M01.S02.F01-EC01, verifies M01.S02.F01-BR01): Given an invoice without email, when I confirm, then it is listed as not sent with the reason.
Design references (written by design steps; leave empty when writing a story)
<!-- design-refs:start -->
M01.S02-SC01 · default, result, error (M01.S02.F01-US02-AC01, M01.S02.F01-US02-AC02) -> https://www.figma.com/design/sample?node-id=1-3 · design/I-001-bulk-invoicing/02-mockups/M01.S02-bulk-actions.md@1.0.0 · approved
<!-- design-refs:end -->
## 8. Handoff to development
Handed off (product approver, 2026-10-04).
""")
w("design/00-design-setup.md", """
pdlc_step: "G00"
scope: product
doc_version: 1.0.0
status: approved
depends_on: [product/00-product-context.md@1.1.0]
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-01
""", """
# Design setup: Ledgerly
Capability level: B (read and diagram). Label: Observed.
""")
D = "design/I-001-bulk-invoicing"
w(f"{D}/02-mockups/M01.S02-bulk-actions.md", """
pdlc_step: "G02"
initiative: I-001
scope: M01.S02
doc_version: 1.0.0
status: approved
depends_on: [design/00-design-setup.md@1.0.0, product/I-001-bulk-invoicing/03-ux/M01.S02-bulk-actions.md@1.0.1, product/I-001-bulk-invoicing/04-stories/M01.S02-bulk-actions.md@1.0.1]
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-04
""", """
# Mockups: I-001 M01.S02 Bulk actions
| Screen ID | State | Frame | Link |
|---|---|---|---|
| M01.S01-SC01 | selected | M01.S01-SC01 · Invoice list / selected / desktop | https://www.figma.com/design/sample?node-id=1-2 |
| M01.S02-SC01 | result | M01.S02-SC01 · Bulk send dialog / result / desktop | https://www.figma.com/design/sample?node-id=1-3 |
""")
w(f"{D}/03-handoff/M01.S02-bulk-actions.md", """
pdlc_step: "G03"
initiative: I-001
scope: M01.S02
doc_version: 1.0.0
status: approved
depends_on: [design/I-001-bulk-invoicing/02-mockups/M01.S02-bulk-actions.md@1.0.0, product/I-001-bulk-invoicing/04-stories/M01.S02-bulk-actions.md@1.0.2]
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-05
""", """
# Design handoff: I-001 M01.S02
| Story | Frames |
|---|---|
| M01.S02.F01-US01 | M01.S01-SC01 |
| M01.S02.F01-US02 | M01.S02-SC01 |
""")
w("dev/00-dev-setup.md", """
pdlc_step: "D00"
scope: product
doc_version: 1.0.0
status: approved
depends_on: [product/00-product-context.md@1.1.0]
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-01
""", """
# Dev setup: Ledgerly
Code repositories: web (front end), api (back end). Label: Provided.
""")
w("dev/architecture.md", """
pdlc_step: "D01"
scope: product
doc_version: 1.0.0
status: approved
depends_on: [dev/00-dev-setup.md@1.0.0]
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-01
""", """
# Architecture: Ledgerly
L3: relational database (Observed). Background jobs: DEC-001.
""")
V = "dev/I-001-bulk-invoicing"
w(f"{V}/01-tech-design.md", """
pdlc_step: "D01"
initiative: I-001
scope: I-001
doc_version: 1.0.0
status: approved
depends_on: [dev/architecture.md@1.0.0, product/I-001-bulk-invoicing/02-prd.md@1.2.0]
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-05
""", """
# Tech design: I-001
Bulk send runs as a background job per DEC-001. Threat model: sending to wrong customer (M01.S02.F01-BR01 enforced server side).
""")
w(f"{V}/05-qa/M01.S02-bulk-actions.md", """
pdlc_step: "D05"
initiative: I-001
scope: M01.S02
doc_version: 1.0.1
status: approved
depends_on: [product/I-001-bulk-invoicing/04-stories/M01.S02-bulk-actions.md@1.0.2, dev/I-001-bulk-invoicing/01-tech-design.md@1.0.0]
change_requests: []
open_items: 0
blocking: []
result: "1/3 pass"
updated: 2026-10-07
""", """
# QA: I-001 M01.S02 (test design, then results)
## 3. Test cases
| TC ID | Covers | Level | Expected | Result |
|---|---|---|---|---|
| M01.S02.F01-US01-TC01 | M01.S02.F01-US01-AC01 | frontend unit | count matches selection | Pass |
| M01.S02.F01-US02-TC01 | M01.S02.F01-US02-AC01 | integration | each invoice reports sent or not sent | Not run |
| M01.S02.F01-US02-TC02 | M01.S02.F01-US02-AC02, M01.S02.F01-EC01 | integration | invoice without email listed as not sent with reason | Not run |
""")
w(f"{V}/03-tasks/M01.S02-bulk-actions.md", """
pdlc_step: "D03"
initiative: I-001
scope: M01.S02
doc_version: 1.0.0
status: approved
depends_on: [dev/I-001-bulk-invoicing/01-tech-design.md@1.0.0, product/I-001-bulk-invoicing/04-stories/M01.S02-bulk-actions.md@1.0.2, dev/I-001-bulk-invoicing/05-qa/M01.S02-bulk-actions.md@1.0.0]
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-08
""", """
# Tasks: I-001 M01.S02
```yaml pdlc-tasks
- id: M01.S02.F01-US01-T01
  title: Selection state in the invoice list
  layer: frontend
  repo: web
  status: done
  build: When the account owner ticks draft invoices, the invoice list shall show the count of selected invoices.
  implements: [M01.S02.F01-US01-AC01]
  tests: [M01.S02.F01-US01-TC01]
  budget: {files: 2, lines: "+60 / -5"}
- id: M01.S02.F01-US02-T01
  title: Bulk send endpoint and job
  layer: api
  repo: api
  status: in_progress
  depends_on: [M01.S02.F01-US01-T01]
  build: When the account owner confirms a bulk send, the send endpoint shall queue one job per selected invoice.
  implements: [M01.S02.F01-US02-AC01, M01.S02.F01-US02-AC02]
  tests: [M01.S02.F01-US02-TC01, M01.S02.F01-US02-TC02]
  budget: {files: 4, lines: "+150 / -10"}
  subtasks:
    - id: M01.S02.F01-US02-T01-ST01
      title: Skip invoices without email
      status: backlog
```
## 6. Specification review
| Item | Result | Reviewer |
|---|---|---|
| Architecture and tech design (DEC-001) | OK | dev lead |
| Acceptance criteria and edge cases | OK | dev lead |
| Constraints (I-001-NFR01, Open, non-blocking) | OK | dev lead |
| Test design (05-qa@1.0.0) | OK | dev lead |
| Tasks, tests, budgets | OK | dev lead |
Sign-off: dev lead, 2026-10-08.
""")
w("decisions/DEC-001-background-jobs.md", """
pdlc_step: "DEC"
scope: DEC-001
doc_version: 1.0.0
status: approved
depends_on: []
change_requests: []
open_items: 0
blocking: []
updated: 2026-10-05
""", """
# DEC-001: Bulk work runs as background jobs
Owner: development. Context: I-001 sends up to 200 invoices (M01.S02.F01-FR01). Decision: a job queue. Consequences: progress is shown per invoice.
""")
tracker = """# tracker.yaml: the tracking data for this product. tracker.md is generated from it (python pdlc.py board).
product: Ledgerly (sample)
config:
  design_stage: true
  version_scheme: semver
  statuses:
    backlog: Backlog
    in_definition: In definition
    in_design: In design
    ready_for_dev: Ready for dev
    in_progress: In progress
    in_review: In review
    in_qa: In QA
    done: Done
    released: Released
    blocked: Blocked
    removed: Removed
initiatives:
  - id: I-001
    title: Bulk invoicing
    slug: bulk-invoicing
    status: in_progress
    scopes:
      - id: M01.S02
        na: {D02: "no data change"}
items:
  - {id: M01, type: module, title: Billing, status: released}
  - {id: M01.S01, type: sub-module, parent: M01, title: Invoices, status: released}
  - {id: M01.S01.F01, type: feature, parent: M01.S01, title: Create invoice, status: released}
  - {id: M01.S01.F02, type: feature, parent: M01.S01, title: Invoice list, status: released, initiative: [I-001]}
  - {id: M01.S02, type: sub-module, parent: M01, title: Bulk actions, status: in_progress, initiative: [I-001], source: product/I-001-bulk-invoicing/02-prd.md}
  - {id: M01.S02.F01, type: feature, parent: M01.S02, title: Bulk send, status: in_progress, initiative: [I-001], source: product/I-001-bulk-invoicing/02-prd.md}
  - id: M01.S02.F01-US01
    type: story
    parent: M01.S02.F01
    initiative: [I-001]
    scope: M01.S02
    title: Select draft invoices
    status: in_review
    depends_on: []
    dep_level: 0
    source: product/I-001-bulk-invoicing/04-stories/M01.S02-bulk-actions.md
  - id: M01.S02.F01-US02
    type: story
    parent: M01.S02.F01
    initiative: [I-001]
    scope: M01.S02
    title: Send selected invoices
    status: ready_for_dev
    depends_on: [M01.S02.F01-US01]
    dep_level: 1
    fix_version: v1.4.0
    source: product/I-001-bulk-invoicing/04-stories/M01.S02-bulk-actions.md
  - {id: TD-001, type: tech_debt, title: Invoice list query does a full scan, status: backlog, source: decisions/DEC-001-background-jobs.md}
queries:
  - id: Q-001
    question: Can a bulk send include invoices of several currencies?
    about: [M01.S02.F01-US02]
    raised_by: D01
    blocking: false
    status: answered
    answer: product/I-001-bulk-invoicing/02-prd.md@1.2.0
versions:
  - {id: v1.4.0, goal: Bulk send, status: planned}
change_requests: []
"""
with open(os.path.join(ROOT, "tracker.yaml"), "w") as f:
    f.write(tracker)
print("sample written to", ROOT)
