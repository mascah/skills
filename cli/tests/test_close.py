import pytest
from grove import close
from grove.pages import GroveError
from conftest import edit

W = "docs/grove/work/W-001-engage-range-readout.md"


def ready(root):
    edit(root, W, "status: active", "status: done")
    edit(root, W, "- [ ]", "- [x]")
    edit(root, W, "## Evidence\n", "## Evidence\nHUD shows range; 3 scenario tests pass.\n")
    edit(root, "docs/grove/capabilities/autopilot.md", "updated: 2026-09-09", "updated: 2026-09-13")
    edit(root, "docs/grove/capabilities/autopilot.md", "- [ ] Engage range is shown and changeable.", "- [x] Engage range is shown and changeable.")


def test_close_moves_and_reports(root):
    ready(root)
    r = close.close(root, "W-001")
    assert r["id"] == "W-001" and r["updated"] == ["autopilot"] and r["unchanged"] == []
    assert r["moved_to"] == "docs/grove/history/work/W-001-engage-range-readout.md"
    assert (root.repo / r["moved_to"]).exists() and not (root.repo / W).exists()
    assert r["next"]["id"] == "W-003"  # W-002 has an unresolved blocking question
    assert "3 scenario tests pass" in r["evidence"]


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
