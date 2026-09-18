---
type: work
id: W-014
status: proposed
created: 2026-09-18
updated: 2026-09-18
kind: feature
size: bounded
scope: [work-planning]
priority: 2
depends_on: []
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
- [ ] Regression fixtures reject a declaration delivering a still-proposed unit, active unit, done-but-unarchived unit, abandoned unit, missing ID or invalid closure evidence/relationships; a properly closed committed delivery passes.
- [ ] Uncommitted closure cannot make an open committed candidate pass. Advancing the branch after a previous pass validates the newly resolved candidate, and output identifies exactly which commit was checked.
- [ ] Missing/malformed/inapplicable or inherited stale declarations fail actionably. A multi-unit delivery with one unfinished declared unit fails; explicit partial delivery passes only for its properly closed subset and reports remaining work.
- [ ] The check runs read-only in a fresh clone without claims or local executor state and reports equivalent results for the same committed inputs through text/JSON and exit status.
- [ ] Shared closure validation retains dependency, release-member, blocking-question, acceptance/disposition, evidence and capability-reconciliation requirements without moving files or automatically closing tasks.
- [ ] Close instructions commit closure and delivery metadata, then validate before successful completion handoff. A representative lifecycle walkthrough demonstrates failure on omitted closure and success after repair, with limits on merge enforcement and human judgment stated.
- [ ] Focused validator/CLI regression tests, the full existing CLI suite, grove lint and plugin validation pass; actual commands and tested revision are recorded.

## Evidence
Shaping only, 2026-09-18: builder's repeated missed-closure report and acceptance of a separate check, with possible PR automation later. Inspected skills checkout c88b228: cli/grove/close.py, cli/grove/cli.py and skills/close/SKILL.md. The current close gate validates only when called; the skill handoff offers raw Git merge commands. No validator implementation or verification performed.

## Next
Prepare with W-013 via grove batch W-013 W-014. Inspect close/work/index and Git contract helpers; choose the committed declaration contract, candidate/base validation, historical closure checks and partial-delivery semantics in a shared plan. Implement sequentially where CLI and lifecycle instructions overlap; W-014 can ship independently of claims. PR automation and a merge wrapper remain later options.
