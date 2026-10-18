# Jurisdictions, local law, and compliance (reference pack for sec-00 and sec-03)

Laws differ by country, state, city, and sector, change often, and sometimes apply to a product because of where its **users** are, not where the company is. This pack is a **research protocol and question list**, not legal advice and not a list of facts. Every legal requirement in a report is a **Reference** that cites the official source, the version, and the date read. An obligation nobody has verified is **Open** and marked "needs legal review". Applicability is Provided by the person or their counsel, or Open.

## 1. Scope questions (sec-00 asks these; none is defaulted)
1. In which countries, states or provinces, and cities do the company, its servers, its staff, its vendors, and its users operate? Where is data stored and processed, and where does it move?
2. Which sectors does the product touch (finance, health, education, children, government, telecom, insurance, critical infrastructure, e-commerce, employment)?
3. Which data classes are processed (personal, sensitive personal, financial, health, biometric, children's, location, government identifiers)?
4. Which contractual or certification obligations exist (customer security questionnaires, SOC 2, ISO/IEC 27001, PCI DSS, HIPAA business associate agreements, government cloud rules)?
5. Who is the legal contact, the data protection officer or equivalent, and who may accept risk?

## 2. Regimes to check, by family (examples to verify, not a complete or current list)
- **Cross-region privacy:** EU General Data Protection Regulation and member-state laws; UK GDPR and Data Protection Act 2018; Swiss FADP.
- **India:** Digital Personal Data Protection Act, 2023 and the rules under it (verify which provisions are in force); Information Technology Act, 2000 and rules; CERT-In directions (incident reporting and log retention); sector regulators (for example RBI, SEBI, IRDAI, health data rules) including data-localization expectations.
- **United States:** state privacy laws (California CCPA/CPRA and the growing set of other states), sector laws (HIPAA, GLBA, FERPA), COPPA for children, state breach-notification laws, FTC rules, and state biometric laws.
- **Other Asia-Pacific:** Singapore PDPA, Japan APPI, South Korea PIPA, Australia Privacy Act, China PIPL with the Data Security Law and Cybersecurity Law (including cross-border transfer rules), Thailand PDPA, Indonesia PDP Law, Vietnam data laws, Malaysia PDPA, New Zealand Privacy Act.
- **Middle East and Africa:** Saudi Arabia PDPL, UAE federal PDPL and free-zone regimes, Turkey KVKK, South Africa POPIA, Nigeria NDPA, Kenya Data Protection Act, Egypt data protection law.
- **Americas other:** Canada PIPEDA and provincial laws, Brazil LGPD, Mexico, Argentina, Colombia, Chile.
- **Europe other:** Russia data-localization law, Ukraine, and others by country.
- **Sector and security frameworks:** PCI DSS, EU NIS2 and DORA, EU Cyber Resilience Act and AI Act where relevant, ISO/IEC 27001 and 27701, SOC 2, NIST frameworks, government cloud schemes.
- **Accessibility and consumer law** where the product is public: for example EU accessibility legislation, Section 508, local equivalents (these overlap with design obligations).
- **Hyper-local rules:** city, state, or sector rules and regulator circulars that apply to one place (for example local data-residency requirements, local-language notice requirements, retention periods, local reporting windows, mandatory registration with an authority). Search for the regulator in each place the product operates, not only national law.

## 3. Research protocol (for each place and sector in scope)
1. Identify the regulator and the official publication (government gazette, regulator website, official text). Prefer primary sources.
2. Read the current text and the status: in force, partially in force, amended, or pending, and the commencement dates. Record the date you read it.
3. Extract the obligations that touch software and operations: lawful basis and consent, notice and language, user rights and response times, children, retention and deletion, cross-border transfer, localization, security measures, breach notification (who, how fast), record-keeping, registration, appointment of local officers, penalties.
4. Map each obligation to the system: where the data is, which control meets it, what evidence shows it. Gaps are findings.
5. Where sources conflict or are unclear, say so, keep the item Open, and send it to legal review. Do not interpret ambiguity in the product's favor.
6. Keep the list of regimes as a living table: regime, place, applicability (Provided or Open), source and date, obligations found, status.

## 4. Privacy audit questions against the real system (sec-03)
1. Which personal data does the system actually collect and store, field by field (read from schemas, forms, API payloads, logs, analytics, backups, and third-party calls)? Compare with what the product claims to collect.
2. For each data class: lawful basis or consent record, purpose, retention, deletion mechanism (including backups, logs, search indexes, analytics, and processors), access roles, and encryption.
3. Do consent, withdrawal, access, correction, export, and deletion actually work end to end in the running system? In the response time the local rule sets?
4. Cross-border and cross-region flows: where each store and each processor is, and the mechanism that allows the transfer.
5. Children and other protected groups: detection, parental consent, and restricted processing.
6. Third parties: which receive data, under which agreements, with which data.
7. Breach readiness: detection, decision, and notification path to each regulator and to users within the local deadlines; evidence of a test.
8. Data-subject and regulator-facing records: processing register, data protection impact assessments where required, retention schedule, audit logs.
9. Security measures required by law as written (encryption, access control, logging, incident response) mapped to the technical findings.
10. Dark patterns, tracking before consent, cookie and SDK behavior in web and mobile clients.
