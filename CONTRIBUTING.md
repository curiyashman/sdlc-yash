# Contributing

This repository is **maintainer-gated**. Anyone can fork and open a pull request on a public GitHub repo; that does not mean every PR will be accepted.

## Rules

1. **Do not push to `main`.** Direct pushes are blocked. Changes land only through a pull request.
2. **Every PR needs maintainer acceptance.** At least one approving review from a [CODEOWNER](.github/CODEOWNERS) is required before merge. Unsolicited PRs may be closed without merge.
3. **Open an issue first** (or ask the maintainer) before submitting substantial work. Drive-by refactors and drive-by skill rewrites are usually declined.
4. **CI must pass.** The `check` workflow must be green on the PR.
5. **Edit `source/`, not generated folders.** Never change `Common/`, `Product/`, `Design/`, `Development/`, `QA/`, `Deployment/`, or `Security/` by hand. Run `python source/build.py` and commit the regenerated output with your source change.
6. **Keep the product-agnostic rule.** Skills must not hard-code a customer’s product, stack, or org.

## What we accept

- Bug fixes in `tools/pdlc.py`, `source/build.py`, or tests
- Clear gaps in skill steps that break the documented flow
- Doc fixes that match the current six-team model

## What we usually decline

- Large rewrites without prior agreement
- Adding a product’s private docs into this skills repo
- Changes that duplicate `dev-05` / `dev-06` with QA / Deployment stages instead of using `config.qa_stage` / `config.deploy_stage`

## Maintainer

PRs are reviewed and merged by [@curiyashman](https://github.com/curiyashman).
