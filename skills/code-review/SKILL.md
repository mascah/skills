---
name: code-review
description: Use when reviewing a branch, PR, or working diff for requirement gaps, defects, integration risks, and project conventions.
---

# Review the actual change

Read [execution and evidence](references/execution.md). Resolve the review
base from the caller or known branch baseline; state it. Include relevant staged
and unstaged changes when reviewing work in progress. Check that refs resolve
and inspect the complete selected diff and relevant surrounding code. An empty
diff is a finding about scope, not evidence of successful review.

Locate the originating request, issue body or canonical spec/slice and project
standards. Use existing context; setup and tracker access are unnecessary when
the sources are supplied locally. If a source is unavailable, report that gap
and continue the review that is possible; never invent requirements.

Check both intended behavior and conventions against the files. Look for
defects, missing acceptance, regression sensitivity, failure/recovery sequences,
ordering/migration risks, stale documents and integration assumptions. Evaluate
costly abstractions against actual caller needs with
`codebase-design` when useful. Distinguish a real
defect from a preference and from an unexercised runtime boundary.

Use direct review or focused independent review under caller policy; no fixed
agent roster or mandatory fan-out. Report findings by consequence, with file or
diff location, concrete trigger, expected/actual effect and supporting evidence.
List checks actually run, requirements coverage and unavailable validation.
For no material findings, say that with the review scope and residual limits.
Review alone does not authorize unrelated fixes, merge or publication; within
an implementation mandate, fix material findings and recheck affected behavior.

The `codebase-design` helper is optional. Without it, evaluate whether interfaces hide useful complexity, related changes stay together, and tests observe public behavior; avoid speculative abstractions.
