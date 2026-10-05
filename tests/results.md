# Refactor verification record

Baseline: `045a78f`; implementation branch: `refactor/mascah-skills`.
Date: 2026-10-05. Runtime: Codex with fresh-context evaluation agents and local
Python 3.13.12. No installed upstream plugin was invoked.

## Baseline and core checkpoint

Suite state: stage-2 candidate after `c76042e` (eight skills; dirty implementation
files on this branch). Stage-2 commit contains the exact candidate and this record.

Baseline evaluation applied legacy work/setup and upstream to-spec to temporary
projects. The supplied normalization bug reproduced (`'A' != 'a'`). Legacy work
required Grove/work identity and could not proceed; setup required the absent
CLI. Upstream to-spec's tracker publication/readiness defaults exceeded a local
draft request. No forbidden commands or external writes were performed by the
evaluator. Setup idempotence was not exercised at baseline. Raw report for this
session: `/private/tmp/mascah-baseline-_dk73jzp/report.md`.

Core forward-test used all eight new skills in four isolated temporary git
worktrees. Parent inspected the report and reran the bug's final three tests:

| Exercise | Observed actions and result |
| --- | --- |
| Issue-only bug (`implement`, `tdd`, `code-review`) | Added a literal regression through public normalize; three tests ran with one meaningful failure, then all three passed after `.lower()`. Only implementation/test changed; no spec, plan or setup. |
| Setup rerun | Preserved custom paths, local-only tracking, unrelated AGENTS/workflow content and byte-identical delegating CLAUDE. Second pass produced identical full file hashes and one pointer. |
| Settled shaping (`shaping`, `domain-modeling`, `codebase-design`, `to-spec`) | Used existing terms/interfaces; no unnecessary interview, glossary, ADR or implementation. Saved only custom-path spec. |
| Delivery extraction (`to-spec`) | Moved six rollout slices into one linked plan, repaired acceptance links, kept requirements byte-identical and no duplicate sequence. |

Raw report/inventories: `/private/tmp/mascah-core-eval-_sfw5qf5/` (report.md,
per-fixture before/after hashes, uncommitted fixture worktrees). Evidence is
agent-executed application of instructions, not a deterministic setup runtime.
The evaluator's temporary helper proves this setup execution's idempotence;
damaged markers, changing preferences and concurrent edits were not exercised.

Core distribution: `python3 scripts/validate.py` reported eight skills/zero
errors; `python3 -m unittest discover -s tests -v` passed 12 checks against copied
trees and mutations; `python3 __init__.py` registered the eight expected skills;
`git diff --check` passed. The validator clean-copy test first failed because
the validator was absent. After implementation, broken reference, helper,
anchor, metadata, version, release target, Hermes inventory, escaping path and
retired instruction fixtures were rejected. Claude manifest validation passed
with the expected warning that root CLAUDE.md is not plugin context (it is
repository guidance, while reusable context ships in skills/references).

The first stage-1 commit unexpectedly triggered the existing legacy lefthook
and ran Grove lint/172 legacy tests. That invocation was an execution mistake,
not new-suite verification. Stage 2 replaces those hook/CI commands; later
commits use only the replacement checks.
