"""Local executor: at most one attempt per invocation against an exported contract. One driver owns
the run (flock), the attempt is recorded before its process exists, pid plus start identity decide
ownership on resume, and every outcome is durable in ledger.json. The adapter is any command that
receives the contract path and an attempt directory and writes result.json there. Stdlib only.
"""
import fcntl
import json
import os
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from .contract import checkout, digest, load_contract, validate_result
from .pages import GroveError

SCHEMA = 1
TERMINAL = ("complete", "cancelled", "exhausted")
# The child may not start until its pid and identity are durable: EOF (driver died first) exits without running.
LAUNCHER = 'import os,sys; token=sys.stdin.buffer.read(1); sys.exit(125) if token != b"1" else os.execvp(sys.argv[1], sys.argv[1:])'
EXIT = {"complete": 0, "partial": 1, "blocked": 1, "failed": 1, "interrupted": 1, "waiting": 3, "owned": 4, "exhausted": 5, "cancelled": 6}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def start_identity(pid):
    """Process start time as `ps` prints it, or None when gone; pid reuse never re-establishes ownership."""
    try:
        out = subprocess.run(["ps", "-o", "stat=", "-o", "lstart=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    except OSError:
        return None
    if not out or out.split()[0].startswith("Z"):
        return None
    parts = out.split(None, 1)
    return parts[1] if len(parts) > 1 else None


def alive(pid, identity=None):
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    return identity is None or start_identity(pid) == identity


def write_atomic(path, value):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(value, indent=1, sort_keys=True) + "\n")
    os.replace(tmp, path)


def wait_fingerprint(repo, c, result):
    sources = (result.get("wait") or {}).get("sources") or list(c["sources"])
    parts = [f"{rel}:{digest((repo / rel).read_bytes()) if (repo / rel).is_file() else 'missing'}" for rel in sources]
    return digest("\n".join(parts).encode())


def kill(proc):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait()


def run(root, contract_path, adapter, state=None, max_attempts=3, timeout=None):
    if not adapter:
        raise GroveError("run needs an adapter command after --")
    c = load_contract(contract_path)
    state = Path(state) if state else root.repo / ".grove" / "runs" / c["id"][:12]
    state.mkdir(parents=True, exist_ok=True)
    ledger_path = state / "ledger.json"
    lock = open(state / "driver.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        lock.close()
        return {"outcome": "owned", "launched": False, "attempt": None, "reason": f"another driver holds {state / 'driver.lock'}", "ledger": str(ledger_path)}
    try:
        if ledger_path.exists():
            ledger = json.loads(ledger_path.read_text())
            if ledger.get("contract") != c["id"]:
                raise GroveError(f"{ledger_path} belongs to contract {str(ledger.get('contract'))[:12]}, not {c['id'][:12]}; use another --state")
        else:
            ledger = {"schema": SCHEMA, "contract": c["id"], "work": c["order"], "attempts": [], "outcome": None, "reason": None, "skipped_waits": 0}
        attempts = ledger["attempts"]
        receipt = lambda **kw: {"launched": False, "ledger": str(ledger_path), "attempt": len(attempts), **kw}
        # Resume: a recorded attempt without an outcome is owned while its process lives; otherwise it was interrupted.
        for a in attempts:
            if a["outcome"] is None:
                if alive(a.get("pid"), a.get("identity")):
                    return receipt(outcome="owned", reason=f"attempt {a['n']} is still owned by live process {a['pid']}")
                a.update(outcome="interrupted", reason="process exited without a result", finished=now(), checkout=checkout(root.repo))
                write_atomic(ledger_path, ledger)
        if ledger["outcome"] in TERMINAL:
            return receipt(outcome=ledger["outcome"], reason=ledger["reason"])
        last = attempts[-1] if attempts else None
        if last and last["outcome"] == "waiting":
            result = json.loads((state / "attempts" / str(last["n"]) / "result.json").read_text())
            if wait_fingerprint(root.repo, c, result) == last["wait_fingerprint"]:
                ledger["skipped_waits"] += 1
                write_atomic(ledger_path, ledger)
                return receipt(outcome="waiting", reason=f"unchanged wait: {last['wait_on']}")
        spent = sum(a["outcome"] != "waiting" for a in attempts)   # a wait is not a failed attempt
        if spent >= max_attempts:
            ledger.update(outcome="exhausted", reason=f"{spent} attempts without completion")
            write_atomic(ledger_path, ledger)
            return receipt(outcome="exhausted", reason=ledger["reason"])
        # ponytail: every non-waiting attempt counts toward max_attempts, interrupted ones included; split
        # an infrastructure budget out if a real harness shows interruptions dominate. write_atomic does
        # not fsync: the ledger survives process death, not power loss.
        n = len(attempts) + 1
        attempt_dir = state / "attempts" / str(n)
        attempt_dir.mkdir(parents=True, exist_ok=True)
        a = {"n": n, "started": now(), "driver_pid": os.getpid(), "pid": None, "identity": None, "outcome": None, "reason": None, "dir": str(attempt_dir)}
        attempts.append(a)
        write_atomic(ledger_path, ledger)   # the record exists before any process does
        with open(attempt_dir / "log.txt", "ab") as log:
            proc = subprocess.Popen([sys.executable, "-c", LAUNCHER, *adapter, str(contract_path), str(attempt_dir)], cwd=root.repo,
                                    stdin=subprocess.PIPE, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        a.update(pid=proc.pid, identity=start_identity(proc.pid))
        if not a["identity"]:
            kill(proc)
            a.update(outcome="failed", reason="could not establish process identity; nothing ran", finished=now(), checkout=checkout(root.repo))
            write_atomic(ledger_path, ledger)
            return receipt(outcome="failed", launched=True, attempt=n, reason=a["reason"])
        write_atomic(ledger_path, ledger)
        proc.stdin.write(b"1")
        proc.stdin.close()
        received = []

        def on_signal(signum, frame):
            received.append(signal.Signals(signum).name)
            raise KeyboardInterrupt

        previous = {s: signal.signal(s, on_signal) for s in (signal.SIGTERM, signal.SIGINT)}
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            kill(proc)
            a.update(outcome="failed", reason=f"timed out after {timeout}s")
        except KeyboardInterrupt:
            kill(proc)
            a.update(outcome="cancelled", reason=f"driver received {received[0] if received else 'interrupt'}")
            ledger.update(outcome="cancelled", reason=a["reason"])
        finally:
            for s, handler in previous.items():
                signal.signal(s, handler)
        result_path = attempt_dir / "result.json"
        if a["outcome"] is None:
            a["exit_code"] = proc.returncode
            if not result_path.exists():
                a.update(outcome="failed", reason=f"adapter exited {proc.returncode} without result.json")
            else:
                try:
                    result = validate_result(c, json.loads(result_path.read_text()))
                except (ValueError, GroveError) as exc:
                    a.update(outcome="failed", reason=f"invalid result: {exc}")
                else:
                    head = checkout(root.repo)["head"]
                    if result["tested"]["head"] != head:
                        a.update(outcome="failed", reason=f"result claims tested revision {result['tested']['head'][:12]} but the checkout is {head[:12]}")
                if a["outcome"] is None:
                    a.update(outcome=result["outcome"], reason=result["next"])
                    if result["outcome"] == "waiting":
                        a.update(wait_on=result["wait"]["on"], wait_fingerprint=wait_fingerprint(root.repo, c, result))
                    elif result["outcome"] == "complete":
                        ledger.update(outcome="complete", reason=result["next"])
        a.update(finished=now(), checkout=checkout(root.repo))
        spent = sum(x["outcome"] != "waiting" for x in attempts)
        if ledger["outcome"] is None and a["outcome"] != "waiting" and spent >= max_attempts:
            ledger.update(outcome="exhausted", reason=f"{spent} attempts without completion")
        write_atomic(ledger_path, ledger)
        outcome = ledger["outcome"] if ledger["outcome"] == "exhausted" else a["outcome"]
        return receipt(outcome=outcome, launched=True, attempt=n, reason=a["reason"], result=str(result_path) if result_path.exists() else None)
    finally:
        lock.close()


def render_run(r):
    lines = [f"attempt {r['attempt'] or '-'}: {r['outcome']}" + (" (launched)" if r["launched"] else " (nothing launched)"), f"reason: {r['reason']}"]
    if r.get("result"):
        lines.append(f"result: {r['result']} (grove reconcile it against the contract)")
    return "\n".join(lines + [f"ledger: {r['ledger']}", ""])
