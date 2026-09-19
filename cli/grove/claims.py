"""Shared work-claim registry: visible from every linked worktree via the common git dir, so
no tracked file changes and no commit are needed to see who owns what. Stdlib only."""
import json
import os
import secrets
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from .pages import GroveError, parse_frontmatter

SCHEMA = 1


class Owned(GroveError):
    """Refused because the claim is held by another checkout; cli exits 4 for this."""


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _run(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def _git(repo, *args):
    p = _run(repo, *args)
    if p.returncode:
        raise GroveError(f"git {' '.join(args)}: {p.stderr.strip() or 'failed'}")
    return p.stdout.strip()


def _git_path(repo, arg):
    out = _git(repo, "rev-parse", arg)
    p = Path(out)
    return p if p.is_absolute() else (Path(repo) / p).resolve()


def _grove_dir(repo):
    return _git_path(repo, "--git-common-dir") / "grove"


def registry_path(repo):
    return _grove_dir(repo) / "claims.json"


def owner_token(repo):
    """Same worktree = same owner, always; the agent never carries or types a token."""
    path = _git_path(repo, "--git-dir") / "grove-owner"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(secrets.token_hex(8))
    return path.read_text().strip()


def load_claims(repo):
    path = registry_path(repo)
    if not path.exists():
        return {"schema": SCHEMA, "claims": {}}
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        raise GroveError(f"claims registry unreadable: {path}; fix or remove it by hand")
    if not isinstance(data, dict) or not isinstance(data.get("claims"), dict):
        raise GroveError(f"claims registry unreadable: {path}; fix or remove it by hand")
    return data


def _write(repo, data):
    path = registry_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
    os.replace(tmp, path)


class _locked:
    """os.O_EXCL lock file around read-check-write; refuses instead of hanging when truly stuck.
    # ponytail: one global lock; fine for a handful of worktrees, per-account locks if throughput matters
    """

    def __init__(self, repo):
        self.repo = repo
        self.path = _grove_dir(repo) / "claims.lock"

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + 2.0
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                return self
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise GroveError(f"another grove is writing claims; retry, or remove {self.path} if none is running")
                time.sleep(0.01)

    def __exit__(self, *exc):
        self.path.unlink(missing_ok=True)
        return False


def acquire(root, ids, take=False):
    """Claim the whole set or nothing. Already owned by this checkout: no-op. Owned elsewhere
    without --take: refuse all, nothing written."""
    repo = root.repo
    owner = owner_token(repo)
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    worktree = _git(repo, "rev-parse", "--show-toplevel")
    with _locked(repo):
        data = load_claims(repo)
        claims = data["claims"]
        if not take:
            foreign = [wid for wid in ids if claims.get(wid) and claims[wid]["owner"] != owner]
            if foreign:
                lines = [f"{wid}: claimed by {claims[wid]['branch']} ({claims[wid]['worktree']})" for wid in foreign]
                raise Owned("already claimed:\n" + "\n".join(lines))
        acquired_at = now()
        result = {}
        for wid in ids:
            existing = claims.get(wid)
            if existing and existing["owner"] == owner and not take:
                result[wid] = existing  # same-owner retry: no change
                continue
            claims[wid] = result[wid] = {"branch": branch, "worktree": worktree, "owner": owner, "acquired": acquired_at}
        _write(repo, data)
    return result


def release(root, ids):
    """Release only claims owned by this checkout; a foreign claim is refused with its owner
    and the --take hint. Releasing an id with no claim is a no-op."""
    repo = root.repo
    owner = owner_token(repo)
    with _locked(repo):
        data = load_claims(repo)
        claims = data["claims"]
        foreign = [wid for wid in ids if claims.get(wid) and claims[wid]["owner"] != owner]
        if foreign:
            lines = [f"{wid}: owned by {claims[wid]['branch']}; release refused, use --take to override" for wid in foreign]
            raise Owned("\n".join(lines))
        released = [wid for wid in ids if wid in claims]
        for wid in released:
            del claims[wid]
        _write(repo, data)
    return released


def _page_filename(root, claim_id):
    page = root.get(claim_id)
    return page.path.name if page is not None else f"{claim_id}.md"


def observe(root, claim_id, claim):
    """One label per claim: local disk/ref state first (cheap, no git needed for the worktree
    check), then committed content on the claiming branch. Never executes in another checkout."""
    repo = root.repo
    if not Path(claim["worktree"]).is_dir():
        return "worktree missing"
    branch = claim["branch"]
    if _run(repo, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}").returncode:
        return "branch gone"
    name = _page_filename(root, claim_id)
    knowledge_rel = root.rel(root.knowledge)
    history_path = f"{knowledge_rel}/history/work/{name}"
    if _run(repo, "cat-file", "-e", f"{branch}:{history_path}").returncode == 0:
        return "closed on branch, awaiting integration"
    live_path = f"{knowledge_rel}/work/{name}"
    shown = _run(repo, "show", f"{branch}:{live_path}")
    if shown.returncode == 0:
        fm, _ = parse_frontmatter(shown.stdout)
        status = (fm or {}).get("status")
        if status == "active":
            return "active on branch"
        if status == "proposed":
            return "proposed on branch"
    return f"committed on {branch}"


def list_claims(root):
    data = load_claims(root.repo)
    return {wid: {**claim, "observation": observe(root, wid, claim)} for wid, claim in sorted(data["claims"].items())}


def render_claims(claims):
    if not claims:
        return "no claims\n"
    lines = [f"{wid}: {c['branch']} ({c['worktree']}) · {c['observation']}" for wid, c in claims.items()]
    return "\n".join(lines) + "\n"
