# mascah-skills workflow

This is the canonical entry point for the suite's current workflow. It explains
how the activities fit together and links to the owners of their reusable rules.
Skills own their activity-specific procedures; the references below own shared
obligations. Generated per-skill copies are distribution artifacts, not separately
editable policies. The historical refactor specifications record why the system
changed; this guide and its linked owners describe the maintained workflow.

## Activities and routes

| Activity | Question | Possible result | Procedure owner |
| --- | --- | --- | --- |
| discovery | Is the idea worth pursuing; what must we learn? | Continue, defer, abandon or answer | [discovery](../skills/discovery/SKILL.md) |
| shaping | What outcome, constraints and alternatives matter? | Settled intent/acceptance or reason to stop | [shaping](../skills/shaping/SKILL.md) |
| to-spec | What agreed meaning should survive the conversation? | Local canonical spec | [to-spec](../skills/to-spec/SKILL.md) |
| to-tickets | What needs independent assignment? | Optional slice pointers/tickets | [to-tickets](../skills/to-tickets/SKILL.md) |
| triage | What does this request need next? | Investigation, executable unit, human input or rejection | [triage](../skills/triage/SKILL.md) |
| implement | How do we deliver the chosen unit? | Verified change or precise blocker | [implement](../skills/implement/SKILL.md) |
| implement-spec | How do we deliver the whole outcome? | Integrated acceptance across slices | [implement-spec](../skills/implement-spec/SKILL.md) |

Activities are independent entry points, not mandatory consecutive gates. A clear
issue-only bug goes directly to implementation. A bounded feature can be shaped,
saved locally and implemented without tickets. A larger effort may use named
Delivery slices and optional assignments. Discovery can end with contrary evidence
and abandonment, creating no build assignment; a short factual question can stay
in conversation. Optional research/prototype/design helpers support these routes.
Supporting procedure owners are [research](../skills/research/SKILL.md) for primary
evidence, [prototype](../skills/prototype/SKILL.md) for disposable experiments,
[TDD](../skills/tdd/SKILL.md) for meaningful test-first cycles,
[code review](../skills/code-review/SKILL.md) for actual diff/requirement review, and
[architecture investigation](../skills/improve-codebase-architecture/SKILL.md) for
observed friction and candidate trade-offs.

Setup records inferred or chosen project preferences; skills remain usable without
it. Existing project conventions take precedence over suite default locations.

## Rule owners

| Concern | Single maintained owner | Load when |
| --- | --- | --- |
| Mandate, writing safety and truthful claims | [Common discipline](discipline.md) | Any skill |
| Intended scope versus execution detail | [Specification and Delivery](specification.md) | Saving scope or introducing slices |
| Selected scope, prerequisites, resume and completion | [Implementation](implementation.md) | Delivering a unit or whole spec |
| Meaningful checks and evidence | [Verification](verification.md) | Changing/reviewing behavior |
| Caller/worker role and returned evidence | [Delegation](delegation.md) | Delegating or receiving worker work |
| Issue authority, revisions, readiness and coordination | [Assignments](assignments.md) | Consuming/preparing tracker assignments |
| Concrete GitHub commands and partial-failure handling | [GitHub operations](github.md) | Reading/writing through GitHub tools |

Domain definitions and consequential ADR practices are owned by
[domain-modeling](../skills/domain-modeling/SKILL.md), interface/cohesion choices by
[codebase-design](../skills/codebase-design/SKILL.md), and project preference/pointer
preservation by [setup](../skills/setup-mascah-skills/SKILL.md). These procedural
owners contain their own instructions; they do not copy a whole artifact manual.
Discovery/research/prototype own their findings, evidence and disposition formats.

## Durable ownership and coordination

Substantial intent/decisions live in git; the spec/Delivery contract above defines
those owners. A glossary defines language, an ADR records consequential trade-offs,
and persistent discovery records useful unresolved questions/findings/disposition.
Create documents lazily and move settled meaning into its owner with a pointer.
Small standalone issues may own scope as described in Assignments. Tracker progress
is operational coordination; it is not a second specification or mirrored git state.

The caller's mandate controls movement between activities. Implementation with
adequate scope allows routine planning; drafting/research is not publication or
production implementation authority. Read Common discipline for the actual bounds.
Likewise, readiness is actionable scope/access/integrated prerequisites rather than
permission or proof of delivered behavior; its checklist lives once in Assignments.
The runtime owns dispatch, model routing and supervision under Delegation, while
Implementation and Verification define the result and evidence obligations.

## Authoring and distribution

Edit each rule in its owner, not in generated copies. Skills link only to relevant
focused references; conditional references are loaded for the stated situation.
Run python3 scripts/bundle_references.py after editing shared sources and commit
its output with the source. The full guide is kept for understanding/maintenance;
it is not bundled into every installed skill. Each standalone skill carries its
needed local support and fallback guidance for optional helpers. Validation checks
both isolated folders and generated drift; behavior exercises check actual use.
