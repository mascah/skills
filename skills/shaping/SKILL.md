---
name: shaping
description: Use when an idea or change needs clearer outcomes, alternatives, constraints, terminology, or acceptance before implementation.
---

# Shape the intended change

Read [common discipline](references/discipline.md). Use the existing
conversation, spec, code, domain language and prior decisions as the starting
point; do not restart an interview just because this is a new session.

Establish who needs what outcome, why it matters, and what counts as success.
Separate settled facts from assumptions. Investigate questions answerable from
the checkout yourself. Ask focused questions only about consequential unknowns,
trade-offs or intent; combine related questions when that helps the user decide.
Offer a recommendation with concrete alternatives and costs when useful.

Stress-test the proposed behavior with realistic examples, including failure
and recovery where relevant. Resolve ambiguous terms with
`domain-modeling`; compare interfaces with
`codebase-design` only when design needs it.
Preserve established vocabulary and decisions unless new evidence justifies
revisiting them. Ask for changed intent when that affects the mandate.

If saving scope, read [Specification and Delivery](references/specification.md).
Finish with intended behavior, constraints, acceptance, selected alternatives,
consequential decisions, open questions and out-of-scope work. An already clear
idea may need only a short synthesis. When persistence is useful, use
`to-spec` to save settled intent; do not force another
interview. When evidence undermines the premise, answer, defer or abandon with
the reason. Shaping alone authorizes neither implementation nor publication.

Named helpers are optional. Without `domain-modeling`, resolve ambiguous terms against concrete examples and record meaningful definitions. Without `codebase-design`, compare caller-facing alternatives and costs. Without `to-spec`, save settled intent directly using the bundled Specification and Delivery guidance.
