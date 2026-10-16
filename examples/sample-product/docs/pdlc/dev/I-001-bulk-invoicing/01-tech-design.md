---
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
---
# Tech design: I-001
Bulk send runs as a background job per DEC-001. Threat model: sending to wrong customer (M01.S02.F01-BR01 enforced server side).

## Change log
| Version | Date | Change | CR / query / DEC |
|---|---|---|---|
| 1.0.0 | 2026-10-01 | Created | |
