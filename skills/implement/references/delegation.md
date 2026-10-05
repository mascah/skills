# Caller and worker handoff

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
