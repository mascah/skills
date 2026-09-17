---
type: work
id: W-008
status: done
started: 2026-09-17
created: 2026-09-17
updated: 2026-09-17
kind: tooling
size: small
scope: [work-planning]
priority: 1
depends_on: []
---
## Outcome
Exploring an open idea with a human is its own skill, `grove:explore`, that never loads the preparation checklist: it contributes ideas in prose, tests draft recommendations before repeating them, cites code as checkout facts rather than design, and writes to the knowledge tree only when the human says a point is settled or leaning. `grove:shape` keeps answering questions, selecting work and preparing outcomes.

## Why now
A shaping session on a creative question (nullsec W-015, 2026-09-17) followed shape's preparation instructions line by line: an option menu with a recommendation copied untested from a draft page, a question with options every turn, an Evidence append and commit after every exchange, and prototype reward values cited as economy design. The human called the session unhelpful and reverted the commits. Shape names "explore possibilities" as a destination but every later instruction is written for preparing; a gate inside one skill would leave that text loaded. A separate skill removes it from context and makes the exploring/preparing choice the human's slash command.

## Constraints
The explore skill stays short: status, context, find, the conversation rules, the one-write-on-settle rule, and a handoff to `grove:shape` when the human selects. No new size in sizing.md and no CLI change. Shape's description drops exploring so both skills do not trigger on the same request. Shape keeps two general rules that apply when preparing too: a recommendation in a draft page is a draft until tested against the brief and a concrete user; code, data and placeholder content are cited as design only when a capability or decision page owns them.

## Acceptance
- [x] `skills/explore/SKILL.md` exists with the rules above and ends by handing off to `grove:shape` once the human selects.
- [x] `skills/shape/SKILL.md` no longer claims exploring in its description, scopes "compare credible alternatives" to preparing, and carries the draft-recommendation and code-as-fact rules.
- [x] README's loop lists explore before shape; the work-planning capability page names the split and its Code list includes the new skill.
- [x] `grove lint` passes and the change is delivered on a branch with the close handoff block.

## Evidence
- 2026-09-17, branch worktree-W-008-explore-skill (base 2785829, tested 062cfef): added `skills/explore/SKILL.md` (status/context/find, prose-only conversation rules, draft-page and code-as-fact rules, write only on a settled or leaning point, handoff to grove:shape). Shape's description and destination sentence drop exploring and point at explore; "compare credible alternatives" is scoped to preparing; the two general rules are added to shape's discover paragraph; the "exploratory idea can remain broad" sentence is removed. README loop lists explore before shape; work-planning capability names the split and lists the new skill under Code. Diff read back against Acceptance by the implementing agent.
- `grove lint`: 0 errors, 0 warnings. `cd cli && uv run --with pytest python -m pytest -q tests`: 117 passed. The managed guidance block in cli/grove/init.py lists no skills, so downstream repos need no `grove init` rerun.
- Not done here: nullsec's W-015 Bounds and Plan still encode the per-session commit and candidate menu; that rewrite is in the other repo.

## Next
Human integrates the branch from the handoff block, then in nullsec rewrites W-015's Bounds ("every session ends with premise.md committed") and Plan ("candidates, then builder's choice") to match explore and runs the next W-015 session with `grove:explore`.
