# Scaling the report to a new company

Phase 4 of the report-generator mission (2 November 2026). What a new company needs before `build_report.py` produces a
report that passes the gate, which inputs are the same for every company and which depend on the sector, a checklist per
sector, and three candidates from the watchlist.

## 1. The inputs every company needs

| Block | File | What goes in | Source | Effort |
|---|---|---|---|---|
| History | `<co>_data.py` → `HIST`, `SEG_REV/VOL/LOC`, `YEARS` | Seven years (or as many as exist) of P&L, balance sheet, condensed cash flow and segment KPIs; costs negative; `simulate()` must balance | Annual and Q4 reports | 1 day for a first company in a sector, half a day after |
| Market data | `MARKET` | Price and date (last close), shares and dilution, net debt, cash and leases at the last balance-sheet date, 52-week range, segment names, Yahoo symbols | Latest interim report, Yahoo | 1 hour |
| Forecast drivers | `BASE`, `SCENARIO_ADJ`, `TERMINAL`, `WACC_INPUTS`, `COST_CAPITAL`, `ENGINE` | Eight years of drivers, bear/bull deltas, terminal settings, WACC inputs, fixed-cost shares and the revenue engine | The analyst, from the company's guidance and history | The judgement – 1 day |
| View | `CONSENSUS`, `CONSENSUS_Q`, `VARIANT`, `SCENARIO_STORIES`, `KILL`, `PEERS`, `PEER_GROUPS`, `META` | Public consensus (company page, Yahoo), where we differ and when we find out, scenarios as stories, five kill criteria, 6-10 peers in two groups, audit metadata and reasons | Company IR page, Yahoo, the analyst | Half a day |
| Quarterly store | `QUARTERS` | Eight quarters of group lines and segment KPIs | The last four interim reports (comparative columns) | 2 hours |
| Calendar and record | `EVENTS`, `HISTORY` | Next events with their source; earlier calls | Financial calendar (company / NewsWeb / MFN), the judgement log | 15 minutes |
| Narrative | `<co>_deck.py` → `CT["report"]` | Memo, thesis, risks, description, targets, owners, SWOT, 2-4 deep dives with exhibits, competition tables with dated rows, macro rows, revisions, data map, flips, unknowns, sources | The analyst; `example_deck.py` shows every key | 1 day |
| Build | `build_model.py` → `excel_finalize.py` → `verify_dcf.py` → `stress_test.py` → `whatif_runs.py` (→ `sotp_runs.py`) → `build_report.py --refresh-prices` | The gate must pass; the report refuses to build otherwise | Windows with Excel for the finalise/stress/what-if steps | 20 minutes of machine time |

Rules that hold for every company: every figure has a source and a date; estimates are EST; what we do not have says
*not available*; the first build stores its estimates so the second shows revisions; the judgement-log row is the author's,
the build only proposes it.

## 2. What depends on the sector

The workbook is an FCFF model with a location engine (units × volume per mature unit × price) or a segment build
(volume × price). It fits consumer, retail, services and most industrials. Three sectors need more than a data module.

| Sector | What differs | What the toolkit has | What is missing |
|---|---|---|---|
| **Salmon** (MOWI, SALM, LSG, GSF, BAKKA) | Volume = harvest tonnes by region; price = NASDAQ salmon index / contract share; cost per kg (feed, biology); the resource-rent tax (25 % effective on top of 22 %) changes the tax line and the value of Norwegian volumes; biology (mortality, ISA, lice) is the kill criterion; EV/kg is the sector multiple | `META['sector']="salmon"` triggers the tax check (`audit.py` A16, `stress_test.py` adds a +15pp tax stress); the segment build takes tonnes × price | A price deck (forward curve vs spot) as a driver with its source; cost per kg by region in the history; EV/kg and P/NAV of licences in the valuation; a biology block in the deep dives |
| **Oil service** (SUBC, AKSO, TGS, DOFG, ODL, BORR) | Revenue = backlog conversion + book-to-bill; utilisation and day rates per asset class; capex cycles and fleet renewal; the oil price is the macro driver; EBITDA less maintenance capex; peers on EV/EBITDA and backlog coverage | Segment build with volume (days / vessels) × price (day rate); `META['commodity']` for the commodity check; the oil-sensitivity study in oslo-quant for the beta | Backlog and order intake as drivers with the history; a utilisation/day-rate table per asset class; a Brent deck vs forwards (audit B22-style check exists for the deck); fleet age and newbuild commitments in capital allocation |
| **Bank** (DNB, SRBNK, SB1NO, NONG) | No FCFF: net interest income, loan growth, NIM, cost/income, loan losses, CET1 and the payout constraint; valuation by justified P/B (ROE − g)/(COE − g) and dividend discount; the kill criterion is the loss ratio or CET1 headroom | Nothing in the workbook (ANALYSE.md 1.2 lists the bank template as future work); the dashboard's light cases use justified P/B | A bank data module and workbook (balance-sheet-driven P&L, capital, payout), a bank valuation sheet; the report template works once the model exists (the sections are the same, the valuation exhibits change) |
| **Consumer / retail / services** (SATS, OUTLT, EPR, KID, ORK, XXL) | Units, like-for-like, price/mix, gross margin and own brands, store economics, working capital; the template was built on it | Everything: location engine, SOTP by concept, store-economics and capital-allocation slides, two full reports | Per company: the quarterly store, a price tracker, competitor tables with visit dates |

## 3. Checklist per sector

### Consumer, retail and services
- [ ] Seven years of history from the annual reports; segment revenue, units (stores/clubs) and volume per unit per year
- [ ] Eight quarters: group lines plus revenue, segment EBITDA, units, volume and price per unit by segment
- [ ] Price tracker: list price of the comparable product each January (and the Internet Archive for the back history), with the date
- [ ] Competitor table per market: operator, format, units, price for the comparable product, binding, source, visit date
- [ ] Company targets with the source page; management; the top-20 shareholders from the annual report (dated)
- [ ] Drivers: like-for-like, price/mix, net openings, capex per unit, fixed-cost shares, working capital in % of revenue
- [ ] Kill criteria: price/mix growth, like-for-like volume, EBIT adj. margin, cash conversion, leverage
- [ ] Peer groups: same-sector operators and Nordic retail; lease basis stated
- [ ] Macro rows: policy rate, CPI, wages, consumer confidence, FX exposure – each with source and date

### Salmon
- [ ] History: harvest volume by region, achieved price vs the index, cost per kg, EBIT per kg; biology KPIs (mortality, lice treatments)
- [ ] Drivers: volume by region (licences, MAB utilisation), price deck (forward curve with date vs spot), cost per kg, contract share
- [ ] Tax: 22 % corporate plus the resource-rent tax on Norwegian sea-phase profit; `META['sector']="salmon"`
- [ ] Kill criteria: cost per kg above a level, mortality, price deck below cost, leverage
- [ ] Valuation: EV/kg of harvest, EV/EBITDA, P/NAV of licences; peers = the listed farmers; FX (EUR/NOK) on revenue
- [ ] Macro rows: supply growth (Kontali), EUR/NOK, feed prices; deep dive on supply/demand

### Oil service
- [ ] History: backlog, order intake, book-to-bill, utilisation and day rates per asset class, EBITDA less maintenance capex
- [ ] Drivers: backlog conversion by year, new order assumptions, day rates, utilisation, fleet additions/retirements, capex phasing
- [ ] Commodity: Brent deck vs the forward curve with the date; `META['commodity']="brent"`
- [ ] Kill criteria: book-to-bill below 1, utilisation below a level, leverage, covenant headroom
- [ ] Valuation: EV/EBITDA on mid-cycle, backlog coverage, NAV of the fleet (broker values not available – say so)
- [ ] Macro rows: oil price, E&P capex guidance, rig counts; deep dive on the cycle

### Banks
- [ ] A bank model first (not in the toolkit): loans and deposits, NIM, fees, cost/income, loan losses, risk-weighted assets, CET1, payout
- [ ] History: ten years of the above; the loss history through 2008-09 and 2015-16 (oil)
- [ ] Drivers: loan growth, NIM path vs the policy rate, cost growth, loss ratio, CET1 target and buffer
- [ ] Kill criteria: loss ratio, CET1 below requirement plus buffer, NIM compression beyond x bp
- [ ] Valuation: justified P/B, dividend discount, P/E vs peers; the reverse exercise is the implied ROE
- [ ] Macro rows: policy rate path, house prices, unemployment, oil (regional banks)

## 4. Outlet Group – the second company through the template

The private Outlet Group case (IPO 24 September 2026; history 2023-2025 only, no consensus, no quarterly series yet) was
run through the same builder: `EQR_CASE=outlet_data`, output to the ignored `OUTLET/report` folder. What it showed:

- The template handles a short history (blank years are left out of the tables and charts) and a company without consensus
  (every consensus cell says not available and the quarter preview falls back to the H1 reconciliation).
- The sum-of-the-parts runs (`sotp_outlet.json`) feed the valuation section automatically.
- Everything that made the SATS report convincing – the quarterly store, the since-last-edition table, the signposts – is
  data work the first edition of a case cannot have. The Outlet report is therefore an initiation shape: more company and
  unit economics, less run-rate.

## 5. Three new companies from the watchlist

Criteria: the FCFF-with-units model fits without a new template, the company discloses segment KPIs quarterly, a light
case already exists in the dashboard, and the public data lets the report fill at least eight of the eleven sections.

| Company | Why the data is good enough | What fits the template | What has to be collected |
|---|---|---|---|
| **Europris (EPR)** | Quarterly like-for-like, store count, gross margin and own-brand share since the 2015 IPO; Lekekassen and ÖoB in the segment note; company publishes consensus | Location engine (stores × revenue per store × like-for-like), working capital and the central warehouse – the SATS/Outlet pattern; the peer groups already exist | The quarterly store, a price basket vs Rusta/Biltema/Coop, the owner list |
| **Kid (KID)** | Two segments (Kid Interiør, Hemtex) with stores, like-for-like, gross margin and online share per quarter; a Pareto case exists in the user's files for the structure; dividends and leverage well disclosed | Location engine by country; SOTP by brand; the margin-bridge and inventory exhibits from the retail slides | Quarterly store, Swedish competitor table, price basket, FX (SEK, USD sourcing) rows |
| **Mowi (MOWI)** | The richest quarterly disclosure in the sector (harvest, price achievement, cost per kg by region, feed, consumer products); a light case exists; the oslo-quant oil-beta and currency work covers the EUR/NOK channel | Segment build (tonnes × price) and the report sections; the salmon audit and stress hooks exist | The sector-specific blocks of section 2: price deck with its date, cost per kg history, resource-rent tax line, EV/kg valuation, biology deep dive – the first salmon case is a template extension, not only data |

Order: Europris first (closest to the two cases already built), then Kid, then Mowi once the salmon blocks exist.
