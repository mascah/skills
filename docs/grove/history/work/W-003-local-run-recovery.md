---
type: work
id: W-003
status: done
started: 2026-09-15
created: 2026-09-15
updated: 2026-09-15
kind: feature
size: bounded
scope: [autonomous-execution]
priority: 1
depends_on: [W-002]
batch: executor-foundation
plan: docs/plans/2026-09-15-execution-contract-and-local-run.md
batch_reason: Contract export and the local ledger share result identity and should be planned together, with contract implementation first.
---
## Outcome
An optional local executor records one owner per attempt, durable progress and bounded recovery against the exported work contract.

## Why now
Reliable interruption and duplicate-wake behavior must exist before testing multi-hour autonomous execution.

## Constraints
One scheduling authority, preserve partial work, enforce bounds, and skip unchanged waits. Start with a fake process adapter; tmux remains optional visibility.

## Design
Evaluate adapting the existing Bench loop before designing new ownership/recovery machinery. Inspect `~/GitHub/mascah/bench/scripts/bench_loop.py` together with `bench_worker.py`, `bench_run.py`, `bench_control.py`, `bench_exec.py`, `bench_models.py`, `bench_tmux.py`, and their relevant tests. Compare retaining the runtime behind a Grove adapter, extracting a smaller executor, and implementing only demonstrated gaps.

The loop already orchestrates planning, work, review, integration, verification and closure; persists attempts and child outcomes; reconciles interrupted processes/worktrees; and supports both tmux and plain subprocesses. Its current launch path, role adapters, ledger protocol and vault closure are Bench/Claude-specific. Evaluate `closure: local` as an adaptation point, and preserve tmux's operator visibility where useful. Source inspection establishes candidate behavior, not proven compatibility with Grove.

Make the reuse decision during joint W-002/W-003 planning, before implementing a replacement. Implement after W-002 in the same planned implementation if the boundaries remain bounded.

## Acceptance
- [x] Duplicate dispatch cannot create two owners for the same attempt.
- [x] Interruption preserves partial work and resumes after inspecting actual process/checkout state.
- [x] Retry exhaustion and cancellation produce durable explicit outcomes.
- [x] Unchanged human waits spend no agent call.
- [x] Evidence/results retain the W-002 contract identity.
- [x] A recorded reuse assessment explains whether the existing Bench loop is adapted, extracted, or replaced, with source/test evidence and remaining coupling.

## Next
Close; W-004 chooses the first real harness adapter trial against this executor.

## Evidence
Verified on the implementation working tree based on 618c6c94b307 (W-002 closed), Bench read at e39848a:
- Acceptance 1-5: `cli/.venv/bin/python -m pytest cli/tests -q` — 117 passed (11 new in `cli/tests/test_run.py`, observed failing before `cli/grove/run.py` existed or before each review fix). Cases: a held driver lock refuses a second driver and leaves no ledger; a recorded attempt whose pid and start identity are still alive is refused as owned, and after that process dies the next invocation records it interrupted with the dirty checkout inspected and the partial file intact, then launches attempt 2; two failing attempts at `--max-attempts 2` record `exhausted` durably and a third invocation launches nothing; a 0.3s timeout kills the child and records the failure; SIGTERM to a CLI driver kills the sleeping adapter and exits 6 with `cancelled` in the ledger; a waiting result is skipped on the next invocation with no launch, and editing the named question page wakes it; the fake adapter's result carries the contract id and reconciles onto the work page.
- Acceptance 6: reuse assessment with source and test evidence in the shared plan and the autonomous-execution capability page: semantics extracted, no Bench code shared, adaptation rejected for bundle, run-directory, seat-pipeline and launch coupling.
- Real repository round trip (contract e37548baf9e6 on 618c6c94b307): run launched once, skipped the unchanged wait, reconciled once, and the same result was refused after the page changed. The earlier waiting block this wrote here was replaced by this evidence.
- Independent review (reviewer agent, read-only, reproduced each finding): six defects fixed with regression tests: the adapter could start before its pid was durable (now a launch gate holds the child until pid and start identity are written, and a missing identity fails the attempt without running anything); the owned path crashed the CLI instead of exiting 4; waiting attempts spent the attempt budget so a satisfied wait could never be served; a result could claim a tested revision the checkout never had (now failed against the inspected head); wait sources could point outside the repository. Recorded limit: ledger writes do not fsync, so durability covers process death, not power loss.
- `grove lint` — 0 errors, 0 warnings.
