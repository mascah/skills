#!/usr/bin/env bash
# grove run adapter: a headless `claude -p` session that owns its workspace (W-004).
# Usage: grove run CONTRACT -- scripts/adapters/claude-p.sh
# The driver calls this with CONTRACT ATTEMPT_DIR and cwd at the repository root. The adapter
# creates (or resumes) the worktree branch for the contract's work IDs from the exported head,
# runs `grove:work` inside it with the grove plugin loaded, then fills in the tested revision
# and optional test output when the agent left them out. Env: GROVE_MODEL (default sonnet),
# GROVE_PLUGIN_DIR (default: this repository), GROVE_TEST_CMD (optional, run in the worktree).
set -euo pipefail
contract=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
attempt=$(mkdir -p "$2" && cd "$2" && pwd)
plugin=${GROVE_PLUGIN_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}
model=${GROVE_MODEL:-sonnet}
read -r cid head ids < <(python3 -c 'import json,sys; c=json.load(open(sys.argv[1])); print(c["id"], c["checkout"]["head"], "-".join(c["order"]))' "$contract")
wt=.worktrees/$ids
exclude=$(git rev-parse --git-common-dir)/info/exclude
grep -qx '.worktrees' "$exclude" 2>/dev/null || echo '.worktrees' >> "$exclude"
if [ ! -d "$wt" ]; then
  if git show-ref --quiet "refs/heads/$ids"; then git worktree add "$wt" "$ids"; else git worktree add "$wt" -b "$ids" "$head"; fi
fi
prompt="You are running headless under \`grove run\`; no human can answer questions. Your working directory is already the implementation worktree for $ids on branch $ids: do not create or enter another worktree. Run /grove:work $ids and commit everything to this branch.
When finished, write $attempt/result.json in the grove result shape: {\"schema\":1, \"contract\":\"$cid\", \"work\":[\"${ids//-/\",\"}\"], \"outcome\": complete|partial|waiting|blocked|failed, \"tested\":{\"head\":<commit sha you tested>, \"dirty\":false}, \"evidence\":[...], \"findings\":[...], \"next\":\"...\"}.
If you need a human decision or preference, do not guess and do not ask: write a waiting result with \"wait\":{\"on\":\"<what you need>\", \"sources\":[<repo-relative paths that would change when it is answered>]} and stop. If the work already has partial progress on this branch, continue from it instead of starting over."
( cd "$wt" && claude -p "$prompt" --model "$model" --plugin-dir "$plugin" --dangerously-skip-permissions --output-format text ) > "$attempt/claude.txt" 2>&1 || echo "claude exited $?" >> "$attempt/claude.txt"
tested=$(git -C "$wt" rev-parse HEAD)
if [ -n "${GROVE_TEST_CMD:-}" ]; then (cd "$wt" && bash -c "$GROVE_TEST_CMD") > "$attempt/test.txt" 2>&1 || true; fi
python3 - "$attempt" "$tested" <<'EOF'
import json, sys, pathlib
d, tested = pathlib.Path(sys.argv[1]), sys.argv[2]
p = d / "result.json"
if not p.exists():
    sys.exit(0)   # the driver records "exited without result.json"
r = json.loads(p.read_text())
r.setdefault("tested", {}).setdefault("head", tested)
t = d / "test.txt"
if t.exists():
    r.setdefault("evidence", []).append("adapter test command: " + t.read_text().strip().splitlines()[-1][:200])
p.write_text(json.dumps(r, indent=1) + "\n")
EOF
