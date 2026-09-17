# Work map and planning handoff

The user authorized implementation of the workflow review on 2026-09-15, including understanding next work and combining items in one implementation. Humans choose outcomes and constraints; agents prepare and execute within them.

## Contract

- Keep capability scope, ordered release membership (`members`), and work prerequisites (`depends_on`) separate. Resolve references after archival and reject cycles or malformed references.
- Brief `focus` selects a work item or release; ordered members recommend the next eligible work inside it. Work `priority` (1 highest, default 3) and `Why now` express investment order and rationale. Show creation/updated dates, missing preparation, blockers and proposed Next lines.
- Work `batch` and `batch_reason` record an agent's recommendation to consider items together. `grove batch W-NNN ...` assesses any selection: dependency order, external blockers, scope overlap and preparation gaps. A shared implementation can be sequential. Neither a shared batch nor disjoint capability scope certifies safe parallel writes.
- `## Plan` or a repo-relative `plan` artifact supplies implementation preparation. Small work may use its concrete Next action; spikes require Question and Bounds. Missing preparation is visible and is repaired by `/work` under existing authority. Structural readiness does not prove semantic adequacy or grant permission.
- Context includes compact parent/member/dependency summaries, preserves parent constraints, treats blocking questions as required, and supports the planning phase. Release shaping uses capability summaries rather than entire capability bodies. Detailed implementation context retains required constraints and reports omissions.
- Closure requires checked acceptance (or spike disposition), evidence, closed prerequisites/members and no unresolved blocking questions. Choose the next eligible work using the same ordering as status.
- New metadata uses schema 2. Existing schema-1 repositories remain readable, with guidance when legacy prose relationships cannot establish readiness. `grove upgrade` changes only the schema declaration; authors migrate relationships based on evidence.
- Improve the skills and shared guidance: code-grounded planning, scoped research/review, persistent learning, no routine approval gates inside delegated authority, shared implementation and interruption recovery.
- Put the suite's own current knowledge and ordered follow-up work in Grove so the user can immediately inspect the new workflow.

## Implementation sequence

1. Add failing behavior tests for relations, selection, batch assessment, readiness, context, and closure. Preserve existing retrieval checks.
2. Add the shared work model and wire lint, status, batch, context and close to it. Add schema upgrade and CLI coverage.
3. Revise shape/work/close and supporting references/templates; update setup/curate and documentation for migration and selective learning. Validate using the account-import scenario from the baseline evaluation.
4. Initialize this repo's knowledge with delivered behavior and the next executor work; verify a migrated nullsec copy without editing the consuming repo.
5. Run the Python suite, CLI scenarios, skill validation, and independent review. Fix demonstrated defects and record limitations.

## Source adaptation

- [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin): explicit preparation and returning useful lessons to future work; choose research/review depth by uncertainty rather than importing its full workflow. Reports of token cost are not measured evidence for this suite.
- [Harness engineering](https://openai.com/index/harness-engineering/): compact navigation, durable plans and mechanical structural checks. Adopt these in the core now; evaluate runtime observability in executor work.
- [Symphony specification](https://github.com/openai/symphony/blob/main/SPEC.md): work dispatch and execution have distinct responsibilities, with workspaces, attempts and reconciliation. Keep those behind a later versioned executor contract; this increment does not install a service or claim Symphony compatibility.

## Verification record

Baseline skill scenario: the evaluator could infer sequential shared implementation and human release acceptance, but current skills supplied neither a batch protocol nor a planning-readiness contract; they prohibited attached plans. The final evaluation will exercise the revised guidance against the same scenario.
