"""Read-only checks for the shipped skill distribution; Python stdlib only."""
import json
import argparse
from pathlib import Path
import re
import runpy
import sys
from urllib.parse import unquote, urlsplit
from bundle_references import drift


def scalars(text):
    """Parse this repository's intentionally flat YAML scalar metadata.

    Rich YAML is not used by this package. Fail explicitly instead of silently
    treating a nested object, list, or multiline value as a usable skill name.
    """
    values = {}
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        key, separator, raw = line.partition(":")
        if not separator or not re.fullmatch(r"[a-z][a-z-]*", key) or key in values:
            raise ValueError("invalid or duplicate scalar key")
        value = raw.strip()
        if not value or value[0] in "[{|>&*!" or ": " in value or " #" in value:
            raise ValueError("expected a single YAML string scalar")
        if value.startswith('"'):
            value = json.loads(value)
        elif value.startswith("'"):
            if not value.endswith("'"):
                raise ValueError("unclosed quoted scalar")
            value = value[1:-1].replace("''", "'")
        if not isinstance(value, str):
            raise ValueError("expected string")
        values[key] = value
    return values


def headings(text):
    anchors, seen = set(), {}
    for title in re.findall(r"^#{1,6}\s+(.+)$", text, re.M):
        slug = re.sub(r"[^\w\s-]", "", title.lower().replace("`", ""))
        slug = re.sub(r"\s", "-", slug)
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    anchors.update(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)', text))
    return anchors


def validate(root, standalone=False):
    errors = []

    def fail(message):
        errors.append(message)

    def load(path):
        return json.loads((root / path).read_text())

    skill_files = [root / "SKILL.md"] if standalone else sorted((root / "skills").glob("*/SKILL.md"))
    names = {p.parent.name for p in skill_files}
    if not names:
        fail("no skills discovered")
    for directory in (() if standalone else (root / "skills").iterdir()):
        if directory.is_dir() and not (directory / "SKILL.md").is_file():
            fail(f"missing entry point: {directory.name}/SKILL.md")
    for path in skill_files:
        name = path.parent.name
        for bundled in path.parent.rglob('*'):
            if bundled.is_symlink() and not bundled.resolve().is_relative_to(path.parent.resolve()):
                fail(f'{name}: symlink outside skill: {bundled.name}')
        text = path.read_text()
        match = re.match(r"\A---\n(.*?)\n---\n(.+)", text, re.S)
        try:
            if not match:
                raise ValueError("missing YAML frontmatter or body")
            meta = scalars(match[1])
            if set(meta) != {"name", "description"}:
                raise ValueError("expected name and description")
            if meta["name"] != name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
                raise ValueError("name must match directory and lowercase hyphenated format")
            if not 1 <= len(meta["description"]) <= 1024:
                raise ValueError("description length must be 1..1024")
        except (ValueError, KeyError) as exc:
            fail(f"{name}: frontmatter: {exc}")
        if re.search(r"\bgrove(?::[a-z-]+|\s+(?:status|claim|lint|close|context|init|run|export|reconcile|launch|verify-delivery))\b", text, re.I):
            fail(f"{name}: retired Grove runtime instruction")
        if re.search(r"\b(?:grill-with-docs|wayfinder|superpowers:|setup-matt-pocock-skills)\b", text):
            fail(f"{name}: retired or upstream skill dependency")
        for invoked in re.findall(r"\b(?:use|invoke)\s+`([a-z][a-z0-9-]*)`", text, re.I):
            if not standalone and invoked not in names:
                fail(f"{name}: missing skill invocation: {invoked}")

    # Validate local Markdown links across distribution docs, including anchors.
    for path in root.rglob("*.md"):
        if any(part in {".git", ".claude", ".venv", "__pycache__"} for part in path.relative_to(root).parts):
            continue
        text = path.read_text()
        targets = re.findall(r"\]\(([^)]+)\)", text)
        targets += re.findall(r"^\[[^\]]+\]:\s*(\S+)", text, re.M)
        for raw in targets:
            target = raw.strip()
            if target.startswith("<"):
                target = target.split(">", 1)[0][1:]
            else:
                target = target.split(' "', 1)[0]
            url = urlsplit(target)
            if url.scheme in {"https", "http", "mailto"}:
                continue
            resolved = (path.parent / unquote(url.path)).resolve() if url.path else path
            boundary = root
            if not standalone and path.is_relative_to(root / 'skills'):
                boundary = root / 'skills' / path.relative_to(root / 'skills').parts[0]
            if url.scheme or not resolved.is_relative_to(boundary):
                fail(f"{path.relative_to(root)}: link outside skill or outside package: {target}")
            elif not resolved.exists():
                fail(f"{path.relative_to(root)}: missing link: {target}")
            elif url.fragment and resolved.is_file() and resolved.suffix == ".md":
                if unquote(url.fragment) not in headings(resolved.read_text()):
                    fail(f"{path.relative_to(root)}: missing anchor: {target}")

    if standalone:
        return errors, names
    try:
        errors.extend(drift(root))
    except (OSError, ValueError) as exc:
        fail(f'reference drift: {exc}')

    try:
        version = (root / "version.txt").read_text().strip()
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?", version):
            fail("invalid version.txt")
        manifests = [load(".claude-plugin/plugin.json"), load(".codex-plugin/plugin.json"),
                     scalars((root / "plugin.yaml").read_text())]
        for manifest in manifests:
            if not isinstance(manifest, dict):
                raise ValueError("plugin manifest must be an object")
            if manifest.get("name") != "mascah-skills":
                fail("plugin identity must be mascah-skills")
            if manifest.get("version") != version:
                fail("plugin version differs from version.txt")
        if manifests[1].get("skills") != "./skills/":
            fail("Codex skills discovery must use ./skills/")
        for file in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
            marketplace = load(file)
            if not isinstance(marketplace, dict):
                raise ValueError(f"{file}: marketplace must be an object")
            if marketplace.get("name") != "mascah" or len(marketplace.get("plugins", [])) != 1:
                fail(f"{file}: expected mascah marketplace and one plugin")
            entry = marketplace["plugins"][0]
            if entry.get("name") != "mascah-skills":
                fail(f"{file}: expected mascah-skills entry")
            expected = "./" if file.startswith(".claude") else {"source": "local", "path": "./"}
            if entry.get("source") != expected:
                fail(f"{file}: plugin source must resolve to package root")
        if load(".release-please-manifest.json").get(".") != version:
            fail("release manifest version differs from version.txt")
        extras = load("release-please-config.json")["packages"]["."]["extra-files"]
        version_targets = {".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "plugin.yaml"}
        seen_targets = set()
        for entry in extras:
            target = entry if isinstance(entry, str) else entry["path"]
            seen_targets.add(target)
            if not (root / target).is_file():
                fail(f"missing release target: {target}")
            if target in version_targets:
                expected_type = "yaml" if target == "plugin.yaml" else "json"
                if not isinstance(entry, dict) or entry.get("type") != expected_type or entry.get("jsonpath") != "$.version":
                    fail(f"invalid release updater: {target} must update $.version as {expected_type}")
        if not version_targets.issubset(seen_targets):
            fail("release version targets incomplete")
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError) as exc:
        fail(f"manifest metadata: {exc}")

    try:
        entry = runpy.run_path(str(root / "__init__.py"))
        registered = {}

        class Context:
            def register_skill(self, name, path):
                if name in registered:
                    fail(f"Hermes duplicate skill: {name}")
                registered[name] = path

        entry["register"](Context())
        if names != entry["EXPECTED_SKILLS"] or set(registered) != names:
            fail("Hermes expected/discovered inventory mismatch")
        for name, path in registered.items():
            if path.resolve() != root / "skills" / name / "SKILL.md" or not path.is_file():
                fail(f"Hermes invalid registration: {name}")
    except (OSError, KeyError, TypeError, ValueError) as exc:
        fail(f"Hermes discovery: {exc}")
    for retired in ("cli", "templates", "grove.toml", "scripts/adapters", "docs/grove"):
        if (root / retired).exists():
            fail(f"retired distribution path: {retired}")
    return errors, names


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', nargs='?', type=Path)
    parser.add_argument('--skill', type=Path, help='Validate one isolated skill folder')
    args = parser.parse_args()
    package = (args.skill or args.package or Path(__file__).resolve().parents[1]).resolve()
    try:
        problems, skills = validate(package, standalone=args.skill is not None)
    except (OSError, ValueError) as exc:
        problems, skills = [str(exc)], set()
    for problem in problems:
        print(f"ERROR: {problem}")
    print(f"{len(skills)} {'skill' if args.skill else 'skills'}; {len(problems)} errors")
    raise SystemExit(bool(problems))
