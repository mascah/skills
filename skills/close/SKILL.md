---
name: close
description: Use when implementation or investigation is finished and its evidence, project knowledge, and next action need reconciliation. Closes individual work units or a completed shared implementation in dependency order.
---

# grove:close

Read `../../references/knowledge-format.md` once.

1. Load `grove context --work <id> --phase debrief` at the default budget. Resolve any required omissions. Compare the intended outcome with the actual diff and evidence.
2. Reconcile each scoped capability to implemented behavior: update Behavior, acceptance and Code pointers, and its updated date. List deliberately unchanged capabilities under `unchanged`. Preserve a reusable lesson in its existing owner when it could prevent future rediscovery; mechanically checkable recurring mistakes belong in checks. Ordinary edits need no new knowledge page.
3. Fold answered questions into their answer's capability or decision and remove them. Record consequential changes to direction, with sources and supersession where appropriate. Pending human decisions remain explicit questions on the work they block.
4. Verify each acceptance item has evidence identifying what was checked, its result, and the relevant revision or checkout. Preserve actual human judgment with attribution when required. Check only proven acceptance boxes. A spike records its answer, limitations and disposition; promoting its code requires appropriate implementation scope. Close reconciles the selected work with its acceptance and evidence; for a release it additionally reconciles member closure and integration acceptance.
5. For a shared implementation, close prerequisites on independently proven acceptance first. Record the later joint verification in the shared plan and dependent/release evidence once those implementations exist. A release requires closed members plus its own integration and experience acceptance; member completion alone is insufficient.
6. Set status done and updated, run `grove lint`, then `grove close <id>`. Follow any refusal; the gate checks structure while the agent remains responsible for truth. Plans remain available through their references after archival.
7. Inspect the receipt and `grove status`. When a release is in scope, also check its umbrella's activation and Next state; standalone work and batches without a release have no umbrella to check. Maintain the selected focus, ordering rationale, batch recommendations and next action when the result changes them. The next action may be shaping or planning; do not silently activate it. Continue if already authorized; otherwise report the concrete next work and commit the reconciled state to the current branch.
8. Do not merge or push main. End the final message with a handoff block the human can paste into a shell or a fresh session hours later: branch, worktree path, what it contains, and the exact command for each option, so no reply in this session is needed.

```text
Branch worktree-W-NNN-slug at .claude/worktrees/W-NNN-slug: <one line on what it contains>. Options:
  Merge locally:   git -C <repo root> merge worktree-W-NNN-slug && git worktree remove .claude/worktrees/W-NNN-slug
  Open a PR:       git push -u origin worktree-W-NNN-slug && gh pr create --fill   (only when a remote exists)
  Keep the branch: nothing to do; resume with EnterWorktree path=.claude/worktrees/W-NNN-slug
If the merge conflicts, resolve or rebase, rerun grove lint and the checks, then retry.
```
