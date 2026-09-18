---
type: work
id: W-013
status: proposed
created: 2026-09-18
updated: 2026-09-18
kind: feature
size: bounded
scope: [work-planning]
priority: 2
depends_on: []
batch: worktree-completion
batch_reason: Shared lifecycle instructions and a joint claim-to-closed-handoff scenario; prepare together and serialize edits to CLI and skills.
---
## Outcome
Main and every linked worktree can see which branch owns a work unit, avoid duplicate acquisition, and distinguish their own committed work state from progress or closure on another branch. Interrupted ownership can be recovered explicitly without losing work.

## Why now
The builder reports no visibility from main into work claimed in worktrees. On 2026-09-18 they selected shared Git-metadata claims and requested implementation items. Two missed branch closures also motivate W-014; visibility and completion validation solve separate failures. [[D-0003-worktree-claims-and-handoff]]

## Constraints
Local linked worktrees of one repository only; no hosted service, tracked claim files, main-status commits, scheduler or heartbeat requirement. Claims are ownership records, not process-liveness assertions. Preserve checkout-local dependency truth and existing work status semantics. No automatic expiry, closure, merge or push. Keep work and evidence on their branch.

## Design
Resolve the common metadata directory through Git, including linked-worktree .git files, rather than assuming a directory at checkout/.git. Store a versioned Grove registry there with work IDs, branch/worktree identity, claim identity and acquisition time. Expose acquire, inspect, release and explicit takeover operations; exact command spelling and storage format belong to planning. Acquire a requested set atomically: a conflict cannot leave half a batch claimed. Use an ownership token or equivalent so a stale session cannot release a newer owner's claim. Same-owner retries and resume must be safe.

Overlay ownership in text and JSON status, keeping checkout status separate from observed branch/worktree state. Claimed elsewhere means resume/coordinate, not a fresh execution recommendation. Show closed-on-branch awaiting integration distinctly; never satisfy main's dependencies from that observation. Define whether progress observations come from committed or dirty worktree files and label them accurately. Missing worktrees, renamed/deleted branches and malformed records must remain diagnosable without deleting evidence or silently freeing work. Read-only inspection must not execute commands from another checkout.

Define the normal post-integration release path as well as interruption recovery. A close on the feature branch alone must not erase visibility while integration is pending. Handle fast-forward, merge and squash integration conservatively; ambiguous integration requires explicit reconciliation rather than guessed closure. Wire acquisition/resume and release guidance into the work/close discipline and managed init instructions where needed. Reuse W-011 checkpoint concepts without turning a claim into its execution ledger. W-014's validator remains independently usable without this registry.

## Acceptance
- [ ] A real temporary Git repo with main and at least two linked worktrees shows the same claim immediately from each checkout, without tracked-file changes or a main commit; text and JSON distinguish claim from checkout state.
- [ ] Concurrent acquisitions for the same work yield one owner; a conflicting multi-unit request leaves no partial claims. Same-owner retry is safe and a stale owner cannot release a replacement's claim.
- [ ] Work claimed elsewhere is not recommended for duplicate execution; active and closed-on-branch observations do not alter main's recorded state or satisfy its prerequisites.
- [ ] Interrupted ownership, a missing worktree, branch changes and corrupt metadata produce actionable recovery diagnostics. Explicit release/takeover works, and record age alone never frees ownership.
- [ ] A completed branch remains visible until integration/release reconciliation. The chosen normal cleanup path is exercised, including an ambiguous or squash-integration case that requires explicit recovery.
- [ ] Updated lifecycle guidance explains local-only storage and ownership semantics; relevant CLI tests, full existing CLI suite, grove lint and plugin validation pass with evidence recorded.

## Evidence
Shaping only, 2026-09-18: builder report and agreement in the nullsec conversation. Inspected skills checkout c88b228: cli/grove/status.py, cli/grove/cli.py, cli/grove/close.py, references/discipline.md and W-011 context. Existing status indexes only the current knowledge root. Git inspection of nullsec main and its linked station-foundations worktree confirmed the same common metadata directory. No claims implementation or runtime validation performed.

## Next
Run grove batch W-013 W-014 and prepare one shared sequential plan against the current checkout. Settle claim format, atomic locking/recovery, branch observation and cleanup before implementation. Keep existing focus W-010; schedule shared CLI/skill edits after overlapping reliability work. W-013 and W-014 have no hard dependency on each other.
