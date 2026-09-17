import json

import pytest

from grove import cli, close, context, lint, status
from grove.pages import GroveError


def work(root, wid, *, kind="feature", size="bounded", extra="", body="", done=False):
    folder = "history/work" if done else "work"
    p = root.knowledge / folder / f"{wid}-example.md"
    p.write_text(f"---\ntype: work\nid: {wid}\nstatus: {'done' if done else 'proposed'}\n"
                 f"updated: 2026-09-15\ncreated: 2026-09-01\nkind: {kind}\nsize: {size}\n"
                 f"scope: [autopilot]\n{extra}---\n## Outcome\nOutcome for {wid}.\n"
                 "## Constraints\nKeep persisted data.\n## Acceptance\n- [ ] Result holds.\n" + body)
    return p


def focus(root, wid):
    p = root.knowledge / "brief.md"
    p.write_text(p.read_text().replace("type: brief", f"type: brief\nfocus: {wid}"))


def test_focus_release_orders_eligible_members_and_shows_dates(root):
    work(root, "W-100", kind="release", size="large", extra="members: [W-102, W-101]\n")
    work(root, "W-101", body="## Next\nInspect storage.\n")
    work(root, "W-102", extra="depends_on: [W-000]\n", body="## Next\nPrepare parser plan.\n")
    focus(root, "W-100")
    # Finish the old active task so selection is controlled by focus.
    p = root.get("W-001").path
    p.write_text(p.read_text().replace("status: active", "status: abandoned"))
    d = status.status(root)
    assert d["recommendation"]["id"] == "W-102"
    assert d["recommendation"]["readiness"] == "needs-plan"
    assert d["recommendation"]["created"] == "2026-09-01"
    out = status.render_status(d)
    assert "W-100" in out and "0/2" in out
    assert "Prepare parser plan." in out and "2026-09-01" in out
    assert "focus" in d["recommendation"]["selection_reason"].lower()


def test_blocking_question_is_required_context_and_readiness(root):
    d = status.status(root)
    w = next(w for w in d["proposed"] if w["id"] == "W-002")
    assert w["readiness"] == "blocked"
    assert any("target-locks" in x for x in w["blockers"])
    d = context.context(root, "W-002", budget=1)
    assert any("target-locks" in x for x in d["errors"])


def test_context_keeps_parent_constraints_and_archived_dependency_summary(root):
    work(root, "W-100", kind="release", size="large", extra="members: [W-101]\n")
    work(root, "W-101", extra="depends_on: [W-000]\n", body="## Plan\n1. Inspect code and test the change.\n")
    d = context.context(root, "W-101", phase="plan")
    text = "\n".join(d["pages"].values())
    assert "W-100" in text and "Keep persisted data." in text
    assert "W-000" in text and "closed" in text
    assert not any(i["basename"] == "W-000-v3-release" for i in d["included"])


def test_release_shape_context_is_compact_and_has_member_status(root):
    work(root, "W-100", kind="release", size="large", extra="members: [W-101, W-000]\n")
    work(root, "W-101")
    cap = root.get("autopilot").path
    cap.write_text(cap.read_text() + "\n## Details\n" + "Long implementation detail. " * 2000)
    d = context.context(root, "W-100", phase="shape")
    assert not d["errors"]
    text = "\n".join(d["pages"].values())
    assert "W-101" in text and "W-000" in text
    assert "Long implementation detail" not in text


def test_batch_explains_sequence_overlap_and_missing_plans(root, monkeypatch, capsys):
    work(root, "W-101", extra="batch: import\nbatch_reason: Shared import model and integration checks.\n")
    work(root, "W-102", extra="depends_on: [W-101]\nbatch: import\nbatch_reason: Shared import model and integration checks.\n")
    monkeypatch.chdir(root.repo)
    code = cli.main(["batch", "W-102", "W-101", "--json"])
    d = json.loads(capsys.readouterr().out)
    assert code == 0
    assert d["order"] == ["W-101", "W-102"]
    assert d["assessment"] == "needs-planning"
    assert d["shared_scope"] == ["autopilot"]
    assert d["blockers"] == []
    assert "review" in d["parallel"].lower()


def test_batch_external_dependencies_and_human_questions_block(root, monkeypatch, capsys):
    work(root, "W-101", extra="depends_on: [W-002]\n")
    monkeypatch.chdir(root.repo)
    assert cli.main(["batch", "W-101", "--json"]) == 2
    d = json.loads(capsys.readouterr().out)
    assert d["assessment"] == "blocked"
    assert any("W-002" in b for b in d["blockers"])


@pytest.mark.parametrize("extra, message", [
    ("depends_on: [W-999]\n", "W-999"),
    ("depends_on: [W-101]\n", "cycle"),
    ("members: [W-000]\n", "release"),
    ("depends_on: W-000\n", "list"),
    ("depends_on: [1]\n", "work id"),
    ("priority: high\n", "priority"),
    ("batch: import\n", "batch_reason"),
    ("plan: ../outside.md\n", "plan"),
    ("created: 2026-02-31\n", "date"),
])
def test_malformed_work_metadata_lints_without_crashing(root, extra, message):
    work(root, "W-101", extra=extra)
    errors, _ = lint.lint(root)
    assert any(message in e for e in errors)
    assert status.status(root)["recommendation"] is None


def test_membership_dependency_cycle_rejected(root):
    work(root, "W-100", kind="release", size="large", extra="members: [W-101]\n")
    work(root, "W-101", extra="depends_on: [W-100]\n")
    assert any("cycle" in e for e in lint.lint(root)[0])


def test_close_release_refuses_unclosed_member_and_unchecked_acceptance(root):
    p = work(root, "W-100", kind="release", size="large", extra="members: [W-000, W-101]\nunchanged: [autopilot]\n", body="## Evidence\nChecks passed.\n")
    work(root, "W-101")
    p.write_text(p.read_text().replace("status: proposed", "status: done"))
    with pytest.raises(GroveError, match="W-101"):
        close.close(root, "W-100")
    child = root.get("W-101").path
    child.write_text(child.read_text().replace("status: proposed", "status: done"))
    child.rename(root.knowledge / "history/work" / child.name)
    with pytest.raises(GroveError, match="Acceptance"):
        close.close(root, "W-100")
    p.write_text(p.read_text().replace("- [ ]", "- [x]"))
    assert close.close(root, "W-100")["id"] == "W-100"


def test_external_plan_in_context_and_readiness(root):
    plan = root.repo / "docs/plans/import.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("# Import plan\n1. Change parser, then storage; verify integration.\n")
    work(root, "W-101", extra="plan: docs/plans/import.md\n")
    d = context.context(root, "W-101", phase="implement")
    assert any(i["rel"] == "docs/plans/import.md" for i in d["included"])
    assert d["readiness"]["readiness"] == "ready"


def test_legacy_dependencies_do_not_claim_readiness(root):
    w = next(w for w in status.status(root)["proposed"] if w["id"] == "W-003")
    assert w["readiness"] == "needs-shaping"
    assert any("depends_on" in reason for reason in w["preparation"])


def test_upgrade_preserves_config_and_is_idempotent(root, monkeypatch, capsys):
    p = root.repo / "grove.toml"
    p.write_text(p.read_text() + '\n# user config\n[custom]\nkeep = "yes"\n')
    monkeypatch.chdir(root.repo)
    assert cli.main(["upgrade"]) == 0
    assert 'schema = 2' in p.read_text() and 'keep = "yes"' in p.read_text()
    before = p.read_text()
    assert cli.main(["upgrade"]) == 0
    assert p.read_text() == before


def test_release_acceptance_question_does_not_block_member_implementation(root):
    work(root, "W-100", kind="release", size="large", extra="members: [W-101]\n")
    work(root, "W-101", body="## Plan\n1. Implement and verify import.\n")
    q = root.knowledge / "questions/usability.md"
    q.write_text("---\ntype: question\nid: usability\nstatus: open\nupdated: 2026-09-15\nblocks: [W-100]\n---\n## Question\nHuman judges release usability.\n")
    rows = {w["id"]: w for w in status.status(root)["proposed"]}
    assert rows["W-100"]["readiness"] == "blocked"
    assert rows["W-101"]["readiness"] == "ready"


def test_empty_acceptance_checklist_cannot_close(root):
    p = work(root, "W-101", extra="unchanged: [autopilot]\n", body="## Evidence\nChecks passed.\n")
    p.write_text(p.read_text().replace("status: proposed", "status: done").replace("- [ ] Result holds.", "A result."))
    with pytest.raises(GroveError, match="Acceptance"):
        close.close(root, "W-101")


def test_context_refuses_scalar_relationship(root):
    work(root, "W-101", extra="depends_on: W-002\n", body="## Plan\nImplement then verify.\n")
    d = context.context(root, "W-101")
    assert d["errors"] and d["readiness"]["readiness"] != "ready"


def test_context_refuses_malformed_question_blockers(root):
    p = root.get("target-locks").path
    p.write_text(p.read_text().replace("blocks: [W-002]", "blocks: W-002"))
    d = context.context(root, "W-002")
    assert any("blocks must be a list" in e for e in d["errors"])


def test_upgrade_preserves_schema_text_in_multiline_strings(root, monkeypatch, capsys):
    p = root.repo / "grove.toml"
    p.write_text('notes = """\nschema = 1\n"""\n' + p.read_text())
    monkeypatch.chdir(root.repo)
    assert cli.main(["upgrade"]) == 0
    import tomllib
    d = tomllib.loads(p.read_text())
    assert d["schema"] == 2
    assert d["notes"] == "schema = 1\n"


@pytest.mark.parametrize("kind, body, message", [
    ("feature", "## Dependencies\nW-002 must finish.\n", "depends_on"),
    ("release", "", "members"),
])
def test_close_refuses_unresolved_relationship_preparation(root, kind, body, message):
    p = work(root, "W-101", kind=kind, extra="unchanged: [autopilot]\n", body=body + "## Evidence\nChecks passed.\n")
    p.write_text(p.read_text().replace("status: proposed", "status: done").replace("- [ ]", "- [x]"))
    with pytest.raises(GroveError, match=message):
        close.close(root, "W-101")
