# Threat model (reference pack for dev-01)

Use this pack for the product-wide architecture (baseline) and for every initiative's tech design. Also use it when a change touches authentication, permissions, personal data, payments, file upload, or other external input. The threat model is part of the tech design file (section "Threat model"), not a separate file.

## Method
1. **Assets:** what an attacker would want, for example personal data, money movement, credentials, tenant data, admin actions, and availability. Cite the PRD IDs (FR, BR, NFR) that make each asset matter.
2. **Actors and trust boundaries:** anonymous user, signed-in user per role, tenant admin, internal staff, integrations and webhooks, background jobs, third-party services. Mark every place data crosses a boundary.
3. **Data flows:** list each flow that crosses a boundary as `DF01` through `DFnn` in this file. Give its source, destination, data, and transport.
4. **Threats per flow (STRIDE):**

   | Letter | Threat | Question |
   |---|---|---|
   | S | Spoofing | Can someone act as another user or service? |
   | T | Tampering | Can data or requests be changed in transit or at rest? |
   | R | Repudiation | Can an action be denied for lack of evidence? |
   | I | Information disclosure | Can data leak to the wrong role, tenant, log, or vendor? |
   | D | Denial of service | Can the flow be exhausted, or abused for cost? |
   | E | Elevation of privilege | Can a role reach actions above its level? |

5. **Rate each threat** with the team's scale (for example likelihood and impact as low, medium, or high). Ratings are Provided by the team or Recommendations with stated reasoning, never invented facts.
6. **Mitigations:** for each threat, the decision that addresses it (an L4, L8, L9, L10, L12, or L13 decision, or a DEC). Each mitigation becomes a requirement for dev-03 tasks and a test case in dev-05. A threat accepted without mitigation needs a DEC with its owner and reason.

## Table in the tech design
| TH ID | Flow | STRIDE | Threat | Rating | Mitigation (layer decision, DEC) | Task / test | Label |
|---|---|---|---|---|---|---|---|

TH IDs are local to the tech design file (`TH01` and onwards). Tasks cite them with the file, for example "tech design TH03".

## Checklist of common items to ask about (not to assume)
- Tenant isolation on every query and file path; object-level authorization on every ID taken from a request.
- Input validation and output encoding; file upload type, size, and scanning; server-side request forgery on any URL the product fetches.
- Secrets handling and rotation; least-privilege service credentials; audit logs for admin actions.
- Rate limits and cost limits on expensive or abusable endpoints (including AI calls).
- Webhook signature verification and replay protection.
- Session handling, multi-factor options, account recovery abuse.
- Personal data in logs, analytics, error reports, and AI prompts.
- Backup encryption and restore tests; incident and breach runbooks.
