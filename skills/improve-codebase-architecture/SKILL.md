---
name: improve-codebase-architecture
description: Use when observed architectural friction or repeated changes warrant investigating improvements and their costs.
---

# Investigate costly friction

Read project vocabulary, relevant ADRs and the affected code/history. Use
[codebase-design](../codebase-design/SKILL.md) for useful interface/cohesion
principles and [workflow](../../references/workflow.md) for mandate. Read
[execution](../../references/execution.md) before writing. Start with the user's
pain point or evidence from changing areas, not an exhaustive hunt for refactors.

Trace real caller behavior and change paths. Identify where a concept requires
scattered knowledge, callers learn excessive detail, failures cross interfaces,
or meaningful verification is difficult. Test an apparent shallow wrapper with
the deletion test. Distinguish observed cost from a speculative abstraction
opportunity. Respect existing decisions; reopening one needs new consequential
evidence, not stylistic preference.

Compare a small set of credible candidates, including retaining the current
design. Give affected areas, concrete pain/evidence, proposed change, expected
caller/maintainer/test benefits, migration risks and costs, recommendation
strength and uncertainty. Use diagrams or a visual artifact when they clarify
relationships; a concise prose comparison may suffice. No mandatory HTML report,
new architecture vocabulary or agent roster is needed.

Recommend the most useful next investigation or selected candidate. Route a
selected change into [shaping](../shaping/SKILL.md) and durable decisions when
needed. Investigation may conclude that no refactor is justified. A review
request does not authorize implementation; act on an existing implementation
mandate only within its selected scope. Return evidence, options and next step,
preserving useful rationale without creating routine speculative work tickets.
