# Specification and Delivery ownership

Adopt the project's spec location, otherwise docs/work/<effort>/spec.md. A spec
owns Problem, Intended behavior, Constraints, Acceptance, Decisions and Out of
scope as useful. Omit empty sections; concrete behavior examples beat exhaustive
manufactured stories. Use stable descriptive acceptance anchors when slices
need pointers. Expose consequential open questions: a draft may contain them,
but the affected unit cannot be ready with unresolved meaning.

Delivery owns execution only: named slices linked to acceptance, structural
prerequisites, affected areas, migration sequence, integration and handoff.
Tiny work needs none; use inline Delivery by default. Extract a linked plan.md
when independent reading/maintenance warrants it, moving the detail rather than
copying it. Requirements stay in the spec, and scope changes update that owner.
Do not turn every test, command or commit into a slice or ticket.

Example: existing login sessions remain valid is acceptance. Deploying a reader
that accepts both token formats before changing issuance belongs in Delivery.
A long multi-team rollout may move that sequence into one linked plan; neither
a local feature spec nor its plan requires credentials or tickets.

Retain useful delivered specs/plans as history. Current behavior belongs in code
and maintained project docs; consequential enduring rationale belongs in an ADR.
Substantive tracker discussion changes update the spec/slice. Routine assignment,
labels/comments and PR links remain tracker coordination, not document updates.
