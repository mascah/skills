---
name: shape
description: Use when researching an uncertainty, selecting the next investment, or preparing Grove work and releases. Captures intent, relationships, and enough design for the next activity. Open ideas without a selected outcome belong to grove:explore.
---

# grove:shape

Read `../../references/knowledge-format.md` and `../../references/sizing.md` once. Use `../../references/planning.md` when preparing implementation or combining work.

## Discover and decide

Start with `grove status`. State the useful destination: answer a question, select work, or prepare an authorized outcome; an open idea with no selected outcome belongs to `grove:explore`. Load `grove context --work <id> --phase shape`; without a work unit, use `grove find <topic>` to locate the owning knowledge. Inspect relevant code and evidence before asking about facts you can investigate.

Connect the proposed outcome to current behavior, user evidence, and project ambition. Identify the consequential uncertainty and the decisions that depend on it. Investigate with a bounded source lookup or experiment when the answer could change the next action. Test assumptions against concrete user, failure, and recovery scenarios. A recommendation sitting in a draft page is a draft until tested the same way. Code, data and placeholder content show what the checkout does, not what the project intends; cite them as design only when a capability or decision page owns them. When preparing, compare credible alternatives for consequential technical choices and recommend one with its trade-offs and reconsideration condition.

Humans choose outcomes and constraints; agents research, design, plan, and execute within the recorded mandate. Ask only for missing preferences or decisions outside that mandate. One consequential question is often sufficient; batch independent choices when useful. A missing technical detail is an investigation task.

## Persist and order

Before the first write, enter a worktree branch: use the harness's native `EnterWorktree` when it exists, otherwise `git worktree add`, with the same detection `references/discipline.md` uses. With no work ID yet, name it for the topic (`worktree-shape-<slug>`).

Update the existing owning capability, decision, or term as meaning settles. Capabilities describe implemented behavior; proposed work holds intended changes. Record consequential choices with sources and rejected alternatives. Fold answered questions into their durable answer and remove them; unresolved blocking questions name the affected work IDs.

Create or refine work with the smallest honest size. Capture Outcome, Constraints, Acceptance, and the Design needed to understand the change. Distinguish capability `scope`, ordered release `members`, and `depends_on` prerequisites. A release's final acceptance gate does not automatically block its members. Specify blockers on the work they actually prevent.

Set brief `focus`, priority and `Why now`, and concrete Next actions, including for proposed work. Preserve creation dates; unknown migrated dates stay unknown. Put shared implementation candidates under the same `batch` with a `batch_reason`, then run `grove batch <ids>`. Inspect interfaces and write ownership before recommending parallel execution. One implementation may contain sequential dependent tasks.

For an existing schema-1 project, run `grove upgrade` before adding the new metadata. Translate prose relationships from evidence; do not infer dependencies from numeric IDs or common scope. Where ordering is ambiguous, surface the gap.

Run `grove lint` and `grove status`. Explain the next useful action, its reason, blockers, and which items can be planned together. Continue into planning or implementation when already authorized. Commit the resulting knowledge on the branch with a Conventional Commits `docs` subject, then end the final message with the handoff block `skills/close/SKILL.md` uses (branch, worktree path, what it contains, merge/PR/keep options).
