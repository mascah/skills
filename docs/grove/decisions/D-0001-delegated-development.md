---
type: decision
id: D-0001
status: accepted
updated: 2026-09-15
applies_to: [work-planning, knowledge-context, autonomous-execution]
---
## Context
The user is evolving the Bench/Grove workflow into repo-local skills and a CLI usable across agent harnesses.

## Decision
Humans choose outcomes and constraints; agents research, plan, and execute within them. This is the user's explicit answer in the 2026-09-15 workflow review conversation. Routine stage advancement needs no extra permission; reserved human judgment and changes to the mandate remain explicit decisions.

## Alternatives rejected
- Human approval of every work unit's technical plan: adds routine coordination beyond the requested boundary.
- Unbounded agent selection of new product outcomes: exceeds the default delegation.

## Consequences
Persist intent, preparation, relationships and evidence so a new session can continue. Keep runtime orchestration optional behind a versioned contract, and make structural checks distinguishable from judgments about product quality.

## Reconsider when
The user changes the delegation for a project, outcome, or run.
