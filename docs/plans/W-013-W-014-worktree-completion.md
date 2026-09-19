# W-013 + W-014 — shared worktree claims and completion-handoff check

Execution: Controller loop; four sequential tasks T1→T4, no overlap.
Reason: T1-T3 each own disjoint CLI modules but share `cli/grove/cli.py`, `close.py` and the test fixture; T4 edits guidance that W-015 also touches on this branch, so it runs last and additively.
Delegation: Fresh implementer (sonnet) and fresh task reviewer (opus) per task; the lead owns work pages, evidence and close.
Runtime: Interactive session; no executor. Real temp git repos in tests, never the live checkout.
Reassess: If `git archive` of a candidate tree cannot be loaded by `load_root` unchanged (T3), fall back to per-file `git show` reads; if the O_EXCL lock proves flaky on the shared metadata dir, switch to `os.replace` with a compare-and-swap on file mtime. Neither changes the commands.

Inspected base: `82d4b16` on 2026-09-18, after W-015 is planned for this branch. `batch W-013 W-014`: no blockers, both needed a plan; shared scope work-planning. No hard dependency; W-014 ships without claims.

## Settled design

### W-013 claims registry
- Location: `<git rev-parse --git-common-dir>/grove/claims.json`; per-checkout owner token in `<git rev-parse --git-dir>/grove-owner` (the per-worktree gitdir), created on first acquire with `secrets.token_hex(8)`. The agent never carries a token; same worktree = same owner, so retry and resume are safe by construction.
- Format: `{"schema": 1, "claims": {"W-013": {"branch": "worktree-W-013", "worktree": "/abs/path", "owner": "hex", "acquired": "2026-09-18T10:00:00+00:00"}}}`. Malformed JSON → `GroveError("claims registry unreadable: <path>; fix or remove it by hand")`; never deleted or rewritten by the CLI.
- Atomicity: `os.open(lock, O_CREAT|O_EXCL)` on `<common>/grove/claims.lock` around read→check→write-temp→`os.replace`; lock removed in `finally`. Lock present → refuse with the lock path (`another grove is writing claims; retry, or remove <lock> if none is running`). No expiry of claims; the lock is held only for the mutation. `# ponytail: one global lock; fine for a handful of worktrees`.
- Commands, `cli/grove/claims.py`, registered in `cli.py`:
  - `grove claim <ids...> [--json]` acquires the whole set or nothing. Already owned by this owner → no change, exit 0. Owned by another → refuse all, exit 4 (reuse the run "owned elsewhere" code), listing branch/worktree per conflict. Records branch (`git rev-parse --abbrev-ref HEAD`) and worktree (`git rev-parse --show-toplevel`).
  - `grove claim --release <ids...>` releases only claims owned by this checkout; a foreign claim is refused with its owner's branch and the `--take` hint. `grove claim --take <ids...>` re-acquires for this checkout regardless of owner, printing what was taken; this is the explicit recovery path.
  - `grove claims [--json]` lists every claim with an observation: `worktree missing`, `branch gone`, `integrated` (branch is an ancestor of this checkout's HEAD), `closed on branch, awaiting integration` (`git cat-file -e <branch>:<history path>`), `active on branch` / `proposed on branch` (status read from `git show <branch>:<work path>`), or `possibly squash-merged: verify and release with --take` (history page present at HEAD while the branch is not an ancestor). Observations read committed files only and are labelled `committed on <branch>`; nothing executes in another checkout.
- Status overlay (`status.py`): `status()` adds `claims` (the same observations) and each work row gains `claim: {...}|None`. Render appends `claimed on <branch> (<worktree>) · <observation>` under the row. The recommendation skips work claimed by another owner and says `resume or coordinate: claimed on <branch>`. Readiness, blockers and prerequisites are untouched; a closed-on-branch observation never counts as `closed`.
- Cleanup after integration: `grove claim --release` from the worktree, or `--take` then `--release` from main when the worktree is gone. `grove claims` shows `integrated` so the human knows it is safe.

### W-014 delivery declaration and validator
- Declaration: `docs/grove/deliveries/<branch>.json` (JSON, so `Root.pages` ignores it): `{"schema": 1, "delivers": ["W-013", "W-014"], "retains": ["W-015"]}`. `retains` lists declared-unfinished work the branch touched (explicit partial delivery). `grove close <id>` appends the id to this file for the current branch and prints the path; the agent adds `retains` by hand when needed.
- Freshness rule: the validator only accepts a declaration file that changed between base and candidate (`git diff --name-only <base>..<candidate> -- docs/grove/deliveries/`). Zero changed → `no delivery declaration on this branch`; more than one → `ambiguous`; malformed JSON → `malformed`. All exit 2. A declaration inherited from an earlier branch is therefore inapplicable by construction, with no commit hash embedded.
- Command: `grove verify-delivery [CANDIDATE] [--base REF] [--json]`, `cli/grove/delivery.py`; candidate defaults to `HEAD`, base to `main`. Resolves both once (`git rev-parse --verify`), prints `checked <sha>` first. Loads the candidate tree read-only: `git archive <sha> grove.toml docs/grove | tar -x -C <tmpdir>` (stdlib `tarfile`), then `load_root(tmpdir)` so lint and `WorkIndex` run unchanged on committed content only; uncommitted closure cannot leak in.
- Checks per delivered id, on the candidate root: page resolves uniquely, is in `history/work` with `status: done` (proposed/active/unarchived/abandoned/missing all fail with the state named), was not already in history at base (`git cat-file -e <base>:<history path>` must fail), and `closure_errors(root, work)` is empty. Each `retains` id must exist and not be closed. Lint on the candidate root must have 0 errors. Any failure → exit 1 with one line per failure; text and `--json` carry the same list plus `checked`, `base`, `delivers`, `retains`.
- Shared closure policy: factor `close.py` into `closure_errors(root, work) -> list[str]` (status done, blockers and relationship gaps, acceptance/disposition, evidence, capability staleness vs `unchanged`) and have `close()` raise on the first non-empty result exactly as today, then rename. The validator calls `closure_errors` only; nothing moves or is archived.
- Limits stated in guidance: the check proves structure and references, not the truth of human judgments; direct `git merge` bypasses it.

### Guidance (T4, additive to W-015's text)
- `references/discipline.md`: claim before the first change (`grove claim <ids>` in the worktree), release after integration, `--take` for recovery; a claim is ownership, not liveness.
- `skills/work/SKILL.md` Prepare step 1: refuse to start work `grove status` shows claimed elsewhere; acquire the batch.
- `skills/close/SKILL.md`: step 6 commits closure plus the declaration `grove close` wrote; new step: `grove verify-delivery` against the committed branch, repair on failure, and only then the handoff block, which now also carries `grove claim --take <ids> && grove claim --release <ids>` after the merge line, since the worktree's owner token is gone once it is removed. Partial handoff names `retains`.
- `cli/grove/init.py` BLOCK: one line: `Claim work before changing it (grove claim <ids>) and run grove verify-delivery before handing a branch to the human.`

## Tasks
- T1 (W-013 acceptance 1, 2, 4): `cli/grove/claims.py`, `cli/grove/cli.py`, `cli/tests/test_claims.py`. Fixture: `git_init(root)` then `git worktree add <tmp>/wt-a -b a` and `wt-b -b b`; assert the same claim from all three checkouts, atomic multi-id refusal with no partial write, same-owner retry, foreign release refused, `--take`, missing-worktree/branch-gone/malformed diagnostics. Concurrency: two threads on `claim` for the same id → exactly one owner.
- T2 (W-013 acceptance 3, 5): `cli/grove/status.py`, `cli/grove/claims.py` (observations), `cli/tests/test_status.py`. Assert text and JSON carry the claim, prerequisites of main are not satisfied by a closed-on-branch observation, recommendation skips foreign claims, `integrated` and `possibly squash-merged` labels.
- T3 (W-014 acceptance 1-5): `cli/grove/close.py` (factor + write declaration), `cli/grove/delivery.py`, `cli/grove/cli.py`, `cli/tests/test_close.py`, `cli/tests/test_delivery.py`. Fixture: commit the fixture repo, branch, close W-001 via `close()`, commit, verify passes; variants reject proposed, active, done-unarchived, abandoned, missing, bad evidence; uncommitted closure fails; advancing the branch re-checks the new sha; inherited declaration exits 2; partial delivery with `retains`; run in a fresh `git clone` of the temp repo.
- T4 (W-013 acceptance 6, W-014 acceptance 6, 7): guidance files above, `cli/tests/test_init.py` block assertion, and one end-to-end test in `cli/tests/test_workflow.py`: claim → close → declaration → verify → release. Then full suite, `grove lint`, `claude plugin validate .`.

## Joint verification
The T4 workflow test plus the lead's recorded run of `grove claims`, `grove status` and `grove verify-delivery` on this very branch before its own close.

## Recovery
On interruption read `.grove-run/ledger.md` for the last accepted task, `git diff --stat`, and resume the next task; the claim/delivery modules are independent, so a half-done T3 does not invalidate T1/T2 evidence.
