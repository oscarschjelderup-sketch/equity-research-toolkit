# 04 – The craft: what the authoritative frameworks say, and what is special about Oslo Børs

Researcher 4 of 4. Written 22 Oct 2026. Purpose: collect statements from authoritative frameworks that are concrete enough to become a **rule** (ideally an automated check) in the Excel DCF toolkit and deck builder, plus the Oslo Børs specifics a reviewer at a Norwegian broker will expect to see.

Conventions in this file:
- Everything is paraphrased. Short quotes only where wording matters.
- **[derived]** = simple arithmetic I did on a sourced number. **[judgement]** = my own analytical view, not taken from a source. All other statements carry a source.
- "via search excerpt" = the page itself could not be opened (timeout or 403); the statement comes from the search engine's excerpt of that page and should be re-checked before it is quoted in a deck.

---

## 1. Method and sources

**Method.** About 40 web searches and about 30 page fetches on 22 Oct 2026. When PDFs could not be read through the fetch tool, I extracted the saved copy with `pdftotext` and read the text (PwC/FFN 2025, Ødegaard lecture note, Damodaran terminal-value slides, Damodaran 2009 financial firms paper, Mauboussin/Johnson 1997 CAP paper, VPFF Standard 3, CFA Research Challenge guidelines). The session's web-search limit ran out before I got to Damodaran's narrative ("story to numbers") material, his young-growth-company material, a primary Equinor price deck, OSEBX sector weights and an October 2026 10y NGB quote. Those gaps are listed in the final section.

**Sources (all accessed 22 Oct 2026)**

| # | Source | URL | Read how |
|---|---|---|---|
| S1 | PwC & FFN, *Risikopremien i det norske markedet 2025* (survey 7 Oct–7 Nov 2025, 130 answers out of 1,314 sent, 9.9 % response rate) | https://finansfag.no/uploads/Risikopremien/MRP2025.pdf (same report: https://www.pwc.no/no/nyheter/risikopremien-i-det-norske-markedet-2025.pdf, 403 for the fetch tool) | Full text |
| S2 | B. A. Ødegaard, lecture note *Risikopremien i det norske markedet* (dated 27 Aug 2026 in the text) | https://ba-odegaard.no/teach/notes/risikopremien_i_norge/forelesning.pdf | Full text |
| S3 | NHH/FFN, AFA programme, content page | https://www.nhh.no/en/executive/afa-og-finans/afa-faglig-innhold/ | Page |
| S4 | VPFF Bransjestandard nr. 3 *Analyseavdelingens uavhengighet og integritet* (revised 25 Nov 2025, in force 1 Feb 2026); sections 4.2.2–4.2.3 restate Commission Delegated Regulation (EU) 2016/958 arts. 3–4 | https://www.vpff.no/images/Standard-3-Analyseavdelingens-uavhengighet-og-integritet-feb-2026.pdf | Full text |
| S5 | CFA Institute, Standards of Practice Guidance V(A) Diligence and Reasonable Basis (updated Apr 2024) | https://cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-v-a | Page |
| S6 | CFA Institute, Standard V(B) Communication with Clients (updated Jan 2024) | https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-v-b | Page |
| S7 | CFA Institute, Standard III(B) Fair Dealing (updated Apr 2024) | https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-iii-b | Page |
| S8 | CFA Institute Research Challenge, Written Report guidelines (PDF dated 24 Jul 2024) | https://www.cfainstitute.org/-/media/documents/support/research-challenge/challenge/rc-written-report-guidelines.pdf | Full text |
| S9 | Koller, Goedhart, Wessels (McKinsey), *Valuation*, 8th ed., Wiley, May 2025 – publisher table of contents only | https://www.wiley-vch.de/en/areas-interest/finance-economics-law/valuation-978-1-394-27941-8 | TOC |
| S10 | McKinsey, *How to value cyclical companies* | https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/how-to-value-cyclical-companies | via search excerpt (page timed out) |
| S11 | Cao, Jiang, Koller, *Balancing ROIC and growth to build value*, McKinsey on Finance, Spring 2006; Jiang & Koller, *A long-term look at ROIC* (2006) | https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/balancing-roic-and-growth-to-build-value ; https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/a-long-term-look-at-roic | via search excerpt (pages timed out) |
| S12 | Jennergren, *Value driver formulas for continuing value* (SSE working paper / technical note) | https://ideas.repec.org/p/hhb/hastba/2011_005.html | Abstract via search |
| S13 | Damodaran, slides *Terminal value: the tail that wags the dog? / Myths 5.1–5.4* | https://pages.stern.nyu.edu/~adamodar/pdfiles/country/TerminalValue.pdf | Full text |
| S14 | Damodaran, blog *Myth 5.2: As g → r … To Infinity and Beyond!*, 30 Nov 2016 | https://aswathdamodaran.blogspot.com/2016/11/myth-52-as-g-rto-infinity-and-beyond.html | Page |
| S15 | Damodaran, *Country default spreads and risk premiums*, updated 5 Jan 2026 | https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html | Page |
| S16 | Damodaran, *Little Book of Valuation* web page, commodity value drivers | https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/commodityvaluedrivers.htm | Page |
| S17 | Damodaran, *Valuing Financial Service Firms*, Apr 2009 | https://pages.stern.nyu.edu/~adamodar/pdfiles/papers/finfirm09.pdf | Full text |
| S18 | Damodaran stable-growth lecture slides (session 9 / session 12) | https://pages.stern.nyu.edu/~adamodar/pdfiles/valonlineslides/session9.pdf ; https://pages.stern.nyu.edu/~adamodar/podcasts/valUGspr23/session12slides.pdf | via search excerpt |
| S19 | Mauboussin & Johnson, *Competitive Advantage Period: The Neglected Value Driver*, CSFB *Frontiers of Finance*, 1997 | https://pages.stern.nyu.edu/~adamodar/pdfiles/eqnotes/cap.pdf | Full text |
| S20 | Morgan Stanley Counterpoint Global (Mauboussin & Callahan), updated CAP report, 14 Apr 2026 – landing page only | https://www.morganstanley.com/im/it-it/institutional-investor/insights/series/consilient-observer.html | via search excerpt |
| S21 | Mauboussin & Rappaport, *Expectations Investing* – Q&A summary | https://www.fool.com.au/2022/01/20/expectations-investing-a-qampa-with-michael-mauboussin-and-alfred-rappaport-usfeed/ | via search excerpt |
| S22 | Conglomerate discount evidence: CBS thesis on Atlas Copco; NOVA thesis (Honeywell field lab) | https://research.cbs.dk/en/studentProjects/conglomerate-discount-a-case-study-of-atlas-copco-ab/ ; https://run.unl.pt/bitstream/10362/186153/1/HONEYWELL_FIELD_LAB_ON_CONGLOMERATE_DISCOUNT_VALUE_UNDER_CONGLOMERATE_STRUCTURE.pdf | via search excerpt |
| S23 | FTI Consulting, *Valuation implications of IFRS 16*, 19 Sep 2025 | https://www.fticonsulting.com/fr-fr/france/insights/articles/valuation-implications-ifrs-16 | Page |
| S24 | Norsk Petroleum, *The petroleum tax system* (page shows updated 08.10.2026) | https://norskpetroleum.no/en/economy/petroleum-tax | Page |
| S25 | Skatteetaten, Petroleum tax regulations | https://www.skatteetaten.no/en/business-and-organisation/reporting-and-industries/industries-special-regulations/oil-and-gas-exploration-and-petroleum-tax/the-petroleum-tax-office-and-the-petroleum-tax-system/petroleum-tax-regulations | via search excerpt |
| S26 | Stortinget, Innst. 179 S (2024–2025) and Innst. 377 S (2025–2026) on ground-rent tax for aquaculture; RSM Norway note | https://www.stortinget.no/globalassets/pdf/innstillinger/stortinget/2024-2025/inns-202425-179s.pdf ; https://stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2025-2026/inns-202526-377s/ ; https://www.rsm.global/norway/nb/node/660 | via search excerpt |
| S27 | Regjeringen, *Resultater fra auksjon av nye oppdrettstillatelser 2024*; iLaks coverage of 2022/2023 auctions | https://www.regjeringen.no/no/aktuelt/resultater-fra-auksjon-av-nye-oppdrettstillatelser-2024/id3046941/ ; https://ilaks.no/mtb-auksjonen-avsluttet-8-243-tonn-ble-solgt-for-15-milliarder-kroner/ | via search excerpt (403) |
| S28 | Salmon pricing: Euronext Salmon Futures page; Fish Pool forward prices page | https://www.euronext.com/en/for-investors/commodities/salmon-futures ; https://fishpool.eu/forward-prices/ | via search excerpt |
| S29 | SalmonBusiness, Mowi Q1 2025 per-kg results; Arctic Securities comment on Mowi EV/kg (Jun 2026) | https://www.salmonbusiness.com/mowi-q1-ebit-rises-to-e214-million-farming-cost-down-to-e5-89-kg/ ; https://www.salmonbusiness.com/arctic-mowi-harvests-may-exceed-guidance-by-6000-tonnes-in-q2/ | via search excerpt |
| S30 | Norges Bank, press release 24 Sep 2026: policy rate raised to 4.50 % | https://www.norges-bank.no/aktuelt/nyheter/Pressemeldinger/2026/2026-09-24-rente/ | Page |
| S31 | Trading Economics, Norway 10Y government bond yield | https://tradingeconomics.com/norway/government-bond-yield | via search excerpt |
| S32 | Næs, Skjeltorp, Ødegaard, *What factors affect the Oslo Stock Exchange?*, Norges Bank WP 24/2009; *Liquidity at the Oslo Stock Exchange*, Norges Bank WP 9/2008 | https://www.norges-bank.no/en/news-events/news-publications/Papers/Working-Papers/2009/WP-200924 ; https://ba-odegaard.no/wps/liquidity_ose/index.html | Abstracts via search |
| S33 | Shipping NAV practice: TradeWinds (2022), Golden Horn dry bulk analysis (Mar 2024), Rubico NAV release (Jun 2026) | https://tradewindsnews.com/finance/streetwise-tanker-investors-have-cleaned-up-in-2022-but-is-the-game-over-or-just-in-early-innings-/2-1-1299130 ; https://goldenhorn.substack.com/p/dry-bulk-equities-analysis-march ; https://www.barchart.com/story/news/4223457/rubico-announces-management-estimate-of-net-asset-value-to-183-1-million-a-94-increase-from-the-previously-reported-nav | via search excerpt |
| S34 | Equinor long-term Brent assumption (Q3 2025 press coverage) | https://www.bairdmaritime.com/offshore/drilling-production/equinor-trims-oil-outlook-after-weaker-than-expected-quarterly-profit ; https://equinor.com/news/equinor-fourth-quarter-and-full-year-2025-results | via search excerpt |
| S35 | Systemic risk buffer: Norges Bank advice 12 May 2026; Finanstilsynet assessment 29 Apr 2026 | https://www.norges-bank.no/aktuelt/nyheter/Brev-og-uttalelser/2026/2026-05-12-systemrisikobuffer/ ; https://www.finanstilsynet.no/contentassets/1fac8d8b67964abca2b13d45448f97f9/vurdering-av-systemrisikobufferen.pdf | via search excerpt |
| S36 | Personal dividend tax (shareholder model): Smartepenger, Nordnet | https://www.smartepenger.no/skatt/601-aksjebeskatning ; https://www.nordnet.no/blogg/dette-bor-du-vite-om-skatt-pa-utbytte | via search excerpt (not Skatteetaten) |
| S37 | BI master thesis (2017), IFRS 16 effects in Norwegian retail | https://biopen.bi.no/bi-xmlui/handle/11250/2479265 | Abstract via search |
| S38 | LBS Valuation programme page | https://london.edu/executive-education/finance/valuation | via search excerpt |
| S39 | Euronext index price lists (OSEBX and sector indices), 2026 | https://live.euronext.com/en/products/indices/sector?page=11 | via search excerpt |

---

## 2. Per framework: statements that can become rules

### 2.1 PwC / FFN survey 2025 – the Norwegian market's own parameters (S1)

FFN (Forening for Finansfag Norge) is the current name of NFF (Norske Finansanalytikeres Forening). S1 and S2 use both names. Figures are for 2025, with page numbers from the report.

| Parameter | 2025 finding | Page |
|---|---|---|
| Market risk premium | Median **5.0 %**, unchanged every year from 2017 to 2025. Mean 5.1 % (2024: 4.9 %). The quartile table (4.2.1) did not extract cleanly, so no quartiles are given here | 4, 9 |
| Required return, liquid OSE share, beta = 1 (new question) | Answers between 8.0 % and 9.0 %, median and mean **8.4 %**. With the 10y NGB at 4.0 % on 1 Nov 2025 this implies an MRP of about 4.4 %, below the directly stated 5.0 % | 4, 10 |
| Risk-free rate | **55 %** use the 10-year government bond (48 % in 2024). **17 %** use a normalised rate, with median **3.5 %**; 90 % of those use ≤ 4.0 %. The 10y NGB was 4.0 % on 1 Nov 2025 | 4, 7 |
| Size ("småbedrifts") premium, used by 67 % | Medians by equity value: > NOK 5 bn **0 %**; 2–5 bn **1 %**; 1–2 bn **2 %**; 0.5–1 bn **2 %**; 0.1–0.5 bn **3 %**; < 0.1 bn **4 %** | 10 (fig. 4.3.2) |
| Illiquidity, **unlisted** shares | 79 % adjust. 55 % use a discount to value (median **20 %**, mean 24 %; 80 % between 15 % and 40 %). 45 % add to the required return (median **2.0 %**, mean 3.5 %) | 12–13 |
| Long-term inflation | Median **2.0 %**, equal to Norges Bank's target | 14 |
| Terminal growth in a DCF | Median **2.0 %**; 58 % answer exactly 2.0 %; the share at ≥ 2.5 % fell to 26 %. Respondents on average set terminal growth equal to expected inflation | 15 |
| Control premium (Oslo Børs) | Median band **20–30 %** | 16 |
| ESG | 58 % adjust cash flow and/or required return for weak ESG performers | 16 |
| Long-run historical MRP | Appendix cites Knivsflå (NHH, 2024): about 5.0 % on average over 1914–2024, varying by up to roughly ±3 % with the cycle (countercyclical) | 19 |
| Double counting | Appendix warning: the premia are asked about one at a time, several can cover the same risk, the required return must be judged as a whole, and any overlap adjustment must be justified by the valuer | 20 |

Rules this supports: rf = 10y NGB by default, normalised rf allowed if labelled. MRP default 5.0 %. A sanity band for total ke at beta 1. A size-premium lookup table. No illiquidity discount for listed liquid shares. g default 2 %, consistent with inflation. Control premium only in takeover cases. Avoid stacking premia.

### 2.2 Ødegaard lecture note (S2) – useful Oslo-specific colour
- The 2018 survey found 73 % think ownership structure affects the required return. The share saying **state ownership** does *not* affect it rose to 59 % (from 48 %). The 2014 survey had 31 % saying state ownership raises it.
- The 2014 survey estimated an implied MRP of 5.6 % for the OBX constituents, based on a 25 % control premium.
- Several 2014 respondents said the risk-free maturity should match the cash-flow duration ("situasjonsbetinget").

### 2.3 NFF/FFN AFA curriculum (S3)
The AFA programme (NHH + FFN) has eight topics. The two that matter here are:
- **Financial statement analysis:** IFRS principles; accounting flexibility and manipulation; **reclassifying the balance sheet and reclassifying and normalising earnings**; ratio analysis (profitability, growth, liquidity); analysis for forecasting and valuation; default probability; accounting-based incentive pay.
- **Valuation:** how markets price claims; strategic analysis, historical trends and competitor analysis; cash-flow forecasting; **CAPM/WACC in practice**; critical use of multiples; **valuing growth companies with scenarios, and handling bankruptcy risk and illiquidity**; synergy valuation; analyst work methods and market efficiency.
- No textbook list is published.

Rule implication: the curriculum expects reorganised statements (operating vs financing), normalised earnings, scenarios for growth companies and an explicit treatment of default and illiquidity. That matches the toolkit's design.

### 2.4 VPFF Industry Standard no. 3 / EU 2016/958 – mandatory content of a Norwegian investment recommendation (S4)
This is the most concrete "rulebook" for the deck builder. Section 4.2.2 points 1–9 restate EU 2016/958 art. 3. Section 4.2.3 restates the art. 4 requirements that depend on report length.

- 4.2.2(1): separate facts clearly from interpretations, assessments and opinions.
- 4.2.2(2): all sources must be reliable; flag any doubt about a source.
- 4.2.2(3): label all forecasts, expectations and target prices as such, and state the material assumptions behind them.
- 4.2.2(5)–(6): say where details on the valuation method and its assumptions can be found, including for proprietary models.
- 4.2.2(7): state the planned update frequency.
- 4.2.2(8): give the **date and time for every price** quoted.
- 4.2.2(9): if the recommendation differs from one issued in the previous 12 months on the same instrument, state the change and the date of the earlier one.
- 4.2.2(10) (VPFF addition): link to the issuer's published sustainability reporting.
- 4.2.3(1)–(2): list all material sources; give the date and time the report was **completed**.
- 4.2.3(3): summarise the valuation basis, method and assumptions behind the TP, and summarise any **changes** to them.
- 4.2.3(4): explain what the rating means (buy/sell/hold) and the **time horizon**, with a risk warning that includes a **sensitivity analysis of the assumptions**.
- 4.2.3(5): list the firm's recommendations on the issuer over the previous 12 months, each with date, analyst, TP, market price at the time, direction and validity period.
- Independence (section 2): recommendations must reflect the analyst's own view. The analyst must not commit in advance to a rating and must not change ratings or estimates without a factual, professional basis.

### 2.5 CFA Institute (S5–S8)
- **V(A) Diligence and reasonable basis** (S5). A reasonable basis covers macro conditions, the company's operating and financial history, industry conditions and **stage of the cycle**, **the output and limitations of quantitative models**, and whether the peer group is appropriate. Analysts must make reasonable efforts to **test model output**. Testing should include a broad range of assumptions, including **negative events and risk levels outside historical data** (example 6: a worst case missing from the historical database). Recommended firm procedure: written minimum standards for scenario testing, including cash-flow sensitivity to inputs. Third-party research must be checked for assumptions, rigour, timeliness and objectivity. Recommendations should be updated when material new information arrives.
- **V(B) Communication** (S6). Disclose the basic format and general principles of the process. Disclose significant limitations and risks. Distinguish fact from opinion: earnings estimates and price views are opinions, and model outputs are estimates, so do not overstate their precision. Keep records so you can explain what was omitted from a report.
- **III(B) Fair dealing** (S7). Any buy/sell/hold opinion is a recommendation. Clients should receive it at about the same time. A changed recommendation must reach everyone. This is mainly relevant to the review-edition workflow (no "pre-release" to selected readers).
- **Research Challenge report format** (S8, Jul 2024). Maximum 10 A4 pages plus a 10-page appendix. The front page must show the company, exchange, ticker, sector, industry, rating, **current price "as of" date** and **TP with % up/downside**. Required sections are Business Description, Industry Overview & Competitive Positioning, Investment Summary, Valuation, Financial Analysis, Investment Risks, ESG. Scoring weights: Valuation 20, Financial Analysis 20, Investment Summary 15, Risks 15, ESG 15, Industry 10, Business Description 5.

### 2.6 McKinsey – Koller, Goedhart, Wessels, *Valuation* 8th ed. (S9–S12)
The book text is not public. What can be verified:
- **Structure** (S9). The 8th edition (May 2025) has separate chapters on ROIC (8), Growth (9), Reorganizing the Financial Statements (11), Estimating Continuing Value (14), Cost of Capital (15), EV to value per share (16), **Analyzing the Results (17)**, Multiples (18), Valuation by Parts (19), Taxes (20), **Leases (22)**, Inflation (26), Cross-Border (27), High-Growth Companies (39), Emerging Markets (41), **Cyclical Companies (42)** and **Banks (43)**. Appendix H is a "Two-Stage Formula for Continuing Value". This confirms the toolkit's module list matches the book's.
- **Key value driver formula** (S12, and widely reproduced): CV = NOPLAT(t+1) × (1 − g/RONIC) / (WACC − g). Implications: growth adds value only if RONIC > WACC; when RONIC = WACC, CV is the same at any g. Critique (S12, Jennergren): in its basic form the formula effectively ignores inflation's effect on existing invested capital, and its constant-parameter assumption is restrictive. Jennergren proposes splitting CV into two value-driver terms (existing operations and new investment).
- **ROIC and growth evidence** (S11, via search excerpt). For about 7,000 US non-financial firms over 1963–2004, median ROIC excluding goodwill averaged close to 10 %, fairly stable and around the cost of capital. The median ROIC of the largest firms stayed about 9 % over 40 years. Real revenue growth of the top 500 faded from about 7 % to about 2 % within about 10 years. **ROIC persists far more than growth does.** Industry ROIC differences are durable (brands, patents).
- **Cyclicals** (S10, via search excerpt). No single forecast can predict the cycle, so use multiple probability-weighted scenarios: (1) a normal-cycle scenario built from past cycles, (2) a new-trend scenario, then weight them. Consensus forecasts **do not predict the cycle** and are consistently too optimistic. Prefer **through-cycle or 2–3-year forward multiples**, since point-in-time multiples mislead.

### 2.7 Damodaran (S13–S18)
- **Growth cap** (S13 slides 12–17; S14). Stable g cannot exceed the growth of the economy, and Damodaran treats this as a mathematical rather than an economic constraint. His practical proxy is **g ≤ the risk-free rate used in the valuation**. A looser version allows **up to rf + 1 pp**. Using the rf handles currency and inflation automatically. A high g with a low rf overvalues, and the reverse undervalues.
- **Growth is not free** (S13 slides 20–27; S18). In stable growth, g = reinvestment rate × ROIC, so **reinvestment rate = g / RONIC**. Example: 3 % / 10 % gives 30 %. If RONIC = cost of capital, TV does not change with g.
- **Two dangerous practices** (S13). (1) "Just grow the final-year FCFF another year." (2) Setting capex = depreciation and ΔNWC = 0 while still assuming growth. Damodaran says about half of all DCFs do the latter. It implies ROIC heads to infinity, and inflation alone makes capex exceed depreciation.
- **Zero excess returns** (S13). Purists set RONIC = WACC in perpetuity. Damodaran sees the logic but notes that excess returns tend to last much longer than high growth does.
- **Exit multiples** (S13 slide 8). An exit multiple taken from today's peer pricing makes a "Trojan Horse DCF". Instead, convert intrinsic inputs into an implied multiple.
- **Finite lives** (S13 slides 5–7). Use a growing annuity or liquidation/salvage value when value comes from a finite-lived asset, such as reserves or a leased site.
- **Negative growth** (S13 slides 29–35). It is legitimate. In 2015, 79.22 % of oil and gas E&P firms in his sample had negative revenue growth. With asset sales, the reinvestment rate can be negative: g / ROC with g < 0.
- **Country/ERP data** (S15, updated 5 Jan 2026). Norway is Aaa, with country risk premium 0.00 % and total ERP **4.23 %**, the same as the mature-market ERP implied in the table. For comparison, the US is Aa1 with CRP 0.23 % and ERP 4.46 %.
- **Commodity companies** (S16). Don't extrapolate the current year's cycle position. Normalise over a full cycle (cycles run from 2–3 years to more than 10). For firms that changed size, average **ratios** (margins, capex/revenue) rather than absolute amounts. With short histories, use sector-average margins. A normalised commodity price above spot makes the stock look cheap: the valuation then reflects your commodity view more than your view of the company. The "safest" approach is market prices: **spot for the current year and forwards/futures for later years**.
- **Financial service firms** (S17, Apr 2009). Use **equity** models (DDM, FCFE adapted for regulatory capital, excess-return model), not EV/FCFF, because debt, capex and working capital are not definable for banks. Reinvestment includes the regulatory capital needed to grow, so a growing bank cannot pay out 100 %. The two key drivers are cost of equity and ROE, and ROE depends partly on regulation. Excess-return model: equity value = book equity today + PV of future excess returns, where excess return = (ROE − ke) × book equity. Price/sales cannot be used for banks.

### 2.8 Mauboussin and Rappaport – reverse DCF, CAP (S19–S21)
- **Expectations investing** (S21). Start from the price and solve for the price-implied expectations (PIE) for sales growth, operating margin, investment rate and cost of capital. Then compare those expectations with your own view instead of forecasting first.
- **CAP** (S19, 1997). CAP is the period over which a company earns returns on incremental investment above its cost of capital. After the CAP no value is created, so the model uses a perpetuity of NOPAT/WACC (no growth premium). Market-implied CAP (MICAP) is found by extending the explicit forecast until DCF value equals the market price, using unbiased (consensus) inputs. In 1997 the US market's CAP was estimated at **10–15 years**, with individual firms ranging from **0–2 years to over 20**. Low-multiple companies tend to have short CAPs. Packaged food industry MICAPs were 14–16 years. An updated version (S20) was published by Morgan Stanley Counterpoint Global on 14 Apr 2026, but only the landing page was seen.

### 2.9 SOTP and conglomerate discount (S22)
- The evidence is mixed. A CBS thesis's literature review found strongly contradictory results and only weak evidence of a global discount, and concluded that a universal, non-company-specific discount is "somewhat erroneous". A NOVA field lab found a 9 % discount for Honeywell, which it called lower than commonly observed. Practitioner sources quote 10–25 %, but these are secondary and the classic Berger–Ofek figures were not verified.
- Mechanics: value each subsidiary with its own method, multiply by the ownership share, sum, then subtract holding costs and net debt at the holding level.
- Rule implication: a holding discount must be explicit, company-specific and justified. Don't apply it silently.

### 2.10 Leases (S23, S9 chapter 22, S37)
- Under IFRS 16, lease costs move out of EBITDA. If lease liabilities are in net debt, EBITDA must be the post-IFRS 16 figure. For legacy or pre-IFRS 16 comparisons, add lease expense back (or deduct it from EBITDA) and use **EBITDAaL** for lease-heavy sectors. **Standardise the lease treatment across all peers and transactions.** Match cash flows and discount rate on the same basis (pre or post IFRS 16), with lease gearing included in WACC only if lease liabilities are treated as debt. When lease payments are excluded from operating cash flow, include ROU replacement in the terminal year (S23).
- A BI study of Norwegian retailers (S37) found capitalising leases raises EBITDA, EBIT and NOPLAT but likely lowers ROIC and ROCE.

### 2.11 LBS
I could not reach a public page for an LBS "Corporate Finance Programme" listing modules (accounting and financial analysis, valuation, financial strategies). The LBS Valuation programme page (S38, via search excerpt) lists stocks, bonds, cross-border investments, real-asset NPV, cost of capital and capital market behaviour. No rule-level content. See the final section.

---

## 3. Oslo Børs specifics

### 3.0 Market-wide facts

- **Rates.** Norges Bank raised the policy rate to **4.50 %** (from 4.25 %), decided 23 Sep 2026 and in force from 25 Sep 2026. Guidance is to stay around this level for a while before easing gradually, with inflation reaching 2 % in 2029. The next decision is 5 Nov 2026 (S30). The 10y NGB was 4.0 % on 1 Nov 2025 (S1 p. 7). It was quoted at 4.36 % on 7 Apr 2026, after a March 2026 high of 4.48 %, the highest since 2008 (S31, via search excerpt). **No October 2026 quote was found.** The toolkit must take it as a dated input.
- **Factor structure.** For 1980–2006, a three-factor model (market, size, **liquidity**) fits OSE returns reasonably well. The oil price drives sector **cash flows** but is **not a priced risk factor** (S32, WP 24/2009). Liquidity improved over time, mostly for the largest firms. Spreads are countercyclical (S32, WP 9/2008).
  - Implications: model oil exposure in cash flows and scenarios, not as a ke add-on. Size and liquidity premia have empirical support on OSE, which fits the survey practice in S1.
- **Small and illiquid names.** Use the PwC/FFN size medians (S1) for listed small caps. The 20 % / +2 % illiquidity figures are for **unlisted** shares and should not be applied to liquid listed shares (S1 p. 12).
- **State ownership.** In surveys, a majority do not adjust ke for state ownership (S2).
- **Control premium.** Median 20–30 % (S1). Relevant for takeover-scenario TPs only.
- **Personal dividend tax (shareholder model).** Dividends and gains are grossed up by 1.72 for 2025 and 2026, giving 37.84 % effective (22 % × 1.72), before the shielding deduction (skjermingsfradrag) (S36, secondary; Skatteetaten not checked). [judgement] CAPM-based ke in S1 is stated before personal tax. Keep personal tax out of the company DCF and mention it only in a shareholder-return discussion.
- **Sector moves in 2026** (S39, via search excerpt; index price lists, not weights). By Jul–Sep 2026 the Seafood index was down roughly 12–16 % YTD, while the Shipping and Oil Service indices were up roughly 50–76 % YTD. **OSEBX sector weights were not found.**

### 3.1 Salmon farming (Mowi, SalMar, Lerøy, Grieg, Bakkafrost, etc.)

| | |
|---|---|
| **Value drivers** | Salmon price (spot per kg and the forward curve), harvest volume (tonnes gutted weight), farming cost per kg, EBIT/kg by region (Mowi reports this by country, S29), licence capacity (MAB/MTB), biology (mortality, lice). |
| **Standard approach** | EV/kg capacity or harvest checked against EBIT/kg. Example: an Arctic Securities comment (Jun 2026) put Mowi at about NOK 230 EV/kg, against about NOK 23 EBIT/kg in good years, or about 10× EV/EBIT (S29, via search excerpt). DCF on price × volume − cost per kg, with the ground-rent tax modelled separately. Licence value as a cross-check on asset value. |
| **Key numbers to model** | **Price deck:** the Euronext Salmon Future settles in cash against the weekly SISALMONI index (Sitagri). Fish Pool says its forward prices are indications only (S28). **Cost/kg and EBIT/kg:** Mowi Q1 2025 farming cost was €5.89/kg; operational EBIT/kg was €2.50 in Norway, €1.80 in Scotland and €0.90 in Chile (S29). **Ground-rent tax:** effective rate **25 %**, agreed May 2023 and applying from income year 2023. The government had proposed 40 %. It covers salmon, trout and rainbow trout (S26). Ground-rent income is taxed with the ordinary 22 % plus the ground-rent tax. Because corporate tax is deducted first, the formal rate is above the effective rate; the 2022 proposal's example was 51.3 % × (1 − 0.22) = 40 %. By the same arithmetic, 25 % effective ≈ 32 % formal [derived]. **Norm price:** in effect from 1 Jul 2024, set by an independent council (Normprisrådet) to reflect market value at the pen edge. A Storting majority in Innst. 377 S (2025–26) wants to abolish the council from income year 2027. **Final status not verified** (S26). **Licence prices:** the 2024 auction sold 17,330 t MTB for NOK 5,288.6 m (S27), or about NOK 305k per tonne MTB [derived]. Mowi paid NOK 246k/t and SalMar NOK 278k/t. The October 2023 re-auction cleared at NOK 181,972/t (S27). |
| **Typical traps** | Applying a flat 22 % tax to Norwegian farming profit (it ignores ground rent). Using one spot price for the whole forecast instead of spot, then forwards, then a stated long-term price (S16). Treating Norwegian and other regions' EBIT/kg as interchangeable (S29). Ignoring that forward prices are indications in a thin market (S28). [judgement] Mixing EUR prices with NOK reporting without an explicit FX path. |

### 3.2 Oil & gas E&P (Equinor, Aker BP, Vår Energi, smaller NCS names)

| | |
|---|---|
| **Value drivers** | Oil and gas price deck, production profile, reserves (finite life), opex/boe, capex, **petroleum tax**, USD/NOK. |
| **Standard approach** | [judgement, common practice] Field-by-field NAV/RNAV with finite-life cash flows, not a perpetuity. Damodaran supports annuity or liquidation TVs for finite-lived assets (S13). Cross-check with EV/DACF or EV/2P. |
| **Key numbers to model** | **Tax** (S24, page updated 08.10.2026): corporate tax 22 % plus special tax 71.8 %, with corporate tax deductible in the special-tax base, giving a 78 % marginal rate. Since 2022 the special tax is a **cash-flow tax**: investments are expensed immediately in the special-tax base. The uplift was cut to 12.4 % in the 2023 budget. Financing costs are not deductible in the special-tax base. The special-tax value of losses is **refunded**. Losses and exploration costs can be offset across fields on the NCS. The Petroleum Price Council sets norm prices for oil sold to affiliates; gas uses actual prices. **Price deck:** Damodaran's "safest" approach is spot, then forwards (S16). Equinor's long-term Brent assumption was reported at USD 75/bbl for 2030–2040, down from 80 at the start of the decade (Q3 2025, press coverage; Equinor's own table not read) (S34). Equinor's 2025 net impairments were USD 2,481 m, partly from updated price assumptions (S34). |
| **Typical traps** | Applying 22 % tax to NCS profits. Using a perpetuity TV on depleting reserves (S13). Normalising the oil price above the forward curve and calling the result "undervalued", which is really a commodity call (S16). Assuming oil is a priced risk factor in ke; on OSE it shows up in cash flows (S32). Positive perpetual growth in a sector where most firms have shrinking revenue (S13). Currency mismatch: USD cash flows discounted at a NOK rate (S14). |

### 3.3 Oil service (drillers, subsea, supply vessels, equipment)

| | |
|---|---|
| **Value drivers** | Customer capex cycle, utilisation and day rates, backlog, fleet/asset values, leverage. |
| **Standard approach** | Cyclical approach (S10): probability-weighted normal-cycle and new-trend scenarios; through-cycle or 2–3-year forward multiples; normalised margins averaged as ratios (S16). Asset-heavy names are cross-checked against asset values, as for shipping. |
| **Key numbers** | Through-cycle EBITDA margin, utilisation, backlog cover, net debt/EBITDA. [judgement] No sourced sector-specific benchmarks were found. |
| **Typical traps** | Extrapolating peak-year earnings. In 2026 the Oil Service index was up roughly 50–76 % YTD (S39, price data), which makes the current year a high point to anchor on. Relying on consensus, which misses the cycle and is biased upward (S10). |

### 3.4 Shipping (tankers, dry bulk, gas carriers, car carriers, containers)

| | |
|---|---|
| **Value drivers** | Spot and time-charter rates (TCE), fleet supply (orderbook, scrapping), second-hand vessel values, leverage, dividend policy. |
| **Standard approach** | **P/NAV.** NAV = book equity − book value of vessels + market value of vessels, with vessel values from **charter-free broker valuations** (S33). DCF and earnings yield are secondary cross-checks. |
| **Key numbers** | Broker vessel values per ship, net debt, charter coverage and backlog, cash breakeven. Leverage amplifies NAV moves: a 2022 estimate put a 32 % rise in asset values at about a 50 % rise in listed NAVs (S33). A March 2024 dry-bulk sample traded at an average P/NAV of 0.73 (S33). |
| **Typical traps** | USD reporting with a NOK listing (rule: value in USD with a USD rf, then convert at spot) (S14). Treating P/NAV < 1 as automatically cheap; markets lag rate and asset-value cycles (S33). Using a perpetuity on an ageing fleet without replacement capex (S13 dangerous practice 2). |

### 3.5 Banks (DNB, SpareBank 1 banks, other savings banks)

| | |
|---|---|
| **Value drivers** | ROE vs cost of equity, loan growth, losses, CET1 requirement and excess capital, payout. |
| **Standard approach** | Equity models: DDM, FCFE where reinvestment is the regulatory capital needed for growth, or the excess-return model (S17). Multiples: P/B against ROE, and P/E. Not FCFF/WACC and not P/S (S17). [derived from S17's excess-return model] With constant parameters, P/B = (ROE − g)/(ke − g), so P/B > 1 only if ROE > ke. |
| **Key numbers** | ROE, ke (CAPM with S1 inputs), CET1 ratio vs requirement. The **systemic risk buffer is 4.5 %**, kept in the Ministry's 2024 decision and applying to banks, mortgage companies and finance companies. A 2026 review is under way (Finanstilsynet letter 29 Apr 2026, Norges Bank advice 12 May 2026), and Norges Bank highlighted household debt and commercial-property exposure (S35). **The current countercyclical buffer level and any 2026 decision were not verified.** |
| **Typical traps** | Running the industrial FCFF template on a bank (S17). Assuming 100 % payout with growth (S17). Ignoring that equity-certificate (EK-bevis) savings banks have a different ownership structure [judgement, not researched]. |

### 3.6 Consumer / retail (e.g. Europris, XXL, Kid, SATS-type service retailers, discount and outlet retailers)

| | |
|---|---|
| **Value drivers** | Like-for-like growth, gross margin, store roll-out economics, rent, working capital (inventory), lease commitments. |
| **Standard approach** | FCFF DCF plus EV/EBIT, P/E or EV/EBITDAaL peer multiples. Lease treatment has to be consistent (S23). |
| **Key numbers** | Lease liabilities and rent (pre-IFRS 16 rent cost), inventory days, capex per new store, ROIC with and without leases. Capitalising leases raises EBITDA, EBIT and NOPLAT and lowers ROIC (S37). |
| **Typical traps** | Mixing a post-IFRS 16 EBITDA with an EV that excludes lease debt, or the reverse. Peers on different lease bases (S23). Missing ROU replacement in the terminal year when leases are excluded from FCF (S23). Roll-out growth assumed free (no capex/NWC per store), which is the Damodaran reinvestment rule at segment level (S13). |

### 3.7 Technology / growth (software, energy-transition tech, health-tech)

| | |
|---|---|
| **Value drivers** | Revenue growth, path to target margin, reinvestment (sales-to-capital), dilution, survival risk. |
| **Standard approach** | Scenario DCF with explicit failure risk (AFA curriculum, S3; McKinsey ch. 39, S9). **Reverse DCF and market-implied CAP** to show what the price already assumes (S19, S21). |
| **Key numbers** | Implied revenue CAGR or margin at the current price, implied CAP vs the 10–15-year market reference (1997) (S19), cash runway. |
| **Typical traps** | Perpetual g above rf (S14). Long high growth with no reinvestment (S13). Size and liquidity premia omitted for small OSE caps (S1, S32). [judgement] Ignoring dilution from options or warrants. |

---

## 4. Candidate rule list (40)

Auto = can be an automated check in the Excel model or deck builder. **Yes** = hard check, **Warn** = soft warning, **Report** = show the figure with no threshold, **No** = needs judgement or a reviewer.

| # | Rule | Source | Auto |
|---|---|---|---|
| **Cost of capital** ||||
| R1 | rf = 10y NGB yield at a stated date. A normalised rf is allowed only if labelled as such and shown next to the spot yield. | S1 p. 7; S2 | Yes (date + value required; label if ≠ spot) |
| R2 | Default MRP = 5.0 %. Warn outside 4.0–6.0 % ([judgement] band around the median). Show Damodaran's ERP for Norway (4.23 %, Jan 2026) as a second opinion. | S1 p. 8–9; S15 | Warn |
| R3 | Check total ke for a beta-1 share against the survey's 8.0–9.0 % (median 8.4 %). Flag rf + MRP outside that band. | S1 p. 10 | Warn |
| R4 | Size premium from the PwC/FFN lookup by equity value (0/1/2/2/3/4 %). Deviations must be justified. | S1 p. 10 | Yes (lookup + flag) |
| R5 | No illiquidity discount on liquid listed shares. For unlisted: median 20 % discount **or** +2 % ke, never both. | S1 p. 12–13 | Yes |
| R6 | Don't stack premia (size + illiquidity + ESG + company-specific) without an overlap note. | S1 p. 20 | Warn (more than one add-on → note required) |
| R7 | Currency consistency: the rf currency must equal the cash-flow currency. USD cash flows (E&P, shipping) need a USD rf, then conversion at spot. | S14; S13 slide 13 | Yes |
| R8 | Oil exposure goes into cash flows and scenarios, not into a ke add-on. | S32 | No (reviewer) |
| R9 | Control premium (20–30 % median) only in an explicit takeover scenario, never in the base TP. | S1 p. 16 | Yes (flag if used in base) |
| **Terminal value** ||||
| R10 | g ≤ rf (hard). g ≤ rf + 1 pp is the absolute ceiling. | S14; S13 slide 14 | Yes (error) |
| R11 | Default g = 2.0 % (survey median = inflation target). Warn if g > 2.5 %. | S1 p. 14–15 | Warn |
| R12 | TV by value driver: NOPLAT(t+1) × (1 − g/RONIC) / (WACC − g). The implied reinvestment rate must equal g/RONIC. | S12; S13 slides 21–22; S18 | Yes |
| R13 | No growth without reinvestment: if g > 0, then capex > D&A or ΔNWC > 0 in the TV year. | S13 slide 26 | Yes (error) |
| R14 | RONIC ≥ WACC unless explicitly value-destroying, and RONIC ≤ the explicit-period ROIC. Show the "RONIC = WACC" TV next to the base case. | S13 slides 23–24; S11; S19 | Yes |
| R15 | The TV base year must be normalised (margin, capex, NWC). Don't simply grow the last forecast year's FCFF. | S13 slide 25; S16 | Warn (TV-year margin vs through-cycle average shown) |
| R16 | DCF is primary. Exit multiples are cross-checks only. Show the **implied** EV/EBITDA and EV/EBIT at the TV. | S13 slide 8 | Report + Yes (block exit-multiple TV as primary) |
| R17 | Report TV as a % of EV. | S13 ("tail that wags the dog") | Report |
| R18 | Finite-life assets (reserves, time-limited concessions, leased sites) get an annuity or liquidation TV, not a perpetuity. | S13 slides 5–7 | Yes (sector switch) |
| R19 | Negative g is allowed for declining businesses, with a reinvestment rate of g/ROC (negative = asset release). | S13 slides 29–35 | Yes (consistency check) |
| R20 | Keep real and nominal consistent: inflation in the cash flows matches the inflation implied by rf (about 2 % target). | S14; S1 p. 14 | Warn |
| **Forecast, cyclicals and commodities** ||||
| R21 | Cyclicals: probability-weighted scenarios (normal cycle + new trend), with probabilities summing to 1. | S10 | Yes |
| R22 | Normalise on ratios (margins, capex/sales) averaged over a full cycle, not absolute averages, for firms that changed size. | S16 | Yes (through-cycle ratio block) |
| R23 | Commodity deck: spot for year 1, forwards for later years, then a stated long-term price. Record the source and date for each price. | S16; S28; S34 | Yes (price deck sheet) |
| R24 | If the LT commodity price is above the forward curve, show value at the forward curve as well, and label the gap as a commodity view. | S16 | Yes |
| R25 | Peer multiples for cyclicals: through-cycle or 2–3-year forward, not spot trailing. | S10 | Yes (peer table columns) |
| R26 | Don't anchor on consensus for cyclicals. Warn if a cyclical's forecast rises every year with no down year. | S10 | Warn |
| **Expectations and SOTP** ||||
| R27 | Always run a reverse DCF: solve for implied revenue CAGR or margin at the current price. | S21 | Yes |
| R28 | Report market-implied CAP. Reference ranges: market 10–15 years, firms 0–2 to over 20 (1997 US data, context only). | S19 | Report |
| R29 | SOTP: own method per segment × ownership share. Any holding discount must be an explicit, justified line, with no default value. | S22 | Yes (line required; warn if blank without a note) |
| **Leases** ||||
| R30 | Lease consistency triangle: EBITDA basis, net-debt definition and WACC gearing must all be pre-IFRS 16 or all post-IFRS 16. | S23; S9 ch. 22 | Yes |
| R31 | Peers on the same lease basis as the target (EBITDAaL for lease-heavy sectors). | S23 | Warn (peer lease flag) |
| R32 | If lease payments are excluded from FCF, include ROU replacement in the TV year. | S23 | Yes |
| **Sector and Norway-specific** ||||
| R33 | Salmon: Norwegian farming profit is taxed at 22 % plus ground-rent tax (25 % effective, since 2023). Check the norm-price regime and its 2027 status before publishing. | S26 | Yes (sector tax switch) |
| R34 | NCS E&P: 78 % marginal tax (22 % + 71.8 %), with immediate expensing in the special-tax base and a refundable special-tax value of losses. Never a flat 22 %. | S24; S25 | Yes (sector tax switch) |
| R35 | Banks: equity valuation (DDM, FCFE or excess return), no FCFF/WACC, no P/S. Payout must leave enough capital to keep CET1 ≥ requirement given loan growth. | S17; S35 | Yes (template switch + CET1 path check) |
| R36 | Shipping and asset-heavy offshore: show P/NAV from dated broker (charter-free) vessel values beside the DCF. | S33 | Report |
| **Communication (deck builder)** ||||
| R37 | Front page: rating, current price with **date and time**, TP with % up/downside, time horizon, and what the rating means. | S4 4.2.2(8), 4.2.3(4); S8 | Yes |
| R38 | Mark forecasts and TP as opinions. Keep fact and opinion visibly separate. List the material sources and the completion date and time. | S4 4.2.2(1–3), 4.2.3(1–2); S6 | Yes (template fields) |
| R39 | Risk section with a **sensitivity analysis of the key assumptions** (WACC × g at minimum, plus the main operating driver) and at least one downside scenario outside the historical range. | S4 4.2.3(4); S5 | Yes |
| R40 | Change log: if the TP or rating changed within 12 months, state the previous TP and rating, the date and the reason. Keep a 12-month history table. | S4 4.2.2(9), 4.2.3(3), 4.2.3(5) | Yes |

Also considered but left out of the 40: the issuer's sustainability-report link (S4 4.2.2(10)); the CFA Research Challenge section order (S8); planned update frequency (S4 4.2.2(7)); fair dissemination of the review edition (S7). All of these are easy template fields.

---

## Det som ikke lot seg finne offentlig

- **The NFF/FFN AFA curriculum in full.** Only the eight-topic outline and the course descriptions are public (S3). No reading list, lecture notes or exam material. I found no "NFF recommendations on valuation" document. The FFN's public valuation-parameter output is the PwC survey (S1). NFF's historical public outputs that turned up were corporate-governance (NUES) and consultation responses, not valuation standards.
- **McKinsey *Valuation*, 8th ed.** Only the table of contents is public (S9). The book's actual continuing-value guidance (RONIC defaults, fade, inflation-adjusted CV in Appendix H), the lease chapter and the "Analyzing the Results" checks were not available. McKinsey's own articles (S10, S11) timed out, so their content here comes from search excerpts.
- **PwC/FFN raw data and a 2026 edition.** The 2026 survey had not been found by 22 Oct 2026 (the 2025 survey ran in Oct–Nov 2025). pwc.no blocks automated fetching. Part of the 2022–2025 size-premium table (4.3.3) was garbled in the text extraction, so only the 2025 medians in figure 4.3.2 are used.
- **Damodaran: narrative ("story to numbers", possible/plausible/probable), young growth companies, the 2026 ERP paper.** These were not reached because the session's search limit ran out. Only the country ERP table (S15) was read; the US implied ERP of 4.23 % for Jan 2026 matched it, but that came from a secondary summary.
- **Mauboussin/Rappaport** *Expectations Investing* text and the 2026 Counterpoint CAP update. Only the 1997 CAP paper (S19) and secondary summaries were read.
- **LBS Corporate Finance programme module content.** There is no public module list for a programme of that name. Only the LBS Valuation programme summary (S38) was found.
- **OSEBX sector weights (2026).** The Euronext factsheet returned 403. Only index price moves were seen (S39).
- **10y NGB yield for October 2026.** The latest quote seen was from April 2026 (S31). It must be entered manually with a date.
- **Countercyclical buffer level and the 2026 systemic-risk-buffer decision** (S35). Not verified.
- **Primary Equinor or Aker BP price-deck tables** (real or nominal, 2040+). Only press coverage was seen (S34).
- **Salmon:** the outcome of the proposal to abolish the norm-price council from 2027, and any 2025 or 2026 licence auction results (S26, S27). Regjeringen pages returned 403.
- **Broker sector methodology.** I found no public, authoritative description of how Oslo brokers (Pareto, DNB Carnegie, Arctic, SB1 Markets) model oil service, shipping or tech. Section 3 combines general frameworks with single public examples.
- **Skatteetaten primary source on the shareholder model** (1.72 / 37.84 % for 2025–26) and the 2026 shielding rate. Only secondary sources were seen (S36).
- **The classic conglomerate-discount studies** (Berger–Ofek 1995, Lang–Stulz 1994). Not read. Practitioner ranges in S22 are secondary.
