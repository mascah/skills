"""Read-only committed-delivery check: does a candidate revision actually deliver the work its
own declaration claims, with no dependence on local claims or uncommitted state. Stdlib only."""
import json
import subprocess
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path

from .close import DECL_DIR, closure_errors
from .contract import git
from .lint import lint
from .pages import GroveError, load_root

SCHEMA = 1


class Inapplicable(GroveError):
    """No usable delivery declaration on this branch; cli exits 2 for this."""


def _resolve(repo, ref):
    return git(repo, "rev-parse", "--verify", ref).strip()


def _exists_at(repo, rev, path):
    p = subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"{rev}:{path}"], capture_output=True)
    return p.returncode == 0


def _declaration(repo, base_sha, candidate_sha):
    # Three-dot: merge-base(base, candidate)..candidate, so a delivery another branch already
    # merged to base after this branch forked does not show up as a second "changed" declaration.
    changed = [l for l in git(repo, "diff", "--name-only", f"{base_sha}...{candidate_sha}", "--", f"{DECL_DIR}/").splitlines() if l]
    if not changed:
        raise Inapplicable("no delivery declaration on this branch")
    if len(changed) > 1:
        raise Inapplicable("ambiguous delivery declaration: " + ", ".join(sorted(changed)))
    path = changed[0]
    try:
        data = json.loads(git(repo, "show", f"{candidate_sha}:{path}"))
    except (GroveError, ValueError) as exc:
        raise Inapplicable(f"malformed delivery declaration {path}: {exc}")
    if not isinstance(data, dict) or data.get("schema") != SCHEMA or not isinstance(data.get("delivers"), list):
        raise Inapplicable(f"malformed delivery declaration {path}")
    delivers = [w for w in data["delivers"] if isinstance(w, str)]
    retains = [w for w in data.get("retains", []) if isinstance(w, str)] if isinstance(data.get("retains"), list) else []
    return delivers, retains


def _load_tree(repo, sha, tmp):
    """Read-only load of grove.toml + docs/grove at sha into tmp; per-file `git show` if `git
    archive` can't be read back."""
    p = subprocess.run(["git", "-C", str(repo), "archive", sha, "grove.toml", "docs/grove"], capture_output=True)
    if p.returncode == 0:
        with tarfile.open(fileobj=BytesIO(p.stdout)) as tar:
            tar.extractall(tmp, filter="data")
        try:
            return load_root(tmp)
        except GroveError:
            pass
    listing = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", sha, "grove.toml", "docs/grove"],
                              capture_output=True, text=True)
    if listing.returncode:
        raise GroveError(f"cannot read tree at {sha}: {listing.stderr.strip()}")
    for rel in filter(None, listing.stdout.splitlines()):
        show = subprocess.run(["git", "-C", str(repo), "show", f"{sha}:{rel}"], capture_output=True)
        if show.returncode == 0:
            dest = tmp / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(show.stdout)
    return load_root(tmp)


def _find(tree, wid):
    return [p for p in tree.pages(history=True) if p.type == "work" and p.id == wid]


def verify_delivery(root, candidate="HEAD", base="main"):
    repo = root.repo
    candidate_sha = _resolve(repo, candidate)
    try:
        base_sha = _resolve(repo, base)
    except GroveError:
        raise Inapplicable(f"base ref {base!r} does not resolve; pass --base")
    delivers, retains = _declaration(repo, base_sha, candidate_sha)
    errors = []
    with tempfile.TemporaryDirectory(prefix="grove-verify-") as tmp:
        tree = _load_tree(repo, candidate_sha, Path(tmp))
        for wid in delivers:
            matches = _find(tree, wid)
            if not matches:
                errors.append(f"{wid}: no such work id")
                continue
            if len(matches) > 1:
                errors.append(f"{wid}: id resolves to {len(matches)} pages")
                continue
            work = matches[0]
            if not work.in_history:
                errors.append(f"{wid}: {work.status} work is not archived")
                continue
            if work.status != "done":
                errors.append(f"{wid}: history status is {work.status}, not done")
                continue
            if _exists_at(repo, base_sha, tree.rel(work.path)):
                errors.append(f"{wid}: already closed at base")
                continue
            errs = closure_errors(tree, work)
            if errs:
                errors.append(f"{wid}: {errs[0]}")
        for wid in retains:
            matches = _find(tree, wid)
            if not matches:
                errors.append(f"retains {wid}: no such work id")
            elif len(matches) > 1:
                errors.append(f"retains {wid}: id resolves to {len(matches)} pages")
            elif matches[0].in_history:
                errors.append(f"retains {wid}: already closed")
        lint_errors, _ = lint(tree)
        if lint_errors:
            errors.append(f"candidate lint has {len(lint_errors)} error(s): " + "; ".join(lint_errors))
    return {"checked": candidate_sha, "base": base_sha, "delivers": delivers, "retains": retains, "errors": errors}


def render_delivery(d):
    lines = [f"checked {d['checked']}", f"base {d['base']}",
             f"delivers: {', '.join(d['delivers']) or 'none'}",
             f"retains: {', '.join(d['retains']) or 'none'}"]
    if d["errors"]:
        lines += ["", "errors:"] + [f"- {e}" for e in d["errors"]]
    else:
        lines.append("delivery verified")
    return "\n".join(lines) + "\n"
