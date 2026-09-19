---
type: work
id: W-010
status: done
created: 2026-09-18
started: 2026-09-18
updated: 2026-09-18
kind: fix
size: bounded
scope: [work-planning]
priority: 1
depends_on: []
batch: overnight-controller
batch_reason: Both units share the controller instructions, run ledger and recovery rules; use sequential edits and one joint recovery trial.
plan: docs/plans/W-010-W-011-controller-reliability.md
---
## Outcome
Grove's controller consumes each worker attempt once, receives a compact result reference instead of repeated full reports, and can distinguish completed, blocked and still-running work without empty notification polling or abandoned background commands. It uses ordinary subagents rather than teammates for this workflow.

## Why now
The nullsec overnight run delivered 51 distinct idle events plus 18 explicit teammate messages, made 33 empty notification reads, and repeated its final handoff after ten delayed idle events. A fixer and replacement also went idle without collecting background checks. These are the first reliability fixes selected from the run; compaction tuning is deferred. [[D-0002-controller-loop-execution]]

## Constraints
- Instruction and prompt-template changes; no new scheduler, daemon, mailbox transport, or CLI result-schema change. Keep runtime state in the existing gitignored `.grove-run/` ledger and reports.
- User direction, 2026-09-18: instruct the agent not to use teammates and to prefer ordinary subagents; leave the agent-teams flag and user configuration unchanged. Do not silently select a team when the harness cannot honor that instruction; record the limitation and reassess within authority.
- Preserve explicit model selection, review independence, bounded fix rounds and lead ownership. Use the harness's supported subagent continuation mechanism, not an assumed teammate messaging API.
- Report provenance remains attributable to task, attempt and tested checkout. An idle event is not proof of acceptance. Legitimate new attempts and unresolved failures must not be suppressed as duplicates.

## Design
Update `skills/work/SKILL.md`, `skills/work/implementer.md`, `skills/work/reviewer.md`, `references/planning.md` and `references/discipline.md` together.

Keep the full report on disk; the ordinary completion return contains only task/attempt identity, outcome or verdict, tested revision/checkout and report path, plus a concise blocker if applicable. No extra SendMessage repeating completion. Reserve messages for actionable blockers or coordination. Record accepted attempt/report identity in the existing ledger; a late notification for the same consumed result causes no redispatch, report reread or repeated user handoff. A later fix attempt has a distinct identity and is consumed normally. Prefer attempt-specific report paths so an old result cannot be mistaken for a fresh fix.

Workers own launched checks until the exit status/output is collected. Prefer foreground checks. If the harness yields a running command, keep its handle and use the supported completion mechanism; do not finish with an unsupported promise to wake later. An actual handoff of waiting work records the handle, owner, evidence path and wake condition. The controller uses one supported wait mechanism for each outstanding attempt, and investigates an idle worker without a terminal report rather than indefinitely waiting for file existence. Replacement cannot leave two writers or two test owners on the same task; reconcile or stop the old attempt first.

Instructions must select the ordinary-subagent dispatch path and verify the returned type/handle on the first trial. In Claude Code, naming a dispatch can turn it into a teammate when teams are enabled; do not rely on the phrase "no teams" while using such arguments. Revalidate dispatch and resume capabilities at execution. Keep harness-specific details small and explicit.

Alternatives: keep teams and deduplicate only at the lead (leaves worker lifecycle overhead); disable teams globally (user deferred); add a transport deduplicator or supervisor (premature runtime scope). Reconsider instruction-only control if the bounded trial cannot demonstrate the required behavior.

## Acceptance
- [x] Implementer, reviewer and controller instructions agree on file-backed reports and compact returns, with no redundant completion SendMessage or full-report repetition.
- [x] A bounded ordinary-subagent trial records actual dispatch type and continuation handles with the agent-teams setting unchanged; an implement/review/fix sequence preserves model and review rules without teammates.
- [x] Replay a consumed result and a late idle notice: neither advances the task again nor repeats the handoff. Deliver a new fix-attempt result: it is processed once. Missing or mismatched report identity is investigated, not accepted.
- [x] Exercise a delayed command and an idle worker without a report: output/exit status is collected or an explicit owned wait is recorded, with one wait mechanism and no competing replacement writer. No empty notification-poll loop is used.
- [x] Record trial revision, scenarios, actual calls/results and limitations; `grove lint` and plugin validation pass. Reconcile work-planning behavior only after implementation.

## Evidence
Shaping source: [nullsec run analysis](../../evidence/2026-09-18-nullsec-overnight-run.md). No implementation or runtime trial performed during shaping.

- 2026-09-18 T1 (SKILL.md, implementer.md, reviewer.md, planning.md, discipline.md), base 82d4b16: implementer Agent `model: sonnet` (named ordinary subagent; harness returned `<name>@session` id resumable with SendMessage, agent-teams setting untouched); task reviewer `model: opus` a1 verdict fix (1 blocking: reviewer template paths not attempt-numbered; 2 minor); fix round 1 resumed the same sonnet implementer (a2); scoped re-review resumed the same opus reviewer: accept. 1 fix round. Implementer evidence: `grove lint` 0 errors, `claude plugin validate .` passed. Runtime observations during this run: the implementer's compact return arrived as a harness message and was consumed once; a later idle_notification for the same consumed attempt caused no redispatch, reread or handoff (ledger line kept); the reviewer's return also arrived once plus one idle duplicate, ignored. Topology fact: although every dispatch was an ordinary Agent-tool subagent with an explicit model and no team was created, the harness presented the named workers as a team roster to each other and labelled their returns as teammate messages; the agent-teams setting was not changed, and instructions therefore rely on the dispatch call and handle, not on the harness's labels.
- 2026-09-18 T3 trial, revision 78462ae, trial worker Agent `model: sonnet` (no task reviewer; the whole-branch review covers it). Runtime: `sleep 4 && echo delayed-ok` in the foreground returned `delayed-ok`, exit 0, collected before reporting; `pytest -q cli/tests/test_launch.py` 7 passed; the Bash tool ran both synchronously, so no running-handle decision point occurred. Recorded replay (not runtime), table in the run's `.grove-run/W-010-trial.md`: duplicate completion and late idle notice for a consumed attempt → 0 dispatches, 0 rereads, 0 handoffs; new fix-attempt return with report → consumed once; return with missing report or unmatched contract → investigated, not accepted; idle worker without report → resumed once, not replaced; `outcome: waiting` report → one wait on that worker; replacement while owned → refused until reconciled; every row cites its deciding sentence in `skills/work/SKILL.md`. Harness facts from this run's ledger: Agent tool dispatches with explicit model returned resumable ids (`<name>@session`), returns arrived as harness messages, one real late idle notification for a consumed attempt was ignored. Limitation: the `outcome: waiting` handoff and the empty-poll avoidance are shown by replay and by this run's own controller behavior, not by a forced background command; teams setting untouched.

## Next
None for this unit; the controller rules are in place. The `outcome: waiting` handoff path is shown by replay only; record the first runtime occurrence in work-planning when a run hits it.
