---
type: decision
id: D-0004
status: accepted
updated: 2026-09-18
applies_to: [work-planning]
---
## Context
Only `grove:work` isolates itself; `references/discipline.md` exempts shaping and curation as "short knowledge-only edits", and `grove:shape`, `grove:curate` and `grove:explore` never read that file at all. The one rule they do load, the managed `grove init` block, says to use a worktree when *implementing*, which a shaping session does not read as applying to itself. So every planning agent commits to main, and concurrent planning agents share one working directory and one index: `git add -A` from one stages another's half-written page, producing a clean commit that contains someone else's unfinished work. Git offers no lock for this; only separate checkouts prevent it.

On 2026-09-18 the builder hit the visible symptom instead. Work on `worktree-W-009` (16:36-16:37) diverged from main while another session shaped W-010 through W-014 onto main (16:44-16:50); the close handoff's `git merge --ff-only` then refused. A dry-run merge was conflict-free, because knowledge pages are one file per thing. The `--ff-only` was the only obstacle, and the repo's `commit-msg` hook already permits `Merge ` subjects.

## Decision
Every Grove session commits on its own worktree branch. Nothing commits to main, shaping and curation included, and the human integrates each branch. The rule moves into the managed `grove init` block, which all five skills load, rather than staying in `discipline.md`, which only `grove:work` reads. The close handoff drops `--ff-only` so an ordinary divergence is a normal merge rather than a rebase.

The builder chose this on 2026-09-18 over the cheaper alternatives below, accepting one merge per shaping session as the cost of removing the shared-index hazard.

## Alternatives rejected
- Keep shaping on main and serialize it: cheapest, but relies on never running two planning agents at once, which is the behavior that prompted this.
- Fix only the `--ff-only`: addresses the symptom the builder noticed and leaves the shared index untouched.
- Acquire a shaping claim from the W-013 registry: most precise, but W-013 is bounded and unbuilt, so nothing would improve until it ships. [[D-0003-worktree-claims-and-handoff]]
- Commit shaping to main through a lock file or merge queue: new machinery for a problem separate checkouts already solve.

## Consequences
Main becomes integration-only, so `grove status` on main cannot see work shaped on an unmerged branch. This makes W-NNN minting races more likely, not less: two shapers on separate branches can both take the next free id, where shaping on main serialized them through one index. `grove lint` already errors on duplicate `id` and duplicate basename, so a collision is caught at merge rather than silently kept, and the repair is a rename plus its `depends_on`, `members`, `batch` and `focus` references. Branches are therefore meant to be merged promptly, not accumulated. No id allocator is introduced.

Brief `focus` is a single shared value that shaping used to own on main. With shaping on a branch it needs a stated owner rather than last-merge-wins. The pressure for W-013's cross-worktree visibility increases, but neither unit blocks the other. W-013 (closed 2026-09-18, shared worktree claims)

## Reconsider when
Duplicate-id repair at merge becomes frequent enough to justify an allocator, the per-session merge proves more friction than the shared-index hazard it removes, or W-013's claims registry can carry shaping ownership directly.
