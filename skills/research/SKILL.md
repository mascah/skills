---
name: research
description: Use when investigating a bounded question that needs source evidence, current API facts, or durable findings.
---

# Gather evidence for a decision

Read [common discipline](references/discipline.md). Identify the question,
why its answer matters, constraints and what would change the next useful action.
Reuse relevant local findings and prior decisions, verifying them against current
sources instead of repeating settled research or trusting stale conclusions.

Use primary sources: actual code, official docs, specifications, original papers
or first-party data. Check unstable API/product facts against current sources;
record date/version/revision and link each consequential claim to its evidence.
Separate observations, source claims, inferences and unresolved uncertainty.
When sources disagree, state the conflict and investigate enough to identify
which applies. Do not imply unavailable sources were inspected.

Choose a bounded search or experiment that can answer the question. Honor caller
delegation policy; research works directly without background tools or fixed
fan-out. Stop when further investigation is unlikely to change the recommendation,
or report the precise input needed to proceed. Do not invent certainty to finish.

Return findings, source-backed recommendation, limits and next useful action.
Persist only when future use warrants it, at the project's existing research
location or in the effort's discovery notes. Move settled intent/decisions to
the appropriate spec, domain glossary or ADR and link rather than
maintaining duplicates. Research may answer, defer or contradict an idea; it
does not automatically create tickets, authorize implementation or publish.
