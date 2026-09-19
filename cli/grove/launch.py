"""W-016: one paste-ready /goal message for one or more work units."""
from .work import batch


class LaunchBlocked(Exception):
    """Raised when batch() reports external blockers; distinct from GroveError so the CLI exits 2, not 1."""

    def __init__(self, blockers):
        self.blockers = blockers
        super().__init__("; ".join(blockers))


def launch(root, ids):
    d = batch(root, ids)
    if d["blockers"]:
        raise LaunchBlocked(d["blockers"])
    order = ", ".join(d["order"])
    return (
        f"/goal {order} are finished in this repo; reach that by running the grove:work skill for {order} "
        "on a worktree branch. Finished: grove status lists each unit under Recent, grove lint reports 0 "
        "errors, every commit sits on the worktree branch with a Conventional Commits subject and a Refs: "
        "footer, and the final message tells the human how to merge. Parked, as an alternative terminal "
        "state per unit: grove:work's bounded fix rounds ran out, or an acceptance box needs a human "
        "judgment, and that unit's Next names the open finding or the judgment. Never write code, run tests "
        "or debug in this session; dispatch per the skill. After compaction or interruption, resume from "
        "grove status and .grove-run/ledger.md; do not restart the run.\n"
    )
