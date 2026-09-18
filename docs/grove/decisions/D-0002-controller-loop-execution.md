---
type: decision
id: D-0002
status: accepted
updated: 2026-09-18
applies_to: [work-planning, autonomous-execution]
sources:
  - https://code.claude.com/docs/en/sub-agents.md
  - https://code.claude.com/docs/en/model-config.md
  - superpowers 6.3.0 skills/subagent-driven-development/SKILL.md
---
## Context
`grove:work` prepared, implemented, debugged, reviewed and closed in one conversation with "single agent" as the default execution approach. A session started on the most capable model therefore paid that model's price for every test-fix loop; one run spent roughly 400k tokens debugging in the live conversation. The user wants the expensive model for planning, cheaper models for code and review, no extra human touch points, and a path to a headless harness later. No harness lets a skill change the caller's model; Claude Code lets a dispatch name its model explicitly.

## Decision
`grove:work` stays one command with no default human checkpoint between plan and execution. The calling session is a controller: it prepares the plan on whatever model it runs, then for bounded and large work dispatches a fresh implementer per task and a fresh reviewer per task, each with an explicit model, runs a bounded fix loop with model escalation, and closes. The lead never writes code or runs a test-fix loop; diffs and review packages stay in files. Small work stays single agent in-session. Model rules live as prose in the skill and are passed on every dispatch; no frontmatter, no configuration. Each task report uses the contract result shape so a later harness can replace the dispatch call without changing the records.

## Overnight controller follow-up
On 2026-09-18 the user selected ordinary subagents and instructions that avoid teammates for the controller loop, leaving the agent-teams flag unchanged. Use file-backed reports with compact, attempt-identified returns, consume each result once, and make workers collect command results or explicitly hand off owned waits. Keep a compact work-run checkpoint for standalone work, batches and releases; umbrella/member state applies only when a release is in scope. Require final review to cover connected interactions. These are accepted directions for W-010 through W-012, not claims about implemented behavior. Evidence: [nullsec overnight analysis](../../evidence/2026-09-18-nullsec-overnight-run.md). Verify the actual subagent dispatch/continuation path; naming a dispatch may turn it into a teammate when teams are enabled.

## Alternatives rejected
- Disabling agent teams globally for the overnight follow-up: the user deferred this on 2026-09-18 in favor of instructions preferring subagents and avoiding teammates. Revisit if a bounded trial cannot honor the instruction or later evidence favors teams.
- Stage skills pinned by frontmatter (`context: fork`, `model`): Claude Code specific, invisible in the transcript, and the user prefers explicit dispatch.
- Separate `/plan` and `/implement` sessions with a human plan review: reintroduces the spec-then-plan babysitting the user found cumbersome in superpowers.
- Detecting the session model and warning: no API for it; would only nag.

## Consequences
The lead's context holds the plan, briefs and short reports only. Debugging beyond one hypothesis is re-dispatched, not performed by the lead. Task results become the unit a headless executor consumes (W-004). W-006 recorded a prose-only controller trial. The later nullsec overnight run supports continuity across compaction, while exposing reporting and worker-lifecycle gaps selected for W-010 through W-012; it does not establish unattended reliability in every harness.

## Reconsider when
A trial shows the loop costs more turns or quality than a single cheaper session, a harness lets the caller change models between stages, or the headless executor needs the stages hoisted out of the skill.
