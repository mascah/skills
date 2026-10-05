---
name: implement
description: Use when delivering a direct request, supplied issue, local spec, or selected Delivery slice with sufficient scope.
---

# Deliver the selected unit

Read [execution and handoff](../../references/execution.md) and
[mandate](../../references/workflow.md). Adopt project instructions and optional
workflow configuration. Accept a direct request, complete issue body, local
spec, or named slice; small work needs no spec, tickets, separate plan or setup.

1. Identify scope, constraints and observable acceptance. Inspect the checkout,
   relevant code and decisions. Read Delivery if present. Resolve scope/revision
   and prerequisites before dependent execution; report specific unavailable
   inputs rather than inventing scope. Plan only the necessary implementation.
2. Reproduce bugs where feasible and make behavioral changes with meaningful
   regression tests, using [tdd](../tdd/SKILL.md) for test-first work. Use
   [codebase-design](../codebase-design/SKILL.md) when an interface needs design.
   Choose routine technical details within the authorized intent; persist
   consequential scope changes in their canonical owner.
3. Implement and run appropriate project checks. Review the actual change with
   [code-review](../code-review/SKILL.md), resolve material findings and verify
   acceptance, including affected integration/recovery behavior. Preserve other
   sessions' changes and record honest limitations.
4. Commit selected changes on the permitted branch according to project policy
   when authorized; report branch/commit or dirty paths, real checks, findings,
   integration state and how to merge/resume. Do not equate a finished branch
   with target-branch integration or close external work without caller policy.

Follow the caller's worker/executor role. Direct execution is supported without
delegation tools; no recursive controller or external CLI is required. For a
whole specified outcome use `implement-spec` when available, preserving this
same unit-level completion contract.
