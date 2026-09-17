# Sizing work

Size controls preparation and verification depth; it does not choose interactive versus unattended execution. Use the smallest honest size, and reassess when the actual code reveals a larger change.

| Size | Required preparation | Execution |
|---|---|---|
| small | Outcome, scope, Acceptance, concrete Next or Plan | Change and run relevant existing checks; verify acceptance |
| spike | Question, Bounds, experiment Plan | Stay within bounds; record answer and limitations in Disposition |
| bounded | Outcome, scope, Constraints, Design as needed, Plan, Acceptance | Tests first where useful logic changes; verify and review the diff |
| large | Bounded preparation plus Checkpoints and Verification | Verify incremental integration; reconcile knowledge at useful checkpoints |

Any size may have dependencies or belong to a shared implementation. `members` is an ordered list on a release, while `scope` always contains capabilities. Release acceptance includes integration and any required human judgment. A release is not an executable batch; assess selected members with `grove batch`.

A small work unit may carry its entire plan in Next. Larger units can use `## Plan` or a `plan` artifact. See `planning.md`. Neither a large document nor a populated section proves readiness; the agent checks adequacy against the checkout. Lint validates relationships and structural invariants; status reports preparation gaps.
