---
type: work
id: W-014
status: done
created: 2026-09-18
started: 2026-09-18
updated: 2026-09-18
kind: feature
size: bounded
scope: [work-planning]
priority: 2
depends_on: []
plan: docs/plans/W-013-W-014-worktree-completion.md
batch: worktree-completion
batch_reason: Shared lifecycle instructions and a joint claim-to-closed-handoff scenario; prepare together and serialize edits to CLI and skills.
---
## Outcome
A branch cannot receive a successful Grove completion handoff while any work it declares delivered is still proposed, active, unarchived or missing required closure records. The same read-only check can validate a committed candidate in a clean clone and later run on PRs.

## Why now
The builder reports two cases of completed code merged to main while the task remained proposed because the branch had not closed it. The close instruction already exists; an executable committed-state check is the selected protection. [[D-0003-worktree-claims-and-handoff]]

## Constraints
No automatic closure, merge, push, local merge wrapper or CI/branch-protection installation. No dependency on shared local claims, process state or dirty working files. Preserve human acceptance requirements: structural validation cannot prove their truth. Partial integration is allowed only when delivery and unfinished work are explicit. No implicit claim that direct git merge is blocked.

## Design
Introduce a versioned, committed delivery declaration identifying the work delivered by the branch and explicitly retained unfinished work when relevant. Planning must choose its location, identity/base semantics and freshness rules so a declaration inherited from an earlier branch cannot silently validate an unrelated delivery. Local claims can help prepare/check completeness when available, but the portable validator cannot depend on them. Document the limit that declared work and repository structure cannot prove every code change has been attributed honestly.

Resolve the supplied candidate ref to a commit once and validate that committed tree, with the comparison base/target needed by the selected declaration contract. Report the resolved commit and covered work. Reject missing, malformed, ambiguous or inapplicable declarations. Do not trust an older successful receipt or closure that exists only in the worktree/index. Avoid a self-referential requirement to embed the final commit hash in its own committed declaration; bind validator output to the resolved commit instead.

Each delivered ID must resolve uniquely to archived, successfully closed work in the candidate tree. Check applicable closure invariants for acceptance or spike disposition, evidence, capability reconciliation or unchanged scope, blockers, prerequisites and release members. Factor reusable validation from cli/grove/close.py where appropriate instead of letting two closure policies drift; never mutate/archive work during validation. Validate recorded completion against its completion metadata rather than treating every later capability change as a fresh closure obligation. A multi-unit branch must account for all declared delivery; an open release umbrella is not delivered merely because some members close. An abandoned unit cannot satisfy successful delivery or prerequisites.

Have the close workflow prepare the declaration, commit reconciled closure, run the validator against that commit and only then print a successful completion handoff. A failure leaves an actionable repair/resume path. A partial handoff names the closed delivered subset and pending work clearly. Return deterministic exit status plus human-readable and machine-readable results usable by future PR checks. Direct Git merges remain outside this check's enforcement.

## Acceptance
- [x] Regression fixtures reject a declaration delivering a still-proposed unit, active unit, done-but-unarchived unit, abandoned unit, missing ID or invalid closure evidence/relationships; a properly closed committed delivery passes.
- [x] Uncommitted closure cannot make an open committed candidate pass. Advancing the branch after a previous pass validates the newly resolved candidate, and output identifies exactly which commit was checked.
- [x] Missing/malformed/inapplicable or inherited stale declarations fail actionably. A multi-unit delivery with one unfinished declared unit fails; explicit partial delivery passes only for its properly closed subset and reports remaining work.
- [x] The check runs read-only in a fresh clone without claims or local executor state and reports equivalent results for the same committed inputs through text/JSON and exit status.
- [x] Shared closure validation retains dependency, release-member, blocking-question, acceptance/disposition, evidence and capability-reconciliation requirements without moving files or automatically closing tasks.
- [x] Close instructions commit closure and delivery metadata, then validate before successful completion handoff. A representative lifecycle walkthrough demonstrates failure on omitted closure and success after repair, with limits on merge enforcement and human judgment stated.
- [x] Focused validator/CLI regression tests, the full existing CLI suite, grove lint and plugin validation pass; actual commands and tested revision are recorded.

## Evidence
Shaping only, 2026-09-18: builder's repeated missed-closure report and acceptance of a separate check, with possible PR automation later. Inspected skills checkout c88b228: cli/grove/close.py, cli/grove/cli.py and skills/close/SKILL.md. The current close gate validates only when called; the skill handoff offers raw Git merge commands. No validator implementation or verification performed.

- 2026-09-18 T3 (`cli/grove/close.py` factored into `closure_errors` plus `record_delivery`, `cli/grove/delivery.py`, `cli/grove/cli.py`, `cli/tests/test_close.py`, `cli/tests/test_delivery.py`, one `git_init` line in `cli/tests/test_workflow.py`), base cb834c7: implementer Agent `model: sonnet`; task reviewer `model: opus` a2 fix (1 blocking: close renamed the page into history before the declaration write could fail; 11 minor), a3 accept. 2 fix rounds, both on the same sonnet implementer. Evidence: suite 169 passed, `grove lint` 0 errors, `claude plugin validate .` passed. Tests in real temp git repos: properly closed committed delivery passes; still-proposed, active, done-but-unarchived, abandoned, missing and invalid-closure ids rejected; uncommitted closure does not make an open committed candidate pass; advancing the branch re-checks the new sha and `checked <sha>` names it; inherited declaration exits 2; multi-unit delivery with one unfinished unit fails; explicit `retains` partial delivery passes for the closed subset and reports the rest; a fresh `git clone` gives the same JSON and exit status; freshness uses merge-base so another branch's merged declaration does not make a correct branch ambiguous; unresolvable base exits 2; detached HEAD refusal leaves the live page in place.
- 2026-09-18 T4 shared with W-013 (close SKILL.md: `grove close` writes closure and the declaration, a commit step, then `grove verify-delivery` with repair and recommit before the handoff, which carries `grove claim --release` and names `retains`; discipline.md limits: structure and references only, direct `git merge` bypasses; init BLOCK line; workflow test), base 312a946: implementer Agent `model: sonnet`; reviewer `model: opus` a1 fix (1 blocking on step order), a2 accept. 1 fix round. Suite 170 passed, `grove lint` 0 errors, `claude plugin validate .` passed. Lifecycle walkthrough is the executable test: failure when the declaration names a still-proposed unit, success after repair.
- 2026-09-18 joint verification on this branch: `grove verify-delivery HEAD --base main` at 2e4ea5e failed (exit 1) because the validator archived only `docs/grove`, so every history page with a `plan:` under `docs/plans/` failed lint in the candidate tree. Repair dispatch (`model: sonnet`) committed f29c57c: the validator loads the whole `docs` tree plus `grove.toml`, with a regression test; suite 172 passed, lint 0 errors, validate passed. Rerun at f29c57c: `checked f29c57c…`, delivers W-010, W-011, W-012, W-015, W-013, W-014, retains W-016, `delivery verified`, exit 0. `grove claims` on this repository reports no claims: the run began before `grove claim` existed, so this branch was never claimed.

## Next
None for this unit; close writes the declaration and verify-delivery gates the handoff. PR automation and a merge wrapper remain later options (D-0003).
