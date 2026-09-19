---
name: curate
description: Use when asked to tidy, audit, or curate project knowledge, or after code changed outside grove. Finds drift between knowledge and code and proposes fixes; later runs unattended on a schedule.
---

# grove:curate

Read `../../references/knowledge-format.md` once.

## Steps

1. Before the first write, enter a worktree branch: use the harness's native `EnterWorktree` when it exists, otherwise `git worktree add`, with the same detection `references/discipline.md` uses. With no work ID yet, name it for the topic (`worktree-shape-<slug>`).
2. Run `grove lint`. Repair mechanically unambiguous errors; investigate relationship or meaning conflicts before changing them. List remaining warnings.
3. Run `grove status`. Review focus, priority rationale, release membership, dependencies, batch recommendations, missing plans and Next actions. Dates signal possible drift; an old item is not automatically obsolete. For schema 1, upgrade the declaration and translate relationships from evidence before claiming readiness.
4. For each accepted decision lint reports as unreferenced: read it, then `grove find` its subject. Propose one of: link it from the capability it governs, move it to history as superseded, or delete it if it never applied.
5. For each capability with a missing code pointer: `grove find` the behavior in the codebase (`rg` over `src/`, `crates/`, `client/`) and propose the corrected pointer, or mark the capability `draft` and open a question.
6. Read `git log --since=<last close date> --stat` for the repo. For each changed source path, find capabilities whose Code section names it and check the Behavior section still holds. Propose edits.
7. For each open question, check whether its Resolution path has been met. If yes, propose the fold.
8. Apply evidence-backed reconciliation within the user's mandate. Present concrete choices that change outcomes/constraints or need human judgment. Do not turn routine maintenance into an approval queue. For unattended use, persist findings and waiting conditions; unchanged blockers should not cause repeated investigations.
9. Run `grove lint` and `grove status`, then commit on the branch with a Conventional Commits `docs` subject. End the final message with the handoff block `skills/close/SKILL.md` uses (branch, worktree path, what it contains, merge/PR/keep options).

## Rules
- Curation repairs missed upkeep. It does not replace closing work properly.
- Never inject history into live pages. If something old matters again, open a work unit or question.
