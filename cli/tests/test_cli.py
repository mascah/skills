import json
import os
import shutil
import pytest
from grove import cli
from conftest import FIX


@pytest.fixture
def repo(tmp_path, monkeypatch):
    shutil.copytree(FIX, tmp_path, dirs_exist_ok=True)
    monkeypatch.chdir(tmp_path)
    return tmp_path


def run(capsys, *args):
    code = cli.main(list(args))
    out = capsys.readouterr()
    return code, out.out, out.err


def test_status_text_and_json(repo, capsys):
    code, out, _ = run(capsys, "status")
    assert code == 0 and out.startswith("# demo\n")
    code, out, _ = run(capsys, "status", "--json")
    assert code == 0 and json.loads(out)["active"][0]["id"] == "W-001"


def test_lint_exit_codes(repo, capsys):
    code, out, _ = run(capsys, "lint")
    assert code == 0 and "lint: 0 errors, 2 warnings" in out and "warning:" in out
    t = repo / "docs/grove/terms/tick.md"
    t.write_text(t.read_text().replace("status: settled", "status: gone"))
    code, out, _ = run(capsys, "lint")
    assert code == 1 and "bad status 'gone'" in out


def test_context_exit_codes(repo, capsys):
    code, out, _ = run(capsys, "context", "--work", "W-001")
    assert code == 0 and out.startswith("# Context: W-001 (implement)")
    code, out, _ = run(capsys, "context", "--work", "W-001", "--budget", "100")
    assert code == 2 and "## Errors" in out
    code, out, _ = run(capsys, "context", "--work", "W-001", "--phase", "shape", "--json")
    assert code == 0 and "brief#not-now" in json.loads(out)["pages"]


def test_grove_error_exit_1(repo, capsys):
    code, _, err = run(capsys, "context", "--work", "W-999")
    assert code == 1 and "no work unit W-999" in err


def test_find_and_close_and_init(repo, capsys):
    if shutil.which("rg"):
        code, out, _ = run(capsys, "find", "orbit")
        assert code == 0 and "capability autopilot draft" in out
    code, _, err = run(capsys, "close", "W-001")
    assert code == 1 and "not done" in err
    code, out, _ = run(capsys, "init")
    assert code == 0 and "CLAUDE.md block" in out


def test_no_config(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    code, _, err = run(capsys, "status")
    assert code == 1 and "grove init" in err


def test_invalid_grove_toml(repo, capsys):
    (repo / "grove.toml").write_text("schema = = 1\n")
    code, _, err = run(capsys, "status")
    assert code == 1 and "grove.toml" in err and "not valid TOML" in err
