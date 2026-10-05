---
name: prototype
description: Use when a disposable experiment can answer a bounded design, logic, usability, or technical feasibility question.
---

# Build an experiment that answers a question

Read [mandate](references/workflow.md),
[artifact ownership](references/artifacts.md), and
[execution](references/execution.md). Establish the question, scope, limits
and observable evidence before building. If those are already supplied, proceed
within them without reopening intent. Ask only when ambiguity changes the probe.

Choose the simplest artifact that exposes the decision: a small script for a
technical property, state transitions for logic, or a runnable visual for UI.
Use project tooling where practical; keep the experiment in an isolated branch
or scratch location, clearly marked disposable. Provide a simple run command
and show relevant state/results. Do not introduce production routes, credentials,
data writes or dependencies beyond the experiment's authorized bounds.

Run representative cases that answer the question, including its important
failure conditions. Verification can be a small executable assertion, measured
result or visual observation; avoid a production framework or polish that adds
no evidence. Describe mocks/simplifications and what they cannot establish.
Preserve failure evidence when it changes the conclusion.

Report question, artifact/run instructions, observed result, verdict and limits.
Persist useful findings or precise decision-rich snippets in discovery, spec or
ADR as appropriate, linking disposable artifact/revision when worth retaining.
Keep production changes a separate authorized decision; a promising prototype
is not automatically promoted or merged. For a failed premise, defer/abandon
with the evidence instead of manufacturing implementation work.
