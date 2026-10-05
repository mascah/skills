# mascah-skills

A personal engineering skill suite for hobby projects. Shape useful changes,
keep durable intent in git, and implement with meaningful verification. Skills
are independently invocable; setup, specs, plans, tickets and delegation are
optional when the work does not need them. Each skill works independently of
upstream plugins.

## Install

Each published skill folder contains its supporting references and works alone.
Install selected skills with [the skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add mascah/skills --skill implement --agent codex
```

Or install the full plugin through a supported harness below. Helper skills are
optional; each entry point includes guidance for operating without them.

Claude Code:

```sh
claude plugin marketplace add mascah/skills
claude plugin install mascah-skills@mascah --scope project
```

Codex:

```sh
codex plugin marketplace add mascah/skills
codex plugin add mascah-skills@mascah
```

Hermes (local checkout; create the parent plugins directory if needed):

```sh
ln -s /path/to/this/repo ~/.hermes/plugins/mascah-skills
hermes plugins enable mascah-skills
```

Hermes registers `mascah-skills:<skill>` through the retained Python entry
point. Runtime delegation and scheduling belong to the caller's configuration.
Installation guidance follows [Claude's plugin docs](https://code.claude.com/docs/en/discover-plugins),
[OpenAI's plugin packaging docs](https://developers.openai.com/plugins/build/plugins),
and [Hermes's plugin docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins).
Claude/Codex syntax was also checked against local CLI help on 2026-10-05.
Personal installation is separate from repository validation.

## Use

Invoke skills using the harness's skill picker or namespaced skill command.
For example in Claude Code, `/mascah-skills:shaping`; in Hermes,
`skill_view("mascah-skills:shaping")`. In Codex, select the installed skill or
request it by name. No global hook runs this entire workflow.

| Skill | Use |
| --- | --- |
| `setup-mascah-skills` | Optionally record paths, tracker and execution preferences |
| `shaping` | Clarify intent, alternatives and acceptance |
| `domain-modeling` | Resolve terminology and consequential decisions |
| `to-spec` | Save agreed intent locally |
| `implement` | Deliver a direct task, issue, spec or slice |
| `tdd` | Meaningful tests through observable interfaces |
| `code-review` | Review changes against scope and conventions |
| `codebase-design` | Design cohesive modules and useful interfaces |
| `to-tickets` | Draft or publish selected Delivery slice assignments |
| `triage` | Investigate requests and check actionable readiness |
| `implement-spec` | Deliver and integrate whole-spec acceptance |
| `discovery` | Investigate ideas, with continue/defer/abandon/answer outcomes |
| `improve-codebase-architecture` | Investigate real architectural friction |
| `research` | Gather primary evidence for a bounded question |
| `prototype` | Run clearly disposable design experiments |

A clear bug can go straight to `implement` with its supplied issue body.
A feature can use `shaping` → `to-spec` → `implement-spec` without tracker access.
For independent assignment, `to-tickets` creates concise scope pointers and
`triage` checks readiness. Ticket creation does not apply `ready-for-agent`;
closed/rejected blockers and unmerged work do not establish prerequisites.
A spec keeps execution in Delivery; extract a linked plan only when independent
maintenance warrants it. Setup writes one compact workflow file and preserves
unrelated agent instructions on rerun. Existing project paths win.

An uncertain idea can go through `discovery`, use `research` or `prototype`,
and stop with evidence that it should be abandoned. Architecture investigation
compares observed costs and routes selected improvements into `shaping`; it
does not automatically refactor a project.

[The canonical workflow guide](references/workflow.md) explains the complete
system and links to each single maintained rule/procedure owner. Skills carry
only relevant focused references, with conditional loading for tracker/delegation
work; the guide itself is not copied into their installations.
[Attribution](ATTRIBUTION.md) identifies adapted sources.

## Develop and release

Python 3.12+ with its standard library is sufficient:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 __init__.py
git diff --check
```

The complete workflow remains in `references/workflow.md`, linking focused
rule owners and activity procedures. Edit a reusable rule only in its owning
root reference, or activity-specific guidance in its SKILL.md. The full guide
is not bundled into individual skills. Then run
`python3 scripts/bundle_references.py` and commit its generated copies under
`skills/<name>/references/` together with the source. Those directories are
generated-only; skill-specific authored support can live elsewhere inside its
skill folder. The helper follows local links and bundles only required files.
It is development tooling; users and installers need no build step.

Validation rejects copy drift and links escaping an individual skill. To check
one installed folder, run `python3 scripts/validate.py --skill /path/to/skill`.
Structural tests include every skill copied alone, a clean plugin distribution
and deliberately broken fixtures. Run [behavior exercises](tests/scenarios.md) in fresh contexts when
skill instructions change; record observed results and limits in
[the verification record](tests/results.md). Structural validation does not
prove agent behavior, live tracker access or Hermes delegation.

Write on an isolated branch/worktree and use Conventional Commits. CI and
lefthook run structural/test/registration checks. Release Please opens the
release PR after integration to main; its simple release updates `.github/version.txt`,
the `.github/.release-please-manifest.json` and Claude/Codex/Hermes version fields.
Configuration lives in `.github/release-please-config.json`; package/updater paths
still resolve from the repository root. Review that PR
before releasing. This implementation does not publish or tag a release.

The personal suite version baseline is 0.1.0. For this reset, `last-release-sha`
in the Release Please config anchors commit collection at the last integrated suite revision. Remove that
temporary field after the first successful new release PR is merged, restoring
automatic release-boundary discovery. Old remote tags/releases are not removed by
changing version files or force-pushing a branch. See the
[Release Please reset option](https://github.com/googleapis/release-please/blob/main/docs/manifest-releaser.md).
