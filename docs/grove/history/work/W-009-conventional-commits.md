---
type: work
id: W-009
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
Every commit an agent makes through a Grove skill, in any repo that has run `grove init`, has a Conventional Commits subject (`type(scope): summary`), so release tooling such as release-please can derive versions and changelogs from history.

## Why now
This repo's lefthook `commit-msg` hook already requires conventional subjects, but the skills never state the format. After the hook landed, agents still committed `W-004: ...` and `grove: close W-004` subjects and worked around the hook (`4530c15`, `f78b6a2`, `afc10d6`). The rule has to live where every skill session reads it, not in one repo's hook.

## Constraints
Prose rule only: no new CLI check, hook or config. Keep the work ID discoverable from history. Repos without a hook still follow the rule.

## Design
Put the rule in the two places every committing session already loads: the managed `## Grove` block that `grove init` installs (covers shape, curate, explore, setup and close on any repo) and `references/discipline.md` (covers `grove:work`). The work ID goes in a `Refs: W-NNN` footer, not the subject. Knowledge-only commits use `docs`; the close commit is `docs: close W-NNN`; the type otherwise follows the change (`feat`, `fix`, `refactor`, `test`, `ci`, `chore`).

Rejected: work ID as the scope (`feat(W-004): ...`). Scope names a code area and release-please groups the changelog by it; a work ID there is noise for readers of the changelog. Reconsider if a repo needs per-work changelog grouping.

## Acceptance
- [x] `cli/grove/init.py` BLOCK has one line stating the conventional subject rule and the `Refs: W-NNN` footer; `grove init` rerun on this repo updates CLAUDE.md and AGENTS.md.
- [x] `references/discipline.md` states the same rule once, in the workspace section, including the `docs: close W-NNN` form.
- [x] `scripts/adapters/claude-p.sh` headless prompt says commits must be conventional.
- [x] `cli/tests/test_init.py` asserts the block mentions the rule; suite and `grove lint` pass; the change is delivered on a branch whose own commits are conventional.

## Evidence
Branch `worktree-W-009` from `edab734`. Single agent, in-session (small work); no delegation.
- `cli/grove/init.py` BLOCK gained one line: Conventional Commits subject, `docs` for knowledge-only, `docs: close <id>` for the close, work ID in a `Refs: <id>` footer.
- `grove init` rerun from this checkout (`PYTHONPATH=cli python3 -c "from grove.cli import main; main()" init`) printed `updated CLAUDE.md block` / `updated AGENTS.md block`; both files now carry the rule. The `grove` on PATH is an editable install of the main checkout, so it cannot exercise a worktree's code.
- `references/discipline.md` workspace section states the rule once, including `docs: close W-NNN`; `scripts/adapters/claude-p.sh` headless prompt requires it.
- `cli/tests/test_init.py` asserts the block mentions "Conventional Commits" and "Refs: <id>".
- `uv run --extra dev --project cli pytest cli/tests -q`: 118 passed. `grove lint`: 0 errors, 0 warnings.

## Next
None; the rule is in place. Future Grove sessions in any initialized repo commit conventionally.
