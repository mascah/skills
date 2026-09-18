---
type: work
id: W-011
status: proposed
created: 2026-09-18
updated: 2026-09-18
kind: fix
size: small
scope: [work-planning]
priority: 2
depends_on: []
batch: overnight-controller
batch_reason: Both units share the controller instructions, run ledger and recovery rules; use sequential edits and one joint recovery trial.
plan: docs/plans/W-010-W-011-controller-reliability.md
---
## Outcome
A release run keeps its umbrella state accurate and resumes from a compact checkpoint after interruption or compaction, without repeating accepted worker attempts or treating deferred human judgments as completed acceptance.

## Why now
Nullsec W-019 stayed proposed through overnight implementation even though its members were activated and integrated. The morning follow-up needed human correction. Two lead compactions were survived, but the run lacked one explicit release/task/result checkpoint contract.

## Constraints
Use existing work pages, plans and `.grove-run/ledger.md`; no new knowledge schema, state database, hook or scheduler. Keep runtime handles local and durable work outcomes on work pages. Do not duplicate full reports into the checkpoint. Human gates can remain pending while independent members proceed. Activation does not imply closure.

## Design
In `skills/work/SKILL.md` and `references/planning.md`, activate the selected umbrella when its first authorized member starts. At member boundaries and before a wait/handoff, record current member/task/attempt, completed and consumed results with tested revision, outstanding worker or command handles and their owners, next action, and pending human judgments. Reuse the same ledger records selected for W-010 rather than a parallel state file.

On resume, compare the checkpoint with Git status, current work state and live worker handles before redispatch. If a process/session restart lost the handles, preserve partial work and reconcile available evidence instead of assuming a worker still exists. Close reconciles release state with member closure and integration evidence; tests never replace a deferred human judgment. Keep the checkpoint short enough to reread routinely.

No hard prerequisite: this can use the existing dispatch ledger independently. W-010 is a shared implementation candidate because its result identities improve the joint recovery trial, not because it must close first.

## Acceptance
- [ ] Instructions activate the release umbrella when member execution begins and update its Next as members finish, while retaining final human gates.
- [ ] The checkpoint contains enough information to locate the current attempt, consumed evidence, live work/owners, pending judgments and next action without loading worker transcripts or full diffs.
- [ ] A fixture with two completed members, one outstanding attempt and a deferred human gate resumes from checkpoint: no completed attempt is dispatched again, outstanding work is reconciled, and the umbrella is active with the human box unchecked.
- [ ] Close/handoff checks umbrella state explicitly; `grove lint` and plugin validation pass, and the fixture result and limitations are recorded.

## Evidence
Shaping source: [nullsec run analysis](../../evidence/2026-09-18-nullsec-overnight-run.md). No implementation performed.

## Next
Apply with W-010 in the shared sequential plan; extend the existing ledger/Next guidance and verify release recovery against the fixture. Independently implementable if batching is inconvenient.
