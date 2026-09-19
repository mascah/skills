---
name: explore
description: Use when thinking through an open idea, a creative direction, or a question whose answer is a human's taste or preference, before any work is selected. A conversation that contributes ideas and writes only what the human settles.
---

# grove:explore

Start with `grove status`. Load `grove context --work <id> --phase shape` when a work unit owns the idea; otherwise `grove find <topic>` for the owning knowledge. Do not read `../../references/planning.md` or `../../references/sizing.md`; nothing here is being prepared.

Exploring is a conversation, not preparation. Contribute ideas in prose. Take one idea seriously and push it until it breaks rather than laying out candidates, and ask a question only when the human's reactions do not already answer it. No option menus, no comparison tables, no recommendation ranked against alternatives.

A recommendation sitting in a draft page is a draft. Test it against the brief and a concrete user before repeating it. Code, data and placeholder content show what the checkout does, not what the project intends; cite them as design only when a capability or decision page owns them.

Write nothing to the knowledge tree until the human says a point is settled or leaning. Before that first write, enter a worktree branch: use the harness's native `EnterWorktree` when it exists, otherwise `git worktree add`, with the same detection `references/discipline.md` uses; with no work ID yet, name it for the topic (`worktree-shape-<slug>`). Then record that point once, in its owner, and commit on the branch with a Conventional Commits `docs` subject, ending the final message with the handoff block `skills/close/SKILL.md` uses. Evidence holds settled points and the human's actual reactions, never a turn log. If no idea lands, say so and record the reaction only when asked.

When the human selects an outcome, continue with `grove:shape` to prepare it.
