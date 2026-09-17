# Implementer brief template

The lead fills this in per task and dispatches a fresh implementer with the Agent tool (`model: sonnet`; `model: opus` on fix-loop rounds 4-5), prompt equal to the brief's file path.

```text
# Task brief: <work id>/<task>

Worktree: <path> (branch <branch>, base <base revision>). Work only there. Do not commit.

## Task
<What to change, in the implementer's own files: the behavior wanted, files to touch, interfaces to keep stable. No more than the task needs.>

## Acceptance line served
<The one acceptance line from the work page this task proves.>

## Rules
- Work only inside the named worktree; never touch main or another worktree.
- Write the failing test first wherever the change has logic — a branch, loop, parser, or state transition — per discipline.md; a one-line change with no logic needs no new test.
- Debugging: one hypothesis at a time. Reproduce, read the code path, form one hypothesis, test it alone, fix at the root. Stop and report after three failed hypotheses instead of stacking further guesses.
- Do not commit.
- Do not touch files outside this task's scope.

## Report format
Write the report to `.grove-run/<task>-report.md` and repeat it as your final message.

contract: <work id>/<task>
work: <work id>
outcome: done | blocked | waiting
tested revision: <git rev-parse HEAD> (uncommitted diff against <base>)
evidence:
- <command>: <result>
findings:
- <anything the reviewer or lead must know; empty if none>
next: <one line>
```
