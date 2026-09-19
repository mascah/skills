---
type: work
id: W-011
status: done
created: 2026-09-18
started: 2026-09-18
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
A work run resumes from a compact checkpoint after interruption or compaction, whether it covers one work unit, a batch or a release. It preserves current work state, accepted results, outstanding activity and pending human judgments without repeating completed steps. Release umbrella state is tracked only when a release is in scope.

## Why now
The nullsec overnight run survived two lead compactions but lacked one explicit work/task/result checkpoint contract. Its W-019 umbrella also stayed proposed through member implementation and needed human correction. That release-specific symptom exposed a general work-run recovery gap; a run need not belong to a release.

## Constraints
Use existing work pages, plans and `.grove-run/ledger.md`; no new knowledge schema, state database, hook or scheduler. Keep runtime handles local and durable work outcomes on work pages. Do not duplicate full reports into the checkpoint. Scale to the run: small single-agent work can use its existing Next/evidence without creating a worker ledger. Do not require a release, invent an umbrella or add member fields to standalone work. Human gates can remain pending while independent work proceeds. Activation does not imply closure.

## Design
In `skills/work/SKILL.md` and `references/planning.md`, keep each selected work unit's state current. At meaningful task/work boundaries and before a wait/handoff, record selected work IDs, current step and task/attempt when present, completed steps and consumed results with tested revision, outstanding worker or command handles and their owners when present, next action, and pending human judgments. Reuse existing Next/evidence and the same ledger records selected for W-010 rather than a parallel state file. Only when the run belongs to a release, also activate its umbrella when the first authorized member starts and track member progress against release acceptance.

On resume, compare the checkpoint with Git status, current work state and any live worker handles before repeating steps or redispatching. If a process/session restart lost the handles, preserve partial work and reconcile available evidence instead of assuming a worker still exists. Close reconciles the selected work with its acceptance and evidence; for a release it additionally reconciles member closure and integration acceptance. Tests never replace a deferred human judgment. Keep the checkpoint short enough to reread routinely.

No hard prerequisite: this can use the existing dispatch ledger independently. W-010 is a shared implementation candidate because its result identities improve the joint recovery trial, not because it must close first.

## Acceptance
- [x] Instructions cover standalone work, a batch without a release, and release members. Each keeps its own work state and Next current; only the release case activates and updates an umbrella.
- [x] The checkpoint contains enough information to locate the current attempt, consumed evidence, live work/owners, pending judgments and next action without loading worker transcripts or full diffs.
- [x] Recovery scenarios cover standalone work, a batch and a release with completed steps, outstanding activity and a deferred human gate: no completed step or accepted attempt is repeated, outstanding work is reconciled, and human boxes remain unchecked. Standalone/batch scenarios require no umbrella; the release scenario keeps its umbrella active.
- [x] Small single-agent work uses existing Next/evidence without a worker ledger. Close/handoff checks selected work state and any applicable umbrella state; `grove lint` and plugin validation pass, with scenario results and limitations recorded.

## Evidence
Shaping source: [nullsec run analysis](../../evidence/2026-09-18-nullsec-overnight-run.md). No implementation performed.

- 2026-09-18 T1 (SKILL.md checkpoint/scale/resume sentences, close/SKILL.md steps 4 and 7, planning.md one-sentence pointer), base 78462ae, small work run as one dispatched implementer Agent `model: sonnet`; task reviewer `model: opus` accept, 0 blocking, 6 minor (two wording items folded into the W-012 dispatch). Implementer evidence: `grove lint` 0 errors, `claude plugin validate .` passed. Recorded replay (not runtime), five scenarios in the run's `.grove-run/W-011-scenarios.md`: (a) standalone bounded unit, (b) batch without a release, (c) release with one closed member and an active umbrella, (d) small single-agent work from Next/Evidence alone, (e) handles lost after a process restart. Reviewer traced every decision to a sentence in the final text: no completed step or consumed attempt repeated, outstanding attempt resumed or recorded as interrupted before a new attempt, human boxes unchecked in all five, umbrella touched only in (c). Runtime evidence for the same rules: this run's own lead resumed dispatched workers by handle and consumed each attempt once (see W-010 evidence). Limitation: no lead compaction occurred during this run, so checkpoint recovery after compaction is shown by replay only.
- 2026-09-18 cold checkpoint read (verification worker Agent `model: sonnet`, named by the whole-branch review for transition "resume from ledger + Next"), at e915c20: from `.grove-run/ledger.md`, the work pages' status and Next, `git log` and `git status` alone, with no report, review or transcript, the worker reconstructed the selected order, open attempts, every attempt's verdict and tested revision, outstanding handles, pending human items and the next action; nothing needed a report file. Two lessons recorded: a ledger line that was later corrected reads as a false positive in isolation (write the correction on the line's own subject, or mark it), and stale pre-implementation Next text misleads a cold reader, which is why close rewrites Next.

## Next
None for this unit; checkpoint and resume rules are in place. Record the first real lead compaction recovery in work-planning when one happens.
