---
name: implement-spec
description: Use when delivering an entire local specification across its slices, with or without tracker tickets or delegation.
---

# Complete the specified outcome

Read the entire spec, inline Delivery or its linked plan, relevant project
instructions and prior decisions. Use [execution](../../references/execution.md)
for implementation/evidence, [artifact ownership](../../references/artifacts.md)
for scope changes, and [GitHub readiness](../../references/github.md) only when
tracker assignments apply. A local spec needs no tickets, credentials or setup.

Identify all acceptance obligations and their delivery slices. Revalidate
dependencies and checkout observations. Choose an integration branch/workspace
consistent with project isolation; one branch and direct execution suffice.
Honor existing caller policy, ownership and worker roles. Use focused delegation
only when available, permitted and useful; do not prescribe separate implementer,
reviewer and merger agents or an external CLI for every slice.

Use [implement](../implement/SKILL.md) for selected units in genuine dependency
order. Verify a prerequisite's integrated work before dependent execution; a
closed rejected issue or unmerged worker return alone is insufficient. With
tickets, do not dispatch a parent alongside its child units. Collect returned
evidence and inspect actual changes before integrating delegated results.

Maintain concise progress/handoff for sustained work without duplicating scope
or mirroring live tracker status into git. Resume from checkout and existing
evidence, preserving partial work. A newly discovered scope change updates its
owner. A missing input blocks affected slices with a concrete waiting condition;
continue independent authorized slices.

After integrating selected results, verify whole-spec acceptance and affected
interaction/recovery paths, then [review](../code-review/SKILL.md) the combined
diff. Individual files, green components or worker reports do not establish the
whole outcome. Fix material gaps and recheck. Return accepted/remaining scope,
branch/commits, real checks, limitations, integration state and merge/resume
instructions. Tracker changes, PRs, merge, publication and cleanup of caller
workspaces require their existing authorized policy; do not infer them from
successful implementation.
