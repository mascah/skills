"""Bundle canonical support files into committed, standalone skill folders."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def local_links(text):
    targets = re.findall(r'\]\(([^)]+)\)', text)
    targets += re.findall(r'^\[[^\]]+\]:\s*(\S+)', text, re.M)
    for raw in targets:
        raw = raw.strip()
        raw = raw.split('>', 1)[0][1:] if raw.startswith('<') else raw.split(' "', 1)[0]
        target = urlsplit(raw)
        if not target.scheme and target.path:
            yield unquote(target.path)


def bundles(root):
    """Return each skill's required canonical files, including transitive links."""
    canonical = (root / 'references').resolve()
    result = {}
    for entry in sorted((root / 'skills').glob('*/SKILL.md')):
        needed = {}
        pending = [canonical / link[len('references/'):] for link in local_links(entry.read_text())
                   if link.startswith('references/')]
        while pending:
            source = pending.pop().resolve()
            if not source.is_relative_to(canonical) or not source.is_file():
                raise ValueError(f'missing or escaping canonical reference: {source}')
            relative = source.relative_to(canonical)
            if relative in needed:
                continue
            needed[relative] = source.read_bytes()
            for link in local_links(source.read_text()):
                pending.append(source.parent / link)
        result[entry.parent] = needed
    return result


def drift(root):
    errors = []
    for skill, needed in bundles(root).items():
        directory = skill / 'references'
        existing = {p.relative_to(directory): p for p in directory.rglob('*') if p.is_file()}
        for name, content in needed.items():
            if name not in existing or existing[name].read_bytes() != content:
                errors.append(f'reference drift: {skill.name}/references/{name}; run python3 scripts/bundle_references.py')
        for name in existing.keys() - needed.keys():
            errors.append(f'unused generated reference: {skill.name}/references/{name}')
    return errors


def generate(root):
    # These skill references directories are generated-only; author skill-specific
    # support elsewhere in the skill, and canonical shared guidance at repo root.
    plans = bundles(root)
    # Refuse before any mutation: generated files must never redirect writes.
    for skill, needed in plans.items():
        directory = skill / 'references'
        for path in [directory, *directory.rglob('*')]:
            if path.is_symlink():
                raise ValueError(f'generated reference symlink is not allowed: {path}')
        for name in needed:
            if not (directory / name).resolve().is_relative_to(skill.resolve()):
                raise ValueError(f'generated reference escapes skill: {name}')
    for skill, needed in plans.items():
        directory = skill / 'references'
        for path in directory.rglob('*'):
            if path.is_file() and path.relative_to(directory) not in needed:
                path.unlink()
        for name, content in needed.items():
            destination = directory / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists() or destination.read_bytes() != content:
                destination.write_bytes(content)
    print('Bundled references for standalone skills')


if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).resolve().parents[1]
    generate(root)
