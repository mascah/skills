import shutil
import pytest
from grove import find
from grove.pages import GroveError

pytestmark = pytest.mark.skipif(shutil.which("rg") is None, reason="ripgrep not installed")


def test_find_excludes_history_by_default(root):
    hits = find.find(root, "orbit")
    assert any(h.startswith("capability autopilot draft docs/grove/capabilities/autopilot.md:") for h in hits)
    assert not any("history/" in h for h in hits)
    hits = find.find(root, "orbit", history=True)
    assert any("decision D-0000 superseded docs/grove/history/decisions/D-0000-fixed-orbit.md:" in h for h in hits)


def test_find_type_filter_and_regex(root):
    hits = find.find(root, "tick", type_="term")
    assert hits and all(h.startswith("term ") for h in hits)
    hits = find.find(root, r"W-00[23]", regex=True)
    assert any("question target-locks open" in h for h in hits)


def test_find_no_hits(root):
    assert find.find(root, "zzzzzz") == []


def test_find_without_rg(root, monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: None)
    with pytest.raises(GroveError, match="ripgrep"):
        find.find(root, "x")


def test_find_non_page_hits(root):
    hits = find.find(root, "vault", history=True)
    assert len(hits) == 1
    assert hits[0].startswith("file README - docs/grove/history/README.md:1:")
    assert not any("None" in h for h in hits)
    no_history = find.find(root, "vault")
    assert no_history == []
