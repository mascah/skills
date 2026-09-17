"""Deterministic structure checks. Returns (errors, warnings); never edits."""
import re
from .pages import FOLDER, KINDS, LIST_FIELDS, REQUIRED, SIZES, STATUS, first_line, links, section
from .work import WorkIndex, refs

ID_PREFIX = {"decision": re.compile(r"D-\d{4}"), "work": re.compile(r"W-\d{3}")}

# Type-specific required fields beyond REQUIRED
TYPE_REQUIRED = {
    "decision": {"applies_to"},
    "work": {"kind", "size", "scope"},
    "question": {"blocks"},
}


def lint(root):
    errors, warnings = [], []
    pages = root.pages(history=True)
    by_name = {}
    for p in pages:
        by_name.setdefault(p.basename, []).append(p)
    for name, dups in by_name.items():
        if len(dups) > 1:
            for p in dups:
                errors.append(f"{p.rel}: duplicate basename '{name}'")
    caps = {p.basename for p in pages if p.type == "capability" and not p.in_history}
    referenced = set()
    for p in pages:
        if p.in_history or p.type not in ("capability", "work", "brief"):
            continue
        referenced.update(p.links())

    id_groups = {}
    for p in pages:
        if p.in_evidence or not p.fm:
            continue
        if p.type in ("decision", "work") and p.id:
            id_groups.setdefault((p.type, p.id), []).append(p)
    for (_, dup_id), dups in id_groups.items():
        if len(dups) > 1:
            for p in dups:
                errors.append(f"{p.rel}: duplicate id '{dup_id}'")

    for p in pages:
        e = lambda msg, p=p: errors.append(f"{p.rel}: {msg}")
        w = lambda msg, p=p: warnings.append(f"{p.rel}: {msg}")
        if p.in_evidence:
            continue
        if not p.fm:
            e("no frontmatter")
            continue
        for k in REQUIRED:
            if k not in p.fm:
                e(f"missing {k}")
        for field in ("updated", "started"):
            v = p.fm.get(field)
            if v is not None and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v)):
                e(f"bad date {field} {v!r}")
        folder = p.path.relative_to(root.knowledge).parts
        folder = folder[1] if folder[0] == "history" and len(folder) > 1 else folder[0]
        expected = "brief" if p.path.name == "brief.md" and not p.in_history else FOLDER.get(folder)
        if p.type != expected:
            e(f"type {p.type!r} but folder says {expected!r}")
            continue
        for k in TYPE_REQUIRED.get(p.type, set()):
            if k not in p.fm:
                e(f"missing {k}")
        if p.status not in STATUS.get(p.type, set()):
            e(f"bad status {p.status!r}")
        for k in LIST_FIELDS:
            if k in p.fm and not isinstance(p.fm[k], list):
                e(f"{k} must be a list")
        if p.type in ID_PREFIX:
            m = ID_PREFIX[p.type].match(p.basename)
            if not m or p.id != m.group(0):
                e(f"id {p.id!r} does not match basename")
        elif p.id not in (p.basename, "brief" if p.type == "brief" else None):
            e(f"id {p.id!r} does not match basename")
        for t in p.links():
            targets = by_name.get(t)
            if not targets:
                e(f"unresolved link [[{t}]]")
            elif not p.in_history and targets[0].in_history:
                evidence_links = links(section(p.body, "Evidence")) if p.type == "work" else set()
                work_reference = (p.type == "work" and targets[0].type == "work" and
                                  (targets[0].id in refs(p, "members") + refs(p, "depends_on") or
                                   t in links(section(p.body, "Dependencies"))))
                if t not in evidence_links and not work_reference:
                    e(f"live page links into history: [[{t}]]")
        if p.type == "decision":
            for slug in p.fm.get("applies_to") or [] if isinstance(p.fm.get("applies_to"), list) else []:
                if slug not in caps:
                    e(f"applies_to {slug!r} is not a capability")
            if p.status == "superseded":
                if not p.in_history:
                    e("superseded decision must live in history/decisions")
                if not p.fm.get("superseded_by"):
                    e("superseded without superseded_by")
            if p.status == "accepted" and not p.in_history and p.basename not in referenced and p.id not in referenced:
                w("accepted decision referenced by no capability or work")
        if p.type == "work":
            if "kind" in p.fm and p.fm.get("kind") not in KINDS:
                e(f"bad kind {p.fm.get('kind')!r}")
            size = p.fm.get("size")
            if "size" in p.fm and size not in SIZES:
                e(f"bad size {size!r}")
            if p.status == "active" and "started" not in p.fm:
                e("missing started")
            for slug in p.fm.get("scope") or [] if isinstance(p.fm.get("scope"), list) else []:
                if slug not in caps:
                    e(f"scope {slug!r} is not a capability")
            if p.in_history and p.status not in ("done", "abandoned"):
                e("history work must be done or abandoned")
            if not p.in_history and p.status == "done":
                w("done but not closed")
            if not p.in_history and size == "large" and not section(p.body, "Constraints"):
                e("large work needs a Constraints section")
            if not p.in_history and size in ("large", "bounded") and not section(p.body, "Acceptance"):
                e(f"{size} work needs an Acceptance section")
            if p.status == "active" and not first_line(section(p.body, "Next")):
                w("active work has no Next line")
        if p.type == "capability":
            for line in section(p.body, "Code").splitlines():
                ptr = line.strip().lstrip("-").strip()
                if ptr and not (root.repo / ptr).exists():
                    w(f"code pointer missing: {ptr}")
    errors.extend(WorkIndex(root).errors())
    return list(dict.fromkeys(errors)), warnings
