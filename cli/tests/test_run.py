"""W-003: one owner per attempt, durable outcomes, bounded recovery, unchanged waits cost nothing."""
import fcntl
import json
import os
import signal
import subprocess
import sys
import time

from grove import cli, contract, run as runner
from conftest import edit, git_init
from test_contract import work, PLAN

PROLOGUE = ("import json,sys,pathlib; c=json.load(open(sys.argv[1])); d=pathlib.Path(sys.argv[2]); "
            "emit=lambda outcome, **kw: (d/'result.json').write_text(json.dumps({'schema':1,'contract':c['id'],'work':c['order'],'outcome':outcome,"
            "'tested':{'head':c['checkout']['head'],'dirty':False},'evidence':['fake adapter ran'],'findings':[],'next':'Close.',**kw})); ")


def adapter(body):
    return [sys.executable, "-c", PROLOGUE + body]


def setup(root):
    work(root, "W-101")
    git_init(root)
    c = contract.export(root, ["W-101"])
    path = root.repo / "contract.json"
    path.write_text(json.dumps(c))
    return c, path


def ledger(state):
    return json.loads((state / "ledger.json").read_text())


def test_complete_result_carries_contract_identity_and_reconciles(root, monkeypatch):
    c, path = setup(root)
    state = root.repo / "state"
    r = runner.run(root, path, adapter("emit('complete')"), state=state)
    assert r["outcome"] == "complete" and r["launched"] and r["attempt"] == 1
    a = ledger(state)["attempts"][0]
    assert a["pid"] and a["identity"] and a["outcome"] == "complete" and a["driver_pid"] == os.getpid()
    result = json.loads((state / "attempts" / "1" / "result.json").read_text())
    assert result["contract"] == c["id"]
    assert contract.reconcile(root, c, result)["work"] == ["W-101"]
    assert "fake adapter ran" in (root.knowledge / "work" / "W-101-example.md").read_text()
    # Terminal: a later invocation launches nothing.
    r = runner.run(root, path, adapter("emit('complete')"), state=state)
    assert r["outcome"] == "complete" and not r["launched"] and len(ledger(state)["attempts"]) == 1
    monkeypatch.chdir(root.repo)
    assert cli.main(["run", str(path), "--state", str(state), "--", "true"]) == 0


def test_duplicate_driver_is_refused_without_touching_the_ledger(root):
    c, path = setup(root)
    state = root.repo / "state"
    state.mkdir()
    held = open(state / "driver.lock", "w")
    fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
    r = runner.run(root, path, adapter("emit('complete')"), state=state)
    assert r["outcome"] == "owned" and not r["launched"]
    assert not (state / "ledger.json").exists()
    held.close()


def test_live_attempt_stays_owned_and_a_dead_one_is_recovered_with_partial_work_intact(root):
    c, path = setup(root)
    state = root.repo / "state"
    (state / "attempts" / "1").mkdir(parents=True)
    orphan = subprocess.Popen(["sleep", "30"])
    (state / "ledger.json").write_text(json.dumps({"schema": 1, "contract": c["id"], "work": c["order"], "outcome": None, "reason": None, "skipped_waits": 0,
        "attempts": [{"n": 1, "driver_pid": 0, "pid": orphan.pid, "identity": runner.start_identity(orphan.pid), "outcome": None, "reason": None}]}))
    (root.repo / "partial.txt").write_text("half done\n")
    r = runner.run(root, path, adapter("emit('complete')"), state=state)
    assert r["outcome"] == "owned" and str(orphan.pid) in r["reason"]
    assert ledger(state)["attempts"][0]["outcome"] is None
    orphan.kill()
    orphan.wait()
    r = runner.run(root, path, adapter("emit('complete')"), state=state)
    assert r["outcome"] == "complete" and r["attempt"] == 2
    first = ledger(state)["attempts"][0]
    assert first["outcome"] == "interrupted" and "partial.txt" in first["checkout"]["dirty"]
    assert (root.repo / "partial.txt").read_text() == "half done\n"


def test_retry_exhaustion_and_timeout_are_durable(root):
    c, path = setup(root)
    state = root.repo / "state"
    failing = [sys.executable, "-c", "raise SystemExit(1)"]
    assert runner.run(root, path, failing, state=state, max_attempts=2)["outcome"] == "failed"
    r = runner.run(root, path, failing, state=state, max_attempts=2)
    assert r["outcome"] == "exhausted" and r["launched"]
    l = ledger(state)
    assert l["outcome"] == "exhausted" and len(l["attempts"]) == 2 and "without result.json" in l["attempts"][1]["reason"]
    r = runner.run(root, path, adapter("emit('complete')"), state=state, max_attempts=2)
    assert r["outcome"] == "exhausted" and not r["launched"] and len(ledger(state)["attempts"]) == 2
    slow = root.repo / "slow"
    r = runner.run(root, path, [sys.executable, "-c", "import time; time.sleep(30)"], state=slow, timeout=0.3)
    assert r["outcome"] == "failed" and "timed out" in r["reason"]
    assert not runner.alive(ledger(slow)["attempts"][0]["pid"], ledger(slow)["attempts"][0]["identity"])


def test_cancellation_kills_the_child_and_records_a_durable_outcome(root):
    c, path = setup(root)
    state = root.repo / "state"
    driver = subprocess.Popen([sys.executable, "-m", "grove.cli", "run", str(path), "--state", str(state), "--",
                               sys.executable, "-c", "import time; time.sleep(30)"], cwd=root.repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for _ in range(100):
        if (state / "ledger.json").exists() and ledger(state)["attempts"] and ledger(state)["attempts"][0]["pid"]:
            break
        time.sleep(0.05)
    a = ledger(state)["attempts"][0]
    driver.send_signal(signal.SIGTERM)
    out, _ = driver.communicate(timeout=10)
    assert driver.returncode == 6, out
    l = ledger(state)
    assert l["outcome"] == "cancelled" and l["attempts"][0]["outcome"] == "cancelled" and "SIGTERM" in l["attempts"][0]["reason"]
    assert not runner.alive(a["pid"], a["identity"])


def test_unchanged_wait_spends_no_launch_and_a_changed_input_wakes(root, monkeypatch, capsys):
    c, path = setup(root)
    state = root.repo / "state"
    counter = root.repo / "launches.txt"
    waiting = adapter("open(%r,'a').write('x'); emit('waiting', wait={'on': 'human playtest', 'sources': ['docs/grove/questions/target-locks.md']})" % str(counter))
    r = runner.run(root, path, waiting, state=state)
    assert r["outcome"] == "waiting" and r["launched"] and counter.read_text() == "x"
    monkeypatch.chdir(root.repo)
    assert cli.main(["run", str(path), "--state", str(state), "--", *waiting]) == 3
    assert "unchanged" in capsys.readouterr().out and counter.read_text() == "x"
    assert ledger(state)["skipped_waits"] == 1 and len(ledger(state)["attempts"]) == 1
    edit(root, "docs/grove/questions/target-locks.md", "status: open", "status: parked")
    r = runner.run(root, path, waiting, state=state)
    assert r["launched"] and counter.read_text() == "xx" and len(ledger(state)["attempts"]) == 2


def test_child_runs_only_after_its_identity_is_durable(root):
    """The launch gate: the adapter sees its own pid and start identity already in the ledger."""
    c, path = setup(root)
    state = root.repo / "state"
    checking = adapter("import os; l=json.load(open(%r)); a=l['attempts'][-1]; emit('complete', evidence=['pid %%s identity %%s' %% (a['pid']==os.getpid(), bool(a['identity']))])" % str(state / "ledger.json"))
    r = runner.run(root, path, checking, state=state)
    assert r["outcome"] == "complete"
    assert json.loads((state / "attempts" / "1" / "result.json").read_text())["evidence"] == ["pid True identity True"]


def test_owned_path_reports_exit_4_through_the_cli(root, monkeypatch):
    c, path = setup(root)
    state = root.repo / "state"
    state.mkdir()
    held = open(state / "driver.lock", "w")
    fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
    monkeypatch.chdir(root.repo)
    assert cli.main(["run", str(path), "--state", str(state), "--", "true"]) == 4
    held.close()


def test_waiting_attempts_do_not_spend_the_attempt_budget(root):
    c, path = setup(root)
    state = root.repo / "state"
    waiting = adapter("emit('waiting', wait={'on': 'human', 'sources': ['docs/grove/questions/target-locks.md']})")
    assert runner.run(root, path, waiting, state=state, max_attempts=1)["outcome"] == "waiting"
    edit(root, "docs/grove/questions/target-locks.md", "status: open", "status: parked")
    r = runner.run(root, path, adapter("emit('complete')"), state=state, max_attempts=1)
    assert r["outcome"] == "complete" and r["launched"]


def test_result_claiming_an_untested_revision_fails_the_attempt(root):
    c, path = setup(root)
    state = root.repo / "state"
    r = runner.run(root, path, adapter("emit('complete', tested={'head': '0'*40, 'dirty': False})"), state=state)
    assert r["outcome"] == "failed" and "000000000000" in r["reason"] and c["checkout"]["head"][:12] in r["reason"]
    # An unrelated real commit is refused too: ancestry, not mere existence.
    unrelated = adapter("import subprocess; r=c['checkout']['repo']; g=lambda *a: subprocess.run(['git','-C',r,*a],check=True,capture_output=True,text=True).stdout.strip(); "
                        "h=g('-c','user.name=t','-c','user.email=t@x','commit-tree',g('write-tree'),'-m','stray'); emit('complete', tested={'head': h, 'dirty': False})")
    r = runner.run(root, path, unrelated, state=root.repo / "state2")
    assert r["outcome"] == "failed" and "does not descend" in r["reason"]


def test_wait_sources_must_stay_inside_the_repository(root):
    import pytest
    from grove.pages import GroveError
    c, _ = setup(root)
    for bad in ("/etc/hosts", "../secret", "docs/../../x"):
        with pytest.raises(GroveError, match="repo-relative"):
            contract.validate_result(c, {"schema": 1, "contract": c["id"], "work": c["order"], "outcome": "waiting", "tested": {"head": "abc"},
                                         "evidence": [], "findings": [], "next": "Wait.", "wait": {"on": "human", "sources": [bad]}})


def test_result_tested_on_a_branch_descending_from_the_exported_head_is_accepted(root):
    """W-004: the adapter commits on a worktree branch and leaves the launched checkout alone."""
    c, path = setup(root)
    state = root.repo / "state"
    branching = adapter("import subprocess; r=c['checkout']['repo']; g=lambda *a: subprocess.run(['git','-C',r,*a],check=True,capture_output=True,text=True).stdout.strip(); "
                        "g('worktree','add','-q','wt','-b','W-101'); open(r+'/wt/new.txt','w').write('x'); "
                        "g('-C','wt','add','-A'); g('-C','wt','-c','user.name=t','-c','user.email=t@x','commit','-q','-m','work'); "
                        "emit('complete', tested={'head': g('-C','wt','rev-parse','HEAD'), 'dirty': False})")
    r = runner.run(root, path, branching, state=state)
    assert r["outcome"] == "complete", r["reason"]
    assert contract.checkout(root.repo)["head"] == c["checkout"]["head"]   # launched checkout untouched
