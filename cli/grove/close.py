"""Close gate: refuse until knowledge is reconciled, then move the work unit to history."""
from .lint import lint
from .pages import GroveError, first_line, section
from .status import status
from .work import WorkIndex
import re


def close(root, work_id):
    work = root.get(work_id)
    if not work or work.type != "work":
        raise GroveError(f"no work unit {work_id}")
    if work.in_history:
        raise GroveError(f"{work.id} is already closed")
    errors, _ = lint(root)
    if errors:
        raise GroveError(f"lint has {len(errors)} error(s); fix them first:\n" + "\n".join(errors))
    if work.status != "done":
        raise GroveError(f"{work.id} status is {work.status}, not done")
    index = WorkIndex(root)
    blockers = index.blockers(work) + index.relationship_gaps(work)
    if blockers:
        raise GroveError(f"{work.id} cannot close: " + "; ".join(blockers))
    if work.fm.get("size") == "spike":
        if not section(work.body, "Disposition"):
            raise GroveError(f"{work.id} Disposition is empty")
    else:
        acceptance = section(work.body, "Acceptance")
        if not re.search(r"\[[xX]\]", acceptance) or re.search(r"\[ \]", acceptance):
            raise GroveError(f"{work.id} Acceptance must be present and checked")
    evidence = section(work.body, "Evidence")
    if not evidence:
        raise GroveError(f"{work.id} Evidence section is empty")
    started = str(work.fm.get("started") or work.fm.get("updated"))
    unchanged = [s for s in (work.fm.get("unchanged") or []) if isinstance(s, str)]
    updated = []
    for slug in work.fm.get("scope") or []:
        if slug in unchanged:
            continue
        cap = root.get(slug)
        if cap is None:
            raise GroveError(f"scope {slug!r} is not a capability")
        when = str(cap.fm.get("updated"))
        if when < started:
            raise GroveError(f"{slug} updated {when} is before {work.id} started {started}; reconcile it or list it under unchanged")
        updated.append(slug)
    dest_dir = root.knowledge / "history" / "work"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / work.path.name
    work.path.rename(dest)
    recommendation = status(root)["recommendation"]
    return {
        "id": work.id,
        "outcome": first_line(section(work.body, "Outcome")),
        "updated": updated,
        "unchanged": unchanged,
        "evidence": evidence,
        "moved_to": root.rel(dest),
        "next": recommendation,
    }


def render_receipt(r):
    out = [f"closed {r['id']}: {r['outcome']}", f"moved to {r['moved_to']}",
           f"capabilities updated: {', '.join(r['updated']) or 'none'}",
           f"capabilities unchanged: {', '.join(r['unchanged']) or 'none'}", "evidence:", r["evidence"], ""]
    n = r["next"]
    out.append(f"next: {n['id']} ({n['size']} {n['kind']}): {n['outcome']}" if n else "next: nothing proposed; run grove:shape")
    return "\n".join(out) + "\n"
