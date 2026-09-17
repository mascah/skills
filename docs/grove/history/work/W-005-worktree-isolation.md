---
type: work
id: W-005
status: done
started: 2026-09-16
created: 2026-09-16
updated: 2026-09-16
kind: tooling
size: small
scope: [work-planning]
priority: 1
depends_on: []
---
## Outcome
Concurrent `grove:work` sessions implement in isolated worktree branches and hand integration back to the human with ready-to-run commands instead of editing or merging main themselves.

## Why now
Several agents running `/work` in one repository trample each other's changes on main. A completed session is often read hours later after its cache expires, so the closing message must be usable from a fresh session or shell.

## Constraints
Prefer the harness's native worktree tool; fall back to git. Never merge or push to main automatically. Shaping and curation may stay on main. Focus changes belong to shaping on main, not to an implementing branch.

## Acceptance
- [x] discipline.md states detection, creation, resume, and no-direct-main rules for implementation workspaces.
- [x] work SKILL.md requires the workspace check before the first change.
- [x] close SKILL.md ends with the branch committed and a handoff block listing merge, PR, and keep-branch options with exact commands.
- [x] `grove lint` passes and the change itself is delivered on a branch with that handoff block.

## Evidence
- 2026-09-16, branch worktree-W-005-worktree-isolation (base 3d35576): added `## Workspace isolation` to references/discipline.md; work SKILL.md Execute step opens with the worktree entry; close SKILL.md step 8 carries the handoff block. Read back and confirmed by the implementing agent.
- Also added one line to the managed CLAUDE.md/AGENTS.md block in cli/grove/init.py so downstream repos see the rule and Claude Code's native EnterWorktree tool is permitted; re-ran `grove init` here. Downstream repos pick it up by re-running `grove init`.
- `cd cli && uv run --with pytest python -m pytest -q tests`: 117 passed. `grove lint`: 0 errors, 0 warnings.
- The change was implemented inside a native Claude Code worktree created with EnterWorktree, and the session ended with the handoff block instead of merging.

## Next
Human integrates the branch from the handoff block; downstream repos re-run `grove init`.
