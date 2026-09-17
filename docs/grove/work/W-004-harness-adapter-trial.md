---
type: work
id: W-004
status: proposed
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

## Next
Start at plan step 1 in a worktree branch; the ancestry check is settled and does not need discussion.
