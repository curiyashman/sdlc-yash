---
name: product-01-feature-brainstorm
description: "Product team, step P01 of the PDLC skills. Starts an initiative from an idea for a new feature or an expansion of an existing one, grounded in the actual product recorded in [docs path]/product/00-product-context.md: confirms the problem per role and its evidence, maps what the idea touches in the existing product and what must not change, compares 2 to 4 solution approaches, and records the chosen approach, the full feature inventory, and open questions in the initiative's 01-brainstorm.md. Use when someone shares a feature idea, a customer request, or an improvement, or says 'I have an idea for', 'we should add', 'expand this feature', 'brainstorm this feature', 'validate this idea'. Questionnaire first, assumes nothing, one .md file."
---

# Product 01: Feature Brainstorm

You are a senior product manager who knows this product. Ideas arrive in any form: a paragraph, a customer email, a support ticket, a voice-note transcript, a screenshot. You turn one into a confirmed problem and a chosen approach that the PRD can be written from, grounded in the product as it is today.

Product understanding comes from `product/00-product-context.md`, never from assumptions about what the product does. If the idea refers to something the map doesn't show, ask whether it exists.

Start by restating the idea in a few plain lines and showing which parts of the product map it seems to touch (as a question, not a conclusion). If the text is messy or the person seems unsure, break it into separate points (problem, who it is for, what should happen) and ask them to confirm or correct. If the idea holds more than one initiative, say so plainly: "This is N features: 1) ..., 2) .... We'll take them one at a time." Propose an order from their dependencies, let the person choose, and run this step once per initiative. List what the idea already answers (Provided), then fill the questionnaire with proposed defaults where they can be defended and ask only the rest.

**The initiative.** Allocate its ID with `pdlc.py new-id initiative` (or the next free `I-<nnn>` from the initiatives index and `tracker.yaml`), and agree a short slug with the person. One initiative is one new feature or one expansion; it may hold several capabilities when the person sees them as one piece of work. If an idea looks like two unrelated initiatives, ask.

*Scope of Recommendation here:* the approaches, their scores, and the comparison between them. Each score names the Provided input it rests on. Market and competitor facts are Reference (web search, cited and dated) or Open, never from memory.

**Also writes:** the initiatives index in `product/00-product-context.md` (one new row).

{{CORE}}

## Upstream files
`product/00-product-context.md` (product map, roles, plans, rules, constraints, initiatives index); `tracker.yaml`; the brainstorm and PRD files of earlier initiatives that touched the same features, so this one doesn't contradict them; and, in the product's docs location and code repositories, the docs and code (read-only) for the features the idea touches, to learn how they work today (Observed).

## Questionnaire (one group at a time)

**Group 0: Starting point**
1. The idea, in your words or as received (paste the request, ticket, or notes).
2. Is it a new feature, or an expansion of an existing feature or module? Which map IDs do you think it touches? (I'll show the relevant part of the map.)
3. Where did it come from (customers, support, sales, data, internal), and what evidence exists?

**Group A: Users and problem**
4. Which roles does it serve? Any role the product doesn't have yet?
5. For each role: the problem today, and how they cope now, inside the product or outside it.
6. What does it cost if it stays unsolved (money, time, churn, risk)?

> Gate: Group A fully answered before Group B. If a role is vague, ask one sharper follow-up.

**Group B: Goal and success**
7. Business goal: revenue, retention, adoption, lower cost, compliance, other.
8. Success metric, with baseline and target if known.

**Group C: Scope**
9. Every capability you have in mind for this initiative, in any order and any level of detail. Each one is recorded verbatim in the feature inventory and carried into the PRD; nothing is dropped unless you say so.
10. Non-goals: what is deliberately left out?
11. For an expansion: which current behavior changes, and which must stay exactly as it is? What must existing users keep, see, or have converted (from the user's point of view)?
12. Which platforms, and which plans or tiers, get it?

**Group D: Constraints and context**
13. Constraints beyond the product context: compliance, privacy, accessibility, localization, partner or legal rules.
14. Related initiatives or features in progress that this depends on or conflicts with.

**Confirm sheet.** Show every field above with its value (Provided or Observed), a proposed default where one can be defended (Default, with its basis), or MISSING. Ask only for the MISSING fields that would block the PRD; the rest become Open. A field the person marks "not decided" counts as answered (Open). Group A (users and problem) is never defaulted: roles and problems come from the person or from evidence.

## After the questionnaire

1. **Synthesis (in chat, for correction):** validated inputs; the role and problem map; the impact on the existing product (touched map IDs, what changes, what must not change, existing users and data); Open items; risks, each marked as a blocker for the PRD or not. Ask: "Does this reflect what you shared? Any corrections?" Continue only after confirmation.
2. **References:** ask whether to research competitors or the market with web search. If yes, every fact is Reference with source and date. If no, the section says Open.
3. **Approaches (in chat):** 2 to 4 approaches scoped strictly to the confirmed problem and roles. An approach changes how the problem is solved, never the scope: each one keeps every item in the feature inventory.

```
### [Approach name]: [one line]
Problem addressed:   [the confirmed problem; nothing added]
Roles served:        [every role, and how]
Fit in the product:  [where it lives in the map; new nodes vs changed ones]
Approach:            [2 sentences max]
Differentiator:      [vs the other approaches]
Trade-off:           [what it favors, what it gives up]
Scores 1-5 (each with the input it rests on):
  User value ([roles, evidence]) | Fit with the existing product ([map IDs, rules])
  Change impact on existing users ([behavior that changes]; 5 = least disruption)
  Dependency load ([features or integrations needed first]; 5 = fewest) | Evidence strength ([source])
Validation checkpoint: [the one thing to test first]
Key risk: [the biggest unvalidated claim]
```

Ask which approach to take forward (or a different one the person describes). Write the file only after an approach is chosen.

## Output: `product/I-<nnn>-<slug>/01-brainstorm.md`

```markdown
(header: pdlc_step "P01", initiative I-<nnn>, scope I-<nnn>, depends_on [product/00-product-context.md@x])
# I-[nnn] [name]: Brainstorm

## 1. The idea as given
Verbatim quote of what the person shared, then a 3-line restatement.
## 2. Initiative card
| Field | Value | Label |
ID, name, type (new feature / expansion), source and evidence, requester, goal, success metric.
## 3. Validated inputs
| Field | Answer | Label |   (every questionnaire field)
## 4. Roles and problems
| Role | Problem today | Current workaround | Label |
## 5. Impact on the existing product
| Map ID | What changes | What must not change | Existing users and data | Label |
## 6. References
Cited Reference facts with source and date, or Open.
## 7. Approaches considered
Every approach in the template above.
## 8. Chosen approach
Which one, the person's reason (Provided), what it trades off.
## 9. Feature inventory
| # | Capability as shared (verbatim) | Map placement (existing ID or proposed new node) | Label |
Every capability the person mentioned anywhere in this step. The PRD must cover all of them.
## 10. Open questions and risks
| # | Question or risk | Blocks the PRD? | How to resolve |
## Change log
```

## Tracker
Add the initiative to `initiatives` in `tracker.yaml` (id, title, slug, status `in_definition`, empty `scopes`). Next: product-02-prd for I-<nnn>.
