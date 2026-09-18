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
Yes. `grove:work` runs headless under `grove run` through `scripts/adapters/claude-p.sh` on sonnet, and interruption recovery is real, not "start over": after the driver and agent were killed mid-task, the next invocation marked attempt 1 interrupted, launched attempt 2 in the same worktree, and the agent kept the earlier commit and finished on top of it with no skill change needed. Human-wait, duplicate wake, unchanged wait and success all produced the specified outcomes and exit codes, and the success result reconciled through the new ancestry check while the launched checkout stayed at the exported head.

Gaps found and fixed in this unit: the adapter's prompt split the work id on its dash, so the agent reported `["W","001"]` and the driver refused it (result identity now comes from the contract, never the agent); the CLI tests silently ran git against the real repository when invoked from a git hook (fixture now drops inherited `GIT_*`).

Limits before any multi-hour claim: the adapter needs `--dangerously-skip-permissions`, and Claude Code's own permission classifier refuses to launch it from inside a session, so a human shell or a scheduler must invoke `grove run`. Interrupted and failed attempts both spend the budget; one crash plus one adapter bug used two of three attempts. `grove close` on the branch and `grove reconcile` on the launched checkout both edit the same work page, so the human's merge of the branch will conflict on that page. Only a small unit on one harness was exercised; nothing about hours or codex is known.

## Evidence
- 2026-09-17 interruption (state A, contract 42ad6e8040d0 for W-001): attempt 1 killed with SIGKILL after commit cbc8f3d; attempt 2 receipt: ledger attempt 1 `interrupted`, branch W-001 ends at 57b6ff5 with three commits on top of cbc8f3d, agent closed W-001.
- 2026-09-17 human-wait (state C, contract 02af0176090f for W-002): `attempt 1: waiting`, wait on the owner's greeting word, sources the work page and a question page the agent created; exit 3.
- 2026-09-17 duplicate wake: second `grove run` during attempt 1: `owned (nothing launched)`, exit 4.
- 2026-09-17 unchanged wait: third invocation: `waiting (nothing launched)`, `skipped_waits: 1`, exit 3.
- 2026-09-17 success (state B, contract-1 again): `attempt 1: complete`, tested 57b6ff5 on branch W-001 while the fixture checkout stayed at e5b67bd; `grove reconcile` wrote the evidence block onto the fixture's W-001 page; exit 0.
- Adapter: `scripts/adapters/claude-p.sh`; fixture: `scripts/adapters/make-fixture.sh`.
- 2026-09-17 step 1 at 591de29: `grove run` now accepts a tested revision that descends from the exported head and refuses an unrelated commit; `uv run --extra dev pytest -q tests/` in cli: 118 passed.
- 2026-09-17 step 2: `scripts/adapters/claude-p.sh` written; `scripts/adapters/make-fixture.sh` builds the fixture (W-001 mechanical, W-002 needs a human word). Headless `claude -p --plugin-dir <this repo>` lists all six `grove:*` skills (probe on haiku, max-turns 1).
- 2026-09-17 step 4 not started: the session's permission classifier refused to launch `claude -p --dangerously-skip-permissions` from the adapter, so the runs need a human to start them.

## Next
Close. Later work, if wanted: make `grove reconcile` and a branch-side `grove close` stop editing the same page, and try the same adapter shape on `codex exec` before claiming harness independence.
