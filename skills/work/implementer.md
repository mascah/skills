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
- Run checks in the foreground and collect exit status and output yourself before reporting. If the harness leaves a command running, keep the handle and wait for its completion notification; never finish with a promise to wake later. If a check must genuinely be handed off still running, report `outcome: waiting` and name the command, that you own it, the evidence path you will write, and the wake condition.

## Report format
Write the full report to `.grove-run/<task>-a<N>-report.md`. Your final message is a compact return only, never the full report, and send no extra SendMessage announcing completion.

Full report, written to the file:

contract: <work id>/<task>
work: <work id>
attempt: a<N>
outcome: done | blocked | waiting
tested revision: <git rev-parse HEAD> (uncommitted diff against <base>)
evidence:
- <command>: <result>
findings:
- <anything the reviewer or lead must know; empty if none>
next: <one line>

Compact return, as your final message:

contract: <work id>/<task>
attempt: a<N>
outcome: done | blocked | waiting
tested revision: <git rev-parse HEAD> (uncommitted diff against <base>)
report: .grove-run/<task>-a<N>-report.md
blocker: <one line, only if blocked or waiting>
```
