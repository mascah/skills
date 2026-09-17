"""Versioned execution contract: export a prepared selection, validate an executor's result, and
reconcile it into the work pages only while every exported input is unchanged. Stdlib only.
Readiness is exported as fact; the contract grants no permission."""
import hashlib
import json
import re
import subprocess
from datetime import date
from pathlib import Path

from .pages import GroveError, first_line, section
from .work import WorkIndex, batch, plan_path, refs

SCHEMA = 1
OUTCOMES = ("complete", "partial", "waiting", "blocked", "failed")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if p.returncode:
        raise GroveError(f"git {' '.join(args)}: {p.stderr.strip() or 'failed'}")
    return p.stdout


def checkout(repo):
    """Exact checkout identity: HEAD plus every modified or untracked path."""
    status = git(repo, "status", "--porcelain", "--untracked-files=all")
    return {"repo": str(repo), "head": git(repo, "rev-parse", "HEAD").strip(),
            "dirty": sorted(line[3:] for line in status.splitlines() if line)}


def acceptance(wid, body):
    items = []
    for line in section(body, "Acceptance").splitlines():
        m = re.match(r"^- \[([ xX])\] (.*)$", line.strip())
        if m:
            text = m.group(2).strip()
            items.append({"id": f"{wid}:{len(items) + 1}", "text": text, "revision": digest(text.encode()), "checked": m.group(1) != " "})
    return items


def export(root, ids):
    d = batch(root, ids)
    problems = d["blockers"] + d["preparation"]
    if problems:
        raise GroveError("selection is not prepared for export:\n" + "\n".join(problems))
    index = WorkIndex(root)
    sources, work, scope, parents = {}, [], [], {}

    def source(path):
        rel = root.rel(path)
        sources[rel] = digest(Path(path).read_bytes())
        return rel

    for wid in d["order"]:
        p = index.work[wid]
        source(p.path)
        plan = source(plan_path(root, p)) if p.fm.get("plan") else None
        work.append({"id": wid, "page": p.rel, "outcome": first_line(section(p.body, "Outcome")),
                     "constraints": section(p.body, "Constraints"), "design": section(p.body, "Design"),
                     "next": first_line(section(p.body, "Next")), "scope": refs(p, "scope"), "depends_on": refs(p, "depends_on"),
                     "plan": plan, "acceptance": acceptance(wid, p.body)})
        scope += refs(p, "scope")
        for parent in index.ancestors(wid):
            parents[parent.id] = {"id": parent.id, "constraints": section(parent.body, "Constraints"), "acceptance": section(parent.body, "Acceptance")}
            source(parent.path)
    scope = list(dict.fromkeys(scope))
    brief = index.brief
    if brief:
        source(brief.path)
    for slug in scope:
        cap = root.get(slug)
        if cap is not None and cap.type == "capability" and not cap.in_history:
            source(cap.path)
    decisions = sorted((p for p in root.pages() if p.type == "decision" and p.status == "accepted" and set(refs(p, "applies_to")) & set(scope)),
                       key=lambda p: p.basename)
    for dp in decisions:
        source(dp.path)
    body = {"schema": SCHEMA, "created": date.today().isoformat(), "project": root.project, "checkout": checkout(root.repo),
            "order": d["order"], "work": work,
            "bounds": {"brief": section(brief.body, "Constraints") if brief else "",
                       "decisions": [{"id": dp.id, "decision": first_line(section(dp.body, "Decision"))} for dp in decisions],
                       "parents": list(parents.values())},
            "sources": dict(sorted(sources.items()))}
    return {"id": digest(canonical(body)), **body}


def load_contract(path):
    try:
        c = json.loads(Path(path).read_text())
    except (OSError, ValueError) as exc:
        raise GroveError(f"cannot read contract {path}: {exc}")
    if not isinstance(c, dict) or c.get("schema") != SCHEMA:
        raise GroveError(f"{path}: contract schema must be {SCHEMA}")
    if c.get("id") != digest(canonical({k: v for k, v in c.items() if k != "id"})):
        raise GroveError(f"{path}: contract content does not match its id; the file was edited after export")
    return c


def stale(root, c):
    """Exported inputs whose current bytes differ from the contract, or which are missing."""
    changed = []
    for rel, expected in c["sources"].items():
        p = root.repo / rel
        if not p.is_file() or digest(p.read_bytes()) != expected:
            changed.append(rel)
    return changed


def validate_result(c, r):
    if not isinstance(r, dict) or r.get("schema") != SCHEMA:
        raise GroveError(f"result schema must be {SCHEMA}")
    if r.get("contract") != c["id"]:
        raise GroveError(f"result names contract {str(r.get('contract'))[:12]}, not {c['id'][:12]}")
    if r.get("outcome") not in OUTCOMES:
        raise GroveError("result outcome must be one of " + ", ".join(OUTCOMES))
    work = r.get("work")
    unknown = [w for w in work if w not in c["order"]] if isinstance(work, list) else None
    if not work or unknown is None or unknown:
        raise GroveError("result work must name work in the contract; unknown: " + ", ".join(map(str, unknown or [])))
    tested = r.get("tested")
    if not isinstance(tested, dict) or not isinstance(tested.get("head"), str) or not tested["head"]:
        raise GroveError("result tested.head must identify the tested revision")
    for key in ("evidence", "findings"):
        if not isinstance(r.get(key), list) or not all(isinstance(x, str) for x in r[key]):
            raise GroveError(f"result {key} must be a list of strings")
    if not isinstance(r.get("next"), str) or not r["next"].strip():
        raise GroveError("result next must be a concrete next action")
    wait = r.get("wait")
    if r["outcome"] == "waiting" and not (isinstance(wait, dict) and isinstance(wait.get("on"), str) and wait["on"].strip()):
        raise GroveError("a waiting result must say what it waits on in wait.on")
    sources = wait.get("sources", []) if isinstance(wait, dict) else []
    if wait is not None and not (isinstance(wait, dict) and isinstance(sources, list) and all(
            isinstance(s, str) and s and not Path(s).is_absolute() and ".." not in Path(s).parts for s in sources)):
        raise GroveError("result wait.sources must be repo-relative paths inside the repository")
    return r


def set_section(text, heading, content):
    new = f"## {heading}\n{content.strip()}\n\n"
    pat = re.compile(rf"^## {re.escape(heading)}\s*\n.*?(?=^## |\Z)", re.S | re.M)
    if pat.search(text):
        return pat.sub(lambda m: new, text, count=1)
    return text.rstrip("\n") + "\n\n" + new


def reconcile(root, c, r):
    """Append the result as evidence and replace Next on each named work page. Never checks acceptance."""
    validate_result(c, r)
    changed = stale(root, c)
    if changed:
        raise GroveError("contract inputs changed since export; re-export before accepting this result:\n" + "\n".join(changed))
    today = date.today().isoformat()
    dirty = " (dirty)" if r["tested"].get("dirty") else ""
    block = [f"Run {c['id'][:12]} on {r['tested']['head'][:12]}{dirty}, {today}: {r['outcome']}"]
    block += [f"- {e}" for e in r["evidence"]] + [f"- unresolved: {f}" for f in r["findings"]]
    if r.get("wait"):
        block.append(f"- waiting on: {r['wait']['on']}")
    pages = []
    for wid in r["work"]:
        p = root.get(wid)
        if p is None or p.type != "work" or p.in_history:
            raise GroveError(f"{wid} is not live work")
        text = p.text
        previous = section(p.body, "Evidence")
        text = set_section(text, "Evidence", (previous + "\n\n" if previous else "") + "\n".join(block))
        text = set_section(text, "Next", r["next"])
        text = re.sub(r"^updated: .*$", f"updated: {today}", text, count=1, flags=re.M)
        p.path.write_text(text.rstrip("\n") + "\n")
        pages.append(p.rel)
    return {"contract": c["id"], "work": r["work"], "outcome": r["outcome"], "tested": r["tested"]["head"], "next": r["next"], "pages": pages}


def render_receipt(rc):
    return "\n".join([f"reconciled {', '.join(rc['work'])}: {rc['outcome']} at {rc['tested'][:12]} (contract {rc['contract'][:12]})",
                      *(f"updated {p}" for p in rc["pages"]), f"next: {rc['next']}", ""])
