---
name: domain-modeling
description: Use when resolving ambiguous domain language, changing a glossary, or recording a consequential design trade-off.
---

# Sharpen the domain language

Read the project's workflow, glossary or context map, relevant ADRs and code.
Use [artifact ownership](../../references/artifacts.md) and
[execution](../../references/execution.md) for writes. This discipline changes
the model; merely reading an existing glossary needs no separate session.

Challenge overloaded terms with specific scenarios. For example, does an
"account" mean a customer relationship or a login identity? Ask about intent
when established definitions conflict; check claims about current behavior
against code without silently treating current code as the intended design.
Distinguish neighboring concepts, lifecycle transitions and relationships.

Record resolved terms in the existing glossary, or lazily create `GLOSSARY.md`.
Each entry gives a canonical term, definition, meaningful distinctions and a
domain example when useful. Keep implementation details, scope and progress in
their owning documents. Follow existing context-specific locations in larger
projects rather than inventing a new taxonomy.

For a consequential trade-off that future maintainers would otherwise
misunderstand, record an ADR with context, decision, alternatives, rationale,
consequences and a reconsideration condition. Routine reversible choices need
no ADR. Link from the spec instead of copying the rationale. Reflect newly
resolved language in the affected spec and examples. Return the resolved terms,
decisions and any consequential ambiguity still preventing implementation.
