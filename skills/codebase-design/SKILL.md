---
name: codebase-design
description: Use when designing an interface, improving testability, or evaluating module cohesion and the cost imposed on callers.
---

# Design for callers and maintainers

Read relevant project language, decisions and changing code. Use
[artifact ownership](references/artifacts.md) and
[execution](references/execution.md) for writes. Prefer the project's
vocabulary; these supporting terms explain design rather than replacing it:

| Term | Meaning |
| --- | --- |
| Module | Implementation behind an interface, at the useful scale |
| Interface | Everything a caller must know: inputs, invariants, order, errors, configuration and performance |
| Depth | Useful behavior behind a manageable interface |
| Seam | A location where behavior can vary without rewriting callers |
| Adapter | A concrete implementation satisfying an interface at that seam |
| Leverage | Capability gained per fact a caller must learn |
| Locality | Related changes, knowledge, bugs and checks concentrated together |

Design from concrete usage and acceptance. Compare plausible alternatives when
the choice matters, with caller examples, error handling, constraints, test
surface and migration costs. A small interface should hide real complexity,
not hide necessary guarantees. The deletion test helps: if removing a wrapper
makes complexity vanish it may be needless; if complexity spreads to callers,
it earns its place. Depth is not a line-count ratio.

Test through the interface where behavior is observable. Accept variable
dependencies at genuine seams, keep pure calculations separable where useful,
and make side effects/results understandable. Do not invent interchangeable
adapters or widen production interfaces solely to satisfy an internal mock.
One current implementation can still warrant a seam for an unavailable or
costly external dependency; justify it from observed needs.

Choose the smallest cohesive design that serves current requirements. Preserve
existing decisions unless evidence warrants reconsideration. Record
consequential choices in the spec or an ADR; propose scope changes through
`shaping` rather than performing unsolicited architecture work.
