"""Scoped context for one work unit, in a fixed tier order, within a budget."""
from .pages import GroveError, section, links
from types import SimpleNamespace
from .work import WorkIndex, outcome, refs, plan_path
from .lint import lint

PHASES = ("shape", "plan", "implement", "debug", "debrief")
DECISION_ORDER = {"accepted": 0, "proposed": 1, "rejected": 2}


def _candidates(root, work, phase, included_pages):
    """Yield (tier, basename, text, page_or_None) in inclusion order."""
    by = root.by_basename()
    live = [p for p in root.pages()]
    scope = [s for s in (work.fm.get("scope") or []) if isinstance(s, str)]
    yield 1, work.basename, work.text, work
    index = WorkIndex(root)
    parents = index.ancestors(work.id)
    for parent in parents:
        text = f"## Parent {parent.id}\n{outcome(parent)}\n"
        for heading in ("Constraints", "Acceptance"):
            if section(parent.body, heading):
                text += f"\n## {heading}\n{section(parent.body, heading)}\n"
        yield 1, parent.basename + "#contract", text, parent
    for field in ("depends_on", "members"):
        related = []
        for wid in refs(work, field):
            p = index.work.get(wid)
            if p:
                w = index.summary(p)
                related.append(f"- {wid}: {w['readiness']} — {w['outcome']} ({p.rel})")
            else:
                related.append(f"- {wid}: missing work")
        if related:
            yield 1, work.basename + "#" + field, f"## {field}\n" + "\n".join(related) + "\n", work
    if work.fm.get("plan") and phase in ("plan", "implement", "debug", "debrief"):
        path = plan_path(root, work)
        yield 1, work.basename + "#plan", path.read_text(), SimpleNamespace(rel=root.rel(path), type="plan")
    owner_ids = {work.id, *(p.id for p in parents)}
    blocking = [q for q in index.questions if owner_ids.intersection(refs(q, "blocks"))]
    for q in blocking:
        yield 1, q.basename, q.text, q
    # Tier 2: scoped capabilities (only live, type=capability)
    caps = []
    for s in scope:
        if s in by:
            p = by[s]
            if not p.in_history and p.type == "capability":
                caps.append(p)
    for c in caps:
        if work.fm.get("kind") == "release" and phase == "shape":
            text = f"## Capability {c.id}\n"
            for heading in ("Acceptance", "Constraints", "Code"):
                if section(c.body, heading):
                    text += f"\n## {heading}\n{section(c.body, heading)}\n"
            yield 2, c.basename, text, c
        else:
            yield 2, c.basename, c.text, c
    # Tier 3: decisions
    decisions = [p for p in live if p.type == "decision" and p.status != "superseded"
                 and set(p.fm.get("applies_to") or []) & set(scope)]
    if phase not in ("shape", "plan"):
        decisions = [p for p in decisions if p.status != "rejected"]
    for d in sorted(decisions, key=lambda p: (DECISION_ORDER.get(p.status, 9), p.basename)):
        yield 3, d.basename, d.text, d
    # Tier 3.5: brief#not-now in shape
    brief = None
    if phase == "shape":
        brief = next((p for p in live if p.type == "brief"), None)
        if brief and section(brief.body, "Not now"):
            yield 4, "brief#not-now", "## Not now\n" + section(brief.body, "Not now") + "\n", brief
    # Tier 4: terms linked from included pages (not from all candidates)
    linked = set()
    for text in included_pages.values():
        linked.update(links(text))
    for t in sorted(linked):
        if t in by and by[t].type == "term" and not by[t].in_history:
            yield 4, t, by[t].text, by[t]
    # Tier 5: open questions
    for q in live:
        if q.type != "question" or q.status != "open" or q.id in {b.id for b in blocking}:
            continue
        hits = set(q.links())
        if work.id in (q.fm.get("blocks") or []) or work.basename in hits or hits & set(scope):
            yield 5, q.basename, q.text, q


def context(root, work_id, phase="implement", budget=6000):
    if phase not in PHASES:
        raise GroveError(f"phase must be one of {', '.join(PHASES)}")
    work = root.get(work_id)
    if not work or work.type != "work":
        raise GroveError(f"no work unit {work_id}")
    d = {"work": work.id, "phase": phase, "budget": budget, "used": 0, "included": [], "omitted": [], "errors": [], "code": [], "pages": {}}
    index = WorkIndex(root)
    d["readiness"] = index.summary(work)
    d["errors"].extend(lint(root)[0])
    if d["errors"]:
        d["readiness"]["readiness"] = "invalid"
    if phase == "debrief":
        d["acceptance"] = section(work.body, "Acceptance")
    if d["errors"]:
        return d
    for tier, name, text, page in _candidates(root, work, phase, d["pages"]):
        tokens = len(text) // 4
        rel = page.rel
        entry = {"tier": tier, "basename": name, "rel": rel, "tokens": tokens}
        if d["used"] + tokens <= budget:
            d["used"] += tokens
            d["included"].append(entry)
            d["pages"][name] = text
            if page and page.type == "capability":
                for line in section(page.body, "Code").splitlines():
                    ptr = line.strip().lstrip("-").strip()
                    if ptr:
                        d["code"].append(ptr)
        else:
            d["omitted"].append(entry)
            if tier <= 3:
                d["errors"].append(f"{name} (tier {tier}, {tokens} tokens) does not fit budget {budget}; raise --budget or read {rel}")
    return d


def render_context(d):
    out = [f"# Context: {d['work']} ({d['phase']}), {d['used']}/{d['budget']} tokens", ""]
    w = d["readiness"]
    out += [f"Preparation: {w['readiness']} (structural checks; validate against the checkout)"]
    out += [f"- {x}" for x in w["blockers"] + w["preparation"]] + [""]
    if d["phase"] == "debrief":
        acc = d.get("acceptance", "")
        out += ["## Acceptance checklist", acc, ""]
    pages = [(i, d["pages"][i["basename"]]) for i in d["included"]]
    code = ["## Code"] + [f"- {c}" for c in d["code"]] + [""] if d["code"] else []
    body = []
    for i, text in pages:
        if d["phase"] == "debug" and i["tier"] == 4 and code:
            body += code
            code = []
        body += [f"<!-- {i['basename']} -->", text.rstrip(), ""]
    out += body + code
    out += ["## Sources"] + [f"- {i['rel']}" for i in d["included"]] + [""]
    if d["omitted"]:
        out += ["## Omitted"] + [f"- {i['basename']} (tier {i['tier']}, {i['tokens']} tokens): {i['rel']} or `grove find {i['basename']}`" for i in d["omitted"]] + [""]
    if d["errors"]:
        out += ["## Errors"] + [f"- {e}" for e in d["errors"]] + [""]
    return "\n".join(out)
