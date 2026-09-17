---
name: work
description: Use when implementing one or several Grove work units. Prepares missing plans, executes within the authorized outcome, verifies acceptance, and reconciles knowledge through grove:close.
---

# grove:work

Read `../../references/discipline.md` and `../../references/planning.md` once.

## Prepare

1. Run `grove status`. Resolve the selected work IDs. For several units, run `grove batch <ids>`; inspect external blockers and the dependency order. If given a release, select its next eligible members and preserve its final acceptance obligations.
2. Run `grove context --work <id> --phase plan` for each selected unit and inspect its code pointers. Required context omissions must be resolved before coding: raise the budget or fetch the named sources, keeping each relevant constraint available. Do not scan the entire knowledge tree.
3. Check the specification, current checkout, prerequisites, and existing plan. Resolve technical unknowns from evidence. Prepare or repair the plan per planning.md, including a shared plan for a combined implementation. Record and surface its execution decision header (approach, reason, delegation, runtime and reassessment condition), or the small-work Next equivalent. Choose agent coordination and durable execution separately, using inspected ownership and available harness capabilities. A `ready` result means required content is present, not that the plan is correct, current, or authorized. Human outcomes and constraints define the mandate; routine technical choices inside it need no additional approval.
4. Fix unresolved blocking questions and missing relationships before dependent implementation. Ask the human only when the answer requires their preference or changes the mandate; continue independent work meanwhile. A release playtest can remain pending while its members proceed.

## Execute and verify

Enter the implementation worktree per discipline.md before the first change. Set each unit active when its execution starts, with started/updated dates and Next. Run lint. If scope grows beyond the recorded size, resize, update the plan and checks, and continue within authority; propose changes to outcomes or constraints before relying on them. A resize into bounded or large moves execution into the controller loop below, even if it started small.

Branch on the unit's recorded `size`.

**Small**: implement in-session as before. Single agent, run the existing suite, record evidence, proceed to close.

**Bounded or large**: run the controller loop. The lead prepares, dispatches, reviews reports and review files, and closes; it never writes code, runs tests, or debugs itself. For each plan task, in dependency order:

1. Record the base revision: `git rev-parse HEAD`.
2. Write `.grove-run/<task>-brief.md` from `skills/work/implementer.md`: the task, the files/interfaces it touches, the acceptance line it serves, the discipline rules that apply, and the report format.
3. Dispatch a fresh implementer with the Agent tool, `model: sonnet`, prompt equal to the brief's path. It writes its report to `.grove-run/<task>-report.md` and returns it as its final message.
4. Write the diff to a file, never into the lead's context: `git diff <base> > .grove-run/<task>-diff.patch`.
5. Dispatch a fresh task reviewer, `model: opus`, using `skills/work/reviewer.md` with the brief, report, and diff paths. It writes `.grove-run/<task>-review.md`.
6. Fix loop, when the review has blocking findings: rounds 1-3 resume the same implementer with SendMessage, attaching the findings; rounds 4-5 dispatch a fresh implementer on `model: opus`. Each round's scoped re-review of only the changed files resumes the same task reviewer with SendMessage, never a fresh one. After round 5, stop, record the still-open findings, and report to the human instead of looping further.
7. Append the task's evidence line to the work page: models used per dispatch, fix rounds run, tested revision, and the command results the report carries. Append one line to `.grove-run/ledger.md`: task, dispatch, model, outcome.

After the last task, dispatch one whole-branch review on the session model (name it explicitly in the dispatch), allow at most one fix dispatch on `model: sonnet`, then invoke `grove:close`.

Model rules, stated once: implementer dispatches use sonnet; reviewer and escalated-fix dispatches use opus; planning and the final whole-branch review use the session model. Every dispatch names its model explicitly. These are prose rules, not configuration: no frontmatter, no grove.toml entry.

`.grove-run/` is gitignored; it holds briefs, reports, diffs, reviews, and the ledger for the run, kept out of the lead's context and off the branch.

Record completed steps and evidence as work proceeds: command, result, tested revision or checkout, and acceptance it supports. Keep Next specific. To hand a prepared selection to an executor or a later session, run `grove export <ids> --out FILE`; it records source and checkout identity, acceptance and bounds, and refuses unprepared work. The executor returns a result document (contract id, work, outcome, tested revision, evidence, findings, next); `grove reconcile RESULT --contract FILE` writes it onto the work pages and refuses when any exported input changed. Acceptance boxes stay the agent's or human's judgment. Shared implementation retains per-unit acceptance and adds joint integration checks. Serialize shared writes; use separate workspaces for concurrent implementation only after inspecting ownership and interfaces.

On interruption, inspect current checkout, plan progress, and evidence before continuing. Small work inspects the partial diff directly; a bounded or large unit instead reads `git status`/`git diff --stat` and `.grove-run/ledger.md` for the last completed dispatch, not the diff itself. Reconcile changed assumptions and invalidated checks. Never treat an agent exit or a checked task as proof of acceptance.

For small work, review the resulting diff against the specification and plan; bounded and large work get this from the loop's whole-branch review instead. Use a focused independent review where a consequential boundary warrants it. Confirm each acceptance condition with appropriate evidence. Human judgment uses the actual attributed response and its context; do not replace it with test output or invent it.

Check proven acceptance boxes, then invoke `grove:close` for each completed unit in dependency order. Keep a release open until its integration and human acceptance conditions hold. Report the next useful action and remaining wait explicitly.
