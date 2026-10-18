# Platforms and responsive design (reference pack)

Used by every Design step. Nothing here is a default for a product: platforms, breakpoints, and native-versus-shared choices come from the product context and the G00 *Platform and responsive profile*. Where a number below is a Reference, re-verify it at run time and record the date.

## 1. The platform and responsive profile (owned by G00, cited by G01 to G04 and by development)
One table in `design/00-design-setup.md` section 4. Rows only for platforms the product needs (Provided by the product context, or Open).

| Platform | In scope? / order | Approach | Size classes or breakpoints | Orientation | Input modes | Native conventions followed | Min OS / browser | Source and label |
|---|---|---|---|---|---|---|---|---|
| Web (desktop, tablet, phone browsers) | | responsive web / PWA | | | pointer, touch, keyboard | | | |
| iOS (iPhone, iPad) | | native / cross-platform | | | touch, keyboard, pointer on iPad | Apple Human Interface Guidelines | | |
| Android (phone, tablet, foldable) | | native / cross-platform | | | touch, keyboard, stylus | Material Design / Android guidance | | |

*No platform is assumed.* Web only, app only (iOS, Android, or both), and mixed products are all valid. When the product says web first, design web first and record the other platforms as `later` rows, so the tokens and components are built to extend to them without rework; when it is app only, there are no web rows and no web breakpoints. A platform that moves from `later` to in scope is a change handled through the profile (update mode), not a redesign.

*Approach options:* one responsive web app; separate native apps; one cross-platform codebase with shared design and platform-specific behavior; a mix. State which, as Provided or Default. The choice drives how many component variants exist.

## 2. Breakpoints and size classes
- Derive breakpoints from the product's content and layouts, not from a device list. Start from where the product's real screens break (table columns, navigation, forms, dashboards), then name the breakpoints. Record the reason for each.
- Web: define a small set of named breakpoints (commonly 4 to 6) with the minimum width, the column grid, the gutter and margin, and the content max width. Use min-width, mobile-first logic. Text and layouts must also survive 200 percent zoom and 320 CSS px reflow (WCAG 1.4.4 and 1.4.10).
- iOS: design in size classes (compact and regular width and height), not in device sizes; honor safe areas, Dynamic Island and home indicator, and iPad multitasking widths.
- Android: use window size classes (compact, medium, expanded) and adaptive layouts; honor insets, edge-to-edge, the system back, and foldable postures if required.
- Orientation: say which orientations are supported per platform. Locking an orientation is a decision with a reason.

## 3. What adapts at each size (decide per pattern, then per screen)
| Concern | Questions |
|---|---|
| Navigation | Which pattern at each size (top bar, side rail, drawer, tab bar, bottom bar)? What is always reachable? |
| Layout | Columns, reflow order, what stacks, what hides (and where hidden content moves; never silently drop information) |
| Data views | Table to card list, column priority, horizontal scroll as a last resort, sticky headers |
| Forms | Single column on small sizes, field grouping, keyboard type per field, autofill, inline versus summary errors |
| Overlays | Modal, sheet, popover, full screen: which at each size; dismiss gestures; focus return |
| Density and targets | Density per size and input mode; target sizes (WCAG 2.5.8 minimum 24 CSS px; larger recommended for touch, and the platform guidelines for iOS and Android: re-verify the current values) |
| Media and charts | Aspect ratios, simplified charts, alternatives to hover |
| Text | Type scale per size, line length, text expansion, Dynamic Type (iOS) and font scaling (Android and web) |
| Input | Hover has an equivalent on touch; gestures have a visible alternative; keyboard and switch access everywhere |
| States | Offline, slow network, interrupted flows, background and resume on mobile |

## 4. Platform conventions (follow them unless the product has a reason not to)
- Back, share, selection, permission prompts, notifications, pull to refresh, and haptics behave as the platform's users expect. A deviation is a Recommendation with a reason.
- Shared design, platform-specific behavior: the same tokens and semantic components, mapped to native controls where users expect them (pickers, sheets, switches, system dialogs).
- Never ship iOS patterns on Android or the reverse by default; record where the product deliberately unifies them.

## 5. What each Design step must do
| Step | Responsibility |
|---|---|
| G00 | Capture and confirm the profile (section 1). Everything else cites it |
| G01 | Screen design list shows each screen's platforms and the navigation pattern per size class; charts note where the flow differs by platform |
| G02 | One frame per screen, state, and platform or size class that the profile requires; a layout adaptation note per screen (what reflows, collapses, or changes pattern) |
| G03 | Reviews every required platform and size class, the adaptation notes, native-convention deviations, targets, zoom and reflow, orientation |
| G04 | Tokens (type scale, spacing, grid, density) and every component spec carry the platform and responsive behavior; the test matrix covers the profile |

## 6. Test matrix (G04 and development)
Rows: browser engines and versions, OS versions, size classes, orientation, input modes (pointer, touch, keyboard, screen reader, switch), zoom 200 percent, text scaling, reduced motion, dark and light themes. Source the minimum versions from the product context and analytics if Provided; otherwise Open. State which cells can be checked automatically and which need a person or a device.

## 7. Sources to study (Reference; verify version and date)
Apple Human Interface Guidelines (developer.apple.com/design/human-interface-guidelines); Material Design 3 adaptive layout and window size classes (m3.material.io, developer.android.com/design); WCAG 2.2 (1.4.4, 1.4.10, 1.3.4 Orientation, 2.5.1, 2.5.7, 2.5.8); MDN responsive design and container queries; Figma auto layout, variables, and modes (help.figma.com).
