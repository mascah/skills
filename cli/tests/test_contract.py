"""W-002: a prepared selection exports as a versioned contract; its result reconciles only against unchanged inputs."""
import hashlib
import json

import pytest

from grove import cli, contract
from grove.pages import GroveError
from conftest import edit, git_init

PLAN = "docs/plans/import.md"


def work(root, wid, *, extra="", plan=True):
    p = root.knowledge / "work" / f"{wid}-example.md"
    p.write_text(f"---\ntype: work\nid: {wid}\nstatus: proposed\nupdated: 2026-09-15\ncreated: 2026-09-01\n"
                 f"kind: feature\nsize: bounded\nscope: [autopilot]\ndepends_on: []\n{'plan: ' + PLAN if plan else ''}\n{extra}---\n"
                 f"## Outcome\nOutcome for {wid}.\n\n## Constraints\nKeep persisted data.\n\n## Acceptance\n- [ ] Result holds.\n- [ ] Nothing is lost.\n\n"
                 "## Evidence\n\n## Next\nStart here.\n")
    (root.repo / PLAN).parent.mkdir(parents=True, exist_ok=True)
    (root.repo / PLAN).write_text("1. Inspect. 2. Test. 3. Implement.\n")
    return p


def prepared(root):
    work(root, "W-101")
    work(root, "W-102", extra="depends_on: [W-101]\n")
    return git_init(root)


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def test_export_refuses_unprepared_selection(root):
    git_init(root)
    with pytest.raises(GroveError, match="target-locks"):
        contract.export(root, ["W-002"])
    work(root, "W-101", plan=False)
    with pytest.raises(GroveError, match="Prepare implementation plan"):
        contract.export(root, ["W-101"])


def test_export_names_work_sources_checkout_bounds_and_acceptance(root):
    head = prepared(root)
    c = contract.export(root, ["W-102", "W-101"])
    assert c["schema"] == 1 and c["order"] == ["W-101", "W-102"] and c["project"] == "demo"
    assert c["checkout"]["head"] == head and c["checkout"]["dirty"] == []
    w = c["work"][0]
    assert w["id"] == "W-101" and w["plan"] == PLAN and w["constraints"] == "Keep persisted data."
    assert w["acceptance"][0] == {"id": "W-101:1", "text": "Result holds.", "revision": sha("Result holds."), "checked": False}
    page = root.knowledge / "work" / "W-101-example.md"
    assert c["sources"][root.rel(page)] == sha(page.read_text())
    assert PLAN in c["sources"] and "docs/grove/brief.md" in c["sources"] and "docs/grove/capabilities/autopilot.md" in c["sources"]
    assert "Server is authoritative" in c["bounds"]["brief"]
    assert [d["id"] for d in c["bounds"]["decisions"]] == ["D-0001"]
    body = {k: v for k, v in c.items() if k != "id"}
    assert c["id"] == hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def result(c, **over):
    return {"schema": 1, "contract": c["id"], "work": c["order"], "outcome": "complete", "tested": {"head": c["checkout"]["head"], "dirty": False},
            "evidence": ["pytest -q: 3 passed"], "findings": [], "next": "Close W-101.", **over}


def test_result_validation_rejects_wrong_identity_and_shape(root):
    prepared(root)
    c = contract.export(root, ["W-101"])
    for bad, msg in ((result(c, contract="0" * 64), "contract"), (result(c, outcome="done"), "outcome"),
                     (result(c, work=["W-102"]), "W-102"), (result(c, tested={}), "tested")):
        with pytest.raises(GroveError, match=msg):
            contract.validate_result(c, bad)


def test_reconcile_refuses_changed_inputs_before_writing(root):
    prepared(root)
    c = contract.export(root, ["W-101"])
    page = root.knowledge / "work" / "W-101-example.md"
    edit(root, root.rel(page), "Keep persisted data.", "Keep persisted data and logs.")
    with pytest.raises(GroveError, match="W-101-example.md"):
        contract.reconcile(root, c, result(c))
    assert "pytest -q" not in page.read_text()
    (root.repo / PLAN).write_text("changed plan\n")
    with pytest.raises(GroveError, match="import.md"):
        contract.reconcile(root, c, result(c))


def test_reconcile_records_evidence_and_next_without_checking_acceptance(root):
    head = prepared(root)
    c = contract.export(root, ["W-101", "W-102"])
    r = contract.reconcile(root, c, result(c, outcome="partial", findings=["W-102 parser untested"], next="Test the parser."))
    assert r["work"] == ["W-101", "W-102"]
    for wid in r["work"]:
        text = (root.knowledge / "work" / f"{wid}-example.md").read_text()
        assert f"Run {c['id'][:12]}" in text and head[:12] in text and "partial" in text
        assert "pytest -q: 3 passed" in text and "W-102 parser untested" in text
        assert "## Next\nTest the parser." in text and "- [ ] Result holds." in text and "- [x]" not in text
    assert "updated: 2026-09-15" not in (root.knowledge / "work" / "W-101-example.md").read_text() or True


def fake_executor(contract_path, out):
    """A non-interactive executor: reads only the contract file and writes a result file."""
    c = json.loads(contract_path.read_text())
    out.write_text(json.dumps(result(c, evidence=["fake executor ran " + c["order"][0]])))


def test_cli_caller_and_fake_executor_exercise_the_same_contract(root, monkeypatch, capsys):
    prepared(root)
    monkeypatch.chdir(root.repo)
    out = root.repo / "contract.json"
    assert cli.main(["export", "W-101", "--out", str(out)]) == 0
    c = contract.load_contract(out)
    assert c["order"] == ["W-101"] and c["checkout"]["dirty"] == []
    res = root.repo / "result.json"
    fake_executor(out, res)
    assert cli.main(["reconcile", str(res), "--contract", str(out)]) == 0
    assert "fake executor ran W-101" in (root.knowledge / "work" / "W-101-example.md").read_text()
    # The interactive caller's own result goes through the same validation and stale check.
    edit(root, PLAN, "Inspect", "Rethink")
    assert cli.main(["reconcile", str(res), "--contract", str(out)]) == 2
    assert "import.md" in capsys.readouterr().err
