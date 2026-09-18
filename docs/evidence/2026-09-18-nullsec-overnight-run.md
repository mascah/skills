# Nullsec overnight controller run

Analysis recorded 2026-09-18. Source: Claude Code session `9e36d344-4f38-4105-aedd-7342ec990a00`, version 2.1.276, project nullsec. On the builder's machine the transcript is `~/.claude/projects/-Users-mascah-GitHub-mascah-nullsec/9e36d344-4f38-4105-aedd-7342ec990a00.jsonl`; child transcripts are in the matching session directory's `subagents/`. Counts below exclude the subsequent human playtest discussion unless stated. Local transcript references are provenance, not required inputs for future execution.

## Observations

- Requested outcome: finish W-019 members through Grove, defer named human judgments, record integrated checks, and hand off an unmerged worktree. Run began 2026-09-18 05:59:40 UTC and reached its final implementation handoff at 15:33:35 UTC (23:59 MDT September 17 to 09:33 MDT September 18; about 9h34m).
- 38 Agent dispatches: 21 sonnet and 17 opus. The final handoff reports W-021 through W-025 closed, W-026 mechanical evidence recorded, human judgments deferred, and test/measure/visual green at revision `161d2d7`. This analysis inspected the transcript, not a fresh rerun of those checks.
- Two lead `system/compact_boundary` records: line 1053 at 07:45:16 UTC, 366,741 to 17,005 tokens in 104,813 ms; line 2136 at 13:39:16 UTC, 367,656 to 15,786 tokens in 89,219 ms. Six further boundaries across five child transcripts: impl-U2 twice; impl-U3, impl-V1, impl-V2 and impl-X1 once each. Eight total recorded boundaries. The observed lead threshold was about 367k, not evidence for a much smaller threshold's effectiveness.
- 51 idle notifications in delivered user-message envelopes, with 51 distinct sender/timestamp pairs. Their result payloads total 128,691 characters. Also 18 explicit teammate messages, often repeating the same task report. Distinguish repeated report content from transport replay: no duplicate sender/timestamp event was found in those 51.
- All 33 ReadNotifications calls returned `No queued notifications.` This did not establish that a worker was still running or had not completed.
- The plan said no agent team, but named Agent dispatches became teammates. The brief repeatedly required the report both on disk and as the final message; some workers also sent it through SendMessage. The lead independently watched and read report files.
- Line 2574 delivers ten delayed idle notices just after the final handoff, including a notice dated 13:38:08 UTC. Line 2580 repeats the handoff in response, despite no new work result.
- W-025 branch fixing/verification occupied about 13:37–14:40 UTC. A fixer and its replacement ended turns while waiting for background commands, without the expected report. The lead used overlapping report watchers, inspected worker transcripts, and explicitly resumed the finisher at 14:37. The whole interval includes useful work and testing; it is not all measured wasted time.
- The umbrella W-019 remained proposed while members were activated. The lead acknowledged this omission during the morning follow-up (line 2651).
- Morning playtesting found stale canvas after closing 3D, confusing damaged-ship redispatch and misleading duration labels despite green checks. These illustrate missing integrated interaction coverage, not permission to implement nullsec fixes here.

## Accepted direction

The user agreed to shape the highest-priority opportunities: single result delivery, reliable worker completion, ordinary subagents, release checkpoints and integrated interaction review. The user explicitly chose instructions preferring subagents and avoiding teammates for now; do not disable or change the agent-teams flag. Revisit the choice with later evidence. This authorizes shaping; implementation remains proposed work.

## Interpretation and limits

Shaping correction, 2026-09-18: the user objected to calling the general mechanism "release checkpoints" because work-skill runs need not be releases. W-011 covers work-run checkpoints for standalone units, batches and releases; umbrella/member bookkeeping is conditional on a release being in scope. The observed nullsec release remains an example, not a universal requirement.

The controller carried useful work across compactions. The clearest observed coordination problems were multiple result-delivery paths, delayed idle messages and workers finishing a turn without collecting command results. These observations do not prove compaction caused state drift, that every idle event was unnecessary, or that a prose rule guarantees harness behavior. A small runtime trial must verify dispatch type and recovery before claiming the fixes work.

Official harness reference inspected during analysis: [Agent teams](https://code.claude.com/docs/en/agent-teams), especially named dispatch conversion and automatic delivery of final answers in idle notifications. Verify current tool behavior when implementing; do not copy a stale teammate-only resume API into an ordinary-subagent workflow.
