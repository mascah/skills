---
type: work
id: W-016
status: active
created: 2026-09-18
started: 2026-09-18
updated: 2026-09-18
kind: tooling
size: small
scope: [autonomous-execution]
priority: 2
depends_on: []
sources:
  - https://code.claude.com/docs/en/goal.md
---
## Outcome
`grove launch <ids>` prints one paste-ready `/goal` message for one or more work units, so a long interactive Claude Code session keeps a completion condition and its two drift rules across compaction while the lead's context holds only the plan, briefs and short reports.

## Why now
The builder runs the controller loop for many hours interactively, often through Remote Control, and finds implementation is markedly better with a goal anchor that outlives compaction. What compaction loses is not the mandate, which `grove context` refetches from the work pages, but the lead's role and stop rules: it starts debugging itself, quits early, or asks the human at night. Settled in an explore session on 2026-09-18: a CLI command, not a skill, because the message is a template over the selected IDs with nothing for a model to decide; interactive paste is the primary use and a headless `claude -p` launch is a later option, not built now. [[D-0002-controller-loop-execution]]

## Constraints
One subcommand and one test file; no skill, no hook, no change to `grove:work`, `grove export` or the run adapter. Stdout carries exactly the message, one line beginning with `/goal `, so `grove launch W-010 W-011 | pbcopy` pastes clean; diagnostics go to stderr. Validate the selection with the existing `batch()`: refuse closed, unknown or release IDs, exit 2 on external blockers, and accept preparation gaps because `grove:work` prepares missing plans itself. The message names no model, harness setting or worktree path; those belong to the skill and discipline it invokes. Do not restate outcomes, constraints or acceptance from the pages.

## Design
`cli/grove/launch.py` with `launch(root, ids) -> str`, registered in `cli/grove/cli.py` beside `export`. It calls `batch()` for order and blockers and renders one paragraph from the ordered IDs:

- Condition: the units are finished in this repo; reach it by running the `grove:work` skill for `<ids in order>` on a worktree branch. The invocation is inside the condition because `/goal` starts its turn from the condition text and chaining two slash commands in one message is undocumented.
- Finished: `grove status` lists each unit under Recent, `grove lint` reports 0 errors, every commit sits on the worktree branch with a Conventional Commits subject and a `Refs:` footer, and the final message tells the human how to merge. Recent is the heading `render_status` prints for closed work, so the evaluator can check it from the transcript.
- Parked, as an alternative terminal state per unit: `grove:work`'s bounded fix rounds ran out, or an acceptance box needs a human judgment, and that unit's Next names the open finding or the judgment. Without this the goal loop fights the skill's round-5 stop: the skill parks, the evaluator says not done, the lead keeps hammering.
- Drift rules: never write code, run tests or debug in this session, dispatch per the skill; after compaction or interruption resume from `grove status` and `.grove-run/ledger.md` rather than restarting.

`/goal <condition>` in Claude Code 2.1.277 starts a loop in which a small model checks the condition after each turn and starts the next turn until it holds, is judged impossible, an unrecoverable error occurs or `/clear` runs; it runs in interactive sessions, Remote Control and `claude -p`. Whether the goal survives compaction is undocumented; the binary carries a `restoreGoalFromTranscript` path, which the first real run confirms or refutes.

Rejected: a `grove:launch` skill, since no judgment is added and a skill costs a model turn per launch; sharing text with `scripts/adapters/claude-p.sh`, whose headless prompt ends in a waiting result rather than a parked state, until a second consumer exists.

## Acceptance
- [x] `grove launch W-A W-B` prints exactly one line on stdout, beginning with `/goal `, naming each selected ID in dependency order inside a `grove:work` invocation, the finished state, the parked state and both drift rules; nothing else reaches stdout.
- [x] Closed, unknown and release IDs are refused with a `grove:` error; an external blocker exits 2 with the batch blockers on stderr; a selection that only needs a plan still prints.
- [x] `cli/tests/test_launch.py` covers the lines above; the CLI suite, `grove lint` and plugin validation pass.
- [ ] One pasted message in an interactive Claude Code session on a small unit records in Evidence: the goal loop invoked `grove:work`, the session ended on closed or parked, and whether a compaction occurred and the goal persisted, or that none was observed.

## Evidence
Shaping only, 2026-09-18, checkout 12124c1. Verified: `cli/grove/cli.py` registers subcommands with argparse and routes `export` through `batch()` then `export()`; `batch()` in `cli/grove/work.py` refuses history, done and release IDs, returns dependency order, external blockers and preparation gaps; `render_status` in `cli/grove/status.py:95` prints closed work under `## Recent`; `skills/close/SKILL.md` ends with the merge handoff block the condition relies on; `skills/work/SKILL.md` stops after fix round 5 and reports to the human. Claude Code 2.1.277 `strings` output contains `restoreGoalFromTranscript` and `ProposeGoalTool`; the `/goal` docs describe the condition-checking loop, `/goal clear`, and `claude -p "/goal ..."`, and do not document compaction or chaining slash commands. Human reactions in the explore session: the CLI "makes sense"; interactive use with Remote Control is the need, headless "still not something I fully have a need for yet"; "yes lets add this". No implementation performed.

- 2026-09-18 T1 (`cli/grove/launch.py`, `cli/grove/cli.py`, `cli/tests/test_launch.py`), base 82d4b16, committed 346a5a9: implementer Agent `model: sonnet`; task reviewer `model: opus` accept, 0 blocking, 4 minor. 0 fix rounds. Evidence: 7 new tests (one stdout line with `/goal ` prefix, ordered ids in a `grove:work` clause, finished state, parked state, both drift rules; `W-000` and `W-999` refused with `grove:` on stderr exit 1; unclosed external `depends_on` exits 2 with the blocker on stderr and empty stdout; preparation-gap-only selection prints), suite 125 passed, `grove lint` 0 errors, `claude plugin validate .` passed; `grove launch W-016` printed one line starting `/goal W-016 are finished in this repo; reach that by running the grove:work skill for W-016 on a worktree branch.`
- 2026-09-18 interactive observation, partial: the session that implemented this branch was started from a hand-pasted `/goal` whose text matches the launch template for `W-010 … W-016` (same condition, finished state, parked state and drift rules, without the `grove launch` comma formatting), because the command did not exist yet. The goal loop did start `grove:work`, the lead never wrote code or tests, and no compaction occurred in the session, so goal persistence across compaction was not observed. This is not the acceptance trial: the message was not produced by `grove launch` and the unit was not small. Box 4 stays unchecked.

## Next
Parked on box 4, a human-run trial: in a fresh interactive Claude Code session on this repo after merging, run `uv run --project cli grove launch <one small unit>` and paste the line as the session's `/goal`; record in Evidence whether the goal loop invoked `grove:work`, whether the session ended closed or parked, and whether a compaction occurred and the goal persisted (or that none was observed). Then check box 4 and run `grove close W-016`. Code, tests and the capability page are done and merged with this branch.
