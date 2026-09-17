from grove import lint
from conftest import edit


def errs(root):
    return lint.lint(root)[0]


def warns(root):
    return lint.lint(root)[1]


def test_fixture_is_clean_with_expected_warnings(root):
    e, w = lint.lint(root)
    assert e == []
    assert any("D-0003-single-plane.md: accepted decision referenced by no capability or work" in x for x in w)
    assert any("fly-ship.md: code pointer missing: client/src/hud.ts" in x for x in w)
    assert len(w) == 2


def test_missing_frontmatter_and_fields(root):
    p = root.knowledge / "terms" / "tick.md"
    p.write_text("## Meaning\nno fm\n")
    assert any("terms/tick.md: no frontmatter" in x for x in errs(root))
    p.write_text("---\ntype: term\nstatus: settled\n---\n")
    e = errs(root)
    assert any("missing id" in x for x in e) and any("missing updated" in x for x in e)


def test_type_folder_status_enum(root):
    edit(root, "docs/grove/terms/tick.md", "type: term", "type: decision")
    assert any("type 'decision' but folder says 'term'" in x for x in errs(root))


def test_bad_status_kind_size(root):
    edit(root, "docs/grove/work/W-002-selection-brackets.md", "status: proposed", "status: shipped")
    edit(root, "docs/grove/work/W-002-selection-brackets.md", "kind: feature", "kind: epic")
    edit(root, "docs/grove/work/W-002-selection-brackets.md", "size: bounded", "size: huge")
    e = errs(root)
    assert any("bad status 'shipped'" in x for x in e)
    assert any("bad kind 'epic'" in x for x in e)
    assert any("bad size 'huge'" in x for x in e)


def test_list_fields_and_id_shape(root):
    edit(root, "docs/grove/decisions/D-0002-no-target-locks.md", "applies_to: [autopilot]", "applies_to: autopilot")
    assert any("applies_to must be a list" in x for x in errs(root))
    edit(root, "docs/grove/decisions/D-0001-adaptive-autopilot.md", "id: D-0001", "id: D-9999")
    assert any("id 'D-9999' does not match basename" in x for x in errs(root))


def test_duplicate_basename(root):
    (root.knowledge / "history" / "decisions" / "tick.md").write_text(
        "---\ntype: decision\nid: tick\nstatus: superseded\nupdated: 2026-01-01\napplies_to: []\nsuperseded_by: D-0001\n---\n")
    assert any("duplicate basename 'tick'" in x for x in errs(root))


def test_unresolved_link_and_history_link(root):
    edit(root, "docs/grove/capabilities/fly-ship.md", "[[tick]]", "[[tock]]")
    assert any("unresolved link [[tock]]" in x for x in errs(root))
    edit(root, "docs/grove/capabilities/autopilot.md", "## Behavior\n", "## Behavior\n[[D-0000-fixed-orbit]]\n")
    assert any("autopilot.md: live page links into history: [[D-0000-fixed-orbit]]" in x for x in errs(root))


def test_history_link_allowed_from_evidence(root):
    edit(root, "docs/grove/work/W-001-engage-range-readout.md", "## Evidence\n", "## Evidence\nSee [[W-000-v3-release]].\n")
    assert not any("links into history" in x for x in errs(root))


def test_scope_and_applies_to_must_be_capabilities(root):
    edit(root, "docs/grove/work/W-001-engage-range-readout.md", "scope: [autopilot]", "scope: [autopilot, warp]")
    assert any("scope 'warp' is not a capability" in x for x in errs(root))
    edit(root, "docs/grove/decisions/D-0001-adaptive-autopilot.md", "applies_to: [autopilot, fly-ship]", "applies_to: [tick]")
    assert any("applies_to 'tick' is not a capability" in x for x in errs(root))


def test_done_outside_history_is_warning_only(root):
    edit(root, "docs/grove/work/W-001-engage-range-readout.md", "status: active", "status: done")
    e, w = lint.lint(root)
    assert e == []
    assert any("W-001-engage-range-readout.md: done but not closed" in x for x in w)


def test_history_work_must_be_done_or_abandoned(root):
    edit(root, "docs/grove/history/work/W-000-v3-release.md", "status: done", "status: active")
    assert any("history/work/W-000-v3-release.md: history work must be done or abandoned" in x for x in errs(root))


def test_question_resolved_is_error(root):
    edit(root, "docs/grove/questions/target-locks.md", "status: open", "status: resolved")
    assert any("bad status 'resolved'" in x for x in errs(root))


def test_superseded_placement(root):
    edit(root, "docs/grove/decisions/D-0002-no-target-locks.md", "status: rejected", "status: superseded")
    e = errs(root)
    assert any("D-0002-no-target-locks.md: superseded decision must live in history/decisions" in x for x in e)
    assert any("D-0002-no-target-locks.md: superseded without superseded_by" in x for x in e)


def test_size_sections(root):
    edit(root, "docs/grove/work/W-003-encounter-tuning.md", "## Constraints\n", "## Limits\n")
    assert any("W-003-encounter-tuning.md: large work needs a Constraints section" in x for x in errs(root))
    edit(root, "docs/grove/work/W-002-selection-brackets.md", "## Acceptance\n", "## Checks\n")
    assert any("W-002-selection-brackets.md: bounded work needs an Acceptance section" in x for x in errs(root))


def test_active_without_next_is_warning(root):
    edit(root, "docs/grove/work/W-001-engage-range-readout.md", "## Next\nAdd the range field to the HUD state message.\n", "## Next\n")
    assert any("W-001-engage-range-readout.md: active work has no Next line" in x for x in warns(root))


def test_missing_type_specific_required_fields(root):
    # Decision missing applies_to
    edit(root, "docs/grove/decisions/D-0003-single-plane.md", "applies_to: []", "")
    e = errs(root)
    assert any("D-0003-single-plane.md: missing applies_to" in x for x in e)
    # Question missing blocks
    edit(root, "docs/grove/questions/target-locks.md", "blocks: [W-002]", "")
    e = errs(root)
    assert any("target-locks.md: missing blocks" in x for x in e)
    # Work missing started when active
    edit(root, "docs/grove/work/W-001-engage-range-readout.md", "started: 2026-09-12", "")
    e = errs(root)
    assert any("W-001-engage-range-readout.md: missing started" in x for x in e)
    # Work missing kind should emit only "missing kind", not "bad kind None"
    edit(root, "docs/grove/work/W-002-selection-brackets.md", "kind: feature", "")
    e = errs(root)
    assert any("W-002-selection-brackets.md: missing kind" in x for x in e)
    assert not any("bad kind" in x for x in e)


def test_orphan_decision_from_non_work_pages(root):
    # Adding link to D-0003 from a term should not suppress the orphan warning
    edit(root, "docs/grove/terms/tick.md", "## Meaning\n", "## Meaning\n[[D-0003-single-plane]]\n")
    w = warns(root)
    assert any("D-0003-single-plane.md: accepted decision referenced by no capability or work" in x for x in w)


def test_bad_date_format(root):
    edit(root, "docs/grove/capabilities/autopilot.md", "updated: 2026-09-09", "updated: 2026-9-9")
    e = errs(root)
    assert any("bad date" in x and "2026-9-9" in x for x in e)


def test_duplicate_id(root):
    (root.knowledge / "work" / "W-000-again.md").write_text(
        "---\ntype: work\nid: W-000\nstatus: proposed\nupdated: 2026-09-12\n"
        "kind: feature\nsize: small\nscope: []\n---\n## Outcome\nx\n"
    )
    e = errs(root)
    assert any("duplicate id 'W-000'" in x for x in e)


def test_evidence_files_are_not_pages(root):
    ev_dir = root.knowledge / "history" / "evidence"
    ev_dir.mkdir(parents=True)
    (ev_dir / "PLAYTEST-v3.md").write_text("Notes without frontmatter.\n")
    assert errs(root) == []
    (ev_dir / "PLAYTEST-v4.md").write_text("---\ntype: evidence\nfoo: bar\n---\nArbitrary frontmatter.\n")
    assert errs(root) == []
    edit(root, "docs/grove/work/W-001-engage-range-readout.md", "## Evidence\n", "## Evidence\nSee [[PLAYTEST-v3]].\n")
    assert errs(root) == []


def test_evidence_exemption_only_for_work(root):
    # Adding history link to capabilities (not work) should still error even if in Evidence
    edit(root, "docs/grove/capabilities/autopilot.md", "## Behavior\n", "## Behavior\n## Evidence\n[[D-0000-fixed-orbit]]\n")
    e = errs(root)
    assert any("autopilot.md: live page links into history: [[D-0000-fixed-orbit]]" in x for x in e)
