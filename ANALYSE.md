# ANALYSE – the rules a case must follow

Distilled from the phase 1 research (`docs/research/`, sources there). Every rule cites its evidence: `01`-`04` are
the research notes, `#n` a failure mode in 03 section 5, `Rn` a candidate rule in 04 section 4, `S`/`A`/`C` a
source, study or case in those notes. Changes to this file come as pull requests with `verify_dcf.py`,
`audit.py` and the calibration report as evidence (phase 4).

A rule is enforced in one of four ways: **CHECK** (automatic in `model_builder/audit.py`, run by `verify_dcf.py`),
**GATE** (`case_gate.py`, in CI), **STRESS** (`stress_test.py`, research-driven block), **TEMPLATE** (the deck and
prep-page structure). A rule marked **JUDGE** can only be forced as a question: the audit flags it and the case
must answer in `META['reasons']`, which puts the judgement on the record.

---

## 1. Rules that always apply

### 1.1 Law and conduct (Norway)

| Rule | Why / source | How |
|---|---|---|
| A recommendation names its author, date and time of every price used, the rating definitions and horizon, a summary of the valuation method and assumptions, a sensitivity analysis in the risk section, the planned update frequency and the 12-month history of ratings and targets | MAR art. 20 and delegated regulation 2016/958 art. 3-4, restated in VPFF Standard 3 (Feb 2026) – 03 §3.1, 04 R37-R40 | CHECK B30 (META `disclosures`) |
| Facts are kept apart from opinions; forecasts and targets are labelled as opinions; estimates are marked EST | 2016/958 art. 3; 04 R38 | TEMPLATE |
| Conflicts are disclosed: own holdings, mandates, issuer payment. Issuer-paid research carries no rating or target | 2016/958 art. 6; VPFF 2.4; Finanstilsynet's Arctic Securities letter (14 Apr 2021): a research head's holding missing from a report – 03 §3.2 | CHECK B29 (META `conflicts`) |
| No trading on, or disclosure of, inside information; a recommendation is not shared with the issuer's insiders before publication except for fact checks without the rating/target | MAR art. 7-10, 14; VPFF Standard 3 quiet periods – 03 §3.1 | Conduct rule; noted on the prep page |
| Personal rule for this toolkit: paper money in every automated account; nothing trades; decisions are the author's | Mission (DECISIONS.md) | — |

### 1.2 Accounting and method

| Rule | Source | How |
|---|---|---|
| One lease basis end to end: FCFF after lease payments, net debt and WACC ex leases (pre-IFRS 16) – or the reverse, never mixed. Peers on the same basis or flagged | 04 R30-R32; 03 #23, A24-A25 | CHECK B23 |
| The EV-to-equity bridge is complete: net debt, minorities, associates, pensions, other – each filled or explicitly zero | 03 #24 | CHECK B24 |
| Diluted share count, including issues after the balance-sheet date | 03 #25 | CHECK B25 |
| Price, balance sheet and valuation dates stated; balance sheet no older than 120 days | 03 #26; 2016/958 | CHECK B26 |
| rf = Norwegian 10-year government bond on a stated date (a normalised rf only if labelled and shown beside the spot) | PwC/FFN 2025 (55 % use it) – 04 R1 | CHECK B21 |
| Market risk premium 5.0 % by default; outside 4-6 % needs a reason. Size premium from the PwC/FFN medians by equity value (> NOK 5bn 0 %, 2-5bn 1 %, 0.5-2bn 2 %, 0.1-0.5bn 3 %, < 0.1bn 4 %); size + specific ≤ 3pp; no stacking without a note; no illiquidity discount on liquid listed shares | 04 R2-R6, S1 | CHECK B21 (JUDGE) |
| Discount rate in the currency of the cash flows; a company that reports in USD/EUR is valued in that currency and converted once at a dated spot rate | 04 R7; 03 #21-#22 | CHECK B21-B22 |
| WACC weights and beta relevering use the same D/V | 03 #20 | CHECK B20 |
| Terminal value: g ≤ rf; reinvestment = g / RONIC; RONIC ≥ WACC and its ratio to WACC justified above 1.5x; TV share of EV reported, > 80 % needs a reverse-DCF statement | 04 R10-R14, R17; Damodaran S13-S14; 03 #5-#7 | CHECK A5-A7 |
| Exit multiple is a cross-check, never the primary TV; the Gordon TV's implied multiple shown | 04 R16; 03 #28 | CHECK B28 |
| Working capital and capex follow growth: no NWC release or capex below depreciation in growth years without a driver | 03 #17-#19; 04 R13 | CHECK B17-B19 (JUDGE) |
| DCF carries at least half the target weight; heuristic targets (P/E x EPS, PEG) are not targets | 03 #29, A5-A6 | CHECK B29 |

### 1.3 Expectations – the point of a case

| Rule | Source | How |
|---|---|---|
| Every case runs a reverse DCF and states in numbers what the price implies (margin, growth, WACC) and where the view differs by at least 1pp; DCF at least 10 % from the price. No gap, no case | 04 R27 (Mauboussin & Rappaport S21); only 1 of 13 public reports does it – 02 §3.1 | GATE (CI) |
| A BUY/SELL whose estimates sit within ±2 % of consensus everywhere is not supported | 03 #11, A14-A15 | CHECK A11 |
| Expected total return above Ke + 15pp needs the reverse DCF and a bear case below the price on the front page; above Ke + 40pp is a warning | 03 #13; targets imply ~15pp too much return (A1), error grows with upside (A4) | CHECK A13 |
| The rating scale is symmetric around the cost of equity | 03 #14 | CHECK A14 |
| A model older than 120 days, or a price down 25 % since the model date, blocks publishing until updated | 03 #12, A12 | CHECK A12 (`--price-now`) |

### 1.4 Forecasts – where optimism hides

| Rule | Source | How |
|---|---|---|
| Real revenue CAGR above 20 % over the explicit period needs a reason (achieved by 18 % of small and 0.2 % of large firms over ten years) | Base Rate Book (A20) – 03 #1 | CHECK A1 (JUDGE) |
| Bear at least 25 % below base; scenarios span a realistic growth range (consensus dispersion 8.3 % vs realised 18.7 %) | A20 – 03 #2 | CHECK A2 (JUDGE) |
| Final-year margin above the historical maximum + 2pp, or above the peer median and still rising, needs a reason; the value at the last-3-year mean margin is shown | 03 #3-#4, A4, A20 | CHECK A3-A4 (JUDGE), STRESS #4 |
| Company guidance is an input, not the forecast: flag forecasts above the top of guidance or equal to it | 03 #10, A13, A16 | CHECK A10 |
| Binary events (trial, licence, tender, court) are probability-weighted with the failure value shown | 03 #15, cases C5, C14-C18 | CHECK A15 |
| Leverage: peak net debt / EBITDA above 4x or interest cover below 2x requires a refinancing or distress scenario; dividends above FCFE for two years are flagged | 03 #27 – the most frequent killer on Oslo Børs (8 of 21 cases) | CHECK B27 (JUDGE) |

---

## 2. What separates the best from the average

**Caveat first.** Norway's rankings are investor votes on usefulness, not accuracy scores; Kapital itself reported
that the 2021 winners' favourite stocks lagged the index, and no Nordic accuracy ranking is public after 2015
(01 §5). "Best" below therefore means *what the most-voted analysts and the best-structured public reports do*,
and the toolkit's own standard is calibration (`oq book calibrate`), not resemblance.

| Pattern | Evidence | In the toolkit |
|---|---|---|
| **Sector depth over breadth.** The same names win the same sector for years: offshore (Huseby Karlsen, DNB), oil (Sveen-Nilsen, SB1), IT (Kongslie, SB1), industrials/real estate (Jonassen, ABG), banks (Astrup → Svendsen) | 01 §2-§4 | Sector rules (§3) and a research book that grows sector by sector |
| **Page one is a self-contained memo:** conclusion and method weights, one quantified value driver, key data, a 3-5 year estimates table | All 13 public reports – 02 §3.1 | TEMPLATE §5 |
| **One named value driver**, with the house assumption next to the latest datapoint and the company target | 02 §3.1 (R6, R4, R5) | "Key judgement" box; targets-vs-model slide |
| **A range and how it was built** (sensitivity grid, scenarios, method weights) | 02 §3.1 (R1, R3, R6) | Sensitivity, scenarios, football field |
| **Explicit KPI assumptions before valuation** | ABG Xplora note, 4 pp of KPI tables – 02 §3.1 | Growth-engine and assumptions slides |
| **Peers argued, not dumped** (ranked on metrics before selection; method choice explained) | 02 §3.1 (R6, R1, R2) | Peers slide with the growth regression |
| **What the public sample lacks** – reverse DCF (1 of 13), kill criteria (0 of 13), house vs consensus (0 of 13) | 02 §3.1 | Mandatory here (GATE, thesis tracker, consensus slide) |

---

## 3. Sector rules – Oslo Børs is not one market

| Sector | Value with | Must model | Traps (source) | Audit hooks |
|---|---|---|---|---|
| **Salmon farming** | DCF on price x volume − cost/kg; EV/kg and EBIT/kg cross-check; licence value | Price deck: spot year 1, then forwards (Euronext salmon futures), then a stated long-term price; EBIT/kg by region; ground-rent tax 25 % effective on top of 22 % since 2023 (norm-price regime under review for 2027) | Flat 22 % tax; one spot price for all years; regions treated alike (04 §3.1, R33; case C2) | META `sector="salmon"`, `commodity`, `commodity_deck` → A9, A16, STRESS tax +15pp |
| **Oil & gas E&P** | Field-by-field NAV with finite-life cash flows; EV/DACF, EV/2P cross-check | 78 % marginal tax (22 + 71.8 %), immediate expensing, refundable losses; dated price deck vs forwards; USD cash flows with a USD rf | 22 % tax; perpetuity TV on depleting reserves; a commodity call disguised as "undervalued" (04 §3.2, R18, R23-R24, R34) | `sector="eandp"`, `reporting_currency="USD"`, `cyclical=True` → A8, A9, A16, B21-B22 |
| **Oil service / drilling** | Probability-weighted cycle scenarios; through-cycle or 2-3-year forward multiples; asset values | Utilisation, day rates, backlog cover, through-cycle margin, net debt / EBITDA | Peak-year extrapolation; consensus misses the cycle; leverage (04 §3.3; cases C1 Seadrill, C7) | `cyclical=True` → A8, B27 |
| **Shipping** | P/NAV on dated charter-free broker vessel values beside the DCF | TCE, fleet supply, vessel values, cash breakeven; USD | P/NAV < 1 read as cheap; perpetuity on an ageing fleet; currency (04 §3.4, R36) | `cyclical=True`, `reporting_currency="USD"` |
| **Banks** | Equity models only: DDM, FCFE net of regulatory capital, excess return (P/B = (ROE − g)/(ke − g)) | ROE vs ke, CET1 path vs requirement (systemic risk buffer 4.5 %), loan growth, losses | FCFF/WACC template on a bank; 100 % payout with growth (04 §3.5, R35) | The toolkit's FCFF template does **not** apply – a bank template is future work |
| **Consumer / retail** | FCFF DCF + EV/EBIT, P/E or EV/EBITDAaL peers | Like-for-like, gross margin, store roll-out economics (capex and inventory per store), rent, inventory days | Lease basis mixed; roll-out growth assumed free; NWC (04 §3.6; cases XXL, Kid) | B17, B23, B27; store-economics and SOTP slides |
| **Technology / growth** | Scenario DCF with failure risk; reverse DCF and market-implied competitive advantage period | Implied CAGR/margin at the price, sales-to-capital, dilution, cash runway | g above rf; growth without reinvestment; dilution ignored (04 §3.7; cases Kahoot, Nel, Crayon) | A1, A6, B19, B25 |

---

## 4. The 30 failure modes as checks

Run: `python model_builder/audit.py <workbook> <map> <case_data> [--price-now P] [--strict]`, or automatically at
the end of `verify_dcf.py` (with `EQR_CASE`). `stress_test.py` ends with the research-driven stresses.

| # | Failure mode (03 §5) | Check | Type |
|---|---|---|---|
| 1 | Growth above base rates | A1 real CAGR > 20 % → FLAG | CHECK, JUDGE |
| 2 | Range too narrow | A2 bear > 75 % of base or growth spread < 5pp → FLAG | CHECK, JUDGE |
| 3 | Hockey-stick margins | A3 final margin > historical max + 2pp → FLAG | CHECK, JUDGE |
| 4 | No mean reversion | A4 above peer median and rising → FLAG; STRESS margin at last-3-year mean | CHECK, STRESS |
| 5 | Terminal returns not faded | A5 RONIC/WACC > 2.0x FLAG, > 1.5x WARN; STRESS RONIC = WACC | CHECK, STRESS |
| 6 | Terminal growth not paid for | A6 g > rf FAIL; reinvestment ≠ g/RONIC FAIL | CHECK |
| 7 | TV dominance | A7 > 80 % WARN; > 90 % without reverse DCF FAIL | CHECK |
| 8 | Peak-cycle earnings | A8 cyclical: terminal margin > mean + 1 SD → FLAG | CHECK, JUDGE |
| 9 | Commodity deck | A9 model price vs forward > ±10 % → FLAG; missing deck → MISSING | CHECK, JUDGE |
| 10 | Anchoring to guidance | A10 above the top of, or equal to, guidance → FLAG | CHECK |
| 11 | Herding on consensus | A11 BUY/SELL within ±2 % of consensus → FAIL | CHECK |
| 12 | Stale target | A12 price −25 % since model → FAIL; model > 120 days → WARN | CHECK |
| 13 | Target optimism | A13 TSR > Ke + 15pp without reverse DCF and bear below price → FLAG | CHECK |
| 14 | Skewed rating scale | A14 asymmetric or < ±5 % → WARN | CHECK |
| 15 | Binary event | A15 probabilities must sum to 1 | CHECK |
| 16 | Tax regime | A16 salmon/E&P tax below the regime → FAIL; STRESS +15pp | CHECK, STRESS |
| 17 | Working capital | B17 NWC/sales falls > 5pp or > 1pp in a growth year → FLAG; STRESS NWC held | CHECK, STRESS |
| 18 | Capex below D&A | B18 in growth years → WARN | CHECK |
| 19 | Growth not paid for | B19 reads the workbook's return-on-new-capital check | CHECK |
| 20 | Leverage in WACC | B20 D/E ≠ D/V/(1 − D/V) FAIL; forecast D/V > 5pp off → WARN | CHECK |
| 21 | rf/ERP/currency | B21 bands, size lookup, currency → FLAG/FAIL; STRESS WACC +1pp | CHECK, STRESS |
| 22 | Reporting currency | B22 needs a dated FX rate | CHECK |
| 23 | IFRS 16 | B23 bridge must deduct net debt ex leases on the pre-IFRS 16 basis | CHECK |
| 24 | EV bridge | B24 minorities/associates/pensions | CHECK |
| 25 | Shares and dilution | B25 diluted ≥ basic; issues after the balance sheet | CHECK |
| 26 | Stale balance sheet | B26 > 120 days → WARN | CHECK |
| 27 | Leverage and dividends | B27 > 4x or cover < 2x → FLAG; dividends > FCFE 2 years → WARN | CHECK, JUDGE |
| 28 | Exit vs Gordon | B28 implied multiple vs exit input > ±25 % → WARN | CHECK |
| 29 | Heuristic target / conflicts | B29 DCF weight < 50 % FAIL; conflicts block missing → MISSING | CHECK |
| 30 | Disclosures | B30 the 2016/958 fields | CHECK |

**First results (22 Oct 2026).** SATS and a second, private case pass every hard check. Each has five judgement flags, answered in
`META['reasons']` from the cases' own text (margin above history, peers below, RONIC ≥ 2x WACC, NWC and
debt-funded dividends) – those answers are the author's to confirm. Both have two MISSING: the conflicts block
(holdings), which only the author can fill, and for SATS no checkable guidance in the model's units (A10), for
the private case no consensus yet (A11). The research-driven stress says what the judgement flags are worth:
**at the last-3-year mean margin both cases turn SELL** (SATS NOK 30.5; the private case's figure stays private). The margin is the case.

---

## 5. Writing template – deck and prep page

From the patterns in 02 §3-§4; the toolkit's additions (reverse DCF, kill criteria, consensus, calibration) are
marked **+**.

**Deck (initiation, ~20 slides):**
1. Front page: thesis in one line; rating + TP with % and horizon; price with date and time; 3 headed paragraphs
   (business → value driver → valuation); key data; 3-4 year estimates table; chart vs OSEBX.
2. Investment case in 3-4 points, each with a number.
3. The one value driver: house assumption vs latest datapoint vs company target; NOK per share per unit.
4. Company and business model; 5. Market and competition; 6. Strategy and targets vs house estimates.
7. Forecast assumptions: KPI tables by year.
8. Estimates, **+ vs consensus** (or vs company targets when there is none).
9. Valuation summary: football field with method weights.
10. DCF with WACC build and 2-D sensitivity; 11. Peers with selection logic; 12. Scenarios with probabilities.
13. **+ What the market prices in** (reverse DCF; GATE).
14. Risks: named, each with direction and NOK-per-share effect; sensitivity table (2016/958).
15. **+ Catalysts with dates and kill criteria** (thesis tracker).
16. Appendix: statements, store/unit economics, SOTP, capital allocation.
17. Disclosures: author, status, conflicts, rating definitions, method summary, price times, **+ 12-month history from
    the judgement log**.

**Prep page (one page):** header (price, market cap, EV, next event date) → verdict line (rating, TP, upside,
method weights) → three paragraphs with a number each → bear/base/bull strip → **+ what the market prices in** →
estimates table (2 actual + 3 forecast) → top three risks beside two dated catalysts → **+ one kill criterion** →
**+ audit status line** (FAIL/FLAG/MISSING counts from `audit.py`).
