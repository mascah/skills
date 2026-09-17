# Knowledge format (schema 2)

Knowledge lives under the configured root (default `docs/grove/`) in its code repository. Discover it through `grove status`, `grove context`, and `grove find`; fetch named sources when necessary. Write with the templates and check with `grove lint`.

## Content and ownership

| Path | Type | Holds | Status |
|---|---|---|---|
| `brief.md` | brief | Purpose, audience, constraints, not now; selected focus | active, parked, retired |
| `capabilities/<slug>.md` | capability | Behavior implemented today, acceptance, design notes, code pointers | draft, settled |
| `decisions/D-NNNN-<slug>.md` | decision | Choice, rationale, alternatives, reconsideration condition | proposed, accepted, rejected, superseded |
| `work/W-NNN-<slug>.md` | work | Intended change or question, design, plan, acceptance, progress | proposed, active, done, abandoned |
| `questions/<slug>.md` | question | Unresolved question, affected work, resolution path | open, parked |
| `terms/<slug>.md` | term | Meaning reused across pages | draft, settled |
| `history/work/` | work | Closed work and evidence | done, abandoned |
| `history/decisions/` | decision | Superseded direction | superseded |
| `history/evidence/` | any files | Verification, playtests, sourced research | |

Ordinary retrieval excludes history. Typed relationships resolve archived work identities and compact completion summaries without loading historical bodies. Attached plans/designs live outside this page tree, for example `docs/plans/`; they remain owned by their work and available after closure.

## Frontmatter

Every page requires `type, id, status, updated` (ISO date). Identity survives file movement. Brief id is `brief`; capability/question/term id equals its basename; decision/work ids are `D-NNNN`/`W-NNN`.

- Brief: optional `focus: W-NNN` selects an outcome or release.
- Decision: `applies_to` capability slugs; optional bare-ID `supersedes` and `superseded_by`.
- Work: `kind` (feature, fix, refactor, spike, tooling, migration, investigation, release), `size` (small, spike, bounded, large), capability `scope`, `started` when active; optional `unchanged` capabilities at close.
- Question: `blocks` work IDs. A parked question still blocks named work; parking is not an answer. Name a release for a release acceptance gate; name its members only if it also prevents those tasks.
- Optional `sources`: URLs or evidence references.

Work planning fields:

| Field | Meaning |
|---|---|
| `created` | Original creation date; leave unknown for migrated work without evidence |
| `priority` | Integer 1 highest through 5; default 3. `## Why now` explains the choice |
| `members` | Ordered required work IDs; only releases use this field |
| `depends_on` | Work IDs that must be closed before this unit executes/closes; use `[]` to declare none |
| `batch` + `batch_reason` | Slug and reason to consider units in one implementation |
| `plan` | Repo-relative path to an implementation plan; alternatively use inline `## Plan` |

Membership, dependency and scope are distinct. Members may depend on one another; membership alone does not require sequential implementation. Cycles across members/dependencies are invalid. A done work file becomes a satisfied prerequisite only after `grove close` archives it; abandoned work is not satisfied.

## Selection and preparation

Status recommends unblocked active work first, then the selected focus and its ordered members, then priority and ID as a stable tie-break. It states the reason. Agents maintain selection from evidence; the CLI does not infer importance from age or prose. A completed focus can be replaced as part of debrief.

Structural preparation is reported as `needs-shaping`, `needs-plan`, `ready`, or `blocked`. Missing content/relationships require shaping; missing implementation steps require planning. Ready means required content exists. The agent must still validate code, plan adequacy, authority and freshness. Final states include `needs-close`, `closed`, and `abandoned`.

`grove batch <ids>` assesses the selected implementation units, including internal order, external blockers, shared scope and missing preparation. Batch labels are recommendations. The command cannot prove parallel code ownership, compatibility of technical designs, or permission to execute.

## Body and links

Use `##` sections, no H1. Work Outcome/Constraints/Acceptance/Design provide its specification; Plan provides implementation steps. Long design references can be linked from Design. Read `planning.md` for preparation, shared plans and resume behavior.

Wikilinks use unique basenames, optionally with display text: `[[fly-ship|flight]]`. Live pages may link to history from work Evidence, or reference historical work declared in members/depends_on. Legacy work links under Dependencies remain readable during migration. Keep historical narrative out of ordinary context.

## Lifecycle

Capabilities describe what the checkout implements; decisions describe direction; work describes the change between them. Do not treat accepted direction as implemented behavior.

Update an existing owner when its meaning changes. Create a decision only for consequential rationale; create a term only when reused. Fold resolved questions into their durable answer and delete the question. Rejected approaches worth remembering stay discoverable with reconsideration conditions.

Before close, reconcile scoped capabilities or explain unchanged scope, prove and check acceptance (a spike records Disposition), record evidence, and satisfy named blockers/prerequisites. Releases additionally require closed members and release acceptance. `grove close` checks structure; the agent checks truth and records actual human judgment when required. A small change may produce zero new knowledge pages. Keep routine logs outside current knowledge.

## Migration

The CLI reads schema 1 and 2. Run `grove upgrade` before authoring schema-2 metadata so older CLIs refuse the newer repository. This updates only the schema declaration, preserving configuration and knowledge. Then use shape/curate to translate relationships from evidence, select focus, and assess preparation. Prose Dependencies without an explicit depends_on field surface as needs-shaping. Do not guess creation dates or mark legacy plans ready without reviewing them. Re-run `grove init` to refresh managed agent guidance when needed.
