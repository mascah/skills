---
type: work
id: W-012
status: done
created: 2026-09-18
started: 2026-09-18
updated: 2026-09-18
kind: fix
size: small
scope: [work-planning]
priority: 3
depends_on: []
---
## Outcome
The final review of a multi-component change checks the connected user actions and recovery paths affected by the change, so passing component checks cannot silently stand in for integrated behavior or a human usability judgment.

## Why now
Nullsec's green integrated commands did not expose a frozen canvas after closing/reopening 3D, damaged-ship redispatch behavior or confusing duration labels. Task-local evidence and screenshot existence left gaps in the player sequence. Worker reliability is selected first; this is the next review-quality improvement.

## Constraints
Apply proportionally to changed behavior. No mandatory browser suite for every task, no duplicate sim acceptance tests, no new eval framework, no nullsec code changes. Preserve existing evidence and run additional checks only for uncovered or invalidated behavior. Human taste and motivation remain attributed human judgments; deferred sessions do not block independent implementation.

## Design
Extend the whole-branch review instructions in `skills/work/SKILL.md`, `skills/work/reviewer.md` where shared guidance belongs, `references/planning.md` and `references/discipline.md`. The lead identifies a short end-to-end sequence from the outcome and changed interfaces; the reviewer maps each transition to evidence and flags untested boundaries. A focused verification worker checks uncovered mechanical transitions on the integrated revision and inspects the visible result when presentation changed. Existing test evidence can satisfy a transition; indiscriminate reruns cannot.

Representative cases from nullsec: dispatch -> close/reopen optional view -> return -> dispatch again; damaged return -> next dispatch; duration label -> actual completion semantics. These are examples to reason about, not a universal game checklist. Product-specific assertions belong to the owning project's work. Distinguish mechanical defects, missing evidence and reserved human judgments in the report.

## Acceptance
- [x] Final review instructions require a short affected interaction/recovery sequence and evidence mapping, with an explicit disposition for each uncovered transition.
- [x] A walkthrough using the nullsec examples exposes stale-view, damaged-redispatch and misleading-label gaps without calling the green component suite sufficient evidence; a non-UI example demonstrates that browser testing is not mandatory.
- [x] Verification rules retain useful existing evidence, delegate only missing checks and leave deferred human judgments unchecked. `grove lint` and plugin validation pass.

## Evidence
Shaping source: [nullsec run analysis](../../evidence/2026-09-18-nullsec-overnight-run.md). No implementation performed.

- 2026-09-18 T1 (SKILL.md whole-branch review step, reviewer.md whole-branch variant, planning.md preparation sentence, discipline.md review rule), base 330a2e5, small work run as one dispatched implementer Agent `model: sonnet`; task reviewer `model: opus` a1 fix (2 blocking: the one fix dispatch had been narrowed to exclude the verification worker's findings; report cited a stale revision; 2 minor); fix round 1 resumed the same implementer (a2); scoped re-review by the same reviewer: accept. 1 fix round. Evidence: `grove lint` 0 errors, `claude plugin validate .` passed. Walkthroughs (recorded, in the run's `.grove-run/W-012-walkthroughs.md`): nullsec sequence (dispatch → close/reopen 3D view → return → dispatch; damaged return → next dispatch; duration label → completion semantics) with a green component suite lands all three transitions on "missing evidence" with a named check, never on "covered"; non-UI sequence (`grove launch` CLI plus skill text) satisfies its mechanical transitions from existing test evidence, reserves one human judgment unchecked, and needs no browser suite.

## Next
None for this unit; the final-review sequence rule is in place. Reassess only if a run needs an executable verification framework instead of prompt guidance.
