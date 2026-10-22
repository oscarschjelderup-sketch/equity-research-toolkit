# Phase 4: keep the lead – the monthly routine

- `ROUTINE.md`: six steps on the 2nd of each month – prices, case status and calibration (`oq book monthly`), the
  audit and gate for every case with today's price, new evidence in `docs/research/updates/YYYY-MM.md`, proposed
  `ANALYSE.md` changes on a local branch with the audit and calibration as evidence, and a report in Norwegian.
- oslo-quant (`phase-4-routine`): `oq book monthly` (status table, kill criteria due, calibration, recorded log heads
  that catch a rewritten log), and calibration scored on a common date for the adjusted and quoted series.
- A scheduled Claude task `equity-research-monthly` runs the routine; it never pushes or opens a PR on its own.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
