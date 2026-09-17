---
type: work
id: W-001
status: done
created: 2026-09-15
updated: 2026-09-15
started: 2026-09-15
kind: feature
size: large
scope: [work-planning, knowledge-context]
priority: 1
depends_on: []
plan: docs/plans/2026-09-15-work-map-and-planning.md
---
## Outcome
A person and a fresh agent can identify the next useful work, understand release membership and preparation, and assess selected units for one shared implementation.

## Why now
Nullsec's v4 umbrella and recorded W-011 recommendation were hidden by the old flat status view; preparation depended on unstated agent judgment.

## Constraints
Preserve existing knowledge; use current code as evidence; keep the executor optional. Implement within [[D-0001-delegated-development]].

## Design
Separate typed scope/membership/dependency relationships, structural readiness, and batch assessment. Use a shared model in status, context, lint and closure.

## Checkpoints
1. Work relationships, selection and batch assessment verified.
2. Planning and closure guidance evaluated with a shared implementation scenario.
3. Nullsec-copy migration and full local checks complete.

## Verification
Python suite, CLI scenarios, independent code/skill review, local skill validation, and a temporary nullsec knowledge copy.

## Acceptance
- [x] Status shows the selected release, dates, blockers, preparation and next work with its reason.
- [x] Batch assessment identifies sequential internal dependencies, external blockers and shared scope without claiming parallel safety.
- [x] Context retrieves parent contracts, relevant plans and required blocking questions within a reported budget.
- [x] Closure preserves references, refuses unmet acceptance and uses the same recommendation logic as status.
- [x] Updated skills guide preparation, combined implementation and human acceptance within delegated authority.

## Evidence
Verification on the implementation working tree based on d5988d6796b61a5830a6a0026dee1fa11688955c:
- Status/selection and batch acceptance: `cli/.venv/bin/python -m pytest cli/tests -q` — 100 passed, including release focus, dates, blocked questions, internal order and overlapping scope cases.
- Context and closure acceptance: the same suite covers parent contracts, plans, required omission errors, invalid metadata, historical dependencies, checked acceptance and refusal of unresolved relationship preparation.
- Skill acceptance: independent account-import scenario exercised missing/shared plans, sequential dependent closure, retained plan references and the human release gate in an isolated CLI fixture.
- Packaging: all five skill validators and the Codex plugin validator passed; `python3 __init__.py` registered all five skills; `grove --version` returned 0.2.0.
- `grove lint` — 0 errors, 0 warnings; `git diff --check` — clean.
- Full observations, reviewer fixes and nullsec-copy measurements: [[2026-09-15-workflow-evaluation]].

## Next
W-002 and W-003 can be planned as one implementation, with contract export before run ownership/recovery.
