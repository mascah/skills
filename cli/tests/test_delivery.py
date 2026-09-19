import json
import os
import subprocess

import pytest
from grove import cli, close, delivery
from grove.pages import load_root
from conftest import edit

W1 = "docs/grove/work/W-001-engage-range-readout.md"
W2 = "docs/grove/work/W-002-selection-brackets.md"


def ready_w001(root):
    """Make W-001 pass every closure invariant, without touching git."""
    edit(root, W1, "status: active", "status: done")
    edit(root, W1, "- [ ]", "- [x]")
    edit(root, W1, "## Evidence\n", "## Evidence\nHUD shows range; 3 scenario tests pass.\n")
    edit(root, "docs/grove/capabilities/autopilot.md", "updated: 2026-09-09", "updated: 2026-09-13")
    edit(root, "docs/grove/capabilities/autopilot.md", "- [ ] Engage range is shown and changeable.", "- [x] Engage range is shown and changeable.")


def gitenv(repo):
    return {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@x", "PATH": os.environ["PATH"], "HOME": str(repo)}


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True, env=gitenv(repo)).stdout.strip()


def init_main(root):
    """Commit the fixture as-is on a branch explicitly named 'main', regardless of the host's default."""
    git(root.repo, "init", "-q", "-b", "main")
    git(root.repo, "add", "-A")
    git(root.repo, "commit", "-q", "-m", "fixture")
    return git(root.repo, "rev-parse", "HEAD")


def commit_all(root, msg):
    git(root.repo, "add", "-A")
    git(root.repo, "commit", "-q", "-m", msg)
    return git(root.repo, "rev-parse", "HEAD")


def start_branch(root, name):
    git(root.repo, "checkout", "-q", "-b", name)


def checkout(root, name):
    git(root.repo, "checkout", "-q", name)


def archive_manually(root, rel):
    """Move a live work page straight into history, bypassing close()'s own validation."""
    src = root.repo / rel
    dest = root.repo / "docs/grove/history/work" / src.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dest)


# --- the happy path ----------------------------------------------------------------------------

def test_pass_on_properly_closed_delivery(root):
    init_main(root)
    start_branch(root, "feature")
    ready_w001(root)
    close.close(root, "W-001")
    sha = commit_all(root, "close W-001")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d == {"checked": sha, "base": git(root.repo, "rev-parse", "main"), "delivers": ["W-001"], "retains": [], "errors": []}


def test_pass_when_history_page_has_a_plan_outside_docs_grove(root):
    """A closed unit's page can carry `plan: docs/plans/x.md` (grove:work's shared-plan
    convention); the candidate tree the verifier extracts must include that file too, not just
    docs/grove, or plan_path() raises 'plan file missing' against the extracted tmp tree."""
    init_main(root)
    start_branch(root, "feature")
    plan = root.repo / "docs/plans/w001.md"
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text("# plan\n")
    edit(root, W1, "started: 2026-09-12", "started: 2026-09-12\nplan: docs/plans/w001.md")
    ready_w001(root)
    close.close(root, "W-001")
    commit_all(root, "close W-001")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == []


def test_pass_when_main_gained_another_branch_declaration_after_the_fork(root):
    """Three-dot freshness: a sibling delivery merged to main after this branch forked must not
    make this branch's own declaration look ambiguous."""
    init_main(root)
    start_branch(root, "feature")
    checkout(root, "main")
    other = root.repo / "docs/grove/deliveries/other.json"
    other.parent.mkdir(parents=True, exist_ok=True)
    other.write_text(json.dumps({"schema": 1, "delivers": [], "retains": []}))
    commit_all(root, "main gains another branch's declaration")
    checkout(root, "feature")
    ready_w001(root)
    close.close(root, "W-001")
    sha = commit_all(root, "close W-001")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == [] and d["delivers"] == ["W-001"] and d["checked"] == sha


# --- rejections, one hypothesis per closure state -----------------------------------------------

def test_reject_still_proposed(root):
    init_main(root)
    start_branch(root, "feature")
    close.record_delivery(root, "W-002")  # W-002 stays proposed, untouched
    commit_all(root, "declare")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == ["W-002: proposed work is not archived"]


def test_reject_active(root):
    init_main(root)
    start_branch(root, "feature")
    close.record_delivery(root, "W-001")  # W-001 stays active, untouched
    commit_all(root, "declare")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == ["W-001: active work is not archived"]


def test_reject_done_but_unarchived(root):
    init_main(root)
    start_branch(root, "feature")
    ready_w001(root)  # status done, but never moved to history/
    close.record_delivery(root, "W-001")
    commit_all(root, "declare")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == ["W-001: done work is not archived"]


def test_reject_abandoned(root):
    init_main(root)
    start_branch(root, "feature")
    edit(root, W1, "status: active", "status: abandoned")
    close.record_delivery(root, "W-001")
    commit_all(root, "declare")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == ["W-001: abandoned work is not archived"]


def test_reject_missing_id(root):
    init_main(root)
    start_branch(root, "feature")
    close.record_delivery(root, "W-999")
    commit_all(root, "declare")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == ["W-999: no such work id"]


def test_reject_invalid_closure_missing_evidence(root):
    init_main(root)
    start_branch(root, "feature")
    edit(root, W1, "status: active", "status: done")
    edit(root, W1, "- [ ]", "- [x]")
    archive_manually(root, W1)  # bypasses close(); lands in history with no Evidence
    close.record_delivery(root, "W-001")
    commit_all(root, "declare")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == ["W-001: W-001 Evidence section is empty"]


def test_reject_invalid_closure_unchecked_acceptance(root):
    init_main(root)
    start_branch(root, "feature")
    edit(root, W1, "status: active", "status: done")
    edit(root, W1, "## Evidence\n", "## Evidence\nok\n")
    archive_manually(root, W1)  # one acceptance box left unchecked
    close.record_delivery(root, "W-001")
    commit_all(root, "declare")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == ["W-001: W-001 Acceptance must be present and checked"]


# --- committed vs. worktree state --------------------------------------------------------------

def test_uncommitted_closure_does_not_pass(root):
    init_main(root)
    start_branch(root, "feature")
    ready_w001(root)
    close.close(root, "W-001")  # archives and declares in the worktree only
    with pytest.raises(delivery.Inapplicable, match="no delivery declaration"):
        delivery.verify_delivery(root, "feature", "main")


def test_advancing_branch_rechecks_new_sha(root):
    init_main(root)
    start_branch(root, "feature")
    ready_w001(root)
    close.close(root, "W-001")
    sha1 = commit_all(root, "close W-001")
    d1 = delivery.verify_delivery(root, "feature", "main")
    assert d1["checked"] == sha1 and d1["errors"] == []
    edit(root, "docs/grove/capabilities/autopilot.md", "## Code\n", "## Code\n<!-- note -->\n")
    sha2 = commit_all(root, "unrelated follow-up")
    assert sha2 != sha1
    d2 = delivery.verify_delivery(root, "feature", "main")
    assert d2["checked"] == sha2 and d2["errors"] == []


def test_inherited_declaration_present_at_base_exits_2(root):
    decl = root.repo / "docs/grove/deliveries/old.json"
    decl.parent.mkdir(parents=True, exist_ok=True)
    decl.write_text(json.dumps({"schema": 1, "delivers": ["W-000"], "retains": []}))
    init_main(root)  # the declaration ships as part of main itself, as if inherited
    start_branch(root, "feature")  # candidate == base; nothing new committed on this branch
    with pytest.raises(delivery.Inapplicable, match="no delivery declaration"):
        delivery.verify_delivery(root, "feature", "main")


def test_unresolvable_base_exits_2(root):
    init_main(root)
    start_branch(root, "feature")
    close.record_delivery(root, "W-001")
    commit_all(root, "declare")
    with pytest.raises(delivery.Inapplicable, match="does not resolve"):
        delivery.verify_delivery(root, "feature", "no-such-branch")


def test_malformed_declaration_exits_2(root):
    init_main(root)
    start_branch(root, "feature")
    decl = root.repo / "docs/grove/deliveries/feature.json"
    decl.parent.mkdir(parents=True, exist_ok=True)
    decl.write_text("{not json")
    commit_all(root, "declare")
    with pytest.raises(delivery.Inapplicable, match="malformed"):
        delivery.verify_delivery(root, "feature", "main")


def test_ambiguous_declaration_exits_2(root):
    init_main(root)
    start_branch(root, "feature")
    for name in ("a", "b"):
        p = root.repo / f"docs/grove/deliveries/{name}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"schema": 1, "delivers": [], "retains": []}))
    commit_all(root, "declare twice")
    with pytest.raises(delivery.Inapplicable, match="ambiguous"):
        delivery.verify_delivery(root, "feature", "main")


# --- multi-unit and partial delivery -------------------------------------------------------------

def test_multi_unit_delivery_with_one_unfinished_fails(root):
    init_main(root)
    start_branch(root, "feature")
    ready_w001(root)
    close.close(root, "W-001")          # declares + closes W-001
    close.record_delivery(root, "W-002")  # W-002 stays proposed
    commit_all(root, "close W-001, declare W-002 too")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == ["W-002: proposed work is not archived"]


def test_explicit_retains_partial_delivery_passes(root):
    init_main(root)
    start_branch(root, "feature")
    ready_w001(root)
    close.close(root, "W-001")
    decl_path = root.repo / "docs/grove/deliveries/feature.json"
    decl = json.loads(decl_path.read_text())
    decl["retains"] = ["W-002"]
    decl_path.write_text(json.dumps(decl))
    commit_all(root, "close W-001, retain W-002")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == [] and d["delivers"] == ["W-001"] and d["retains"] == ["W-002"]


def test_retains_id_already_closed_fails(root):
    init_main(root)
    start_branch(root, "feature")
    ready_w001(root)
    close.close(root, "W-001")
    decl_path = root.repo / "docs/grove/deliveries/feature.json"
    decl = json.loads(decl_path.read_text())
    decl["retains"] = ["W-000"]  # already closed in history at base
    decl_path.write_text(json.dumps(decl))
    commit_all(root, "close W-001, wrongly retain closed W-000")
    d = delivery.verify_delivery(root, "feature", "main")
    assert d["errors"] == ["retains W-000: already closed"]


# --- portability: read-only in a fresh clone -----------------------------------------------------

def test_fresh_clone_matches(root, tmp_path):
    init_main(root)
    start_branch(root, "feature")
    ready_w001(root)
    close.close(root, "W-001")
    commit_all(root, "close W-001")
    d1 = delivery.verify_delivery(root, "feature", "main")

    clone_dir = tmp_path.parent / (tmp_path.name + "-clone")
    subprocess.run(["git", "clone", "-q", str(root.repo), str(clone_dir)], check=True, capture_output=True)
    for name in ("main", "feature"):  # a local clone only auto-tracks the source's checked-out branch
        subprocess.run(["git", "-C", str(clone_dir), "checkout", "-q", "-B", name, f"origin/{name}"], check=True, capture_output=True)
    clone_root = load_root(clone_dir)
    d2 = delivery.verify_delivery(clone_root, "feature", "main")
    assert d1 == d2


# --- CLI wiring: exit codes 0 (pass), 1 (content failure), 2 (inapplicable) --------------------

def test_cli_exit_codes(root, monkeypatch, capsys):
    init_main(root)
    start_branch(root, "feature")
    monkeypatch.chdir(root.repo)
    code = cli.main(["verify-delivery", "feature", "--base", "main"])
    assert code == 2 and "no delivery declaration" in capsys.readouterr().err

    close.record_delivery(root, "W-002")  # still proposed
    commit_all(root, "declare")
    code = cli.main(["verify-delivery", "feature", "--base", "main"])
    out = capsys.readouterr().out
    assert code == 1 and "W-002" in out and "checked" in out

    ready_w001(root)
    close.close(root, "W-001")
    commit_all(root, "close W-001 too")
    code = cli.main(["verify-delivery", "feature", "--base", "main", "--json"])
    d = json.loads(capsys.readouterr().out)
    assert code == 1 and d["errors"] == ["W-002: proposed work is not archived"]
