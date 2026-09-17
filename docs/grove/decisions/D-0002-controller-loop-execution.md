---
type: decision
id: D-0002
status: accepted
updated: 2026-09-17
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

## Alternatives rejected
- Stage skills pinned by frontmatter (`context: fork`, `model`): Claude Code specific, invisible in the transcript, and the user prefers explicit dispatch.
- Separate `/plan` and `/implement` sessions with a human plan review: reintroduces the spec-then-plan babysitting the user found cumbersome in superpowers.
- Detecting the session model and warning: no API for it; would only nag.

## Consequences
The lead's context holds the plan, briefs and short reports only. Debugging beyond one hypothesis is re-dispatched, not performed by the lead. Task results become the unit a headless executor consumes (W-004). The user is not yet convinced this is better; the trial in W-006 records evidence either way.

## Reconsider when
A trial shows the loop costs more turns or quality than a single cheaper session, a harness lets the caller change models between stages, or the headless executor needs the stages hoisted out of the skill.
