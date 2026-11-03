"""SATS ASA – narrative text for the pitch deck. Numbers on the slides come from the Excel model; the facts below are
from SATS ASA's interim reports and presentations (Q4 2019-Q2 2026), the 2025 Capital Markets Day, satsgroup.com
(management) and, for the size of the Nordic fitness market, EuropeActive/Deloitte as quoted in the 2026 Pareto case
workbook. Macro figures: Norges Bank, the Riksbank and Konjunkturinstitutet (September 2026). Keys are read with
deck_case.ct(key, default)."""

YF = "Yahoo Finance consensus (Oct 2026)"

CT = dict(
    # ---- cover
    cover_title="SATS – Healthy body, healthy margins",
    cover_dates="Share price of 30.10.26 (close); estimates after the Q3 2026 report (02.11.26)",
    # ---- company overview
    ov_chapter="#1 The equity story of the Nordic fitness market leader",
    ov_subtitle="SATS ASA – the leading fitness club operator in the Nordics, with pricing power and operating leverage",
    ov_key="{comp} is the **#1 fitness operator in the Nordics** with **{vol}k members** in {locs} clubs across Norway, Sweden, "
           "Finland and Denmark. **Membership subscriptions (83% of revenue)**, proven **pricing power** and a largely fixed "
           "club cost base lift the **EBIT adj. margin to ~{m:.0f}% by 2030E** – with **ROIC well above WACC**.",
    ov_sources="Sources: SATS ASA interim reports (Q4 2019–Q2 2026), satsgroup.com, case team estimates.  "
               "(1) EBIT adjusted: pre-IFRS 16 (after lease payments) and excl. special items.",
    vol_label="Members", vol_word="member",
    employees_row=("Employees", "~10,000"),
    ov_recurring="**Recurring revenue:** 83% of sales are monthly memberships; personal training and retail the rest",
    ov_pricing="**Pricing power:** revenue per member up ~6% a year in 2024-25 and +6% currency adjusted in Q2 2026",
    ov_leverage="**Operating leverage:** EBITDA before IFRS 16 up from NOK 0.61bn (2023) to NOK 0.87bn (2025) and NOK 0.99bn LTM Q3 2026",
    mgmt=[("SG", "CEO – Sondre Gravir", "Joined SATS in 2018"),
          ("CE", "CFO – Cecilie Elde", "Joined SATS in 2016"),
          ("GS", "CDO – Gaute Sandal", "Chief Digital Officer, joined SATS in 2017")],
    ov_hist_from=4,                      # charts from 2023A (2020-22 distorted by the pandemic)
    # ---- market overview (deck_slides5.market_overview_kpi)
    market=dict(
        chapter="#2 Leading positions in every Nordic market",
        subtitle="SATS is #1 in Norway, Sweden and Finland and #2 in Denmark – price, utilisation and new clubs drive growth",
        sources="Sources: SATS ASA interim reports and the Q2 2026 presentation (clubs, members, revenue per member, market positions, "
                "committed pipeline); Nordic fitness members (5.2m, 2025): EuropeActive/Deloitte European Health & Fitness Market Report "
                "2025, as quoted in the 2026 Pareto case workbook.",
        p1_title="More members per club",
        p2_title="Revenue per member (NOK/month)",
        arpm_years=["2023", "2024", "2025"],
        arpm=[("Norway", [551, 573, 608]), ("Sweden", [540, 573, 627]), ("Finland", [550, 588, 608]), ("Denmark", [517, 590, 628])],
        p3_title="~15% of all Nordic fitness members",
        share=[("SATS", 0.146), ("Other operators", 0.854)],
        share_centre=["2025", "Nordics"],
        positions=["**#1 in Norway:** 120 clubs (78 SATS, 42 Fresh Fitness)",
                   "**#1 in Sweden** by revenue: 93 clubs",
                   "**#1 in Finland** (ELIXIA): 32 clubs",
                   "**#2 in Denmark:** 28 clubs in Greater Copenhagen"],
        p4_title="Demand absorbs price increases",
        tailwinds=[("+3%", "member growth in 2025 on a flat club base – 755,000 members at year end"),
                   ("+7%", "currency-adjusted revenue growth in Q2 2026 with three fewer clubs than a year earlier"),
                   ("13", "club openings committed through 2028; a run-rate of 8-12 a year is targeted from 2027")],
        boxes=[("Opportunities", ["**Price increases above cost inflation** backed by product tiers and upgrades",
                                  "**Higher utilisation:** more members per club at near-zero marginal cost",
                                  "**Roll-out:** 8-12 new clubs a year at NOK 7-8m each with a ~3-year payback"]),
               ("Disruption", ["**Boutique studios and digital training** – met with premium concepts inside the clubs and the SATS app",
                               "**Low-cost segment** – addressed with Fresh Fitness (42 clubs in Norway)",
                               "**GLP-1 weight-loss drugs** – so far neutral to positive: users join to keep muscle mass"]),
               ("Threats", ["**Low-cost expansion** in the big cities could cap pricing power – Sweden is the contested market",
                            "**Regulation:** Denmark's VAT on group training and PT (2026) cut the Danish member base by 4%"])],
    ),
    # ---- valuation slide
    thesis_quality="**Little operating leverage priced in:** the share price implies a {m_imp:.1f}% EBIT margin in {yl} (11.7% today) – we model {m_our:.1f}%",
    thesis_growth="**Growth engine intact:** revenue per member, members per club and 7-8 net openings a year (13 committed through 2028, target 8-12)",
    thesis_catalysts="**Catalysts:** Q4 report 9 Feb 2027 (2026 EBITDA before IFRS 16 above NOK 1.0bn), the next buyback programme, the 2027 openings",
    # ---- risks: title, description, probability (1-3), impact (1-3)
    risks=[
        ("Low-cost competition", "Low-cost chains add capacity in the big cities and cap price increases; SATS answers with Fresh Fitness and product tiers.", 3, 3),
        ("Cost inflation", "Personnel and rent are ~70% of costs – Norwegian wage growth of ~4% above the growth in revenue per member reverses the operating leverage.", 2, 3),
        ("Denmark and Finland", "Denmark lost 4% of its members after VAT on group training and PT (2026); both countries earn thin margins.", 3, 1),
        ("Roll-out execution", "8-12 openings a year after years of a flat club count; only 13 clubs are committed through 2028.", 2, 2),
        ("Consumer slowdown", "Memberships are discretionary: the member base fell 9% in 2020 and took two years to recover.", 1, 3),
    ],
    beta_header="Peer betas (5y monthly, Blume-adjusted)",
    skip_guide=True,                     # the template guide slide is not part of a case deck
    # ---- assumptions slide: the personnel cost ratio is the key judgement in the forecast
    pers_note="Personnel costs rose from 35.4% of revenue (2023) to 37.3% (2025) as the group added group-training hours and staff.",
    # ---- club economics slide (deck_slides6.unit_economics_slide)
    unit=dict(
        sources="Sources: SATS ASA Q4 2023-Q4 2025 reports and the Q2 2026 presentation (country EBITDA before IFRS 16 and before group "
                "overhead; clubs, members, ARPM), SATS Capital Markets Day 2025 (openings, expansion capex, payback, maintenance capex, "
                "leverage and distribution policy), case team estimates (Excel model).",
        margin_years=["2023", "2024", "2025", "Q2 2026"],
        margins=[("Norway", [0.26, 0.29, 0.31, 0.37]), ("Sweden", [0.21, 0.18, 0.19, 0.25]),
                 ("Finland", [0.10, 0.10, 0.11, 0.15]), ("Denmark", [0.03, 0.09, 0.10, 0.11])],
        margin_note="Country EBITDA before IFRS 16 and before group overhead (~NOK 0.6bn a year); Q2 is seasonally the strongest quarter.",
        # country, clubs, members ('000), ARPM NOK/month, country EBITDA margin Q2 2026 – Q2 2026 presentation p2, p20-23
        snapshot=[("Norway", 118, 341, 652, 0.37), ("Sweden", 92, 254, 634, 0.25), ("Finland", 32, 70, 606, 0.15),
                  ("Denmark", 28, 79, 594, 0.11), ("Group", 270, 744, 635, 0.22)],
        # company guidance (CMD 2025 / Q2 2026) for the comparison table; the model column is computed
        guidance=dict(openings="8-12 a year from 2027; 13 clubs committed through 2028",
                      capex="NOK 7-8m per club",
                      payback="About three years",
                      maturity="220 mature clubs earn ~19% more club EBITDA than the average club",
                      mcapex="~5% of revenue (4.6% LTM Q2 2026)",
                      fcf="Free cash flow 64% of EBITDA LTM Q2 2026 (after tax and interest)",
                      leverage="1.5-2.0x NIBD/EBITDA, lower end (1.1x at 30 Jun 2026)",
                      payout=">50% of net profit via semi-annual dividends and buybacks (152% in H1 2026)"),
    ),
    # ---- cash slide (deck_slides6.cash_slide)
    cash_sources="Sources: Case team estimates (Excel model: Output and Model sheets). EBITDAaL = EBITDA after lease payments (pre-IFRS 16); "
                 "free cash flow to equity after tax, interest, working capital and all capex. Buybacks at the modelled share price.",
    # ---- competition and macro slide (deck_slides6.competition_macro_slide)
    comp=dict(
        subtitle="SATS is the premium price leader at roughly twice the low-cost chains; Norwegian wage growth of ~4% is the cost line to watch",
        # operator, segment, markets, clubs, indicative monthly price, note
        rows=[("SATS / ELIXIA", "Premium, group training", "NO SE FI DK", "228", "NOK 450-1,000 by tier and club", "ARPM NOK 635 (Q2 2026)"),
              ("Fresh Fitness (SATS)", "Low-cost", "NO", "42", "NOK 299-399", "SATS's low-cost flank"),
              ("Nordic Wellness", "Mid / low-cost", "SE", "450+", "SEK 299-699", "Largest by clubs; targets 600 by 2030"),
              ("Fitness24Seven", "Low-cost, 24/7", "SE NO FI", "280+", "SEK 199-399", "Five countries incl. CO, TH"),
              ("EVO Fitness", "Low-cost, 24/7", "NO (+DE, CH)", "~75 (EST)", "NOK 249-399", "Unstaffed clubs"),
              ("Actic", "Mid-market", "SE", "~100", "n.a.", "Shrinking; Norway sold 2025"),
              ("PureGym / Fitness World", "Low-cost", "DK", "n.a.", "n.a.", "#1 in Denmark")],
        takeaway="SATS's price premium rests on group training (1,800 classes a day), club clusters in the capitals and the Fresh "
                 "Fitness flank. Sweden is the contested market: Nordic Wellness adds ~30 clubs a year and SATS's Swedish margin "
                 "(25% in Q2 2026) is two thirds of Norway's.",
        sources="Sources: operators' websites and price comparisons (klikk.no; Börskollen, Aug 2025; subger.com, Mar-Jul 2026) – list prices "
                "are indicative and not like-for-like (tiers, binding periods, start fees differ); club counts from company websites and job "
                "postings (Nordic Wellness, Fitness24Seven), Affärsvärlden (Actic) and SATS Q2 2026 (270 clubs incl. 42 Fresh Fitness). "
                "Macro: Norges Bank MPR 3/26, Riksbank MPR Sep 2026, Konjunkturinstitutet Sep 2026, Oslo Børs (10-year government bond). "
                "EST = case team estimate.",
    ),
    macro=dict(
        # indicator, Norway, Sweden
        rows=[("Policy rate (Oct 2026)", "4.50%", "1.75%"),
              ("CPI 2026E / 2027E", "3.3% / 2.6%", "1.5% / 2.1% (KPIF)"),
              ("Wage growth 2026E / 2027E", "4.4% / 4.0%", "3.5% / 3.4%"),
              ("10-year government bond (7 Oct 2026)", "4.71%", "–"),
              ("SATS revenue per member, Q2 2026 (curr. adj.)", "+7%", "+5%"),
              ("SATS country EBITDA margin, Q2 2026", "37%", "25%")],
        bullets=["**Price runs ahead of cost today:** ARPM +6% vs. total costs +4% currency adjusted in Q2 2026. The base case lets "
                 "the spread close – price/mix 2.5% against 3.0% fixed-cost inflation from 2028.",
                 "**Wages are the cost line:** personnel is 37% of revenue and Norwegian wage growth is 4.4%/4.0% – hence 3.25% "
                 "fixed-cost inflation in 2027 (wages on ~60% of the fixed base, CPI-indexed rent on the rest).",
                 "**Sweden has less pricing room:** KPIF of 1.5-2% and low-cost capacity – we model 2-3% price growth there and "
                 "let utilisation do the work. Norwegian rates keep the discount rate high (risk-free 4.71%)."],
    ),
    # ---- footnotes: replace the template's 'illustrative' wording with the real sources
    footnote_subs=[
        (" Example values – update before use.", ""),
        ("Bloomberg consensus as provided in the case material (example data – replace)", YF),
        ("Bloomberg consensus as provided in the case material", YF),
        ("Bloomberg consensus (case material)", YF),
        ("Norges Bank (risk-free rate), NFF/PwC risk premium survey, Bloomberg (peer betas)",
         "Norwegian 10-year government bond 7 Oct 2026 (risk-free rate), NFF/PwC risk premium survey 2025, Yahoo Finance (peer betas)"),
        ("EV incl. lease liabilities (IFRS 16 basis).",
         "EV excl. lease liabilities (pre-IFRS 16 basis); peers: 2026E = last twelve months, 2027E = next twelve months consensus."),
        ("Example Company ASA and all market data are fictional.",
         "Data: SATS ASA interim reports and Yahoo Finance (see sats_data.py for sources)."),
        (" Figures are illustrative.", ""),
        ("Figures are illustrative.", ""),
    ],
)


# ---- research report (deck_builder/build_report.py reads CT["report"]). Numbers in the text are quoted from the sources named
# in each exhibit; the model numbers (target, scenario values, estimates) are read from the workbook by the builder.
Q3 = "SATS ASA Q3 2026 interim report, 27 Oct 2026"
Q3D = "27 Oct 2026"
CT["report"] = dict(
    kind="Update after the Q3 2026 report",
    title="Operating leverage is showing up – the price does not yet",
    abstract="We keep BUY on SATS after a third quarter in which revenue per member rose 7% currency adjusted, EBITDA before IFRS 16 rose 22% "
             "to NOK 235m and the nine-month figure reached NOK 764m (+18%). Our 2026 estimates move up to the run-rate; the share price still "
             "implies an EBIT margin below today's. The target price and the scenario values are read from the model on the right.",
    memo=[
        ("Q3 2026: price did the work", "Revenue grew 2% reported and 7% currency adjusted to NOK 1 324m with 0.5% fewer members and six fewer clubs; "
         "operating costs excluding depreciation were flat reported (+6% currency adjusted). EBITDA before IFRS 16 rose 22% to NOK 235m and EBIT before "
         "IFRS 16 rose 33% to NOK 182m; EPS NOK 0.69 against 0.48 (all [Q3-26])."),
        ("Against the company's own targets", "The mid-term ambition is EBITDA before IFRS 16 of NOK 1.1bn. The last twelve months are at NOK 988m "
         "(871 + 764 − 647), 90% of the way there, and consensus has 2026 at 1 010 and 2027 at 1 137. The pipeline rose from 13 to 18 committed clubs "
         "through 2028 and the leverage range was widened to 1.0-2.0x with leverage at 1.1x."),
        ("What changed in our numbers", "Norway price/mix for 2026 is raised to 7.5% (from 5.5%) and fixed-cost inflation for 2026 is cut to 1.0% (from 1.5%) "
         "to match the nine-month run-rate; nothing else in the forecast is touched. The estimate-revision table shows every line old against new."),
        ("Valuation", "Fair value is 70% DCF and 30% peer multiples, rolled forward twelve months. The reverse DCF on the valuation page shows the final-year "
         "EBIT margin the price implies against ours and against the 11.7% earned in 2025; the case gate requires the gap to be at least one point."),
    ],
    case_lead="The thesis is unchanged: a largely fixed club cost base turns price increases and fuller clubs into margin, and the share price pays for "
              "little of it. Q3 2026 is the fourth quarter in a row in which price ran ahead of cost.",
    since_last=[("Operating leverage", "EBIT adj. margin rises from 11.7% (2025) to ~15% on a largely fixed cost base; 2026 EBITDA after leases 946 (first edition)",
                 "Q3 2026 EBITDA before IFRS 16 +22% to NOK 235m, nine months NOK 764m (+18%); LTM 988. Opex ex D&A flat reported on 2% fewer clubs", "confirmed"),
                ("Pricing power", "Price/mix 5.5% in Norway and 2-3% elsewhere in 2026; the kill criterion is group price/mix below 1.5%",
                 "ARPM +7% currency adjusted in every country in Q3; reported +7% in Norway, −2% in SEK/EUR/DKK on the stronger krone", "confirmed"),
                ("Roll-out", "7-8 net openings a year from 2027; 13 clubs committed through 2028",
                 "18 clubs committed through 2028; 3 openings and 6 closures in nine months of 2026 (268 clubs)", "on track"),
                ("Capital returns", "Buybacks to 1.25x leverage on top of a 50-60% payout; share count −4% a year",
                 "NOK 372m buybacks and NOK 271m dividends in nine months (148% of net profit); leverage 1.1x; target range widened to 1.0-2.0x", "confirmed"),
                ("Denmark and Finland", "Thin margins; Danish VAT cut the member base 4% (first-edition risk)",
                 "Danish members −4% y/y but country EBITDA +86% to NOK 16m on price; Finland +18% to NOK 15m", "watch")],
    since_last_source="First edition of the case (6 Oct 2026); " + Q3,
    thesis=["**Recurring revenue:** 85% of revenue is monthly membership fees (NOK 1 131m of 1 324m in Q3 2026).",
            "**Pricing power:** ARPM +7% currency adjusted in Q3 2026 in every country; Norway +7% reported to NOK 607 per month.",
            "**Fixed cost base:** ~70% of personnel and ~60% of other opex are fixed per club (case model); opex ex D&A flat reported in Q3 on 2% fewer clubs.",
            "**Capital returns:** NOK 643m returned in nine months (372 buybacks + 271 dividends) against net profit of NOK 435m; leverage 1.1x."],
    risks_down=["Low-cost chains (Nordic Wellness, Fitness24Seven, EVO) add capacity in the capitals and cap price increases – Sweden is the contested market.",
                "Norwegian wage growth of ~4% on a 37%-of-revenue personnel line reverses the operating leverage if ARPM growth falls below 2%.",
                "Denmark: the VAT change of 1 Jan 2026 cut the Danish member base by 4% y/y; a similar change elsewhere would repeat it.",
                "Roll-out execution: 8-12 openings a year from 2027 after years of a flat club count."],
    risks_up=["Members per club in Sweden back to the 2019 level earlier than modelled (a year of the base case in one step).",
              "A larger buyback than the policy implies while leverage sits at the bottom of the 1.0-2.0x range.",
              "Group training and premium tiers lift the mix beyond the 2.5-3% price growth in the model."],
    description=["SATS ASA is the largest fitness club operator in the Nordics: 268 clubs and 752 000 members at 30 Sep 2026 under the SATS, ELIXIA and "
                 "Fresh Fitness brands, with online training in the SATS app.",
                 "Revenue is membership fees (85%) plus personal training and retail; Norway is 47% of revenue, Sweden 33%, Finland 9%, Denmark 10% (Q3 2026).",
                 "The model is a location engine: clubs × members per mature club × revenue per member, with a three-year ramp for new clubs."],
    revenue_by_category=dict(year="2025A", rows=[("Membership revenue", 4574), ("Other revenues (PT, retail)", 935)],
                             source="SATS ASA Q4 2025 report, key figures", date="10 Feb 2026"),
    targets=[("EBITDA before IFRS 16, mid-term", "NOK 1.1bn (LTM Q3 2026: NOK 988m)", Q3 + ", p10"),
             ("Club openings", "8-12 a year from 2027; 18 committed through 2028", Q3 + ", CEO letter"),
             ("Leverage", "1.0-2.0x net debt / EBITDA before IFRS 16 (1.1x at 30 Sep 2026)", Q3 + ", p10"),
             ("Distribution", "≥ 50% of net profit as buybacks and semi-annual dividends; DPS to grow over time", Q3 + ", p10")],
    management=[("SG", "CEO – Sondre Gravir", "Joined SATS in 2018"), ("CE", "CFO – Cecilie Elde", "Joined SATS in 2016"),
                ("GS", "CDO – Gaute Sandal", "Chief Digital Officer, joined SATS in 2017")],
    owners=None,   # the company's largest-shareholders page loads its table dynamically and could not be read on 2 Nov 2026 – see the data map
    swot=dict(strengths=["#1 in Norway, Sweden and Finland, #2 in Denmark (company)", "Highest revenue per member among listed fitness peers (Visible Alpha not used; peers' reports)",
                         "Prepaid memberships: contract liabilities of NOK 632m fund working capital (30 Sep 2026)"],
              weaknesses=["Member base flat to down (−0.5% y/y) – growth is price, not volume", "Finland and Denmark earn 12% country margins against 30% in Norway"],
              opportunities=["Members per club in Sweden and Denmark below the Norwegian level", "18 committed clubs and 8-12 a year from 2027",
                             "Group training and premium tiers lift ARPM and cut churn (company)"],
              threats=["Low-cost capacity in the capitals", "Wage and rent inflation on a fixed base", "Regulation: VAT on services (Denmark 2026)"]),
    quarter_lead="The Q4 2026 report is due on 9 February 2027. Consensus for the quarter is public on the company's website (Modular Finance, seven "
                 "contributors); our quarter is the annual model split by the seasonality of 2024-2025, not a separate quarterly forecast.",
    deep_dives=[
        dict(title="Price against cost: every country lifted revenue per member faster than costs in Q3 2026",
             question="Operating leverage is the thesis. Did the quarter show price running ahead of cost in each country, or only in Norway?",
             text=["Revenue per member rose 7% currency adjusted in all four countries in Q3 2026 (Norway +7% reported; Sweden, Finland and Denmark +6% currency "
                   "adjusted and −2% reported on the stronger krone). Country EBITDA before IFRS 16 rose 9% in Norway, 17% in Sweden (+26% currency adjusted), "
                   "18% in Finland and 86% in Denmark; group EBITDA before IFRS 16 rose from NOK 192m to 235m.",
                   "The bridge by country shows where the NOK 43m came from: Norway and Sweden NOK 16-17m each, Denmark NOK 8m after the VAT-driven price "
                   "increase, Finland NOK 3m. Sweden's margin reached 24% (20%), still two thirds of Norway's 30%."],
             exhibits=[dict(kind="bar", title="Revenue per member by country, Q3 2025 vs Q3 2026 (NOK per month, reported)", x=["Norway", "Sweden", "Finland", "Denmark"],
                            series=[("Q3 2025", [566, 585, 575, 595]), ("Q3 2026", [607, 575, 566, 585])], source=Q3 + ", country pages", date=Q3D,
                            note="Reported in NOK; currency adjusted +7% in Norway, +6% in Sweden, Finland and Denmark (company)."),
                       dict(kind="waterfall", title="EBITDA before IFRS 16, Q3 2025 → Q3 2026 by segment (NOKm)", labels=["Q3 2025", "Norway", "Sweden", "Finland", "Denmark", "Group", "Q3 2026"],
                            values=[192, 16, 17, 3, 8, -1, 235], totals=[0, 6], source=Q3 + ", note 2 (segment EBITDA before IFRS 16)", date=Q3D),
                       dict(kind="bar", title="Country EBITDA margin before IFRS 16, Q3 2025 vs Q3 2026", x=["Norway", "Sweden", "Finland", "Denmark"],
                            series=[("Q3 2025", [0.296, 0.200, 0.100, 0.062]), ("Q3 2026", [0.299, 0.238, 0.125, 0.116])], unit="%", source=Q3 + ", country pages", date=Q3D),
                       dict(kind="bar", title="Country EBITDA before IFRS 16 by quarter (NOKm, before group overhead)", stacked=True,
                            x=["Q4 24", "Q1 25", "Q2 25", "Q3 25", "Q4 25", "Q1 26", "Q2 26", "Q3 26"],
                            series=[("Norway", [165, 180, 222, 172, 184, 198, 248, 187]), ("Sweden", [74, 74, 99, 89, 92, 82, 120, 105]),
                                    ("Finland", [17, 11, 19, 12, 16, 11, 19, 15]), ("Denmark", [12, 12, 14, 9, 26, 22, 16, 16])],
                            source="SATS ASA interim reports Q4 2025-Q3 2026, country pages", date=Q3D, note="Q2 is the seasonally strongest quarter; Q4 2025 Denmark includes the year-end effects the company notes."),
                       dict(kind="table", title="Group cost lines, Q3 2026 vs Q3 2025 and nine months (NOKm)", headers=["Line", "Q3 2026", "Q3 2025", "y/y", "9M 2026", "9M 2025", "y/y"],
                            rows=[["Revenue", "1 324", "1 293", "+2% (+7% cc)", "4 249", "4 081", "+4%"], ["Cost of goods sold", "(34)", "(35)", "−3%", "(109)", "(109)", "0%"],
                                  ["Personnel expenses", "(465)", "(461)", "+1%", "(1 550)", "(1 490)", "+4%"], ["Other operating expenses", "(293)", "(295)", "−1%", "(916)", "(908)", "+1%"],
                                  ["Lease payments (instalments + interest)", "(300)", "(311)", "−4%", "(913)", "(932)", "−2%"], ["EBITDA before IFRS 16", "235", "192", "+22%", "764", "647", "+18%"]],
                            source=Q3 + ", income statement and cash flow statement", date=Q3D, left=(3, 6), wrap=False)],
             into_model=[("Price/mix growth, Norway 2026E", "7.5% (first edition 5.5%) – ARPM +7% Q3, +6% YTD", "Drivers | priceA"),
                         ("Fixed-cost inflation 2026E", "1.0% (first edition 1.5%) – opex ex D&A +1.4% reported for 9M", "Drivers | cpi"),
                         ("Price/mix growth, Sweden and Finland/Denmark 2026E", "unchanged 2.0% / −1.0% (reported ARPM −2% in SEK/EUR/DKK translation)", "Drivers | priceB, priceC")]),
        dict(title="Utilisation: the member base is flat, so the next step of margin must come from fuller clubs",
             question="Members fell 0.5% y/y in Q3 2026 while clubs fell 2%. Are the remaining clubs filling up, and where is the headroom?",
             text=["Members per club rose in every country except Denmark: Norway 2 949 (2 916 a year earlier), Sweden 2 824 (2 695), Finland 2 250 (2 219), "
                   "Denmark 2 786 (2 929 after the VAT change). The company reports 1.9% more members per square metre and 2% more workouts.",
                   "The base case keeps like-for-like volume growth at 1.0% in Norway and 1.5% in Sweden for 2026 and lets it fade; the 2026 figures below are "
                   "the run-rate test of that assumption. The Danish member loss (−4%) is the one segment where the model's 0% for 2026 looks generous."],
             exhibits=[dict(kind="line", title="Members per club by country (members ÷ clubs at quarter end)", x=["Q4 24", "Q1 25", "Q2 25", "Q3 25", "Q4 25", "Q1 26", "Q2 26", "Q3 26"],
                            series=[("Norway", [2838, 2932, 2849, 2916, 2875, 2950, 2890, 2949]), ("Sweden", [2611, 2674, 2632, 2695, 2753, 2817, 2761, 2824]),
                                    ("Finland", [2290, 2290, 2226, 2219, 2219, 2250, 2188, 2250]), ("Denmark", [2828, 2966, 2929, 2929, 2964, 3000, 2821, 2786])],
                            source="SATS ASA interim reports Q4 2025-Q3 2026, country pages (members and clubs); own division", date=Q3D),
                       dict(kind="bar", title="Members ('000) and clubs by country, Q3 2026 vs Q3 2025", x=["Norway", "Sweden", "Finland", "Denmark"],
                            series=[("Members Q3 2025", [347, 256, 71, 82]), ("Members Q3 2026", [345, 257, 72, 78])], source=Q3 + ", country pages", date=Q3D,
                            note="Clubs: Norway 117 (119), Sweden 91 (95), Finland 32 (32), Denmark 28 (28)."),
                       dict(kind="line", title="Members by country ('000, quarter end)", x=["Q4 24", "Q1 25", "Q2 25", "Q3 25", "Q4 25", "Q1 26", "Q2 26", "Q3 26"],
                            series=[("Norway", [332, 346, 339, 347, 345, 351, 341, 345]), ("Sweden", [248, 254, 250, 256, 256, 262, 254, 257]),
                                    ("Finland", [71, 71, 69, 71, 71, 72, 70, 72]), ("Denmark", [82, 86, 82, 82, 83, 84, 79, 78])],
                            source="SATS ASA interim reports Q4 2025-Q3 2026, country pages", date=Q3D),
                       dict(kind="line", title="Revenue per member by country (NOK per month, reported)", x=["Q4 24", "Q1 25", "Q2 25", "Q3 25", "Q4 25", "Q1 26", "Q2 26", "Q3 26"],
                            series=[("Norway", [589, 622, 609, 566, 607, 653, 652, 607]), ("Sweden", [600, 623, 641, 585, 651, 654, 634, 575]),
                                    ("Finland", [623, 626, 611, 575, 634, 635, 606, 566]), ("Denmark", [604, 632, 618, 595, 654, 625, 594, 585])],
                            source="SATS ASA interim reports Q4 2025-Q3 2026, country pages", date=Q3D,
                            note="Q3 is the seasonally weakest quarter for ARPM (summer freezes); reported NOK, so the 2026 figures for Sweden, Finland and Denmark carry the stronger krone.")],
             into_model=[("Like-for-like volume growth 2026E", "Norway 1.0%, Sweden 1.5%, Finland & Denmark 0.0% – unchanged; members per club +1% to +5% y/y except Denmark", "Drivers | lflA/B/C"),
                         ("Net new clubs 2026E", "−1 per segment (3 openings, 6 closures to Q3) – unchanged", "Drivers | netA/B/C")]),
        dict(title="Targets against delivery: 90% of the way to the NOK 1.1bn ambition",
             question="The CMD 2025 set an EBITDA-before-IFRS-16 ambition of NOK 1.1bn, 8-12 openings a year, leverage of 1.5-2.0x (now 1.0-2.0x) and a payout above 50%. Where is each one after Q3 2026?",
             text=["EBITDA before IFRS 16 has gone from NOK 615m (2023) to 737m (2024), 871m (2025) and 988m in the twelve months to September 2026 – NOK 112m short of the "
                   "ambition. Consensus has 2026 at 1 010 and 2027 at 1 137; our model has 1 001 and 1 093, i.e. we reach the ambition a year later than the market does.",
                   "Openings are the one target behind plan: three openings and six closures in nine months of 2026 against a plan of 8-12 openings a year from 2027. The pipeline "
                   "has moved (18 committed clubs, from 13), which is what the roll-out variant perception on page 2 watches."],
             exhibits=[dict(kind="bar", title="EBITDA before IFRS 16: delivered against the mid-term ambition (NOKm)", x=["2023", "2024", "2025", "LTM Q3 2026", "2026E cons.", "2027E cons.", "Ambition"],
                            series=[("EBITDA before IFRS 16", [615, 737, 871, 988, 1010, 1137, 1100])], legend=False,
                            source="SATS ASA annual and interim reports (2023-2025, LTM); consensus published by SATS (Modular Finance, 28 Oct 2026); CMD 2025 ambition", date="28 Oct 2026",
                            note="LTM = FY2025 871 + 9M 2026 764 − 9M 2025 647. The ambition has no date; the company says progress 'is expected to unfold gradually'."),
                       dict(kind="table", title="Company targets against the latest actuals", headers=["Target (source)", "Level", "Latest actual", "Status"],
                            rows=[["EBITDA before IFRS 16 (CMD 2025, Q3 2026 report)", "NOK 1.1bn mid-term", "NOK 988m LTM Q3 2026 (90%)", "on track"],
                                  ["Club openings (CMD 2025)", "8-12 a year from 2027", "3 openings, 6 closures 9M 2026; 18 committed through 2028", "behind, pipeline growing"],
                                  ["Leverage (Q3 2026 report)", "1.0-2.0x net debt / EBITDA before IFRS 16", "1.1x", "at the bottom of the range"],
                                  ["Distribution (Q3 2026 report)", "≥ 50% of net profit; DPS rising", "NOK 643m vs net profit 435m (148%) in 9M 2026", "above"],
                                  ["Maintenance capex (CMD 2025)", "~5% of revenue", "NOK 131m on 4 249m (3.1%) in 9M 2026", "below – a Q4 catch-up is usual"]],
                            source="SATS CMD 2025; " + Q3, date=Q3D, left=(1, 2, 3))],
             into_model=[("Mid-term ambition in the model", "EBITDA after leases 1 001 (2026E), 1 093 (2027E), 1 178 (2028E) – the ambition is reached in 2027-28", "Model | ebitdaal"),
                         ("Openings 2027E-2028E", "+7 / +8 net – the lower end of 8-12 less closures", "Drivers | netA/B/C")]),
        dict(title="Capital returns and the pipeline: NOK 643m returned in nine months, 18 clubs committed",
             question="Can the company return more than half of net profit and still fund 8-12 openings a year?",
             text=["Nine months to September 2026: free cash flow NOK 369m before the seasonally strong fourth quarter, buybacks NOK 372m (8.7m shares), "
                   "dividends NOK 271m, net debt NOK 1 056m and leverage 1.1x. A new club costs NOK 7-8m (CMD 2025) – ten a year is NOK 70-80m, a fifth of free cash flow.",
                   "The model's buybacks of ~NOK 416m in 2026 and ~NOK 350m a year after that keep leverage at 1.25x; the widened range (1.0-2.0x) makes that the "
                   "conservative end. The share count falls about 4% a year in the base case."],
             exhibits=[dict(kind="table", title="Cash generation and distribution, nine months 2026 (NOKm)", headers=["Item", "9M 2026", "9M 2025", "Source"],
                            rows=[["Net cash flow from operations", "1 428", "1 425", "cash flow statement"], ["Lease instalments and interest", "(913)", "(932)", "cash flow statement"],
                                  ["Capex", "(145)", "(212)", "cash flow statement"], ["Free cash flow (company APM)", "369", "262", "key figures"],
                                  ["Share buybacks", "(372)", "(177)", "cash flow statement"], ["Dividends paid", "(271)", "(127)", "cash flow statement"],
                                  ["Net debt, end of period", "1 056", "1 087", "key figures"], ["Leverage (x)", "1.1", "1.3", "key figures"]],
                            source=Q3, date=Q3D, left=(3,)),
                       dict(kind="table", title="Club pipeline and openings", headers=["Item", "Value", "Source"],
                            rows=[["Clubs at 30 Sep 2026", "268 (274 a year earlier)", Q3], ["Committed openings through 2028", "18 (13 at the Q2 report)", Q3 + ", CEO letter"],
                                  ["Planned openings from 2027", "8-12 a year", Q3 + ", outlook"], ["Capex per new club", "NOK 7-8m, ~3-year payback", "CMD 2025"],
                                  ["Model: net new clubs 2027E / 2028E", "+7 / +8 (all segments)", "Drivers | net"]],
                            source=Q3 + "; SATS CMD 2025; case model", date=Q3D, left=(1, 2))],
             into_model=[("Leverage target", "1.25x NIBD / EBITDA after leases – unchanged (range widened to 1.0-2.0x)", "Drivers | lev_t"),
                         ("Payout ratio 2026E-2027E", "50% – unchanged; buybacks take leverage to the target", "Drivers | payout"),
                         ("Diluted shares", "192.1m + 1.1m matching shares", "Inputs | shares, dilutive")]),
    ],
    competition={
        "Norway": dict(intro="SATS is the premium price leader; Fresh Fitness is its own low-cost flank. EVO (unstaffed, 24/7) is the low-cost challenger in the cities.",
                       rows=[("SATS", "Premium, group training", "117 clubs (Q3 2026)", "NOK 450-1 000 by tier and club", "12 months or none", Q3 + "; sats.no", Q3D),
                             ("Fresh Fitness (SATS)", "Low-cost", "42 clubs (Q2 2026)", "NOK 299-399", "None", "SATS Q2 2026 presentation; freshfitness.no", "Aug 2026"),
                             ("EVO Fitness", "Low-cost, 24/7, unstaffed", "~75 (EST)", "NOK 249-399", "None", "evofitness.no; klikk.no price comparison", "Aug 2025"),
                             ("Actic", "Mid-market", "Norway sold 2025", "n.a.", "n.a.", "Affärsvärlden", "2025")],
                       prices=[("SATS regional", 749), ("SATS one club", 649), ("Fresh Fitness", 349), ("EVO", 349)],
                       price_source="klikk.no price comparison (Aug 2025) and the operators' websites; list prices for a comparable monthly membership",
                       price_note="List prices are indicative and not like-for-like: tiers, binding periods and start fees differ. Not re-collected for this edition (EST where marked).",
                       takeaway="The premium is about 2x the low-cost price; Norway's ARPM still rose 7% in Q3 2026, so the premium holds. The kill criterion is group price/mix growth below 1.5%."),
        "Sweden": dict(intro="The contested market: Nordic Wellness and Fitness24Seven add capacity every year and Sweden's country margin (24%) is two thirds of Norway's.",
                       rows=[("SATS", "Premium, group training", "91 clubs", "SEK 499-799", "12 months or none", Q3 + "; sats.se", Q3D),
                             ("Nordic Wellness", "Mid / low-cost", "450+ clubs; targets 600 by 2030", "SEK 299-699", "12 months", "nordicwellness.se; Börskollen", "Aug 2025"),
                             ("Fitness24Seven", "Low-cost, 24/7", "280+ clubs (5 countries)", "SEK 199-399", "None", "fitness24seven.com; job postings", "Jul 2026"),
                             ("Actic", "Mid-market", "~100 clubs, shrinking", "n.a.", "n.a.", "Affärsvärlden", "2025")],
                       prices=[("SATS", 699), ("Nordic Wellness", 499), ("Fitness24Seven", 299)],
                       price_source="Börskollen (Aug 2025), subger.com (Mar-Jul 2026), operators' websites", price_note="Indicative list prices, SEK per month; not like-for-like.",
                       takeaway="We model 2-3% price growth in Sweden against 3-3.5% in Norway and let utilisation (members per club +5% y/y in Q3 2026) do the work."),
        "Finland and Denmark": dict(intro="Small segments (9% and 10% of revenue) with thin margins; Denmark's VAT change of 2026 is the regulatory precedent.",
                                    rows=[("ELIXIA (SATS)", "Premium", "32 clubs, Finland", "EUR 60-100", "12 months or none", Q3 + "; elixia.fi", Q3D),
                                          ("SATS Denmark", "Premium", "28 clubs, Greater Copenhagen", "DKK 450-650", "12 months or none", Q3 + "; sats.dk", Q3D),
                                          ("PureGym / Fitness World", "Low-cost", "#1 in Denmark (c.40 clubs in Copenhagen)", "n.a.", "n.a.", "puregym.dk", "2025"),
                                          ("Fitness24Seven, Fressi", "Low-cost / mid", "largest chains in Finland", "n.a.", "n.a.", "operators' websites", "2025")],
                                    takeaway="Both countries earn 12% country margins; the model keeps price/mix at −1% in 2026 (Danish VAT) and 2.5% after."),
    },
    macro=dict(columns=["Norway", "Sweden"],
               rows=[("Policy rate", "4.50% (Oct 2026)", "1.75% (Sep 2026)", "Norges Bank; Riksbank", "Oct 2026"),
                     ("CPI 2026E / 2027E", "3.3% / 2.6%", "1.5% / 2.1% (KPIF)", "Norges Bank MPR 3/26; Riksbank MPR Sep 2026", "Sep 2026"),
                     ("Wage growth 2026E / 2027E", "4.4% / 4.0%", "3.5% / 3.4%", "Norges Bank MPR 3/26; Konjunkturinstitutet", "Sep 2026"),
                     ("10-year government bond", "4.71% (7 Oct 2026)", "–", "Oslo Børs", "7 Oct 2026"),
                     ("SATS ARPM growth, Q3 2026 (currency adjusted)", "+7%", "+6%", Q3, Q3D),
                     ("SATS country EBITDA margin, Q3 2026", "30%", "24%", Q3, Q3D)],
               bullets=["**Wages → personnel costs (37% of revenue):** Norwegian wage growth of 4.4%/4.0% on ~60% of the fixed base is why fixed-cost inflation is 3.25% in 2027 and 3.0% after.",
                        "**CPI → rent:** leases are CPI-indexed; Norwegian CPI 2.6% in 2027 is the rent line. Nine-month lease payments fell 2% on the stronger krone and fewer clubs.",
                        "**Policy rate and bond yield → discount rate:** risk-free 4.71% keeps the WACC at 9.1%; a 1pp lower WACC is worth about NOK 5 per share (sensitivity table).",
                        "**FX:** a stronger NOK cuts reported Swedish, Finnish and Danish revenue and costs alike (−5pp on Q3 revenue growth); the model is in reported NOK."]),
    sources=[("SATS ASA interim reports Q4 2019-Q3 2026 (satsgroup.com / MFN)", "History, quarterly series, balance sheet, shares, KPIs, targets, pipeline", "27 Oct 2026 (Q3 2026)"),
             ("SATS ASA Capital Markets Day 2025", "Mid-term ambition, openings, capex per club, payback, leverage and distribution policy", "2025"),
             ("Consensus published by SATS (Modular Finance, 7 contributors)", "Revenue, EBITDA, EBITDA before IFRS 16, net profit, members for Q4 2026E-2027E; mean target price", "28 Oct 2026"),
             ("Yahoo Finance via yfinance", "Daily closes for SATS.OL and OSEBX.OL, EPS consensus (5 analysts), recommendation split, peer multiples (23 Sep 2026)", "2 Nov 2026"),
             ("SATS financial calendar as published on MFN", "Next events (Q4 2026 report 9 Feb 2027, AGM 13 Apr 2027)", "27 Oct 2026"),
             ("Norges Bank MPR 3/26, Riksbank MPR Sep 2026, Konjunkturinstitutet", "Policy rates, CPI and wage forecasts", "Sep-Oct 2026"),
             ("Oslo Børs", "10-year government bond yield (risk-free rate)", "7 Oct 2026"),
             ("PwC/NFF Risikopremien 2025", "Market risk premium, size premium, long-term growth", "2025"),
             ("Operators' websites; klikk.no, Börskollen, subger.com price comparisons; Affärsvärlden", "Competitor clubs and indicative prices (first-edition observations)", "Aug 2025-Jul 2026"),
             ("Case model (Equity Research Toolkit workbook, model_builder/sats_data.py)", "Every estimate, scenario, sensitivity and valuation figure", "2 Nov 2026")],
    revision_notes=["Norway price/mix 2026E raised to 7.5% from 5.5%: ARPM +7% in Q3 and +6% for nine months, nine-month Norwegian revenue +8%.",
                    "Fixed-cost inflation 2026E cut to 1.0% from 1.5%: opex ex D&A +1.4% reported for nine months on six fewer clubs and a stronger krone; lease payments −2%.",
                    "Market data: price NOK 43.95 (30 Oct 2026 close), balance sheet 30 Sep 2026, 192.1m shares; consensus from the company's published table (28 Oct 2026).",
                    "No change to 2027-2033 drivers, scenarios, WACC or terminal assumptions."],
    reverse_text=["The implied final-year margin sits between the 11.7% earned in 2025 and our 15.1%: the price pays for part of the operating leverage, not for the roll-out.",
                  "Solved on growth instead, the price implies a revenue CAGR half a point below ours with the same cost base.",
                  "The gate asks for a 1pp gap on at least one driver and 10% between DCF and price; both are met (valuation page)."],
    data_map=[("Largest shareholders", "Not collected", "satsgroup.com loads the table dynamically; the 2025 annual report's top-20 list was not retrieved for this edition"),
              ("Quarterly history by segment, Q4 2024-Q3 2026", "Collected", "interim reports (key figures, note 2, country pages)"),
              ("Consensus by line (revenue, EBITDA, EBITDA before IFRS 16, net profit, members; Q4 2026E, 2026E, 2027E)", "Have", "published by SATS (Modular Finance, 7 contributors, 28 Oct 2026)"),
              ("Consensus EBIT, EPS, DPS by year", "Partly", "EPS from Yahoo Finance (5 analysts); EBIT and DPS not published"),
              ("Price study (list prices over time, competitor screen)", "Not re-collected", "the first-edition observations (Aug 2025-Jul 2026) are reused with their dates"),
              ("Forward P/E history on consensus", "Missing", "Bloomberg/FactSet; replaced by trailing multiples on year-end prices")],
    flips=["Price/mix 1pp a year lower than the base case takes the DCF to NOK 35 and the rating to SELL (target 41); 0.5pp lower gives NOK 45 and a BUY at a target of 50 (what-if runs).",
           "Margins reverting to the last three years' mean (stress #4) gives NOK 31 – a SELL at a target of 33.",
           "RONIC equal to the WACC in the terminal value gives NOK 48 (removes NOK 6 per share); a WACC one point higher gives NOK 47 – the rating survives both.",
           "The personnel ratio staying at the 2025 level (no operating leverage on wages) gives NOK 47.",
           "The bear case – price growth capped near 2% by low-cost competition while wages grow 4% – is NOK 31 today and NOK 38 in twelve months (SELL)."],
    unknowns=["Churn by membership tier and the share of members with group training – the company gives growth rates, not levels.",
              "Rent indexation terms and lease maturities per country beyond the aggregate lease liability.",
              "The October 2026 buyback volume and the next programme's size (first visible in the Q4 report).",
              "How much of the 7% currency-adjusted ARPM growth is list price and how much is mix (tiers, add-ons) – the price tracker was not updated for this edition.",
              "Peer unit economics on a consistent basis (members, revenue per member, cost per club) – available to the sell side through Visible Alpha."],
)
