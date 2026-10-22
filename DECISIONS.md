# Decisions

One entry per decision: date, what, why, alternatives considered. Newest last. The mission (Oscar, 22 Oct 2026):
make the toolkit and oslo-quant the best analysis setup one person can have for Oslo Børs, with every judgement
logged so it can be measured. Rules: no invented numbers (estimates marked EST), sources for every "best
practice" claim, structure not wording from other analysts, no push without an explicit yes, private cases and
the research book stay out of public repositories.

## 2026-10-22 – Working method

- **One branch per phase** (`phase-1-research`, `phase-2-rules`, `phase-3-measurable`, `phase-4-routine`). The
  mission asks for one pull request per phase *and* no push without an explicit yes. The two are reconciled by
  committing each phase on its own branch with the PR description in `docs/pr/phase-N.md`; the PR is opened only
  after Oscar says yes to the push.
- **Phase 1 runs as four parallel research agents** (rankings; report structure; documented errors; the craft),
  each writing one file in `docs/research/` with a source for every claim and a section "Det som ikke lot seg finne
  offentlig". Paywalled sources (Bloomberg, FactSet, Infront, broker portals, Kapital's full ranking tables) are
  named as such, not reconstructed.
- **Copyright:** the research notes describe the structure of analyst reports (sections, order, lengths, what is
  quantified) and paraphrase arguments; no report text is reproduced beyond short attributed quotes.
- **No self-assessment of quality.** Whether a case is good is decided by the calibration report (phase 3) and
  blind judges Oscar recruits, not by the tool's author.

## 2026-10-22 – Phase 3 built ahead of phases 1-2 where it does not depend on the research

- **Judgement log lives in oslo-quant, data stays private.** Code: `osloquant/judgements.py` (public repo); data:
  `~/osloquant-home/judgements.jsonl` (private, like the research book). Append-only JSON lines, each row with the
  SHA-256 of its content and of the previous row. Alternative rejected: a git branch per log (public by default)
  and a database (edits are silent). The chain makes edits visible, not impossible; the head hash is printed on
  every write and recorded by the monthly routine (phase 4) so a rewritten file can be spotted against it.
- **What a judgement is:** date, call price, rating (BUY/HOLD/SELL), 12-month target, bear/base/bull values,
  scenario probabilities (must sum to 1; the target must lie between bear and bull), kill criteria, thesis. A
  changed view is a new row. Kill checks are their own rows (criterion, breached, action).
- **Calibration metrics:** total return from the *call price* (not that day's close) times the dividend factor of
  the adjusted series; excess over OSEBX; direction = sign of excess for BUY/SELL, within ±10 % for HOLD; price
  vs target; inside the bear-bull band; three-way Brier score of the scenario nearest the outcome, only after the
  horizon. Calls younger than 12 months are "provisional" and reported separately – they are not evidence.
- **First two rows logged 22 Oct 2026**, one per research-book case; the rows, their figures and the head hash
  stay in `~/osloquant-home/judgements.jsonl` (private).
- **Case gate thresholds** (`model_builder/case_gate.py`, tested in CI on the example and SATS workbooks): the
  reverse DCF must be solved, at least one market-implied driver (final-year EBIT margin or revenue CAGR) must
  differ from ours by ≥ 1.0pp, and |DCF/price − 1| ≥ 10 %. 1pp is the smallest gap that moves value by more than
  the sensitivity table's half-step (≈ NOK 4/share per pp of margin in both cases); 10 % matches the toolkit's
  BUY/SELL thresholds. Both are provisional until the phase 1-2 research says what top analysts use.
- **Blind test design:** documents under opaque ids, order shuffled per judge (seeded by initials), the key in a
  separate file never sent to judges (`*.key.json` git-ignored), fairness warnings for word counts outside ±25 %,
  differing sections or broker names. Fewer than five judges is reported as anecdote. Specs for private cases
  are git-ignored.
- **Public signal page:** `site/signals.html` in oslo-quant states that no buy signal pays after a 0.5 % round trip,
  with the scorecard, and the caveats (survivorship, overlapping windows inflate t-statistics).

## 2026-10-22 – Phase 2: rules and checks

- **ANALYSE.md is the rulebook**; every rule cites the research note, source, study or case behind it. English,
  like the rest of the repository.
- **The 30 failure modes run in Python, not as new Excel check rows** (`model_builder/audit.py`). Reason: they need
  the case's META (sector, guidance, conflicts, reasons) and must run in CI without Excel; adding 30 rows to the
  Checks sheet would change the cell map of every committed workbook. `verify_dcf.py` prints the audit when
  `EQR_CASE` is set; `stress_test.py` ends with research-driven stresses from a fresh copy of the workbook.
- **Six statuses** – PASS, WARN, FLAG, FAIL, MISSING, N/A, plus JUSTIFIED. A missing input is MISSING, never PASS.
  A judgement flag clears only with a written reason in `META['reasons']`, which keeps the judgement on the record.
- **Thresholds** (proposals from 03 §5 unless sourced): real CAGR 20 % (Base Rate Book: 18 % of small firms reach it
  over ten years), bear ≥ 25 % below base and growth spread ≥ 5pp, final margin ≤ historical max + 2pp, RONIC/WACC
  warn 1.5x / flag 2.0x, TV share 80/90 %, commodity deck ±10 % vs forwards, consensus ±2 %, price −25 % or model
  > 120 days, TSR Ke + 15/40pp, NWC/sales −5pp (or −1pp in a growth year), D/V ±5pp, ERP 4-6 % and size + specific
  ≤ 3pp (PwC/FFN 2025), exit vs Gordon ±25 %, DCF weight ≥ 50 %, balance sheet ≤ 120 days.
- **NWC release rule refined after the first run:** a business with negative working capital (SATS: prepaid
  memberships) releases cash as it grows at a stable ratio; only a falling NWC/sales ratio is flagged.
- **Margin-reversion stress uses the last three actual years**, not the full history: SATS's history includes the
  pandemic years 2020-21 and gave a meaningless NOK 1.7 per share. Result: SATS NOK 30.5 – SELL; the private case also turns SELL.
- **META reasons for SATS (public) and the private case (git-ignored data module)** are taken from the cases' own
  documented rationale and labelled so; the conflicts block is left empty for the author. B30 disclosures are filled
  in META; showing them on a disclosure slide is template work for the next deck build.
- **The reverse-DCF case gate moves into phase 2** (it is rule 1.3 of ANALYSE.md and its test sits in the same test
  file as the audit test).
- **Banks:** the FCFF template does not apply (04 R35); a bank template is listed as future work, not built.

## 2026-10-22 – Phase 4: the monthly routine

- **A scheduled Claude task, not a Windows task:** step 4 (new rankings, reports, errors) needs web research and
  judgement, which a script cannot do. The numeric steps are commands (`oq book monthly`, `audit.py`, `case_gate.py`)
  so the task only orchestrates and writes. It runs on the 2nd of the month at 09:00 local time (the 1st can be a
  holiday; the previous month's data is complete by then) and only while the desktop app is open – a missed month
  shows as a missing `monthly/YYYY-MM.md`.
- **Proposals, not changes:** the task may edit `ANALYSE.md` only on a local branch `monthly-YYYY-MM`; it never
  pushes, never opens a PR and never writes to the judgement log or the research book.
- **Recorded heads:** `oq book monthly` appends the log's head hash to `judgements-heads.txt`; a later check fails if
  any recorded head no longer matches its row – this catches a log rewritten as a fresh, internally valid chain.
- **Calibration on a common date:** returns come from the adjusted series; the quoted series is used only when it
  has the same date (it is recorded on request and lagged by three sessions on 22 Oct, which put SATS at +8.2 % instead
  of +5.8 % in the first run).
