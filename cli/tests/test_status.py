from grove import status


def test_status_structure(root):
    d = status.status(root)
    assert d["pitch"].startswith("A browser space game")
    assert d["constraints"].startswith("Solo builder")
    assert [{k: w[k] for k in ("id", "basename", "size", "kind", "outcome", "next")} for w in d["active"]] == [{"id": "W-001", "basename": "W-001-engage-range-readout", "size": "small", "kind": "feature",
                            "outcome": "Enabling engagement shows the orbit range the autopilot will hold and lets the pilot change it.",
                            "next": "Add the range field to the HUD state message."}]
    assert [w["id"] for w in d["proposed"]] == ["W-002", "W-003", "W-004"]
    assert d["proposed"][2]["outcome"] == "Does Babylon 8 break the HUD overlay?"
    assert d["questions"] == [{"id": "target-locks", "blocks": ["W-002"], "question": "Does selection need a lock state for [[fly-ship]]?"}]
    assert d["recent"] == [{"id": "W-000", "updated": "2026-09-10", "outcome": "v3 delivered: the expedition journey."}]
    assert d["lint"] == {"errors": 0, "warnings": 2}


def test_status_orders_blocking_questions_first(root):
    (root.knowledge / "questions" / "art.md").write_text(
        "---\ntype: question\nid: art\nstatus: open\nupdated: 2026-09-13\nblocks: []\n---\n## Question\nWho draws the ships?\n")
    q = status.status(root)["questions"]
    assert [x["id"] for x in q] == ["target-locks", "art"]


def test_render_is_compact(root):
    out = status.render_status(status.status(root))
    assert out.startswith("# demo\n")
    assert "## Active\n- W-001 (small feature): Enabling engagement" in out
    assert "  next: Add the range field" in out
    assert "## Proposed\n- W-002 (bounded feature): Screen-space selection with brackets." in out
    assert "## Questions\n- target-locks [blocks W-002]: Does selection need" in out
    assert "## Recent\n- W-000 2026-09-10: v3 delivered" in out
    assert out.rstrip().endswith("lint: 0 errors, 2 warnings")
    assert len(out) // 4 < 2000
