---
type: work
id: W-006
status: done
started: 2026-09-17
created: 2026-09-17
updated: 2026-09-17
kind: tooling
size: bounded
scope: [work-planning]
priority: 1
depends_on: []
---
## Outcome
`grove:work` prepares in the calling session and then executes bounded and large work as a controller loop: fresh implementer per task, fresh reviewer per task, explicit cheaper models on every dispatch, bounded fix rounds with escalation, one final review, then close. The lead never writes code or debugs, so the session's model choice no longer sets the cost of implementation.

## Why now
A `/work` run started on Fable recently spent about 400k tokens debugging in the live conversation. Every further `/work` on a bounded unit repeats that until the lead stops implementing. [[D-0002-controller-loop-execution]]

## Constraints
One command, no default human checkpoint between plan and execution; an optional plan-only stop is acceptable. Humans still own outcomes and constraints; the lead owns the work page, evidence and `grove close`. Model rules are prose in the skill and every dispatch names its model; no frontmatter and no grove.toml configuration. Task reports use the contract result shape (outcome, tested revision, evidence lines, findings, next) so the loop can later be hoisted into a harness. Diffs and review packages go to files, not into the lead's context. Small work stays single agent in-session.

## Design
- `skills/work/SKILL.md` Execute: after the worktree entry and activation, branch on size. Small: implement in-session as today. Bounded and large: for each plan task record the base revision, write a brief file, dispatch an implementer (model sonnet) with the brief path, receive its report, write the diff to a file, dispatch a task reviewer (model opus) with brief, report and diff paths, run the fix loop (rounds 1-3 resume the implementer, rounds 4-5 fresh implementer on opus, scoped re-review each round, stop and report after 5), append the task's evidence to the work page, continue. After the last task dispatch one whole-branch review on the session model, one fix dispatch, then `grove:close`.
- Two prompt templates beside the skill: implementer (task, interfaces, acceptance line, discipline rules, report format) and task reviewer (spec compliance and quality, findings with evidence, no re-running tests the implementer ran).
- `references/planning.md`: replace the execution table so the controller loop is the default for bounded and large, single agent the small default, and teams remain the exception; add the model rules (implementer sonnet, reviewer and escalation opus, planning and final review on the session model; always name the model); note the report shape equals the contract result.
- `references/discipline.md`: the lead never runs a test-fix loop; a failure returns to a dispatched implementer with the finding attached, and the debugging rule applies inside the implementer.
- Files for briefs, reports, diffs and the loop ledger live under the worktree in a gitignored path so the transcript does not carry them.
- Confirm on the first run that the Agent tool `model` parameter is honored and that the dispatched implementer operates inside the lead's worktree; record either way.

## Plan
```text
Execution: Controller loop applied to this unit itself (dogfood); tasks T1 -> T2 sequential, T3 lead-only.
Reason: T2 wording must match the terms T1 introduces; all edits are prose in four files with one owner, so no team. Running W-006 through its own loop supplies the trial evidence without waiting for another bounded unit.
Delegation: T1 implementer (sonnet) + reviewer (opus); T2 implementer (sonnet) + reviewer (opus); final whole-branch review on the session model (Fable 5.1); lead writes plan, briefs, evidence, close.
Runtime: Interactive session; Agent tool dispatch with explicit `model`; run files under .grove-run/ in the worktree.
Reassess: If the Agent tool ignores `model` or implementers cannot write in the lead's worktree, fall back to in-session single agent and record the unmet requirement.
```
Base: worktree-W-006-controller-loop-work from c6a7ceb.
- T1 (acceptance 1, 2): `skills/work/SKILL.md` Execute branches on size and spells out the loop; add `skills/work/implementer.md` and `skills/work/reviewer.md` templates; add `.grove-run/` to .gitignore.
- T2 (acceptance 3): `references/planning.md` execution table + model rules + report-shape note; `references/discipline.md` lead-side test-fix loop rule.
- T3 (acceptance 4, 5): lead records per-dispatch models, fix rounds and context use in Evidence; `grove lint`; `claude plugin validate`; final review dispatch; `grove:close`.

## Acceptance
- [x] work SKILL.md branches on size and describes the per-task dispatch, review, fix loop, escalation, and final review with explicit models.
- [x] Implementer and task-reviewer prompt templates exist and use the contract result shape for reports.
- [x] planning.md makes the loop the bounded/large default and carries the model rules; discipline.md forbids lead-side test-fix loops.
- [x] One real bounded unit runs through the loop and its Evidence records the models used per dispatch, the number of fix rounds, and the lead's approximate context use.
- [x] `grove lint` passes and the plugin still registers.

## Evidence
- 2026-09-17 T1 (SKILL.md Execute + implementer.md/reviewer.md + .gitignore), base c6a7ceb: implementer Agent `model: sonnet` (self-reported claude-sonnet-5, worked in the lead's worktree, confirmed via `git rev-parse --show-toplevel`); task reviewer `model: opus` returned fix (1 blocking: dropped resize sentence; 2 minor); fix round 1 resumed the same sonnet implementer; scoped re-review on opus: accept. 1 fix round. Implementer evidence: `grove lint` 0 errors; `claude plugin validate .` passed (1 pre-existing marketplace warning).
- 2026-09-17 T2 (planning.md execution table + model rules; discipline.md lead-never-debugs), base c6a7ceb: implementer `model: sonnet` (self-reported claude-sonnet-5); task reviewer `model: opus` returned fix (1 blocking: stale "Default to a single agent" lead sentence, which the implementer had flagged but left out of scope; 1 minor: discipline.md review rule); fix round 1 resumed the same sonnet implementer; scoped re-review on opus: accept. 1 fix round. `grove lint` 0 errors.
- 2026-09-17 T3/final, base c6a7ceb: whole-branch review dispatched on the session model (`model: fable`, Fable 5.1) returned fix (1 blocking: SKILL.md told the lead to review diffs; 6 minor wording/consistency items); one fix dispatch on `model: sonnet` applied all seven; lead confirmed by reading the final Execute section of skills/work/SKILL.md (not the diff). Dispatch ledger: 2 implementers (sonnet), 2 task reviewers (opus), 2 fix rounds total (one per task, both resumed the same sonnet implementer; no escalation to opus needed), 1 final review (fable), 1 final fix (sonnet). The Agent tool `model` parameter was honored (each agent self-reported claude-sonnet-5 / opus / fable) and dispatched agents wrote inside the lead's worktree (`git rev-parse --show-toplevel` in each report). Lead context at close: about 100k tokens total, of which roughly 30k was preamble before the first dispatch; the lead never opened a diff.
- Lead checks: `grove lint` 0 errors, 0 warnings; `claude plugin validate .` passed (1 pre-existing marketplace description warning); `cd cli && uv run --with pytest python -m pytest -q tests` 117 passed.
- Trial caveat: this unit is prose-only, so the fix loop never exercised a failing test; W-004 or the next code-bearing bounded unit is the first real test of the debugging boundary.

## Next
grove:close W-006; then W-004 chooses its first harness trial from this run's ledger.
