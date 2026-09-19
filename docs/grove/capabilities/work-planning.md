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

Every dispatch is an ordinary subagent through the Agent tool with an explicit model; the run's first dispatch verifies the returned handle and records it in the ledger, and a harness that returns a teammate or no resumable handle is recorded as a limitation rather than worked around by changing settings. Workers write full reports to attempt-numbered paths (`<task>-a<N>-report.md`, `-diff.patch`, `-review.md`) and return only compact lines, with no completion message. Each attempt is consumed once through the ledger: a late or duplicate notification for a ledgered attempt causes no redispatch, reread or handoff, and a mismatched or report-less return is investigated. Workers own their checks in the foreground; a still-running check is handed off as `outcome: waiting` with command, owner, evidence path and wake condition, and the lead waits on that one worker without polling. The run checkpoint is the ledger plus each work page's Next, scaled to standalone work (no ledger), batches (per-member lines, no umbrella) and releases (umbrella activated at the first member's start); resume compares it with the checkout and live handles before redoing anything. The whole-branch review maps a short affected interaction and recovery sequence to evidence with an explicit disposition per uncovered transition (mechanical defect, missing evidence naming the check, or reserved human judgment); one focused verification worker runs only the missing checks, then one fix dispatch may follow. Runtime evidence so far comes from this repository's own W-010 to W-016 run; the harness labelled ordinary named subagents as a team roster while the dispatch handles behaved as subagents.

Every session that writes, shaping, curation and explore included, works on its own worktree branch, named after the work IDs or `worktree-<skill>-<slug>` when no ID exists, native harness tool first and git fallback second, so concurrent sessions never share an index. In the worktree the session claims its selected work with `grove claim <ids>` before the first change: the registry lives in the git common directory, is local and never committed, acquires a set atomically, and a claim is ownership, not liveness; `grove claim --release` and `--take` release and recover ownership and `grove claims` lists claims with committed-file observations. `grove status` overlays those claims, skips foreign-claimed work with "resume or coordinate", and never lets a branch observation satisfy this checkout's prerequisites. Knowledge edits and the close commit land on the branch; `grove close` also writes the committed delivery declaration `docs/grove/deliveries/<branch>.json`, and `grove verify-delivery [CANDIDATE] [--base REF] [--json]` validates the committed tree read-only (exit 0 verified, 1 errors, 2 inapplicable): exactly one declaration changed since the merge-base, each delivered id archived, done, new since base and free of `closure_errors`, which close and the validator share; `retains` names explicit partial delivery. Close never merges or pushes main; after the validator passes it ends with a handoff block giving the human the plain merge, claim release, PR and keep-branch commands, usable from a fresh session after the original context is gone, and every planning skill ends with the same block. Brief `focus` is set by the shaping session on its branch and merge order decides between competing changes. The managed agent-instruction block installed by `grove init` states these rules. [[D-0003-worktree-claims-and-handoff]] [[D-0004-every-session-branches]] Commits use Conventional Commits subjects (`type(scope): summary`) with the work ID in a `Refs: W-NNN` footer rather than the subject, knowledge-only commits typed `docs` and the close commit `docs: close W-NNN`; the managed block and `references/discipline.md` both state it, so repos without a `commit-msg` hook follow it too.

## Acceptance
- [x] A selected release and its required members are visible with dates and completion summaries.
- [x] Dependencies remain resolvable after closure; cycles and malformed references are reported.
- [x] Missing plans and unresolved legacy relationships are visible before execution.
- [x] Selected units can be assessed for a shared implementation with explicit order and blockers.
- [x] Closure checks acceptance, evidence, prerequisites, members and blocking questions, then uses the status selection rules.
- [x] A claim made in one checkout is visible from main and every linked worktree without a commit, and a delivery declaring an unclosed unit fails `grove verify-delivery`.

## Limits
Readiness is structural. The CLI cannot establish that a plan is correct, detect all conflicting code writes, or prove the truth of evidence. Creation dates of legacy work remain unknown when not recorded. Model choice per dispatch is skill prose; the CLI does not enforce it, and the dispatched model is known only from the agent's self-report. Claims are visible only within one machine's common git directory, and observation labels are relative to the current checkout's HEAD. Claims and `verify-delivery` prove structure and references, not human judgment, and a direct `git merge` bypasses both. Goal persistence across compaction and the `outcome: waiting` handoff are shown by recorded replay, not by a runtime run.

## Code
- cli/grove/work.py
- cli/grove/status.py
- cli/grove/close.py
- cli/grove/lint.py
- cli/grove/claims.py
- cli/grove/delivery.py
- cli/tests/test_claims.py
- cli/tests/test_delivery.py
- cli/tests/test_workflow.py
- skills/curate/SKILL.md
- skills/explore/SKILL.md
- skills/shape/SKILL.md
- skills/work/SKILL.md
- skills/work/implementer.md
- skills/work/reviewer.md
- skills/close/SKILL.md
- references/planning.md
- references/discipline.md
- cli/grove/init.py
