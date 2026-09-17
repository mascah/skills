---
name: setup
description: Use when a repo has no grove.toml, or when adopting grove in a repo that has prior project docs to distill. Sets up docs/grove and writes the brief with the user.
---

# grove:setup

Prerequisite: `grove --version` works. If not, tell the user to run `uv tool install --editable <path-to-skills-repo>/cli`.

Read `../../references/knowledge-format.md` once before writing any page.

## Steps

1. Run `grove init` from the repo root. Report the actions it prints.
2. Read `README.md` and any existing docs index. Do not read every doc; list them.
3. Draft the brief from existing direction and user input: Pitch, Who it's for, Why, Constraints, Not now. Ask only for missing consequential information. Keep each under 80 words. Set `focus` when an outcome is selected; release membership belongs in work units.
4. If prior knowledge exists (a prior planning vault, an ADR folder, a wiki), distill it:
   - Write one capability page per cohesive thing the checkout does today, using `../../templates/capability.md`. Fill `## Code` with real paths. Acceptance lines that hold are `[x]`; accepted but unbuilt are `[ ]` and name a work unit.
   - Migrate decisions that still apply with `applies_to` filled. Superseded ones go to `history/decisions/` with `superseded_by`. Rejected ones worth remembering stay live with a Reconsider-when section.
   - Do not migrate resolved questions or session logs. Open questions get `blocks` filled.
   - Terms only when linked from two or more pages.
   - Delivered releases become one `history/work/` entry each. In-flight work becomes work units sized per `../../references/sizing.md`.
   - Keep capability scope, ordered release members, and execution prerequisites separate. Record priority/Why now and candidate batches from evidence. Preserve known dates; mark missing creation dates unknown. Evidence starts empty; migration provenance belongs in Outcome or sources.
   - Reuse valid specifications and plans. Attach detailed plans with the repo-relative `plan` field and assess remaining preparation. Before removing an obsolete document, search for code or tools that read/write its path; preserve required artifacts.
   - Record where the prior records live in `docs/grove/history/README.md`.
5. Run `grove lint`. Fix every error. Explain each remaining warning to the user or fix it.
6. Run `grove status` and confirm with the user that it names the right next action.
7. Commit.

## Rules
- Write only what applies now. Every page you create must help a future decision or action.
- Ask before deleting user-owned docs. Grove owns only `docs/grove/` and its managed block.
