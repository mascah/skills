"""Compact work map using the same selection rules as closure."""
from .lint import lint
from .pages import first_line, section
from .work import WorkIndex, closed, outcome, refs


def status(root):
    index = WorkIndex(root)
    brief = index.brief
    work = index.ordered()
    questions = sorted((p for p in index.questions if p.status == "open"),
                       key=lambda p: (not refs(p, "blocks"), p.basename))
    history = sorted((p for p in index.work.values() if p.in_history),
                     key=lambda p: (p.fm.get("updated") or "", p.basename), reverse=True)[:3]
    errors, warnings = lint(root)
    eligible = [w for w in work if w["status"] in ("active", "proposed") and w["readiness"] != "blocked"]
    groups = []
    for w in work:
        if w["kind"] != "release" or w["status"] not in ("active", "proposed"):
            continue
        members = [index.summary(index.work[wid]) for wid in w["members"] if wid in index.work]
        groups.append({**w, "children": members, "closed": sum(closed(index.work.get(wid)) for wid in w["members"]),
                       "total": len(w["members"])})
    batches = {}
    for w in work:
        if isinstance(w["batch"], str) and w["status"] in ("proposed", "active"):
            batches.setdefault(w["batch"], []).append(w)
    return {
        "project": root.project, "pitch": first_line(section(brief.body, "Pitch")) if brief else "",
        "constraints": section(brief.body, "Constraints") if brief else "", "focus": index.focus,
        "recommendation": eligible[0] if eligible and not errors else None,
        "active": [w for w in work if w["status"] == "active"],
        "proposed": [w for w in work if w["status"] == "proposed"],
        "groups": groups, "batches": batches,
        "pending_close": [w for w in work if w["status"] == "done"],
        "questions": [{"id": p.id, "blocks": refs(p, "blocks"), "question": first_line(section(p.body, "Question"))} for p in questions],
        "recent": [{"id": p.id, "updated": p.fm.get("updated"), "outcome": outcome(p)} for p in history],
        "lint": {"errors": len(errors), "warnings": len(warnings)}, "schema": root.schema,
    }


def _lines(w, indent=""):
    label = w['kind'] if w['size'] == w['kind'] else f"{w['size']} {w['kind']}"
    lines = [f"{indent}- {w['id']} ({label}): {w['outcome']}",
             f"{indent}  {w['readiness']} · priority {w['priority']} · created {w['created'] or 'unknown'} · updated {w['updated']}"]
    if w["next"]:
        lines.append(f"{indent}  next: {w['next']}")
    if w["why_now"]:
        lines.append(f"{indent}  why now: {w['why_now']}")
    if w["blockers"]:
        lines.append(f"{indent}  blocked: {'; '.join(w['blockers'])}")
    elif w["preparation"] and w["readiness"] != "closed":
        lines.append(f"{indent}  prepare: {'; '.join(w['preparation'])}")
    return lines


def render_status(d):
    out = [f"# {d['project']}", d["pitch"], "", "## Constraints", d["constraints"], "", "## Next"]
    w = d["recommendation"]
    if w:
        out += [f"{w['id']} — {w['readiness']}: {w['next'] or (w['preparation'][0] if w['preparation'] else w['outcome'])}",
                w["selection_reason"]]
    else:
        out.append("Fix lint errors before selecting work." if d["lint"]["errors"] else "No eligible work; resolve blockers or shape the next outcome.")
    if d["focus"]:
        out.append(f"Focus: {d['focus']}")
    out += ["", "## Active"]
    for w in d["active"]:
        out += _lines(w)
    out += ["", "## Proposed"]
    grouped = set()
    for group in d["groups"]:
        out += [f"- {group['id']} release: {group['outcome']} ({group['closed']}/{group['total']} closed)"]
        if group["next"]:
            out.append(f"  next: {group['next']}")
        for w in group["children"]:
            out += _lines(w, "  ")
            grouped.add(w["id"])
        grouped.add(group["id"])
    for w in d["proposed"]:
        if w["id"] not in grouped:
            out += _lines(w)
    if d["batches"]:
        out += ["", "## Consider together"]
        for name, items in d["batches"].items():
            ids = " ".join(w["id"] for w in items)
            out.append(f"- {name}: {ids} — {items[0]['batch_reason']}")
            out.append(f"  assess: grove batch {ids}")
    if d["pending_close"]:
        out += ["", "## Awaiting closure"] + [f"- {w['id']}: grove close {w['id']}" for w in d["pending_close"]]
    out += ["", "## Questions"]
    for q in d["questions"]:
        tag = f" [blocks {', '.join(q['blocks'])}]" if q["blocks"] else ""
        out.append(f"- {q['id']}{tag}: {q['question']}")
    out += ["", "## Recent"] + [f"- {r['id']} {r['updated']}: {r['outcome']}" for r in d["recent"]]
    if d["schema"] < 2:
        out += ["", "Schema 1: grove upgrade enables the schema-2 contract; review legacy prose relationships before execution."]
    out += ["", f"lint: {d['lint']['errors']} errors, {d['lint']['warnings']} warnings"]
    return "\n".join(out) + "\n"
