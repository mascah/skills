---
name: setup-mascah-skills
description: Use when configuring or updating a project's paths, tracker labels, and execution preferences for mascah-skills.
---

# Adopt the project

Setup is optional. Discover existing conventions before choosing defaults. Read
[workflow](../../references/workflow.md), [artifact ownership](../../references/artifacts.md),
and [writing discipline](../../references/execution.md).

1. Inspect agent instructions, documentation locations, glossary/context maps,
   ADRs, git remotes and project check commands. Read any existing workflow file.
   A remote is evidence of a possible tracker, not a mandate to use it.
2. Record known paths and preferences in one compact workflow file, by default
   `docs/agents/workflow.md`. Include specs/discovery/optional plans, domain docs,
   tracker (GitHub repository, local-only, or existing other convention), label
   mapping if applicable, project checks, isolation/commit rules and caller
   executor policy. Record only operational preferences that are actually known;
   no credentials, model routing invented by the skill, or required empty files.
3. Ask only when a missing preference changes behavior and cannot be inferred.
   Without a selected tracker, retain local-only operation. Use familiar triage
   roles or existing equivalents when applicable: `needs-triage`, `needs-info`,
   `ready-for-agent`, `ready-for-human`, `wontfix`.
   For GitHub, record the explicit repository and the role-to-label mapping,
   following [the tracker contract](../../references/github.md). Setup records
   preferences; it does not create labels or change readiness remotely.
4. Make the workflow discoverable from instructions used by the project's
   harnesses. Preserve unrelated AGENTS/CLAUDE content. If CLAUDE already delegates
   to AGENTS, one pointer in AGENTS is enough; otherwise add a small pointer where
   each active harness reads it. When the harness is unknown, use an existing
   AGENTS file, or create one with the pointer if neither exists.
5. Manage only your own pointer block, using markers
   `<!-- mascah-skills:start -->` and `<!-- mascah-skills:end -->`. On rerun update
   that block once and merge workflow preferences with existing user content;
   adopt existing equivalent pointers instead of adding duplicates. Ambiguous or
   damaged markers require a targeted repair, not replacing the whole file.

Finish with the chosen paths, changes, checks and how to edit preferences later.
Setup creates no spec, glossary, ADR, ticket, or label merely to fill a scaffold.
Skills remain independently usable when context is inferable without setup.
