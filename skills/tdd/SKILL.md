---
name: tdd
description: Use when implementing behavioral changes test-first, reproducing bugs, or improving regression tests through observable interfaces.
---

# Test behavior first

Read project check conventions, vocabulary and relevant acceptance. Apply
[verification obligations](../../references/execution.md). Select the highest
useful observable interface that catches the behavior; adopt existing test
patterns. Routine seam choices need no additional approval when scope is clear.
For unresolved interface design, consult [codebase-design](../codebase-design/SKILL.md).

Work in small vertical cycles:

1. Write one regression or acceptance test with expected results from the
   requirement or an independently worked example. Name the production defect
   that would make it fail.
2. Run it before the fix. Inspect the failure: it must demonstrate missing or
   wrong behavior, not a typo, import failure, or broken fixture. A test already
   passing is evidence of existing behavior, not a red cycle.
3. Write only enough implementation to pass. Run the test and relevant checks.
4. Refactor while keeping checks green, then repeat for the next behavior. Run
   the appropriate project suite before claiming completion.

Example: supplied scope says `normalize(' A ') == 'a'`. Exercise the public
function with that independent literal; observe `'A' != 'a'`, add lowercase
normalization, and rerun. Also preserve relevant existing behavior.

Prefer real behavior over internal mocks, private methods or assertions that
recompute the implementation. Use fakes/stubs for unavailable external systems
at a real boundary, and state what the fake cannot prove. Avoid tests that
merely mirror wording, constants or implementation structure.

Documentation and mechanical configuration use proportionate checks. If code
was written before the test, report tests-after honestly; do not invent a red
run. When claiming a test-first cycle, demonstrate the meaningful failure and
subsequent pass. Never discard useful authorized work merely to reenact a ritual.
