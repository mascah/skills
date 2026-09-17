"""Knowledge pages: frontmatter, links, loading. Stdlib only.
Frontmatter is a YAML subset: scalars, inline lists, and `- item` lists."""
import json
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

TYPES = {"brief", "capability", "decision", "work", "question", "term"}
FOLDER = {"capabilities": "capability", "decisions": "decision", "work": "work", "questions": "question", "terms": "term"}
STATUS = {
    "brief": {"active", "parked", "retired"},
    "capability": {"draft", "settled"},
    "decision": {"proposed", "accepted", "rejected", "superseded"},
    "work": {"proposed", "active", "done", "abandoned"},
    "question": {"open", "parked"},
    "term": {"draft", "settled"},
}
KINDS = {"feature", "fix", "refactor", "spike", "tooling", "migration", "investigation", "release"}
SIZES = {"small", "spike", "bounded", "large"}
LIST_FIELDS = {"applies_to", "scope", "unchanged", "blocks", "sources", "members", "depends_on"}
REQUIRED = ["type", "id", "status", "updated"]
SCHEMA = 2

LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]")
FM = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


class GroveError(Exception):
    """User-facing failure; cli prints str(exc) and exits 1."""


def _scalar(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        if v[0] == '"':
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                pass
        return v[1:-1]
    if v == "true":
        return True
    if v == "false":
        return False
    if v in ("", "null", "~"):
        return None
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


def _split_list(s):
    out, cur, q = [], "", None
    for ch in s:
        if q:
            cur += ch
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            cur += ch
        elif ch == ",":
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return out


def parse_frontmatter(text):
    m = FM.match(text)
    if not m:
        return None, text
    fm, last = {}, None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"^\s+-\s*(.*)$", line)
        if item and last:
            if not isinstance(fm[last], list):
                fm[last] = []
            fm[last].append(_scalar(item.group(1)))
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        last = k.strip()
        if v.startswith("[") and v.endswith("]"):
            try:
                fm[last] = json.loads(v)
            except json.JSONDecodeError:
                inner = v[1:-1].strip()
                fm[last] = [_scalar(x) for x in _split_list(inner)] if inner else []
        else:
            fm[last] = _scalar(v)
    return fm, text[m.end():]


def links(text):
    return [t.strip() for t, _ in LINK.findall(text)]


def section(body, heading):
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def first_line(text):
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


@dataclass
class Root:
    repo: Path
    knowledge: Path
    project: str
    schema: int

    def pages(self, history=False):
        out = []
        for p in sorted(self.knowledge.rglob("*.md")):
            rel = p.relative_to(self.knowledge)
            if rel.parts[0] == "history":
                if not history or p.name == "README.md":
                    continue
            out.append(Page(p, self))
        return out

    def by_basename(self):
        return {p.basename: p for p in self.pages(history=True)}

    def get(self, key):
        """Look up by basename or by id (D-0001, W-003, slug); a live page wins over history."""
        by = self.by_basename()
        if key in by:
            return by[key]
        candidates = [p for p in by.values() if p.id == key]
        live = next((p for p in candidates if not p.in_history), None)
        return live if live is not None else next(iter(candidates), None)

    def rel(self, path):
        return Path(path).relative_to(self.repo).as_posix()


class Page:
    def __init__(self, path, root):
        self.path = Path(path)
        self.root = root
        self.text = self.path.read_text()
        fm, self.body = parse_frontmatter(self.text)
        self.fm = fm or {}

    @property
    def type(self):
        return self.fm.get("type")

    @property
    def id(self):
        return self.fm.get("id")

    @property
    def status(self):
        return self.fm.get("status")

    @property
    def basename(self):
        return self.path.stem

    @property
    def in_history(self):
        return "history" in self.path.relative_to(self.root.knowledge).parts

    @property
    def in_evidence(self):
        parts = self.path.relative_to(self.root.knowledge).parts
        return len(parts) > 1 and parts[0] == "history" and parts[1] == "evidence"

    @property
    def rel(self):
        return self.root.rel(self.path)

    def tokens(self):
        return len(self.text) // 4

    def links(self):
        out = links(self.body)
        for v in self.fm.values():
            for x in (v if isinstance(v, list) else [v]):
                if isinstance(x, str):
                    out += links(x)
        return out


def load_root(start):
    start = Path(start).resolve()
    for d in [start, *start.parents]:
        cfg = d / "grove.toml"
        if cfg.exists():
            try:
                data = tomllib.loads(cfg.read_text())
            except tomllib.TOMLDecodeError as exc:
                raise GroveError(f"grove.toml is not valid TOML: {exc}")
            schema = int(data.get("schema", 0))
            if schema > SCHEMA:
                raise GroveError(f"grove.toml schema {schema} is newer than this grove ({SCHEMA}); upgrade grove")
            return Root(repo=d, knowledge=d / data.get("root", "docs/grove"), project=data.get("project", d.name), schema=schema)
    raise GroveError("no grove.toml found here or above; run `grove init`")
