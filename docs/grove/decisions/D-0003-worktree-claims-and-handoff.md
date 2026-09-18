---
type: decision
id: D-0003
status: accepted
updated: 2026-09-18
applies_to: [work-planning]
---
## Context
The builder reported on 2026-09-18 that main cannot see work claimed or active in another worktree, and twice completed code was merged while its work page remained proposed because closure had been omitted on the branch. The close skill already requires closure before handoff, but the CLI has no shared claim or completion-handoff check. The builder accepted shared Git-metadata claims and a separate handoff validator, then requested implementation work items in this conversation.

## Decision
Store local work ownership in a Grove-managed registry under the directory Git reports as its common metadata directory. All linked worktrees consult the same registry without commits to main. Keep work state, acceptance, evidence and closure versioned on the implementation branch. A claim means ownership, not proof of a live process or completed work.

Provide a separate completion-handoff validator that checks the committed delivery declaration and closed work at an explicitly resolved candidate commit. Its correctness must not depend on local claims, so the same check can run in a clean clone or future PR automation. The close skill invokes it after committing closure and before presenting a completion handoff. W-013 and W-014 hold the intended changes; these are not implemented capabilities yet.

## Alternatives rejected
- Commit activation to main before each branch: adds coordination commits and does not keep progress or closure synchronized.
- Infer ownership only by scanning worktrees: cannot atomically prevent duplicate claims, and stale worktrees can mislead.
- Add a hosted tracker now: unnecessary for the current local-worktree workflow; revisit for cross-machine ownership.
- Add more closure reminders alone: the instruction already exists and the reported failure recurred.
- Automatically close work when code merges: merge success cannot prove acceptance or knowledge reconciliation.

## Consequences
Claims are local metadata, neither committed nor pushed. Acquisition and release/takeover need concurrency-safe ownership checks and explicit recovery; elapsed time alone must not release a claim. Status distinguishes checkout state from branch observations, avoids suggesting work owned elsewhere, and does not satisfy main's prerequisites from unmerged branch closure.

The completion handoff records which work the branch delivers in committed data. Partial delivery must explicitly distinguish closed delivered units from unfinished work. Validation checks structure and evidence references, not the truth of human judgments. Command names, registry/declaration formats, integration detection and cleanup are implementation-design tasks.

A local merge wrapper is optional future convenience; direct Git commands would bypass it. Required PR automation could enforce the validator later, but neither a wrapper nor CI integration is selected for this first implementation. Existing W-010/W-011 reliability work remains the selected focus.

## Reconsider when
Ownership must span independent clones or machines; a tested workflow cannot recover claims safely; or repeated bypass of the standalone handoff check warrants a merge wrapper or protected-branch automation.
