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

## 2026-11-02 – Report generator, phase 1: the structure of a full broker report

- **Reference document:** DNB Markets' 45-page update note on SATS (7 March 2025, Q1 and CMD preview). It is read for
  structure and method only; no sentence is reproduced, and the private copy stays outside the repository
  (`docs/rapport/struktur.md`).
- **The eleven-section template (phase 2) follows the brief, not the note's page order:** the note is a pre-results
  update, so its proportions (half the pages on self-collected data) tell us what to prompt a case author for, while the
  section list of the brief tells us what every report must contain. The data map in `struktur.md` section 5 marks each
  input Have / Collect / Missing; "Missing" prints as *not available* in the report, never as an estimate.
- **Report language English, conversation Norwegian** – the repository's existing convention; the Norwegian file names
  (`docs/rapport/`) are the brief's.
- **Rendering: HTML with print CSS, printed to PDF by headless Chrome (or Edge) – not PowerPoint and not reportlab.**
  A 25-40-page document with dense tables, footers on every exhibit and running headers is a paged document, not a deck;
  python-pptx would need PowerPoint to export a PDF, and reportlab is not installed here. HTML keeps the content testable
  on Linux CI (the test asserts on the HTML – sections, sources, EST marks, "not available" cells) while the PDF step runs
  wherever a Chromium binary exists (locally, and on GitHub's Ubuntu runners). Charts are matplotlib SVG, embedded inline
  so the HTML is one self-contained file.
- **Previous estimates must be stored to show estimate revisions.** Every report build writes the estimate table to
  `reports/<ticker>/estimates_<date>.json`; the next build diffs against the latest earlier file. The first report of a
  company shows "first report – no previous estimates".
- **Quarterly data is a new block in the data module** (`QUARTERS`: revenue, EBITDA before and after the lease
  adjustment, EBIT, net profit, EPS and the segment lines per quarter, plus the operating KPIs). The annual model is not
  changed; the quarter preview splits the annual forecast with the seasonality of the last two years and labels the
  result EST.

## 2026-11-02 – Report generator, phase 2: the template

- **One builder, eleven sections, in `deck_builder/`** (`build_report.py` + `report/`), next to the deck builder because it
  reads the same `model_map.json`, `deck_data.ModelData` and case modules. The deck is unchanged.
- **The gate is part of the builder, not a separate step:** `rb_gate.evaluate` runs the Checks sheet, `verify_dcf.py`
  (parsed), the audit, the case gate and `stress_test.py` before a single section is rendered, and the result is printed
  in the disclosures. `stress_test.py` now writes `stress_<case>.json` (the report's stress table reads it) – a
  twelve-line addition, no change to what it tests. `--skip-gate` exists for CI and layout work and is visible on the page.
- **Section 4 (quarter preview) splits the annual model, it does not forecast quarters.** Our quarter = the full-year
  forecast × the average share of that quarter in the last full years, labelled EST and explained in the exhibit note.
  A separate quarterly model would double the driver set for little gain; the honest reading is "run-rate against the
  annual estimate".
- **Consensus:** Yahoo's revenue and EPS means (annual and current quarter) are the only consensus shown; EBITDA, EBIT,
  DPS and segment consensus print *not available* with the name of the source the sell side uses.
- **Own-history multiples instead of a forward P/E history:** trailing P/E and EV/EBITDA after leases at year-end prices
  from the company's own numbers, plus today's price on our first forecast year, labelled as such. A consensus-based
  forward history needs Bloomberg and is listed under what we do not know.
- **Peer groups** come from `PEER_GROUPS` in the data module (name → peer names from `PEERS`); the implied value per
  share by group uses min / median / max of the group's NTM multiple on the model's metric for the Comps year.
- **The fictional Example Company carries the template test** (`example_deck.py`, `QUARTERS`, `PEER_GROUPS`, `META` in
  `example_data.py`): every optional block filled with invented, labelled data, so CI exercises every code path without a
  real company; SATS is filled in phase 3.
- **Outputs:** `examples/<TICKER>/report/` holds the PDF, `prices.json`, `estimates_<date>.json`, `gate.json`; the HTML
  is git-ignored (regenerated). Private cases pass `--out-dir` to an ignored folder.

## 2026-11-02 – Report generator, phase 3: SATS after the Q3 2026 report

- **Second edition of the SATS case, two drivers touched.** Norway price/mix 2026E 7.5 % (5.5 %) and fixed-cost inflation
  2026E 1.0 % (1.5 %), both to the nine-month run-rate of the Q3 report; nothing else in the forecast, the scenarios, the
  WACC or the terminal value changes. The lower 2026 cost base carries through the forecast (final-year EBIT margin 15.9 %
  against 15.1 %), which is what a fixed cost base does; the target moves from 54 to 58 and the rating stays BUY.
- **Price = last close before the model date (30 Oct 2026), not an intraday quote;** `fetch_prices` drops today's row.
- **Consensus from the company's own page.** SATS publishes a Modular Finance consensus (revenue, EBITDA, EBITDA before
  IFRS 16, net profit, members; seven contributors). It is public, so it is used for the annual and Q4 2026E lines; EPS
  comes from Yahoo (five analysts) because the company page has none. Both sources are named in the exhibit.
- **The quarterly store is eight quarters deep** (Q4 2024–Q3 2026), from the comparative columns of the four last
  reports, with country revenue, country EBITDA before IFRS 16, clubs, members and ARPM. Older quarters are a collection task.
- **Shareholders not collected:** the company page builds its table in the browser and the annual-report list was not
  retrieved; the report says so instead of copying a third-party snapshot of unknown date.
- **Page count:** the SATS report is 25 pages with the content the brief lists, at a type size readers of broker research
  are used to (10pt body). The 25–40 range of the brief assumes the self-collected pages (price tracker, multi-year KPI
  series, city competition) that the DNB note has and this edition does not; they are listed in the comparison document
  as the next edition's work, not padded.
- **The research-book row stays the author's.** The build writes a proposed row to the private case folder
  (`~/osloquant-home/cases/proposals/`) and never to `judgements.jsonl`.

## 2026-11-02 – Report generator, phase 4: scaling

- **One data module and one narrative dict per company; the template does not change per company.** What changes per
  sector is the model (`docs/rapport/skalering.md` section 2): consumer/retail/services run today; salmon and oil service
  need driver blocks (price deck, cost per kg, backlog, day rates) and sector valuation exhibits; banks need a model that
  does not exist in the toolkit. The checklists in section 3 are the collection work per sector.
- **Short histories:** a company with three audited years (an IPO prospectus) prints three-year tables and charts;
  `_hist_years()` takes the years with revenue data instead of the workbook's seven columns.
- **The private case stays out of the repository.** Its report is built into the ignored `OUTLET/` folder with the same
  command; the scaling note describes what the run showed without its figures.
- **Candidates in order:** Europris, Kid, Mowi – the first two reuse the retail pattern as it is; Mowi is the first salmon
  case and therefore a template extension.

## 2026-11-02 – Report generator, phase 5: the dashboard reads the reports

- **`build_report.py` publishes to the oslo-quant home** (`~/osloquant-home/cases/reports_pdf/<TICKER>/`: the PDF, the
  estimates snapshot and a `meta_<date>.json` with kind, title, pages and the gate result) unless `--no-publish`. The
  dashboard lists them on the stock page, shows the latest estimates against the previous edition and raises a decision
  item when a report's target differs from the research-book view. The toolkit never writes to the research book or the
  judgement log: a report is an input to a decision, not the decision.

## 2026-11-03 – Elkem: the first case outside consumer (examples/ELKEM)

- **The company in the brief no longer exists.** The brief named Silicones, Silicon Products and Carbon Solutions and Bluestar
  as owner. Elkem transferred the majority of Silicones to Bluestar on 30 April 2026 against the redemption of Bluestar's
  52.9 % stake, reclassified Elkem Iceland and the retained silicones plants as held for sale, raised NOK 1.8bn of equity and
  reports Silicon, Foundry Alloys and Carbon from Q3 2026. The case is built on the company as it is; the brief's questions
  (segments, cycle, cost, China/Bluestar, capital allocation) are answered for the new perimeter in `data/FORSTAAELSE.md`.
- **One year of history, on purpose.** Only 2025 exists restated on the current perimeter (Q3 2026 report). The workbook runs
  with `HIST_START = 6`; the 2021-2025 division series from the Capital Markets Update is kept in `DIVISION_HISTORY` and used
  in the report and in the through-cycle test (audit A8). Mixing the old structure's seven years (NOK 46bn of revenue in 2022)
  with the new 15bn perimeter would have made every growth rate and ratio wrong.
- **Segments = external revenue per division** (Silicon 8 945 + "Other" 403, Foundry Alloys 2 642, Carbon 2 976), so that the
  three segments sum to group revenue; division totals incl. internal sales (9 452 / 4 181 / 3 272) are quoted where the
  company's own margins are discussed. Volume = the division's sales volume in tonnes.
- **Cost per tonne, not cost per krone of revenue.** Raw materials and energy are built as unit cost × volume with input inflation
  (`_unit_cost_build()`), and the workbook receives the derived COGS share per year (47.5 % in 2026E falling to 45 % by 2028E as
  prices recover, rising again from 2031E with the power step). This is what makes a price recovery drop through to EBITDA; a
  fixed percentage would have hidden the operating leverage. Growth capex through sales-to-capital is switched off (s2c = 50):
  price-led revenue needs no capital and all capex sits in maintenance capex (~100 % of D&A plus Rana).
- **Base case below the company's target.** Silicon prices +10 % (2027E) and +5 % (2028E) from the trough, volumes flat to +2 %,
  Foundry Alloys and Carbon at 22 % and ~27 % margins: group EBITDA 1.9bn (13 %) in 2026E, 2.6bn (17 %) in 2027E, 3.0bn (18 %)
  in 2028E, fading to 17 % by 2033E. The >20 % target is the bull case. The bear case holds prices at the 2026 trough for eight
  years with higher power costs (probability 30 %, bull 25 % – a cyclical with a fat downside tail).
- **Non-operating assets at the company's own figures.** Held-for-sale net assets NOK 3 423m (Iceland ~1.3bn at an estimated
  fair value equal to book with a 0-3.0bn range; Roussillon 1.7bn) and 1.3 million EU ETS allowances at NOK 1 200m (zero book
  value) enter the EV bridge: NOK 13 a share, shown separately and removed in the what-if runs. The reader must be able to see
  the value with and without them.
- **Result:** DCF NOK 47.0 (WACC 8.1 %, terminal growth 2 %, RONIC 10 %), target NOK 48, BUY against a price of 30.92; the price
  implies a final-year EBIT adj. margin of 7.4 % against our 10.6 % and the 10.7 % of the trough year 2025; terminal growth is not
  solvable as a single driver (the value-driver terminal value cannot bring the DCF down to the price), which the report states.
- **Template changes made for this case, all backwards compatible:** (1) `Inputs 7 / eq_issue` – equity raised after the last
  actual year-end reduces net debt and adds to book equity in the first forecast year, with a matching cash-flow row (`cf_issue`);
  without it the 2026E leverage breached the base-case kill check; (2) the WACC peer-beta table sizes itself to `len(PEERS)` (it
  was fixed at eight rows and twelve peers overwrote the median row – Python and Excel WACC differed); (3) the terminal-growth
  solver accepts −15 % and the gate accepts an explicitly unsolvable driver; (4) `loc_g` returns 0 when the previous average is
  blank (one-year histories); (5) generic labels in the report: `QUARTERS['kpis']`, `seg_ebitda_label`, `seg_volume_label`,
  `MARKET['loc_label'/'rpu_label']`, `competition[...]['headers']` – the old fitness texts remain the defaults.
- **Not in the workbook, by design and stated as such:** segment-level costs and a segment SOTP (`sotp_runs.py` is a location
  engine); the division economics live in the deep dives and the SOTP is a table with EST multiples. Listed as the first items to
  build before the next industrial case (`examples/ELKEM/LÆRDOM.md`).
- **Consensus:** Elkem publishes none; Yahoo revenue (5-6 analysts) and EPS (3) are used and named; EBITDA/EBIT/DPS and the
  quarter are "not available". Price series: paid indices are not used; dated public points (SunSirs, Mysteel, Ferroglobe filings,
  Argus as quoted) with a note that they are points, not a series.
- **Prices from the oslo-quant store, not Yahoo directly** (`prices.json` written from the store's adjusted closes and its OSEBX
  series), as the brief asked; the Yahoo symbol stays in `MARKET` for the refresh path.
- **The research-book row stays Oscar's.** The build writes a proposal to `~/osloquant-home/cases/proposals/`; ELK is added to the
  dashboard watchlist with the three things to watch (Silicon margin, EU review, leverage).
