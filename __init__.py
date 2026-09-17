"""Hermes Agent plugin entry. Registers skills/*/SKILL.md as grove:<name>."""
from pathlib import Path

SKILLS = Path(__file__).resolve().parent / "skills"


def register(ctx):
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        ctx.register_skill(skill_md.parent.name, skill_md)


if __name__ == "__main__":
    seen = {}
    register(type("Ctx", (), {"register_skill": lambda self, n, p: seen.__setitem__(n, p)})())
    assert set(seen) == {"setup", "explore", "shape", "work", "close", "curate"}, seen
    assert all(p.is_file() for p in seen.values())
    print("ok", sorted(seen))
