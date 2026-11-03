# The structure of a full broker report – learned from DNB Markets on SATS (7 March 2025)

Phase 1 of the report-generator mission (see `DECISIONS.md`, 2 November 2026). The document studied is DNB Markets'
45-page note *SATS – Time to raise the bar* (Q1 and CMD preview, 7 March 2025, two analysts, BUY, target NOK 34 at a
share price of NOK 31). It is an **update note before a results day and a capital markets day**, not an initiation, so it
is thin on company description and thick on the quarter, the targets and the proprietary data. We learn the structure
and the method, not the words: nothing below reproduces the report's text, and the figures quoted are the report's own
numbers used to describe how an exhibit is built.

The four questions of the phase are answered in sections 1–4. Section 5 maps the result onto the eleven sections of our
template (phase 2) and lists, for every input, whether we **have** it free, can **collect** it ourselves, or **lack** it.

Conventions used in the tables: *Have* = already in the toolkit or available from a free source we already use (company
reports, Yahoo Finance via yfinance, NewsWeb, SSB, Norges Bank, the Riksbank, the European Commission); *Collect* = we
can assemble it ourselves from public web pages with a date on every observation; *Missing* = a paid source (Bloomberg,
FactSet, Visible Alpha, Similarweb, Holdings.se) with no free equivalent – the report prints "not available" there.

---

## 1. Section by section

| # | Pages | Section | What it contains | The question it answers | Data it needs | Status |
|---|---|---|---|---|---|---|
| 1 | 1 | **Front page** | Title (a thesis in five words) and a lead paragraph that states the call. Five headed paragraphs: the quarter vs consensus, status vs the company's own targets, the expected target revision with four numbered drivers, estimate revisions, valuation and rating. Right rail: rating and target, 12-month price vs OSEBX, a summary box (rating and previous, price, target and previous, upside, ticker), capital structure (shares basic and diluted, market cap, adjusted NIBD end of year, adjusted EV, ND/EBITDA, NAV per share, free float), next event with date, estimate-change table (sales and adjusted EPS, old/new/% for three years), a seven-year financial table 2021–2027e (revenue, adjusted EBITDA and EBIT, PTP, reported and adjusted EPS, DPS, growth rates, margin, EV/Sales, EV/EBITDA, EV/EBIT, P/E, P/B, ROE, dividend yield, FCF yield), analyst names and a pointer to the disclosures | What is the call, why now, what changed, what does it cost | Own estimates (model), previous estimates (a stored earlier model), price history and OSEBX (Yahoo), consensus (Bloomberg) | Have, except the **previous estimates** (we must store each build) and **consensus** beyond Yahoo's revenue/EPS means |
| 2 | 2 | **Investment case overview** | Price chart with the 12-month target and a bull/bear fan drawn from today's price to three values a year out; target-price methodology in three bullets (14x 2025e P/E; bull = +4 % revenue at 13x; bear = −4 % revenue at 15x); three boxes side by side – downside risks, "our case and how we differ from consensus" (two quantified bullets), upside risks; an EBITDA bridge 2024 → 2025e → 2026e by country | What has to be true, what could break it, where we differ | Scenario values (model), segment EBITDA by year (company segment note), consensus (for the "differ" box) | Have (segment EBITDA requires the country pages of the quarterly reports – the annual model holds segment revenue only) |
| 3 | 3 | **Company overview and SWOT** | Three-bullet description; sales by country and by category (two pies, estimate year); financial targets (medium- and long-term, from the last CMD); key management; five largest shareholders with stakes; SWOT with two or three quantified bullets per quadrant | What is the business and who owns it | Company reports and CMD, shareholder list | Have (shareholders: the annual report's top-20 list and NewsWeb flagging notices replace Holdings.se; the date must be printed) |
| 4 | 4 | **ESG overview** | Positive/negative trends, company actions, short- and long-term drivers | Is there an ESG angle that changes the numbers | Company sustainability report | Have, but low value in this case – the report itself concludes the scope is limited. Our template folds material ESG points into company overview and risks instead of a standalone page |
| 5 | 5–6 | **Quarter preview** | One page of text (revenue split into member growth, ARPM growth and other revenue; opex per club; EBITDA and underlying EBITDA vs consensus; net profit) and one full-page table: P&L lines – house estimate, consensus, % and absolute difference, same quarter last year, full-year estimate; then segment revenue, EBITDA and margin by country; growth and margin lines | What will the quarter show and where is the surprise | Quarterly history by segment (company reports), own quarterly estimates (a quarterly split of the annual model), consensus (Bloomberg/Infront – "n.a." for every segment line even at DNB) | **Collect** the quarterly history; **Have** Yahoo's quarterly EPS and revenue consensus for the current and next quarter; segment consensus **Missing** |
| 6 | 7–9 | **Targets vs delivery (CMD preview)** | Three bridges: the company's own target bridge from the last CMD, the realised bridge over the same period, and the realised bridge by country; a net-profit bridge by country; the expected new target range with the four drivers each turned into NOKm and EPS (Sweden members per club back to 2019 = c.NOK 130m EBITDA = NOK 0.48 EPS; other revenue back to 20 % of sales = c.NOK 70m = NOK 0.27); long-term margin targets vs the latest actual | Has the company delivered what it promised, and what will it promise next | CMD presentations, quarterly reports | Have |
| 7 | 10–16 | **Deep dive 1: the unexploited potential** | Revenue and adjusted EBITDA 2019–2024 with margin; EBITDA by segment stacked; change by segment vs 2019 and y/y; Sweden bridges 2023–24 and 2019–24 (members, ARPM, opex); the opex increase split into openings and existing clubs; average members per club quarterly since 2018 for the group and by country; openings and closures by country and year; members per sqm; clubs by country split opened before/after 2019; group ARPM split membership/other; ARPM by country with growth since 2019; membership ARPM adjusted for FX and the low-cost brand; list prices with and without group training; other revenues 2016–2024; other ARPM by country | Where is the next NOK 300m of EBITDA and what has to happen operationally | Country pages of every quarterly report since 2018 (members, clubs, ARPM, revenue, EBITDA), company websites for prices | **Collect** (all public; a quarterly KPI store per company is the work) |
| 8 | 16–22 | **Competition per market** | For each market a table of operators: clubs, price for the comparable membership, whether group training is offered, notes; maps of club networks in Stockholm, Copenhagen, Helsinki and Tampere; a count of competitor clubs in the capital | Is the price premium defensible where the growth is supposed to come from | Operator websites (club finders, price pages), Google Maps | **Collect** the tables with a visit date per operator; maps are optional (club counts per city carry the argument) |
| 9 | 23–25 | **Price study** | List prices per membership type and year 2019–2025 for each country (a proprietary tracker), the most popular membership marked; the implied average increase vs the contractual-price guidance; a screen of competitor prices for one-club and regional memberships with the date the sites were visited | How much of revenue growth is price, and is the company pricing above the market | Company price pages over time, competitor price pages | **Collect** going forward (date-stamped observations); the back history can be rebuilt from the Internet Archive and labelled as such |
| 10 | 26–29 | **Market outlook** | A bridge of discretionary consumption per household (wage growth, non-discretionary inflation, rate cuts) for two years ahead; CPI, policy rate and unemployment charts; the savings rate; for Sweden a bullet list of drivers with the Riksbank's numbers; wage growth vs inflation forecasts; consumer confidence for four countries; web traffic for the company's sites and for the industry by quarter | Does the consumer have room for a price increase | SSB, Norges Bank, the Riksbank, Statistics Sweden, the European Commission's consumer-confidence series, Similarweb | Have, except **web traffic (Similarweb – Missing)** |
| 11 | 30 | **Estimate revisions** | New vs old for three years: every P&L line, per-share data, growth and margins, then revenue, EBITDA, margin and underlying EBITDA by division | What changed in the model and why (two sentences) | Stored previous estimates | Have once each build is stored (phase 2 writes `reports/<code>/estimates_<date>.json`) |
| 12 | 31–35 | **Valuation** | A valuation summary table: four peer groups × nine multiples (EV/EBITDA, EV/EBIT, P/E for three years), median/min/max of the peers, the implied market-cap range drawn as a bar with the current value and the target marked; DCF and an M&A multiple as extra rows; an implied-multiples grid: ten share prices across, the multiples the company would trade at; 12-month forward P/E vs its own history and average; forward P/E vs peer groups over ten years; current vs historical by peer group; a peer table (market cap, sales/EBITDA/EPS CAGR, EV/EBITDA, EV/EBIT, P/E for four years); operating comparison with the listed fitness peers (clubs, members, revenue per member, opex per club and member, EBITDA) from a consensus database | What is it worth on every yardstick, and what does the price imply | Model (DCF), peer multiples and consensus (Bloomberg), forward-P/E history (Bloomberg), peer KPIs and estimates (Visible Alpha) | DCF, implied grid and the summary table **Have** with Yahoo multiples (LTM and NTM only); forward-P/E history **partly** (price / our own forward EPS, or trailing P/E – labelled); peer group history and peer KPI estimates **Missing** |
| 13 | 36–43 | **Financial statements** | Forecast changes P&L; by segment and assumptions; quarterly numbers (six actual and five estimated quarters) with adjustments; annual P&L 2018–2027e with adjustments; cash flow; balance sheet; valuation ratios; key ratios | The full audit trail | Model | Have (annual); quarterly estimates need the quarterly split |
| 14 | 44–45 | **Disclosures** | Recommendation structure and definitions, distribution of ratings, positions, analyst certification, jurisdictions | Who wrote this, under what rules, with what conflicts | — | Have: our `META['disclosures']` and VPFF Standard 3 items (ANALYSE 1.1); plus the line that this is a student case study and not investment advice, on the front page |

**Proportions.** Of 45 pages: 2 on the call, 2 on the company, 2 on the quarter, 3 on targets, 7 on the deep dive, 10
on competition and prices, 4 on macro, 1 on revisions, 5 on valuation, 8 on financial tables, 2 on disclosures. Half the
report is data the analysts collected themselves (sections 7–9). That is the lesson for scaling (phase 4): the generic
parts come from the model; the convincing parts come from a per-company data collection that a template can only
prompt for.

---

## 2. The charts that carry the argument – and how each is built

| Chart | Carries | Construction |
|---|---|---|
| **EBITDA bridge by country** (p2, p7–8) | The thesis in one picture: where the improvement came from and where the next one comes from | Waterfall: start bar (year 0 EBITDA), one floating bar per country for the change year 0 → 1, end bar, repeated for year 1 → 2. Country deltas = segment EBITDA (reported, after the lease adjustment) differences. Group functions as an "other" bar. Labels on every bar, source line "Company (historical), house (estimates)" |
| **Target bridge vs realised bridge** (p7) | Credibility of management: what the CMD promised per driver vs what came in | Two waterfalls side by side with the same driver order (LFL, maturing clubs, ARPM, cost). The realised bridge decomposes the EBITDA change into members × previous ARPM, ARPM change × new members, and the cost change. The driver split is the analyst's calculation and is sourced as "Company (figures), house (calculation)" |
| **Average members per club** (p12) | The volume lever: capacity utilisation vs the pre-pandemic level | Quarterly series since Q4 2018 for the group and by country: members at period end / clubs at period end. The key number is the gap to Q4 2019 (−10 % in Sweden) and it is quoted in the text next to the chart |
| **Members per sqm** (p13) | Corrects the members-per-club series for smaller new clubs | Members / total sqm at year end, four points; only possible when the company discloses sqm (SATS does in the CMD material) |
| **Openings and closures by country** (p13) | The portfolio churn behind the utilisation drop | Stacked columns per year, one panel for openings and one for closures; from the quarterly reports' club counts and the CMD |
| **ARPM, group and by country** (p14–15) | The price lever: how much of revenue growth is price, and whether it is FX | ARPM = membership revenue / average members / 12 (per month). Group split membership/other; by country with growth since 2019 as a label; an FX- and mix-adjusted variant with the adjustment stated in a note |
| **Membership price ladder** (p15, p23–24) | Pricing power and the mix effect of the group-training tier | Grouped bars per country: the comparable membership with and without group training, the % difference labelled; the proprietary tracker is a grouped bar per membership type with one bar per year 2019–2025 and the most popular membership marked |
| **Competitor price screen** (p25) | Position in the market: who is above and who is below | Sorted horizontal bars, one per chain, two panels (one-club and regional, same binding terms), a note with the date the websites were visited |
| **Discretionary consumption per household** (p26) | Macro reduced to one number per year that matters to the company | Bridge: level year 0, + wage growth, − inflation on non-discretionary consumption, + interest-rate cuts, = level year 1, repeated; inputs from SSB (consumption shares), Norges Bank (wages, CPI, policy rate path) |
| **Price with target fan** (p2) | The call and its range at a glance | Price history 12 months; a triangle from today's price to bear/target/bull values 12 months out, each labelled "NOK x (±y %)" |
| **12-month forward P/E vs own history** (p32) | The valuation argument: cheap against itself | Price / consensus NTM EPS, monthly, with the long-run average as a horizontal line. We can draw price / our own NTM EPS and trailing P/E from reported EPS, labelled as such; the consensus-based history needs Bloomberg |
| **Valuation summary** (p31) | Every yardstick on one page | For each peer group and multiple: implied market cap = multiple (min/median/max) × the company's basis − net debt, drawn as a horizontal range bar with the median marked; vertical lines for the current market cap and the target. The DCF and an M&A multiple get their own rows |
| **Implied multiples grid** (p31) | What a buyer at NOK x pays on every multiple | Columns = share prices from well below to well above the target; rows = each multiple; cell = (price × shares + net debt) / basis, or price / EPS. Pure arithmetic on model values |
| **Peer KPI panels** (p34–35) | Why the company trades where it does: slower unit growth than peers, higher revenue per member | Grouped bars per peer, one bar per year, CAGR labelled. History from the peers' reports is free; the estimate years need a consensus database |
| **Quarterly table** (p37) | The pattern of the year: seasonality and the run-rate | Eleven quarters across, P&L lines down, growth and margins at the bottom |

---

## 3. What makes the report convincing

1. **One chain from claim to target.** The thesis is a predicted company event (a raised medium-term target), given as a
   range in NOKm, broken into four drivers, and each driver is turned into EBITDA and EPS. The estimate revisions page
   shows those numbers entering the model; the valuation page prices the resulting EPS at a stated multiple. A reader can
   follow one number from page 1 to page 36.
2. **Every claim has a number behind it, and the number has a source and a date.** "Sweden is behind" is members per
   club 10 % below Q4 2019; "prices went up" is +15.4 % average list price with the most popular membership flat;
   "competition is tougher in Stockholm" is a club count by operator. Sources name the company, the website visited and
   the date; calculations by the analysts are labelled as such.
3. **The variant perception is explicit and dated.** The quarter estimate is 9 % above consensus on the line that
   matters, the reason is given (ARPM growth), and the date on which it will be tested is on page 1.
4. **Scenarios have values and assumptions.** Bull and bear are numbers a year out with their construction stated,
   drawn into the price chart. (Their construction is mechanical – ±4 % revenue and a multiple – which is the weakest
   part; see section 4.)
5. **Risks run both ways** and sit next to the case, three bullets each, specific to the company (VAT, Denmark losses,
   M&A in Finland).
6. **Proprietary data.** Half the pages show data the analysts collected: a price tracker over seven years, club counts
   per city, competitor price screens. This is what a reader cannot get elsewhere and what separates the note from a
   model print-out.
7. **Transparency about change.** Old and new estimates side by side with the percentage change on every line, and a
   two-sentence explanation of what moved.
8. **Consistent definitions.** Reported and IFRS-16-adjusted EBITDA are kept apart throughout, the valuation multiples
   state which basis they use, and the same basis is used for the peers.
9. **Historical depth.** Series run from 2016–2019, so the pandemic years are visible as a dip rather than as the base.
10. **The front page works alone.** A reader who stops after one page knows the rating, target, upside, what changed,
    the quarter's surprise and the valuation argument. Our research note 02 found this in every strong report.

What we will **not** copy:

- The target comes from a single P/E multiple on one year's EPS. Our rules require the DCF to carry at least half the
  weight (ANALYSE 1.2) and the multiple to be a cross-check.
- Bull and bear are ± a revenue percentage and a multiple, not stories with triggers. Ours are scenarios with a
  probability, a story, what has to happen and a signpost (Thesis sheet).
- There is no reverse DCF, no kill criterion and no list of unknowns (the three gaps research note 02 found in every
  public report).
- The ESG page says in its own words that ESG does not change the numbers. We do not spend a page on it.
- A "NAV per share" appears in the capital-structure box without definition. Every number in our boxes carries its
  definition in the glossary.

---

## 4. What we will do better

| Addition | What it is | Where it comes from |
|---|---|---|
| **What the market prices in** | A page that backs out the final-year EBIT margin, the revenue CAGR, the WACC and the terminal growth the share price implies, next to ours, with the gap in pp and the no-growth value; the case gate (≥ 1pp on a driver, ≥ 10 % DCF vs price) printed with its result | Reverse_DCF sheet, `case_gate.py` |
| **Kill criteria** | A table of the five KPIs that would end the case: threshold, direction, latest actual, status (ok / watch / broken) and the action; the same rows that feed the judgement log | Thesis sheet, `KILL` in the data module |
| **What we do not know** | Three lists: data we lack (with the name of the paid source the sell side uses), the assumptions that move value most (ranked from the one-at-a-time what-if runs, with the value and rating at each), and the changes that flip the conclusion (the stress tests: margin reversion to the three-year mean, RONIC = WACC, the bear scenario) | `whatif_runs*.json`, `stress_test.py`, the data-availability map in section 5 |
| **Scenarios as stories** | Bear, base and bull with probability, value, the story, what has to happen and the signpost; the probability-weighted value against the target | Thesis sheet |
| **A record of the call** | The 12-month history of ratings and targets, the call price, and the calibration so far, from the judgement log – which MAR/2016/958 requires and the public reports show only as a list | `oq book` (oslo-quant) |
| **Consensus honestly labelled** | Where consensus is public (Yahoo: revenue and EPS means, number of analysts, target range) we show it; every other consensus cell says "not available" and names the source we lack | Consensus sheet |
| **Sources and dates on every exhibit, EST on every estimate** | A footer under every table and chart: source, date of the data, date of the price; estimates marked EST in the header row | Template rule (ANALYSE 1.1) |
| **A data-availability map printed in the report** | The have/collect/missing table of section 5 for the company in question, so the reader sees what the report could not do | Template |
| **The build is gated** | `verify_dcf.py` and `stress_test.py` must pass; the report prints the check summary (30 checks, the audit statuses) and refuses to build if the master check fails | `model_builder/verify_dcf.py`, `stress_test.py` |

---

## 5. Mapping onto our template and the data map

The eleven sections of the phase-2 template, the DNB sections they absorb, and what each needs.

| Our section | DNB sections | Inputs | Have | Collect | Missing |
|---|---|---|---|---|---|
| 1 Front page | 1 | Rating, target, upside, key figures, next event, estimate changes, financial table 2021–2028e, price vs OSEBX | Model (Deck_Feed, Output, Analysis), Yahoo prices, OSEBX from oslo-quant, calendar from NewsWeb/company | Previous estimates: store each build | Consensus beyond Yahoo means |
| 2 Investment case | 2 (+ our 4) | Thesis, variant perception, bull/bear with assumptions, risks both ways, kill criteria, price chart with fan | Thesis, Consensus and Reverse_DCF sheets; `VARIANT`, `SCENARIO_STORIES`, `KILL` | — | — |
| 3 Company overview | 3 (+ 4 where material) | Description, revenue by segment and geography, targets, management, owners, SWOT | Data module (`SEG_REV`), case text (`mgmt`), CMD targets | Top shareholders from the annual report / NewsWeb with date | Holdings.se-type daily register |
| 4 Quarter preview | 5 | Our quarter by line and segment vs last year and consensus | Quarterly history to be added to the data module (`QUARTERS`), a quarterly split of the annual forecast (seasonality from the last two years) | Quarterly KPI store | Segment consensus; group consensus except Yahoo's quarterly EPS/revenue |
| 5 Deep dives (2–4) | 6, 7, 9 | Themes that decide the case, each ending in a number that enters the model (members per club → `lfl`, ARPM → `price`, cost per club → `cpi`/`pers_var`, openings → `net`) | The model rows they feed | The per-company KPI series and price observations | — |
| 6 Competition | 8 | Operators, units, prices, binding, with source and date per observation | — | Operator websites, job postings, trade press – a `COMPETITION` block in the data module with a date per row | Maps (optional) |
| 7 Macro | 10 | The drivers that reach the P&L (wages → personnel, CPI → rent, policy rate → consumer, FX → translation) | SSB, Norges Bank MPR, Riksbank MPR, EC consumer confidence (`MACRO` block with source and date) | — | Similarweb-type web traffic |
| 8 Estimate revisions | 11 | New vs old per line and segment, with reasons | Current model vs the stored previous build | — | — |
| 9 Valuation | 12 | DCF, reverse DCF, SOTP where relevant, multiples vs 2–4 peer groups, forward P/E vs own history, implied multiples at ten prices | DCF, Sensitivity, Comps, Football and Reverse_DCF sheets; peers from Yahoo (LTM/NTM); SOTP from `sotp_runs.py` | A second peer group per sector (the data module holds one; phase 4 adds `PEER_GROUPS`) | Forward-P/E and peer-group history on consensus EPS; peer operating estimates |
| 10 Financial statements | 13 | Full P&L, cash flow, balance sheet, key ratios, history and estimates | Output and Analysis sheets, Hist | Quarterly history | — |
| 11 What we do not know | — | Missing data, the assumptions that carry most, what would flip the conclusion | What-if runs, stress tests, this map | — | — |
| Disclosures | 14 | Author, dates, rating scale, method, update frequency, 12-month history, conflicts, the student-case line | `META['disclosures']`, judgement log | — | — |

**Where we match the report with free data:** sections 1–3, 6–11 and the disclosures. **Where we can only match it by
collecting data ourselves:** the quarterly KPI store (members, clubs, ARPM, revenue and EBITDA by country per quarter),
the price tracker and the competitor tables – the same work the DNB analysts did, with a date on each observation.
**Where we print "not available":** consensus by segment and by line beyond Yahoo's means, consensus-based forward
multiple histories, peer operating estimates, web traffic, and a daily shareholder register.

---

## 6. Sources

- DNB Markets, *SATS – Time to raise the bar*, equity research, 7 March 2025, 45 pages (read 2 November 2026; private
  copy, not in the repository). Used for structure only.
- `docs/research/02_how_they_write.md` (22 October 2026): the matrix of 13 public reports, which this note extends with
  one full-length, independent (non-commissioned) update note.
- `ANALYSE.md` sections 1.1–1.3 for the rules the template enforces.
