# Attribution and retained rationale

This is an independently maintained personal suite, not an upstream plugin
fork or a runtime dependency on either source.

- [Matt Pocock skills](https://github.com/mattpocock/skills), inspected at
  `4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d`: adapted ideas from setup,
  domain-modeling, to-spec, implement, tdd, code-review, codebase-design,
  grilling/grill-with-docs, to-tickets, triage, implement-spec, wayfinder,
  research, prototype and improve-codebase-architecture. In particular:
  domain language, observable tests, cohesive interfaces, useful questions and
  vertical delivery. Publication defaults, mandatory tracker scaffolds,
  interviews and orchestration were replaced by this suite's contracts.
- [Superpowers](https://github.com/obra/superpowers), package `6.4.2`: adapted
  selective brainstorming, planning, worktree, test and truthful verification
  disciplines. This suite does not require its approval gates, model policy or
  controller/worker fan-out.
- Repository history at `045a78f`: retained the shared-index isolation rationale
  in [an ADR](docs/adr/isolated-writing-sessions.md), scope/mandate boundaries in
  [workflow](references/workflow.md), and trustworthy completion, integrated
  interaction checks and recovery lessons in [execution](references/implementation.md).
  The former CLI, schema, work records, controller loop and adapters are retired.
  Old source and evidence remain available through git history rather than an
  archive in the current distribution.

The former W-016 launch acceptance trial is superseded by application removal;
it was not successfully completed by this refactor. W-007's proposed evaluation
spike never ran here as that spike. Its useful idea is represented by the new
fixture exercises and their separately recorded results. Historical changelog
entries describe their original releases and are preserved.

Applicable upstream MIT notices follow.

## Matt Pocock

MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Superpowers

MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
