# AI features addendum (reference pack)

Read this pack when a feature uses an AI model (generation, classification, extraction, search ranking, agents). It adds to the normal steps; it doesn't replace them.

## Product (product-02, product-04)
- **Behavior requirements:** what the feature must do, must never do, and how it must behave when unsure. Examples: refuse, ask, hand over to a human, show confidence. Write these as FRs, BRs, and NFRs as usual.
- **Eval set:** the expected behavior, as examples that Product owns. Each eval case is an input with the expected result or the rule for judging it, written in the stories file as `M01.S01.F01-EV01` (`pdlc.py new-id ev M01.S01.F01`). Include ordinary cases, edge cases, and must-refuse cases.
- **Thresholds:** the pass rate per eval group that counts as acceptable. These are Provided by the team, never invented. The thresholds are acceptance criteria.
- **Data rules:** which user data may be sent to a model provider, whether outputs may be stored or used for training, and the consent this needs (see `compliance.md` if it is bundled).
- **Cost and speed:** expectations as users and the business experience them, for example how long a user waits and the acceptable cost per use. Record numbers only when the team provides them.

## Design (design-02)
Show every state an AI feature has: thinking or streaming, partial result, low confidence, refusal, failure and retry, human handover, edit and undo of AI output, and feedback capture (for example a thumbs up or down with a reason). Make clear which content the AI generated.

## Development (dev-01, dev-03, dev-04)
- **Model choice:** the decision, as a DEC: provider, model, version pinning, region, and data retention terms (Reference, with date).
- **Prompts:** prompts are versioned files in the code repository with an ID and a change log. A prompt change is a code change with its own eval run.
- **Guardrails:** input and output checks, tool permissions for agents, and limits on actions an agent may take without confirmation.
- **Budgets:** limits per request and per user for tokens or cost, timeouts, and the fallback when the model is slow or down. Add these to L9 Caching and L10 Rate limiting.
- **Observability:** in L12, log prompt version, model version, latency, cost, and outcome, without personal data unless allowed.
- **Threat model:** add prompt injection, data exfiltration through tools, and cost abuse (see `threat-model.md`).

## QA (dev-05)
- **Run the eval set** as a test suite against each candidate build. Report the pass rate per group against the thresholds; below a threshold means No-Go.
- **Red-team cases:** prompt injection, jailbreaks, and personal data leakage, logged like other test cases.
- **Regression:** re-run the eval set on every prompt or model change.

## Operations (dev-06)
- **Monitoring:** quality sampling, cost, latency, refusal and failure rates, and drift against the eval set.
- **Rollback:** the plan for a prompt or model version, the same as for code.
- **Provider changes:** a provider deprecating or changing a model is an upgrade item (`UPG-`) in dev-07.
