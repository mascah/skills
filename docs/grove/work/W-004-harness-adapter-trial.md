---
type: work
id: W-004
status: active
started: 2026-09-17
created: 2026-09-15
updated: 2026-09-17
kind: spike
size: spike
scope: [autonomous-execution]
priority: 2
depends_on: [W-003]
---
## Question
Does `grove:work` survive being run headless by `grove run` through a `claude -p` adapter that owns the workspace, including interruption recovery, so the contract and ledger are exercised by a real harness?

## Bounds
One isolated fixture project with one small exported work unit. The adapter is a shell script; no new CLI machinery beyond the tested-revision check. `claude -p` is the only installed harness besides `codex`; Hermes, OpenClaw, Symphony and OpenCode are not on this machine and are out of bounds. The unattended run bypasses permissions only inside the fixture checkout. No recurring schedule, no external publication, no multi-hour run: record actual limits first.

## Plan
1. Change `grove run` so the tested-revision check accepts any revision that descends from the exported checkout head (`git merge-base --is-ancestor`), keeping the refusal for unrelated or missing revisions; extend `cli/tests/test_run.py` with a branch-commit case (settled, see [[autonomous-execution]] design notes).
2. Write `scripts/adapters/claude-p.sh` (path may move): given the contract path and attempt directory, create a worktree and branch from the exported head, launch `claude -p` inside it with a prompt naming the contract, the attempt directory and the headless rules (no questions: write a `waiting` result naming the paths waited on; on completion write `result.json` there), then read the branch head into `tested.head` and the fixture's test command output into evidence if the agent omitted them.
3. Build the fixture: a tiny repo with grove initialised, one small prepared work unit, `grove export` to a contract.
4. Run the cases in this order and record each in Evidence: interruption (kill the child mid-task, re-invoke, confirm the second attempt resumes in the existing worktree per discipline.md rather than starting over), human-wait (a unit whose plan needs a human choice; confirm a `waiting` result and an unchanged-fingerprint no-op relaunch), duplicate wake (second `grove run` while the first lives exits 4), success (result reconciles onto the work page).
5. Disposition names the gaps found in the skill prose or driver, and whether interruption recovery is real or "start over".

## Disposition

## Evidence
- 2026-09-17 step 1 at 591de29: `grove run` now accepts a tested revision that descends from the exported head and refuses an unrelated commit; `uv run --extra dev pytest -q tests/` in cli: 118 passed.
- 2026-09-17 step 2: `scripts/adapters/claude-p.sh` written; `scripts/adapters/make-fixture.sh` builds the fixture (W-001 mechanical, W-002 needs a human word). Headless `claude -p --plugin-dir <this repo>` lists all six `grove:*` skills (probe on haiku, max-turns 1).
- 2026-09-17 step 4 not started: the session's permission classifier refused to launch `claude -p --dangerously-skip-permissions` from the adapter, so the runs need a human to start them.

## Next
Human runs the interruption case: build the fixture with `scripts/adapters/make-fixture.sh DIR`, `grove export W-001 --out c1.json` there, then from DIR `GROVE_TEST_CMD=./test.sh GROVE_PLUGIN_DIR=<this repo> uv run --project <this repo>/cli grove run c1.json --state STATE -- <this repo>/scripts/adapters/claude-p.sh`; once `.worktrees/W-001/hello.sh` appears, `kill -9` the driver and the adapter's process group (pid in STATE/ledger.json), re-run the same command, and record whether attempt 2 resumes on the existing branch. Then human-wait with W-002, duplicate wake, success, and write Disposition.
