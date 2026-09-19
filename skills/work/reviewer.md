# Task reviewer brief template

The lead fills this in per task and dispatches a fresh task reviewer with the Agent tool (`model: opus`), passing the brief, report, and diff paths.

```text
# Task review: <work id>/<task>

Brief: .grove-run/<task>-brief.md
Report: .grove-run/<task>-a<N>-report.md
Diff: .grove-run/<task>-a<N>-diff.patch

## Job
Check the diff against the brief's acceptance line: does it do only what the brief asks, does the acceptance line have real evidence, is the diff itself sound (correctness, dead code, scope creep beyond the brief)? Do not re-run tests the implementer's evidence already lists; spot-check at most one command from that evidence if something looks off, running it in the foreground and collecting its exit status and output yourself. Each finding cites a file:line and states why it blocks close or is minor.

## Output
Write the full review to `.grove-run/<task>-a<N>-review.md`. Your final message is a compact return only, never the full review, and send no extra SendMessage announcing completion.

Full review, written to the file:

contract: <work id>/<task>
attempt: a<N>
verdict: accept | fix
tested revision: <base revision the diff is against>
findings:
- [blocking|minor] <file:line> — <what and why>
next: <one line for the lead>

Compact return, as your final message:

contract: <work id>/<task>
attempt: a<N>
verdict: accept | fix
tested revision: <base revision the diff is against>
report: .grove-run/<task>-a<N>-review.md
```
