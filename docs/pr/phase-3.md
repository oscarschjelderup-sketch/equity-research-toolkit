# Phase 3: make judgement measurable

Two repositories, one branch each (`phase-3-measurable`).

**oslo-quant**
- `osloquant/judgements.py` + `oq book sync | add | kill | verify | calibrate`: an append-only, hash-chained log of
  every call (date, call price, rating, 12-month target, bear/base/bull, scenario probabilities, kill criteria) and
  every kill-criterion check; any edited, removed or reordered row is found by `verify`. The data is private
  (`~/osloquant-home/judgements.jsonl`).
- Calibration report: total return from the call price incl. dividends, excess over OSEBX, direction hit rate,
  price vs target, bear-bull band, three-way Brier score after the horizon, kill checks breached and acted on;
  provisional calls reported apart. First two calls logged (the two research-book cases).
- `oq signals publish` → `site/signals.html`: the public scorecard says plainly that no technical buy signal pays after
  a 0.5 % round trip, with the numbers and the caveats.
- Tests: 288 passed.

**Equity Research Toolkit**
- `blindtest/`: form builder with opaque ids and a separate key, scorer, fairness warnings; SATS spec with our case
  and a public-data consensus summary; the broker-argument document is left for the organiser (paywalled sources).
- The reverse-DCF gate in CI shipped with phase 2 (`case_gate.py`).
- Tests: 16 passed (13 + 3 blind-test).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
