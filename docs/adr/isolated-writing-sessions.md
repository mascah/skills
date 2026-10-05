# Isolate writing sessions

## Context

Concurrent agents sharing one checkout and index can stage another session's
half-written files. Documentation and shaping sessions have the same risk as
code sessions. Git's index lock does not isolate independently intended edits.

## Decision

Every writing session in this repository uses an isolated worktree branch.
Main is the integration target; the user integrates completed branches. Preserve
other sessions' worktrees and stage only owned changes. Use an ordinary merge
when branches diverge; fast-forward-only is not a required handoff constraint.

## Alternatives and consequences

Serializing all writing on main is cheaper but relies on no concurrent sessions.
A new lock or claim service would add machinery already avoided by separate
checkouts. Isolation costs a merge per writing session and requires resolving
conflicts between concurrent intent explicitly. Reconsider if the merge cost
outweighs the demonstrated shared-index risk or the harness provides equivalent
isolation.

## Provenance

Retains the rationale of the former Grove D-0004 decision from repository history
at `045a78f`. Its work-ID allocation and claim registry are retired, not required
by this decision.
