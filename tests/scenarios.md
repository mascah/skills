# Skill acceptance exercises

Use a fresh agent context with the named shipped skill, its references and a
small temporary project. Give it the request and raw fixture, not the expected
answer. Inspect the resulting files, commands, tracker recordings and report.
Keep writes inside fixtures; never post to a real tracker for these exercises.
Static validation cannot substitute for these executions.

| Scenario / skill | Fixture and request | Required observation |
| --- | --- | --- |
| Small issue-only bug / `implement`, `tdd`, `code-review` | Supplied issue: normalize trims/lowercases; tiny Python function only strips. Implement. | Regression fails then passes through public function; no forced spec, tickets, plan or setup. |
| Local feature spec / `implement-spec`, `codebase-design` | Local empty-state spec with inline Delivery, small module, no tracker access. Implement entire spec. | Uses local scope/Delivery and checks whole acceptance without credentials/tickets. |
| Large Delivery extraction / `to-spec` | Settled spec plus lengthy multi-team migration sequence; save independently maintained rollout. | Requirements stay in spec; sequence moves into one linked plan, no duplicate. |
| Abandoned idea / `discovery`, `research`, `prototype` | Explore offline cache; local measurements contradict benefit. Preserve useful conclusion. | Evidence, disposition, reconsideration; no assignment or production promotion. |
| Already discussed idea / `shaping`, `domain-modeling` | Settled empty-state behavior/constraints and a glossary; one optional visual choice remains. | Uses known intent, investigates available facts and asks only consequential questions. |
| Ticketed feature / `to-tickets`, `triage` | Spec with two dependent Delivery slices, parent issue and recording tracker; authorize fixture publication. | Short canonical pointers at usable revision, correct edges, children executable independently when eligible, parent excluded from dispatch. |
| Missing revision/context / `implement` | Assignment points at nonexistent revision; separate issue-only request cannot be fetched. | Names missing input, performs no dependent execution, never claims scope read. |
| Rejected or unmerged dependency / `triage`, `implement-spec` | Closed blocker marked rejected; alternative has implementation only on unmerged branch. | Neither closure nor unmerged code alone satisfies an integrated prerequisite. |
| Tracker progress / `triage` | Existing spec and issues; authorize assignment/label/comment fixture updates. | Records operations without local spec/plan changes for routine progress. |
| Scope change in discussion / `triage`, `to-spec` | Comment changes substantive behavior; authorize local scope update and fixture pointer refresh. | Canonical owner updated; issue remains summary/pointer, no competing requirements. |
| Delegated worker / `implement` | Worker role with supplied scope/revision/constraints, caller owns dispatch/merge. | Obeys role, meaningful checks and branch/evidence report, no recursive controller. |
| No delegation tools / `implement-spec` | Local feature scope; delegation unavailable. | Direct implementation completes and accurately reports capabilities. |
| New effort folder / `to-spec`, `discovery` | Fresh project without workflow preferences; save a settled spec, then persist discovery notes for the same effort. | Spec lands in `docs/work/<yymmdd>-<effort>/` dated that day; discovery joins that folder instead of creating a second one. |
| Setup rerun / `setup-mascah-skills` | Existing workflow, nondefault docs paths, unrelated AGENTS/CLAUDE content; run twice. | Preserves paths/instructions, updates managed material once, no duplicate pointers or empty files. |
| Clean plugin installation / all | Copy each skill alone and install selected skills through the actual installer outside repository/upstream installs. | All 15 isolated folders resolve local support; optional helper fallbacks work; generated-copy drift is rejected; plugin discovery surfaces agree. |

Also exercise `improve-codebase-architecture` against a changing module with
observed caller friction and an existing ADR. It should compare costs/benefits,
use project vocabulary and propose selected shaping work without implementing
a refactor merely because a review ran.

Record date, suite revision, runtime, scenario inputs, observed actions/artifacts,
external calls and failure conditions in [results.md](results.md). Report live
Hermes-to-CLI, scheduler, live GitHub and user-project trials separately; fixture
checks do not establish them. No general evaluation platform is required.
