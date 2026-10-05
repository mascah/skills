# Refactor the personal suite into mascah-skills

## Intent and agreed direction

Make this repository an independently maintained personal skill suite that Mike can use in hobby projects. Grove has become a standalone application elsewhere; this repository should stop shipping its CLI, knowledge schema, templates, and operating workflow.

The user approved all four delivery stages on 2026-10-05 and intends to execute them today. Stage 2 is the first usable checkpoint, not the end of the requested scope. This document records the design and the execution sequence; it does not claim that the replacement suite has been implemented.

The suite takes inspiration from Matt Pocock's skills and selected Superpowers disciplines, adapted to the user's preferences. It must work without either upstream plugin installed.

Inspected baseline: this repository at `ec87bb2`; the local Matt Pocock checkout at `4588b32`; Superpowers skill package `6.4.2`. Recheck the checkout and upstream sources when implementing. Existing Grove behavior and metadata remain in place at this baseline.

The planning branch retires the Grove-specific AGENTS/CLAUDE instructions immediately. Do not create transitional Grove work records or require its CLI to execute this refactor. The remaining legacy files can be inspected directly and are removed in stage 2. The planning branch otherwise delivers this document, not the replacement skill suite.

## Constraints

- The plugin is named `mascah-skills` in every supported harness. The marketplace can remain `mascah`.
- Keep the existing Claude Code, Codex, and Hermes packaging surfaces, while removing the Grove application.
- Durable intent and consequential decisions live in git. GitHub can own everyday coordination. Small standalone tasks may live entirely in issues.
- Plain Markdown is sufficient. Do not introduce a replacement CLI, work-ID registry, knowledge schema, synchronization service, or required scaffold of empty files.
- Existing project conventions override default paths. Skills remain useful without setup when their required context can be inferred.
- Discovery and shaping may conclude that an idea should be abandoned, deferred, or answered without implementation.
- Delegation remains supported. Runtime-specific orchestration and model choices belong to the caller's operational policy.
- Ask for missing intent or a change in mandate; do not insert repeated approvals for routine technical decisions within already authorized work.
- Verification is proportional to the change. Behavioral changes deserve meaningful tests; documentation and mechanical configuration do not require contrived TDD cycles.
- All four stages are planned here. Hermes scheduler/configuration changes are outside this repository's implementation scope.

## Workflow and vocabulary

These are independently invocable activities, not mandatory consecutive gates.

| Activity | Question it answers | Possible result |
| --- | --- | --- |
| `discovery` | Is this worth pursuing, and what do we still need to learn? | Findings, a decision, defer/abandon, or a promising direction |
| `shaping` | What exactly would we change, for whom, and under which constraints? | Clear intent, resolved terminology, alternatives and acceptance, or a reason to stop |
| `to-spec` | What agreed intent should survive this conversation? | A local specification |
| `to-tickets` | Which parts need independent assignment or tracking? | Optional tickets pointing to defined deliverables |
| `implement` | How do we deliver this selected unit and prove it works? | Verified change, or a precise unresolved blocker |
| `implement-spec` | How do we deliver the entire specified outcome? | Integrated result across any necessary slices |
| `triage` | What is this request, and what does it need next? | Investigation, shaping, an executable assignment, human input, or rejection |

`discovery` replaces the role of Matt's `wayfinder`. `shaping` incorporates the useful interview behavior of `grilling` and `grill-with-docs`, with `domain-modeling` as a supporting discipline. Do not retain a second mandatory grilling layer or the old command names as automatic aliases.

Examples of valid routes:

- A clear bug report goes directly to `implement`.
- An uncertain idea goes through discovery and is abandoned after evidence contradicts its premise. A useful reason is recorded; no spec or tickets are generated.
- A bounded feature is shaped, written as a spec, and implemented directly.
- A larger change gets a spec with Delivery slices; selected slices become tracker issues.
- A question can be answered in the current conversation without creating a discovery document. Persistence is justified by future use, not by having invoked a skill.

No activity silently upgrades a request to discuss, research, or draft into authorization to implement or publish externally. Conversely, invoking implementation with an adequate scope authorizes routine planning and technical decisions inside that scope.

## Artifact ownership

Default paths in a consuming project:

```text
docs/agents/workflow.md
docs/work/<effort>/spec.md
docs/work/<effort>/discovery.md  # only for discovery that needs persistence
docs/work/<effort>/plan.md       # only when extracted from Delivery
docs/adr/
GLOSSARY.md
```

Create files lazily, adopt existing equivalent locations, and use relative links for portable references. No required YAML frontmatter, global numeric IDs, status fields, assignees, or copied comment threads in specs.

### Specification

A spec owns the intended change: Problem, Intended behavior, Constraints, Acceptance, Decisions, and Out of scope. Omit empty optional sections. Use concrete behavioral examples when they clarify requirements; do not manufacture exhaustive user stories.

Unresolved consequential questions are explicit. A draft can exist with open questions, but an affected implementation unit cannot be declared ready while its meaning is unresolved. Avoid reopening a decision merely because a new session started.

Technical choices that constrain the implementation belong in Decisions. Observations about the current files or implementation order belong in Delivery and must be revalidated against the checkout.

### Delivery and the optional plan

The user accepted **Delivery inside the spec by default, extracted only when useful**. Planning is an activity, not a mandatory additional artifact or user-invoked phase.

A Delivery section owns only execution information: named slices, real dependencies, affected areas, sequencing or migration steps, integration checks, and necessary handoff context. Each slice links to the acceptance it serves; it does not restate the full specification.

For example, a spec can require that existing login sessions remain valid. Delivery can say to deploy a reader that accepts both token formats before switching token issuance. The former defines correctness; the latter preserves correctness during the change.

- Tiny changes need no persistent Delivery section.
- A straightforward feature can use a short inline sequence.
- Extract to `plan.md` when execution detail needs independent reading or maintenance, such as a long migration or several teams sharing a rollout sequence. Replace the inline detail with a link; do not keep both copies.
- A plan never becomes a second specification. If scope changes, update its owning spec or slice.
- When a spec has tickets, the named slices and structural dependencies live once in Delivery or its extracted plan. Issues refer to them and show live progress.
- Do not prescribe every test/command/commit as a separate ticket. Do not commit merely to mirror an assignment, label, or progress checkbox.
- After delivery, retain useful specs and plans as history. Current behavior belongs in the code and maintained project documentation; consequential enduring rationale belongs in an ADR.

This refactor uses an inline Delivery section below to demonstrate that a four-stage effort does not automatically need a separate plan file.

### Discovery, domain language, and decisions

Persistent discovery notes hold the question or destination, constraints, known facts and sources, unresolved questions and dependencies, and a disposition. Record abandonment with its rationale and a reconsideration condition when that prevents repeated investigation. Short unsuccessful conversations need no compulsory artifact.

Move settled content into its durable owner and link to it instead of maintaining duplicate narratives. Glossaries define domain terms, not implementation details. Use ADRs for consequential trade-offs that a future maintainer would otherwise misunderstand; not every choice needs one.

## Tracker contract

GitHub is the initial external tracker. A repo can operate entirely from local Markdown with no tracker. Do not build a generic multi-provider adapter system in this refactor; an existing non-GitHub project convention can be described in its workflow file.

For substantial work, an issue contains a short summary, the local spec/slice pointer, the repository and usable revision, and any necessary coordination links. Full scope and acceptance remain recoverable from that revision without GitHub. An issue summary may aid browsing but is not a competing requirements document.

For a small standalone task, the issue itself can own scope and acceptance. Without tracker access, a caller must provide that issue content; the skill cannot claim to recover unavailable information from git. If the task grows into substantial design work, promote its scope into a spec and replace the issue's authority with a pointer.

The tracker owns assignment, labels, discussion, run/progress updates, and PR links. Only discussion that changes substantive scope or durable decisions requires a document update. Native dependency relationships, when supported, are a view of the structural dependencies in Delivery; update that view when those dependencies change, without mirroring every status transition into git.

`ready-for-agent` denotes an actionable implementation assignment, not merely a well-written document:

- Its scope and acceptance are unambiguous, accessible, and within the caller's authority.
- Its required inputs are available at an identified revision; unpushed local documents do not qualify.
- Its blockers are satisfied by available integrated work, not merely by a closed issue.
- It is not already being executed elsewhere under the caller's coordination policy.
- A parent spec tracking issue is not queued alongside its child implementation tickets. It can be executable when it is itself the sole chosen implementation unit.
- Research or human decision tickets are not silently passed to an implementation-only queue.

Writing a spec or creating tickets does not automatically apply the label. `triage` prepares and checks readiness; an implementation worker rechecks it before starting. If context or a prerequisite is unavailable, report the specific missing input and continue only independent authorized work.

Use the familiar `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix` labels where useful, adopting a project's existing equivalents. Do not require every local request to enter a formal tracker state machine. An issue may be closed because it was rejected; closure alone never proves a dependency was delivered.

## Delegation and runtime policy

Delegation is compatible with the suite. Remove the old hard-coded Grove controller loop, not the ability to delegate.

The reusable skills define the assignment and completion obligations: scope/reference and revision, constraints, acceptance, relevant project commands, and a final report with branch/commit, checks actually run, remaining findings, and a concrete waiting condition when blocked. A runtime can supply this as a prompt with context pointers; no new serialized execution-contract system is needed.

The caller owns CLI selection, model routing, concurrency, process supervision, retries, deduplication, and worktree lifecycle. Hermes may pick up a ready issue and delegate to Codex or Claude Code, which performs `implement` against the assignment. The caller verifies the returned evidence and integration state before recording completion.

The suite honors an existing executor policy. Without one, the current agent may implement directly and use focused delegation when the harness supports it and the task warrants it. Do not require an external CLI or fresh agent per step. Respect assignment ownership and prevent recursive controller/worker delegation through an explicit worker role when the caller uses one.

Hermes-specific operational instructions should live with Hermes. A standing preference in `SOUL.md` could point to that policy if appropriate for that installation; exact placement and commands should be checked there when configuring it. This refactor will not edit Hermes configuration, schedule jobs, or claim that CLI delegation has been exercised.

## Skill inventory and shared references

Keep the flat `skills/<name>/SKILL.md` structure, which the current Hermes registration already scans. Use supporting files inside a skill when specific to it and a small shared `references/` directory for cross-skill contracts. Plugin installations must ship those references; isolated-install checks must detect broken paths.

| Skill | Responsibility | Available by |
| --- | --- | --- |
| `setup-mascah-skills` | Discover and record project paths, tracker and execution preferences in one compact workflow file | Stage 2 |
| `shaping` | Refine intended outcomes, alternatives, constraints and acceptance; invoke domain modeling as needed | Stage 2 |
| `domain-modeling` | Sharpen and maintain terminology and consequential decisions | Stage 2 |
| `to-spec` | Synthesize settled intent into a local spec, with optional Delivery | Stage 2 |
| `implement` | Deliver a request, issue, spec, or named slice with proportionate verification | Stage 2 |
| `tdd` | Behavioral tests through meaningful interfaces, with a genuine failing test when using TDD | Stage 2 |
| `code-review` | Check requirements, defects, and project conventions against the actual diff | Stage 2 |
| `codebase-design` | Support interface design, testability, and cohesive modules using the project's vocabulary | Stage 2 |
| `to-tickets` | Turn independently assignable Delivery slices into tracker entries | Stage 3 |
| `triage` | Verify requests, investigate ambiguity, prepare runnable assignments, and manage tracker state | Stage 3 |
| `implement-spec` | Complete and integrate a whole spec, with or without tickets | Stage 3 |
| `discovery` | Maintain useful questions and findings across sessions, including defer/abandon outcomes | Stage 4 |
| `improve-codebase-architecture` | Investigate costly architectural friction and shape selected improvements | Stage 4 |
| `research` | Gather primary-source evidence and preserve findings where useful | Stage 4 |
| `prototype` | Answer a bounded design question with clearly disposable artifacts | Stage 4 |

Shared files: `references/workflow.md` for routes and mandate, `references/artifacts.md` for ownership and formats, and `references/execution.md` for verification and delegation obligations. Add `references/github.md` in stage 3 for concrete tracker operations. These are small instructions and examples, not the old scaffold templates or a new runtime.

Skills can be invoked independently. Supporting references are loaded when relevant; there is no global trigger that runs the whole suite for every task. Setup preserves existing AGENTS/CLAUDE instructions and provides a discoverable pointer for the harnesses actually in use. Re-running setup updates its own material without duplicating it or overwriting unrelated instructions.

## Acceptance

- **A1 — Identity and removal:** Supported plugin manifests identify `mascah-skills`; the current distribution contains no Grove CLI, `grove.toml`, old templates, executor adapters, or active instructions requiring Grove commands.
- **A2 — Portable artifacts:** An agent with the checkout can understand substantial scope and decisions without tracker access. Small issue-only work is an explicit exception. Requirements have one owner.
- **A3 — Proportional workflow:** Small work can be implemented without a spec, tickets, or a plan. A spec needs neither tickets nor an extracted plan. Discovery can stop without creating implementation work.
- **A4 — Delegation:** Both direct implementation and caller-managed CLI delegation fit the same skill obligations; runtime-specific model/process control is not imposed by the reusable skills.
- **A5 — Coordination:** GitHub readiness and issue pointers identify an executable unit and usable revision. Missing context, rejected dependencies, duplicate parent/child dispatch, and unresolved human decisions do not produce false completion.
- **A6 — Complete suite:** Every listed skill and its referenced support material ships and resolves without upstream plugins installed, with the new shaping/discovery names used consistently.
- **A7 — Verification and distribution:** Manifest consistency, skill discovery, internal links, and representative behavior scenarios are checked. Installation guidance and release automation match the final files. Retain appropriate upstream notices for adapted material.

## Delivery

Implementation evidence and runtime limits are recorded in
[the verification record](../../../tests/results.md). This specification remains
the intended contract; that record distinguishes exercised behavior from
unexercised integrations.

Execution: sequential integration checkpoints, with focused delegation permitted by the executing harness and task ownership. Reason: shared conventions and packaging precede dependent skills. Runtime: interactive implementation by default; an external caller can delegate under the contract above. Reassess parallelism after common references and entry-point names stabilize.

All four stages are part of this effort. Stage 2 must be installable and usable on its own; do not defer essential support dependencies until stage 4. The stages are deliverables, not mandatory GitHub issues. Use one implementation branch unless actual independent ownership justifies additional branches.

### Stage 1 — Establish the shared workflow

Depends on: this design. Covers A2, A3, A4 and the contract portion of A5.

1. Create `references/workflow.md`, `references/artifacts.md`, and `references/execution.md` from the decisions above. Keep one owner for each rule and link to it from consuming skills.
2. Include concise examples for a direct small task, an inline-Delivery spec, an extracted plan, a local-only project, and a discovery effort abandoned after learning something.
3. Define the minimum caller/worker handoff, authority boundaries, revision handling, and truthful completion report. Keep Hermes command flags and model policies out of these references.
4. Create `tests/scenarios.md` with the behavior scenarios listed under Verification below. These are acceptance exercises, not assertions about incidental wording.
5. Review the examples together: each requirement has one owner, no route implies every phase, and no document embeds a mirrored tracker status.

Checkpoint: the common rules can guide authoring every skill without requiring the old Grove schema. References for existing Grove skills remain until those consumers are removed in stage 2.

### Stage 2 — Ship the first usable mascah-skills core

Depends on stage 1. Covers A1 and the core of A2, A3, A4, A6, A7.

1. Author the eight stage-2 skills in the inventory, adapting upstream behavior to the common contracts. Fold interviewing into `shaping`; make `to-spec` synthesize rather than start another mandatory interview. Make `implement` accept local inputs and supplied issue content without requiring setup or tracker access.
2. Rename `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, and `plugin.yaml` consistently. Update descriptions and prompts; retain marketplace identity `mascah`. Verify current harness metadata formats before changing their structure.
3. Update `__init__.py`'s Hermes registration description and its expected inventory. Preserve its lightweight skill registration; deleting the Grove CLI does not mean deleting the Hermes plugin entry point.
4. Review the repository AGENTS/CLAUDE guidance already updated on the planning branch and align it with the implemented suite. Retain useful isolation, truthful verification, and Conventional Commits practices without imposing obsolete work IDs or closure commands.
5. Remove `cli/`, `templates/`, `grove.toml`, `scripts/adapters/`, old `setup`, `explore`, `shape`, `work`, `close`, and `curate` skills, and Grove-only references (`knowledge-format`, `planning`, `discipline`, `sizing`). Transfer only rules still needed into their new owners.
6. Review the old `docs/grove/`, `docs/plans/`, `docs/evidence/`, and external-workflow notes directly, extracting still-relevant rationale before removal. W-016's Grove launch trial is superseded by removal, not successfully completed; W-007's useful evaluation idea is covered by the new validation scenarios without pretending the old spike ran. Preserve this refactor spec. The planning branch has already retired Grove governance; use ordinary document/Git checks and the replacement suite checks without reopening the old CLI workflow.
7. Replace Grove pytest/lint jobs in `.github/workflows/ci.yml` and `lefthook.yml`. Add a small `scripts/validate.py` using the existing Python footprint to check skill names/frontmatter, referenced skills/files, plugin identity/version consistency, and Hermes discovery. Do not build another workflow CLI. Check a known-broken copied fixture as well as a valid tree so the validator demonstrates that it detects a meaningful defect.
8. Remove deleted CLI version targets from `release-please-config.json`; keep `.release-please-manifest.json`, `version.txt`, and the remaining plugin version fields consistent. Update README installation, update/reinstall instructions for the renamed plugin, and the usable core routes. Do not invent harness commands: verify them before documenting.
9. Record upstream provenance in `ATTRIBUTION.md` and preserve applicable copyright/license notices for adapted material. Keep upstream history in git rather than carrying an obsolete archive directory in the current distribution.
10. Run `python3 scripts/validate.py`, `python3 __init__.py`, and the core behavior scenarios. Validate from a clean copied/exported tree so root-relative or accidental upstream dependencies cannot hide. Inspect `git diff --check` and the final diff.

Checkpoint: a hobby project can install `mascah-skills`, optionally configure it, shape a feature, save a spec, and implement a direct task or spec with meaningful review. No Grove installation is necessary. This is the first usable release checkpoint; publishing or tagging still follows the repository's release process.

### Stage 3 — Add tracker coordination and whole-spec execution

Depends on stage 2. Covers A5 and remaining implementation paths in A6.

1. Add `references/github.md` and extend setup to record the repo's tracker and label mapping. Verify current GitHub operations against primary documentation before writing concrete commands. Keep credentials and runtime-specific tool access out of tracked files.
2. Author `to-tickets`: reuse or introduce named Delivery slices only when assignment warrants it; preserve structural dependencies in their canonical owner; draft useful issue summaries and pointers; publish only within the user's authorization. Do not automatically label every new issue ready or modify unrelated parent issues.
3. Author `triage`: reproduce bugs where feasible, check for existing implementations and prior durable decisions, resolve missing scope, and apply the configured readiness vocabulary. Preserve substantive decisions locally and operational discussion in the tracker.
4. Author `implement-spec`: support specs with and without tickets, honor dependencies and the caller's execution policy, integrate results, and verify whole-spec acceptance. Do not prescribe a worker/reviewer/merger fan-out for every spec.
5. Extend `implement` to resolve tracker pointers and validate scope/revision/prerequisites. If a supplied issue-only task cannot be fetched, report the missing content rather than inventing scope. External status changes follow the authorized caller policy, with implementation-complete and integrated/merged state distinguished.
6. Update discovery inventories, README examples, and relevant checks. Exercise issue-body fixtures and a recording/stubbed tracker interface without posting to real projects. A real GitHub smoke test needs an explicitly selected test repo and permission for its external writes; do not claim live integration from fixture checks.

Checkpoint: ready implementation assignments can be handed to a caller such as Hermes with a complete scope pointer and completion contract. Repo documents do not receive commits for routine label, assignment, or comment changes. A spec can still be implemented without creating tickets.

### Stage 4 — Complete discovery, architecture improvement, and cleanup

Depends on stages 1–3 for shared contracts and tracker behavior. Covers the remaining discovery and completeness cases in A3, A6, A7.

1. Author `research` and `prototype`: use primary evidence; capture useful findings; clearly distinguish experiments from production; do not automatically promote a prototype into implementation.
2. Author `discovery` from the useful wayfinder concepts. Keep destination, questions, evidence, decisions and disposition locally; use optional tickets only for separately assigned investigations. Allow continue, defer, abandon, and answer-only outcomes. Avoid mandatory one-question-per-session limits or a hard-coded research fan-out; honor the caller's delegation policy.
3. Author `improve-codebase-architecture`: begin with observed pain, changing areas, and existing decisions; explain benefits and costs; use visuals when they make choices clearer; route selected candidates into shaping. A review does not mandate a refactor.
4. Audit the full skill-reference graph. No shipped skill may invoke `grill-with-docs`, `wayfinder`, an absent helper, or an upstream plugin. Check that stage-4 additions did not reintroduce mandatory artifacts or a runtime-specific orchestration loop.
5. Finish removing superseded Grove material and dead paths in hooks, automation, ignore rules, and documentation. Preserve intentional historical/provenance mentions; do not rewrite old changelog history merely to make a string search empty.
6. Run structural checks and every behavior scenario. Try the installed suite in one user-selected hobby project if available; otherwise state the unexercised environment explicitly. Record results with the revision and real limitations.
7. Review the integrated diff for A1–A7, update installation and workflow documentation to the final inventory, and hand off the branch with checks and merge instructions. Do not mark integration complete merely because individual skill files exist.

Checkpoint: all requested activities and their supporting skills are usable together, with clear persistence and delegation boundaries and no dependency on the old Grove application.

## Verification scenarios

Use a fresh agent context or the executing harness's supported skill evaluation mechanism against small fixture projects. First establish the expected behaviors below; then record the observed actions, artifacts, external calls, and failure conditions. Static validation alone cannot prove that an agent follows a skill. Do not build a general evaluation platform as part of this refactor.

| Scenario | Required observation |
| --- | --- |
| Small issue-only bug | Implements from supplied scope; no forced spec, tickets, or plan; meaningful regression verification |
| Local feature spec | Implements without GitHub credentials or tickets; reads inline Delivery if present |
| Large Delivery extraction | Moves execution detail to one linked plan, leaving requirements in the spec and no duplicate sequence |
| Abandoned idea | Discovery records useful evidence and an appropriate disposition; creates no implementation assignment |
| Shaping an already discussed idea | Uses known facts, asks only consequential unresolved questions, and preserves the settled intent |
| Ticketed feature | Issues point to canonical slices; structural blockers match; the parent is not dispatched alongside children |
| Missing revision/context | Stops dependent execution with a specific missing input; never claims inaccessible scope was read |
| Rejected or unmerged dependency | Does not treat issue closure alone as successful delivery |
| Tracker progress | Assignment, label and routine comment changes require no local document updates |
| Scope change in discussion | Updates the canonical spec/slice; issue summary stays a pointer rather than acquiring competing requirements |
| Delegated worker | Receives scope/revision/constraints; follows caller role; reports evidence without recursively launching another controller |
| No delegation tools | Direct implementation remains usable and honest about unavailable capabilities |
| Setup rerun | Preserves unrelated agent instructions and existing paths; does not duplicate its managed content |
| Clean plugin installation | All skill/support references resolve with no Matt/Superpowers installation; each retained harness discovers the intended inventory |

Perform behavioral checks with available runtimes and report which ones were actually exercised. Live Hermes-to-CLI execution, a real scheduler/webhook, or a live GitHub mutation are not verified by prose review or stubbed calls.

## Outside this refactor

- The standalone Grove application and its repository.
- A new scheduler, webhook service, cross-machine locking service, or bidirectional issue/document synchronization system.
- Changes to the user's Hermes SOUL, runtime configuration, cron jobs, installed upstream skills, or unrelated projects.
- Automatic GitLab/Linear/Jira integrations beyond respecting an existing project convention.
- Porting Matt's entire suite, a general skill-evaluation platform, or mandatory agent teams.

## References

- Source material inspected: `/Users/mascah/GitHub/mattpocock/skills`, especially the named engineering skills and their direct dependencies, at `4588b32`.
- Superpowers brainstorming, planning, verification, worktree and testing disciplines, package `6.4.2`; use principles selectively rather than preserving every gate or orchestration rule.
- Existing repository references and Grove knowledge retrieved through its CLI at `ec87bb2`; retain lessons about isolation, meaningful acceptance and trustworthy handoffs without retaining their application-specific mechanism.
