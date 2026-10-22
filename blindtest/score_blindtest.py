"""Aggregate blind-test answers: mean score per criterion and author, mean rank, how often each author ranked first.

    python score_blindtest.py out/sats.key.json answers/*.json

Answers whose test id does not match the key, or that reference unknown documents, are skipped with a warning.
With fewer than five judges the result is anecdote, and the report says so.
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path


def score(key: dict, answers: list[dict]) -> dict:
    ids = key["key"]
    used, skipped = [], []
    for a in answers:
        if a.get("test") != key["test"] or set(a.get("ranks", {})) != set(ids):
            skipped.append(a.get("judge", "?"))
            continue
        used.append(a)
    out = {"test": key["test"], "judges": len(used), "skipped": skipped, "authors": {}}
    for oid, author in ids.items():
        crit: dict[str, list[float]] = {}
        for a in used:
            for c, v in a["scores"].get(oid, {}).items():
                if v is not None:
                    crit.setdefault(c, []).append(v)
        ranks = [a["ranks"][oid] for a in used]
        out["authors"][author] = {
            "mean_rank": statistics.mean(ranks) if ranks else None,
            "first_place": sum(r == 1 for r in ranks),
            "mean_score": statistics.mean([v for vs in crit.values() for v in vs]) if crit else None,
            "by_criterion": {c: statistics.mean(v) for c, v in crit.items()},
        }
    out["note"] = ("fewer than five judges: anecdote, not evidence" if len(used) < 5 else "")
    return out


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    key = json.loads(Path(argv[0]).read_text(encoding="utf8"))
    answers = [json.loads(Path(p).read_text(encoding="utf8")) for p in argv[1:]]
    res = score(key, answers)
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
