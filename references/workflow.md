# Routes and mandate

Read a project's agent instructions and, if present, its workflow file (default
`docs/agents/workflow.md`). Existing paths and executor policy take precedence.
Infer missing conventions from the checkout; setup is optional.

Choose the activity that answers the current request:

| Need | Activity | Useful result |
| --- | --- | --- |
| Investigate whether an idea is worthwhile | `discovery` | Evidence and continue, defer, abandon, or answer-only |
| Clarify intended change | `shaping` | Outcomes, alternatives, constraints, acceptance |
| Preserve settled intent | `to-spec` | Local spec |
| Assign independent deliverables | `to-tickets` | Optional tickets referring to Delivery slices |
| Deliver one chosen unit | `implement` | Verified change or specific blocker |
| Deliver the whole spec | `implement-spec` | Integrated acceptance across slices |
| Classify and prepare a request | `triage` | Investigation, assignment, human input, or rejection |

These are independent entry points. A clear small bug goes straight to
implementation. A bounded feature can go from shaping to a spec to implementation
without tickets. A question can be answered in conversation without any file.
Use `research`, `prototype`, `domain-modeling`, and `codebase-design` when their
particular discipline helps; do not turn them into universal gates.

Preserve the caller's mandate. Discussion, research, drafting, and review do not
authorize production implementation or external publication. An implementation
request with sufficient scope authorizes routine local planning and technical
choices. Ask for missing intent or a changed mandate, not repeated approval for
already authorized decisions. External writes must be covered by the user's
request or an explicit caller policy. Finish a reviewable local draft before
asking for publication authorization when it is missing.

Persistence is justified by future use. An abandoned offline-sync idea may record
the evidence that connectivity already meets the need and a reconsideration
condition; it creates no implementation assignment. Short investigations need
no compulsory discovery document.

For artifact ownership and examples, read [artifacts.md](artifacts.md). For any
writing or implementation session, read [execution.md](execution.md).
