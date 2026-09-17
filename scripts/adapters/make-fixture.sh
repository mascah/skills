#!/usr/bin/env bash
# Build the W-004 trial fixture: a tiny grove project with one small unit (W-001, mechanical) and one
# that needs a human choice (W-002). Usage: make-fixture.sh DIR
set -euo pipefail
dir=$1
rm -rf "$dir" && mkdir -p "$dir" && cd "$dir"
git init -q && git config user.name fixture && git config user.email fixture@example.com
grove init >/dev/null
cat > docs/grove/brief.md <<'EOF'
---
type: brief
id: brief
status: active
updated: 2026-09-17
focus: W-001
---
## Pitch
A shell greeting tool, used only to exercise grove headless runs.

## Who it's for
The W-004 trial.

## Why
Prove `grove run` with a real harness adapter.

## Constraints
Plain bash, no dependencies. Every script has a runnable check in `test.sh`.

## Not now
Anything beyond greeting.
EOF
cat > docs/grove/work/W-001-hello-script.md <<'EOF'
---
type: work
id: W-001
status: proposed
created: 2026-09-17
updated: 2026-09-17
kind: feature
size: small
scope: []
priority: 1
depends_on: []
---
## Outcome
`./hello.sh NAME` prints `hello, NAME` and `./test.sh` checks it.

## Acceptance
- [ ] `./hello.sh grove` prints exactly `hello, grove`.
- [ ] `./test.sh` exits 0 and fails when hello.sh is broken.

## Evidence

## Next
Write hello.sh and test.sh, run test.sh, record the output.
EOF
cat > docs/grove/work/W-002-greeting-word.md <<'EOF'
---
type: work
id: W-002
status: proposed
created: 2026-09-17
updated: 2026-09-17
kind: feature
size: small
scope: []
priority: 2
depends_on: []
---
## Outcome
`./hello.sh` uses the greeting word the project owner picks instead of `hello`.

## Constraints
The greeting word is the owner's taste. It is not recorded anywhere yet; do not guess it. Ask before implementing.

## Acceptance
- [ ] The owner's chosen word is recorded in this page's Design section.
- [ ] `./hello.sh grove` prints that word followed by `, grove`.

## Evidence

## Next
Obtain the greeting word from the owner, record it under Design, then implement.
EOF
git add -A && git commit -qm fixture
echo "fixture at $dir ($(git rev-parse --short HEAD))"
