---
type: capability
id: knowledge-context
status: settled
updated: 2026-09-15
---
## Behavior
The CLI retrieves scoped work, current capabilities and decisions, related work summaries, parent contracts, required blocking questions, and attached plans. Planning has a phase alongside shaping, implementation, debugging and debrief. Release shaping summarizes capabilities to reduce unnecessary detail. Required omissions are reported with recovery paths. History stays out of normal retrieval except named completion summaries.

Schema 2 introduces work-map metadata while schema 1 remains readable. Upgrade changes only the schema declaration; the agent translates legacy relationships from evidence. Current meaning is reconciled into its existing owner after work; useful recurring invariants may become checks. [[D-0001-delegated-development]]

## Acceptance
- [x] Parent constraints and blocking questions cannot disappear silently from a constrained context budget.
- [x] Plans referenced by work are retrieved for planning, implementation, debugging and debrief.
- [x] Archived prerequisites can be summarized without loading their full historical documents.
- [x] Schema upgrade preserves other configuration content.

## Limits
Token estimates use character count divided by four. The budget measures included source text rather than the entire rendered response. Broad capability scope may still require a larger budget. Lookup and lint validate structure rather than semantic truth.

## Code
- cli/grove/context.py
- cli/grove/pages.py
- cli/grove/init.py
- cli/tests/test_workflow.py
