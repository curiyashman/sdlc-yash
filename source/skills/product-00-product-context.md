---
name: product-00-product-context
description: "Product team, step P00 of the PDLC skills (product-00 to 07 for the product team, design-00 to 03 for the design team, dev-00 to 07 for the development team). Records the actual product understanding every initiative builds on, in [docs path]/product/00-product-context.md: what the product is, users, roles and plans, the living product map (modules, sub-modules, features with stable IDs and their status), business rules and glossary, user-facing integrations, constraints and applicable compliance regimes, product approvers, and tracker conventions; creates the shared tracker.yaml and offers to install the lint script and CI check. On later runs it syncs the map with what has shipped. Use when a product team starts with the skills, documents an existing product, or asks 'set up product context', 'document our product', 'update the product map'. Questionnaire first, assumes nothing, one .md file."
---

# Product 00: Product Context

You are the product lead who writes down what the product actually is, so every initiative starts from the real product instead of from assumptions. Initiatives (new features or expansions of existing ones) are brainstormed against this file, and each initiative's PRD adds to or changes the product map here.

**Modes**
- **Setup**: no `product/00-product-context.md` yet. Run the questionnaire, then create it, create `tracker.yaml` if none exists, and offer to install the lint script and its CI check.
- **Sync**: after a release or an approved PRD. Mark released features Live, nodes added by approved PRDs as Planned (if the PRD step hasn't already), and removed nodes Removed, from `tracker.yaml` and the PRDs (MINOR bump).
- "Where are we", "what next", and status questions belong to `pdlc-next`; this skill doesn't answer them.
- **Update**: change a convention or a fact. If the change affects files already written (for example renamed statuses), list those files and update them only with the person's OK. A change to an approved requirement goes through product-05-change-request.

*Scope of Recommendation here:* conventions (status names, version scheme, tool mapping, docs path), offered as defaults on the confirm sheet, and a draft grouping of an existing product into modules, built from Observed material. Record them only once confirmed. Product facts in the map are Provided or Observed, never invented.

**Also writes:** `tracker.yaml` (created in Setup mode, with `config` and one item per map node); with permission, `<docs path>/.pdlc/pdlc.py` (a copy of this skill's `scripts/pdlc.py`) and the CI workflow from `references/ci-pdlc-lint.yml` in the repository that holds the docs.

{{CORE}}

## Questionnaire

**Step 1: Product basics**
1. Product name, and a short slug for file names.
2. What it is and who it is for, in a few lines; product category; platforms (web, iOS, Android, desktop, API, other).
3. Is it live, in development, or not built yet? (A product not built yet starts with an empty or seed map; its first initiative defines the core.)
4. Where does this product's documentation live (repository or other store, branch, folder), and which code repositories belong to it (name, link, what each holds)? I'll read the docs and the code (read-only) to learn the current implementation and draft the product map; everything read is Observed. Any material outside the docs location and code repositories (help center, designs, analytics) to read too?
5. Chain files go in `docs/pdlc/` in the docs location, or another folder? When product files are generated elsewhere (for example in a Claude project), who commits them to the docs folder?

**Step 2: Users, roles, plans**
6. Every user type and role, including admin, operator, and support roles: what each does and what each may do.
7. Markets, regions, and languages served.
8. Plans, tiers, or entitlements, and which features each includes (if access differs by plan).

**Step 3: Product map** (one module at a time)
9. The modules today (functional areas such as Billing, Onboarding, Reporting), or confirm a draft built from the material in question 4.
10. For each module: its sub-modules and features, each with a one-line description and a status (Live, In build, Planned, Retired).
11. Business rules and terms everyone must use the same way (glossary).
12. Integrations users see or rely on (payments, email, SSO, third-party apps).

**Step 4: Constraints and people**
13. Constraints every initiative must respect: privacy, data residency, accessibility target, localization, brand or legal rules. Which compliance regimes apply (for example personal data laws such as India's DPDP Act or the GDPR, card payments, payment regulators, tax invoicing)? Use `references/compliance.md` to ask the applicability questions; each applicable regime is recorded as Provided with its source, and every unverified point stays Open with "needs legal review".
14. Product team: who brainstorms, writes PRDs, designs UX, and writes stories; who approves PRDs, UX, stories (the handoff), and change requests; who answers development queries.
15. Where the design system lives (path or link), so UX can use its component names, or "none yet". Visual design and design tokens are handled separately per project.

**Step 5: Project management**
16. Tracker: the Markdown tracker in the docs location only, or also an external tool (Jira, Linear, other)? Import files are made only when asked for.
17. Status names for each role: backlog, in definition, in design (only with a design stage), ready for dev (the handoff), in progress, in review, in QA, done, released, blocked, removed. Default: those names as written.
18. Does the team use estimates (story points, hours, other) or none, and sprints or continuous flow? Only the team enters them; the skills never propose them.
19. Version scheme for releases (for example semantic versions), or something else?
20. If an external tool is used, how items map to it (for Jira, for example: Initiative to Epic, Feature to Component or Label, Story to Story, Task to Task, Sub-task to Sub-task, Query to Task with a label).

## Output: `product/00-product-context.md`

```markdown
(header: pdlc_step "P00", scope product)
# [Product]: Product context

## 1. Product card
| Field | Value | Label |
Name, slug, description, category, platforms, stage (live / in development / not built), docs location (repository or store, branch, folder), docs path, code repositories (name, link, what each holds), other material sources, who commits product files generated elsewhere.

## 2. Users, roles, and plans
| Role | What they do | What they may do | Plans or tiers | Label |
Markets, regions, languages. Plans and the features each includes.

## 3. Product map
| ID | Level | Name | Description | Status (Live / In build / Planned / Retired / Removed) | Roles | Initiatives | Label |
The living tree of the whole product. The Initiatives column lists every initiative that added or changed the node.

## 4. Business rules and glossary
| Rule or term | Meaning | Applies to (map IDs) | Label |

## 5. User-facing integrations
| Integration | What users do with it | Map IDs | Label |

## 6. Constraints and compliance
| Constraint | Applies to | Source | Label |
Applicable regimes: | Regime | Applies because | Source and date read | Legal contact | Label |

## 7. Product team and approvals
| Role | Person | Approves or answers |

## 8. Tracker conventions
| Convention | Value | Label |
Status names mapped to roles (also in `tracker.yaml` config), estimates, rhythm, version scheme, external tool and mapping, design stage on or off.

## 9. Design system
Location, or "none yet".

## 10. Initiatives index
| ID | Name | Type (new feature / expansion) | Touches (map IDs) | Status | Folder |

## 11. Open questions
## Change log
```

**`tracker.yaml` in Setup mode.** Create it with the layout in the conventions [Tracker data]: `product`, `config` (status names from question 17, version scheme, `design_stage` if already known), empty `initiatives`, `queries`, `versions`, `change_requests`, and `items` with one entry per module, sub-module, and feature in the product map (type, parent, title, status: Live nodes `released`, In build `in_progress`, Planned `backlog`, Retired `removed`). Then run `lint --fix` and `board`, which writes `tracker.md`.

## Tracker
Map nodes are items in `tracker.yaml`, so later initiatives can depend on existing features. In Sync mode, update their status to match the map. Next: product-01-feature-brainstorm for the first initiative, or product-02-prd when a written spec for it already exists.
