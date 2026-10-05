# GitHub operations

Read project repository and mapped labels. Use existing harness GitHub tools or gh;
credentials and runtime access stay outside tracked files. Local-only work needs
no tracker. Missing access requires supplied scope or a concrete missing input.

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
and report that limit. Parent/sub-issue relationships are also external mutations; edit only selected
units within authority. Do not modify unrelated parent issues.

Sources: [issue view](https://cli.github.com/manual/gh_issue_view),
[create](https://cli.github.com/manual/gh_issue_create),
[edit](https://cli.github.com/manual/gh_issue_edit),
[comment](https://cli.github.com/manual/gh_issue_comment), and
[issue dependencies REST API](https://docs.github.com/en/rest/issues/issue-dependencies).
