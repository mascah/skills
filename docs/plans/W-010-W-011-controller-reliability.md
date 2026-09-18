# W-010 + W-011 — reliable worker results and work-run recovery

Execution: One controller, sequential implementation tasks; ordinary subagents, no teammates.
Reason: Both units edit the work skill, planning guidance and existing run ledger contract. Separate simultaneous writers would compete on those interfaces.
Delegation: Focused implementer and independent reviewer per task, using existing explicit model rules. The lead owns work pages, checkpoints, evidence and closure.
Runtime: Interactive harness; verify ordinary-subagent dispatch and continuation before the first implementation worker. No settings changes and no claim of a new durable executor.
Reassess: If this harness cannot avoid teammates or return/resume a worker through supported handles, record the limitation and adapt within the mandate; do not silently change the flag, select a team or fabricate a successful trial.

Inspected base: `edab734` on 2026-09-18. This is a shaping plan, not implementation evidence. Revalidate against the checkout when starting, especially if W-009 has changed discipline guidance.

`grove batch W-010 W-011` on 2026-09-18 reports prepared, no external blockers, shared scope work-planning, and order W-010 then W-011. The file ownership inspection above selects sequential writes despite the lack of a hard prerequisite edge.

## Ownership and order

- T1, W-010: `skills/work/SKILL.md`, `skills/work/implementer.md`, `skills/work/reviewer.md`, `references/planning.md`, `references/discipline.md`. Select the actual ordinary-subagent dispatch/continuation path; replace repeated full reports with compact returns and file-backed result identity; define ownership of commands, waiting, consumed results and replacement attempts. Preserve models, fix bounds and review independence. Do not introduce a new CLI contract schema.
- T2, W-011: after T1's edits, the same single owner updates `skills/work/SKILL.md`, `references/planning.md` and `skills/close/SKILL.md`. Add compact checkpoint/recovery rules for standalone work, batches and releases using the ledger vocabulary T1 just established. Small single-agent work keeps its checkpoint in existing Next/evidence; umbrella activation and member tracking apply only to releases. This ordering avoids conflicting instructions; neither unit has a closure prerequisite on the other.
- T3, joint verification: one bounded fixture/trial using the final instructions. Record each work's acceptance separately, then one final consistency review and reconciliation of the work-planning capability. Close independently proven units in implementation order.

W-012 also touches review guidance but can follow in a separate change. W-009 shares discipline.md only; no concurrent edits to it. W-007's eval runner is not a prerequisite: use a small fixture and recorded transcript, not a new test framework. If W-007 supplies a suitable runner by then, reuse it.

## Trial and checks

Prepare a throwaway standalone-work fixture with completed steps, one outstanding task, and one deferred human judgment. Use a trivial reversible implementation and independent review, including a requested fix round; limit the runtime trial to those roles and one recovery exercise. Replay checkpoint variants for a batch without a release and for a release with completed members; do not run the implementation trial three times. Capture actual dispatch type, model, returned handles and continuation behavior with the agent-teams flag untouched. A named worker label is not proof of topology.

Verify these outcomes before claiming acceptance:

1. Reports stay on disk; completion returns identify task/attempt/revision/path without repeating the full report. There is no extra completion SendMessage.
2. Replay the same consumed result and a late idle event through the controller's scenario input: zero new dispatches, zero re-acceptances and no repeated handoff. A new fix-attempt result is consumed exactly once. Missing or stale identity cannot satisfy completion.
3. Delay a small command and capture its exit status. Exercise an idle worker without a report: resume/reconcile it through supported mechanisms, or record an explicit waiting owner/handle. Do not start a replacement while the old attempt can still write or own the same test. No empty queue-poll loop or duplicate watcher.
4. Resume the controller from checkpoint after a context reset: it identifies completed and outstanding work without worker-transcript archaeology and preserves the deferred human gate. Replay standalone, batch and release variants: no umbrella is needed for the first two; only the release variant tracks an active umbrella and member acceptance. Walk through small single-agent work using Next/evidence without a worker ledger, and lost runtime handles after a process restart; do not claim a simulated context reset proves crash recovery.

Use runtime evidence for dispatch/completion behavior and a recorded scenario replay for duplicate suppression and checkpoint decisions; label the distinction. Do not assert prompt wording alone guarantees behavior. Keep the trial bounded; failure records a limitation and reassessment, not endless retries.

Run `grove lint`, plugin validation and the repository's commit hooks. No new tests that merely assert prose strings. No compaction-threshold experiment in this work. Keep implementation artifacts under `.grove-run/`, but summarize trial revision, calls, outcomes and limitations in each work's Evidence so closure does not depend on an untracked file surviving.

## Recovery

On interruption load each work's context, this plan and the latest ledger checkpoint. Inspect Git status and live work ownership; resume the first unaccepted task. Keep existing evidence attributable to its tested checkout. A late notification alone cannot reopen accepted work.
