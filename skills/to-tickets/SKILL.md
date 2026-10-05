---
name: to-tickets
description: Use when independently assignable deliverables from a spec or agreed scope need tracker entries or local ticket drafts.
---

# Assign useful deliverables

Read [common discipline](references/discipline.md),
[Specification and Delivery](references/specification.md), and
[tracker scope/readiness](references/assignments.md).
For GitHub operations read [the concrete commands](references/github.md);
local drafts need no tracker tools. Setup/tickets are not implementation prerequisites.

Reuse named slices and real structural dependencies. Introduce slices only
when independent assignment warrants them, linking each to acceptance. Prefer
verifiable end-to-end increments; mechanical migrations may need expand,
migrate and contract stages to preserve compatibility. Do not create a separate
ticket for every command, test, commit or technical layer. Keep structural
information once in Delivery or its extracted plan.

Draft concise titles/summaries with repository, canonical path/slice, usable
revision, acceptance pointer and necessary coordination links. Small standalone
tasks may own acceptance in the issue; promote substantial design to a spec.
Identify missing revision/context explicitly. Local drafts may refer to the
current dirty input but are not ready remote assignments until accessible.

Publish only the selected tickets within existing authority; otherwise return
complete reviewable drafts. With no tracker use local drafts at the project's
existing location, or provide them in the response if persistence adds no value.
When publishing, inspect existing tickets to avoid duplicates, create before
wiring native dependencies, and report partial failures accurately.

Creating tickets does not apply `ready-for-agent`. Use
`triage` to check readiness and parent/child dispatch ownership.
Do not modify unrelated parents. Return the canonical slice mapping, structural
edges, draft or real ticket links, operations actually performed and unavailable
inputs; ordinary tracker progress requires no local document changes.

The `triage` helper is optional. Without it, apply the readiness checklist in the bundled tracker scope/readiness reference directly; do not dispatch overlapping parent/child assignments.
