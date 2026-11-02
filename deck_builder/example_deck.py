"""Example Company ASA – narrative for the report template. EVERYTHING HERE IS FICTIONAL, like example_data.py: the
company, the competitors, the prices, the macro table and the shareholders are invented to exercise every section of
the report. Copy this file to <company>_deck.py for a real case and replace every entry with sourced material.

Only the `report` key is used by build_report.py; the pitch deck keeps its template texts (deck_case.ct defaults).
"""

FIC = "Fictional example data (example_deck.py)"
D = "1 Oct 2026"

CT = dict(
    report=dict(
        kind="Initiation (template example)",
        title="Pricing power on a fixed cost base",
        memo=[
            ("Why now", "The next report is the first after the price increase; the quarter preview shows what a clean read of operating "
                        "leverage looks like on our numbers against the one consensus line that is public."),
            ("Against the company's own targets", "Management guides to a mid-term margin of 20 % before leases; our base case gets to 18 % "
                                                  "and the share price implies less. The gap is the case."),
            ("What changed", "First report – no previous estimates. Each build stores its estimates, so the next report shows old against new."),
            ("Valuation", "70 % DCF and 30 % peer multiples, rolled forward twelve months. The bear case sits below the price, the bull case "
                          "is the company's own ambition delivered."),
        ],
        case_lead="One sentence a reader should remember: the market pays for today's margin, not for the operating leverage of the next three years.",
        thesis=["**Recurring revenue** – memberships are 80 % of sales and are paid monthly in advance.",
                "**Pricing power** – list prices rose faster than costs in each of the last three years (deep dive 1).",
                "**Fixed cost base** – about two thirds of costs are fixed per location (deep dive 2), so price and utilisation drop through.",
                "**Capital returns** – net debt below 1.5x EBITDA after leases; the payout policy is more than half of net profit."],
        risks_down=["A low-cost entrant caps price increases in the capital region.", "Wage inflation above price growth for two years running.",
                    "A VAT change on the service lines (fictional regulatory risk)."],
        risks_up=["Utilisation returns to the pre-pandemic level a year early.", "A larger buyback than the policy implies.",
                  "A bolt-on acquisition in segment C at the right multiple."],
        description=["Example Company ASA is a fictional Nordic operator of subscription-based service locations in three segments (A, B, C).",
                     "Revenue is monthly memberships (about 80 %) plus ancillary services and retail.",
                     "The model is a location engine: locations × members per mature location × price, with a three-year ramp for new locations."],
        revenue_by_category=dict(year="2025A", rows=[("Memberships", 4350), ("Ancillary services", 720), ("Retail", 363)], source=FIC, date=D),
        targets=[("Mid-term EBITDA margin before leases", "20 %", FIC), ("Openings per year", "6-8", FIC), ("Leverage", "1.0-2.0x NIBD / EBITDA after leases", FIC),
                 ("Payout", "> 50 % of net profit", FIC)],
        management=[("CEO", "CEO – A. Example", "Fictional; joined 2018"), ("CFO", "CFO – B. Example", "Fictional; joined 2016")],
        owners=dict(rows=[("Founder Holding AS", 0.21), ("Nordic Pension Fund", 0.08), ("Index Fund I", 0.05), ("Value Partners", 0.04), ("Treasury shares", 0.01)],
                    source=FIC, date=D),
        swot=dict(strengths=["Largest network in each market (fictional)", "Highest revenue per member among listed peers", "Prepaid memberships fund working capital"],
                  weaknesses=["Segment C still loss-making", "Slower unit growth than peers"],
                  opportunities=["Utilisation back to 2019 levels", "Premium tiers and group training lift the mix"],
                  threats=["Low-cost capacity in the capitals", "Wage and rent inflation on a largely fixed base"]),
        quarter_lead="The quarter is the first with the January price increase in every month; we expect the increase to show in revenue per member "
                     "before it shows in costs.",
        deep_dives=[
            dict(title="Price: how much of revenue growth is price, and is it above the market?",
                 question="If price is the engine, the list-price history and the competitor screen must show room to continue.",
                 text=["Our fictional price tracker records the list price of the comparable membership each January. The most popular membership "
                       "rose 4 % a year on average; the premium tier rose faster.",
                       "The competitor screen puts the company at the top of the range, with the low-cost chains at about half the price."],
                 exhibits=[dict(kind="bar", title="List price of the comparable membership, NOK per month", x=["2021", "2022", "2023", "2024", "2025", "2026"],
                                series=[("Regional membership", [549, 569, 599, 629, 649, 669]), ("Premium", [699, 739, 779, 829, 869, 899])], source=FIC, date=D),
                           dict(kind="hbar", title="Competitor price screen – one location, no binding (NOK per month)",
                                labels=["Example Company", "Operator B", "Operator C", "Low-cost D", "Low-cost E"], values=[669, 629, 599, 349, 299], highlight="Example", unit="nok",
                                source=FIC + " – fictional operator websites", date=D)],
                 into_model=[("Price/mix growth, segment A", "3.0 % a year 2027-29", "Drivers | px_a"), ("Price/mix growth, segment B", "2.5 % a year", "Drivers | px_b")]),
            dict(title="Utilisation: members per location against the pre-pandemic level",
                 question="Where is the next step of margin: more members in the same locations.",
                 text=["Members per mature location are still 6 % below 2019 in segment B. Closing half the gap over three years is the base case; closing it fully is the bull case."],
                 exhibits=[dict(kind="line", title="Members per location (index, Q4 2019 = 100)", x=["Q4 19", "Q4 20", "Q4 21", "Q4 22", "Q4 23", "Q4 24", "Q4 25"],
                                series=[("Segment A", [100, 91, 95, 99, 100, 101, 102]), ("Segment B", [100, 88, 90, 92, 93, 93, 94])], source=FIC, date=D),
                           dict(kind="waterfall", title="EBITDA after leases bridge 2025A → 2026E (NOKm)", labels=["2025A", "Price", "Volume", "New locations", "Costs", "2026E"],
                                values=[1190, 180, 60, 40, -170, 1300], totals=[0, 5], source=FIC + "; case model", date=D)],
                 into_model=[("Like-for-like volume growth, segment B", "1.5 % → 0.5 % a year", "Drivers | lfl_b")]),
        ],
        competition={
            "Capital region (fictional)": dict(rows=[("Example Company", "Premium", "94", "NOK 549-899", "12 months", FIC, D), ("Operator B", "Mid-market", "40", "NOK 499-629", "None", FIC, D),
                                                     ("Low-cost D", "Low-cost, 24/7", "60", "NOK 299-349", "None", FIC, D)],
                                               prices=[("Example Company", 669), ("Operator B", 629), ("Low-cost D", 349)], price_note="Fictional list prices, one location, no binding.",
                                               takeaway="The premium is about 2x the low-cost price; the case needs the premium to hold, not to widen."),
            "Second market (fictional)": dict(rows=[("Example Company", "Premium", "77", "SEK 499-799", "12 months", FIC, D), ("Operator F", "Low-cost", "120", "SEK 249-399", "None", FIC, D)],
                                              takeaway="More low-cost capacity than in the capital region: we model lower price growth here (2.5 %)."),
        },
        macro=dict(columns=["Country 1", "Country 2"],
                   rows=[("Policy rate", "4.50 %", "1.75 %", "Central banks (fictional values)", D), ("CPI 2026E / 2027E", "3.3 % / 2.6 %", "1.5 % / 2.1 %", FIC, D),
                         ("Wage growth 2026E / 2027E", "4.4 % / 4.0 %", "3.5 % / 3.4 %", FIC, D), ("Consumer confidence", "-9", "-5", FIC, D)],
                   bullets=["**Wages → personnel costs** (37 % of revenue): 4 % wage growth on the fixed part is the 3.25 % fixed-cost inflation in 2027.",
                            "**CPI → rent**: leases are CPI-indexed; 2.6 % CPI is the rent line.", "**Policy rate → discount rate** through the risk-free rate."],
                   exhibits=[dict(kind="line", title="Policy rate path (fictional), %", x=["2024", "2025", "2026", "2027", "2028"], series=[("Country 1", [0.045, 0.045, 0.045, 0.04, 0.035]), ("Country 2", [0.04, 0.0225, 0.0175, 0.02, 0.02])],
                                  unit="%", source=FIC, date=D)]),
        revision_notes=["Fictional: price/mix in segment A raised to 3.0 % after the January list prices."],
        reverse_text=["The implied margin is below today's margin: the price assumes the operating leverage reverses.",
                      "Our base case is the company's mid-term ambition less two points."],
        data_map=[("Quarterly segment consensus", "Missing", "Infront/Bloomberg not used"), ("Price tracker 2019-2026", "Collected", "fictional tracker, January each year")],
        flips=["Price/mix 1pp lower a year turns the rating to HOLD; 1.5pp lower to SELL (what-if runs).",
               "RONIC = WACC in the terminal value removes about a fifth of the value."],
        unknowns=["Churn by membership tier – not disclosed.", "Rent indexation terms per location – not disclosed.", "The split of 'other revenue' between services and retail by country."],
        events=[("2026-11-12", "Q3 2026 report (fictional)", FIC), ("2027-02-11", "Q4 2026 report (fictional)", FIC)],
        history=[("2026-10-01", "BUY", 146, 122.0, "Initiation (fictional)")],
    ),
)
