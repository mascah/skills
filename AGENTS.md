<!-- grove:begin -->
## Grove
Project knowledge lives in `docs/grove/`. Do not read that tree directly; use the CLI.
- Start every session with `grove status`.
- Before touching a work unit run `grove context --work <id>` (add `--phase shape|plan|debug|debrief` when not implementing).
- For one implementation spanning several units, run `grove batch <ids>` and prepare a shared plan.
- After writing any knowledge page run `grove lint`.
- Implement in a git worktree on its own branch, never on main; the close handoff tells the human how to merge.
- Finish implementation with the `grove:close` skill, which ends in `grove close <id>`.
<!-- grove:end -->
