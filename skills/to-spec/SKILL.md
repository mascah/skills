---
name: to-spec
description: Use when saving settled conversation or design intent as a local specification, or updating its canonical scope.
---

# Save the agreed intent

Read [artifact ownership](../../references/artifacts.md),
[mandate](../../references/workflow.md), and [execution](../../references/execution.md).
Synthesize known intent from the conversation, existing docs and relevant code.
Use project language and respect prior decisions. Setup and tracker access are
unnecessary. Do not start a second mandatory interview; ask only about a
consequential gap that cannot be represented honestly as an open question.

Write or update the existing owner; otherwise use
`docs/work/<effort>/spec.md`. Give it Problem, Intended behavior, Constraints,
Acceptance, Decisions, and Out of scope as useful. Omit empty optional sections.
Use concrete behavior examples and meaningful verification boundaries; choose
routine test details from the project rather than asking approval for each
interface. Expose unresolved consequential meaning, and identify affected units
as not ready instead of inventing a decision.

For execution detail, use Delivery inline by default: named slices linking to
acceptance, genuine dependencies, affected areas, migration sequence and
integration checks. Tiny work needs none. If independent maintenance warrants a
plan, move the sequence into one linked `plan.md` and replace inline detail with
the link. Requirements remain in the spec. Revalidate checkout observations and
avoid prescribing every command or commit as a deliverable.

When substantive discussion changes scope, update this canonical owner; issue
summaries remain pointers. Saving a spec does not publish it, create tickets or
apply readiness labels. Return the path, settled meaning, consequential gaps,
document checks and any next step already within the caller's mandate.
