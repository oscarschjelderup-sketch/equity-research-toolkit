# 02 – How they write: the structure of Nordic sell-side research

Researcher 2 of 4. Written 22 Oct 2026. The subject is **structure**, not wording. Everything below is paraphrased. Page counts, dates and numbers are taken from the documents themselves. Where something could not be verified it says "unknown".

---

## 1. Method and sources

**Method.**
1. I ran web searches for public Nordic research: broker commissioned-research portals, sponsored-research providers, issuer IR pages and press.
2. I opened every candidate:
   - PDFs were read through WebFetch and converted locally to text with PyMuPDF. Page counts come from the PDF page tree.
   - JavaScript-rendered portals (DNB Carnegie Access, ABG Sundal Collier Commissioned Research, Redeye, Inderes) were read in a browser, using page text only. Cookie banners were declined.
3. For each document I recorded:
   - how the front page is built;
   - the section order (from heading font sizes);
   - the valuation method, and whether scenarios, sensitivities, consensus comparison, catalysts or implied-expectations analysis appear;
   - where the risks sit.

**Limits.**
- **DNB Carnegie Access.** The site puts a professional-investor confirmation in front of the full reports. I did not accept it. For Lytix and CDON, only the public web summary, page count and key stats were used.
- **Redeye.** Full reports are now behind a premium paywall. Only the public preview template and an old one-page press release were used.
- **Press.** Finansavisen and DN redirect to a login wall, so no article text could be read.
- **Search budget.** The session's shared web-search budget ran out during the work. Later sources were reached by following links from pages already found.

**Sources** (all accessed 22 Oct 2026). R-numbers are used in the matrix.

| # | Document | Broker / provider | URL |
|---|---|---|---|
| R1 | Inderes – *Finnish market done; pan-Nordic next*, Initiation of Coverage, 18 May 2022 (66 pp) | SEB Corporate Research (commissioned) | https://research.sebgroup.com/pdf/InderesIOC_180522.pdf |
| R2 | Nordea – *A major discrepancy between price and value*, Initiation of coverage, 12 Jun 2023 (37 pp) | Inderes | Report page https://www.inderes.se/en/research/nordea-major-discrepancy-between-price-and-value ; PDF https://www.inderes.se/files/5901f5d5-9e5d-4999-88c1-b54b1ee611ff |
| R3 | Candles Scandinavia – *Expansion to spark growth and shareholder value*, Initiation of coverage, 11 Sep 2025 (37 pp) | Carlsquare Equity Research (commissioned) | https://carlsquare.com/wp-content/uploads/2025/09/Initial-coverage-report-Candles-20250911.pdf (landing page https://carlsquare.com/equity-research-candles-scandinavia-expansion-to-spark-growth-and-shareholder-value/) |
| R4 | Lytix Biopharma (Oslo) – *Maturing pipeline sets up for a pivotal year – initiating coverage*, 9 Mar 2026 (60 pp per portal listing) | DNB Carnegie Access (commissioned) | https://access.dnbcarnegie.com/publication/ad72ca0d-6100-4623-3815-08de7dd4fcd7 ; list https://access.dnbcarnegie.com/companies/1614/equity-research |
| R5 | CDON – *Ready to capture full potential – initiating coverage*, 17 Jun 2026 (57 pp per portal listing) | DNB Carnegie Access (commissioned) | https://access.dnbcarnegie.com/publication/cc191768-b0ca-4c60-33de-08decb8e5131 ; list https://access.dnbcarnegie.com/companies/1639/equity-research |
| R6 | Xplora Technologies (Oslo) – *Connection established*, 19 Aug 2025 (20 pp). The oldest note on the portal (likely the first ABG commissioned note); labelled "Post-results comment" | ABG Sundal Collier Commissioned Research | https://cr.abgsc.com/contentassets/3b0a272d2ba24984bec306600c3f9acd/pdf/connection-established.pdf ; list https://cr.abgsc.com/foretag/xplora_technologies/Equity-research/ |
| R7 | StrongPoint (Oslo) – *The American dream*, 10 Jul 2026 (10 pp), post-results | ABG Sundal Collier Commissioned Research | https://cr.abgsc.com/contentassets/512b4f0a088848ccb54b8504bc4a0b8e/pdf/the-american-dream.pdf |
| R8 | Photocure (Oslo) – *Rapid acceleration in the US market*, Outlook, 11 Apr 2019 (14 pp) | Edison Investment Research (commissioned) | https://www.edisongroup.com/research/rapid-acceleration-in-the-us-market/23912/ ; PDF https://d3s3shtvds09gm.cloudfront.net/14c29341f3084d850ad604731924b89c.pdf |
| R9 | BerGenBio (Oslo) – *Progressing towards key inflection points*, update, 16 Dec 2020 (3 pp) | Edison Investment Research (commissioned) | https://www.edisongroup.com/research/progressing-towards-key-inflection-points/28511/ ; PDF https://d3s3shtvds09gm.cloudfront.net/e84249f46cffb37037440bfdc81ba1a6.pdf |
| R10 | CapMan – *Moving in the right direction*, pre-results update, 14 Jul 2026 (11 pp) | Nordea Commissioned Equity Research | https://research.nordea.com/api/reportfileapi?id=1e08e751-67e7-4863-837a-bcdb2a0ab27b (via https://www.inderes.dk/third-party-research/capman-moving-in-the-right-direction-nordea) |
| R11 | BankNordik – *Another guidance upgrade*, flash, 15 Oct 2021 (3 pp) | Nordea Commissioned Research | https://research.nordea.com/api/reportfileapi?id=719601 |
| R12 | Zwipe (Euronext Growth Oslo) – *The Ecosystem Coming Together* (7 Sep 2020, web preview) and *Pilot Mode* (17 May 2022, 1-page press release) | Redeye | https://www.redeye.se/research/792967/zwipe-the-ecosystem-coming-together ; https://storage.mfn.se/d0d5883d-54d2-47b4-ae3f-bc4ccda8c84e/zwipe-pilot-mode.pdf |
| R13 | *Equity Research in an IPO process*, 3 May 2022 (15 slides). A Pareto analyst on how pre-IPO research and valuation ranges are built | Pareto Securities (Euronext seminar) | https://www.euronext.com/sites/default/files/2022-05/5.%20Equity%20research_IPO%20Valuation_Eirik%20Haavaldsen.pdf |

**Supporting documents** (not reports; used for definitions and context):
- **S1.** Pareto Securities research disclaimer. Defines "sponsored research" and the Buy/Hold/Sell bands. https://paretosec.com/compliancedownloads/disclaimer.pdf
- **S2.** Finanstilsynet, *Euronext Growth Oslo* thematic report, Jan 2022, ch. 7 "Investment firms' investment recommendations" (pp. 15–16). https://finanstilsynet.no/contentassets/293fc2101d0643009da1ff27aab79037/euronext-growth-oslo-report-january-2022.pdf
- **S3.** Aker ASA IR "Analyst coverage" page (9 brokers, names only). https://www.akerasa.com/investors/aker-share/analysts
- **S4.** DNB Carnegie Access company listings. They show page counts per note type for CDON, Lytix, Lifecare ASA and Carasent. https://access.dnbcarnegie.com/companies/1486/equity-research and https://access.dnbcarnegie.com/companies/1493/equity-research
- **S5.** Announcements of initiations, used to locate reports:
  - Norne/Ignitis: https://ignitisgrupe.lt/en/news/norne-securities-initiated-coverage-ignitis-group
  - DNB Carnegie/CDON: https://www.inderes.dk/en/releases/dnb-carnegie-access-cdon-ready-to-capture-full-potential-initiating-coverage
  - Nordea/Solwers: https://inderes.fi/releases/solwers-oyj-nordea-initiated-coverage-on-solwers
  - Carlsquare/Candles: https://www.inderes.dk/en/releases/carlsquare-initiation-of-coverage-candles-scandinavia-expansion-to-spark-growth-and-shareholder-value

Coverage of the sample: 13 documents.
- Six are initiations or first notes: R1–R6.
- Five are updates or flashes: R7, R9–R12.
- One is an outlook report: R8.
- One is a methodology deck: R13.
- Six concern Oslo-listed companies: R4, R6, R7, R8, R9, R12.

---

## 2. Matrix

Abbreviations:
- **FV** = fair value range.
- **TP** = target price.
- **CR** = commissioned / sponsored research.
- **ests** = estimates.
- "Implied" = an explicit what-the-market-prices-in or reverse-valuation section. This is *not* the same as "multiples implied by our fair value".

| # | Company / broker / date | Type, pages | First page (rating, TP, bullets, what is quantified) | Thesis framing | Market-implied / reverse-DCF? | Valuation methods | Peer table design | Risks: where; kill criteria; catalysts | Estimate tables; vs consensus | Charts |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | Inderes / SEB / 18 May 2022 | Initiation, CR, 66 pp | No rating; **FV range EUR 35–39**. Headline plus a lead paragraph. Three headed paragraphs: business, growth, valuation. The valuation paragraph states the method weights (DCF/peers 60/40). Quantifies market share (~2/3 of Finnish listed cos), organic CAGR, Nordic market ≈7× Finland. Key-data box plus a 5-year financials table (2020–24E, ~20 rows incl. multiples, ROE/ROCE, FCF yield). 12M absolute/relative share chart | "Proven at home, now scaling to the region": growth option on top of a defensive core | Partial. A separate block values only the existing contract base (NPV of one contract × contract count). It shows how much of the price the mature business explains, but is not framed as market-implied | DCF (WACC 8.5%, TG 2%) ±2pp growth sensitivity → 36–42; peers (2024E EV/EBITDA 9–11x) → 30–36; blend 60/40, then range narrowed 5% at each end | Peers grouped; columns: price, mkt cap, P/E, EV/Sales, EV/EBITDA, EV/EBIT for 3 years, plus sales growth and EBIT margin; average/median rows; subject company "SEB est." row at bottom. Followed by a page of peer descriptions | Dedicated "Key risks" chapter (pp. 38–39, 7 headed risks) placed **before** financials/valuation. No kill criteria. No dated catalysts (Q1 recap and outlook only) | 2022E and 2023–24E estimate chapters; Bloomberg consensus used for peers only, no vs-consensus for the subject | Football-field "valuation range by method", DCF assumption table, 2-D DCF sensitivity grids, contract trend, market-size charts |
| R2 | Nordea / Inderes / 12 Jun 2023 | Initiation, 37 pp (translated from Finnish) | Cover page only. P.2: rating scale graphic (Buy/Accumulate/Reduce/Sell), **Buy, TP EUR 12.5**, risk level; 4 headed paragraphs (thesis, business, turnaround, valuation); key figures table 2022–25E; guidance box. P.3: charts plus **"Value drivers" and "Risk factors" bullet lists side by side**, plus valuation multiples table | "Price vs value gap": the market is too pessimistic about the sustainability of earnings | **Yes.** (a) Implicit cost of equity backed out from P/B, consensus ROE and g (Gordon) for Nordic banks over 5 years. (b) P/B vs ROE regression across peers. (c) "What would have to happen to justify today's price": crisis-level loan losses or a return to zero rates, each translated into a P/E | P/E and P/B target multiples (TP = 9x P/E, 1.4x P/B); justified P/B (Gordon); peer regression; historical P/E vs 10-yr average; total distribution yield | Separate "Peer group valuation" page; plus regression chart | Risk-factor bullets on p.3 and a "Risk profile of the business model" page after company description. No kill criteria; no dated catalysts | 4-page estimates chapter; consensus used heavily (Bloomberg ROE consensus) for valuation, not as an explicit "us vs consensus" table | Many: share price vs index, income/EBIT, EPS/DPS, ROE vs P/B scatter, implicit COE history |
| R3 | Candles Scandinavia / Carlsquare / 11 Sep 2025 | Initiation, CR, 37 pp | Labelled "Commissioned equity research". Sidebar: company blurb, CEO/CoB, list, price, mkt cap, EV, performance table, **Bear/Base/Bull share values (SEK 30/65/97) with up/downside %**. Main column: lead paragraph plus 3 headed paragraphs (capacity, acquisition, investment case). Quantifies sales growth, acquisition revenue/EBITDA contribution, implied deal multiple | "Capacity plus M&A unlock growth and margin catch-up to peers" | No. Only "implicit multiples of our fair value" (EV/EBITDA 13.4x vs peers 7.2x) | Weighted: DCF 60% + EV/EBIT 2026 20% + EV/EBIT 2027 20% → base SEK 65; bull/bear via DCF with different growth/margin paths | "Reference group" chapter (pp. 18–22) with NTM EV/EBITDA and EV/EBIT; historical premium/discount discussion | Investment-case bullets (p.3) carry the risk caveats; **one-page "Risks and Challenges" at p.32, after valuation**. No kill criteria or dated catalysts | Financial history and forecasts chapter (pp. 23–28); accounts appendix (pp. 33–36). No consensus | Share performance; scenario fan; peer multiples |
| R4 | Lytix Biopharma (Oslo) / DNB Carnegie / 9 Mar 2026 | Initiation, CR, 60 pp | (Web summary.) **FV range NOK 14–18**, no rating. Lead paragraph quantifies total peak-sales potential (~USD 1bn by 2036–37), names the key near-term events (data readouts, pivotal-study start, H2 2026) and the main risk. Then 3 headed paragraphs: asset, per-indication peak sales and launch years, valuation and risks. Portal sidebar: FV range with date, mkt cap, next report date, key stats | "Pipeline about to be de-risked; one indication carries the value" | Unknown (full report not read) | SOTP by indication (biotech rNPV-style) | Unknown | Main risks (clinical setbacks, delays leading to financing need) stated **in the summary**; catalysts given by half-year. Kill criteria unknown | Unknown | Unknown |
| R5 | CDON / DNB Carnegie / 17 Jun 2026 | Initiation, CR, 57 pp | (Web summary.) **FV range SEK 71–87**. Lead paragraph (turnaround done, now investing; management target vs house estimate +30%). Headed paragraphs: business model, upside if target met, valuation | "Turnaround complete, now growth; upside if management hits its 2027 target" | Partly: quantifies upside **if management's target is met vs house estimate**. Not a market-implied analysis | Peer multiples (mainly 2027e EV/EBITDA) + 0–20% premium for growth; DCF as cross-check (SEK 80–99) | Unknown | Unknown | Unknown | Unknown |
| R6 | Xplora (Oslo) / ABG / 19 Aug 2025 | First note on the portal, CR, 20 pp | "Commissioned research – Not rated". 3 bullets (strong quarter; **'25–'28e EBIT CAGR 30%**; EV/EBIT falling from 18x to 6.6x). 3 headed paragraphs incl. **FV range NOK 42–69**. Sidebar: estimate-change % table (Sales/EBIT/EPS, 3 yrs), key data, performance chart vs OSE, 3-yr multiples table (P/E, EV/EBITDA, EV/EBIT, FCF yield, lease-adjusted ND/EBITDA) | "One KPI drives the value": converting device buyers into subscribers | No | DCF scenarios: 3 growth × 3 long-term margin cases, WACC 11%, TG 2% → NOK 42–69; multiples on own estimates (EV/EBIT, FCF/EV yield) | Two-step peer design: (1) broad hardware peers; (2) peers **scored/ranked on key metrics** to pick the 3 most relevant; then EV/EBITDA–capex vs those | Risks paragraph on p.2 next to company description (standard ABG layout). No kill criteria; next event date on front | Quarter-vs-ABGSCe deviation table; estimate changes; P&L/BS/CF estimates; 4 pages of KPI assumption tables (devices, subscribers, recurring revenue, profitability). No consensus | KPI bar charts, multiple paths, peer tables |
| R7 | StrongPoint (Oslo) / ABG / 10 Jul 2026 | Post-results update, CR, 10 pp | Same ABG template: 3 bullets, actual vs ABGSCe in text, **FV range NOK 8–18** | "Mixed quarter; first US customer is the new leg" | No | DCF (WACC ~10%, TG 2.5%) → NOK 8–27 plus a 2-D sensitivity (WACC × TG, TG × margin) | None in this note | p.2 risks paragraph; next event date on front | Estimate changes + annual estimates page | Revenue, GM, growth, LTM EBITDA margin charts |
| R8 | Photocure (Oslo) / Edison / 11 Apr 2019 | Outlook, CR, 14 pp | No rating. Price/mkt cap/net cash box, 1/3/12-month performance, **4-year estimate table** (Revenue, PBT, EPS, DPS, P/E, yield). 4 headed paragraphs (growth, investment, partner sales, **valuation NOK 57/share**) | "US launch drives the franchise" | No | rNPV per product (probability, launch year, peak sales, rNPV) + net cash | None | P.2 investment summary has a fixed 4-part frame: company, valuation, financials, **sensitivities**. Full "Sensitivities" section before valuation. Next event in sidebar; no kill criteria | Financial summary exhibit (P&L/BS/CF, 2 actual + 2 forecast years); no consensus | Numbered "Exhibits" (pipeline table, clinical data, sales regions, reimbursement) |
| R9 | BerGenBio (Oslo) / Edison / 16 Dec 2020 | Update, CR, 3 pp | Same Edison front page; valuation per share | "Data flow towards registrational study" | No | rNPV by indication (per-share split given) | None | **Dated catalysts**: named congress with dates, H1 2021 readout, 2021 study start, 2023 filing | Financial summary exhibit | Few |
| R10 | CapMan / Nordea / 14 Jul 2026 | Pre-results update, CR, 11 pp | Labelled "Marketing material commissioned by". **Fair value range EUR 1.6–2.0** (SOTP). Estimate-change % table, key data incl. **next report date**, 7-year summary table (2022–2028E, ~18 rows) | "Momentum building" ahead of results | No | SOTP: fee business at EV/EBIT range, carry at lower multiple, group costs, balance-sheet investments at book ±10%; DCF cross-check (EUR 2.5–3.0) with distribution chart | None | "Main risks" box on the valuation page. Disclosure explains a 1–5 risk rating that feeds the cost of capital, and notes that a 1–2pp change in an assumption can move fair value 30%+ | Detailed annual + quarterly estimates; full reported/forecast statements. No consensus | Estimate-revision table, SOTP bar, DCF distribution |
| R11 | BankNordik / Nordea / 15 Oct 2021 | Flash, CR, 3 pp (1 page content) | One paragraph: guidance change vs house estimate, read-across to **consensus** (expects it to move up), FV range DKK 192–215 (Gordon growth) | Event reaction | No | Gordon growth model | None | None | Mentions consensus direction only | None |
| R12 | Zwipe (Euronext Growth Oslo) / Redeye / 2020 & 2022 | Updates (preview + 1-p PR) | Public preview lists what the full report contains: update, estimates, **bear/base/bull valuation**, **"Redeye Rating" scores for People, Business, Financials (each with positives/negatives)** and "Market Edge" scores. 2022 PR names catalysts (card-scheme certification, larger orders) | Catalyst-led | Unknown | DCF-based fair value range (bear/base/bull) | Unknown | Catalysts named qualitatively | Unknown | Unknown |
| R13 | Pre-IPO research / Pareto / 3 May 2022 | Methodology deck, 15 slides | The slide "most discussed with investors" is the **valuation range**. It shows the range's midpoint, implied EV/EBITDA and P/E at the range ends for 4 years, the discount to asset values, a peer comparison and dividend yield at different payout ratios | n/a | Implied multiples **at the proposed price range** (forward check, not reverse DCF) | Range on "normal valuation metrics" plus peer data plus asset values; premium/discount vs peers explicitly argued | Peer multiples bar charts | Process: model → management workshop → Q&A → report (legal/management fact-check, **not** the valuation range) → roadshow feedback | Revenue estimates vs guidance | Football-field/bars |

---

## 3. Patterns

### 3.1 What the best-structured reports share

1. **The first page is a self-contained memo with a fixed grid** (all 13; clearest in R1, R2, R6, R10).
   - Left column: headline, a lead paragraph that already states the valuation conclusion, then 3–4 headed paragraphs. In the strongest, those paragraphs run business → driver → valuation (R1, R3, R4, R5).
   - Right column: key-data box, share-price chart vs index, and a multi-year estimate/multiples table.
   - The valuation conclusion and its method are always on page 1, often with the weighting: R1 60/40, R3 60/20/20, R5 multiples plus 0–20% premium.
2. **One named value driver, quantified on page 1.**
   - R6: the subscriber conversion rate, with the house assumption stated next to the first observed datapoint.
   - R4: peak sales by indication, with launch years.
   - R5: upside if management's target is met.
   - R2: earnings sustainability, priced through ROE.
   - Weaker notes describe the company without isolating a driver.
3. **A range, not a point, plus how the range was built.**
   - All commissioned reports give a fair value range (R1, R3, R4–R7, R10, R11).
   - The best explain the width: R1 uses ±2pp growth sensitivity, then trims 5% at each end. R6 uses a 3×3 growth × margin grid. R3 uses explicit bear/base/bull.
4. **The assumptions behind the forecast are made explicit.** R6 has four pages of KPI assumption tables (devices, subscribers, ARPU-type recurring revenue, margins) ahead of valuation. R1 has a DCF assumption table by year bucket.
5. **Peer work is argued, not dumped.**
   - R6 ranks candidate peers on key metrics before choosing three.
   - R1 explains why it uses EV/EBITDA (acquisition accounting distorts lower P&L lines) and adds a page of peer descriptions.
   - R2 regresses P/B on ROE across peers.
6. **A cross-check method.** R5 (DCF behind multiples), R10 (DCF behind SOTP), R1 and R3 (blend).
7. **"What the market prices in" is rare.** Only R2 does it explicitly, by backing out the implied cost of equity and translating stress cases into P/E. The others show "multiples implied by our fair value" (R3, R13). That is the forward direction, not the reverse. No document in the sample contains a formal reverse DCF.
8. **Kill criteria are absent everywhere, and dated catalysts are uncommon.**
   - Catalysts with actual dates appear mainly in biotech (R9 congress dates, R4 by half-year).
   - Elsewhere the only date is the next report date in the sidebar (R6, R7, R10).
9. **Comparison with consensus is rare in commissioned research.**
   - R11 mentions where consensus will likely move.
   - R2 uses consensus as a valuation input.
   - No report has a "house vs consensus" estimate table.
   - The usual comparison is actual vs the broker's own estimate (R6, R7: a deviation table; estimate-change % on the front).

### 3.2 Typical section order

Initiations R1, R2 and R3 all follow essentially:

1. Front page (summary + key data + estimates table).
2. Contents (R1, R2, R3).
3. Investment case / thesis (3–5 pp; R1, R3).
4. Company description and business model (often the longest block: R2 9 pp; R1 ~14 pp).
5. Market and competition.
6. Strategy, targets, growth drivers.
7. Risks:
   - R1: dedicated chapter *before* the financials.
   - R2: a "risk profile" page after the business model.
   - R3: one page *after* valuation.
8. Historical financials and forecasts.
9. Valuation, usually in this order: summary of methods → DCF with assumptions and sensitivity grid → peers → (SOTP).
10. Appendix: full P&L/BS/CF tables.
11. Disclosures (2–3 pp).

Updates (R6, R7, R10) keep the same front page, then: risks/company page → quarter review vs estimate → estimate changes → valuation → statements → disclosures.

### 3.3 Typical lengths

| Document type | Pages |
|---|---|
| Initiation | **37–66** (R2 37, R3 37, R5 57, R4 60, R1 66) |
| DNB Carnegie pre-results note | 14–16 (S4) |
| DNB Carnegie post-results note | 10–16 (S4) |
| DNB Carnegie news/flash | 5–6 (S4) |
| ABG updates | 10–20 (R6, R7) |
| Nordea update | 11 (R10) |
| Nordea flash | 3 (R11) |
| Edison outlook | 14 (R8) |
| Edison update | 3 (R9) |

Pareto's own deck (R13) reports 19, 49 and 66 initiations in 2019, 2020 and 2021, from roughly 40 analysts covering about 400 companies. It also notes that a large share of distributed research is never opened. That argues for a front page that works on its own.

### 3.4 Commissioned vs independent research

- **Labelling and rating.**
  - Commissioned research: "Commissioned research", "Marketing communication/material commissioned by …" (R1, R3, R6, R7, R10, R11). There is **no rating and no target price**, only a fair value range. ABG prints "Not rated" (R6, R7).
  - Pareto's disclaimer (S1): "sponsored research" is paid for by the issuer, written without instruction rights for the company, and treated as a minor non-monetary benefit under MiFID II.
  - Independent research uses a rating plus a 12-month target. Pareto: Buy above +10% expected total return, Hold within ±10%, Sell below −10% (S1). Nordea's disclosure (R10) also refers to absolute ratings for its non-commissioned research.
- **Hybrid.** Inderes (R2) has an agreement with the issuer according to its disclaimer, yet publishes a four-step rating with a target price and a risk level.
- **Content emphasis.**
  - Commissioned reports spend more pages on company description and market education (R1 ~14 pp company overview; R3 ~12 pp, pp. 6–17). They are written for retail and new investors and publicly distributed.
  - Valuation is presented as a range with method weights.
  - Risks are often one short paragraph or one page (R3, R6, R7). R1 is the exception, with a full chapter.
  - Nordea's disclosure states whether the issuer reviewed the report before publication (R10: not reviewed).
  - In pre-IPO research, legal and management check facts but **not** the valuation range (R13).
- **Independent research.** The full independent reports from Pareto, Arctic, SB1 Markets, Danske, DNB Carnegie and Nordea are not publicly readable (section 5). What is visible publicly is the rating, target price and a one-line reason reproduced by press or aggregators. The structural comparison above therefore rests on commissioned and hybrid material, plus the Pareto deck and disclaimer.
- **Regulation.** Finanstilsynet's review of recommendations on Euronext Growth (S2) found that firms use templates to meet the Market Abuse Regulation (MAR) content rules, but often give minimal disclosures. Examples: rating history only for the issuer itself, and lead-manager roles in private placements not disclosed.

---

## 4. Suggested skeletons (derived only from the patterns above)

### 4.1 Initiation deck (about 18–22 slides; the written initiations run 37–66 pp, so a deck compresses each block to 1–3 slides)

| # | Section | Must quantify | Pattern / reference |
|---|---|---|---|
| 1 | **Front page / summary** | Headline thesis in one line. Rating + TP, *or* FV range if framed as non-rated. 3 headed paragraphs (business → value driver → valuation). Key data (price, mkt cap, EV, free float, next event date). 3–4 year estimates/multiples table. Share chart vs OSEBX | R1, R2, R6, R10 |
| 2 | **Investment case in 3–4 points** | Each point has a number: growth CAGR, margin path, the one KPI | R1 pp.3–7, R3 p.3, R6 bullets |
| 3 | **The one value driver** | House assumption vs latest datapoint vs management target; value per share of ±1 unit | R6 (conversion rate), R5 (target vs estimate) |
| 4–6 | **Company and business model** | Revenue mix, unit economics, customers/contracts | R1, R2 (9 pp compressed) |
| 7–8 | **Market and competition** | Market size and share, peer positioning | R1, R2 |
| 9 | **Strategy and management targets** | Stated financial targets vs house estimates | R2 p.23–24, R5 |
| 10–11 | **Forecast assumptions** | KPI tables by year (volumes, price, margin, capex) | R6 pp.8–10, R1 DCF assumption table |
| 12 | **Estimates** | P&L/CF summary; estimate changes if any; vs consensus *if available* (rare publicly, so add it as an edge) | R6, R10; absence noted in 3.1 point 9 |
| 13 | **Valuation summary (football field)** | Each method's range, the weights and the final range/TP | R1 p.53, R3 weight table |
| 14 | **DCF** | WACC, TG, explicit-period assumptions, 2-D sensitivity grid | R1 p.54, R7 p.4 |
| 15 | **Peers** | Peer selection logic (ranking on metrics), 3-year multiples, premium/discount argument | R6 p.13–14, R1 p.55–56 |
| 16 | **Scenarios** | Bear/base/bull values per share with assumptions stated | R3, R6 (3×3), R12 |
| 17 | **What the market prices in** | Implied growth/margin/CoE at today's price; what has to happen to justify the price | R2 pp.29–31 (only example found) |
| 18 | **Risks** | 4–7 named risks, each with direction and rough per-share impact | R1 pp.38–39; R2 p.3 drivers-vs-risks layout |
| 19 | **Catalysts and kill criteria** | Dated events (report dates, AGM, trial readouts) and what would invalidate the thesis | R9, R4. Kill criteria are an addition: none found in the sample |
| 20 | **Appendix** | Full P&L/BS/CF; peer descriptions | R1, R3, R10 |
| 21 | **Disclosures** | Status (independent / not rated / student work), conflicts, data sources | S1, S2, R10 |

### 4.2 Prep page (one page, front-page grid of R1/R6/R10)

1. **Header.** Company, ticker, date, price, mkt cap, EV, next event date (R6, R10).
2. **Verdict line.** Rating + TP *or* FV range, upside %, and the method weights in one sentence (R1, R3, R5).
3. **Three headed paragraphs**, each with at least one number:
   - (a) what the business is;
   - (b) the single value driver, house vs datapoint vs target;
   - (c) valuation and cross-check.
4. **Bear/base/bull strip.** Value per share and up/downside (R3 front-page sidebar).
5. **What the market prices in.** One line, e.g. implied growth or CoE at today's price (R2).
6. **Estimates table.** 2 actual + 3 forecast years: revenue, EBIT, EPS, FCF, EV/EBIT, P/E, FCF yield, ND/EBITDA (R6, R10).
7. **Top 3 risks and 2 dated catalysts.** Side by side, as in R2 p.3's value drivers vs risk factors.
8. **Kill criterion.** One line: what result or event would make you change your mind. Not found in any public report; added as a differentiator.

---

## 5. Det som ikke lot seg finne offentlig

- **Independent (non-commissioned) broker research on Oslo Børs companies.** Full reports from Pareto, Arctic, SpareBank 1 Markets, DNB Carnegie (independent side), ABG (independent side), Danske, Nordea, SEB, Kepler Cheuvreux, Fearnley and Clarksons. These are distributed via the brokers' client portals and aggregators (Bloomberg, FactSet, Infront, LSEG/Refinitiv, S&P Capital IQ aftermarket). Only names of covering analysts are public on IR pages (S3), and headline rating/target changes appear in press or aggregator snippets.
- **Full text of DNB Carnegie Access reports** (R4, R5, Lifecare, Carasent). They are behind a professional-investor confirmation gate; only web summaries and page counts were used.
- **Full Redeye reports** (now premium), including the actual Redeye Rating scores and bear/base/bull values for Zwipe.
- **Press coverage of initiations and upgrades in DN, Finansavisen and E24.** Login or paywall; no article text could be read. E24 returned no usable search hits.
- **Consensus estimates** (Infront/Modular Finance/Vara/Bloomberg/FactSet). None of the public reports show a house-vs-consensus table, so how brokers present this could not be verified.
- **Pre-IPO investor-education research** (Pareto R13 describes the process). The actual PIR documents for Oslo IPOs are restricted to investors and not public.
- **Page counts and structure of SB1 Markets' and Danske's initiations** (e.g. of Nekkar, reported via LinkedIn/aggregators): unknown.
- **Norne Securities' sponsored initiations** (e.g. NattoPharma 2019, Ignitis 2024): announced publicly, but the report files were not located within the available search budget, so they are not analysed here.
