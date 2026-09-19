<!-- grove:begin -->
## Grove
Project knowledge lives in `docs/grove/`. Do not read that tree directly; use the CLI.
- Start every session with `grove status`.
- Before touching a work unit run `grove context --work <id>` (add `--phase shape|plan|debug|debrief` when not implementing).
- For one implementation spanning several units, run `grove batch <ids>` and prepare a shared plan.
- After writing any knowledge page run `grove lint`.
- Every session that writes, shaping and curation included, works on its own worktree branch and never commits to main; a non-work session with no work ID yet is named for its skill and topic (`worktree-<skill>-<slug>`); each session ends by saying how to merge.
- Claim work before changing it (`grove claim <ids>`) and run `grove verify-delivery` before handing a branch to the human.
- Finish implementation with the `grove:close` skill, which ends in `grove close <id>`.
- Give every commit a Conventional Commits subject (`type(scope): summary`, `docs` for knowledge-only changes, `docs: close <id>` for the close) and put the work ID in a `Refs: <id>` footer, never in the subject.
<!-- grove:end -->
