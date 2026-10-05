# Execution and handoff

## Before writing

Inspect the actual checkout, branch, dirty files, existing worktrees and project
commands. Respect the project's isolation rule; use an isolated branch/worktree
when required, preserving other sessions' changes. Never reset another worker's
branch or stage unrelated edits. Use the project's commit convention (here,
Conventional Commits); tracker references must be real and are optional.

Resolve the selected scope and acceptance from the request or canonical document.
For a remote assignment, identify repository, scope path/slice, and a usable
revision; verify it resolves and the documents match it. Local requests may use
the current checkout, with relevant uncommitted inputs explicitly identified.
Unpushed local documents cannot serve as ready remote assignments. Recheck
prerequisites against available integrated code and evidence. Closure of an
issue, a worker exit, or a green component check alone proves neither delivery
nor integration. Missing input blocks only dependent work; name the exact path,
revision, issue content, or decision needed and continue independent authorized
work.

## Implement and verify

Plan at the smallest useful depth. Follow Delivery if present and revalidate its
checkout observations. Preserve settled intent; update its owner when scope
changes. Use meaningful regression/acceptance tests for behavioral changes, and
a test-first loop through observable interfaces when useful. Documentation and
mechanical configuration use appropriate document/diff/structural checks rather
than contrived behavioral tests.

Run relevant project checks, inspect their output and review the actual diff
against acceptance and project conventions. Verify interaction and recovery sequences when the change
affects them: record which transitions were exercised, including integration
boundaries. Component success does not prove an end-to-end interaction.
Fix material findings and recheck affected behavior. Record tests actually run,
tested revision/dirty state, failures, pending human judgments and unexercised
integrations. Never describe a stub or prose review as a live integration.

On interruption, inspect git and existing progress/evidence and any caller-owned
running work before repeating actions. For sustained work, leave enough handoff
context in Delivery or a concise local note to identify completed slices,
outstanding owners, checks and the next action. Do not create a new run schema.

## Direct and delegated execution

Honor the caller's executor policy. Without one, implement directly; focused
delegation is optional when tools and scope warrant it. No external CLI, fresh
agent per step, model choice, fixed fan-out, or controller loop is required.
The caller owns model/CLI routing, concurrency, retries, deduplication, process
supervision and worktree lifecycle. A worker follows its assigned role; it does
not recursively launch a controller or widen its mandate. Avoid overlapping
writes, and give one owner responsibility for integration.

A minimum handoff is an ordinary prompt:

> Worker role: implement the normalization bug in the supplied issue body at
> repository revision `<actual-sha>`. Acceptance: trimming and case normalization
> work through the public function. Preserve the dependency policy and run the
> project's documented test command. Return branch/commit, actual checks,
> remaining findings and integration state. The caller owns dispatch and merge.

Use pointers for accessible content; supply unavailable issue-only scope in
full. If capabilities are absent, implement directly when authorized or report
the missing capability. Do not fabricate delegation or runtime validation.

## Completion report

Report selected scope; branch and commit (or dirty paths); checks and their
results; remaining findings, human judgments and runtime limits; whether results
are merely implemented, integrated on the chosen branch, or merged into the
target; and how to merge or resume. A blocked report names a concrete waiting
condition and the independent work completed. Caller verification precedes
recording completion. External progress, closure and PR changes follow only the
authorized caller policy.
