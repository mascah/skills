---
type: work
id: W-007
status: proposed
created: 2026-09-17
updated: 2026-09-17
kind: spike
size: spike
scope: [work-planning, autonomous-execution]
priority: 2
depends_on: [W-006]
---
## Question
Can a small eval suite run a Grove skill headlessly against a fixture repo and report structural outcomes and cost, so skill edits can be checked and compared instead of discovered in live sessions?

## Bounds
One fixture repo with a shaped small unit and a shaped bounded unit. One headless run per scenario, on demand only, no CI or schedule. Assertions are structural (acceptance checked, evidence present, capability updated, `grove lint` clean, branch plus handoff block) and cost-shaped (lead tokens, dispatch count, models per dispatch, fix rounds). No LLM grading of code or plan quality. Cap total spend for the spike at a few runs; record the per-run cost.

## Plan
1. Bounded lookup: what `claude plugin eval` provides (scenario format, sandbox, report, cost accounting) versus a shell script around `claude -p`, `grove status` and `grove lint`. Choose the smaller one that yields the required assertions and report.
2. Build the fixture repo from a copy of this suite's `grove init` output plus two work pages; keep it under `cli/tests/fixtures` or an equivalent gitignored path.
3. Run the small scenario and the bounded scenario (exercising the W-006 loop) once each; collect the structural assertions and cost report.
4. Run the bounded scenario a second time after a deliberate skill regression (remove the worktree rule) to confirm the suite catches it.
5. Disposition: keep, extend, or drop; name what the suite cannot see.

## Disposition

## Evidence

## Next
After W-006 closes, do step 1 and record the chosen runner before building the fixture.
