---
type: work
id: W-015
status: done
created: 2026-09-18
started: 2026-09-18
updated: 2026-09-18
kind: tooling
size: small
scope: [work-planning]
priority: 2
depends_on: []
---
## Outcome
Every Grove skill session commits on its own worktree branch and says how to merge it, so two planning agents never share a working directory, and an ordinary divergence between a branch and main is a normal merge instead of a refused fast-forward.

## Why now
`grove:shape`, `grove:curate` and `grove:explore` never read `references/discipline.md`, so its worktree rule and its "shaping and curation may stay on main" exemption are both invisible to them. The only rule they load is the managed `grove init` block, whose worktree line says *implement*, which a shaping session does not apply to itself. Concurrent planning agents therefore share main's index, where `git add -A` from one stages another's half-written page with no conflict and no lint error. On 2026-09-18 the builder saw the milder symptom: `worktree-W-009` diverged from main while another session shaped W-010 through W-014, and the close handoff's `--ff-only` refused a merge that a dry run showed to be conflict-free. [[D-0004-every-session-branches]]

## Constraints
Prose and one test assertion only: no CLI command, hook, lock file, id allocator or merge wrapper. Keep the rule in the managed block, which every skill loads, rather than in a reference only `grove:work` reads. Do not weaken the existing conventional-commit or close-before-handoff rules. Branch naming must work before a work ID exists. `grove lint` remains the backstop for duplicate IDs; do not add a reservation scheme.

## Design
Replace the exemption in `references/discipline.md` with the general rule, and move the rule itself into `cli/grove/init.py` BLOCK so shape, curate, explore, setup and close all receive it. Reword the block's existing worktree line from "Implement in a git worktree" to cover any session that writes, so no skill can read itself as exempt.

`skills/shape/SKILL.md`, `skills/curate/SKILL.md` and `skills/explore/SKILL.md` end by committing on the branch and printing the same handoff shape `grove:close` already uses, so the human gets the merge command without a reply. Name a shaping branch for its topic when no work ID exists yet, e.g. `worktree-shape-<slug>`.

Drop `--ff-only` from the handoff in `skills/close/SKILL.md`; a plain `git merge` fast-forwards when it can and merges when it cannot, and the repo's `commit-msg` hook already allows `Merge ` subjects. Keep the existing "if the merge conflicts, rebase" fallback line.

`references/discipline.md` currently says focus "belongs to shaping on main". With shaping on a branch that sentence is false, so give brief `focus` a stated owner rather than letting last-merge-win silently.

Accepted cost, recorded in [[D-0004-every-session-branches]]: work shaped on an unmerged branch is invisible to `grove status` on main, so two shapers can mint the same W-NNN. `grove lint` errors on duplicate `id` and basename, so this surfaces at merge; the repair is a rename plus its references. Branches are meant to be merged promptly. [[W-013-shared-worktree-claims]] would remove the blind spot but is not a prerequisite.

## Acceptance
- [x] The `grove init` BLOCK states that every session works on a worktree branch and never commits to main, with no wording that a non-implementing session can read as exempt; `grove init` rerun updates CLAUDE.md and AGENTS.md.
- [x] `references/discipline.md` no longer exempts shaping and curation, and its brief `focus` sentence names an owner that is true when shaping runs on a branch.
- [x] `skills/shape/SKILL.md`, `skills/curate/SKILL.md` and `skills/explore/SKILL.md` each end on a branch and print a handoff block carrying the merge command; a shaping branch has a name that does not require a work ID.
- [x] `skills/close/SKILL.md` offers a plain `git merge`; a branch diverged from main by unrelated knowledge commits merges without a rebase.
- [x] `cli/tests/test_init.py` asserts the block carries the rule; the CLI suite, `grove lint` and plugin validation pass, and the change is delivered on its own branch.

## Evidence
Shaping only, 2026-09-18, checkout d4e4917. Verified: `references/discipline.md:6` holds the exemption; `grep -rln discipline.md skills/ references/` returns only `skills/work/SKILL.md` and `skills/work/implementer.md`; `skills/close/SKILL.md:21` hardcodes `--ff-only`; `lefthook.yml` `commit-msg` permits `Merge ` and `Revert ` subjects; `cli/grove/lint.py:22-25,39-42` errors on duplicate basename and duplicate id. `git merge-tree --write-tree main worktree-W-009` exited 0 with a clean tree, showing the divergence carried no conflict. Branch/main timeline from `git log --date=format`: 16:36-16:37 against 16:44-16:50. No implementation performed.

- 2026-09-18 T1 (init.py BLOCK, discipline.md Workspace isolation, shape/curate/explore skills, close handoff, test_init.py, CLAUDE.md and AGENTS.md via `grove init`), base 47521ad, small work run as one dispatched implementer Agent `model: sonnet`; task reviewer `model: opus` accept, 0 blocking, 4 minor (curate branch prefix folded into the W-013/W-014 guidance task). 0 fix rounds. Evidence: `test_init.py` asserts the block says sessions never commit to main; `grove lint` 0 errors; `claude plugin validate .` passed; CLI suite green for every test except two in `test_claims.py` that belonged to the concurrent in-flight W-013 T2 edit, recorded there. Merge demonstration in a throwaway temp repo: main advanced by an unrelated commit after the branch diverged, and a plain `git merge <branch>` on main succeeded without rebase (commands and output in the run's `.grove-run/W-015-T1-a1-report.md`). Delivered on branch worktree-W-010-W-016.

## Next
None for this unit; every skill now branches and hands off a plain merge. Reassess if duplicate W-NNN repair at merge becomes frequent (D-0004).
