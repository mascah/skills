---
type: capability
id: work-planning
status: settled
updated: 2026-09-18
---
## Behavior
Work keeps capability scope, ordered release membership and prerequisites separate. Status shows the selected focus, structural preparation, dates, blockers, candidate shared implementations, and a next recommendation. Active unblocked work comes first, then focus/member order, then priority and ID. Batch assessment reports dependency order, external blockers, shared capabilities, and preparation gaps; agents inspect code before deciding whether writes can run in parallel.

Explore is a conversation about an open idea: ideas in prose, no option menus, draft-page recommendations tested before they are repeated, code cited as checkout fact rather than design, and a knowledge write only when the human settles a point. It never loads the preparation references. Shape develops the specification and selection from evidence once an outcome is selected. Work prepares or repairs the plan against the checkout, executes under existing authority, and keeps per-unit evidence and Next current. Several units can share a plan and implementation with sequential dependent steps. Release acceptance remains separate from member completion. [[D-0001-delegated-development]]

Plans open with an execution decision: approach, reason, delegation, runtime and reassessment condition. A single agent is the default for small work. Bounded and large work run as a controller loop: the lead prepares on the session model, dispatches a fresh implementer (sonnet) and a fresh task reviewer (opus) per task with the model named on every dispatch, runs at most five fix rounds with escalation to opus from round four, takes one whole-branch review on the session model, then closes. Teams remain the exception and still need inspected ownership, interfaces, acceptance and integration checks that justify coordination costs. [[D-0002-controller-loop-execution]] Durable execution is chosen separately from agent coordination. Work records and surfaces this decision during preparation; the CLI does not select an agent topology or provide an executor.

For bounded and large work the lead never writes code, runs a test-fix loop or reads the diff; briefs, reports, diffs, reviews and the run ledger live under gitignored `.grove-run/` in the worktree, and each task report uses the contract result shape so a harness can later consume it. Fix rounds most often catch a sentence the implementer dropped or left out of scope as "pre-existing"; briefs should name the whole section as owned, not only the lines to change.

Implementation runs in an isolated worktree branch named after the work IDs, native harness tool first and git fallback second, so concurrent sessions do not collide on main. Knowledge edits and the close commit land on that branch. Close never merges or pushes main; it ends with a handoff block giving the human the merge, PR and keep-branch commands, usable from a fresh session after the original context is gone. Brief focus changes stay with shaping on main. The managed agent-instruction block installed by `grove init` states the rule. Commits use Conventional Commits subjects (`type(scope): summary`) with the work ID in a `Refs: W-NNN` footer rather than the subject, knowledge-only commits typed `docs` and the close commit `docs: close W-NNN`; the managed block and `references/discipline.md` both state it, so repos without a `commit-msg` hook follow it too.

## Acceptance
- [x] A selected release and its required members are visible with dates and completion summaries.
- [x] Dependencies remain resolvable after closure; cycles and malformed references are reported.
- [x] Missing plans and unresolved legacy relationships are visible before execution.
- [x] Selected units can be assessed for a shared implementation with explicit order and blockers.
- [x] Closure checks acceptance, evidence, prerequisites, members and blocking questions, then uses the status selection rules.

## Limits
Readiness is structural. The CLI cannot establish that a plan is correct, detect all conflicting code writes, or prove the truth of evidence. Creation dates of legacy work remain unknown when not recorded. Model choice per dispatch is skill prose; the CLI does not enforce it, and the dispatched model is known only from the agent's self-report.

## Code
- cli/grove/work.py
- cli/grove/status.py
- cli/grove/close.py
- cli/grove/lint.py
- skills/explore/SKILL.md
- skills/shape/SKILL.md
- skills/work/SKILL.md
- skills/work/implementer.md
- skills/work/reviewer.md
- skills/close/SKILL.md
- references/planning.md
- references/discipline.md
- cli/grove/init.py
