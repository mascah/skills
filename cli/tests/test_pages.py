from pathlib import Path
import pytest
from grove import pages


def test_parse_frontmatter_scalars_and_lists():
    fm, body = pages.parse_frontmatter(
        '---\ntype: decision\nid: D-0001\nstatus: accepted\nupdated: 2026-09-14\n'
        'applies_to: [fly-ship, autopilot]\nsources: ["https://x", "[[a|b]]"]\n---\n## Context\nhi'
    )
    assert fm == {"type": "decision", "id": "D-0001", "status": "accepted", "updated": "2026-09-14",
                  "applies_to": ["fly-ship", "autopilot"], "sources": ["https://x", "[[a|b]]"]}
    assert body == "## Context\nhi"
    assert pages.parse_frontmatter("no fm") == (None, "no fm")
    fm, _ = pages.parse_frontmatter('---\nblocks:\n  - W-002\n  - W-003\nunchanged: []\n---\n')
    assert fm == {"blocks": ["W-002", "W-003"], "unchanged": []}


def test_links_and_section_and_first_line():
    t = "see [[fly-ship|flight]] and [[D-0001-thing]] and [[tick#h|T]]"
    assert pages.links(t) == ["fly-ship", "D-0001-thing", "tick"]
    body = "## Outcome\n\nRange readout shown.\nMore.\n\n## Next\n- do x\n## Z\n"
    assert pages.section(body, "Outcome") == "Range readout shown.\nMore."
    assert pages.section(body, "Missing") == ""
    assert pages.first_line(pages.section(body, "Next")) == "- do x"
    assert pages.first_line("") == ""


def test_page_identity(tmp_path):
    k = tmp_path / "docs" / "grove"
    (k / "decisions").mkdir(parents=True)
    (k / "history" / "work").mkdir(parents=True)
    d = k / "decisions" / "D-0007-go-server.md"
    d.write_text("---\ntype: decision\nid: D-0007\nstatus: accepted\nupdated: 2026-09-01\napplies_to: [x]\n---\n## Decision\n[[x]]\n")
    w = k / "history" / "work" / "W-003-old.md"
    w.write_text("---\ntype: work\nid: W-003\nstatus: done\nupdated: 2026-09-01\nkind: fix\nsize: small\nscope: [x]\n---\n")
    root = pages.Root(repo=tmp_path, knowledge=k, project="demo", schema=1)
    dp, wp = pages.Page(d, root), pages.Page(w, root)
    assert (dp.type, dp.id, dp.status, dp.basename) == ("decision", "D-0007", "accepted", "D-0007-go-server")
    assert dp.in_history is False and wp.in_history is True
    assert dp.links() == ["x"]
    assert dp.tokens() == len(d.read_text()) // 4
    assert root.rel(d) == "docs/grove/decisions/D-0007-go-server.md"


def test_root_pages_and_lookup(tmp_path):
    k = tmp_path / "docs" / "grove"
    (k / "capabilities").mkdir(parents=True)
    (k / "history" / "decisions").mkdir(parents=True)
    (k / "brief.md").write_text("---\ntype: brief\nid: brief\nstatus: active\nupdated: 2026-09-01\n---\n## Pitch\np\n")
    (k / "capabilities" / "fly-ship.md").write_text("---\ntype: capability\nid: fly-ship\nstatus: settled\nupdated: 2026-09-01\n---\n")
    (k / "history" / "decisions" / "D-0001-old.md").write_text("---\ntype: decision\nid: D-0001\nstatus: superseded\nupdated: 2026-09-01\napplies_to: []\nsuperseded_by: D-0002\n---\n")
    (k / "history" / "README.md").write_text("Bench commit abc.\n")
    (tmp_path / "grove.toml").write_text('schema = 1\nproject = "demo"\nroot = "docs/grove"\n')
    root = pages.load_root(k / "capabilities")
    assert root.project == "demo" and root.knowledge == k
    assert sorted(p.basename for p in root.pages()) == ["brief", "fly-ship"]
    assert sorted(p.basename for p in root.pages(history=True)) == ["D-0001-old", "brief", "fly-ship"]
    assert root.get("D-0001").basename == "D-0001-old"
    assert root.get("fly-ship").type == "capability"
    assert root.get("nope") is None


def test_load_root_errors(tmp_path):
    with pytest.raises(pages.GroveError, match="grove.toml"):
        pages.load_root(tmp_path)
    (tmp_path / "grove.toml").write_text('schema = 99\nproject = "demo"\nroot = "docs/grove"\n')
    with pytest.raises(pages.GroveError, match="schema 99"):
        pages.load_root(tmp_path)


def test_fixture_loads(root):
    live = {p.basename for p in root.pages()}
    assert "W-000-v3-release" not in live and "W-001-engage-range-readout" in live
    assert root.get("W-000").in_history


def test_get_prefers_live_page_over_history_on_duplicate_id(root):
    # history/work/W-000-v3-release.md already carries id W-000; add a live duplicate.
    (root.knowledge / "work" / "W-000-again.md").write_text(
        "---\ntype: work\nid: W-000\nstatus: proposed\nupdated: 2026-09-12\n"
        "kind: feature\nsize: small\nscope: []\n---\n## Outcome\nx\n"
    )
    p = root.get("W-000")
    assert p.basename == "W-000-again" and not p.in_history
