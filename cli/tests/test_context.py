import pytest
from grove import context
from grove.pages import GroveError
from conftest import edit


def names(items):
    return [i["basename"] for i in items]


def test_implement_tiers(root):
    d = context.context(root, "W-001")
    assert names(d["included"]) == ["W-001-engage-range-readout", "autopilot", "D-0001-adaptive-autopilot", "tick"]
    assert [i["tier"] for i in d["included"]] == [1, 2, 3, 4]
    assert "target-locks" not in names(d["included"])  # blocks W-002 and links fly-ship, neither in W-001 scope
    assert d["code"] == ["crates/sim/src/autopilot.rs"]
    assert d["omitted"] == [] and d["errors"] == []
    assert "D-0002-no-target-locks" not in names(d["included"])  # rejected hidden in implement
    assert "D-0000-fixed-orbit" not in names(d["included"])  # superseded never


def test_question_included_via_blocks_or_body_link(root):
    d = context.context(root, "W-002")
    assert "target-locks" in names(d["included"])  # via blocks
    edit(root, "docs/grove/questions/target-locks.md", "blocks: [W-002]", "blocks: []")
    d = context.context(root, "W-002")
    assert "target-locks" in names(d["included"])  # via [[fly-ship]] in body, fly-ship in W-002 scope


def test_shape_adds_rejected_and_not_now(root):
    d = context.context(root, "W-001", phase="shape")
    assert "D-0002-no-target-locks" in names(d["included"])
    assert "brief#not-now" in names(d["included"])
    assert "Player markets" in d["pages"]["brief#not-now"]


def test_budget_omits_lower_tiers_first(root):
    full = context.context(root, "W-001")["used"]
    d = context.context(root, "W-001", budget=full - 1)
    assert names(d["omitted"]) == ["tick"] and d["errors"] == []


def test_budget_error_when_tier_1_to_3_omitted(root):
    d = context.context(root, "W-001", budget=20)
    assert names(d["included"]) == []
    assert any("W-001-engage-range-readout" in e and "does not fit" in e for e in d["errors"])


def test_unknown_work_and_phase(root):
    with pytest.raises(GroveError, match="no work unit W-999"):
        context.context(root, "W-999")
    with pytest.raises(GroveError, match="phase"):
        context.context(root, "W-001", phase="dance")


def test_render(root):
    full = context.context(root, "W-001")["used"]
    out = context.render_context(context.context(root, "W-001", budget=full - 1))
    assert out.startswith("# Context: W-001 (implement)")
    assert "## Code\n- crates/sim/src/autopilot.rs" in out
    assert "## Sources\n" in out and "docs/grove/work/W-001-engage-range-readout.md" in out
    assert "## Omitted\n" in out and "grove find" in out


def test_render_debrief_and_debug(root):
    out = context.render_context(context.context(root, "W-001", phase="debrief"))
    assert "## Acceptance checklist\n- [ ] Range shown before the autopilot acts." in out
    out = context.render_context(context.context(root, "W-001", phase="debug"))
    assert out.index("## Code") < out.index("<!-- tick -->")


# Fix round 1 tests
def test_debrief_acceptance_when_work_omitted(root):
    work_tokens = root.get("W-001").tokens()
    # budget = work_tokens - 1, so W-001 doesn't fit but may allow smaller items
    budget = work_tokens - 1
    d = context.context(root, "W-001", phase="debrief", budget=budget)
    # W-001 should not be included
    assert all(i["basename"] != "W-001-engage-range-readout" for i in d["included"])
    # But acceptance should be rendered from d["acceptance"]
    out = context.render_context(d)
    assert "## Acceptance checklist\n- [ ] Range shown before the autopilot acts." in out


def test_tier_4_terms_from_included_only(root):
    work_tokens = root.get("W-001").tokens()
    tick_tokens = root.get("tick").tokens()
    # budget = work_tokens + tick_tokens, enough for both if they were both candidates
    budget = work_tokens + tick_tokens
    d = context.context(root, "W-001", budget=budget)
    # W-001 fits, autopilot doesn't
    assert d["included"][0]["basename"] == "W-001-engage-range-readout"
    assert all(i["basename"] != "autopilot" for i in d["included"])
    # tick is linked from autopilot (not included), not from W-001
    # So it should not be included or even attempted
    assert all(i["basename"] != "tick" for i in d["included"])
    assert all(i["basename"] != "tick" for i in d["omitted"])


def test_scoped_capability_filters_history_and_type(root):
    # tick is a term, not a capability; add it to scope
    edit(root, "docs/grove/work/W-001-engage-range-readout.md", "scope: [autopilot]", "scope: [autopilot, tick]")
    d = context.context(root, "W-001")
    # tick should not be included at tier 2 (it's not a capability)
    assert not any(i["tier"] == 2 and i["basename"] == "tick" for i in d["included"])


def test_shape_not_now_omitted_is_not_an_error(root):
    full = context.context(root, "W-001", phase="shape")
    tier123 = sum(i["tokens"] for i in full["included"] if i["tier"] <= 3 and i["basename"] != "brief#not-now")
    d = context.context(root, "W-001", phase="shape", budget=tier123)
    assert d["errors"] == []
    assert "brief#not-now" in names(d["omitted"])


def test_brief_not_now_rel_uses_configured_root(root):
    import shutil
    # Change grove.toml to use "knowledge" as root
    groovy = root.repo / "grove.toml"
    groovy.write_text('schema = 1\nproject = "demo"\nroot = "knowledge"\n')
    # Move docs/grove to knowledge
    shutil.move(str(root.repo / "docs" / "grove"), str(root.repo / "knowledge"))
    # Reload root
    from grove.pages import load_root
    root_reloaded = load_root(root.repo)
    d = context.context(root_reloaded, "W-001", phase="shape")
    # Find brief#not-now entry
    brief_not_now = next((i for i in d["included"] if i["basename"] == "brief#not-now"), None)
    assert brief_not_now is not None
    # Its rel should be knowledge/brief.md
    assert brief_not_now["rel"] == "knowledge/brief.md"
