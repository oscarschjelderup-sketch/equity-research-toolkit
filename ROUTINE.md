# The monthly routine

Runs on the 2nd of every month (scheduled Claude task `equity-research-monthly`, 09:00 local; it runs when the
desktop app is open, or on the next launch). Each step leaves a file, so a missed month is visible.

| Step | What | Command / output |
|---|---|---|
| 1 | Prices | `oq record --raw` (oslo-quant) |
| 2 | Status of every case in the research book: price vs target, bear and bull; kill criteria due after the month's reports; calibration; the judgement log's head hash recorded | `oq book monthly` → `~/osloquant-home/monthly/YYYY-MM.md` |
| 3 | Audit every case: the 30 failure modes and the reverse-DCF gate, with today's price | `python model_builder/audit.py <xlsx> <map> <case> --price-now P` and `case_gate.py` |
| 4 | New evidence: rankings (Kapital, Prospera, Extel), new public initiations or analyses on Oslo Børs names, documented analyst errors and Finanstilsynet decisions in the month | `docs/research/updates/YYYY-MM.md`, sourced, with "Det som ikke lot seg finne offentlig" |
| 5 | Proposed changes to `ANALYSE.md`, only where the new evidence or the calibration report supports them | a local branch `monthly-YYYY-MM` with `docs/pr/monthly-YYYY-MM.md`; evidence = the audit output and the calibration report |
| 6 | Report to Oscar (Norwegian): what changed, what is due, what needs a decision | the task's final message |

Rules: nothing is pushed and no pull request is opened without Oscar's explicit yes; the judgement log is never
edited (a changed view is a new row, written by Oscar with `oq book add` or `oq book sync`); kill checks are logged
by Oscar with `oq book kill`; the paper accounts are not touched; private cases and the research book stay out of
public repositories; no invented numbers, sources for every claim, structure not wording.
