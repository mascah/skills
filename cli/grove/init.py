"""Set up a repo for grove. Safe to rerun; touches only the managed block in agent files."""
import datetime
import json
import re
import tomllib
from pathlib import Path
from .pages import SCHEMA, GroveError, load_root

BLOCK_BEGIN = "<!-- grove:begin -->"
BLOCK_END = "<!-- grove:end -->"
BLOCK = """## Grove
Project knowledge lives in `docs/grove/`. Do not read that tree directly; use the CLI.
- Start every session with `grove status`.
- Before touching a work unit run `grove context --work <id>` (add `--phase shape|plan|debug|debrief` when not implementing).
- For one implementation spanning several units, run `grove batch <ids>` and prepare a shared plan.
- After writing any knowledge page run `grove lint`.
- Every session that writes, shaping and curation included, works on its own worktree branch and never commits to main; a non-work session with no work ID yet is named for its skill and topic (`worktree-<skill>-<slug>`); each session ends by saying how to merge.
- Claim work before changing it (`grove claim <ids>`) and run `grove verify-delivery` before handing a branch to the human.
- Finish implementation with the `grove:close` skill, which ends in `grove close <id>`.
- Give every commit a Conventional Commits subject (`type(scope): summary`, `docs` for knowledge-only changes, `docs: close <id>` for the close) and put the work ID in a `Refs: <id>` footer, never in the subject."""
BRIEF_TEMPLATE = """---
type: brief
id: brief
status: active
updated: {today}
---
## Pitch
One sentence: what this is and for whom.

## Who it's for

## Why

## Constraints

## Not now
"""
HISTORY_README = "Records that no longer apply live here. Excluded from `grove status`, `grove context`, and `grove find` by default.\n"
DIRS = ("capabilities", "decisions", "work", "questions", "terms", "history/work", "history/decisions", "history/evidence")
_BLOCK_RE = re.compile(re.escape(BLOCK_BEGIN) + r"\r?\n.*?\r?\n" + re.escape(BLOCK_END), re.S)


def upgrade(root):
    if root.schema == SCHEMA:
        return f"schema {SCHEMA}: already current"
    cfg = root.repo / "grove.toml"
    old = cfg.read_text()
    expected = {**tomllib.loads(old), "schema": SCHEMA}
    # Validate the entire candidate's meaning: a lookalike declaration may be inside
    # a multiline string or table. Preserve every other config value and byte.
    pattern = r'''(?m)^[ \t]*(?:schema|"schema"|'schema')[ \t]*=[ \t]*(\d[\d_]*)'''
    for match in re.finditer(pattern, old):
        start, end = match.span(1)
        new = old[:start] + str(SCHEMA) + old[end:]
        try:
            valid = tomllib.loads(new) == expected
        except tomllib.TOMLDecodeError:
            valid = False
        if valid:
            cfg.write_text(new)
            return f"upgraded schema to {SCHEMA}; review members, depends_on, focus and plans with grove:shape; content unchanged"
    raise GroveError("grove.toml needs a top-level integer schema declaration")


def replace_block(text, body):
    # Check if there's a well-formed block
    match = _BLOCK_RE.search(text)
    if match:
        # Preserve the line ending style from the original block
        original_block = match.group(0)
        if "\r\n" in original_block:
            block = f"{BLOCK_BEGIN}\r\n{body}\r\n{BLOCK_END}"
        else:
            block = f"{BLOCK_BEGIN}\n{body}\n{BLOCK_END}"
        return _BLOCK_RE.sub(lambda _: block, text)

    # Check for malformed markers (begin without end, or end before begin, etc.)
    has_begin = BLOCK_BEGIN in text
    has_end = BLOCK_END in text
    if has_begin or has_end:
        raise GroveError("malformed grove block markers")

    # No existing block, append one
    block = f"{BLOCK_BEGIN}\n{body}\n{BLOCK_END}"
    sep = "" if not text or text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    return f"{text}{sep}{block}\n"


def init(repo):
    repo = Path(repo)
    actions = []
    cfg = repo / "grove.toml"
    if not cfg.exists():
        cfg.write_text(f'schema = {SCHEMA}\nproject = {json.dumps(repo.name)}\nroot = "docs/grove"\n')
        actions.append("wrote grove.toml")
    root = load_root(repo)
    k = root.knowledge
    knowledge_path = root.rel(k)
    for d in DIRS:
        (k / d).mkdir(parents=True, exist_ok=True)
        keep = k / d / ".gitkeep"
        if not keep.exists():
            keep.touch()
    brief = k / "brief.md"
    if not brief.exists():
        brief.write_text(BRIEF_TEMPLATE.format(today=datetime.date.today().isoformat()))
        actions.append(f"wrote {knowledge_path}/brief.md")
    readme = k / "history" / "README.md"
    if not readme.exists():
        readme.write_text(HISTORY_README)
        actions.append(f"wrote {knowledge_path}/history/README.md")
    for name in ("CLAUDE.md", "AGENTS.md"):
        f = repo / name
        old = f.read_text() if f.exists() else ""
        try:
            new = replace_block(old, BLOCK.replace("docs/grove/", knowledge_path + "/"))
        except GroveError as e:
            raise GroveError(f"{name}: {e}") from None
        if new != old:
            f.write_text(new)
            actions.append(f"{'updated' if BLOCK_BEGIN in old else 'wrote'} {name} block")
    return actions
