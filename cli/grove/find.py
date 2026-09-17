"""ripgrep over live knowledge, each hit prefixed with type/id/status."""
import shutil
import subprocess
from pathlib import Path
from .pages import GroveError, Page


def find(root, query, history=False, type_=None, regex=False):
    if shutil.which("rg") is None:
        raise GroveError("grove find needs ripgrep (rg) on PATH")
    cmd = ["rg", "-n", "-i", "--no-heading", "--color", "never", "-g", "*.md"]
    if not history:
        cmd += ["-g", "!**/history/**"]
    if not regex:
        cmd.append("--fixed-strings")
    cmd += ["-e", query, str(root.knowledge)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode not in (0, 1):
        raise GroveError(proc.stderr.strip())
    out, cache = [], {}
    for raw in proc.stdout.splitlines():
        path, line, text = raw.split(":", 2)
        p = Path(path)
        page = cache.get(p) or cache.setdefault(p, Page(p, root))
        # Handle non-page files (files without frontmatter)
        if not page.fm:
            if type_ and type_ != "file":
                continue
            out.append(f"file {page.basename} - {root.rel(p)}:{line}: {text.strip()}")
        else:
            if type_ and page.type != type_:
                continue
            out.append(f"{page.type} {page.id} {page.status} {root.rel(p)}:{line}: {text.strip()}")
    return out
