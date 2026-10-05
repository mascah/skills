# GitHub coordination

Read the project's workflow for repository, tracker convention and label mapping.
Use the harness's existing GitHub tools or `gh`; no new provider adapter is
needed. A local-only project can work entirely from its Markdown. Credentials
and tool access stay outside tracked documents. Missing access means use supplied
content or return a concrete missing input, not fabricated scope.

## Scope pointers

Substantial work has one local requirements owner. A useful issue body is:

```markdown
Implement the compatibility reader for the export migration.

Scope: docs/work/export-v2/spec.md; Delivery slice: compatibility-reader.
Repository: OWNER/REPO; revision: FULL_IMMUTABLE_SHA.
Acceptance: spec.md#existing-exports-remain-readable at that revision.
Delivery/dependencies: spec.md#delivery (or its linked plan).
Coordination: related issue/PR links, when they exist.
```

Include a permalink to the file at the usable revision when available. Resolve
paths and anchors against that revision before publication/readiness. An issue's
summary helps browsing but does not duplicate full acceptance. Small standalone
issues may instead own their scope and acceptance; without access their complete
content must be supplied. Promote growing design work into a spec and change
issue authority to a pointer. Do not treat inaccessible issue-only content as
recoverable from git.

## Readiness contract

`ready-for-agent` means an actionable implementation assignment:

- Scope/acceptance are unambiguous, accessible and within the caller's authority.
- Required inputs exist at the identified usable revision. Unpushed local docs
  do not qualify for a remote assignment.
- Hard prerequisites are delivered in available integrated work, checked through
  code, accepted evidence and merge state. A closed rejected issue or an unmerged
  worker branch alone does not satisfy them.
- Assignment is not already executing under the caller's coordination policy.
- Parent and child units do not overlap in the dispatch queue. A parent spec
  issue is coordination-only when children are the selected implementation units;
  it can execute when it is the sole chosen whole-spec unit.
- Research, missing human decisions and unavailable inputs are not silently
  queued as implementation work.

`triage` prepares and checks this contract; `implement` rechecks before starting.
Spec/ticket creation alone never applies readiness. Familiar optional roles are
`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`;
adopt existing equivalents. Do not force local requests through a state machine.
When a readiness check fails, identify the missing input/integration/owner and
which independent work remains possible. Avoid dispatching both a parent and its
children even if both happen to carry the ready label.

Structural dependencies live in Delivery or its one linked plan. Native GitHub
edges are a view of that structure; refresh them when structure changes, not on
every progress update. Tracker assignment, labels, comments and PR links need
no local document edit. Substantive scope or decision changes update the local
owner; point the issue back to it at a usable revision. Implementation complete,
integrated on a branch and merged into the target are distinct states.

## Concrete operations

Checked against primary docs and local `gh` help on 2026-10-05. Check installed
help/server support before relying on newer flags. Use explicit repository and
issue identities. Reads are allowed within the task; every external mutation
must be covered by the user's request or caller policy. Draft complete bodies
locally first when publication authority is absent. Never post just to test.

Read body, discussion and current coordination:

```sh
gh issue view ISSUE --repo OWNER/REPO --json number,title,body,state,labels,assignees,comments,url
gh api --paginate repos/OWNER/REPO/issues/ISSUE/dependencies/blocked_by
```

Create a selected issue from a real multiline file; omit ready labels until
readiness is separately checked:

```sh
gh issue create --repo OWNER/REPO --title 'Compatibility reader' --body-file /tmp/issue-body.md
```

Authorized progress/body updates (use the project's mapped label strings):

```sh
gh issue edit ISSUE --repo OWNER/REPO --add-assignee '@me'
gh issue edit ISSUE --repo OWNER/REPO --add-label ready-for-agent --remove-label needs-triage
gh issue edit ISSUE --repo OWNER/REPO --body-file /tmp/issue-body.md
gh issue comment ISSUE --repo OWNER/REPO --body-file /tmp/progress.md
```

For native dependencies use installed `--add-blocked-by`/`--remove-blocked-by`
flags only if help shows them. Older CLIs can use the documented REST endpoint:

```sh
gh api repos/OWNER/REPO/issues/BLOCKER --jq .id
gh api --method POST repos/OWNER/REPO/issues/DEPENDENT/dependencies/blocked_by -F issue_id=BLOCKER_DATABASE_ID
gh api --method DELETE repos/OWNER/REPO/issues/DEPENDENT/dependencies/blocked_by/BLOCKER_DATABASE_ID
```

The payload is the blocker's numeric database `id`, not its issue number. Create
issues first to obtain identities, then wire edges in dependency order. If the
server lacks native edges, use short coordination pointers to canonical Delivery
and report that limit. Inspect state after partial failures before retrying:
an error can follow a successful write, so do not blindly create duplicates.
Parent/sub-issue relationships are also external mutations; edit only selected
units within authority. Do not modify unrelated parent issues.

Sources: [issue view](https://cli.github.com/manual/gh_issue_view),
[create](https://cli.github.com/manual/gh_issue_create),
[edit](https://cli.github.com/manual/gh_issue_edit),
[comment](https://cli.github.com/manual/gh_issue_comment), and
[issue dependencies REST API](https://docs.github.com/en/rest/issues/issue-dependencies).
