# External workflow patterns adopted in Grove

Reviewed 2026-09-15. These are design adaptations, not installed integrations or measured performance comparisons.

| Source | Useful practice | Incorporated now | Follow-up |
|---|---|---|---|
| [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin) and its [planning skill](https://github.com/EveryInc/compound-engineering-plugin/blob/main/skills/ce-plan/SKILL.md) | Distinguish intended outcomes from implementation preparation; make lessons usable by the next cycle | Shape establishes intent/design; work prepares a durable plan; close reconciles reusable meaning into its owner | Evaluate targeted research/review against actual failures and cost |
| [OpenAI harness engineering](https://openai.com/index/harness-engineering/) | Repository knowledge as the record, short navigational entry points, durable plans, mechanically enforced invariants | Repo-local work map, attached/shared plans, required-context omission errors, relationship checks and closure gates | Test runtime observability and isolated workspaces in the executor trial |
| [OpenAI Symphony](https://github.com/openai/symphony) and its [specification](https://github.com/openai/symphony/blob/main/SPEC.md) | Separate work selection from attempt orchestration; explicit workspaces, retries and reconciliation | Keep CLI readiness separate from runtime authority; capture executor work as W-002 through W-004 | Compare a Symphony-backed adapter with other available harness routes using a versioned Grove contract |

Compound Engineering's current entry point routes planning through several supporting phases. Grove uses progressive retrieval with one focused planning reference and proportional investigation/review. A fixed reviewer roster, exhaustive research, or a prescribed planning percentage is not part of Grove's contract. The user-reported token-cost concern remains a hypothesis until measured on comparable tasks.

The harness-engineering article describes an operating environment as well as a documentation practice. Grove adopts navigation and enforceable structural rules now; browser access, observability and runtime isolation need project-specific evidence. A checked plan or successful agent exit cannot substitute for that evidence.

Symphony is an execution candidate, not a replacement for shaping or project meaning. An adapter should consume prepared Grove work and return attributable evidence, leaving one process responsible for scheduling each attempt. This change installs no Symphony service and makes no claim that Hermes, OpenClaw or Symphony recovery has been exercised.

## Cost evaluation

Measure the same task before/after: correct first action, constraints missed, user interventions, input/cache/output tokens when available, elapsed time, repeated research/review and useful final result. Character-count estimates from CLI payloads can measure retrieval size but cannot establish whole-run token savings.

Prefer deterministic bookkeeping over model reconstruction. Load the work map first, then selected work; retrieve attached details when their phase needs them. Preserve required omissions visibly instead of hiding constraints to meet a target. Run reviews where risk warrants them and retain reusable lessons in their existing owner. A recurring check belongs in tests/lint when it can be enforced mechanically.

## Next implementation

`grove status` in this repo names the current next work. W-002 (execution contract) and W-003 (run ownership/recovery) are recorded as a candidate shared implementation, with W-002 first. W-004 is the later harness trial. Run `grove batch W-002 W-003` to see the current prerequisites and preparation gaps rather than treating this prose as live scheduling state.

The user additionally identified the existing Bench loop (a prior private executor) as a potential executor. Assess adapting that runtime during W-002/W-003 planning, before implementing new recovery machinery. Its source already contains planning/work/review/integration/verification orchestration, durable child outcomes, interruption reconciliation, and tmux/plain-subprocess modes. Its launch, role, ledger and closure conventions need an explicit compatibility assessment. W-004 should compare the chosen adaptation using the same recovery scenarios as other candidates. This is a source-based candidate assessment; the runtime was not executed during this update.
