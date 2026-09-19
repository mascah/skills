"""W-016: grove launch prints one paste-ready /goal message for one or more work units."""
import shutil

import pytest

from grove import cli
from grove.launch import LaunchBlocked, launch
from grove.pages import GroveError
from conftest import FIX, edit


@pytest.fixture
def repo(tmp_path, monkeypatch):
    shutil.copytree(FIX, tmp_path, dirs_exist_ok=True)
    monkeypatch.chdir(tmp_path)
    return tmp_path


def run(capsys, *args):
    code = cli.main(list(args))
    out = capsys.readouterr()
    return code, out.out, out.err


def test_launch_prints_one_goal_line(root):
    msg = launch(root, ["W-004", "W-001"])
    lines = msg.splitlines()
    assert len(lines) == 1 and msg.endswith("\n")
    line = lines[0]
    assert line.startswith("/goal ")
    assert "grove:work skill for W-004, W-001" in line
    assert "grove status lists each unit under Recent" in line
    assert "grove lint reports 0 errors" in line
    assert "Conventional Commits subject and a Refs: footer" in line
    assert "tells the human how to merge" in line
    assert "bounded fix rounds ran out" in line
    assert "acceptance box needs a human judgment" in line
    assert "Never write code, run tests or debug in this session" in line
    assert "resume from grove status and .grove-run/ledger.md" in line
    assert "do not restart the run" in line


def test_launch_cli_writes_only_the_message_to_stdout(repo, capsys):
    code, out, err = run(capsys, "launch", "W-004", "W-001")
    assert code == 0 and err == ""
    assert out.count("\n") == 1
    assert out.startswith("/goal ")


def test_launch_cli_refuses_closed_unknown_release(repo, capsys):
    code, out, err = run(capsys, "launch", "W-000")
    assert code == 1 and out == "" and err.startswith("grove: ")
    code, out, err = run(capsys, "launch", "W-999")
    assert code == 1 and out == "" and err.startswith("grove: ")


def test_launch_cli_exits_2_on_blocker(repo, capsys):
    p = repo / "docs/grove/work/W-002-selection-brackets.md"
    p.write_text(p.read_text().replace("scope: [fly-ship]", "scope: [fly-ship]\ndepends_on: [W-004]"))
    code, out, err = run(capsys, "launch", "W-002")
    assert code == 2 and out == "" and "W-004 is not closed" in err


def test_launch_refuses_closed_unknown_and_release_ids(root):
    with pytest.raises(GroveError):
        launch(root, ["W-000"])  # closed/release, lives in history
    with pytest.raises(GroveError):
        launch(root, ["W-999"])  # unknown


def test_launch_exits_2_on_external_blocker(root):
    edit(root, "docs/grove/work/W-002-selection-brackets.md", "scope: [fly-ship]", "scope: [fly-ship]\ndepends_on: [W-004]")
    with pytest.raises(LaunchBlocked) as exc:
        launch(root, ["W-002"])
    assert any("W-004 is not closed" in b for b in exc.value.blockers)


def test_launch_prints_with_only_a_preparation_gap(root):
    # W-003 has a prose Dependencies section but no depends_on field: a preparation gap, not a blocker.
    msg = launch(root, ["W-003"])
    assert msg.startswith("/goal ") and len(msg.splitlines()) == 1
