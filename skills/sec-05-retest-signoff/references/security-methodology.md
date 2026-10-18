# Security assessment methodology (reference pack for sec-01 to sec-05)

The Security team works as an independent, adversarial reviewer: it assumes the system is vulnerable until it has shown otherwise, and it looks at the product the way an attacker, a malicious insider, a careless user, and a regulator would. Everything here is **methodology and checks**. Standards and tool names are Reference: verify the current version and record the date.

## 1. Rules of engagement (hard limits; confirmed in sec-00 before anything runs)
1. **Authorization first.** Test only systems, accounts, and environments the person confirms they own or are authorized to test, in writing, with the dates, targets, and any third-party terms (cloud provider and vendor testing policies). No scope, no testing.
2. **Environment.** Staging or a production-like copy with test data by default. Production only with explicit written approval, a window, and a stop contact. Never against third-party systems, shared infrastructure, or real users' data.
3. **Non-destructive.** Confirm that a weakness exists with the smallest proof (reading a harmless record you own, showing a response difference, showing a header). Stop at proof of access. No data exfiltration, no persistence, no denial-of-service or load attacks, no destructive payloads, no account takeover of real users, no social engineering or physical testing unless the engagement says so in writing.
4. **No weapons.** The team writes findings, safe verification steps, and fixes. It does not write or deliver working exploits, malware, or tooling meant to attack other systems. Where a standard scanner or a benign probe confirms an issue, that is the evidence.
5. **Evidence handling.** Evidence (requests, responses, screenshots, hashes) is stored with secrets and personal data redacted. Any real secret or personal data found is reported by location and type, never copied into the report, and handled as an incident if live.
6. **Stop conditions.** Stop and tell the contact if testing causes instability, if real personal data is exposed, if a critical issue is live in production, or if scope is unclear.
7. **Fresh eyes.** The team reads the code, configuration, and running system, and does not read the product, design, development, QA, or deployment documents or earlier threat models. It forms its own view of what the system does and what matters from what it finds, and from the scope sheet only.

## 2. Standards to apply (select by what the system is)
| Area | Reference |
|---|---|
| Web applications | OWASP Top 10, OWASP Application Security Verification Standard (ASVS), OWASP Web Security Testing Guide (WSTG) |
| APIs | OWASP API Security Top 10 |
| Mobile (iOS, Android) | OWASP MASVS and MASTG |
| LLM and AI features | OWASP Top 10 for LLM Applications; MITRE ATLAS |
| Weakness classes | MITRE CWE (Top 25), MITRE ATT&CK for attacker behavior |
| Secure development | NIST Secure Software Development Framework (SP 800-218); software supply chain: SLSA, SBOM (CycloneDX or SPDX) |
| Cloud and infrastructure | CIS Benchmarks; cloud provider security best practices and well-architected security pillars |
| Identity | NIST SP 800-63 (digital identity) |
| Threat modeling | STRIDE (security), LINDDUN (privacy) |
| Severity | CVSS (current version) with exploitability context (EPSS, known-exploited lists) and business impact |

## 3. Attack surface (sec-01)
Enumerate from the code and the running system, not from documentation:
- Entry points: web routes, API endpoints (including undocumented ones found in code), webhooks, file uploads, message queues, scheduled jobs, admin and back-office consoles, mobile app components and deep links, command-line tools, third-party callbacks.
- Identities and roles: how users, services, and administrators authenticate; the roles the code actually enforces.
- Data: stores (databases, caches, object storage, search indexes), what they hold (classify), where data flows, and which third parties receive it.
- Trust boundaries and secrets: where input crosses a boundary; where secrets, keys, and tokens live.
- Infrastructure: hosts, containers, networks, cloud accounts and roles, DNS and certificates, CI/CD, package registries, the software supply chain.
Then, as an attacker: the most valuable assets, the cheapest paths to them, and the abuse cases (account takeover, privilege escalation, tenant crossing, fraud, data scraping, cost abuse, ransomware-style impact).

## 4. Checks by domain (sec-02). Test what applies; record what was not tested.
1. **Authentication:** credential storage and policy, brute-force and credential-stuffing resistance, multi-factor and recovery abuse, session and token lifecycle (entropy, expiry, rotation, revocation, binding), single sign-on and OAuth/OIDC flows (redirect URIs, state, PKCE), default and shared accounts.
2. **Authorization:** object-level and function-level checks on every endpoint (test with two accounts of the same and different roles and tenants), mass assignment, privilege escalation, forced browsing, horizontal and vertical separation, admin function exposure.
3. **Input handling:** injection classes (SQL, NoSQL, OS command, LDAP, template, expression, header), cross-site scripting and output encoding, request forgery (CSRF, SSRF), insecure deserialization, XML external entities, path traversal, open redirects, file upload handling, regular-expression denial of service.
4. **Business logic:** workflow bypass, race conditions, replay, price or quantity tampering, coupon and referral abuse, limit bypass, inconsistent state transitions.
5. **Data protection:** encryption in transit (protocols, ciphers, certificates, HSTS) and at rest, key management, sensitive data in URLs, logs, caches, backups, analytics, error pages, and client storage; data minimization and masking; secure deletion.
6. **Configuration and platform:** security headers, CORS, cookie flags, error handling and debug modes, default credentials, exposed admin consoles, directory listing, verbose banners, unnecessary services and ports, outdated runtimes.
7. **Dependencies and supply chain:** known vulnerabilities in direct and transitive packages, abandoned or typosquatted packages, license risk, lockfile integrity, build and release pipeline tampering, unpinned actions or images, secrets in repositories and history.
8. **Secrets:** hardcoded keys and tokens in code, history, images, configuration, client bundles, and logs.
9. **Cloud and infrastructure:** public storage and databases, over-permissive roles and policies, network exposure and segmentation, metadata service access, container and cluster hardening, infrastructure-as-code misconfigurations, logging and monitoring gaps, backup exposure.
10. **Database and consoles:** access paths, accounts and grants, row-level isolation, query logging of sensitive data, administrative interfaces, management consoles.
11. **Mobile and client:** insecure storage, certificate pinning where required, exported components, deep link abuse, tamper and debug detection as the risk requires, secrets in the bundle.
12. **AI and automation features:** prompt injection and data exfiltration through tools, over-privileged agents, unsafe output handling, training or logging of personal data, cost abuse.
13. **Availability and abuse:** missing rate and cost limits, expensive endpoints, resource exhaustion paths (reported by analysis, not by attack), lack of monitoring and alerting for the attacks above.
14. **Observability for defenders:** whether attacks above would be seen and alerted on, and whether logs are protected from tampering.
Methods: static review of code and configuration; dependency, secret, container, and infrastructure scanners; dynamic testing of the running system within the rules in section 1; manual verification of every scanner result before it becomes a finding.

## 5. Findings
Each finding has an ID `SF-<nnn>` (`pdlc.py new-id sf`) and: title; affected component and location; domain and CWE; description; how an attacker would use it (attack path, in prose); evidence (redacted); severity (Critical, High, Medium, Low, Informational) with CVSS vector, exploitability context, and the business and regulatory impact; confidence (Confirmed, Likely, Possible); recommended fix with the secure pattern (a concrete design or code-level description, not an exploit); how to verify the fix; owner and a suggested order. Findings are labeled Observed (seen in code or system) or Reference (from a cited source). A scanner hit not verified is "Possible" and says so.

Severity guide: **Critical** is a direct path to full compromise or mass data exposure with little effort; **High** is serious compromise of a role, tenant, or data class; **Medium** needs preconditions or has limited impact; **Low** is hardening; **Informational** has no direct risk. Final severity is the team's Recommendation with reasoning; risk acceptance belongs to the named business owner and is recorded as a DEC.

## 6. Remediation
For each finding: the root cause, the fix at the right layer (design change, code pattern, configuration, platform control), a compensating control if the fix is not immediate, regression test ideas, and a verification step for the retest. Group by root cause so one fix closes many findings. Order by risk reduction and dependency, never by a calendar the team has not set.
