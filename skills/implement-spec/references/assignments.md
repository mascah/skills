# Tracker scope and readiness

## Scope pointers

Substantial work has one local requirements owner. A useful issue body is:

```markdown
Implement the compatibility reader for the export migration.

Scope: docs/work/export-v2/spec.md; Delivery slice: compatibility-reader.
Repository: OWNER/REPO; revision: FULL_IMMUTABLE_SHA.
Acceptance: spec.md#existing-exports-remain-readable at that revision.
Delivery/dependencies: spec.md#delivery (or its linked plan).
Coordination: related issue/PR links, when they exist.
```

Include a permalink to the file at the usable revision when available. Resolve
paths and anchors against that revision before publication/readiness. An issue's
summary helps browsing but does not duplicate full acceptance. Small standalone
issues may instead own their scope and acceptance; without access their complete
content must be supplied. Promote growing design work into a spec and change
issue authority to a pointer. Do not treat inaccessible issue-only content as
recoverable from git.

## Readiness contract

`ready-for-agent` means an actionable implementation assignment:

- Scope/acceptance are unambiguous, accessible and within the caller's authority.
- Required inputs exist at the identified usable revision. Unpushed local docs
  do not qualify for a remote assignment.
- Hard prerequisites are delivered in available integrated work, checked through
  code, accepted evidence and merge state. A closed rejected issue or an unmerged
  worker branch alone does not satisfy them.
- Assignment is not already executing under the caller's coordination policy.
- Parent and child units do not overlap in the dispatch queue. A parent spec
  issue is coordination-only when children are the selected implementation units;
  it can execute when it is the sole chosen whole-spec unit.
- Research, missing human decisions and unavailable inputs are not silently
  queued as implementation work.

`triage` prepares and checks this contract; `implement` rechecks before starting.
Spec/ticket creation alone never applies readiness. Familiar optional roles are
`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`;
adopt existing equivalents. Do not force local requests through a state machine.
When a readiness check fails, identify the missing input/integration/owner and
which independent work remains possible. Avoid dispatching both a parent and its
children even if both happen to carry the ready label.

Structural dependencies live in Delivery or its one linked plan. Native GitHub
edges are a view of that structure; refresh them when structure changes, not on
every progress update. Tracker assignment, labels, comments and PR links need
no local document edit. Substantive scope or decision changes update the local
owner; point the issue back to it at a usable revision. Implementation complete,
integrated on a branch and merged into the target are distinct states.
