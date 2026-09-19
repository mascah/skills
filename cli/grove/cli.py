"""Command line entry point. The only module that prints or exits."""
import argparse
import json
import sys
from pathlib import Path
from . import __version__
from .claims import Owned, acquire, list_claims, release, render_claims
from .close import close, render_receipt
from .context import PHASES, context, render_context
from .contract import export, load_contract, reconcile, render_receipt as render_reconcile, stale
from .find import find
from .init import init, upgrade
from .launch import LaunchBlocked, launch
from .lint import lint
from .pages import GroveError, load_root
from .run import EXIT, render_run, run
from .status import render_status, status
from .work import batch, render_batch


def build_parser():
    p = argparse.ArgumentParser(prog="grove", description="Repo-local project knowledge for coding agents.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="set up this repo (safe to rerun)")
    sub.add_parser("upgrade", help="upgrade the schema declaration; preserve project content")
    sub.add_parser("lint", help="check knowledge structure; exit 1 on errors")
    s = sub.add_parser("status", help="what applies now and what is next")
    s.add_argument("--json", action="store_true")
    b = sub.add_parser("batch", help="assess selected work for one shared implementation")
    b.add_argument("work", nargs="+")
    b.add_argument("--json", action="store_true")
    c = sub.add_parser("context", help="scoped context for one work unit")
    c.add_argument("--work", required=True)
    c.add_argument("--phase", choices=PHASES, default="implement")
    c.add_argument("--budget", type=int, default=6000)
    c.add_argument("--json", action="store_true")
    f = sub.add_parser("find", help="search live knowledge (history excluded)")
    f.add_argument("query")
    f.add_argument("--history", action="store_true")
    f.add_argument("--type", dest="type_")
    f.add_argument("--regex", action="store_true")
    cl = sub.add_parser("close", help="close a done work unit into history")
    cl.add_argument("work")
    cm = sub.add_parser("claim", help="acquire, release or take over work claims")
    cm.add_argument("work", nargs="+")
    cm.add_argument("--release", action="store_true", help="release claims owned by this checkout")
    cm.add_argument("--take", action="store_true", help="re-acquire regardless of current owner")
    cm.add_argument("--json", action="store_true")
    cs = sub.add_parser("claims", help="list claims with branch/worktree observations")
    cs.add_argument("--json", action="store_true")
    la = sub.add_parser("launch", help="print one paste-ready /goal message for one or more work units")
    la.add_argument("work", nargs="+")
    ex = sub.add_parser("export", help="export a prepared selection as a versioned execution contract")
    ex.add_argument("work", nargs="+")
    ex.add_argument("--out", help="write the contract JSON here instead of stdout")
    rc = sub.add_parser("reconcile", help="record an executor result on its work pages; exit 2 if inputs changed")
    rc.add_argument("result")
    rc.add_argument("--contract", required=True)
    rn = sub.add_parser("run", help="run one executor attempt against a contract: grove run CONTRACT [options] -- ADAPTER...")
    rn.add_argument("contract")
    rn.add_argument("--state", help="run directory (default .grove/runs/<contract id>)")
    rn.add_argument("--max-attempts", type=int, default=3)
    rn.add_argument("--timeout", type=float, help="seconds before an attempt is killed")
    return p


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    adapter = []
    if "--" in argv:   # everything after -- is the run adapter command, untouched by argparse
        i = argv.index("--")
        adapter, argv = argv[i + 1:], argv[:i]
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "init":
            for a in init(Path.cwd()):
                print(a)
            return 0
        root = load_root(Path.cwd())
        if args.cmd == "upgrade":
            print(upgrade(root))
            return 0
        if args.cmd == "batch":
            d = batch(root, args.work)
            print(json.dumps(d, indent=2) if args.json else render_batch(d))
            return 2 if d["blockers"] else 0
        if args.cmd == "lint":
            errors, warnings = lint(root)
            for e in errors:
                print(f"error: {e}")
            for w in warnings:
                print(f"warning: {w}")
            print(f"lint: {len(errors)} errors, {len(warnings)} warnings")
            return 1 if errors else 0
        if args.cmd == "status":
            d = status(root)
            print(json.dumps(d, indent=2) if args.json else render_status(d), end="" if not args.json else "\n")
            return 0
        if args.cmd == "context":
            d = context(root, args.work, args.phase, args.budget)
            print(json.dumps(d, indent=2) if args.json else render_context(d))
            return 2 if d["errors"] else 0
        if args.cmd == "find":
            for line in find(root, args.query, args.history, args.type_, args.regex):
                print(line)
            return 0
        if args.cmd == "close":
            print(render_receipt(close(root, args.work)), end="")
            return 0
        if args.cmd == "claim":
            if args.release:
                if args.take:
                    raise GroveError("--release and --take are mutually exclusive")
                d = {wid: True for wid in release(root, args.work)}
                verb = "released"
            else:
                d = acquire(root, args.work, take=args.take)
                verb = "took" if args.take else "claimed"
            if args.json:
                print(json.dumps(d, indent=2))
            else:
                print("\n".join(f"{verb} {wid}" for wid in d) or "nothing to release")
            return 0
        if args.cmd == "claims":
            d = list_claims(root)
            print(json.dumps(d, indent=2) if args.json else render_claims(d), end="" if not args.json else "\n")
            return 0
        if args.cmd == "launch":
            try:
                msg = launch(root, args.work)
            except LaunchBlocked as exc:
                print("\n".join(exc.blockers), file=sys.stderr)
                return 2
            sys.stdout.write(msg)
            return 0
        if args.cmd == "export":
            c = export(root, args.work)
            if args.out:
                Path(args.out).write_text(json.dumps(c, indent=1) + "\n")
                print(f"exported {', '.join(c['order'])} at {c['checkout']['head'][:12]} as contract {c['id'][:12]}: {args.out}")
            else:
                print(json.dumps(c, indent=1))
            return 0
        if args.cmd == "reconcile":
            c = load_contract(args.contract)
            try:
                r = json.loads(Path(args.result).read_text())
            except (OSError, ValueError) as exc:
                raise GroveError(f"cannot read result {args.result}: {exc}")
            changed = stale(root, c)
            if changed:
                print("grove: contract inputs changed since export; re-export before accepting this result:\n" + "\n".join(changed), file=sys.stderr)
                return 2
            print(render_reconcile(reconcile(root, c, r)), end="")
            return 0
        if args.cmd == "run":
            r = run(root, Path(args.contract), adapter, args.state, args.max_attempts, args.timeout)
            print(render_run(r), end="")
            return EXIT[r["outcome"]]
    except Owned as exc:
        print(f"grove: {exc}", file=sys.stderr)
        return 4
    except GroveError as exc:
        print(f"grove: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
