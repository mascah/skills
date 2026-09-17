# Work map and planning evaluation

Evaluated 2026-09-15 on the implementation working tree. This is evidence for W-001; it does not claim a deployed runtime or full harness integration.

## Automated behavior

`cli/.venv/bin/python -m pytest cli/tests -q`: 100 passed. The baseline was 72 passing tests. New cases were observed failing before implementation, including selection, work relationships, batch ordering, required context, archive-safe references, preparation and closure. Existing tests were updated for schema 2, added status fields, and checked acceptance at closure.

Independent code review found three concrete defects, each reproduced and fixed with regression coverage:

- Scalar dependency metadata bypassed context validation. Context now refuses lint errors before emitting actionable context.
- A schema-like line inside a TOML multiline string could be changed by upgrade. Upgrade now verifies that a candidate edit changes only the parsed top-level schema value.
- Closure could bypass unmigrated prose dependencies or absent release membership. These preparation gaps now prevent archival.

A further migration regression verifies that `grove init` refreshes guidance for an existing configured knowledge root rather than creating a second default tree.

## Skill behavior

An independent agent evaluated the old and revised skills against a reliable CSV account-import outcome with no-data-loss constraints, W-101 parser, W-102 persistence, and W-100 release requiring human usability judgment.

Baseline: the evaluator inferred sensible sequencing from judgment, but the skills prohibited attached plans and lacked a batch/preparation protocol. Revised evaluation used an isolated temporary fixture and actual CLI calls:

- Missing member plans: batch reports needs-planning.
- One shared plan: batch reports prepared, with W-101 before W-102.
- W-101 is ready while W-102 waits for its prerequisite's closure.
- A question blocking release usability leaves member implementation eligible.
- Premature W-102 closure refuses; W-101 then W-102 can close in order.
- W-100 refuses closure while usability judgment is pending.
- Archived member context retains its shared plan reference.

All fixture evidence was labeled synthetic. This checks workflow behavior, not actual account-import correctness. The evaluation identified a wording ambiguity about joint verification before dependent implementation exists; planning and close now specify independent prerequisite acceptance first, with later joint verification in the shared plan and dependent/release evidence.

## Nullsec work-map exercise

Copied nullsec's existing knowledge and config into a temporary repo, with read-only code pointers into the source checkout. Upgraded the copied schema and recorded the already documented W-005 membership and W-004 prerequisites; selected W-005 as focus. The consuming repository was not modified.

- Lint: 0 errors, 0 warnings.
- W-005: six required members, with archived W-001 still resolved.
- Recommendation: W-011, needs-plan.
- Rendered status: approximately 1,696 tokens using characters divided by four.

| Shape context | Source estimate at 6,000 budget | Required omissions | Source estimate at 12,000 budget | Required omissions |
|---|---:|---:|---:|---:|
| W-005 release | 5,905 | 13 | 11,784 | 0 |
| W-004 encounter | 5,933 | 4 | 8,291 | 0 |
| W-011 motion | 5,979 | 4 | 8,302 | 0 |

W-005 still omits one optional item at the larger budget. Source-text estimates exclude output wrappers, source lists and omission messages; the rendered W-005 default-budget output was approximately 8,037 tokens by the same character estimate. These measurements do not establish whole-run savings. Broad context still needs explicit expansion; the compact work map now supplies selection without requiring that expansion first.

## Packaging and limits

All five skills passed the skill-creator frontmatter validator. The Codex plugin passed the plugin validator after completing its UI metadata. `python3 __init__.py` confirmed registration of the five skill paths. The CLI reports version 0.2.0. Validators used an already-cached PyYAML module; no runtime dependency was added.

No recurring automation, real executor recovery, multi-hour run, or installed-harness integration was exercised. Structural readiness and closure do not verify the semantic truth of plans or evidence. Existing projects need evidence-based migration of their relationships and plans after upgrading the schema declaration.
