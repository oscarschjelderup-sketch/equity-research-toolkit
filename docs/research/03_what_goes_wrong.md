# 03 - What goes wrong: analyst errors on Oslo Børs, the evidence on analyst biases, and 30 checks a DCF tool can run

Researcher 3 of 4. Written 22 Oct 2026 for the Equity Research Toolkit (Excel DCF model + deck builder, `verify_dcf.py`, `stress_test.py`, `case_gate.py`).

Purpose: turn documented analyst failures, the regulation that binds analysts, and the academic record on analyst bias into concrete checks the toolkit can run before a case is pitched. Everything below is paraphrased from the sources listed. Nothing is invented; where a number could not be confirmed in a source that was actually opened, it is left out and listed in the last section.

---

## 1. Method and sources

**How the work was done (22 Oct 2026).**

1. Web search (several parallel queries in Norwegian and English) for press coverage of Oslo Børs cases (E24, DN, Finansavisen, iLaks, Reuters and others), Finanstilsynet supervisory reports, VPFF industry standards, EU legislation, and academic abstracts.
2. Pages were then opened (WebFetch) where possible. PDFs that the fetcher could not read were downloaded and their text extracted locally (Finanstilsynet's Arctic Securities report, VPFF Standard 3, Credit Suisse's *Base Rate Book*).
3. Two helper searches ran in parallel on the case list (energy/industrial names and consumer/tech/biotech names) under the same rules: dated source, named broker, no unsourced numbers.
4. The existing check list in the toolkit's `Checks` sheet (30 checks, read from `examples/SATS/SATS_ASA_DCF_Model.xlsx`) was read so that section 5 says which failure modes are already covered and which are new.
5. Limits: the session's web-search budget ran out before every lead could be followed. Some press articles are behind paywalls (DN, Finansavisen) and only their headline or search snippet could be seen. These are marked "snippet only".

Evidence grading used below: **[read]** = page or PDF opened and the figure seen in it; **[abstract]** = figure from the abstract or the publisher/repository listing; **[snippet]** = seen only in a search-result snippet, not verified on the page; **[read by helper]** = opened by one of the two helper searches and reported back with its URL. Eight helper pages were re-opened and confirmed in this session (gCaptain on Seadrill; E24 on REC Silicon 7 Nov 2024 and 2 Jan 2025, Kahoot, XXL, Nordic Semiconductor, Crayon, Ultimovacs); those carry the tag [read].

### Source list (all accessed 22 Oct 2026)

Regulation and supervision

| # | Source | URL |
|---|---|---|
| R1 | Finanstilsynet, "Investeringsanbefalinger" (rules page; MAR art. 20, 2016/958, sanctions) | https://finanstilsynet.no/tilsyn/markedsatferd/investeringsanbefalinger |
| R2 | Finanstilsynet, letter/report to Arctic Securities AS, "Undersøkelse av egenhandler gjennomført av analytikere", ref. 20/12305, dated 14.04.2021 (PDF, 21 pages) | https://www.finanstilsynet.no/contentassets/fca87ea51d464c038c4b31511f0abd05/undersokelse-av-egenhandler-gjennomfort-av-analytikere-arctic-securities-as.pdf |
| R3 | Finanstilsynet news page for R2 | https://www.finanstilsynet.no/nyhetsarkiv/tilsynsrapporter/2021/undersokelse-av-egenhandler-gjennomfort-av-analytikere/ |
| R4 | Finanstilsynet annual report 2022, securities firms chapter | https://www.finanstilsynet.no/publikasjoner-og-analyser/arsrapport/arsrapport-2022/rapporter-fra-tilsynsomradene-for-2022/verdipapirforetak/ |
| R5 | Finanstilsynet, "Tilsynsrapport - Arctic Securities AS" (2022) | https://www.finanstilsynet.no/nyhetsarkiv/tilsynsrapporter/2022/tilsynsrapport---arctic-securities-as/ |
| R6 | Finanstilsynet, "Tilsynsrapport - Pareto Securities AS" (2022, Euronext Growth Advisor) | https://www.finanstilsynet.no/nyhetsarkiv/tilsynsrapporter/2022/tilsynsrapport---pareto-securities-as/ |
| R7 | Finanstilsynet, "Tilsynsrapport - Pareto Securities" (2023, placements and market soundings) | https://www.finanstilsynet.no/nyhetsarkiv/tilsynsrapporter/2023/tilsynsrapport---pareto-securities/ |
| R8 | Finanstilsynet, "Finanstilsynet publiserer vedtak som gjelder overtredelse av reglene om markedsatferd" (2021) | https://www.finanstilsynet.no/nyhetsarkiv/nyheter/2021/finanstilsynet-publiserer-vedtak-som-gjelder-overtredelse-av-reglene-om-markedsatferd |
| R9 | Finanstilsynet, "Regler for investeringsanbefalinger gjelder for finfluensere" (2021) | https://finanstilsynet.no/nyhetsarkiv/nyheter/2021/regler-for-investeringsanbefalinger-gjelder-for-finfluensere |
| R10 | Finanstilsynet, "Finanstilsynet presiserer at reglene for investeringsanbefalinger også gjelder for privatpersoner" (2022) | https://finanstilsynet.no/nyhetsarkiv/nyheter/2022/finanstilsynet-presiserer-at-reglene-for-investeringsanbefalinger-ogsa-gjelder-for-privatpersoner |
| R11 | Finanstilsynet, "Investeringsanbefalinger som legges ut på sosiale medier - advarsel fra ESMA" (2024) | https://finanstilsynet.no/nyhetsarkiv/nyheter/2024/investeringsanbefalinger-som-legges-ut-pa-sosiale-medier--advarsel-fra-esma |
| R12 | Finanstilsynet, "MAR: Dokumentere investeringsanbefalinger" | https://prod.finanstilsynet.no/rapportering/fellesrapporteringer/mar-dokumentere-investeringsanbefalinger |
| R13 | Regjeringen, "Ikraftsetting av endringer i verdipapirhandelloven (markedsmisbruk, tilsyn og sanksjoner)" | https://www.regjeringen.no/no/aktuelt/ikraftsetting-av-endringer-i-verdipapirhandelloven-markedsmisbruk-tilsyn-og-sanksjoner/id2787828/ |
| R14 | Commission Delegated Regulation (EU) 2016/958, art. 4 (objective presentation, additional obligations) | https://www.legislation.gov.uk/eur/2016/958/article/4/adopted |
| R15 | Commission Delegated Regulation (EU) 2016/958, art. 6 (conflict disclosures, additional obligations) | https://www.legislation.gov.uk/eur/2016/958/article/6/adopted |
| R16 | Regulation (EU) 596/2014 (MAR), art. 20 | https://www.legislation.gov.uk/eur/2014/596/article/20/adopted/data.html |
| R17 | Verdipapirforetakenes Forbund, Bransjestandard nr. 3 "Analyseavdelingens uavhengighet og integritet", revised 25 Nov 2025, in force 1 Feb 2026 (PDF, 17 pages) | https://www.vpff.no/images/Standard-3-Analyseavdelingens-uavhengighet-og-integritet-feb-2026.pdf |
| R18 | Affärsvärlden, "Arctic Securities-anställd häktad för insiderhandel" (Mar 2026, citing E24) | https://www.affarsvarlden.se/artikel/arctic-securities-anstalld-haktad-for-insiderhandel |
| R19 | Aktiespararna, "Arctic Securities-anställd häktad i insiderutredning" (Mar 2026) | https://www.aktiespararna.se/nyheter/arctic-securities-anstalld-haktad-i-insiderutredning |

Academic and practitioner evidence

| # | Source | URL |
|---|---|---|
| A1 | Bradshaw, Brown & Huang (2013), *Review of Accounting Studies* 18(4) | https://ideas.repec.org/a/spr/reaccs/v18y2013i4d10.1007_s11142-012-9216-5.html |
| A2 | Brav & Lehavy (2003), *Journal of Finance* 58(5) | https://scholars.duke.edu/publication/762064 |
| A3 | Asquith, Mikhail & Au (2005), *Journal of Financial Economics* 75(2); NBER w9246 | https://www.nber.org/papers/w9246 |
| A4 | Bonini, Zanetti, Bianchini & Salvi (2010), *Journal of Business Finance & Accounting* 37(9-10) | https://ideas.repec.org/a/bla/jbfnac/v37y2010i9-10p1177-1217.html |
| A5 | Gleason, Johnson & Li (2013), *Contemporary Accounting Research* 30(1); University of Iowa release 9 Dec 2013 | https://now.uiowa.edu/news/2013/12/more-rigor-more-cash |
| A6 | Bradshaw (2004), *The Accounting Review* 79(1) | https://academicnewsletter.sufe.edu.cn/info/416180 |
| A7 | Michaely & Womack (1999), *Review of Financial Studies* 12(4); Cornell release 5 Jul 2000 | https://ideas.repec.org/a/oup/rfinst/v12y1999i4p653-86.html ; https://news.cornell.edu/node/279454 |
| A8 | Lin & McNichols (1998), *Journal of Accounting and Economics* 25 | https://www.gsb.stanford.edu/faculty-research/publications/underwriting-relationships-analysts-earnings-forecasts-investment |
| A9 | Dechow, Hutton & Sloan (2000), *Contemporary Accounting Research* 17(1) | https://ideas.repec.org/a/wly/coacre/v17y2000i1p1-32.html |
| A10 | Chan, Karceski & Lakonishok (2003), *Journal of Finance* 58(2); NBER w8282 | https://www.nber.org/papers/W8282 |
| A11 | Bordalo, Gennaioli, La Porta & Shleifer (2019), *Journal of Finance* 74(6) | https://shleifer.scholars.harvard.edu/publications/diagnostic-expectations-and-stock-returns-0 |
| A12 | Easterwood & Nutt (1999), *Journal of Finance* 54(5) | https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1777-1797.html |
| A13 | Richardson, Teoh & Wysocki (2004), *Contemporary Accounting Research* 21(4) | https://ideas.repec.org/a/wly/coacre/v21y2004i4p885-924.html |
| A14 | Hong, Kubik & Solomon, "Security Analysts' Career Concerns and Herding of Earnings Forecasts" (SSRN working paper version) | https://papers.ssrn.com/abstract=142895 |
| A15 | Jegadeesh & Kim (2010), *Review of Financial Studies* 23(2) | https://ideas.repec.org/a/oup/rfinst/v23y2010i2p901-937.html |
| A16 | Cen, Hilary & Wei (2013), *Journal of Financial and Quantitative Analysis* 48(1) | https://ideas.repec.org/a/cup/jfinqa/v48y2013i01p47-76_00.html |
| A17 | Barber, Lehavy, McNichols & Trueman (2006), *Journal of Accounting and Economics* 41(1-2) | https://www.gsb.stanford.edu/faculty-research/publications/buys-holds-sells-distribution-investment-banks-stock-ratings |
| A18 | Kadan, Madureira, Wang & Zach (2009), *Review of Financial Studies* 22(10) (citation only) | https://openresearch-repository.anu.edu.au/items/3fa9a21d-6530-420e-a488-643170b69dfa |
| A19 | Alquist & Kilian (2010), *Journal of Applied Econometrics* 25(4) | https://deepblue.lib.umich.edu/handle/2027.42/75776 |
| A20 | Mauboussin, Callahan & Majd, *The Base Rate Book*, Credit Suisse, 26 Sep 2016 (PDF copy; text extracted and read) | https://josephnoko.com/wp-content/uploads/2024/04/The-Base-Rate-Book-Michael-Mauboussin.pdf |
| A21 | Lundholm & O'Keefe (2001), *Contemporary Accounting Research* 18(2) | https://academicnewsletter.sufe.edu.cn/info/411848 |
| A22 | Fernández, "210 common mistakes to avoid when valuing a company", IESE Insight, 17 May 2017 | https://www.iese.edu/insight/articles/210-mistakes-valuing-company/ |
| A23 | Damodaran, terminal value notes and slides (stable growth: g = reinvestment rate x return on capital) | https://pages.stern.nyu.edu/~adamodar/pdfiles/country/TerminalValue.pdf |
| A24 | FTI Consulting, "Valuation implications of IFRS 16" | https://www.fticonsulting.com/uk/insights/articles/valuation-implications-ifrs-16 |
| A25 | Accountancy Age, "IFRS 16 (Leases) - the impact on business valuations" (28 Oct 2019) | https://accountancyage.com/2019/10/28/ifrs-16-leases-the-impact-on-business-valuations/ |
| A26 | NTNU master's thesis on the 2022 aquaculture resource-rent tax and Mowi/SalMar (event study) | https://ntnu.no/bridge/en/node/35891 |
| A27 | BI master's thesis (2018), underwriter analysts and Nordic IPOs | https://biopen.bi.no/bi-xmlui/handle/11250/2578735 |
| A28 | NHH master's thesis, "The Value of Equity Analysts: An Empirical Study of the Informativeness of Analyst Revisions" (OSEBX 2011-2021) | https://openaccess.nhh.no/nhh-xmlui/handle/11250/2982782 |
| A29 | CBS master's thesis on Danish target-price accuracy (2010-2020) | https://research.cbs.dk/en/studentProjects/the-recipe-for-precision-a-study-of-the-target-price-accuracy-of-/ |
| A30 | PwC / Forening for Finansfag Norge, "Risikopremien i det norske markedet 2025" (existence and scope only; PDF returned HTTP 403) | https://www.pwc.no/no/nyheter/risikopremien-i-det-norske-markedet-2025.pdf |

Case sources are listed with each case in section 2.

---

## 2. Oslo Børs case list

Rules applied: a case is listed only if a dated public source describes it. Broker names, ratings and targets appear only when the source states them. Tags: [read] = page opened; [snippet] = search-result snippet only. Quotes are paraphrased. "Failure mode" numbers refer to section 5.

### 2.1 Energy, offshore, seafood, industrials

**C1. Seadrill (SDRL) - the dividend that was not covered by cash flow, 2011-2016**
- Before:
  - 25 May 2011: 17 analysts covered the stock (8 buy, 8 hold, 1 sell); average target NOK 214 (range 165-245); consensus expected the dividend to keep rising (USD 2.97 per share for 2011, then about 3.04 and 3.16). Pareto had a hold, arguing the stock traded at a premium. Source: DN, https://www.dn.no/venter-utbyttevekst-i-seadrill/1-1-1657817 [read by helper]
  - 4 Sep 2012: TDN Finans consensus 6 buy / 10 hold / 1 sell, average target NOK 249 (range 210-296). Pareto target 290 and saw room to raise the dividend; Carnegie cut to hold (target 241); ABG hold (240). Stock near its record of NOK 244.20, yield 8.3%. Source: DN, https://www.dn.no/-vi-har-vart-bortskjemte-med-seadrill/1-1-1875606 [read by helper]
  - 27 Aug 2014: after weak guidance the share fell 5.8% to NOK 218.20; the article said the backlog supported dividends in 2015 (and via Seadrill Partners into 2016). Source: DN, https://www.dn.no/oslo-bors/sdrl/seadrill/derfor-faller-seadrill/1-1-5178675 [read by helper]
- What happened:
  - 26 Nov 2014: Seadrill suspended the dividend altogether, saying it would save about USD 2bn a year; it had 16 rigs under construction with USD 4.7bn of yard instalments still due. Investors had expected a cut of about one third. The share fell as much as 18% intraday and was down 12% at NOK 124.50 by mid-morning; Platou said the share would re-price to peer multiples and expected yield investors to sell; Bernstein called it a concrete sign that conditions were as bad as feared. Source: Reuters via gCaptain, https://gcaptain.com/seadrill-shares-tumble-dividend-cut [read]. The average analyst forecast for the 2015 dividend had been USD 2.46 per share: Maritime Executive/Reuters, https://maritime-executive.com/article/Seadrill-Axes-Dividend-as-Drilling-Market-Slumps-2014-11-26 [read by helper]
  - Late Dec 2014 / 21 Jan 2015: Goldman Sachs had cut to sell with target NOK 59 (share about 79), modelling a loan-covenant breach in 2016 at USD 70 oil and saying the market had not priced it. Source: DN, https://www.dn.no/borskommentar/sdrl/seadrill/seadrill-i-siget/1-1-5291462 [read by helper]
  - 21 Jan 2016: BofA Merrill Lynch cut from neutral to underperform and the target from NOK 70 to 15 (-79%); the share fell 29% that day. Source: DN, https://www.dn.no/borskommentar/marine-harvest/bred-oppgang-pa-borsen/1-1-5558873 [read by helper]
- Failure mode: dividend sustainability never tested against free cash flow after newbuild capex and debt service; peak-cycle day rates capitalised; leverage. Section 5: #27, #8, #9.

**C2. Salmon farmers (Mowi, SalMar, Lerøy, Grieg) - resource-rent tax, 28 Sep 2022**
- Before: on 4 Nov 2019 the majority of the government's aquaculture tax committee (Havbruksskatteutvalget) proposed a 40% resource-rent tax, so the risk was public almost three years before the proposal. Source: iLaks/DN, https://ilaks.no/dn-havbruksskatteutvalget-foreslar-en-40-prosents-sats-for-grunnrenteskatt-for-havbruk [read by helper]. No named broker targets from just before the proposal were found.
- What happened: on 28 Sep 2022 the government proposed an effective 40% rate. SalMar lost about 27% of its market value that day (Salmon Business, https://salmonbusiness.com/it-will-have-a-strong-negative-impact-on-the-entire-industry/ [read by helper]); about NOK 55.9bn of sector market value disappeared in one day (iLaks, 29 Sep 2022, https://ilaks.no/lempet-ut-lakseaksjer-like-for-skattenyhet/ [read by helper]). An NTNU event study estimates event-day falls of about 17% (Mowi) and 30% (SalMar) and value losses of about 18% and 42% from 31 Aug to 31 Dec 2022 (https://ntnu.no/bridge/en/node/35891 [snippet]). SalMar ended 2022 down nearly 38%, worst in the sector (iLaks, 28 Dec 2022, https://ilaks.no/det-har-vaert-et-begredelig-ar-for-lakseaksjene-med-ett-hederlig-unntak/ [read by helper]). On 2 Feb 2023 Kepler Cheuvreux noted consensus estimates assumed a 30-35% rate while share prices implied about 25% (iLaks, https://ilaks.no/?p=178769 [read by helper]); the rate finally adopted was 25% (iLaks, https://ilaks.no/lakseaksjene-til-vaers-etter-enighet-om-grunnrenteskatten/ [snippet]).
- Failure mode: a documented, dated regulatory proposal left out of valuations; tax modelled as the corporate rate only. Section 5: #16, #8.

**C3. Norwegian Air Shuttle (NAS) - growth funded by debt, 2015-2020**
- Before: 27 May 2015 Pareto reiterated buy and raised its target from NOK 400 to 450 with the share at about 302.90, arguing slower short-haul growth would lift margins and long-haul would drive growth in 2016-17 (DN, https://www.dn.no/norwegian/nas/ser-norwegian-50-prosent-opp/1-1-5385069 [read by helper]). Earlier, on 3 Mar 2015, HSBC had gone the other way, from overweight to underweight, target 330 to 200 (DN, https://www.dn.no/norwegian/nas/kutter-norwegian-kursmal-med-130-kroner/1-1-5322540 [read by helper]).
- What happened: 18 Feb 2019 a discounted rights issue of about NOK 3bn sent the share down as much as 15% (Bloomberg, https://www.bloomberg.com/news/articles/2019-02-18/norwegian-air-plunges-after-setting-price-of-rights-issue [snippet]). 14 Apr 2020 a plan to convert about NOK 44.5bn of debt to equity; the share fell 63% at the open and Bernstein cut its target to zero (The Local, https://www.thelocal.com/20200414/norwegian-shares-plummet-by-more-than-half-on-dilution-fears [read by helper]).
- Failure mode: growth and capex optimism (long-haul fleet) with leverage and lease obligations under-weighted; dilution risk. Section 5: #27, #23, #25, #1.

**C4. PGS - refinancing called off, June 2019**
- What happened: on 19 Jun 2019 PGS called off a USD 675m refinancing announced on 27 May; the share fell 24% at first and was down 17% later that morning; net interest-bearing debt was USD 1.3bn at end-Q1. Fearnley attributed the fall to fear of a dilutive equity issue and still thought PGS could refinance without a forced share sale if markets reopened. Source: Reuters via Marine Technology News, https://www.marinetechnologynews.com/news/calls-refinancing-shares-590533 [read by helper]
- Before: no pre-event broker target found.
- Failure mode: refinancing risk in a levered cyclical; bull view anchored on capital markets reopening. Section 5: #27.

**C5. REC Silicon - Moses Lake restart, 2022-2025**
- Before: 19 Sep 2024 the share closed up 29.7% on a silane deal, after a gain of about 60% the previous week (E24, https://e24.no/boers-og-finans/i/25PKAl/oslo-boers-aapner-opp [read by helper]). A Pareto buy with a target raised from NOK 30 to 33 is described only in a Finansavisen forum post (weak source, not used further).
- What happened:
  - 21 Oct 2024: first delivery delayed at customs; share -20.1%; Sparebank 1 Markets said USD 50-100m of new money was needed (E24, https://e24.no/boers-og-finans/i/pPro51/rec-silicon-stuper-20-prosent-etter-mer-moses-lake-troebbel [read by helper]).
  - 7 Nov 2024: Q3 pre-tax loss USD 52.6m; Moses Lake scaled back to about 15% utilisation; cash USD 23.6m; Sparebank 1 Markets expected to cut its 2025 EBITDA estimate by about half (E24, https://www.e24.no/boers-og-finans/i/PpOn95/analytiker-etter-rec-silicons-krisegrep-aksjen-boer-falle-kraftig [read]).
  - 17 Dec 2024 failed customer qualification; production of polysilicon at Moses Lake stopped (PV Tech, 2 Jan 2025, https://www.pv-tech.org/rec-silicon-abandons-us-polysilicon-production-at-moses-lake [read by helper]).
  - 2 Jan 2025: share fell about 50%; Sparebank 1 Markets kept sell and said roughly zero equity value was left, with about zero cash and over USD 400m of interest-bearing debt maturing heavily in 2025-26 (E24, https://e24.no/bors/nyheter/a/299298 [read]).
- Failure mode: ramp-up and qualification optimism; single-customer and controlling-shareholder risk; liquidity runway not modelled. Section 5: #3, #15, #27.

**C6. Nel - pipeline treated as revenue, 2024-2025**
- 1 Oct 2024: a framework deal of more than 1 GW with Hy Stor, signed in April and described by the CEO as a game-changer, fell through. It had never been booked as backlog. Pareto put its value at about NOK 2.5bn against consensus revenue of about NOK 5.4bn for 2025-26 combined; Nordea said consensus had given it at most a 50% probability. Source: E24, https://e24.no/boers-og-finans/i/wgK0R5/analytiker-etter-nels-tapte-storavtale-aksjen-kommer-til-aa-krakke [read by helper]
- 23 Feb 2025: Nordea expected revenue to collapse, citing massive overcapacity. Source: E24, https://e24.no/boers-og-finans/i/jQn27e/venter-kollaps-i-nels-inntekter-ser-skikkelig-daarlig-ut [read by helper]
- Failure mode: estimates anchored to management's pipeline and non-binding agreements instead of firm orders; no probability weighting. Section 5: #10, #15, #1.

**C7. Aker Horizons / Aker Carbon Capture - long-duration growth assets and rising rates, 2021-2025**
- 15 Nov 2023: Pareto warned of a possible write-down of about NOK 2bn on Mainstream Renewable Power because higher rates raise the cost of capital; its rating and target were put under review; the share was down nearly 90% over two years. Source: E24, https://e24.no/boers-og-finans/i/zEBJw4/ser-fare-for-aker-horizons-smell-paa-to-milliarder [read by helper]
- 9 May 2025: Aker's stake, worth about NOK 16.3bn at the 2021 listing, was worth about NOK 600m (about -96% since Jan 2021); Mainstream had been bought in 2021 at a EUR 900m valuation. Source: E24, https://e24.no/energi-og-klima/i/wgGJed/roekkes-nedtur-i-aker-horizons-fra-16-mrd-til-600-mill [read by helper]
- No pre-listing broker targets found.
- Failure mode: terminal-value-heavy valuations at low discount rates; no rate sensitivity. Section 5: #7, #21, #13.

**C8. Prosafe - leverage through a long downturn**
- 1 Sep 2021: Prosafe sought reconstruction with about USD 1.4bn of debt and about USD 1.1bn negative equity; about USD 1.1bn of debt to be converted, leaving existing shareholders with about 1%. Source: E24, https://e24.no/boers-og-finans/i/lV4ll3/boligriggselskapet-prosafe-soeker-rekonstruksjon-i-norge-aksjen-stiger-markant-paa-oslo-boers [read by helper]
- 26 Oct 2023: NOK 350m share issue at NOK 60 vs previous close of 91 after a weak Q3; share down about 27%. Source: E24, https://e24.no/boers-og-finans/i/veJ9Jl/prosafe-aksjen-raser-30-prosent-etter-pengeinnhenting-med-kraftig-rabatt [read by helper]
- No analyst view from before either event found.
- Failure mode: leverage and dilution in a cyclical. Section 5: #27, #25.

**C9. Norske Skog - bankruptcy, Dec 2017**
- 6 Jun 2017: the second-largest shareholder said the proposed rescue plan was worse than bankruptcy for shareholders (DN, https://www.dn.no/bors/rikard-storvestre/norske-skog/nobelsystem-scandinavia/-for-dem-som-har-vart-med-i-20-ar-er-dette-en-katastrofe/2-1-97658 [read by helper]).
- 19 Dec 2017: Norske Skog filed for bankruptcy after the largest secured creditor refused a voluntary recapitalisation; trading suspended (Kraftnytt, https://kraftnytt.no/2017/12/19/norske-skog-slar-seg-konkurs [read by helper]).
- No analyst angle found; listed as a structural-decline-plus-leverage example only.
- Failure mode: leverage in a structurally shrinking market (newsprint); creditors, not shareholders, control the outcome. Section 5: #27, #4.

### 2.2 Consumer, technology, biotech

**C10. XXL - a structural shift treated as weather and timing, 2018-2020**
- Before: after Q3 2018, consensus (SME Direkt) expected 2018 revenue of NOK 9.65bn and EBITDA of about NOK 748m.
- What happened: on 18 Dec 2018 XXL guided 2018 revenue to about NOK 9.4bn and EBITDA to NOK 530-560m; the CEO left after two months. On 19 Dec the share fell 37% at the open (about NOK 2bn of market value) and closed down 30.1% at NOK 23.5, nearly 80% below its October 2016 peak above NOK 110. Source: E24, https://e24.no/boers-og-finans/i/QlvBBW/xxl-aksjen-stuper-37-prosent-etter-negativt-resultatvarsel-og-sjefsavgang [read]. Short sellers had argued debt, high inventory, online competition and costly expansion (HedgeNordic, 20 Dec 2018, https://hedgenordic.com/2018/12/origo-and-bodenholms-xxl-shorts/ [read by helper]).
- Again on 2-3 Jan 2020: 2019 EBITDA guided to NOK 870-900m before inventory write-downs, Q4 sales -12%, and work under way to cut inventory and stay within loan terms (E24, https://e24.no/boers-og-finans/i/rAyyXl/resultatvarsel-fra-xxl-svak-julehandel-og-toeff-konkurranse [read by helper]); on 6 Jan 2020 Danske Bank kept sell and cut its target to NOK 10, expecting an inventory write-down of about NOK 450m (E24, https://e24.no/boers-og-finans/i/wPpjl5/nedgraderer-xxl-meglerhus-ser-22-5-prosent-nedside [read by helper]).
- Failure mode: margin erosion and inventory build (working capital) treated as temporary; the short sellers' balance-sheet case was the right one. Section 5: #4, #17, #12.

**C11. Kahoot - pandemic growth extrapolated, 2021-2023**
- Before: on 7 Jul 2021 Arctic Securities had buy with a NOK 140 target and expected a fall of about 10% on the day.
- What happened: the Q2 2021 update showed about 33,000 net organic paying-subscriber growth (173,000 gross, of which 140,000 from the Motimate acquisition) and operating cash flow USD 4.5m, 54% below Arctic's estimate. The share closed down 26.31% at NOK 43, its worst day ever, losing about NOK 7.25bn of market value. Source: E24, https://e24.no/boers-og-finans/i/O3ppEV/kahoot-faller-10-prosent-etter-handelsoppdatering [read]. On 14 Jul 2023 a consortium led by Goldman Sachs Asset Management's private-equity arm agreed to take Kahoot private at NOK 35 per share (TechCrunch, https://techcrunch.com/2023/07/14/kahoot-acquired [read by helper]).
- Failure mode: lockdown-era growth and acquired growth extrapolated as organic; cash conversion not checked. Section 5: #1, #13, #17.

**C12. Nordic Semiconductor - depth of the inventory correction, 2023-2024**
- Before: on 18 Sep 2023, after a Q3 guidance miss (share -15%), DNB Markets kept buy and called it a normal cyclical dip while noting customer inventories still about 30% above pre-pandemic levels; Arctic had hold and called the warning somewhat surprising (E24, https://e24.no/boers-og-finans/i/3E3Pmq/nod-stuper-etter-resultatvarsel-det-er-naa-man-skal-kjoepe [read by helper]).
- What happened: on 6 Feb 2024 Q4 revenue was USD 108m (vs 191m a year earlier), FY2023 USD 543m (vs 777m), Q1 2024 guided to USD 70-80m. Consensus 2024 revenue had been about USD 575m; SpareBank 1 Markets' seasonal model pointed to about USD 367m. Pareto called the results clearly disappointing and said inventory adjustments mattered more than it had expected. The share fell about 19% at the open. The company had already accepted at the start of 2023 that its USD 1bn revenue target was off the table. Source: E24, https://e24.no/boers-og-finans/i/69LyV0/analytiker-venter-aksjeras-i-nordic-semiconductor [read]
- Failure mode: consensus revenue anchored to the old trajectory and management's target; customer destocking (channel inventory) underestimated; cyclical peak capitalised. Section 5: #10, #8, #2.

**C13. Crayon - earnings in line, cash flow not, 8 Nov 2023**
- Consensus operational free cash flow for Q3 2023 was NOK -157m; the outcome was NOK -987m as net working capital rose by about NOK 1bn quarter on quarter. The share was down more than 15% intraday and closed down 7.86%. ABG Sundal Collier (via TDN Direkt) expected only minor changes to earnings consensus but a significant cut to free-cash-flow consensus. Source: E24, https://e24.no/boers-og-finans/i/eJnRaa/oljeprisfallet-frykter-ikke-lenger-store-konsekvenser-av-konflikten (live feed; Crayon item) [read]
- Failure mode: forecasts built on earnings with working capital as a plug; cash conversion not forecast. Section 5: #17.

**C14. Ultimovacs - one readout re-rates a single-asset pipeline, 7 Mar 2024**
- Before: company-sponsored research (Edison, 16 Feb 2024) gave a risk-adjusted NPV of about NOK 8.5bn (NOK 248 per share), with the INITIUM trial at a 25% probability of success worth about NOK 58.8 per share; all value rested on Phase II trials of one vaccine, UV1 (https://www.edisongroup.com/research/universal-approach-with-critical-readouts-in-march/33251/ [read by helper]).
- What happened: the UV1 study missed its primary endpoint (progression-free survival). DNB Markets expected a fall of about 80%; after the trading halt the share fell about 93%. DNB said confidence in the vaccine for other indications was also weakened and that the company would need to raise cash within the year. Source: E24, https://e24.no/boers-og-finans/i/JQV7oJ/analytiker-venter-aksjekollaps-i-ultimovacs [read]
- Failure mode: trials of the same asset treated as independent probabilities; financing risk after failure not modelled. Section 5: #15, #27.

**C15. Nordic Nanovector - Phase IIa data extrapolated, June 2022**
- Before: Carnegie had hold, target NOK 6.6.
- What happened: on 21-22 Jun 2022 the company said slow recruitment meant no topline data in H2 2022 and an expert panel found the Phase IIb efficacy data less promising than Phase IIa; the share fell about 56% to NOK 3.15 and Carnegie cut its target to NOK 3.7. Source: E24, https://e24.no/bors/nyheter/a/288507 [read by helper]
- Failure mode: binary clinical and recruitment risk under-weighted. Section 5: #15.

**C16. Atlantic Sapphire - scale-up and biology risk, 2020-2022**
- 8 Feb 2022: market value had fallen from about NOK 11.3bn in 2020 to about NOK 3.5bn (E24, https://e24.no/boers-og-finans/i/G3JP0x/tom-laksefabrikk-prises-til-3-3-milliarder [read by helper]).
- 23 May 2022: SpareBank 1 Markets cut its target from NOK 140 to 37 while keeping buy; the article calls the old forecast a significant miss (iLaks, https://ilaks.no/sparebank-1-markets-kaster-kortene-og-hovler-ned-kursmalet-i-atlantic-sapphire/ [read by helper]).
- 17 Oct 2022: higher mortality forced early harvest at low weights; the share fell more than 47% intraday and was down 83% year to date; Arctic still had buy (target NOK 35); Bloomberg showed 4 buy and 5 hold (E24, https://e24.no/boers-og-finans/i/rllzOa/analytiker-etter-atlantic-sapphire-ras-man-vet-ikke-om-de-kommer-til-aa-tjene-penger [read by helper]).
- Failure mode: capacity ramp-up and biology risk; buy ratings kept through repeated misses (slow to cut); funding needs not modelled. Section 5: #3, #12, #27.

**C17. Hexagon Purus - conditional nominations treated as backlog, 2022**
- 14 Feb 2022: a conditional letter of intent with Hino Motors worth about NOK 9bn sent the share up 34% (E24, https://e24.no/boers-og-finans/i/AL5w0j/milliardavtaler-for-hexagon-purus-peker-mot-et-ledende-produkt [read by helper]).
- 25 May 2022: the company lost a separate battery-pack supplier nomination worth about NOK 7bn through 2027; the share fell 17-20% (E24, https://e24.no/boers-og-finans/i/AL1ApE/hexagon-purus-mister-milliardavtale [read by helper]).
- Failure mode: non-binding awards valued as firm orders. Section 5: #10, #15.

**C18. Quantafuel - first-of-a-kind plant priced as proven (market miss; documented broker was bearish)**
- 30 Jun 2021: completion of the Skive plant slipped to mid-Q4; share about -9% after halving since January (E24, https://e24.no/boers-og-finans/i/pAJm8V/ny-forsinkelse-for-quantafuel-aksjen-faller-tungt [read by helper]).
- Feb 2022: a mechanical fault shut Skive; share about -24% to NOK 15.5, about 80% below the January 2021 peak of NOK 79; Nordea (already sell) cut its target to NOK 14 and lowered its success probabilities (E24, https://e24.no/boers-og-finans/i/34KB7q/quantafuel-aksjonaer-etter-kursras-sitter-stoedig-i-aksjen [read by helper]).
- Note: Quantafuel is also the company in which Arctic's head of research bought shares before initiation (section 3.2).
- Failure mode: technology and ramp-up risk not probability-weighted. Section 5: #15, #3.

**C19. Axactor - sponsored research and a mandate from the same broker, Nov 2020 - Jan 2021 (conflict case, not a forecast miss)**
- ABG Sundal Collier published issuer-paid research (17 Nov 2020) with a fair-value range of NOK 7.8-24.2 (DCF) and 6.4-31 (peers) against a share price of NOK 8.4; within a month ABG was among the arrangers of a NOK 532m share issue at NOK 8 and a NOK 2.1bn bond. Source: E24, https://e24.no/boers-og-finans/i/LnoEy9/meglerhus-solgte-positiv-analyse-fikk-storoppdrag-av-samme-selskap [read by helper]
- Failure mode: issuer-paid research and corporate-finance mandates at the same firm; very wide value range presented as support. Section 5: #29, #30.

**C20. Adevinta - take-private below the analyst's expectation (weak case)**
- 21 Nov 2023: Permira and Blackstone bid NOK 115 per share; Danske Bank called it cheap but fair, had expected NOK 120-125, and sketched a 2026 scenario near NOK 200; the independent board could not recommend the offer. Source: E24, https://e24.no/naeringsliv/i/nQob9m/analytiker-om-adevinta-budet-synes-det-er-billig [read by helper]
- No peak-era broker target was found, so no miss is claimed. Listed only as an example of the gap between DCF value and realisable value when a controlling holder sells.

**C21. Huddly - pandemic demand at IPO (weak case)**
- 20 Dec 2021: the share was down 57% since its February 2021 listing; 2021 revenue guidance cut from NOK 400-450m to 350-370m as video-conference demand faded. Source: E24, https://e24.no/boers-og-finans/i/V9ejMd/huddly-sjefen-rykker-ned-etter-kurskollaps [read by helper]
- No underwriter targets were found, so the underwriter-optimism angle is not documented.

### 2.3 Pattern across the cases

| Case | Dominant failure | Section 5 checks |
|---|---|---|
| C1 Seadrill | Dividend > FCF, leverage, peak day rates | 27, 8, 9 |
| C2 Salmon tax | Dated policy proposal not modelled | 16, 8 |
| C3 Norwegian | Growth and fleet capex funded by debt/leases | 27, 23, 25, 1 |
| C4 PGS | Refinancing risk | 27 |
| C5 REC Silicon | Ramp-up/qualification, liquidity | 3, 15, 27 |
| C6 Nel | Pipeline taken as revenue | 10, 15, 1 |
| C7 Aker Horizons | Duration and discount-rate risk | 7, 21, 13 |
| C8 Prosafe | Leverage, dilution | 27, 25 |
| C9 Norske Skog | Leverage in structural decline | 27, 4 |
| C10 XXL | Margin erosion, inventory | 4, 17, 12 |
| C11 Kahoot | Growth extrapolation, cash conversion | 1, 13, 17 |
| C12 Nordic Semi | Destocking, anchoring to target | 10, 8, 2 |
| C13 Crayon | Working capital | 17 |
| C14 Ultimovacs | Correlated binary risk | 15, 27 |
| C15 Nordic Nanovector | Binary/recruitment risk | 15 |
| C16 Atlantic Sapphire | Ramp-up, slow cuts, funding | 3, 12, 27 |
| C17 Hexagon Purus | Conditional awards as backlog | 10, 15 |
| C18 Quantafuel | Technology risk (market miss) | 15, 3 |
| C19 Axactor | Conflict of interest | 29, 30 |
| C20 Adevinta | Value vs realisable price (weak) | - |
| C21 Huddly | Pandemic demand at IPO (weak) | 1 |

The most frequent documented killer is leverage/funding (C1, C3, C4, C5, C8, C9, C14, C16), followed by growth extrapolated from a temporary state (C6, C10, C11, C12, C17, C21), binary events not weighted (C5, C14, C15, C17, C18) and working capital (C10, C11, C13). Pure valuation-arithmetic errors (WACC, IFRS 16, bridge) are rarely visible in press coverage because published notes are not public; the evidence for those comes from section 4.

---

## 3. Regulation: what binds an analyst in Norway, and what Finanstilsynet has found

### 3.1 The rule set

| Layer | What it says (paraphrased) | Source |
|---|---|---|
| **MAR (EU 596/2014) art. 20(1)** | Anyone who produces or disseminates investment recommendations must take reasonable care that the information is objectively presented and must disclose their interests or conflicts of interest concerning the instruments involved. | R16, R1 |
| **Norwegian implementation** | MAR took effect in Norwegian law on 1 March 2021 through verdipapirhandelloven § 3-1; the Commission regulations that supplement MAR (including 2016/958) are implemented through verdipapirforskriften § 3-1. Before that date the equivalent duty sat in the old verdipapirhandelloven § 3-10 and forskrift § 3-10 (this is the provision Finanstilsynet applied to a December 2018 report in the Arctic case, see 3.2). | R13, R2 |
| **Who is covered** | Anyone who recommends or suggests an investment strategy about an issuer or instrument, including statements about current or future value or price, when meant for distribution or the public. Analysts and firms whose main business is producing recommendations are covered even when the material is not meant for publication. Disclaimers do not take a post outside the rules; channel and payment do not matter; private individuals and social-media posts with a sizeable audience are covered. | R1, R9, R10, R11 |
| **Delegated Reg. 2016/958 art. 2-3** | Identify the producer (name, job title, legal person, supervisor). Separate facts from opinions; state if a source is of doubtful reliability; label all projections, forecasts and price targets as such and state the material assumptions behind them. | R14, R17 (VPFF reproduces art. 3) |
| **2016/958 art. 4 (professionals and experts)** | In addition: say if the recommendation was shown to the issuer and then amended; summarise the valuation basis/method and assumptions used to set a price target and any change to them; explain what "buy/hold/sell" means and over what horizon; give a risk warning **that includes a sensitivity analysis of the assumptions**; state planned update frequency; date and time all prices; flag and date any change versus a recommendation issued in the last 12 months; list all recommendations on the issuer in the last 12 months with date, author, price target, market price at the time, direction and validity period. | R14 |
| **2016/958 art. 5-6 (conflicts)** | Disclose: net long/short position above 0.5% of issued share capital; issuer holding above 5% of the firm; market maker/liquidity provider role; lead or co-lead manager of a public offer in the previous 12 months; agreements to supply investment services in the previous 12 months; agreements to produce the recommendation. Investment firms must also describe their information barriers, state whether staff pay is tied to transactions or trading fees, give price and date of shares staff acquired before an IPO, and publish quarterly the share of buy/hold/sell recommendations over 12 months and the share of each category for which the firm provided investment-banking-type services. | R15 |
| **Documentation duty** | Producers must be able to substantiate a recommendation (oral ones included) when Finanstilsynet asks. | R12 |
| **Sanctions** | Breaches can lead to an administrative fine (overtredelsesgebyr) under vphl. § 21-1(1); intentional or negligent breaches can be punished with fines or up to one year in prison under vphl. § 21-15(4) no. 1. Under MAR, Finanstilsynet publishes decisions on administrative sanctions for breaches after 1 March 2021. | R1, R8 |
| **Industry standard (binding on VPFF members): VPFF Standard 3** | First adopted 6 Sep 2005; latest revision 25 Nov 2025, in force 1 Feb 2026. Key points: research must reflect the analyst's own independent judgement; no promising a rating in advance and no changing ratings or estimates without a professional basis (2.1); analyst pay must not be tied directly to specific corporate-finance mandates (2.2); corporate finance and the issuer may not review a report containing a rating or target price before publication - at most a redacted version without target and rating for fact-checking, with written permission from compliance or head of research (2.3); issuer-paid research is marketing material and may carry no rating or target price, only a sufficiently wide valuation range with methodology described (2.4); analysts may not cover issuers they own shares in, and holdings must be sold before coverage starts (3.1); no personal trading while knowing the timing or content of unpublished research (3.3); content requirements mirror 2016/958 and add a link to the issuer's sustainability reporting (4.2); **quiet periods** (9.2): no research from seven days before a prospectus until 30 days after the end of the subscription period / first listing day on a regulated market; on a multilateral trading facility no target or rating until 14 days after first trading day; no research until two trading days after a private placement result is published. | R17 |

### 3.2 Documented Finanstilsynet cases involving research

**Arctic Securities AS - analysts' personal trading and a missing disclosure (letter dated 14 April 2021; R2, R3).** [read]
- Triggered by newspaper reports in October 2020. Finanstilsynet obtained trades and holdings for all analysts in the Norwegian business from August 2018 to October 2020 and compared them with published research.
- It singled out the head of research's trades in BW Offshore (autumn 2018), Quantafuel (August 2020), BW Energy and Aker BioMarine.
- BW Offshore: Finanstilsynet concluded the head of research was already working on a BWO report when he bought shares on 20 November 2018, so the firm should have waited four weeks before publishing (old vphl. § 8-3(2)). It also concluded that his holding should in any case have been disclosed in the report dated 2 December 2018, and that the omission breached the rules on investment recommendations (old vphl. § 3-10(1) with forskrift § 3-10). It called it aggravating that the person was the head of research.
- Quantafuel: the head of research had asked a junior analyst to prepare initiation of coverage in July 2020, attended an internal presentation of the company on 17 August 2020 (the day of his first purchase) and meetings with management around his last purchase on 26 August 2020. Finanstilsynet concluded he knew the likely timing and content of the unpublished research and should not have bought.
- Firm-level conclusions: no adequate procedures to stop analysts who know timing or content of research from trading before clients can act on it; conflicts not limited to a minimum; compliance's pre-clearance did not check the research calendar and did not assess conflicts itself; breach of good business conduct (vphl. § 10-9). The firm's argument that only one employee was involved was rejected: leaders' conduct shapes compliance culture. The page notes the firm took remedial steps; no fine is stated on the pages read.
- Relevance for the toolkit: conflicts are a documented, not hypothetical, failure mode on Oslo Børs, including at head-of-research level. See failure mode 29.

**Arctic Securities and Pareto Securities - Euronext Growth Advisor role (2022; R4, R5, R6).** [read R4; snippet R5, R6]
Thematic review published January 2022 covering Oslo Børs, eight securities firms and four audit firms. Findings summarised in the 2022 annual report: Oslo Børs needed better procedures for checking listing conditions and conflicts; firms acting as Euronext Growth Advisors had to improve conflict handling, revise broad disclaimers in information documents, document calls and electronic communications with issuers, and apply a stricter standard to employees' personal trading. Relevance: the 2020-21 Euronext Growth listing wave was handled by brokers who also wrote the research; post-listing coverage from the arranging bank is the classic underwriter-conflict setting (A7, A8, A9).

**Market-abuse surveillance thematic review (started 2022; R4).** [read] Covers firms' surveillance functions and compliance with MAR monitoring and reporting duties.

**Pareto Securities - placements and market soundings (2023; R7).** [snippet] Part of a thematic review; relevant to how research interacts with wall-crossing during placements (VPFF Standard 3 sections 11.4-11.5).

**Arctic Securities - Økokrim insider case (March 2026; R18, R19).** [snippet] Swedish outlets citing E24 reported that an Arctic Securities employee was remanded in custody for two weeks on suspicion of insider trading and corruption, suspected of passing inside information to a third party who traded on it; Økokrim said two people had been arrested. Arctic said it was not a party and was cooperating. This is an investigation, not a conviction; no verdict was found. It concerns inside information, not research quality, and is listed only because it shows the information-barrier risk in a Norwegian broker.

**Social media / finfluencers (2021, 2022, 2024; R9, R10, R11).** Finanstilsynet has repeatedly stated that MAR art. 20 applies to private individuals and social-media posts, and relayed ESMA's 2024 warning. No individual fine decision for an investment-recommendation breach was found (see section 6).

### 3.3 What this means for an automated tool

The rules translate directly into machine-checkable items for the deck builder: author and firm named; every price dated and timed; target-price method and assumptions summarised; a sensitivity analysis present; a 12-month recommendation history; rating definitions and horizon; conflicts block (holdings, mandates, market making, pay link); and, for issuer-paid work, no rating or target price. These are failure mode 30.

---

## 4. Academic evidence on analyst bias and valuation error

| # | Finding | Paper | Sample | Effect size (as stated in the source) | Grade |
|---|---|---|---|---|---|
| A1 | Target prices are too high and miss by a lot; little persistent skill | Bradshaw, Brown & Huang (2013) | US sell-side 12-month targets, 2000-2009 | Target-implied returns about 15pp above realised; mean absolute target-price error about 45%; 38% of targets met at the 12-month horizon, 64% met at some point during it; persistent differential ability statistically significant but economically weak | [abstract] |
| A2 | Average target sits far above the current price | Brav & Lehavy (2003) | US target prices 1997-1999 | One-year target on average 28% above the current price; the market still reacts to target revisions | [abstract] |
| A3 | Target-price revisions carry information, but accuracy is modest | Asquith, Mikhail & Au (2005) | Full-text reports by Institutional Investor All-American analysts | Targets achieved slightly over 50% of the time; target revisions move prices more than comparable EPS revisions | [abstract] |
| A4 | Errors are large, persistent and larger where predicted upside is larger | Bonini, Zanetti, Bianchini & Salvi (2010) | Italian target prices | Errors auto-correlated, non-mean-reverting, up to 36.6%; error increases with predicted price growth, firm size, and for loss-makers; research intensity and momentum reduce accuracy | [abstract] |
| A5 | Rigour of the valuation model matters | Gleason, Johnson & Li (2013) | 45,600 price targets (mean implied return 82% per the university release); portfolio test on 21,200 forecasts, 1997-2003 | Portfolios formed on targets from analysts using residual-income models gained about 15% in a year; PEG-based target portfolios lost more than 5% | [read release] |
| A6 | Recommendations follow PEG/long-term-growth heuristics, not cash-flow or RIM values; the LTG-driven ones predict returns worst | Bradshaw (2004) | US, 1994-1998 (per Barniv et al. 2009) | Little evidence that RIM values explain recommendations; LTG best explains them but has the weakest link to future excess returns | [abstract] |
| A7 | Underwriter analysts' IPO buys underperform | Michaely & Womack (1999) | 391 US IPOs, 1990-1991 | Over two years, stocks recommended by lead-underwriter analysts trailed those recommended by non-underwriter analysts by more than 50% (buy-and-hold, market-adjusted) | [read release] |
| A8 | Affiliated analysts are more favourable on growth and ratings | Lin & McNichols (1998) | US seasoned equity offerings | Lead/co-underwriter growth forecasts and recommendations significantly more favourable; EPS forecasts not generally higher; lead-underwriter "hold" gets a significantly more negative market reaction (read as a hidden "sell") | [abstract] |
| A9 | Long-term growth forecasts are inflated around equity offerings | Dechow, Hutton & Sloan (2000) | US equity offerings (1,179 offerings 1981-1990 per a secondary summary) | LTG forecasts too optimistic, most by lead-manager analysts; post-offering underperformance is largest where affiliated growth forecasts are highest and disappears once growth optimism is controlled for | [abstract] |
| A10 | Long-run growth barely persists; analysts' LTG is too optimistic | Chan, Karceski & Lakonishok (2003) | US stocks 1951-1997 | No persistence of long-term growth beyond chance; IBES LTG forecasts overly optimistic with little predictive power | [abstract] |
| A11 | Highest-LTG stocks subsequently underperform lowest-LTG stocks; analysts over-extrapolate good news | Bordalo, Gennaioli, La Porta & Shleifer (2019), building on La Porta (1996) | US | Direction stated; model of diagnostic expectations fits the pattern | [abstract] |
| A12 | Asymmetric reaction: too slow on bad news, too strong on good news | Easterwood & Nutt (1999) | US earnings forecasts | Direction stated; interpreted as systematic optimism | [abstract] |
| A13 | "Walk-down" to beatable numbers | Richardson, Teoh & Wysocki (2004) | US | Optimistic early-year forecasts revised down to beatable levels; strongest when the firm or insiders are net sellers after the announcement | [abstract] |
| A14 | Herding linked to career concerns | Hong, Kubik & Solomon | US analysts | Older analysts deviate more from consensus, forecast earlier, revise less; young analysts herd | [abstract] |
| A15 | Herding in recommendations | Jegadeesh & Kim (2010) | US recommendations | Market reacts more to revisions away from consensus; herding more likely at large brokers, low-dispersion stocks, infrequent revisers | [abstract] |
| A16 | Anchoring on the industry median EPS | Cen, Hilary & Wei (2013) | US, 1983-2005 | Optimistic forecasts when firm forward EPS is below the industry median, pessimistic when above | [abstract] |
| A17 | Rating distribution matters; buy-heavy brokers' buys are worth less | Barber, Lehavy, McNichols & Trueman (2006) | 438,000 recommendations, 463 brokers, Jan 1996-Jun 2003 | Share of buys fell from mid-2000 (linked to NASD Rule 2711 disclosure); upgrades to buy from brokers with the fewest buys significantly outperform those from brokers with the most | [abstract] |
| A18 | Regulation reduced optimism in ratings | Kadan, Madureira, Wang & Zach (2009); Madureira (2004 WP) | US, around the 2003 Global Settlement | Working-paper version: brokers moved to less optimistic ratings, most at the ten settling banks | [snippet] |
| A19 | Oil futures do not beat a no-change forecast | Alquist & Kilian (2010) | Monthly crude oil | Futures-based forecasts less accurate (MSPE) than the no-change forecast; later replication finds the ranking sample-dependent | [abstract] |
| A20 | Base rates: high growth is rare and forecasts are too narrow | Mauboussin, Callahan & Majd (2016) | Top 1,000 global companies by market cap, 1950-2015, inflation-adjusted, dead firms included | 3-year real sales CAGR: mean 8.1%, median 5.4%, standard deviation 18.7%; the standard deviation of IBES consensus 3-year growth estimates (Sep 2016) was only 8.3% ("forecasts are commonly too optimistic and too narrow"). Firms starting with sales below USD 325m: 18.1% achieved a 10-year real CAGR above 20%; firms with sales above USD 25bn: 0.2% did. | [read] |
| A21 | DCF and RIM disagree only because of inconsistent inputs | Lundholm & O'Keefe (2001) | Analytical | Inconsistent forecasts, wrong discount rate and missing cash flows (clean-surplus violations) create large value differences | [abstract] |
| A22 | Catalogue of practitioner errors | Fernández (IESE, 2017; earlier "110" and "119 common errors") | Valuations seen as consultant | Seven groups: discount rate and risk, cash flows, terminal value (e.g. inconsistent perpetuity cash flows; arithmetic instead of geometric growth averages), conceptual inconsistencies, interpreting valuation (value vs price), interpreting accounting (profit vs cash), organisational errors | [read] |
| A23 | Stable growth must be paid for | Damodaran (notes) | Analytical | In stable growth g = reinvestment rate x return on capital; worked examples set stable ROC near the cost of capital; g should not exceed nominal economic growth | [snippet of slides] |
| A24 | IFRS 16 makes DCFs easier to get wrong | FTI Consulting; Accountancy Age (2019) | Practitioner | Cash flows and discount rate must be on the same pre- or post-IFRS 16 basis; lease liabilities in net debt only if lease payments are excluded from FCF; terminal value must include continuing lease/renewal outflows; multiples must be lease-consistent across peers | [snippet] |
| N1 | Nordic: underwriter bias not found in a small Nordic IPO sample | BI master's thesis (2018) | 100 Nordic IPOs, 274 buy recommendations | No evidence of biased underwriter recommendations (author notes conflict with Michaely & Womack and suggests post-reform rules as a reason) | [snippet] |
| N2 | Oslo: recommendation revisions move prices | NHH master's thesis | 69 OSEBX firms, 2011-2021 | Recommendation revisions carry large abnormal returns (magnitude not captured) | [snippet] |
| N3 | Denmark: targets inaccurate | CBS master's thesis | 17,667 targets, 709 analysts, Danish stocks 2010-2020 | Mean absolute error 27.8%; 51.9% of targets achieved within 12 months; negative bias in that sample | [snippet] |
| N4 | Aquaculture tax shock priced in two steps | NTNU master's thesis | Mowi, SalMar, 31 Aug-31 Dec 2022 | Proposal lowered value about 18% (Mowi) and 42% (SalMar) over the period; event-day falls about 17% and 30% | [snippet] |

Reading across the table: targets are on average 15-28% too high (A1, A2), are hit roughly half the time (A1, A3, N3), errors grow with the size of the predicted upside (A4), and optimism concentrates where the broker has a deal (A7-A9) or where long-term growth is extrapolated (A6, A10, A11, A20). Analysts move slowly on bad news (A12), herd (A14, A15) and anchor (A16). The better-performing targets come from explicit cash-flow/RIM models rather than PEG heuristics (A5, A6) - which is the toolkit's approach, provided its inputs are internally consistent (A21-A24).

---

## 5. The 30 most common failure modes and the check a DCF tool can run

Legend. **Auto** = fully automatable from the workbook. **Auto + J** = the tool can flag it, but a human must decide whether the flag is justified (the check should require a written reason in the model to clear it). **J** = needs human judgement; the tool can only force the question. "Existing" refers to the current `Checks` sheet numbering (SATS example, 30 checks); "new" means not covered today. Thresholds are proposals for DECISIONS.md, not findings from the sources.

### A. Forecast optimism and behavioural bias

**1. Growth above base rates** - Auto
- What: revenue CAGR in the explicit period far above what companies of that size have historically achieved.
- Evidence: A20 (3-year real CAGR median 5.4%, SD 18.7%; 10-year >20% CAGR achieved by 18.1% of small and 0.2% of very large firms), A10, A11; cases C6, C11, C21.
- Check: convert forecast revenue CAGR to real terms (subtract inflation assumption) and place it in the Base Rate Book distribution for the company's size bucket. WARNING if above the 80th percentile, ERROR-level warning if above the 95th, unless a "growth justification" text cell is filled. New.

**2. Forecast range too narrow (overconfidence)** - Auto
- What: bull and bear cases sit close to base; the dispersion of outcomes is understated.
- Evidence: A20 (consensus SD 8.3% vs realised 18.7%).
- Check: spread between bull and bear 3-year revenue CAGR must be at least 1 standard deviation of the base-rate bucket (or at least 10pp for a small-cap); bear-case value per share must be at least 25% below base. New (extends existing check 16 on scenario probabilities).

**3. Hockey-stick margins** - Auto + J
- What: terminal/last-year EBIT margin above anything the company has delivered.
- Evidence: A4 (error grows with predicted upside), A20 (margins regress toward the mean); ramp-up cases C5, C16, C18.
- Check: last forecast EBIT margin > historical maximum + 2pp, or > 75th percentile of peer margins, without a stated driver -> WARNING. New (existing check 26 covers utilisation only).

**4. No mean reversion in margins or returns** - Auto
- What: above-average margin/ROIC held flat to the terminal year.
- Evidence: A20 (regression toward the mean is documented for margins and CFROI), A23.
- Check: if current EBIT margin or ROIC is above the sector median, the forecast must move at least part of the gap toward the median by the terminal year (e.g. at least 25% of the gap closed), or the "moat" reason cell is filled. New.

**5. Terminal returns not faded (RONIC far above WACC forever)** - Auto
- What: value assumes excess returns on new investment in perpetuity.
- Evidence: A23 (stable ROC near cost of capital in worked examples), Fernández terminal-value errors (A22).
- Check: terminal RONIC / WACC > 1.5 -> WARNING; > 2.0 -> ERROR unless justified. Existing check 11 tests only RONIC >= WACC (a floor), not a ceiling; add the ceiling. Partly existing.

**6. Terminal growth not paid for** - Auto
- What: perpetuity growth with too little reinvestment, or g above long-run nominal growth.
- Evidence: A23 (g = reinvestment rate x RONIC), A22.
- Check: recompute implied reinvestment = g / RONIC and compare with terminal FCF (`DCF|tv_reinv`); abs difference > 1pp of NOPAT -> ERROR. g > risk-free rate of the cash-flow currency -> WARNING. Existing checks 8-9 (WACC > g; g <= 3%) cover part; the reinvestment identity is new.

**7. Terminal value dominance** - Auto
- What: almost all value sits in the terminal year, so the explicit forecast is decoration.
- Evidence: A22 (terminal-value group of errors); case C7.
- Check: TV share of EV > 80% WARNING (existing check 10). Add: if TV share > 90% or explicit-period FCF sum is negative, require a reverse-DCF statement of what must be true in the terminal year. Partly existing.

**8. Peak-cycle earnings capitalised** - Auto + J
- What: a cyclical (drilling, shipping, seismic, salmon, polysilicon, metals) valued on top-of-cycle margins or day rates carried into the terminal value.
- Evidence: cases C1, C2, C12; A20 (mean reversion); A11 (extrapolation of good states).
- Check: for sectors tagged cyclical, terminal EBIT margin must be <= through-cycle average (at least 10 years of history or peer history) + 1 SD; flag if the base year is in the top quartile of the company's own history and the forecast does not decline. New.

**9. Commodity / price deck out of line with the market** - Auto + J
- What: forecast product price (oil, gas, salmon, polysilicon, freight, power) set above the forward curve or above recent realised prices without a stated reason.
- Evidence: A19 (futures do not beat no-change; deck choices are a judgement, so they must be disclosed and stressed); case C1 (day rates vs oil price).
- Check: price deck input vs forward curve / 3-year average realised price; deviation > 10% -> WARNING; stress test must show value at forward-curve prices. New (stress_test.py extension).

**10. Anchoring to management guidance** - Auto + J
- What: forecasts copy company targets (capacity, margin, revenue ambitions) rather than modelling them.
- Evidence: A13 (forecasts managed toward beatable numbers), A16 (anchoring); cases C6, C12, C17.
- Check: store company guidance/targets as an input row; WARNING if forecast equals guidance within 1% in every year (no independent view) or exceeds the top of guidance. Track record: if the company missed its own guidance in 2 of the last 3 years, haircut must be stated. New.

**11. Herding on consensus (no variant view)** - Auto
- What: the model mirrors consensus but carries a strong rating.
- Evidence: A14, A15; toolkit already has `case_gate.py`.
- Check: if revenue, EBIT and EPS are within +-2% of consensus for all three years and the rating is BUY/SELL, ERROR "rating not supported by a variant view" (Consensus sheet `diff_*`). Existing `case_gate.py` tests gap vs market-implied drivers; add the consensus test. Partly existing.

**12. Slow to cut on bad news (stale target)** - Auto
- What: the target is left in place after a profit warning, guidance cut or large price fall.
- Evidence: A12 (underreaction to bad news); cases C10, C16 (buy kept through repeated misses), C1 (79% target cut only in 2016).
- Check: if the price has fallen > 25% since the model date, or a profit warning/quarter has been reported after `Inputs|model_date`, block the deck build until the model date is updated. New.

**13. Target price optimism (upside out of line with history)** - Auto
- What: implied upside so large that, statistically, it is usually wrong.
- Evidence: A1 (15pp excess), A2 (28% average upside), A4 (error grows with predicted upside).
- Check: if TP total return > Ke + 15pp, require bear case and reverse DCF on the front page and an explicit "why the market is wrong" line (Consensus `vp*` cells); if > Ke + 40pp, WARNING. Partly existing via `DCF|tp_excess`; threshold test is new.

**14. Rating scale skewed to BUY** - Auto
- What: buy threshold set so low that most stocks qualify.
- Evidence: A17 (buy-heavy brokers' buys underperform; ratings distribution must be disclosed under 2016/958 art. 6(3), R15).
- Check: BUY threshold (`Inputs|buy_th`) must be at least Ke-consistent (e.g. expected total return > Ke + 5pp) and symmetric with SELL; log every published rating so the deck can show the 12-month rating distribution. New.

**15. Binary event not probability-weighted** - J (Auto for the structure)
- What: a trial readout, licence, contract award, tender or court case is either ignored or assumed to succeed.
- Evidence: cases C5, C14 (trials of one asset are correlated, not independent), C15, C17, C18.
- Check: if a "binary event" flag is set, the TP must be a probability-weighted value with at least two scenarios whose probabilities sum to 100% (existing check 16), and the failure scenario value must be shown on the front page. New for the flag; structure existing.

**16. Policy, tax and regulatory regime risk not modelled** - Auto + J
- What: sector-specific taxes or regulation (resource-rent tax on aquaculture, hydropower and petroleum; licence regimes; subsidy schemes for renewables/hydrogen) held constant.
- Evidence: case C2 (40% proposal public since Nov 2019; NTNU event study N4).
- Check: for sectors tagged as resource-rent or licence-dependent, effective tax must be a separate input from the 22% corporate rate, and stress_test.py must run a "+15pp effective tax" case; WARNING if value falls > 20% and the risk is not in the deck's risk slide. New.

### B. Technical valuation errors

**17. Working capital ignored or released to fund value** - Auto
- What: NWC/sales drops in the forecast, releasing cash, or NWC is held flat while revenue grows.
- Evidence: A22 (cash-flow errors); Lundholm & O'Keefe "missing cash flow" errors (A21); cases C13 (NWC up about NOK 1bn in one quarter), C10, C11.
- Check: forecast NWC/sales vs 3-year historical average; fall > 5pp without stated driver -> WARNING; NWC investment < 0 in any year with revenue growth -> WARNING. Partly existing (check 22 tests net reinvestment as a whole); the NWC-specific test is new.

**18. Capex below depreciation while growing** - Auto
- What: growth without investment; terminal capex below D&A.
- Evidence: A23, A25 (after IFRS 16 "capex = depreciation" no longer holds once right-of-use depreciation is included).
- Check: in growth years capex / (D&A excluding right-of-use depreciation) < 1 -> WARNING; terminal net investment must match check 6. Partly existing (check 22).

**19. Growth not paid for (sales-to-capital too high)** - Auto
- What: incremental revenue per unit of invested capital far above history.
- Evidence: A23; existing check 21 flagged this in the SATS example.
- Check: forecast return on new capital / today's ROIC (existing check 21) and incremental sales-to-capital > 1.5x the historical maximum -> WARNING. Existing (keep).

**20. WACC built from inconsistent leverage** - Auto
- What: beta relevered at one D/V, weights at another, forecast balance sheet at a third.
- Evidence: A21 (wrong discount rate errors), A22 (discount-rate group).
- Check: target D/V in beta relevering = D/V in WACC weights; forecast average net debt/EV within 5pp of target. Existing check 23 covers the forecast balance sheet; add the relevering-vs-weights identity. Partly existing.

**21. Risk-free rate, ERP or currency mismatch** - Auto
- What: NOK cash flows discounted with a USD risk-free rate (or vice versa); ERP outside the range Norwegian practitioners use; country risk double counted.
- Evidence: A22; A30 (annual PwC/FFN survey of the Norwegian market risk premium exists as the local reference; its 2025 value could not be read); case C7 (value broke when rates rose).
- Check: currency of rf must equal currency of the cash flows (`Inputs|currency`); ERP outside a configurable band (set from the latest PwC/FFN survey) -> WARNING; size/specific premia > 3pp combined -> WARNING with reason. New.

**22. Reporting currency vs listing currency** - Auto
- What: USD- or EUR-reporting companies listed in NOK (shipping, offshore, seafood, Adevinta-type cases) - FX applied twice, not at all, or at a stale rate; net debt in a different currency from EV.
- Evidence: A22 (consistency errors); common on Oslo Børs where many issuers report in USD/EUR.
- Check: if reporting currency != quote currency, the model must hold an explicit FX rate with date; value per share computed in reporting currency then converted once; net debt in the same currency as EV. New.

**23. IFRS 16 leases double counted or omitted** - Auto
- What: lease liabilities deducted from EV while lease payments are also deducted from FCF (double count), or EBITDA post-IFRS 16 used with no lease deduction at all (omission); peers' multiples mixed pre/post IFRS 16.
- Evidence: A24, A25; toolkit DECISIONS (lease-adjusted DCF).
- Check: one switch: if FCFF is post-IFRS 16 (lease payments excluded), then lease liabilities must be in the bridge and WACC weights; if pre-IFRS 16 (EBITDAaL), lease liabilities must be zero in the bridge. Terminal FCF must include continuing lease cost. Peer multiples must carry the same lease basis (`Inputs|peer_lease`). Partly existing (`DCF|memo_lease`, peer_lease input); the either/or ERROR is new.

**24. Incomplete EV-to-equity bridge** - Auto
- What: minorities, pensions, associates, preferred/hybrid capital, earn-outs, dividends declared, trapped cash or non-operating assets left out.
- Evidence: A22 (cash-flow and accounting interpretation errors).
- Check: every bridge item (`DCF|b_nibd`, `b_min`, `b_pens`, `b_assoc`, `b_other`) must be filled or explicitly zero with a source; if the income statement shows minority interest but `b_min` = 0 -> ERROR; if associates income > 0 but `b_assoc` = 0 -> ERROR. New.

**25. Share count and dilution** - Auto
- What: basic instead of diluted shares; treasury shares not removed; private placements, repair issues or warrant exercises after the balance-sheet date not included - frequent on Oslo Børs.
- Evidence: A22; cases C3, C8 (dilutive conversions/issues); VPFF quiet-period rules show how often placements happen around coverage (R17).
- Check: diluted share count date must be after the latest share issue announced; `Inputs|shares_dil` >= `Inputs|shares`; if a placement is announced after `Inputs|bs_date`, net debt must include the proceeds and shares the new count. New.

**26. Stale balance sheet / date mismatch** - Auto
- What: price from today, net debt from a balance sheet two quarters old, dividends or deals in between ignored.
- Evidence: A22; 2016/958 requires dates and times on all prices (R14).
- Check: `Inputs|val_date` - `Inputs|bs_date` > 120 days -> WARNING; price date older than 5 trading days at deck build -> ERROR. Partly existing (stub check 12).

**27. Leverage, refinancing and dividend sustainability** - Auto + J
- What: equity valued as EV minus debt with no distress or dilution scenario, although maturities exceed liquidity; dividends funded by debt.
- Evidence: cases C1, C3, C4, C5, C8, C9, C14, C16 - the most frequent killer in section 2.
- Check: net debt/EBITDA > 4x or interest cover < 2x, or debt maturities in the next 24 months > cash + undrawn facilities + forecast FCF -> require a refinancing/distress scenario in the scenario set; dividends > FCFE for two consecutive forecast years -> WARNING. New.

**28. Multiples and exit value inconsistent with the DCF** - Auto
- What: exit multiple implies a growth or return different from the Gordon terminal value; peers from a different year or accounting basis.
- Evidence: A22, A24; existing checks 19-20.
- Check: implied perpetual growth from the exit multiple vs `Drivers|tg` differ by > 1pp -> WARNING; peer year (`Inputs|peer_year`) must equal the multiple year used. Existing checks 19-20 cover range tests; the implied-growth identity is new.

**29. Heuristic target instead of a model / conflicts not disclosed** - Auto
- What: target set by P/E x EPS or PEG while the DCF is ignored; or the deck omits conflicts and affiliations.
- Evidence: A5, A6 (PEG-based targets perform worst); A7-A9 (affiliation bias); R2 (Arctic: holding not disclosed); case C19 (issuer-paid research, then a mandate).
- Check: DCF weight in the target (`Inputs|w_dcf`) must be >= 50% or a reason is given; a conflicts block (own holdings, firm mandates in last 12 months, market making, issuer-paid yes/no) must be filled before the deck builds; if issuer-paid = yes, rating and target must be blank (VPFF 2.4). New.

**30. Missing MAR / 2016/958 disclosures in the published output** - Auto
- What: the deck lacks items the law requires: author, firm, supervisor, price dates and times, valuation-method summary, sensitivity analysis of assumptions, rating definitions and horizon, update frequency, 12-month recommendation history, change vs prior recommendation.
- Evidence: R14, R15, R17; R2 shows Finanstilsynet enforces disclosure.
- Check: deck builder asserts each element is present (slide/field exists and non-empty) and that the sensitivity table is generated from the model, not typed. New.

### Summary table

| # | Failure mode | Type | Status in toolkit |
|---|---|---|---|
| 1 | Growth above base rates | Auto | New |
| 2 | Forecast range too narrow | Auto | New |
| 3 | Hockey-stick margins | Auto + J | New |
| 4 | No mean reversion | Auto | New |
| 5 | RONIC not faded (ceiling) | Auto | Partly (check 11 floor) |
| 6 | Terminal growth not paid for | Auto | Partly (checks 8-9) |
| 7 | Terminal value dominance | Auto | Partly (check 10) |
| 8 | Peak-cycle earnings capitalised | Auto + J | New |
| 9 | Commodity deck vs forward curve | Auto + J | New |
| 10 | Anchoring to guidance | Auto + J | New |
| 11 | Herding on consensus | Auto | Partly (case_gate.py) |
| 12 | Stale target after bad news | Auto | New |
| 13 | Target-price optimism | Auto | Partly (tp_excess) |
| 14 | Skewed rating scale | Auto | New |
| 15 | Binary event not weighted | J | Partly (check 16) |
| 16 | Tax/regulatory regime risk | Auto + J | New |
| 17 | Working capital | Auto | Partly (check 22) |
| 18 | Capex below depreciation | Auto | Partly (check 22) |
| 19 | Growth not paid for | Auto | Existing (check 21) |
| 20 | Inconsistent leverage in WACC | Auto | Partly (check 23) |
| 21 | rf/ERP/currency mismatch | Auto | New |
| 22 | Reporting vs listing currency | Auto | New |
| 23 | IFRS 16 double count/omission | Auto | Partly (memo_lease) |
| 24 | Incomplete EV-to-equity bridge | Auto | New |
| 25 | Share count and dilution | Auto | New |
| 26 | Stale balance sheet/dates | Auto | Partly (check 12) |
| 27 | Leverage, refinancing, dividends | Auto + J | New |
| 28 | Exit multiple vs Gordon | Auto | Partly (checks 19-20) |
| 29 | Heuristic target / conflicts | Auto | New |
| 30 | MAR/2016/958 disclosures | Auto | New |

Count: 23 fully automatable (Auto), 6 flag-plus-judgement (Auto + J), 1 judgement with an automatable structure (J). Seventeen are new, twelve are partly covered today, one (#19) is fully covered.

---

## Det som ikke lot seg finne offentlig

Things searched for that could not be documented from public sources on 22 Oct 2026 (so they are not used above):

**Cases and analyst calls**
- Seadrill's Chapter 11 filing (2017) and the analyst stance just before it - not sourced in this run.
- Named broker targets on Mowi, SalMar, Lerøy and Grieg in the weeks before 28 Sep 2022. A snippet mentioned target cuts by several brokers afterwards, without figures.
- Norwegian Air Shuttle broker targets in 2018 (IAG interest) and 2019.
- Nel consensus and targets at the 2021 peak.
- Scatec 2021-2023 (E24 topic page returned 404 and the search budget was spent). E24's live feed on 22 Oct 2026 showed Scatec down more than 18% after cutting its 2026 earnings estimate for power production, and Komplett down about 15.5%, but with no broker views; not used.
- Elkem, Songa, Archer, Kid, Europris, Navamedic, Vow, Zaptec, Kitron and Norwegian banks: no documented analyst miss found (some headlines only).
- Hurtigruten: not researched beyond the brief (no longer listed).
- Kahoot's peak-era targets (2021 high around NOK 109): only undated E24 live-feed snippets.
- A Pareto note on REC Silicon (buy, target NOK 33) is known only from a Finansavisen forum post; not used.
- Underwriter targets for the 2020-21 Euronext Growth (Merkur) IPO wave compared with outcomes: no public compilation found; DN and Finansavisen coverage is paywalled.
- Adevinta's February 2023 write-down: the helper read the E24 article but did not return a complete URL, so the figures are left out.
- IntraFish (login), Bloomberg (403) and most DN/Finansavisen articles could not be opened directly; DN pages were read by the helper only via the login redirect.

**Regulation and supervision**
- No published Finanstilsynet fine (overtredelsesgebyr) for breach of MAR art. 20 / 2016/958 by an analyst or broker was found. The Arctic case (2021) concluded on breaches but no fine is stated on the pages read.
- No Finanstilsynet thematic review dedicated to the quality or objectivity of investment research (as opposed to conflicts, personal trading, Euronext Growth advisors and market-abuse surveillance) was found.
- The outcome of the March 2026 Økokrim investigation involving an Arctic Securities employee (charges, verdict) was not found.
- No ESMA supervisory briefing with findings specific to MAR art. 20 was found.

**Academic and reference data**
- No NHH or BI master's thesis measuring target-price accuracy on Oslo Børs specifically was found (the closest are an NHH study of revision informativeness on OSEBX and a BI study of Nordic IPO underwriter bias, both seen only as abstracts/snippets; the NHH and BI repositories did not resolve from this machine).
- The 2025 (and 2024) PwC/FFN market-risk-premium survey values: the PDFs returned HTTP 403, so no number is given; check 21's ERP band must be set by hand from the survey.
- Full texts behind paywalls (Bradshaw-Brown-Huang, Bonini et al., Kadan et al.) were not read; figures come from abstracts or university releases. The Gleason-Johnson-Li "82% mean implied return" figure comes from the University of Iowa release, not the paper.
- Published version details of Hong, Kubik and Solomon were not verified (SSRN working paper used).

