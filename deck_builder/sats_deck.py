"""SATS ASA – narrative text for the pitch deck. Numbers on the slides come from the Excel model; the facts below are
from SATS ASA's interim reports and presentations (Q4 2019-Q2 2026), the 2025 Capital Markets Day, satsgroup.com
(management) and, for the size of the Nordic fitness market, EuropeActive/Deloitte as quoted in the 2026 Pareto case
workbook. Macro figures: Norges Bank, the Riksbank and Konjunkturinstitutet (September 2026). Keys are read with
deck_case.ct(key, default)."""

YF = "Yahoo Finance consensus (Oct 2026)"

CT = dict(
    # ---- cover
    cover_title="SATS – Healthy body, healthy margins",
    cover_dates="Share price and estimates as of 06.10.26",
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
    ov_leverage="**Operating leverage:** EBITDA before IFRS 16 up from NOK 0.61bn (2023) to NOK 0.87bn (2025) and NOK 0.95bn LTM",
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
    thesis_catalysts="**Catalysts:** Q3 report 27 Oct 2026 (margins), the next buyback programme, the 2027 opening pipeline",
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
