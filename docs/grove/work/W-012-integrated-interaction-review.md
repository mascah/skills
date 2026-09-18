---
type: work
id: W-012
status: proposed
created: 2026-09-18
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
- [ ] Final review instructions require a short affected interaction/recovery sequence and evidence mapping, with an explicit disposition for each uncovered transition.
- [ ] A walkthrough using the nullsec examples exposes stale-view, damaged-redispatch and misleading-label gaps without calling the green component suite sufficient evidence; a non-UI example demonstrates that browser testing is not mandatory.
- [ ] Verification rules retain useful existing evidence, delegate only missing checks and leave deferred human judgments unchecked. `grove lint` and plugin validation pass.

## Evidence
Shaping source: [nullsec run analysis](../../evidence/2026-09-18-nullsec-overnight-run.md). No implementation performed.

## Next
Small work, single agent: revalidate against the current work/review instructions, add the affected-sequence and evidence-gap rule, run the two walkthroughs and existing validation, then reconcile work-planning. Interactive runtime; no delegation needed. Reassess if this requires an executable verification framework instead of prompt guidance. Implement after the selected reliability batch to avoid concurrent writes to the same instructions; this is scheduling advice, not a hard dependency.
