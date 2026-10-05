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

## Tracker and whole-spec execution

Stage-3 candidate: eleven skills after `311ce59`, with stage-3 files dirty.
The final completion commit records the unchanged tested skill content.
Fresh-context evaluator's report and command/call recordings are under
`/private/tmp/mascah-tracker-eval/evidence/` (report.md, commands.jsonl,
gh-calls.jsonl, triage-results.md and worker-handoff.md).

| Exercise | Observed actions and result |
| --- | --- |
| Ticketed feature | Draft-only phase made reads only. Reused matching existing slice issues, then exercised fresh creation of #100/#101 with real multiline bodies. Native blocked-by wiring used database ID 10100, not issue number 100. Neither new issue received readiness automatically; publication did not edit parent. |
| Missing revision/context | `git cat-file` rejected MISSING; unavailable issue-only body remained explicitly missing. No dependent implementation or invented scope. |
| Rejected/unmerged dependencies | Reproduced main's absent-file failure and success only on worker branch; ancestry check exited 1. Closed-rejected and unmerged prerequisites remained blockers. |
| Parent/child dispatch | Caller selected child slices; parent remained coordination-only. Blocked child was not eligible merely because labelled ready. |
| Routine tracker progress | Stub assignment/labels/comments changed; spec hash and local docs diff remained unchanged. |
| Substantive discussion change | Updated only canonical spec, committed/pushed to local bare fixture origin, then refreshed issue pointer to that accessible fixture SHA. No code change or second scope owner. |
| Local whole spec / no delegation | One isolated branch delivered both inline slices test-first; prerequisite inspected at committed state. Five tests passed, including actual subprocess/filesystem fresh/add/clear/restore lifecycle. |
| Worker role | Supplied scope/revision/constraints used directly, observed meaningful regression failure then three passing tests; branch/commit and caller-owned merge reported without recursive controller. |

Parent inspected reports/state and reran five whole-spec tests and three worker
tests successfully. Fixture whole-spec result is `0cbb9f1`; worker result is
`d50baa2`. Test reruns created only Python bytecode caches in temporary fixtures.
The recording stub and local bare remote prove local emitted calls/state and
fixture availability, not GitHub authentication, hosted revision access or live
server support. Parent/sub-issue operations and write-then-error recovery were
not executed. No real GitHub mutation occurred.

## Discovery and architecture investigation

Stage-4 candidate: fifteen skills after `311ce59`, with stage-4 files dirty;
exact consumed hashes are in the evaluator's skill-source-hashes.json. Fixture
result branch `eval/discovery-architecture`, commit `88d43b1`, under
`/private/tmp/mascah-discovery-eval.TEMZnF/fixture`; report beside it.

Research read primary synthetic requirements/trace. Disposable cache replay ran
1,000 requests: control success 100%, p95 192 ms; TTL reduced origin calls to 170
but returned 460 stale online values. Recorded evidence-backed abandonment and
reconsideration condition; created no spec/tickets/production integration.
The supplied retry protocol question ended answer-only, without a new document.
Architecture investigation reproduced HTML/text formatting drift, compared
retaining current design/shared standard-library formatting/external dependency,
honored the dependency ADR, and recommended shaping only. Production-like code
and ADR stayed unchanged. Parent reran both probes successfully and confirmed
the unchanged production diff. These observations describe synthetic fixtures,
not actual service/cache performance.

Audit caveat: the stage-4 evaluator incidentally read installed using-superpowers
at startup, whose subagent-stop said ignore it. No upstream workflow guided its
scenario execution, but this was not a strict upstream-access-free run. A separate
clean-copy exercise is recorded below; do not present the first run as perfectly
isolated.

Strict clean-copy retry consumed only `/private/tmp/mascah-clean-room-mymdfyd8/`
suite/input, with no installed/upstream access or prior reports. Validator and
Hermes entry ran from `/private/tmp`, discovering fifteen skills/zero errors.
Fresh discovery/research/prototype execution replayed the raw trace: origin met
requirements (100%, p95 192 ms); a different cache-first probe returned 950 stale
values, while online-origin/offline-fallback matched origin and added no observed
benefit. It concluded abandonment and answered the retry question without a
forced project document or assignment. Cache timings were model assumptions,
not measured performance. Report and disposable probe:
`/private/tmp/mascah-discovery-worker/`; parent inspected and reran its assertions
successfully. The earlier clean-copy dispatch hit a runtime usage limit before
execution; this successful retry supplies the actual clean-copy evidence.

## Integrated review and structural checks

Independent whole-branch review inspected base `045a78f` through the candidate,
including untracked stage-3/4 files. It found no Critical/Important defect in
guidance or current distribution. Three minor validator gaps were reproduced
with failing fixtures and fixed: release updater type/$.version, explicit
Use/Invoke skill references, and malformed JSON object diagnostics. All fifteen
tests then passed on Python 3.13.12 and Python 3.12.13. Validator reported fifteen
skills/zero errors; Hermes registration stub discovered the exact fifteen;
Claude skill component validation and diff checks passed. Claude manifest check
has the already documented root-CLAUDE warning, not a missing shipped skill.

Review did not claim live harness installation/delegation, release-service
execution, damaged setup marker/concurrent-edit behavior, legal licensing review,
or performance in an actual user project. Notices and release configuration
were inspected; those runtime/professional boundaries remain explicit limits.

## Remaining integration limits

| Spec acceptance | Delivered evidence |
| --- | --- |
| A1 identity/removal | Three manifests and both marketplaces agree; obsolete runtime/distribution paths absent. |
| A2 portable ownership | Local specs, extracted-plan and tracker scope-change fixtures preserve one requirements owner. |
| A3 proportional workflow | Direct bug, ticket-free local spec, answer-only research and abandoned discovery executed. |
| A4 delegation | Direct and caller-owned worker fixtures ran without required orchestration. Live CLI delegation remains unexercised. |
| A5 coordination | Recording tracker exercised scope/revisions, native dependency IDs, rejected/unmerged blockers, progress and parent exclusion. |
| A6 complete suite | Fifteen entry points and support links validated; every listed skill applied in representative fixture scenarios. |
| A7 verification/distribution | Copied-tree positive/negative checks, two Python versions, manifest/component checks, behavioral exercises and independent review. Personal installations and live services are outside the verified boundary. |

No user-selected hobby project was supplied. Personal Claude/Codex/Hermes
installation, Hermes-to-CLI delegation, scheduler/webhook, live GitHub mutation
and actual Release Please service execution were not exercised. Repository
implementation does not edit those surfaces, merge main, publish or tag a release.
Representative fresh-context fixture checks establish observed behavior only;
they cannot guarantee every future agent interpretation.

## Standalone portability correction

Follow-up branch: fix/portable-skills, baseline 8e4111b, 2026-10-05.
The original whole-plugin checks were insufficient for individual installation:
copying each skill alone exposed 50 missing links across all fifteen skills.
This supersedes any earlier implication that whole-plugin portability also
established individual skill portability.

The correction maintains canonical guidance in root references/ and commits
only the support each skill needs under its local generated references/.
Sibling filesystem links are removed; named helpers are optional with fallback
instructions. Workflow guidance is shortened and no longer pulls in unrelated
support transitively. A development-only bundler tracks direct/transitive needs,
updates changed copies and removes unused copies. No installer build step.

Candidate checks: full validator fifteen skills/zero errors; 21 tests passed,
including every folder copied alone, escaping links/entry-point symlinks,
generated drift, reference-style transitive links, obsolete copy removal and
idempotent generation. Review exposed reference-style omission and generated
symlink write-through; failing fixtures reproduced both, then fixes passed the
suite. Python 3.12 and 3.13 runs, Hermes inventory, Claude component validation
and diff checks passed. Final commit contains the tested candidate.

Actual `npx skills` version 1.5.18, telemetry disabled, project-only installation
with temporary npm cache: all fifteen selected skills installed in copy mode to
`/private/tmp/mascah-npx-portability/copy/.agents/skills/`; implement-spec alone
installed to a second disposable Claude Code project. Despite testing a request
without --copy, the noninteractive installer reported copy mode; no symlink-mode
success is claimed. Every actual installed folder passed isolated validation.
These runs used the local candidate source, not GitHub's not-yet-published branch.
No global skill install or personal plugin configuration was changed.

Fresh-context behavior evaluator read only the named installed implement or
implement-spec entry and its local support, plus its own fixture. It could not
read source suite, root files, helper skills, upstream plugins or personal config.
Issue-only normalization regression failed ('A' != 'a') then all three tests
passed. Whole local empty-state spec regressions failed then three tests passed,
including populated/empty/populated transitions and preserved ordering/escaping.
Actual diffs reviewed and diff checks passed; no helper/outside-file attempt,
tracker calls or manufactured spec/plan ceremony. Parent inspected the report and
reran both three-test suites. Raw report/logs and uncommitted fixture branches:
`/private/tmp/mascah-standalone-0os2r5hz/`. This establishes representative isolated
fallback behavior, not every skill interpretation or live external integration.

Four canonical support sources remain maintained once. Forty required copies
ship (about 140 KB total); unrelated support is not bundled and installers need
no generation step. The root reference architecture in the earlier refactor
spec is superseded by the linked portability follow-up. Existing live runtime
limits remain: no Hermes delegation, browser integration or GitHub publication
was exercised by this correction.

## Focused guidance and workflow SSOT

Follow-up branch refactor/focused-workflow, baseline 03aa6b3, 2026-10-05.
The preceding portability commit solved standalone packaging but only partially
reduced broad context. The current correction restores the complete canonical
workflow guide, linking every activity and shared rule owner; it does not ship
that full maintenance guide into every skill. Scope-specific procedures stay in
their SKILL.md, reusable obligations in focused root leaf references, and generated
copies remain checked distribution artifacts.

Rule transfer: mandate/preservation/truthfulness -> discipline; intended scope,
Delivery/extraction/history -> specification; tracker authority/revisions/readiness
and operational state -> assignments; caller/worker contract -> delegation;
prerequisites/resume/completion -> implementation; proportionate tests/interaction
checks/evidence -> verification; provider-specific operations -> github. The
catch-all artifacts/execution files are retired. Setup, domain modeling and
interface design each bundle only 181 words of common discipline. Tracker and
worker references load under explicit conditions, including local-only triage.

Bundled leaf payload is 51,720 bytes in 32 copies versus 140,187 bytes/40 copies
at 03aa6b3 (63.1% smaller). This is installed support size, not a measured token
saving or a claim that every conditionally bundled file is loaded. The full guide
is deliberately retained for understanding and maintenance at repository level.

Independent static review compared old obligations to new owners and identified
an incorrect fallback pointer and generic partial-write retry guidance that became
unreachable for implementation-only installs. Both were corrected: fallback
points to assignments, inspect-state-before-retry belongs to common discipline.
Its minor guide/inspection/conditional-triage findings were also addressed.
No blocking finding remains in that obligation audit; it is not runtime proof.

Final candidate distribution validator: fifteen skills, zero errors. All 21
structural/isolated-copy/drift tests passed on Python 3.12 and 3.13; Hermes inventory,
Claude skill component validation and diff checks passed. Actual npx skills 1.5.18
reinstalled all fifteen from the local candidate into a disposable Codex project
in copy mode; every installed folder passed isolated validation and none carried
the full workflow guide. Installer log: /private/tmp/mascah-focused-npx/install.log.

Fresh-context isolated evaluator used only copied named skills/local leaf support
and synthetic fixture inputs. Setup twice preserved nondefault docs/specs paths,
user workflow notes, one AGENTS block and byte-identical delegating CLAUDE, creating
no extra scaffold. Domain modeling resolved Customer/Login in glossary without
forcing ADR/spec/implementation. To-spec kept behavioral acceptance in the spec
and eight-stage rollout in one linked plan; seven links/anchors resolved. Triage
rejected missing revision access (git show exit 128) and closed-rejected prerequisite
as runnable implementation, making no tracker write/ready claim. Assigned worker
reproduced normalize(' A ') failure then passed three tests after lowercase fix,
with diff review and caller-owned integration/retries in its report.

Read manifest confirms setup/domain loaded only common discipline; to-spec added
Specification; tracker triage added Assignments but not GitHub operations; worker
implementation added Delegation and did not load tracker guidance. It needed no
full guide, source suite or installed helper. Raw artifacts/evidence:
/private/tmp/focused-behavior-fixture-hy1ebgfk/evaluation/. The first fixture test
used login-shell initialization and emitted a pyenv warning; subsequent commands
used login:false. No personal configuration was intentionally read/changed, but
that first shell's initialization cannot be called perfectly config-free.

The evaluator's local-triage follow-up had prior assignment guidance in context,
so a separate fresh-context trial verified the condition independently. It loaded
only triage and common discipline, executed whitespace normalization against its
documented behavior, and ended investigation without an assignment manual,
spec/ticket/workflow artifact or implementation. Report:
/private/tmp/triage-local-normalize-fke0jm25/report.md. Parent inspected reports
and reran worker checks and fresh local triage function checks successfully.

Evidence establishes synthetic standalone use and local-source installation,
not GitHub published-source installation, external tracker access, live Hermes
CLI delegation or every future interpretation. Shared rules moved rather than
vanished; the complete linked workflow guide remains the maintained entry point.
The focused-guidance commit contains this tested state.
