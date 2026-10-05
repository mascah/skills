"""Hermes entry: register skills/*/SKILL.md as mascah-skills:<name>."""
from pathlib import Path

SKILLS = Path(__file__).resolve().parent / "skills"
EXPECTED_SKILLS = {
    "setup-mascah-skills", "shaping", "domain-modeling", "to-spec",
    "implement", "tdd", "code-review", "codebase-design",
    "to-tickets", "triage", "implement-spec",
    "discovery", "improve-codebase-architecture", "research", "prototype",
}


def register(ctx):
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        ctx.register_skill(skill_md.parent.name, skill_md)


if __name__ == "__main__":
    seen = {}
    register(type("Ctx", (), {"register_skill": lambda self, n, p: seen.__setitem__(n, p)})())
    assert set(seen) == EXPECTED_SKILLS, seen
    assert all(p.is_file() for p in seen.values())
    print("ok", sorted(seen))
