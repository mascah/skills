import shutil
from pathlib import Path
import pytest
from grove.pages import load_root

FIX = Path(__file__).parent / "fixtures" / "repo"


@pytest.fixture
def root(tmp_path):
    shutil.copytree(FIX, tmp_path, dirs_exist_ok=True)
    return load_root(tmp_path)


def edit(root, rel, old, new):
    p = root.repo / rel
    text = p.read_text()
    assert old in text, f"{old!r} not in {rel}"
    p.write_text(text.replace(old, new))
    return p


def git_init(root):
    """Commit the fixture so the checkout has a HEAD; returns the head sha."""
    import subprocess
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@x", "PATH": __import__("os").environ["PATH"], "HOME": str(root.repo)}
    run = lambda *a: subprocess.run(["git", "-C", str(root.repo), *a], check=True, capture_output=True, text=True, env=env).stdout.strip()
    run("init", "-q")
    run("add", "-A")
    run("commit", "-q", "-m", "fixture")
    return run("rev-parse", "HEAD")
