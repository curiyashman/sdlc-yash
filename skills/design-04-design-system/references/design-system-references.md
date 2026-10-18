# Design system references (reference pack)

Used by `design-04-design-system`. Everything here is **Reference**: re-verify the version and URL at run time and record the date in section 10 of the output. Study these for principles, structure, and accessibility practice. Never copy another system's visual identity, icons, illustrations, or source; check the license of anything you adopt.

## Research protocol
1. State the decision the research serves (for example "token naming for themes", "form error pattern").
2. Prefer official documentation and specifications over blogs and summaries.
3. Compare at least two approaches when the trade-off matters, and say what you took (a principle) and what you left.
4. Check license and maintenance status of any library before proposing it (last release, open security issues, license).
5. Record URL, version, and date verified. When there is no web access, mark each unverified point Open.
6. Research only what the decisions need. A long reading list is not a result.

## Design system references (study for structure and principles)
| Source | Study it for |
|---|---|
| Material Design 3 (m3.material.io) | Color roles, tonal palettes, adaptive layout, motion, state layers |
| IBM Carbon (carbondesignsystem.com) | Enterprise data-dense UI, tokens and themes, data visualization, accessibility docs |
| Ant Design (ant.design) | Admin and workflow components, forms, tables |
| Atlassian Design System (atlassian.design) | Tokens, spacing, content design, product-suite consistency |
| Shopify Polaris (polaris.shopify.com) | Commerce and admin patterns, content guidelines |
| GitHub Primer (primer.style) | Developer tooling, tokens, accessibility process |
| Adobe Spectrum (spectrum.adobe.com) | Cross-platform design, internationalization, density |
| GOV.UK Design System (design-system.service.gov.uk) | Plain-language forms, error patterns, evidence-based components |
| US Web Design System (designsystem.digital.gov) | Public-sector accessibility and compliance practice |

## Standards and implementation guidance
| Source | Use |
|---|---|
| WCAG 2.2 (w3.org/TR/WCAG22) | The practical normative target. WCAG 3.0 is a Working Draft (as of 2026-10); do not target it |
| WAI-ARIA Authoring Practices (w3.org/WAI/ARIA/apg) | Keyboard and role patterns, where native HTML does not give the behavior |
| Design Tokens Format Module 2025.10 (designtokens.org; first stable version, 2025-10-28) | Token file format. It is a W3C Community Group Final Report, not a W3C Recommendation: say so |
| Style Dictionary (styledictionary.com) | Token transforms, one option among others |
| Storybook (storybook.js.org) | Component documentation, interaction and accessibility testing, one option |
| Playwright (playwright.dev) | Browser tests, visual comparison, accessibility scans with a rules engine |
| Figma (help.figma.com) | Variables, modes, components, Dev Mode, when Figma is the medium |

## WCAG 2.2 AA criteria that usually shape components (verify wording and level at run time)
| SC | Name | Typical component impact |
|---|---|---|
| 1.4.3 | Contrast (Minimum) | Text and text-on-surface token pairs |
| 1.4.11 | Non-text Contrast | Input borders, focus indicators, icons that carry meaning |
| 1.4.4, 1.4.10 | Resize Text, Reflow | Layouts that survive zoom and narrow widths |
| 2.4.7 | Focus Visible | Focus style on every interactive component |
| 2.4.11 | Focus Not Obscured (Minimum) | Sticky headers, drawers, and toasts over focused items |
| 2.5.7 | Dragging Movements | A non-drag alternative for sorting, sliders, and drag and drop |
| 2.5.8 | Target Size (Minimum), 24 by 24 CSS px | Icon buttons, dense tables, chips |
| 3.3.1 to 3.3.4 | Errors and labels | Form field, error summary, confirmation for consequential actions |
| 3.3.7, 3.3.8 | Redundant Entry, Accessible Authentication (Minimum) | Forms, sign-in, verification |
| 4.1.3 | Status Messages | Toasts, async results, streaming updates |

Reduced motion (`prefers-reduced-motion`) and color-scheme handling are good practice, not AA criteria: write them as product requirements when the team confirms them.

## Compliance regimes (Provided by the product context, never defaulted)
WCAG 2.2 AA, EN 301 549 (EU), Section 508 (US), GIGW (India), ADA-related contractual terms, and sector rules. Use `compliance.md` section 8 for the questions. A matrix row records required evidence, not a verdict. Anything not confirmed is Open: "needs legal review".

## Token naming starter (adapt to the product; do not adopt blindly)
- Primitive: `color.blue.600`, `space.4`, `font.size.300` (what the value is)
- Semantic: `color.text.default`, `color.surface.raised`, `color.border.focus`, `space.stack.md` (what it is for)
- Component: `button.primary.background` (only where a decision is specific to that component)
- Themes change the semantic-to-primitive mapping, never the component code.
