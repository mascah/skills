---
type: capability
id: autonomous-execution
status: draft
updated: 2026-09-17
---
## Behavior
`grove export <ids>` turns a prepared selection into a versioned contract (schema 1): dependency order, checkout head and dirty paths, each unit's outcome, constraints, design, plan path and acceptance lines with per-line revisions, the bounds (brief constraints, accepted decisions applying to the scope, parent release contracts), and a sha256 for every page and plan it was built from. Its `id` is the hash of the canonical content, so an edited contract file is refused. Export refuses blocked or unprepared selections; it records readiness as fact and grants no permission.

A result document names the contract id, work ids, outcome (`complete`, `partial`, `waiting`, `blocked`, `failed`), tested revision, evidence lines, unresolved findings and next action; a waiting result names what it waits on. `grove reconcile` validates the result, recomputes every exported source hash and refuses with the changed paths before writing anything, then appends a dated evidence block and replaces Next on each named work page. It never checks acceptance boxes. The same contract is exercised by the interactive `grove:work` caller and by a non-interactive executor.

`grove run CONTRACT [--state DIR] [--max-attempts N] [--timeout S] -- ADAPTER...` is the optional local executor. It performs at most one attempt per invocation; a scheduler or a person re-invokes it. One driver owns a run through a non-blocking lock; the attempt record exists before its process does and stores the child's pid and start identity, so a later invocation refuses while that process lives and otherwise records the attempt as interrupted with the checkout head and dirty paths it inspected, never touching partial files. The adapter is any command given the contract path and an attempt directory; it must write a result there, which is validated against the contract id. A `waiting` result is fingerprinted from the paths it names, and an unchanged fingerprint exits without launching anything. Attempts are bounded; exhaustion, cancellation on SIGTERM/SIGINT, timeouts and missing results are durable outcomes in `ledger.json`. Exit codes: 0 complete, 1 failed/partial/blocked, 3 waiting, 4 owned elsewhere, 5 exhausted, 6 cancelled.

The suite does not schedule work; scheduling belongs to whatever re-invokes `grove run`. Only a fake process adapter has been exercised. Harness registration makes skills discoverable; it does not establish runtime compatibility.

## Acceptance
- [x] W-002 exports a versioned prepared-work contract with attributable results.
- [x] W-003 provides a local run ledger and tested interrupted-run recovery.
- [ ] W-004 evaluates a real harness adapter before multi-hour operation is claimed.

## Design notes
Keep the executor optional. One authority owns scheduling and each attempt. The executor extracts Bench loop semantics (driver lock, record-before-launch, pid plus start identity, dead-without-result means interrupted, bounded attempts, atomic state writes) and shares no code with Bench; W-003 recorded that adapting the Bench runtime was not bounded because of its bundle, run-directory, seat-pipeline and `claude -p` coupling. The driver's tested-revision check must accept any revision that descends from the exported checkout head (`git merge-base --is-ancestor`), not only the head of the checkout it was launched in: `grove:work` commits on a worktree branch and leaves the launched checkout untouched, so strict equality fails every honest headless completion. Settled with the user 2026-09-17 during W-004 exploration; W-004 makes the change. Leaning from the same exploration: the first real adapter owns the workspace (creates the worktree and branch from the exported head, runs the agent inside it, reads the branch head and test output into the result) and the agent keeps task dispatch, so `grove:work` must not nest a second worktree when launched inside one. The user wants the option, later, to hoist dispatch out of the skill so different stages can run on different harnesses (for example opencode with a local model); the per-task result shape from W-006 is what keeps that open. That is D-0002's reconsider condition, not current work. Interrupted attempts count toward the attempt budget; split an infrastructure budget out only if a real harness shows interruptions dominate. The existing `~/GitHub/mascah/bench/scripts/bench_loop.py` is an explicit executor candidate alongside Symphony and harness-native approaches. Evaluate adapting it during W-002/W-003 planning before choosing new runtime machinery. Its supervisor, worker wrapper and ledger supply execution semantics; tmux supplies optional operator visibility. Candidate status does not imply a selected or tested Grove integration. [[D-0001-delegated-development]]

W-002 planning assessed the Bench loop at Bench `e39848a`: its ledger needs a handoff bundle with six named payload files and a reviewed manifest, a run directory committed under `docs/plan/<release>/runs`, a planner/reviewer seat pipeline, and a `claude -p` launch path; none of that is bounded to adapt for a Grove contract. The contract-to-Bench field mapping (contract id, sources, acceptance revisions, checkout head, result fields) is recorded in the shared plan `docs/superpowers/plans/2026-09-15-execution-contract-and-local-run.md`.

## Code
- cli/grove/contract.py
- cli/grove/run.py
- cli/tests/test_contract.py
- cli/tests/test_run.py
- skills/work/SKILL.md
- references/planning.md
