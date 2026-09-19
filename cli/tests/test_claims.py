import json
import os
import re
import shutil
import subprocess
import threading

import pytest
from grove import cli, claims
from grove.pages import GroveError, load_root
from conftest import git_init


def env(repo):
    return {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@x", "PATH": os.environ["PATH"], "HOME": str(repo)}


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True, env=env(repo)).stdout.strip()


@pytest.fixture
def three(root, tmp_path):
    """main (root) plus two linked worktrees on branches a and b, all sharing one common git dir."""
    git_init(root)
    wts = tmp_path.parent / (tmp_path.name + "-wts")  # sibling dir: nesting worktrees inside repo pollutes its own status
    wts.mkdir()
    wt_a, wt_b = wts / "wt-a", wts / "wt-b"
    git(root.repo, "worktree", "add", "-b", "a", str(wt_a))
    git(root.repo, "worktree", "add", "-b", "b", str(wt_b))
    return root, load_root(wt_a), load_root(wt_b)


# --- acquire/release/take, atomicity ---------------------------------------------------------

def test_visible_from_every_checkout_no_commit_no_tracked_change(three):
    main, a, b = three
    head_before = git(main.repo, "rev-parse", "HEAD")
    claims.acquire(a, ["W-001"])
    assert git(main.repo, "rev-parse", "HEAD") == head_before
    assert git(main.repo, "status", "--porcelain") == ""
    for r in (main, a, b):
        c = claims.load_claims(r.repo)["claims"]["W-001"]
        assert c["branch"] == "a" and c["worktree"] == str(a.repo)


def test_multi_id_conflict_leaves_no_partial_write(three):
    main, a, b = three
    claims.acquire(a, ["W-001"])
    with pytest.raises(claims.Owned):
        claims.acquire(b, ["W-002", "W-001"])
    data = claims.load_claims(main.repo)["claims"]
    assert "W-002" not in data
    assert data["W-001"]["branch"] == "a"


def test_same_owner_retry_is_noop(three):
    main, a, b = three
    first = claims.acquire(a, ["W-001"])["W-001"]
    again = claims.acquire(a, ["W-001"])["W-001"]
    assert again == first


def test_foreign_release_refused_take_succeeds(three):
    main, a, b = three
    claims.acquire(a, ["W-001"])
    with pytest.raises(claims.Owned, match="use --take"):
        claims.release(main, ["W-001"])
    taken = claims.acquire(main, ["W-001"], take=True)["W-001"]
    assert taken["branch"] != "a"
    released = claims.release(main, ["W-001"])
    assert released == ["W-001"]
    assert "W-001" not in claims.load_claims(main.repo)["claims"]


def test_concurrent_claim_same_id_one_owner(three):
    main, a, b = three
    outcomes = {}

    def go(name, r):
        try:
            outcomes[name] = ("ok", claims.acquire(r, ["W-004"])["W-004"]["branch"])
        except GroveError as exc:
            outcomes[name] = ("refused", str(exc))

    ta = threading.Thread(target=go, args=("a", a))
    tb = threading.Thread(target=go, args=("b", b))
    ta.start(); tb.start(); ta.join(); tb.join()

    assert sum(v[0] == "ok" for v in outcomes.values()) == 1
    winner = next(v[1] for v in outcomes.values() if v[0] == "ok")
    assert claims.load_claims(main.repo)["claims"]["W-004"]["branch"] == winner


# --- lock contention -------------------------------------------------------------------------

def test_lock_held_refuses_naming_the_lock_path(root):
    git_init(root)
    lock = claims._grove_dir(root.repo) / "claims.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.touch()
    with pytest.raises(GroveError, match=re.escape(str(lock))):
        claims.acquire(root, ["W-001"])


# --- malformed registry ------------------------------------------------------------------------

def test_malformed_registry(root):
    git_init(root)
    path = claims.registry_path(root.repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json")
    with pytest.raises(GroveError, match="claims registry unreadable"):
        claims.load_claims(root.repo)


# --- observe() ----------------------------------------------------------------------------------

def test_observe_worktree_missing(three):
    main, a, b = three
    c = claims.acquire(a, ["W-003"])["W-003"]
    gone = {**c, "worktree": str(a.repo.parent / "nope")}
    assert claims.observe(main, "W-003", gone) == "worktree missing"


def test_observe_branch_gone(three):
    main, a, b = three
    c = claims.acquire(a, ["W-003"])["W-003"]
    ghost = {**c, "branch": "does-not-exist"}
    assert claims.observe(main, "W-003", ghost) == "branch gone"


def test_observe_active_and_proposed_on_branch(three):
    main, a, b = three
    ca = claims.acquire(a, ["W-001"])["W-001"]  # fixture status: active
    cb = claims.acquire(b, ["W-002"])["W-002"]  # fixture status: proposed
    assert claims.observe(main, "W-001", ca) == "active on branch"
    assert claims.observe(main, "W-002", cb) == "proposed on branch"


def test_observe_closed_on_branch_awaiting_integration(three):
    main, a, b = three
    c = claims.acquire(a, ["W-001"])["W-001"]
    dest_dir = a.repo / "docs" / "grove" / "history" / "work"
    dest_dir.mkdir(parents=True, exist_ok=True)
    (a.repo / "docs" / "grove" / "work" / "W-001-engage-range-readout.md").rename(dest_dir / "W-001-engage-range-readout.md")
    git(a.repo, "add", "-A")
    git(a.repo, "commit", "-q", "-m", "close W-001")
    assert claims.observe(main, "W-001", c) == "closed on branch, awaiting integration"


def test_observe_from_owning_worktree_never_integrated(three):
    """From the checkout that owns the claim, HEAD *is* the claim's branch, so the ancestor test
    would always hold. That must read as 'closed on branch', not 'integrated', both before and
    after main actually merges the branch -- this checkout has no way to see the merge landed
    elsewhere. Only a checkout whose current branch differs from the claim's may report
    'integrated'."""
    main, a, b = three
    c = claims.acquire(a, ["W-001"])["W-001"]
    dest_dir = a.repo / "docs" / "grove" / "history" / "work"
    dest_dir.mkdir(parents=True, exist_ok=True)
    (a.repo / "docs" / "grove" / "work" / "W-001-engage-range-readout.md").rename(dest_dir / "W-001-engage-range-readout.md")
    git(a.repo, "add", "-A")
    git(a.repo, "commit", "-q", "-m", "close W-001")

    assert claims.observe(a, "W-001", c) == "closed on branch, awaiting integration"
    assert claims.observe(main, "W-001", c) == "closed on branch, awaiting integration"

    git(main.repo, "merge", "a", "--no-edit", "-q")
    assert claims.observe(main, "W-001", c) == "integrated"
    assert claims.observe(a, "W-001", c) == "closed on branch, awaiting integration"


# --- CLI ------------------------------------------------------------------------------------

def test_cli_claim_conflict_exits_4(three, monkeypatch, capsys):
    main, a, b = three
    monkeypatch.chdir(a.repo)
    assert cli.main(["claim", "W-001"]) == 0
    capsys.readouterr()
    monkeypatch.chdir(main.repo)
    assert cli.main(["claim", "W-001"]) == 4
    err = capsys.readouterr().err
    assert "grove:" in err and "W-001" in err


def test_cli_claim_release_take_roundtrip(three, monkeypatch, capsys):
    main, a, b = three
    monkeypatch.chdir(a.repo)
    assert cli.main(["claim", "W-002", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["W-002"]["branch"] == "a"

    monkeypatch.chdir(a.repo)
    assert cli.main(["claim", "W-002"]) == 0  # same-owner retry, no-op
    capsys.readouterr()

    monkeypatch.chdir(main.repo)
    assert cli.main(["claim", "--release", "W-002"]) == 4  # foreign release refused
    capsys.readouterr()
    assert cli.main(["claim", "--take", "W-002"]) == 0
    out = capsys.readouterr().out
    assert "took W-002" in out
    assert cli.main(["claim", "--release", "W-002"]) == 0
    assert "released W-002" in capsys.readouterr().out


def test_cli_claims_listing_text_and_json(three, monkeypatch, capsys):
    main, a, b = three
    monkeypatch.chdir(a.repo)
    cli.main(["claim", "W-001"])
    capsys.readouterr()

    monkeypatch.chdir(main.repo)
    assert cli.main(["claims"]) == 0
    out = capsys.readouterr().out
    assert "W-001" in out and "active on branch" in out

    assert cli.main(["claims", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["W-001"]["observation"] == "active on branch"


def test_cli_claims_worktree_missing(three, monkeypatch, capsys):
    main, a, b = three
    monkeypatch.chdir(a.repo)
    cli.main(["claim", "W-003"])
    capsys.readouterr()
    shutil.rmtree(a.repo)

    monkeypatch.chdir(main.repo)
    assert cli.main(["claims"]) == 0
    assert "worktree missing" in capsys.readouterr().out


def test_cli_claims_malformed_registry(root, monkeypatch, capsys):
    git_init(root)
    path = claims.registry_path(root.repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{bad")
    monkeypatch.chdir(root.repo)
    assert cli.main(["claims"]) == 1
    assert "claims registry unreadable" in capsys.readouterr().err
