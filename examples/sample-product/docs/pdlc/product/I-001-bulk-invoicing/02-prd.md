---
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
---
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

## Change log
| Version | Date | Change | CR / query / DEC |
|---|---|---|---|
| 1.0.0 | 2026-10-01 | Created | |
