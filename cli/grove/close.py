"""Close gate: refuse until knowledge is reconciled, then move the work unit to history."""
import json
from .contract import git
from .lint import lint
from .pages import GroveError, first_line, section
from .status import status
from .work import WorkIndex
import re

DECL_DIR = "docs/grove/deliveries"


def closure_errors(root, work):
    """Every closure invariant, in the order `close()` used to check them. Never mutates."""
    errors = []
    lint_errors, _ = lint(root)
    if lint_errors:
        errors.append(f"lint has {len(lint_errors)} error(s); fix them first:\n" + "\n".join(lint_errors))
    if work.status != "done":
        errors.append(f"{work.id} status is {work.status}, not done")
    index = WorkIndex(root)
    blockers = index.blockers(work) + index.relationship_gaps(work)
    if blockers:
        errors.append(f"{work.id} cannot close: " + "; ".join(blockers))
    if work.fm.get("size") == "spike":
        if not section(work.body, "Disposition"):
            errors.append(f"{work.id} Disposition is empty")
    else:
        acceptance = section(work.body, "Acceptance")
        if not re.search(r"\[[xX]\]", acceptance) or re.search(r"\[ \]", acceptance):
            errors.append(f"{work.id} Acceptance must be present and checked")
    if not section(work.body, "Evidence"):
        errors.append(f"{work.id} Evidence section is empty")
    started = str(work.fm.get("started") or work.fm.get("updated"))
    unchanged = [s for s in (work.fm.get("unchanged") or []) if isinstance(s, str)]
    for slug in work.fm.get("scope") or []:
        if slug in unchanged:
            continue
        cap = root.get(slug)
        if cap is None:
            errors.append(f"scope {slug!r} is not a capability")
            continue
        when = str(cap.fm.get("updated"))
        if when < started:
            errors.append(f"{slug} updated {when} is before {work.id} started {started}; reconcile it or list it under unchanged")
    return errors


def current_branch(repo):
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    if branch == "HEAD":
        raise GroveError("cannot record delivery on a detached HEAD; checkout a branch first")
    return branch


def prepare_delivery(root, work_id):
    """Resolve the branch and merge work_id into its declaration, without writing anything.
    Everything that can fail (branch resolution, malformed existing JSON) happens here, so a
    caller can do this before mutating any other file and stay unmutated on failure."""
    branch = current_branch(root.repo)
    path = root.repo / DECL_DIR / f"{branch}.json"
    try:
        data = json.loads(path.read_text()) if path.exists() else {}
    except ValueError as exc:
        raise GroveError(f"delivery declaration {root.rel(path)} is not valid JSON: {exc}")
    if not isinstance(data, dict):
        data = {}
    data["schema"] = 1
    delivers = [w for w in data.get("delivers", []) if isinstance(w, str)] if isinstance(data.get("delivers"), list) else []
    if work_id not in delivers:
        delivers.append(work_id)
    data["delivers"] = delivers
    data["retains"] = data.get("retains") if isinstance(data.get("retains"), list) else []
    return path, data


def write_delivery(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def record_delivery(root, work_id):
    """Append work_id to the committed declaration for the current branch; idempotent."""
    path, data = prepare_delivery(root, work_id)
    write_delivery(path, data)
    return root.rel(path)


def close(root, work_id):
    work = root.get(work_id)
    if not work or work.type != "work":
        raise GroveError(f"no work unit {work_id}")
    if work.in_history:
        raise GroveError(f"{work.id} is already closed")
    errors = closure_errors(root, work)
    if errors:
        raise GroveError(errors[0])
    decl_path, decl_data = prepare_delivery(root, work.id)  # resolve/validate before anything moves
    unchanged = [s for s in (work.fm.get("unchanged") or []) if isinstance(s, str)]
    updated = [s for s in (work.fm.get("scope") or []) if s not in unchanged]
    evidence = section(work.body, "Evidence")
    dest_dir = root.knowledge / "history" / "work"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / work.path.name
    work.path.rename(dest)
    write_delivery(decl_path, decl_data)
    declaration = root.rel(decl_path)
    recommendation = status(root)["recommendation"]
    return {
        "id": work.id,
        "outcome": first_line(section(work.body, "Outcome")),
        "updated": updated,
        "unchanged": unchanged,
        "evidence": evidence,
        "moved_to": root.rel(dest),
        "declaration": declaration,
        "next": recommendation,
    }


def render_receipt(r):
    out = [f"closed {r['id']}: {r['outcome']}", f"moved to {r['moved_to']}",
           f"capabilities updated: {', '.join(r['updated']) or 'none'}",
           f"capabilities unchanged: {', '.join(r['unchanged']) or 'none'}", "evidence:", r["evidence"], "",
           f"declaration: {r['declaration']}"]
    n = r["next"]
    out.append(f"next: {n['id']} ({n['size']} {n['kind']}): {n['outcome']}" if n else "next: nothing proposed; run grove:shape")
    return "\n".join(out) + "\n"
