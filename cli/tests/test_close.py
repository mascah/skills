import json
import pytest
from grove import close
from grove.pages import GroveError
from conftest import edit, git_init

W = "docs/grove/work/W-001-engage-range-readout.md"


def ready(root):
    edit(root, W, "status: active", "status: done")
    edit(root, W, "- [ ]", "- [x]")
    edit(root, W, "## Evidence\n", "## Evidence\nHUD shows range; 3 scenario tests pass.\n")
    edit(root, "docs/grove/capabilities/autopilot.md", "updated: 2026-09-09", "updated: 2026-09-13")
    edit(root, "docs/grove/capabilities/autopilot.md", "- [ ] Engage range is shown and changeable.", "- [x] Engage range is shown and changeable.")


def test_close_moves_and_reports(root):
    git_init(root)
    ready(root)
    r = close.close(root, "W-001")
    assert r["id"] == "W-001" and r["updated"] == ["autopilot"] and r["unchanged"] == []
    assert r["moved_to"] == "docs/grove/history/work/W-001-engage-range-readout.md"
    assert (root.repo / r["moved_to"]).exists() and not (root.repo / W).exists()
    assert r["next"]["id"] == "W-003"  # W-002 has an unresolved blocking question
    assert "3 scenario tests pass" in r["evidence"]
    assert r["declaration"].startswith("docs/grove/deliveries/") and r["declaration"].endswith(".json")
    decl = json.loads((root.repo / r["declaration"]).read_text())
    assert decl == {"schema": 1, "delivers": ["W-001"], "retains": []}


def test_close_declaration_idempotent_and_detached_head_refused(root):
    git_init(root)
    ready(root)
    close.close(root, "W-001")
    branch = (root.repo / "docs/grove/deliveries").glob("*.json")
    decl_path = next(branch)
    before = decl_path.read_text()
    # re-closing the same id is unreachable via close() (already archived), so exercise
    # record_delivery directly to prove appends are idempotent.
    close.record_delivery(root, "W-001")
    assert decl_path.read_text() == before


def test_refuses_not_done(root):
    with pytest.raises(GroveError, match="status is active, not done"):
        close.close(root, "W-001")


def test_refuses_empty_evidence(root):
    edit(root, W, "status: active", "status: done")
    edit(root, W, "- [ ]", "- [x]")
    with pytest.raises(GroveError, match="Evidence section is empty"):
        close.close(root, "W-001")


def test_refuses_stale_capability(root):
    edit(root, W, "status: active", "status: done")
    edit(root, W, "- [ ]", "- [x]")
    edit(root, W, "## Evidence\n", "## Evidence\nok\n")
    with pytest.raises(GroveError, match="autopilot updated 2026-09-09 is before W-001 started 2026-09-12"):
        close.close(root, "W-001")


def test_unchanged_list_satisfies_staleness(root):
    git_init(root)
    edit(root, W, "status: active", "status: done")
    edit(root, W, "- [ ]", "- [x]")
    edit(root, W, "## Evidence\n", "## Evidence\nok\n")
    edit(root, W, "started: 2026-09-12\n", "started: 2026-09-12\nunchanged: [autopilot]\n")
    r = close.close(root, "W-001")
    assert r["updated"] == [] and r["unchanged"] == ["autopilot"]


def test_refuses_on_lint_error(root):
    ready(root)
    edit(root, "docs/grove/terms/tick.md", "status: settled", "status: gone")
    with pytest.raises(GroveError, match="lint has 1 error"):
        close.close(root, "W-001")


def test_refuses_on_bad_date(root):
    ready(root)
    edit(root, "docs/grove/capabilities/autopilot.md", "updated: 2026-09-13", "updated: 2026-9-13")
    with pytest.raises(GroveError, match="bad date"):
        close.close(root, "W-001")


def test_unknown_work(root):
    with pytest.raises(GroveError, match="no work unit W-404"):
        close.close(root, "W-404")


def test_closure_errors_matches_close_without_moving(root):
    with pytest.raises(GroveError) as exc:
        close.close(root, "W-001")
    work = root.get("W-001")
    errors = close.closure_errors(root, work)
    assert errors and errors[0] == str(exc.value)
    assert (root.repo / W).exists()


def test_record_delivery_refuses_detached_head(root):
    git_init(root)
    ready(root)
    sha = close.git(root.repo, "rev-parse", "HEAD").strip()
    close.git(root.repo, "checkout", "--detach", sha)
    with pytest.raises(GroveError, match="detached HEAD"):
        close.close(root, "W-001")
    assert (root.repo / W).exists()  # refused before anything moved
    assert not (root.repo / "docs/grove/history/work/W-001-engage-range-readout.md").exists()
