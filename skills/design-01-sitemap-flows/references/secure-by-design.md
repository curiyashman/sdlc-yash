# Secure by design (reference pack)

Security is part of every step, not a review at the end. This pack lists what each team adds to its own work so that the independent Security team (sec-00 to sec-05) finds a system built to be hard to attack, not one that needs repairs. These items are **requirements and questions**, not legal facts: obligations come from the product context (Provided) and cited sources (Reference). Anything the person has not decided is Open, and the always-explicit areas of the core contract (security and permissions, compliance, irreversible changes) are confirmed, never defaulted.

**Principles every team applies:** least privilege; deny by default; defense in depth; fail closed; minimize data (collect, keep, and show the least); trust nothing from outside a boundary; make the secure way the easy way; log what matters without logging secrets or personal data; assume breach and limit blast radius.

## Product (P00 to P07)
| Step | Adds |
|---|---|
| P00 | Data classes the product handles (public, internal, confidential, personal, sensitive personal, financial, health, children's); the countries, states, cities, and sectors it operates in or serves (these drive hyper-local obligations); regulated or high-risk features; who owns security and privacy decisions; the incident and breach contact |
| P01 | For each approach: who would abuse this feature and how (a one-line abuse idea), and the privacy impact on each role |
| P02 | One NFR per security or privacy obligation, in business terms: who may see or do what, which data is kept for how long, consent and lawful basis, audit trail, regional data constraints (residency), abuse and fraud limits. Roles and permissions as a matrix, with deny by default. Cite the data class of every entity named |
| P03 | Authentication, session, and recovery flows; permission-denied and expired-session states; destructive and irreversible actions confirmed; error messages that do not reveal whether an account or record exists; consent and data-rights screens |
| P04 | Abuse and misuse stories as edge cases (a user acting outside their role, replaying a request, guessing an ID, uploading something hostile, exhausting a limit) with Given/When/Then criteria; privacy criteria (consent withdrawn, deletion requested, export requested, minor detected) |
| P05 | Security and privacy impact of every change request, listed beside the other impacts |
| P06 | Security-related queries and findings tracked like any other item; no release scheduled past an open critical finding without a recorded owner decision |
| P07 | No security, privacy, or compliance claim in launch material that has not been verified and approved |

## Design (G00 to G04)
| Step | Adds |
|---|---|
| G00 | Privacy and security conventions: how sensitive data is masked, how consent and permission states look, who reviews them |
| G01 | Mark authentication steps, trust boundaries, and role-restricted screens on the charts |
| G02 | Frames for permission denied, session expired, locked or throttled, step-up authentication, masked data, consent and withdrawal, and destructive confirmation; copy that does not leak existence or internals; no secrets or personal data in sample data |
| G03 | Review these states, plus accessible authentication (WCAG 2.2 criterion 3.3.8) and consent controls |
| G04 | Secure patterns in the system: password, one-time code, and recovery fields; consent controls; masked-value display and reveal; session timeout dialogs; patterns against clickjacking and look-alike prompts; sensitive fields excluded from autofill and screenshots where required |

## Development (D00 to D07)
| Step | Adds |
|---|---|
| D00 | Secure development setup: protected branches, required reviews, signed commits where used, multi-factor authentication for every account, secret scanning, dependency and static-analysis scanning in the pipeline, least-privilege credentials for agents and the sandbox, no production secrets in development |
| D01 | Security architecture in L4 (identity), L8 (security), L12 (logs), and L13 (recovery): authentication and authorization model, tenant isolation, cryptography and key management, secrets handling, input and output handling, rate and cost limits, supply-chain controls, data residency. The threat model (STRIDE for security, LINDDUN for privacy) in `threat-model.md` |
| D02 | Data classification per column, encryption at rest for confidential and sensitive columns, personal data minimization, retention and deletion mechanism (including backups and logs), row-level access where tenants share tables, audit tables, safe migrations |
| D03 | Each task carries its security build rules: validate input at the boundary, parameterized queries only, authorization check on every object access, encode output, no secrets or personal data in logs, safe error handling, upload limits and scanning, outbound request allow-lists |
| D04 | The coding agent follows the secure coding rules of the task, never adds a dependency without recording it for review, never disables a security control to make a test pass, and never writes secrets, tokens, or personal data into code, tests, or logs |
| D05 | Developer-level tests for every threat mitigation (TH) and abuse edge case: authorization on every role and object, validation limits, error handling, rate limits |
| D07 | Dependency, runtime, and base-image upgrades and vulnerability fixes as maintenance items with an owner and a reason |

## QA (Q00 to Q04)
| Step | Adds |
|---|---|
| Q00 | Functional security/privacy checks in strategy (roles, consent, session); explicit boundary: no penetration testing |
| Q01 | TCs for abuse ECs, permission matrix, privacy flows, session expiry; negative cases with expected results from stories |
| Q02 | Execute those cases; file defects with severity; never mark pass on flaky auth checks |
| Q03 | Release Go blocked by open critical auth/privacy defects unless named risk acceptance |
| Q04 | Abuse-oriented load (credential stuffing simulations only in authorized QA envs per methodology) stays out — leave attacks to Security |

Functional checks that the security and privacy acceptance criteria hold (roles, consent, deletion, export, session behavior) and accessibility of authentication. QA does not perform penetration testing; the Security team does.

## Deployment (O00 to O05)
| Step | Adds |
|---|---|
| O00 | Who may deploy, approve, and access each environment; separation of duties for production |
| O01 | Network segmentation, private data stores, no public admin consoles or databases, least-privilege identities, secrets in a secrets manager, encryption in transit and at rest, baseline hardening, audit logging on |
| O02 | Pipeline security: pinned and verified dependencies and actions, build in an isolated runner, signed artifacts and provenance where the platform supports it, a software bill of materials, scanning gates, no long-lived credentials |
| O03 | Release checks for secrets and configuration, a security sign-off gate before production where the product has a Security stage, and a rollback that restores a safe state |
| O04 | Security-relevant logging and alerts (failed logins, privilege changes, unusual data access), retention that meets obligations, log access control |
| O05 | Incident handling for security events: containment, evidence preservation, notification duties and deadlines taken from the product context, and a post-incident review |

## Security (S00 to S05)
The Security team works from this pack's opposite side: it assumes nothing was done well, and tests the result.
