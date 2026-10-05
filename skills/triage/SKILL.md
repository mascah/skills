---
name: triage
description: Use when classifying a request, investigating a bug or ambiguity, checking readiness, or preparing an implementation assignment.
---

# Prepare the next useful action

Read [GitHub coordination and readiness](../../references/github.md),
[artifact ownership](../../references/artifacts.md), and
[execution](../../references/execution.md). Accept local requests, supplied
issue bodies or accessible tracker references without requiring setup.

Read full scope, relevant discussion, prior triage findings and current
coordination. Search code for existing implementation and durable docs for prior
decisions before repeating investigation. Reproduce bugs where feasible and
record the actual result, commands and limits. A report that cannot be reproduced
may need a concrete input rather than immediate rejection.

Classify what the request needs: investigation, shaping, a runnable implementation
unit, human input, or rejection. Use [shaping](../shaping/SKILL.md) only for
consequential ambiguity, honoring settled facts. Check every readiness condition
in the shared contract, including revision accessibility, integrated blockers,
caller ownership and parent/child overlap. A maintainer's label request does not
make missing prerequisites true; report the specific gap. Research/decision
work does not become an implementation assignment just because it is well written.

Within authorized scope, update substantive intent in its canonical spec/slice
and retain consequential rationale locally. Keep routine assignment, labels,
discussion, progress and PR links in the tracker. Use the configured vocabulary;
apply external changes only under caller authority. Without that authority,
return the concrete recommendation and prepared operations, not invented writes.

Return the disposition with evidence and the next action. For executable work,
give scope/reference and revision, constraints, acceptance, project commands,
prerequisites and caller role. For missing input, name exactly what would make
the unit runnable; continue independent authorized work. Rejection/closure is a
disposition, never evidence that dependent implementation was delivered.
