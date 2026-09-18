# Discipline

Applied proportionally to size during `grove:work`: TDD, debugging, verification, and git worktrees.

## Workspace isolation
Implementation never edits main directly; concurrent sessions trample each other there. Before the first change, detect the workspace: if `git rev-parse --git-dir` differs from `git rev-parse --git-common-dir` you are already in a linked worktree, and if `git worktree list` shows one for this work ID, resume there. Otherwise create one named after the work IDs, using the harness's native worktree tool when it exists (`EnterWorktree` in Claude Code) and `git worktree add .worktrees/<ids> -b <ids>` only when it does not, after confirming the directory is gitignored. Commit everything, including knowledge-page edits and `grove close` results, to that branch. Every commit gets a Conventional Commits subject (`type(scope): summary`) with the work ID in a `Refs: W-NNN` footer and never in the subject; knowledge-only commits use `docs`, and the close commit is `docs: close W-NNN`. Do not change brief `focus` on a branch; focus belongs to shaping on main. Never merge, rebase onto, or push main yourself: the human integrates from the handoff block that `grove:close` prints. Keep the worktree on interruption. Shaping and curation may stay on main because they are short knowledge-only edits.

## Tests first where there is logic
Before changing a branch, loop, parser, or state transition, write the failing test that names the acceptance line it serves. Run it, watch it fail, implement, run it, watch it pass. A one-line change with no logic needs no new test. Small work still runs the existing suite.

## Debugging on surprise
When behavior differs from expectation: reproduce it once, read the code path that produced it before proposing a cause, form one hypothesis, test that hypothesis alone, then fix at the root. Never stack speculative fixes. If three hypotheses fail, record what was learned and seek an independent diagnosis or replan within authority. Ask the human when the resolution changes their outcome or constraints, needs their judgment, or exhausts the authorized options.

## Lead never debugs
For bounded and large work the lead does not run a test-fix loop itself: a failing check returns to a dispatched implementer with the finding attached, and the debugging rule above (one hypothesis at a time, three failures then stop) applies inside the implementer. Small work keeps the existing in-session rule.

## Verification before any claim
"Done", "passing", "fixed" are said only after performing the verification that proves it in this session and reading its result. Record commands, results and tested revision in Evidence. Human acceptance uses the actual attributed response; a command cannot establish taste or usability judgment. If a check was skipped, say so in Evidence.

## Review at bounded and large
Before close the branch is reviewed as a whole. For bounded and large work the dispatched whole-branch review does this, and the lead reads its review file, not the full diff, checking that it covers whether the change does only what the work unit says, each acceptance line has evidence, and no capability's behavior changed without its page changing.

## Subagents
Allowed for independent investigation or parallel implementation. For bounded and large work the controller loop requires them; small work can still finish in-session. The interactive lead still owns the work unit file, the evidence, and the close.

## Context hygiene
Read the knowledge tree only through `grove status`, `grove context`, and `grove find`. When context reports an omission you need, fetch that one file; do not read the directory.
