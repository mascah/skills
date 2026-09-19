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

## Whole-branch review

For the final review of a multi-component change, the brief also carries the lead's affected-sequence list (3-6 transitions across component boundaries, derived from the outcome and changed interfaces). Add a sequence-and-disposition table to the full review, one row per transition:

```text
| Transition | Evidence | Disposition |
| --- | --- | --- |
| <e.g. dispatch → close/reopen view → return → dispatch again> | <test/report line/screenshot, or "none"> | mechanical defect found (cite it) / missing evidence (name the check to run) / reserved human judgment (leave the acceptance box unchecked, name it) |
```

A passing component check never satisfies a transition by itself, and a screenshot's existence is not evidence of what it shows — state what it actually shows or mark the transition missing evidence. Every uncovered transition needs one of the three dispositions above; there is no fourth "assumed fine" outcome. A transition satisfied by cited evidence needs no disposition.
