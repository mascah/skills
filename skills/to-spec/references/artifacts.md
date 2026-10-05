# Durable owners

Adopt existing project locations. Otherwise use `docs/agents/workflow.md`,
`docs/work/<effort>/spec.md`, optional `discovery.md` and `plan.md` beside it,
`docs/adr/`, and `GLOSSARY.md`. Create only files with useful content. Plain
Markdown and relative links suffice; no IDs, frontmatter, registry, required
status fields, or empty scaffold.

| Owner | Content |
| --- | --- |
| Spec | Problem, intended behavior, constraints, acceptance, decisions, out of scope |
| Delivery in spec, or one linked plan | Slices, structural dependencies, sequencing, affected areas, integration and handoff |
| Discovery notes, when useful | Question/destination, constraints, evidence/sources, open questions/dependencies, disposition |
| Glossary | Resolved domain terms and distinctions, without implementation details |
| ADR | Consequential trade-off, alternatives, rationale, consequences and reconsideration |
| Tracker | Assignment, labels, operational discussion/progress, PR links |

Omit empty optional sections. Give acceptance stable descriptive headings or
anchors when slices need to reference it. Concrete examples beat exhaustive
manufactured stories. Expose consequential open questions; a draft may contain
them, but affected implementation is not ready until they are resolved.

Delivery is optional for tiny work and inline by default. Each named slice links
to acceptance without copying it. Extract `plan.md` only when execution detail
needs independent reading or maintenance. Move the detail and replace it with a
link; requirements stay in the spec. Update scope in its owner, not the plan.

Examples:

- **Direct task:** supplied bug scope says normalization trims and lowercases;
  fix and regression verification need no spec, plan, or tickets.
- **Inline Delivery:** a login spec requires existing sessions to remain valid.
  Delivery sequences a dual-format reader before changing issuance and links
  both slices to that acceptance. The rollout order is execution information.
- **Extracted plan:** a long multi-team rollout moves its sequence into a linked
  plan. The spec keeps the behavioral contract and only the plan link under
  Delivery. Issues point to named slices in that plan.
- **Local-only project:** a local spec, inline Delivery and git history provide
  sufficient scope; credentials and tickets are unnecessary.
- **Abandonment:** persistent discovery records evidence, why the premise failed,
  and what new evidence would justify reconsideration, without generating work.

Substantial requirements and consequential decisions must be recoverable from
git at an identified usable revision. An issue summary links to their owner; it
does not become another requirements document. A small standalone issue may own
its scope and acceptance. Without tracker access its content must be supplied.
Promote growing issue-only work to a local spec and replace issue authority with
a pointer. Operational progress alone requires no local document edit.

Move settled findings to their owner and link rather than maintaining parallel
narratives. Retain useful delivered specs/plans as history. Current behavior
belongs in code and maintained project documentation; enduring rationale belongs
in ADRs where useful.
