---
type: work
id: W-013
status: done
created: 2026-09-18
started: 2026-09-18
updated: 2026-09-18
kind: feature
size: bounded
scope: [work-planning]
priority: 2
depends_on: []
plan: docs/plans/W-013-W-014-worktree-completion.md
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
- [x] A real temporary Git repo with main and at least two linked worktrees shows the same claim immediately from each checkout, without tracked-file changes or a main commit; text and JSON distinguish claim from checkout state.
- [x] Concurrent acquisitions for the same work yield one owner; a conflicting multi-unit request leaves no partial claims. Same-owner retry is safe and a stale owner cannot release a replacement's claim.
- [x] Work claimed elsewhere is not recommended for duplicate execution; active and closed-on-branch observations do not alter main's recorded state or satisfy its prerequisites.
- [x] Interrupted ownership, a missing worktree, branch changes and corrupt metadata produce actionable recovery diagnostics. Explicit release/takeover works, and record age alone never frees ownership.
- [x] A completed branch remains visible until integration/release reconciliation. The chosen normal cleanup path is exercised, including an ambiguous or squash-integration case that requires explicit recovery.
- [x] Updated lifecycle guidance explains local-only storage and ownership semantics; relevant CLI tests, full existing CLI suite, grove lint and plugin validation pass with evidence recorded.

## Evidence
Shaping only, 2026-09-18: builder report and agreement in the nullsec conversation. Inspected skills checkout c88b228: cli/grove/status.py, cli/grove/cli.py, cli/grove/close.py, references/discipline.md and W-011 context. Existing status indexes only the current knowledge root. Git inspection of nullsec main and its linked station-foundations worktree confirmed the same common metadata directory. No claims implementation or runtime validation performed.

- 2026-09-18 T1 (`cli/grove/claims.py`, `cli/grove/cli.py`, `cli/tests/test_claims.py`), base 330a2e5: implementer Agent `model: sonnet`; task reviewer `model: opus` accept, 0 blocking, 7 minor (three folded into T2). 0 fix rounds. Implementer evidence: 15 new tests, suite 140 passed, `grove lint` 0 errors, `claude plugin validate .` passed. Tests use a temp repo with main plus two linked worktrees: same claim visible from all three checkouts with no tracked-file change and no commit; multi-id conflict leaves no partial write; same-owner retry exit 0; foreign release refused, `--take` succeeds; two threads yield one owner; missing worktree, branch gone and malformed registry diagnostics.
- 2026-09-18 T2 (`cli/grove/status.py`, `cli/grove/claims.py` observations, `cli/grove/cli.py`, `cli/tests/test_status.py`, `cli/tests/test_claims.py`), base c5aa2e3: implementer Agent `model: sonnet`; task reviewer `model: opus` accept, 0 blocking, 4 minor. 0 fix rounds. Evidence: suite 146 passed, `grove lint` 0 errors, `claude plugin validate .` passed. Tests: text and JSON carry the claim and observation; a unit closed only on its branch shows `closed on branch, awaiting integration` while a dependent unit on main still reports the prerequisite unclosed; recommendation skips a foreign claim with "resume or coordinate"; `integrated` after merge; `possibly squash-merged` when the history page lands on main without the branch; lock-contention refusal names the lock path.
- 2026-09-18 T4 shared with W-014 (discipline.md claim/release/take guidance and limits, work SKILL.md step 1, close SKILL.md, init.py BLOCK line plus generalized branch naming, curate/explore branch lines, test_init.py, end-to-end `test_lifecycle_claim_close_verify_release` in test_workflow.py, CLAUDE.md/AGENTS.md regenerated), base 312a946: implementer Agent `model: sonnet`; task reviewer `model: opus` a1 fix (1 blocking: close skill claimed `grove close` commits and ran the validator before the commit step; 3 minor), a2 accept. 1 fix round. Evidence: suite 170 passed, `grove lint` 0 errors, `claude plugin validate .` passed. The workflow test in a temp repo with a linked worktree: claim → close → declaration → commit → verify passes from main → `closed on branch, awaiting integration` → declaring a proposed unit fails → repair → passes → merge → `integrated` → release.
- 2026-09-18 whole-branch review (Agent `model: fable`, the session model) at e915c20 found that `grove claims` from the owning worktree labelled an unmerged close `integrated`, and that the printed handoff release step failed after `git worktree remove` because the owner token lived there. The one post-review fix dispatch (`model: sonnet`) committed 96bd003: `observe()` skips the HEAD ancestry test on the claim's own branch or worktree (new test covers worktree before merge, main before and after merge, worktree after merge), and the handoff releases with `grove claim --take <ids> && grove claim --release <ids>`. Suite 171 passed, lint 0 errors, validate passed.

## Next
None for this unit; claims and status overlay are in place. Reconsider when ownership must span machines (D-0003).
