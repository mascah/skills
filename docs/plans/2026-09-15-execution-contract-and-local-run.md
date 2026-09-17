# Execution contract and local run ledger (W-002, W-003)

```text
Execution: Single agent; W-002 (contract export/reconcile) then W-003 (local executor) sequentially in one branch.
Reason: W-003 consumes W-002's contract and result shapes and shares cli/grove/contract.py; the design decisions below evolve together and there is no independent deliverable to hand off.
Delegation: None. The interactive agent owns cli/grove, cli/tests, skills/work, references/planning.md and both work pages.
Runtime: Interactive session. No durable executor exists yet; W-003 produces the first one (`grove run`) with a fake adapter only, and it is not used to build itself.
Reassess: None currently identified. If W-003's ledger needs a real harness adapter to prove acceptance, stop and record that as W-004 scope rather than expanding here.
```

Base revision inspected: skills `5c8e04e` (clean), Bench `e39848a` (`~/GitHub/mascah/bench`, clean).

## Specification owners

- W-002 `docs/grove/work/W-002-execution-contract.md`: Outcome, Constraints, Acceptance.
- W-003 `docs/grove/work/W-003-local-run-recovery.md`: Outcome, Constraints, Acceptance.
- Mandate: brief Constraints and [[D-0001-delegated-development]]. Readiness never implies permission; the export records bounds, it grants nothing.

## Bench loop reuse assessment (W-002 acceptance 5, W-003 acceptance 6)

Sources read at Bench `e39848a`: `scripts/bench_loop.py` (1062 lines), `bench_run.py` (899), `bench_worker.py` (315), `bench_models.py`, headers and test names of `bench_control.py`, `bench_exec.py`, `bench_tmux.py`, `test_loop.py`, `test_runs.py`, `test_worker.py`, and `projects/nullsec/out/handoff/main/manifest.json`.

Decision: **extract the execution semantics into a small Grove-owned executor; do not adapt or wrap the Bench runtime.** Bench remains a W-004 comparison candidate for a real harness trial, including its tmux mode.

Why adaptation is not bounded work:

| Bench requirement (source) | Grove situation | Verdict |
|---|---|---|
| `bench_run.contract()` needs a handoff bundle: `manifest.json` schema 1 with six named payload files (`CLAUDE.md`, `SPEC.md`, `GLOSSARY.md`, `DECISIONS.md`, `CONTEXT.md`, `KICKOFF.md`), hashed per-atom `requirements`, and a clean `review.json` from an independent reviewer | Grove has work pages, plans and acceptance lines; no bundle generator (`build_handoff.py`/`handoff.py`/`vault.py` are vault-specific) | Incompatible without porting the generator |
| Run directory fixed at `docs/plan/<release>/runs/<id>` inside the repo, committed by the driver (`Ledger.commit_ledger`) | Grove keeps runtime state out of the knowledge tree and does not auto-commit | Incompatible layout |
| Protocol 3 pipeline: planner seat writes plan JSON, reviewer seat approves, tasks carry `writes` ownership, checks carry argv, verbs `claim/report/submit/review/integrate/verify/complete` | W-003 asks for one owner per attempt plus recovery, not a multi-seat review pipeline | Out of scope |
| `Loop.spawn` hardcodes `bench_worker.py`, which hardcodes `claude -p --output-format stream-json` and role profiles from `bench_models` | W-003 constraint: start with a fake process adapter; harness independence | Incompatible launch path |
| Closure `vault` runs `/bench-debrief` and vault `lint.py`/`readiness.py`; `local` still reads `~/.bench/events.jsonl` through `bench_exec` | Grove reconciles results into work pages via `grove reconcile` | Not reusable |

Semantics extracted (each is a few lines and has a Bench test proving its value):

- One driver per run through a non-blocking `fcntl.flock` on a lock file (`Loop.lock`; `test_two_drivers_cannot_both_take_the_run_before_any_child_exists`).
- Record the attempt before any process exists; store child pid plus `ps lstart` start identity so pid reuse never re-establishes ownership (`bench_worker.start_identity`, `alive`).
- A dead pid with no exit record is `interrupted`; a live one means the attempt is still owned (`Loop.outcome_of`, `reconcile`).
- Bounded attempts with a durable explicit outcome on exhaustion instead of an endless relaunch (`start_work` attempt cap, `decide`).
- Cancellation (SIGTERM) kills the child's process group and records `cancelled` (`bench_worker` KeyboardInterrupt path).
- Atomic state writes via temp file plus `os.replace`.
- Skip unchanged waits without spending a launch (`limit_until`/`wait_limit` shape, generalized to a wait fingerprint).

Remaining coupling: none at runtime. Grove imports nothing from Bench. The contract-to-Bench field mapping below records what an eventual Bench adapter would have to generate.

## Contract to Bench mapping (W-002 acceptance 5)

| Grove contract | Bench equivalent | Adaptation |
|---|---|---|
| `id` = sha256 of canonical JSON without `id` | `manifest.contract_hash` (same construction) | Direct |
| `sources` {path: sha256} | `manifest.files` | Direct; Bench additionally requires the six named files |
| `work[].acceptance[]` with `id`, `text`, `revision` = sha256(text) | `manifest.requirements` {id: {text, revision}} | Direct; Grove ids are `W-NNN:n` |
| `checkout.head` | `state.baseline_commit` | Direct |
| `work[].plan` (path) | protocol-3 plan JSON with tasks/writes/checks | Not derivable; a Bench adapter needs a planner seat or a generated plan |
| `bounds` (brief constraints, decisions) | `CONTEXT.md`, `DECISIONS.md` payload | Would need rendering into named files |
| result `tested.head` | `state.result.commit` | Direct |
| result `evidence[]` | `state.evidence` entries with hashed outputs | Grove records lines, not hashed logs |
| result `findings[]` | `state.intake` | Direct in meaning |
| result `next` | `state.next_action` | Direct |
| result `outcome` (`complete`, `partial`, `waiting`, `blocked`, `failed`) | `state.status` (`active`, `paused`, `complete`) | `waiting`/`blocked` map to `paused` with reason |

## Design

### Contract (W-002)

`grove export <ids...> [--out FILE]` builds one JSON document from a prepared selection. It refuses when `grove batch` reports blockers or missing preparation, and reports why. Fields:

- `schema` 1, `id`, `created`, `project`.
- `checkout`: repo path, `head`, `dirty` paths at export time.
- `order`: dependency order from batch.
- `work[]`: id, page path, outcome, constraints, design, next, scope, depends_on, plan path, `acceptance[]` (`id`, `text`, `revision`, `checked`).
- `bounds`: brief constraints, accepted decisions applying to the scoped capabilities (id and decision line), parent release constraints/acceptance when present.
- `sources`: sha256 of every page and plan the contract was built from (work pages, plans, brief, scoped capabilities, applying decisions, blocking questions).

Result document (written by any executor, interactive or not):

- `schema` 1, `contract` (id), `work` ids, `outcome`, `tested` {head, dirty}, `evidence[]` strings, `findings[]` strings, `next`, optional `wait` {on, sources[]}.

`grove reconcile RESULT --contract FILE`: validates shape, checks the contract file's hash against its `id`, recomputes every `sources` hash and refuses with the changed paths (exit 2) before anything is written, then appends a dated evidence block and replaces Next on each named work page, setting `updated`. It never checks acceptance boxes; that remains the agent's or human's judgment through grove:close.

### Local executor (W-003)

`grove run CONTRACT [--state DIR] [--max-attempts N] [--timeout S] -- ADAPTER...` performs at most one attempt per invocation; a scheduler or a person re-invokes it. State lives in `.grove/runs/<contract id prefix>/` by default: `ledger.json`, `driver.lock`, `attempts/<n>/result.json`. The adapter receives the contract path and attempt directory as its last two arguments and must write `result.json` there. Tests use small Python adapters as the fake process.

Per invocation:

1. Take the driver lock; exit 4 if held.
2. Reconcile: an attempt with a live recorded pid and identity is still owned, exit 4; a dead pid without a result is recorded `interrupted` together with the checkout head and dirty paths inspected now. Partial files are never touched.
3. Terminal ledger outcomes (`complete`, `cancelled`, `exhausted`) print and exit without launching.
4. A last `waiting` result is fingerprinted from its `wait.sources` (or the contract sources); an unchanged fingerprint exits 3 with no launch and a counted skip.
5. Attempt count at `max-attempts` records `exhausted`, exit 5.
6. Record the attempt (owner pid, driver identity), spawn the adapter in its own session, record child pid and start identity, wait with the timeout. SIGTERM/SIGINT kill the process group and record `cancelled`. No result file records `failed`; a result records its outcome and is validated against the contract id.

Exit codes: 0 complete, 1 failed/partial/blocked, 2 error, 3 waiting, 4 owned elsewhere, 5 exhausted, 6 cancelled.

## Steps

1. W-002 tests first in `cli/tests/test_contract.py`: export names work, sources, checkout, acceptance revisions and refuses unprepared selections; result validation; stale-source refusal before write; reconcile appends evidence and Next; the same contract accepted from the CLI path and from an in-process fake executor. Fixture repos get `git init` in a helper.
2. Implement `cli/grove/contract.py` and wire `export`/`reconcile` in `cli.py`.
3. W-003 tests first in `cli/tests/test_run.py`: duplicate driver refused with unchanged ledger; live foreign child refused; dead child recorded interrupted with checkout inspection and partial file intact; retry exhaustion and cancellation durable; unchanged wait spends no launch and a changed wait does; result carries contract id and reconciles.
4. Implement `cli/grove/run.py` and wire `run` in `cli.py`.
5. Update `skills/work/SKILL.md` and `references/planning.md` so the interactive caller uses export/reconcile for handoff and names `grove run` as the local executor with only a fake adapter demonstrated.
6. Full suite, `grove lint`, review the diff against both specifications, record evidence per unit, close W-002 then W-003 with grove:close.

## Joint verification

- The W-003 fake-adapter run produces a result that `grove reconcile` accepts against the exported contract (shared identity, W-002 acceptance 4 and W-003 acceptance 5).
- An edited source page between export and reconcile is refused by reconcile after a `grove run` (W-002 acceptance 3 across the executor boundary).

## Joint verification result

Recorded 2026-09-15 on the working tree based on `618c6c9` (W-002 closed):

- `cli/tests/test_run.py::test_complete_result_carries_contract_identity_and_reconciles`: the fake-adapter result carries the contract id and `grove reconcile` writes it onto the work page.
- Real repository: `grove export W-003` produced contract e37548baf9e6; `grove run` with a scratch waiting adapter launched once (exit 3), skipped the unchanged wait on the second invocation (exit 3, nothing launched, `skipped_waits` 1, pid and start identity recorded); `grove reconcile` accepted the result once, and the second reconcile of the same result was refused with exit 2 because that write changed the W-003 page.

## Risks

- `ps -o lstart` output format differs across platforms; identity is compared as an opaque string produced by the same host, which is what Bench relies on.
- Unattended reliability is not claimed; only the fake adapter is exercised. W-004 evaluates a real harness.

## On interruption

Check `git status`, run the suite, and read the Evidence and Next of each work page. Steps completed are recorded there; unchanged evidence stays attributed to its tested revision.
