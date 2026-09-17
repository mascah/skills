# Task reviewer brief template

The lead fills this in per task and dispatches a fresh task reviewer with the Agent tool (`model: opus`), passing the brief, report, and diff paths.

```text
# Task review: <work id>/<task>

Brief: .grove-run/<task>-brief.md
Report: .grove-run/<task>-report.md
Diff: .grove-run/<task>-diff.patch

## Job
Check the diff against the brief's acceptance line: does it do only what the brief asks, does the acceptance line have real evidence, is the diff itself sound (correctness, dead code, scope creep beyond the brief)? Do not re-run tests the implementer's evidence already lists; spot-check at most one command from that evidence if something looks off. Each finding cites a file:line and states why it blocks close or is minor.

## Output
Write the review to `.grove-run/<task>-review.md` and repeat it as your final message.

contract: <work id>/<task>
verdict: accept | fix
tested revision: <base revision the diff is against>
findings:
- [blocking|minor] <file:line> — <what and why>
next: <one line for the lead>
```
