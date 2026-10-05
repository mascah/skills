# mascah-skills

A personal engineering skill suite for hobby projects. Shape useful changes,
keep durable intent in git, and implement with meaningful verification. Skills
are independently invocable; setup, specs, plans, tickets and delegation are
optional when the work does not need them. No Grove CLI or upstream plugin is
required.

## Install

Install the whole plugin so shared `references/` ships with `skills/`. Copying
one skill directory alone loses its supporting contracts.

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

## Update or migrate from Grove

Refresh the marketplace and reinstall under the new identity. Existing Grove
project files are user-owned migration inputs: inspect them and preserve useful
intent in the project's normal docs; this plugin does not delete them.

Claude Code (use the scope of the previous installation):

```sh
claude plugin uninstall grove@mascah --scope project
claude plugin marketplace update mascah
claude plugin install mascah-skills@mascah --scope project
```

For subsequent updates use `claude plugin update mascah-skills@mascah`.
Codex:

```sh
codex plugin remove grove@mascah
codex plugin marketplace upgrade mascah
codex plugin add mascah-skills@mascah
```

For subsequent Codex refreshes, upgrade the marketplace and remove/add
`mascah-skills@mascah` to reinstall its cached package. Hermes users disable the
old plugin with `hermes plugins disable grove`, remove only their old Grove
plugin link/install after inspection, and enable the new checkout link. Pulling
updates into that checkout updates its files. Start a new harness session after
updating. An old editable Grove CLI installation is independent and can be
uninstalled separately if no project needs it.

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

A clear bug can go straight to `implement` with its supplied issue body.
A feature can use `shaping` → `to-spec` → `implement` without tracker access.
A spec keeps execution in Delivery; extract a linked plan only when independent
maintenance warrants it. Setup writes one compact workflow file and preserves
unrelated agent instructions on rerun. Existing project paths win.

The shared [routes](references/workflow.md), [artifact owners](references/artifacts.md)
and [execution contract](references/execution.md) explain persistence, authority,
verification and direct/delegated handoffs. [The refactor spec](docs/work/mascah-skills-refactor/spec.md)
records the agreed design; current files and checks establish what has shipped.
[Attribution](ATTRIBUTION.md) identifies adapted sources.

## Develop and release

Python 3.12+ with its standard library is sufficient:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 __init__.py
git diff --check
```

Structural tests include a clean copied distribution and deliberately broken
fixtures. Run [behavior exercises](tests/scenarios.md) in fresh contexts when
skill instructions change; record observed results and limits in
[the verification record](tests/results.md). Structural validation does not
prove agent behavior, live tracker access or Hermes delegation.

Write on an isolated branch/worktree and use Conventional Commits. CI and
lefthook run structural/test/registration checks. Release Please opens the
release PR after integration to main; its simple release updates `version.txt`,
the release manifest and Claude/Codex/Hermes version fields. Review that PR
before releasing. This implementation does not publish or tag a release.
