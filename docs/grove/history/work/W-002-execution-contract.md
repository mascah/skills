---
type: work
id: W-002
status: done
started: 2026-09-15
created: 2026-09-15
updated: 2026-09-15
kind: feature
size: bounded
scope: [autonomous-execution, knowledge-context]
unchanged: [knowledge-context]
priority: 1
depends_on: [W-001]
batch: executor-foundation
plan: docs/plans/2026-09-15-execution-contract-and-local-run.md
batch_reason: Contract export and the local ledger share result identity and should be planned together, with contract implementation first.
---
## Outcome
A prepared selection can be exported as a versioned execution input, and its result can be reconciled without relying on chat memory.

## Why now
The new work map and preparation handoff define what an optional executor must consume.

## Constraints
Keep the core harness-independent. Preserve exact source/checkout identity, acceptance and delegated bounds; do not infer permission from readiness.

## Design
Inspect Bench's frozen contracts and the actual input/result expectations of `~/GitHub/mascah/bench/scripts/bench_loop.py`, alongside Symphony's work/attempt boundary. Treat the Bench loop as an executor candidate, not only a source of individual patterns. Specify the smallest input/result shapes, change detection and reconciliation behavior before implementing export.

## Acceptance
- [x] Export names selected work, source revisions, checkout, constraints, plans and acceptance.
- [x] Result identifies tested revision, evidence, unresolved findings and next action.
- [x] Changed inputs are detected before a stale result is accepted.
- [x] One interactive caller and a fake executor exercise the same contract.
- [x] The contract maps explicitly to the Bench loop's inputs/results, with required adaptation or incompatibilities recorded.

## Evidence
Verified on the implementation working tree based on 5c8e04e2ac95 (skills), Bench read at e39848a:
- Acceptance 1-4: `cli/.venv/bin/python -m pytest cli/tests -q` — 106 passed (6 new in `cli/tests/test_contract.py`, each observed failing before `cli/grove/contract.py` existed). Cases: unprepared selection refused (blocking question, missing plan); export names order, checkout head/dirty, plan path, per-line acceptance revisions, page/plan/brief/capability sources, brief constraints and applying decisions, id equals the canonical hash; result validation rejects wrong contract, outcome, work and tested; a changed page or plan is refused with its path before any evidence is written; reconcile appends the run block and replaces Next on every named unit and checks no boxes; the CLI caller and an in-process fake executor both go through export → result → reconcile, and the same result is refused with exit 2 after the plan changes.
- Acceptance 5: Bench reuse assessment and field mapping recorded in the shared plan and the autonomous-execution capability page.
- Real use: `grove export W-002 W-003 --out …` on this repository produced contract 2723af3380a2 naming both units, the shared plan, brief, two capabilities and D-0001.
- `grove lint` — 0 errors, 0 warnings.

## Next
Close; W-003 implements the local executor against this contract.
