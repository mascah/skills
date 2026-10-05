# mascah-skills

This repository ships a personal engineering skill suite. The agreed design and all four delivery stages live in [the refactor specification](docs/work/mascah-skills-refactor/spec.md); current files and [verification results](tests/results.md) establish delivered behavior. The [canonical workflow guide](references/workflow.md) links the single owners of shared rules and skill procedures. Installed skills bundle only their relevant focused references.

## Working here

- The Grove workflow is retired. Do not create Grove work records or run its lifecycle commands. Historical material remains in git; no Grove installation is required.
- Use an isolated worktree branch for writes; do not commit to main. Preserve other sessions' changes and worktrees.
- Use Conventional Commits. Work IDs and tracker references are optional and must correspond to real work; do not manufacture tracking records to satisfy a commit convention.
- Keep requirements in their owning document. Use Delivery inside a spec by default; extract a plan only when independent reading or maintenance warrants it, replacing the inline detail with a link.
- Preserve useful behavior and rationale while removing obsolete machinery. The spec describes intended changes, not proof of implemented behavior.
- Validate changes with checks appropriate to their substance. Documentation changes need document and diff checks; skill behavior needs representative execution scenarios, not only text validation. Report checks actually run and any unexercised runtime integrations.
- Upstream skill repositories, installed plugins, Hermes configuration, and external trackers are reference or integration surfaces; changing this repository does not authorize writes to those surfaces.
- End a writing session with the branch, what changed, verification results, and how to merge or resume it.
