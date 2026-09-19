from grove import init
from grove.pages import load_root


def test_init_fresh_repo(tmp_path):
    actions = init.init(tmp_path)
    assert (tmp_path / "grove.toml").read_text() == f'schema = 2\nproject = "{tmp_path.name}"\nroot = "docs/grove"\n'
    k = tmp_path / "docs" / "grove"
    for d in ("capabilities", "decisions", "work", "questions", "terms", "history/work", "history/decisions", "history/evidence"):
        assert (k / d / ".gitkeep").exists(), d
    assert (k / "brief.md").read_text().startswith("---\ntype: brief\nid: brief\nstatus: active\n")
    assert (k / "history" / "README.md").exists()
    for f in ("CLAUDE.md", "AGENTS.md"):
        t = (tmp_path / f).read_text()
        assert t.count(init.BLOCK_BEGIN) == 1 and "grove status" in t and "grove context --work" in t and "grove lint" in t and "grove:close" in t and "Conventional Commits" in t and "Refs: <id>" in t
        assert "never commits to main" in t
    assert "wrote grove.toml" in actions and "wrote CLAUDE.md block" in actions
    assert load_root(tmp_path).project == tmp_path.name


def test_init_preserves_user_text_and_is_idempotent(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# My rules\nAlways run cargo test.\n")
    init.init(tmp_path)
    t = (tmp_path / "CLAUDE.md").read_text()
    assert t.startswith("# My rules\nAlways run cargo test.\n") and t.count(init.BLOCK_BEGIN) == 1
    (tmp_path / "docs" / "grove" / "brief.md").write_text("---\ntype: brief\nid: brief\nstatus: active\nupdated: 2026-01-01\n---\n## Pitch\nmine\n")
    actions = init.init(tmp_path)
    assert (tmp_path / "docs" / "grove" / "brief.md").read_text().endswith("## Pitch\nmine\n")
    assert (tmp_path / "CLAUDE.md").read_text().count(init.BLOCK_BEGIN) == 1
    assert actions == []


def test_replace_block_swaps_only_managed_text():
    old = "before\n<!-- grove:begin -->\nstale\n<!-- grove:end -->\nafter\n"
    assert init.replace_block(old, "fresh") == "before\n<!-- grove:begin -->\nfresh\n<!-- grove:end -->\nafter\n"
    assert init.replace_block("x\n", "fresh") == "x\n\n<!-- grove:begin -->\nfresh\n<!-- grove:end -->\n"


def test_replace_block_handles_crlf():
    old = "before\r\n<!-- grove:begin -->\r\nstale\r\n<!-- grove:end -->\r\nafter\r\n"
    result = init.replace_block(old, "fresh")
    assert result.count(init.BLOCK_BEGIN) == 1
    assert "fresh" in result
    assert "stale" not in result
    assert result.startswith("before\r\n")
    assert result.endswith("after\r\n")


def test_replace_block_malformed_no_end():
    import pytest
    from grove.pages import GroveError
    old = "x\n<!-- grove:begin -->\nstale\n"
    with pytest.raises(GroveError) as exc_info:
        init.replace_block(old, "fresh")
    assert "malformed" in str(exc_info.value)


def test_replace_block_malformed_reversed():
    import pytest
    from grove.pages import GroveError
    old = "<!-- grove:end -->\n<!-- grove:begin -->\n"
    with pytest.raises(GroveError) as exc_info:
        init.replace_block(old, "fresh")
    assert "malformed" in str(exc_info.value)


def test_init_malformed_markers_raises_error(tmp_path):
    import pytest
    from grove.pages import GroveError
    (tmp_path / "CLAUDE.md").write_text("x\n<!-- grove:begin -->\nstale\n")
    with pytest.raises(GroveError) as exc_info:
        init.init(tmp_path)
    assert "CLAUDE.md" in str(exc_info.value)
    assert "malformed" in str(exc_info.value)
    assert (tmp_path / "CLAUDE.md").read_text() == "x\n<!-- grove:begin -->\nstale\n"


def test_init_quoted_project_name(tmp_path):
    repo = tmp_path / 'foo"bar'
    repo.mkdir()
    actions = init.init(repo)
    assert load_root(repo).project == 'foo"bar'
    assert (repo / "grove.toml").read_text() == 'schema = 2\nproject = "foo\\"bar"\nroot = "docs/grove"\n'


def test_init_refreshes_existing_configured_root(tmp_path):
    (tmp_path / "grove.toml").write_text('schema = 2\nproject = "custom"\nroot = "knowledge"\n')
    init.init(tmp_path)
    assert (tmp_path / "knowledge/brief.md").exists()
    assert not (tmp_path / "docs/grove").exists()
    assert '`knowledge/`' in (tmp_path / "AGENTS.md").read_text()
