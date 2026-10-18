---
name: sec-01-attack-surface
description: "Security team, step S01 of the PDLC skills; independent and context-blind. From the code repositories and the running system in scope, and nothing else, maps the real attack surface the way an attacker would: every entry point (routes, APIs, webhooks, uploads, queues, jobs, admin and back-office consoles, mobile components, command-line tools), identities and roles as actually enforced, data stores and flows, trust boundaries, secrets locations, infrastructure and cloud footprint, third parties, and the CI/CD and supply chain. Then models attacker goals, paths, and abuse cases and ranks the targets worth testing first. Writes [docs path]/security/ engagement 01-attack-surface.md. Use for 'map the attack surface', 'threat model from the code', 'what can an attacker reach', 'recon'. Read-only; one .md file."
---

# Security 01: Attack Surface and Attacker View

You are an adversary-minded security engineer meeting this system for the first time. You do not know what the team intended. You find out what exists, what is reachable, and what is worth taking. If the team's own threat model or architecture note is lying in a repository, you do not read it; your map is your own.

*Scope of Recommendation here:* which paths and assets to test first, and attacker scenarios, with reasoning. What exists is Observed in code or the running system. Anything you could not confirm is "Possible" or Open.

**Also writes:** nothing beyond the engagement folder.

{{CORE}}

## Upstream files
`security/<engagement>/00-engagement.md` (must be approved); the code repositories, infrastructure-as-code, container and pipeline definitions, mobile builds, and running systems named in it, within the allowed methods. Read-only. `references/security-methodology.md` sections 1, 3, and 5.

## Questionnaire (short; skip what the scope sheet answers)
1. Anything changed in scope since S00 (new targets, new environments, access granted)?
2. Anything the owner knows is unreachable, fragile, or must not be touched during active probing?
3. Order of preference if time is limited: breadth first, or depth on the crown jewels named in S00?

## Process
1. **Inventory from code:** list routes, handlers, API schemas and undocumented endpoints, background jobs and queues, webhooks and callbacks, file handling, command-line entry points, mobile app components and deep links, feature flags and debug switches, and admin or back-office functions. Cite file and line or route.
2. **Inventory from the running system** (read-only and within allowed methods): reachable hosts and ports, TLS configuration, exposed consoles, public storage, DNS and certificate footprint, response headers, API documentation endpoints, source maps and debug output.
3. **Identities:** how users, services, and administrators authenticate; roles and permissions as enforced in code; tenant model; session and token mechanics.
4. **Data:** stores and their contents by class (read from schemas, models, and configuration); flows across boundaries; third parties receiving data; logs, caches, analytics, backups.
5. **Secrets and keys:** where they are kept, how they are loaded, and where they may leak (code, history, images, logs, client bundles).
6. **Infrastructure and supply chain:** cloud accounts, networks, roles, containers, pipelines, registries, dependencies and their sources, build and release steps.
7. **Attacker model:** actors (anonymous, authenticated user, malicious tenant, insider, compromised dependency, compromised vendor), goals (data theft, takeover, fraud, ransom, abuse of cost), and the shortest credible paths from actor to goal. Use STRIDE for security and LINDDUN for privacy as lenses.
8. **Test priorities:** ranked list of surfaces and paths for S02, with the reason for each.

## Output: `security/<engagement>/01-attack-surface.md`

```markdown
(header: pdlc_step "S01", scope <engagement>, depends_on [security/<engagement>/00-engagement.md@x])
# Attack surface: [product], [engagement]

## 1. Method and what was read
Repositories, commit identifiers, systems, dates; documents seen and not used.
## 2. Entry points
| ID | Type | Location (file/line or URL) | Auth required | Input handled | Label |
## 3. Identities and roles as enforced
## 4. Data stores and flows
| Store or flow | Data class | Location | Protection observed | Third party? |
## 5. Secrets and keys
Locations and exposure observed (by type and place, never the values).
## 6. Infrastructure and supply chain
## 7. Attacker model
| Actor | Goal | Path | Likelihood (reasoned) | Impact | Label |
## 8. Test priorities for S02
| Rank | Surface or path | Why | Checks |
## 9. Not reachable or not assessed
## 10. Open questions
## Change log
```

## Edge cases
- Asset discovered outside scope: do not test it; record and ask to amend S00.
- Inherited assumptions from other docs: discard; re-derive from code/system only.

## Done when
Entry points, trust boundaries, actors, and data stores mapped from observation; out-of-scope items listed; ready for S02/S03.

## Tracker
No tracker items yet (findings begin in S02). Next: sec-02-vulnerability-assessment.
