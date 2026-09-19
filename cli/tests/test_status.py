import json
import os
import subprocess

import pytest
from grove import claims, status
from grove.pages import load_root
from conftest import edit, git_init


def env(repo):
    return {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@x", "PATH": os.environ["PATH"], "HOME": str(repo)}


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True, env=env(repo)).stdout.strip()


@pytest.fixture
def linked(root, tmp_path):
    """main (root, branch main) plus a linked worktree on branch a; W-002 depends on W-001."""
    edit(root, "docs/grove/work/W-002-selection-brackets.md", "scope: [fly-ship]", "scope: [fly-ship]\ndepends_on: [W-001]")
    git_init(root)
    wts = tmp_path.parent / (tmp_path.name + "-wts")
    wts.mkdir()
    wt_a = wts / "wt-a"
    git(root.repo, "worktree", "add", "-b", "a", str(wt_a))
    return root, load_root(wt_a)


def close_on_branch(a):
    """Move W-001 into history on branch a's checkout and commit, simulating an unintegrated close."""
    dest = a.repo / "docs" / "grove" / "history" / "work"
    dest.mkdir(parents=True, exist_ok=True)
    src = a.repo / "docs" / "grove" / "work" / "W-001-engage-range-readout.md"
    dest_file = dest / src.name
    dest_file.write_text(src.read_text().replace("status: active", "status: done"))
    src.unlink()
    git(a.repo, "add", "-A")
    git(a.repo, "commit", "-q", "-m", "close W-001 on branch")


def test_status_claim_text_and_json(linked):
    main, a = linked
    claims.acquire(a, ["W-001"])
    d = status.status(main)
    by_id = {c["id"]: c for c in d["claims"]}
    assert by_id["W-001"]["branch"] == "a" and by_id["W-001"]["observation"] == "active on branch"
    row = next(w for w in d["active"] if w["id"] == "W-001")
    assert row["claim"]["branch"] == "a" and row["claim"]["observation"] == "active on branch"
    json.dumps(d)  # the whole structure must be JSON-safe

    out = status.render_status(d)
    assert f"claimed on a ({a.repo}) · active on branch" in out


def test_closed_on_branch_does_not_satisfy_main_dependency(linked):
    main, a = linked
    claims.acquire(a, ["W-001"])
    close_on_branch(a)

    d = status.status(main)
    by_id = {c["id"]: c for c in d["claims"]}
    assert by_id["W-001"]["observation"] == "closed on branch, awaiting integration"
    w001 = next(w for w in d["active"] if w["id"] == "W-001")
    assert w001["readiness"] != "closed"
    w002 = next(w for w in d["proposed"] if w["id"] == "W-002")
    assert w002["readiness"] == "blocked"
    assert "W-001 is not closed" in w002["blockers"]


def test_recommendation_skips_a_foreign_claim(linked):
    main, a = linked
    claims.acquire(a, ["W-001"])
    d = status.status(main)
    assert d["recommendation"] is None or d["recommendation"]["id"] != "W-001"
    assert d["coordinate"] == "resume or coordinate: claimed on a"
    assert "resume or coordinate: claimed on a" in status.render_status(d)


def test_observe_integrated_after_merge(linked):
    main, a = linked
    claims.acquire(a, ["W-001"])
    close_on_branch(a)
    git(main.repo, "merge", "a", "--no-edit", "-q")

    d = status.status(main)
    by_id = {c["id"]: c for c in d["claims"]}
    assert by_id["W-001"]["observation"] == "integrated"


def test_observe_possibly_squash_merged(linked):
    main, a = linked
    claims.acquire(a, ["W-001"])
    close_on_branch(a)  # branch a now has the history page, unmerged
    dest = main.repo / "docs" / "grove" / "history" / "work"
    dest.mkdir(parents=True, exist_ok=True)
    src = main.repo / "docs" / "grove" / "work" / "W-001-engage-range-readout.md"
    (dest / src.name).write_text(src.read_text().replace("status: active", "status: done"))
    src.unlink()
    git(main.repo, "add", "-A")
    git(main.repo, "commit", "-q", "-m", "squash close W-001")

    d = status.status(main)
    by_id = {c["id"]: c for c in d["claims"]}
    assert by_id["W-001"]["observation"] == "possibly squash-merged: verify and release with --take"


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
