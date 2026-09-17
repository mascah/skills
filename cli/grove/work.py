"""Work relationships and structural preparation; no execution or inferred authority."""
from datetime import date
from pathlib import Path
import re

from .pages import GroveError, first_line, section


def refs(page, field):
    value = page.fm.get(field, [])
    return [v for v in value if isinstance(v, str)] if isinstance(value, list) else []


def closed(page):
    return page is not None and page.status == "done" and page.in_history


def outcome(page):
    return first_line(section(page.body, "Outcome") or section(page.body, "Question"))


def plan_path(root, page):
    value = page.fm.get("plan")
    if not isinstance(value, str) or not value.strip():
        raise GroveError(f"{page.rel}: plan must be a repo-relative file")
    path = (root.repo / value).resolve()
    if Path(value).is_absolute() or not path.is_relative_to(root.repo.resolve()):
        raise GroveError(f"{page.rel}: plan must stay inside the repository")
    if not path.is_file():
        raise GroveError(f"{page.rel}: plan file missing: {value}")
    return path


class WorkIndex:
    def __init__(self, root):
        self.root = root
        self.pages = root.pages(history=True)
        self.work = {p.id: p for p in self.pages if p.type == "work" and isinstance(p.id, str)}
        self.brief = next((p for p in self.pages if p.type == "brief" and not p.in_history), None)
        self.focus = self.brief.fm.get("focus") if self.brief else None
        self.questions = [p for p in self.pages if p.type == "question" and not p.in_history]

    def ancestors(self, wid):
        found, pending = {}, [wid]
        while pending:
            child = pending.pop()
            for p in self.work.values():
                if not p.in_history and child in refs(p, "members") and p.id not in found and p.id != wid:
                    found[p.id] = p
                    pending.append(p.id)
        return list(found.values())

    def errors(self):
        errors = []
        if self.focus is not None and (not isinstance(self.focus, str) or self.focus not in self.work):
            errors.append("brief: focus must name an existing work id")
        for p in self.work.values():
            for field in ("members", "depends_on"):
                if field not in p.fm:
                    continue
                value = p.fm[field]
                if not isinstance(value, list):
                    errors.append(f"{p.rel}: {field} must be a list")
                    continue
                seen = set()
                for v in value:
                    if not isinstance(v, str) or v not in self.work:
                        errors.append(f"{p.rel}: {field} {v!r} must name an existing work id")
                    elif v in seen:
                        errors.append(f"{p.rel}: duplicate {field} reference {v}")
                    else:
                        seen.add(v)
                if field == "members" and p.fm.get("kind") != "release":
                    errors.append(f"{p.rel}: members belongs to a release work unit")
            priority = p.fm.get("priority", 3)
            if type(priority) is not int or not 1 <= priority <= 5:
                errors.append(f"{p.rel}: priority must be an integer from 1 (highest) to 5")
            if "batch" in p.fm:
                if not isinstance(p.fm["batch"], str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", p.fm["batch"]):
                    errors.append(f"{p.rel}: batch must be a lowercase slug")
                if not isinstance(p.fm.get("batch_reason"), str) or not p.fm["batch_reason"].strip():
                    errors.append(f"{p.rel}: batch needs a batch_reason explaining a shared implementation")
            if "plan" in p.fm:
                try:
                    path = plan_path(self.root, p)
                    if not path.read_text().strip():
                        errors.append(f"{p.rel}: plan file is empty")
                except (GroveError, OSError, UnicodeError) as exc:
                    errors.append(str(exc))
            for field in ("created", "updated", "started"):
                if field in p.fm:
                    try:
                        date.fromisoformat(str(p.fm[field]))
                    except ValueError:
                        errors.append(f"{p.rel}: bad date {field} {p.fm[field]!r}")
        visiting, visited = set(), set()

        def visit(wid):
            if wid in visiting:
                errors.append(f"work relationship cycle through {wid}")
                return
            if wid in visited:
                return
            visiting.add(wid)
            p = self.work[wid]
            for dep in refs(p, "members") + refs(p, "depends_on"):
                if dep in self.work:
                    visit(dep)
            visiting.remove(wid)
            visited.add(wid)

        for wid in self.work:
            visit(wid)
        return errors

    def blockers(self, p, selected=()):
        blockers = []
        for dep in refs(p, "depends_on") + refs(p, "members"):
            if dep not in selected and not closed(self.work.get(dep)):
                blockers.append(f"{dep} is not closed")
        # A release acceptance gate does not prevent preparing/implementing its members.
        # A question that blocks a member must name that member explicitly.
        for q in self.questions:
            if p.id in refs(q, "blocks"):
                blockers.append(f"question {q.id}: {first_line(section(q.body, 'Question'))}")
        return list(dict.fromkeys(blockers))

    def relationship_gaps(self, p):
        gaps = []
        if section(p.body, "Dependencies") and "depends_on" not in p.fm:
            gaps.append("Review prose Dependencies and record depends_on (use [] when none)")
        if p.fm.get("kind") == "release" and not refs(p, "members"):
            gaps.append("Record release members")
        return gaps

    def preparation(self, p):
        gaps = self.relationship_gaps(p)
        size = p.fm.get("size")
        required = ("Question", "Bounds") if size == "spike" else ("Outcome", "Acceptance")
        if size in ("bounded", "large"):
            required += ("Constraints",)
        if size == "large":
            required += ("Checkpoints", "Verification")
        for heading in required:
            if not section(p.body, heading):
                gaps.append(f"Write {heading}")
        has_plan = bool(section(p.body, "Plan"))
        if "plan" in p.fm:
            try:
                has_plan = bool(plan_path(self.root, p).read_text().strip())
            except (GroveError, OSError, UnicodeError):
                has_plan = False
        if not has_plan and not (size == "small" and section(p.body, "Next")):
            gaps.append("Prepare implementation plan" if size != "spike" else "Prepare experiment plan")
        return gaps

    def summary(self, p):
        blockers, prep = self.blockers(p), self.preparation(p)
        if closed(p):
            readiness = "closed"
        elif p.status in ("done", "abandoned"):
            readiness = "needs-close" if p.status == "done" else "abandoned"
        elif blockers:
            readiness = "blocked"
        elif any(not g.startswith("Prepare ") for g in prep):
            readiness = "needs-shaping"
        elif prep:
            readiness = "needs-plan"
        else:
            readiness = "ready"
        priority = p.fm.get("priority", 3)
        return {"id": p.id, "basename": p.basename, "kind": p.fm.get("kind"), "size": p.fm.get("size"),
                "status": p.status, "outcome": outcome(p), "next": first_line(section(p.body, "Next")),
                "created": p.fm.get("created"), "updated": p.fm.get("updated"),
                "priority": priority if type(priority) is int else 3,
                "why_now": first_line(section(p.body, "Why now")),
                "members": refs(p, "members"), "depends_on": refs(p, "depends_on"),
                "parents": [x.id for x in self.ancestors(p.id)],
                "batch": p.fm.get("batch"), "batch_reason": p.fm.get("batch_reason"),
                "plan": p.fm.get("plan"), "readiness": readiness, "blockers": blockers, "preparation": prep}

    def ordered(self):
        focus_order = []

        def walk(wid):
            if wid in focus_order or wid not in self.work:
                return
            focus_order.append(wid)
            for child in refs(self.work[wid], "members"):
                walk(child)

        if isinstance(self.focus, str):
            walk(self.focus)
        rank = {wid: i for i, wid in enumerate(focus_order)}
        rows = [self.summary(p) for p in self.work.values() if not p.in_history]
        rows.sort(key=lambda w: (w["status"] != "active", w["id"] not in rank,
                                 rank.get(w["id"], 0), w["priority"], w["id"]))
        for w in rows:
            if w["status"] == "active":
                reason = "Continue active work"
            elif w["id"] in rank:
                reason = f"Selected focus {self.focus}"
                if w["id"] != self.focus:
                    reason += "; release member order"
            else:
                reason = f"Priority {w['priority']}; ID breaks ties"
            w["selection_reason"] = reason + (f": {w['why_now']}" if w["why_now"] else "")
        return rows


def batch(root, ids):
    from .lint import lint

    index = WorkIndex(root)
    ids = list(dict.fromkeys(ids))
    for wid in ids:
        p = index.work.get(wid)
        if p is None or p.in_history or p.status not in ("proposed", "active"):
            raise GroveError(f"{wid}: select proposed or active work")
        if p.fm.get("kind") == "release":
            raise GroveError(f"{wid}: select its implementation members; release acceptance stays separate")
    errors, _ = lint(root)
    blockers = list(errors)
    for wid in ids:
        blockers.extend(f"{wid}: {b}" for b in index.blockers(index.work[wid], ids))
    order, seen = [], set()

    def visit(wid):
        if wid in seen:
            return
        seen.add(wid)
        for dep in refs(index.work[wid], "depends_on"):
            if dep in ids:
                visit(dep)
        order.append(wid)

    for wid in ids:
        visit(wid)
    rows = [index.summary(index.work[wid]) for wid in order]
    scopes = [set(refs(index.work[wid], "scope")) for wid in ids]
    shared = sorted({s for scope in scopes for s in scope if sum(s in other for other in scopes) > 1})
    gaps = [f"{w['id']}: {g}" for w in rows for g in w["preparation"]]
    return {"work": rows, "order": order, "assessment": "blocked" if blockers else "needs-planning" if gaps else "prepared",
            "blockers": blockers, "preparation": gaps, "shared_scope": shared,
            "parallel": "Requires code ownership and interface review; capability scope does not establish independent writes.",
            "next": "Resolve external blockers" if blockers else "Prepare one shared plan with per-work acceptance and joint verification" if gaps
                    else "Review plans against the checkout and reconcile into one shared implementation plan"}


def render_batch(d):
    lines = [f"# Shared implementation: {', '.join(d['order'])}", f"Assessment: {d['assessment']}",
             "Order: " + " → ".join(d["order"]), "A single implementation may execute dependent items sequentially.",
             "Shared capabilities: " + (", ".join(d["shared_scope"]) or "none recorded"), "Parallel: " + d["parallel"]]
    for w in d["work"]:
        lines.append(f"- {w['id']}: {w['outcome']}")
        if w["batch_reason"]:
            lines.append(f"  together: {w['batch_reason']}")
    for title, key in (("Blockers", "blockers"), ("Preparation", "preparation")):
        if d[key]:
            lines += ["", f"## {title}"] + [f"- {x}" for x in d[key]]
    return "\n".join(lines + ["", "Next: " + d["next"], ""])
