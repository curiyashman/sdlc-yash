# Compliance checklists (reference pack)

These are **questions to answer and verify**, not legal facts. Laws, rules, thresholds, and dates change and depend on the jurisdiction. Handle every item like this:
- **Applicability:** whether a regime applies is Provided (the person or their counsel says so) or Open.
- **Requirements:** each requirement taken from a regime is a **Reference** that cites the official source and the date you read it.
- **Unverified items:** an item nobody has verified stays Open and is marked "needs legal review". It is never filled in from memory.
- **Not legal advice:** this pack does not replace legal advice. It makes sure the right questions reach the right person before anything is built.

## Where the answers land
| Step | What it records |
|---|---|
| product-00 | Which regimes apply to the product, the markets and user types, the legal or compliance contact, and their approval rule (section Constraints) |
| product-02 | One NFR per applicable obligation, in business terms (`I-<nnn>-NFR<nn>`): who may see what, how long data is kept, what users can ask for |
| product-04 | Edge cases the obligations create (consent withdrawn, deletion requested, minor detected, data export requested, breach notice shown), each with an acceptance criterion |
| dev-01 | The threat model (`threat-model.md`), and the decisions in L4 Auth, L8 Security, L12 Logs, and L13 Recovery that meet each NFR, citing the NFR ID |
| dev-05 | Test cases for each obligation's acceptance criteria and NFRs |
| dev-06 | Runbooks the obligations need (breach response, data subject request handling, key rotation) |
| decisions/ | Every interpretation of a rule ("we treat X as not personal data because...") as a DEC with its source |

## 1. Personal data (any jurisdiction)
1. What personal data does the product collect, from whom (customers, their end users, employees), and for which purpose each?
2. On what basis is each kind processed (consent, contract, legal obligation, other), and is that basis recorded per user?
3. How is notice given before collection, and in which languages?
4. Can users see, correct, export, and delete their data? Through which screens or requests, and within what time?
5. How long is each kind kept, and what deletes or anonymizes it afterwards (including backups and logs)?
6. Does any data belong to children or other protected groups? How are they identified and handled?
7. Which vendors (processors) receive personal data, under which agreements, and in which countries?
8. Is personal data transferred outside the country where it was collected? Under which mechanism?
9. Who is told of a personal data breach, within what time, and by whom?
10. Do logs, analytics events, error reports, or AI prompts contain personal data? Can they avoid it?

## 2. India: Digital Personal Data Protection Act, 2023 and the rules made under it
Official sources: the Ministry of Electronics and Information Technology (MeitY) and the Gazette of India. Check which provisions and rules are in force, and from which dates, before relying on any item.
1. Does the product process digital personal data of individuals in India, or offer goods or services to them from outside India?
2. Is the business a Data Fiduciary for this data, a Data Processor for a customer, or both (per data set)?
3. Notice and consent: do the notice's contents, languages, and consent request meet the Act and the current rules? Is withdrawing consent as easy as giving it? Is a Consent Manager used?
4. Children (as the Act defines them) and persons with disabilities who have a lawful guardian: how is verifiable consent of the parent or guardian obtained? What processing is restricted for them (for example tracking, behavioral monitoring, targeted advertising)?
5. Rights of Data Principals (access, correction, completion, erasure, grievance redressal, nomination): through which channel, and within the time the rules set?
6. Grievance officer or contact published, and response times as the rules set?
7. Personal data breach: intimation to the Data Protection Board and to affected Data Principals in the form and time the rules set. Who does it?
8. Retention: is data erased once its purpose is served or consent is withdrawn, with any minimum retention the rules require?
9. Could the business be notified as a Significant Data Fiduciary (data protection officer, independent audit, impact assessment)?
10. Cross-border transfer: any country restrictions notified by the government that affect where data or vendors sit?
11. Sector rules that apply on top (for example from RBI, SEBI, IRDAI, or for health data).

## 3. European Union and United Kingdom: GDPR and UK GDPR
Official sources: EUR-Lex for the GDPR text, the national supervisory authority and the EDPB for guidance, and the ICO for the UK.
1. Is the business established in the EU or UK, or does it offer goods or services to, or monitor, people there?
2. Lawful basis per purpose, and a record of processing activities.
3. Is a data protection impact assessment needed for this initiative?
4. Data processing agreements with processors; transfer mechanism for data leaving the EU or UK.
5. Rights requests (access, rectification, erasure, portability, objection) and the response time.
6. Breach notification to the supervisory authority and to individuals within the time the regulation sets.
7. Cookie and tracking consent under the ePrivacy rules of each market.

## 4. Card payments: PCI DSS
Official source: the PCI Security Standards Council (current PCI DSS version and self-assessment questionnaires).
1. Does card data ever touch the product's servers, browser code it controls, or logs? Can a provider's hosted fields, redirects, or tokens keep it out?
2. Which self-assessment questionnaire or assessment level applies, given that design?
3. Is any sensitive authentication data (for example the card security code) stored anywhere? (It must not be stored after authorization; verify against the current standard.)
4. Which scripts run on payment pages, and how are they authorized and monitored?

## 5. India: payments (Reserve Bank of India)
Official source: RBI circulars and master directions (rbi.org.in). Verify the current circular for each item.
1. Is the business a merchant using a licensed payment aggregator or gateway, or does it need its own authorization?
2. Card-on-file: does the product store any card data, or only tokens issued under RBI's card-on-file tokenization framework?
3. Recurring payments and e-mandates: which additional factor of authentication, pre-debit notifications, and limits apply?
4. Payment system data storage: does any payment data leave India, and if so, under what conditions?
5. Refunds, failed transactions, and dispute timelines that the rules or the provider require.
6. UPI-specific rules from NPCI if UPI is offered.

## 6. India: GST invoicing
Official sources: CBIC and the GST Council notifications, and the GSTN and Invoice Registration Portal documentation.
1. Which documents does the product issue (tax invoice, bill of supply, credit or debit note, receipt voucher)? Do their fields match the current rules (GSTIN, HSN or SAC, place of supply, tax breakup)?
2. Does e-invoicing apply, given the turnover threshold in force? If so, how are IRN and QR code obtained and shown?
3. GSTIN validation of customers; B2B versus B2C handling; reverse charge cases.
4. How long invoices and records must be kept, and in what form.
5. Rounding, currency, and export (zero-rated) invoice rules relevant to the product.

## 7. Communications and marketing
1. Email: consent and unsubscribe rules in each market (for example CAN-SPAM in the US, ePrivacy in the EU).
2. India: commercial SMS and calls under TRAI's TCCCPR. Are DLT registration of headers and templates, and consent records, in place?
3. WhatsApp and other platforms: the platform's own business messaging policies.

## 8. Accessibility
1. Which target does the product commit to (for example WCAG 2.2 AA)?
2. Do public-sector or other customer contracts require a standard (for example India's GIGW for government products, EN 301 549 in EU procurement, Section 508 in US federal procurement)?

## 9. Records, audit, and security baselines
1. Which audit logs must exist (who did what, when), for how long, and who may read them?
2. Do customers require certifications or reports (for example ISO/IEC 27001 or SOC 2)? Which controls does that put on the build?
3. Data residency commitments in contracts.
