"""SATS ASA – narrative text for the pitch deck. Numbers on the slides come from the Excel model; the facts below are
from SATS ASA's interim reports (Q4 2019-Q2 2026), satsgroup.com (management) and, for the size of the Nordic fitness
market, EuropeActive/Deloitte as quoted in the 2026 Pareto case workbook. Keys are read with deck_case.ct(key, default)."""

YF = "Yahoo Finance consensus (Sep 2026)"

CT = dict(
    # ---- cover
    cover_title="SATS – Healthy body, healthy margins",
    cover_dates="Share price and estimates as of 30.09.26",
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
    ov_pricing="**Pricing power:** revenue per member up ~6% a year in 2024-25 while the member base grew",
    ov_leverage="**Operating leverage:** EBITDA before IFRS 16 up from NOK 0.61bn (2023) to NOK 0.87bn (2025)",
    mgmt=[("SG", "CEO – Sondre Gravir", "Joined SATS in 2018"),
          ("CE", "CFO – Cecilie Elde", "Joined SATS in 2016"),
          ("GS", "CDO – Gaute Sandal", "Chief Digital Officer, joined SATS in 2017")],
    ov_hist_from=4,                      # charts from 2023A (2020-22 distorted by the pandemic)
    # ---- market overview (deck_slides5.market_overview_kpi)
    market=dict(
        chapter="#2 Leading positions in every Nordic market",
        subtitle="SATS is #1 in Norway, Sweden and Finland and #2 in Denmark – price, utilisation and new clubs drive growth",
        sources="Sources: SATS ASA interim reports (clubs, members, revenue per member, market positions, signed locations); "
                "Nordic fitness members (5.2m, 2025): EuropeActive/Deloitte European Health & Fitness Market Report 2025, as quoted in the 2026 Pareto case workbook.",
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
                   ("30", "new club locations signed through 2028, against a target of 8-12 openings a year")],
        boxes=[("Opportunities", ["**Price increases above cost inflation** backed by product tiers and upgrades",
                                  "**Higher utilisation:** more members per club at near-zero marginal cost",
                                  "**Roll-out:** 8-12 new clubs a year with a ~3-year payback"]),
               ("Disruption", ["**Boutique studios and digital training** – met with premium concepts inside the clubs and the SATS app",
                               "**Low-cost segment** – addressed with Fresh Fitness (42 clubs in Norway)"]),
               ("Threats", ["**Low-cost expansion** in the big cities could cap pricing power",
                            "**Regulation:** Denmark's VAT on group training and PT (2026) cut the Danish member base by 4%"])],
    ),
    # ---- valuation slide
    thesis_quality="**Little operating leverage priced in:** the share price implies a {m_imp:.1f}% EBIT margin in {yl} (11.7% today) – we model {m_our:.1f}%",
    thesis_growth="**Growth engine intact:** revenue per member, members per club and ~9 net openings a year from 30 signed leases",
    thesis_catalysts="**Catalysts:** Q3 report 27 Oct 2026 (margins), the next buyback programme, the 2027 opening pipeline",
    # ---- risks: title, description, probability (1-3), impact (1-3)
    risks=[
        ("Low-cost competition", "Low-cost chains add capacity in the big cities and cap price increases; SATS answers with Fresh Fitness and product tiers.", 3, 3),
        ("Cost inflation", "Personnel and rent are ~70% of costs – Nordic wage growth above the growth in revenue per member reverses the operating leverage.", 2, 3),
        ("Denmark and Finland", "Denmark lost 4% of its members after VAT on group training and PT (2026); both countries earn thin margins.", 3, 1),
        ("Roll-out execution", "8-12 openings a year after years of a flat club count; new clubs may take longer than three years to mature.", 2, 2),
        ("Consumer slowdown", "Memberships are discretionary: the member base fell 9% in 2020 and took two years to recover.", 1, 3),
    ],
    beta_header="Peer betas (5y monthly, Blume-adjusted)",
    skip_guide=True,                     # the template guide slide is not part of a case deck
    # ---- footnotes: replace the template's 'illustrative' wording with the real sources
    footnote_subs=[
        (" Example values – update before use.", ""),
        ("Bloomberg consensus as provided in the case material (example data – replace)", YF),
        ("Bloomberg consensus as provided in the case material", YF),
        ("Bloomberg consensus (case material)", YF),
        ("Norges Bank (risk-free rate), NFF/PwC risk premium survey, Bloomberg (peer betas)",
         "Norwegian 10-year government bond 30 Sep 2026 (risk-free rate), NFF/PwC risk premium survey, Yahoo Finance (peer betas)"),
        ("EV incl. lease liabilities (IFRS 16 basis).",
         "EV excl. lease liabilities (pre-IFRS 16 basis); peers: 2026E = last twelve months, 2027E = next twelve months consensus."),
        ("Example Company ASA and all market data are fictional.",
         "Data: SATS ASA interim reports and Yahoo Finance (see sats_data.py for sources)."),
        (" Figures are illustrative.", ""),
        ("Figures are illustrative.", ""),
    ],
)
