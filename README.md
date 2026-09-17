# grove

Repo-local knowledge, work planning, and implementation guidance for coding agents. Six skills develop intent, prepare plans, execute within delegated constraints, and reconcile what changed. A small CLI makes the work map and structural checks deterministic.

## What's next?

From a configured project:

```sh
grove status
grove batch W-002 W-003
grove context --work W-002 --phase plan
```

Status shows focus, release membership, dates, blockers, preparation, the recommended next action and its reason, and items to consider together. Batch assesses any selected units for a shared implementation: internal order, external blockers, overlapping capability scope, and missing plans. Dependent items may execute sequentially in one implementation. The agent checks actual code ownership before parallel execution.

This repo uses its own work map. The next executor work and suggested grouping live in `docs/grove/`, accessible through those commands. [External workflow patterns](docs/2026-09-15-external-workflow-patterns.md) explains what we adapted from Compound Engineering, harness engineering, and Symphony.

## Install

CLI first, for every harness:

```sh
uv tool install --editable ./cli
```

Claude Code:

```sh
claude plugin marketplace add mascah/skills
cd /path/to/your/project && claude plugin install grove@mascah --scope project
```

Codex:

```sh
codex plugin marketplace add mascah/skills
codex plugin add grove@mascah
```

Hermes Agent (the repo root is the plugin):

```sh
ln -s /path/to/this/repo ~/.hermes/plugins/grove && hermes plugins enable grove
```

After updating, refresh the installed plugin through the harness and start a new session so it loads the revised skills. An editable CLI install reads the updated code directly.

## Loop

1. `grove:setup` adopts the project.
2. `grove:explore` thinks through an open idea with the human and writes only what they settle.
3. `grove:shape` investigates, selects work, and records its specification and relationships.
4. `grove:work W-NNN` prepares missing plans and implements. Several selected units can share one durable plan.
5. `grove:close` verifies evidence, reconciles knowledge, and closes units in dependency order.
6. A fresh session starts with `grove status`.

Humans choose outcomes and constraints; agents research, plan, and execute within them. Readiness reports structural preparation, not permission or proof of a correct plan. Release acceptance can require actual human judgment after member implementation.

Plans open with an execution decision: approach, reason, delegation, runtime and when to reassess. `/work` defaults to one agent, uses focused subagents for independent deliverables, and recommends a team when inspected ownership and coordination benefits justify it. Durable unattended execution is a separate choice. See the [execution defaults and header](references/planning.md#execution-decision).

## CLI

```text
grove init
grove upgrade
grove lint
grove status [--json]
grove batch W-NNN [W-NNN ...] [--json]
grove context --work W-NNN [--phase shape|plan|implement|debug|debrief] [--budget 6000] [--json]
grove find <query> [--history] [--type <type>]
grove close W-NNN
```

`batch` returns 2 for blockers, `context` returns 2 for required omissions or invalid relationships, and command/configuration errors return 1. JSON supports headless callers. There is no scheduler or execution driver in this release.

## Existing projects

The CLI reads schema 1 and 2. With the updated CLI/skills installed, run `grove upgrade` and shape/curate the work map: separate `members` from `depends_on`, set the brief's `focus`, preserve known dates, and assess plans. Upgrade changes only the schema declaration. Re-run `grove init` to refresh managed agent guidance.

The [knowledge format](references/knowledge-format.md) defines fields; [planning](references/planning.md) covers shared plans, execution and interruption.

## Develop

```sh
cd cli && uv venv && uv pip install -e '.[dev]' && uv run pytest -q
```
