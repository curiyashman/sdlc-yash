---
name: dev-07-maintenance
description: "Development team, step D07 of the PDLC skills: the route for work that has no product requirement, namely hotfixes, tech debt, dependency and platform upgrades, spikes, and chores. Records one item in [docs path]/dev/maintenance/: what and why, evidence, affected code repositories and product areas, risk, the guarantee that product behavior doesn't change (or a query to product when it would), the approach, tests, and rollback; adds it to tracker.yaml as HF-, TD-, UPG-, SPK-, or CHR- with dependencies. Then the item is built with dev-04, tested with dev-05, and shipped with dev-06; a spike ends in a decision (DEC). Use for 'hotfix', 'production bug, urgent', 'tech debt', 'upgrade React / Node / the database', 'security patch', 'spike on X', 'investigate whether', 'clean up', 'chore'. Questionnaire first, assumes nothing, one .md file."
---

# Dev 07: Maintenance

You are a staff engineer who keeps the product healthy. Not all work starts from a requirement: production breaks, code ages, dependencies need upgrades, and some questions need a time-boxed investigation before anyone can decide. This step gives that work a route, so it is tracked, tested, and traceable like everything else, without inventing product requirements.

**Types**
| Type | ID | For | Ends with |
|---|---|---|---|
| Hotfix | `HF-001` | a production defect that cannot wait for the next version | a patch release (dev-06 Hotfix mode) and the bug's root cause |
| Tech debt | `TD-001` | known shortfalls in code, architecture, tests, or tooling | the change merged and verified, or a DEC to accept it |
| Upgrade | `UPG-001` | dependency, runtime, framework, database, or platform upgrades, including security patches and deprecated AI models | the upgrade released, with the install list updated |
| Spike | `SPK-001` | a time-boxed investigation that answers one question | a DEC with the answer and its evidence |
| Chore | `CHR-001` | operational work with no behavior change (rotate keys, clean up data per policy, rename) | done and recorded |

**Product behavior doesn't change here.** If the fix or change alters anything a user sees or relies on, it is not maintenance alone: raise a query to product (`to: product`). Product answers in its files or through a change request. The maintenance item waits for the answer, or ships only the part that doesn't change behavior. A hotfix that restores the behavior the stories already define is not a behavior change.

*Scope of Recommendation here:* approach, risk rating, test and rollback plan, and, for tech debt, whether to fix now, later, or accept with a DEC. Each cites the evidence. Timelines and priorities are the team's.

**Also writes:** a DEC for a spike's answer or an accepted risk; the install list in `dev/architecture.md` (PATCH bump) for upgrades, with the person's OK.

{{CORE}}

## Upstream files
`dev/00-dev-setup.md` (repositories, environments); `dev/architecture.md` (layers, install list); `tracker.yaml` (existing bugs and items); `decisions/`; for a hotfix, the incident file in `dev/releases/` and the stories file that defines the correct behavior; the code repositories (read-only until dev-04).

## Questionnaire (skip what the sources answer)
1. What is it: hotfix, tech debt, upgrade, spike, or chore? In a sentence, what and why now?
2. Evidence: incident, error, logs, metrics, advisory (for example a CVE), deprecation notice with its date, or a team observation. Each with its source.
3. Which code repositories, layers (L1 to L13), and product areas (map IDs, stories) does it touch?
4. Could any user-visible behavior change? If yes, which, and has product been asked?
5. Risk if left as it is, and risk of the change. Use the team's scale or a proposed default (low, medium, high), confirmed.
6. For a spike: the one question it must answer, what counts as an answer, and its time box (team-set).
7. For an upgrade: from and to versions (Reference, cited release notes and dates), breaking changes, and what must be re-tested.
8. For a hotfix: the shortened path the team accepts (for example skip pre-production with a named approver), and what is completed after release (tests, root cause, documents).

## Output: `dev/maintenance/<id>-<slug>.md`

```markdown
(header: pdlc_step "D07", scope <HF/TD/UPG/SPK/CHR ID>, depends_on [the files read, with versions])
# [ID]: [title]

## 1. What and why
Type, evidence (labeled, with sources), affected repositories, layers, and map IDs.
## 2. Behavior guarantee
"No user-visible change", with how it is verified; or the query ID raised to product and what waits for it.
## 3. Approach
For a spike, the question, the method, and the exit condition. Otherwise, the change in requirement form, with no code.
## 4. Risk
| Risk | Rating | Mitigation | Label |
## 5. Tests and verification
Existing tests that must still pass; new tests; for a hotfix, the test that reproduces the defect; for an upgrade, the re-test list.
## 6. Release and rollback
Which version or patch release; the rollback plan; for a hotfix, the shortened path and what is completed after.
## 7. Outcome
Filled at the end: result, DEC ID (spike or accepted risk), PRs, release.
## Change log
```

## Tracker
Add the item to `tracker.yaml` (`pdlc.py new-id hf|td|upg|spk|chr`; type `hotfix`, `tech_debt`, `upgrade`, `spike`, or `chore`; title; status `backlog`; `depends_on`; source this file). Run `lint --fix` and `board`. Next: dev-04-code-plan-build for the item (a spike may need no code), then dev-05-test-qa and dev-06-deploy. A hotfix uses dev-06 Hotfix mode.
