# Preparing and combining work

Planning is an agent responsibility inside the user's authorized outcome and constraints. It is a phase of the normal workflow; the human need not issue another command or approve routine technical choices.

## Preparation contract

A work unit owns its intended behavior and acceptance. Use its Outcome, Constraints, Acceptance, and Design sections as the specification. Scope points to current capabilities; it does not copy every capability into a new specification.

Before implementation, inspect the actual checkout and prepare:

- The chosen approach, affected files/interfaces, and constraints that must survive.
- Steps producing reviewable outcomes in dependency order, each tied to acceptance.
- Meaningful checks at the relevant layer, joint integration checks, and any required human judgment. Fix measurement thresholds before running comparisons. For a multi-component change, name the affected interaction/recovery sequence the final review will check.
- Risks that affect implementation, checkpoints for larger work, and a concrete next action on interruption.

Small work can use a concrete Next action and its acceptance checks. Bounded and large work use an inline `## Plan` or a repo-relative `plan` file. A spike needs its Question, Bounds, an experiment plan, and a Disposition on completion. Plans should identify the checkout/base revision inspected. Revalidate code, constraints, and prerequisites on execution and resume; file existence is only structural preparation.

Use a separate artifact when the detail merits independent retrieval. Place it outside the knowledge-page tree, such as `docs/plans/`, and point to it using `plan`. The context command includes that file for plan, implement, debug and debrief. A larger design may be linked from Design and read when needed. Keep one owner for each requirement; reference acceptance rather than maintaining competing copies. Retain plans as evidence when work closes.

## Execution decision

Choose the execution approach during preparation, after inspecting dependencies, code ownership and available harness capabilities. Default to a single agent for small work and to the controller loop for bounded and large work. Select within the user's constraints and the harness's permissions; routine selection needs no additional human approval.

| Approach | Use when |
| --- | --- |
| Single agent | Small work: all steps fit in one session. |
| Controller loop | Default for bounded and large work: the lead prepares, dispatches a fresh implementer and a fresh task reviewer per task with explicit models, runs bounded fix rounds with escalation, then one final review before close. |
| Agent team | Exception: several substantial workstreams can overlap, have clear ownership and checks, and benefit from ongoing coordination between workers. |

Before choosing a team, name the overlapping tasks, file/workspace owners, stable interfaces, independent acceptance checks, integration owner and combined checks. Explain why expected progress or quality warrants duplicated context, coordination and merge costs. Work-item count, duration and disjoint capability labels alone do not establish useful parallelism. If those conditions are unproven, start with a single lead and record when to reassess.

Model rules for the controller loop default to sonnet for implementers and opus for reviewers and escalated fixes; `skills/work/SKILL.md` owns the full rules. Every dispatch is an ordinary subagent via the Agent tool with an explicit model, not a teammate; verify the actual returned handle on the run's first dispatch rather than assuming the phrase "no teams" is enough.

Each task's full report uses the contract result shape (contract, work, attempt, outcome, tested revision, evidence, findings, next) and lives at an attempt-specific path under `.grove-run/` in the worktree (briefs, `<task>-a<N>-report.md`, `<task>-a<N>-diff.patch`, `<task>-a<N>-review.md`, ledger); the dispatch's own completion return is the compact subset of that shape plus the report path, never the full report repeated.

Choose durability separately: an interactive session or an available durable executor for unattended continuation, checkpoints and recovery across sessions. Long serial work can need a durable executor without needing a team. Tmux provides process visibility; the driver supplies supervision and recovery. Name the actual supported executor or record the unmet requirement; a plan must not claim an unimplemented adapter is available. `grove run CONTRACT -- ADAPTER...` is the local executor: one attempt per invocation, one owner per attempt, durable ledger, bounded attempts and unchanged-wait skipping. Only a fake process adapter has been exercised; no harness adapter is demonstrated until W-004 records one.

Put this compact header at the start of each new or repaired plan, including shared plans, and surface it in the preparation summary. For small work using Next instead of a plan, record the choice and reason there without creating a separate artifact.

```text
Execution: Single agent | controller loop | agent team; task order/overlap.
Reason: Dependency and ownership evidence supporting the choice.
Delegation: Bounded tasks and owners, or none; team plans identify integration ownership below.
Runtime: Interactive session | named durable executor | unmet runtime requirement; availability and recovery needs.
Reassess: Concrete condition that would change the approach, or none currently identified.
```

Update the decision when dependencies, ownership, interfaces or runtime availability change. Combining work into one implementation and choosing how agents execute it are separate decisions; `grove batch` supplies evidence for the first, not an automatic team selection.

## One implementation, several work units

Run `grove batch W-101 W-102` for the actual selection, then load each unit's planning context. The result identifies ordering, external blockers, missing preparation, and shared capability scope. A `batch` label records a recommendation, not authority or proof that code is independent.

Prepare one shared plan naming every selected work ID, its acceptance obligations, ordered tasks, affected files/interfaces, and joint verification. Point each selected work unit's `plan` to that artifact. Dependent items can be implemented sequentially in the same branch/session. Overlapping writes need one owner or serialization. Disjoint capability scopes still require inspection for shared code, fixtures, migrations, and integration boundaries before parallel work.

Keep outcomes and evidence individually attributable. A hard prerequisite closes on its independently verified acceptance before the dependent unit executes. The later joint integration result belongs in the shared plan and dependent/release evidence; it is not required before that dependent implementation exists. If the prerequisite's own acceptance cannot be proved independently, reshape the units or distinguish that coordination need from a hard depends_on edge. A release closes only after its required members and release-level checks are satisfied. An abandoned prerequisite is not successful completion. If selection grows, update the shared plan and reassess the batch before expanding implementation.

## Research, review, and learning cost

Start with local code and relevant current knowledge. Consult external sources for unstable or unresolved facts that could change the approach. Read supporting references only when their phase needs them. Use focused independent review for risky boundaries; a fixed roster of reviewers is not required.

Stop research when more investigation is unlikely to change the next useful action. Record what remains uncertain. Fixes should leave a reusable insight in the owning capability or decision when future work would otherwise repeat the mistake. A recurring mechanically checkable invariant belongs in lint or tests. Routine edits need no new lesson document.

## Interruption and autonomous callers

Keep Next, completed plan steps, evidence paths, and unresolved findings durable. The run checkpoint — the ledger head plus each selected work page's Next, covering selected IDs, current task/attempt, completed tasks with consumed attempt id and tested revision, outstanding handles and owners, pending human judgments, and next action — is owned by `skills/work/SKILL.md`. On resume inspect Git changes, the recorded plan/base, prior evidence, and currently running work before repeating steps. Preserve partial work. Checks invalidated by code changes must run again; unchanged evidence remains attributable to its tested revision, and new success claims require current verification.

Consume each attempt's result once, against its ledgered identity, and investigate rather than accept a mismatched or missing return; `skills/work/SKILL.md`'s controller loop states the full consume-once and owned-wait rules.

For a headless caller, return the work IDs, plan path, current activity, evidence references, next action, and a concrete waiting condition. The durable form is the W-002 contract: `grove export` produces the input and `grove reconcile` accepts a result only against unchanged inputs; a `waiting` result names what it waits on and which paths would change when it is answered. Persist a question when human input is needed; continue independent authorized work. An unchanged wait should not trigger another investigation. Runtime process ownership, scheduling, and retry enforcement belong to the executor, not to a claim made by a skill.
