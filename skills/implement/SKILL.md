---
name: implement
description: Use when delivering a direct request, supplied issue, local spec, or selected Delivery slice with sufficient scope.
---

# Deliver the selected unit

Read [common discipline](references/discipline.md),
[selected-scope delivery](references/implementation.md), and
[verification](references/verification.md). Accept a direct request, supplied
issue body, local spec or slice without required setup, tickets or extra artifacts.

For tracker assignments, read [scope and readiness](references/assignments.md).
Use the project's tracker interface to fetch the body/discussion and resolve its
canonical pointer, or use complete supplied issue-only content. If delegation or
worker roles apply, read [caller/worker handoff](references/delegation.md).

1. Identify scope, constraints and observable acceptance. Inspect the checkout,
   relevant code and decisions. Read Delivery if present. Resolve scope/revision
   and prerequisites before dependent execution; report specific unavailable
   inputs rather than inventing scope. Plan only the necessary implementation.
2. Reproduce bugs where feasible and make behavioral changes with meaningful
   regression tests, using `tdd` for test-first work. Use
   `codebase-design` when an interface needs design.
   Choose routine technical details within the authorized intent; persist
   consequential scope changes in their canonical owner.
3. Implement and run appropriate project checks. Review the actual change with
   `code-review`, resolve material findings and verify
   acceptance, including affected integration/recovery behavior. Preserve other
   sessions' changes and record honest limitations.
4. Commit selected changes on the permitted branch according to project policy
   when authorized; report branch/commit or dirty paths, real checks, findings,
   integration state and how to merge/resume. Do not equate a finished branch
   with target-branch integration or close external work without caller policy.

Follow the caller's worker/executor role. Direct execution is supported without
delegation tools; no recursive controller or external CLI is required. For a
whole specified outcome use `implement-spec`, preserving this
same unit-level completion contract.

Optional helpers: use installed `tdd`, `codebase-design`, `code-review` or `implement-spec` when useful. Without them, write an observable regression before the fix, verify its meaningful failure then pass, compare interface choices against caller needs, review the actual diff against acceptance/conventions, and verify the whole selected outcome directly.
