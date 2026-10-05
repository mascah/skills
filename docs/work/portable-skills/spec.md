# Standalone skill distribution

## Problem

The original plugin layout kept support at root references/ and linked sibling
skills by filesystem path. Individual installers copy a skill directory, leaving
those links broken. Complete-plugin checks did not expose this defect.

## Intended behavior and decisions

Every published skills/<name>/ folder is self-contained before installation.
Shared guidance remains authored once in root references/. A small development
helper derives required support from local links, follows transitive references,
and writes committed copies into each skill's generated-only references/ folder.
Only needed files ship; users never run a build step. Keep skill-specific support
inside its owning skill and optional helper invocations by name with enough
fallback guidance to proceed independently. No symlinks outside skill folders.

## Acceptance

- All local file links resolve inside each skill copied alone.
- Generated copies match canonical sources; stale/unused copies fail validation.
- The helper is idempotent, follows support links and removes obsolete copies.
- Selected skills install with npx skills in disposable project scope.
- Representative isolated skill execution needs neither root files nor helpers.
- Complete Claude/Codex/Hermes plugin inventory and prior contracts remain valid.

## Delivery

Use fix/portable-skills from 8e4111b. Capture the broken isolated baseline, add
negative fixtures, localize links/fallbacks, bundle support, validate individual
folders and full plugin, exercise actual installer and isolated behavior, then
record evidence and branch handoff. Runtime/personal configuration is outside
scope; use temporary projects and no global installation.

## Verification

See [the verification record](../../../tests/results.md#standalone-portability-correction).

## Focused guidance and workflow SSOT follow-up

The next checkpoint preserves references/workflow.md as the complete maintained
entry point: routes, artifact ownership, coordination, delegation, verification
and authoring, with links to each single rule/procedure owner. It is a navigation
and explanatory guide, not a second edited copy of all rules. Root focused
references own reusable obligations; skill bodies own activity-specific methods.
Generated leaf copies remain the standalone distribution form.

Retire catch-all artifacts/execution references after moving useful instructions
to focused owners or owning skills. Setup, domain modeling and interface design
must not load unrelated assignment/delegation/implementation manuals. Tracker and
worker contracts load conditionally. Keep acceptance/readiness authority, inline
Delivery/extraction, abandonment, preservation and truthful evidence intact.

Verify complete guide links and every standalone folder, compare bundled size
against 03aa6b3, inspect the old/new obligation mapping, and exercise representative
isolated authoring, tracker, worker and implementation scenarios. Record results
in tests/results.md. Work on refactor/focused-workflow; no external publication.

Focused-guidance verification: [results](../../../tests/results.md#focused-guidance-and-workflow-ssot).
