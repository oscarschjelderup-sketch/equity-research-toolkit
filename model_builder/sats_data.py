"""SATS ASA – real case data for the Equity Research DCF toolkit (phase 3).

Same interface as example_data.py. All figures in NOKm unless stated. History 2019A-2025A, forecast 2026E-2033E,
valuation date 6 October 2026 (share price of 6 October 2026, balance sheet of 30 June 2026).

Sources (all public; the quarterly reports are at satsgroup.com/reports-presentations)
  [Q4-19] ... [Q4-25]  SATS ASA fourth-quarter interim reports 2019-2025: full-year P&L, balance sheet and cash flow,
                       note 2 (segments), note 4 (shares), notes 6-8 (intangibles, PP&E, right-of-use assets) and the
                       country pages (clubs, members, ARPM). Each year is taken from the latest report that shows it.
  [Q2-26]  SATS ASA Q2 2026 interim report and presentation (Aug 2026): H1 2026, balance sheet 30 June 2026, share
           count, dividend, buybacks, committed club pipeline (13 clubs through 2028), country KPIs
  [CMD-25] SATS ASA Capital Markets Day 2025: mid-term ambitions (EBITDA before IFRS 16 ~NOK 1.1bn, 8-12 openings a year,
           expansion capex NOK 7-8m per club, payback ~3 years, maintenance capex ~5% of revenue, leverage 1.5-2.0x)
  [YF]     Yahoo Finance via yfinance (7 Oct 2026): share prices, shares outstanding, consensus (5 analysts), price
           targets; peer data 23 Sep 2026
  [MACRO]  Norges Bank MPR 3/26 (Sep 2026), Riksbank MPR Sep 2026, Konjunkturinstitutet Sep 2026, Norwegian 10-year
           government bond yield 7 Oct 2026, PwC/NFF Risikopremien 2025 (market risk premium, size premium, long-term growth)
Rounding: the reports round every line to NOK 1m, so a few balance sheet lines carry a +/-1 difference to make the
balance sheet balance and the cash flow tie. EST marks a case team estimate; everything else is reported.
No broker research or paid databases are used, so the file can be published.
"""

YEARS = list(range(2019, 2026))

# ---- segments: A = Norway, B = Sweden, C = Finland + Denmark -----------------------------------------------------
# Revenue per country from the segment notes (note 2) of the Q4 reports. "Group functions and other"
# revenue (NOK 1-2m a year) is added to Norway so that the segments sum to reported group revenue.
SEG_REV = {
    "A": [1832, 1446, 1366, 1941, 2155, 2266, 2472],
    "B": [1308, 1354, 1256, 1377, 1597, 1708, 1898],
    "C": [847, 734, 625, 764, 982, 1090, 1139],          # Finland 343/326/292/361/466/501/516 + Denmark 504/408/333/403/516/589/623
}
# Members ('000) at year end per country [Q4 reports 2019-2025; Q4-20/Q4-21 for 2020].
SEG_VOL = {
    "A": [299, 280, 302, 325, 326, 332, 345],
    "B": [230, 216, 229, 244, 249, 248, 256],
    "C": [159, 132, 137, 152, 156, 153, 154],           # Finland 62/60/64/70/71/71/71 + Denmark 97/72/73/82/85/82/83
}
# Clubs at year end per country [Q4 reports]; group totals 248/253/262/275/276/272/273.
SEG_LOC = {
    "A": [103, 109, 112, 122, 119, 117, 120],
    "B": [79, 84, 88, 92, 95, 95, 93],
    "C": [66, 60, 62, 61, 62, 60, 60],                  # Finland 28/30/32/32/33/31/32 + Denmark 38/30/30/29/29/29/28
}
LOCATIONS = [sum(SEG_LOC[k][i] for k in "ABC") for i in range(7)]

HIST = dict(
    # ---- income statement (costs negative) ----
    revA=SEG_REV["A"], revB=SEG_REV["B"], revC=SEG_REV["C"],
    cogs=[-115, -122, -106, -162, -137, -143, -146],                # income statements; 2022 as restated in the Q4 2023 report
    pers=[-1463, -1352, -1399, -1572, -1677, -1861, -2055],         # personnel expenses; 2022 restated (15m moved to COGS)
    oth=[-925, -925, -924, -1208, -1136, -1119, -1199],             # other operating expenses (2021: -925 reported, -924 so EBITDA = 818)
    da=[-211, -239, -237, -260, -238, -212, -219],                  # D&A of owned assets = total D&A less right-of-use depreciation
    rou_dep=[-761, -806, -805, -860, -940, -985, -998],             # depreciation of right-of-use assets (note 8, "depreciation charge")
    special=[0, -78, 0, 0, 0, 0, 0],                                # 2020 impairment of assets held for sale [Q4-20]
    netfin=[-78, -71, -111, -92, -69, -64, -25],                    # net financial items less interest on lease liabilities
    lease_int=[-187, -196, -187, -189, -224, -246, -251],           # interest on lease liabilities (cash flow statements)
    tax=[-60, -70, 70, 15, -89, -108, -141],
    minority_pl=[0] * 7,
    lease_pay=[-937, -999, -987, -1041, -1171, -1208, -1243],       # instalments + interest [cash flow statements]
    # ---- balance sheet ----
    gw=[2351, 2458, 2425, 2478, 2535, 2570, 2587],                  # goodwill (note 6)
    intang=[113, 120, 144, 110, 93, 91, 80],                        # intangible assets less goodwill (software, trademarks, customer lists)
    ppe=[739, 758, 691, 723, 705, 792, 916],
    rou=[3912, 4568, 4077, 4161, 4570, 4657, 4769],
    other_nca=[239, 204, 247, 335, 278, 223, 215],                  # deferred tax assets, derivatives, other receivables
    inv=[41, 48, 57, 57, 55, 54, 61],
    rec=[136, 120, 117, 126, 136, 159, 161],
    oca=[292, 359, 297, 340, 329, 367, 338],                        # other receivables, prepayments, contract assets, derivatives
    cash=[165, 456, 281, 345, 282, 371, 512],
    equity=[1223, 885, 483, 860, 1020, 1345, 1454],
    minority_bs=[0] * 7,
    debt_nc=[1293, 1938, 2090, 1970, 1721, 1440, 1480],
    debt_c=[8, 11, 12, 19, 17, 12, 9],
    lease_nc=[3521, 4167, 3632, 3666, 4009, 4090, 4189],
    lease_c=[767, 795, 820, 869, 929, 959, 987],
    deftax=[77, 126, 76, 71, 78, 56, 57],                           # deferred tax liability, non-current derivatives and other liabilities
    pay=[122, 119, 138, 116, 130, 178, 100],
    ocl=[977, 1050, 1085, 1104, 1079, 1204, 1363],                  # contract liabilities (prepaid memberships), public fees, tax, other
    # ---- cash flow (condensed) ----
    cfo=[1278, 1035, 811, 962, 1635, 1903, 2054],                   # reported CFO less interest paid on borrowings (+ interest received)
    capex=[-263, -229, -231, -255, -166, -285, -306],               # purchases less proceeds
    acq=[-58, -102, -9, -49, 0, 0, 0],                              # acquisitions net of cash (2019 fitness dk / FitnessXpress / Viscus; 2020 incl. sale of subsidiary -42; 2022 bolt-ons)
    div_paid=[-1032, 0, 0, 0, 0, 0, -127],                          # 2019 = pre-IPO distribution; 2025 = NOK 0.63 for FY2024
    fin_other=[820, 586, 241, 447, -361, -321, -237],               # debt, share issues (IPO 2019, rights issue 2022), buybacks, FX
    # ---- KPIs and per-share data ----
    volA=SEG_VOL["A"], volB=SEG_VOL["B"], volC=SEG_VOL["C"],
    locA=SEG_LOC["A"], locB=SEG_LOC["B"], locC=SEG_LOC["C"],
    locations=LOCATIONS,
    ftes=[None] * 7,                                                # FTEs not disclosed in the interim reports (close to 10 000 employees, mostly part-time)
    shares=[170.0, 170.8, 171.3, 202.7, 204.1, 204.5, 199.0],       # m, issued less treasury shares (note 4; issued = share capital / NOK 2.125 par)
    dps=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.30],                        # for the fiscal year: 2025 = 0.63 (H1, paid 4 Sep 2025) + 0.67 (H2, paid Mar 2026) [Q2-26 presentation]
    price=[22.67, 23.10, 21.10, 8.84, 15.16, 26.50, 40.60],          # year-end close, Oslo Børs [YF]
)


def simulate():
    """Return the historical data dict (the name is kept for interface compatibility with example_data)."""
    out = {k: list(v) for k, v in HIST.items()}
    n = len(YEARS)
    for i in range(n):
        rev = out["revA"][i] + out["revB"][i] + out["revC"][i]
        ta = sum(out[k][i] for k in ["gw", "intang", "ppe", "rou", "other_nca", "inv", "rec", "oca", "cash"])
        tel = sum(out[k][i] for k in ["equity", "minority_bs", "debt_nc", "debt_c", "lease_nc", "lease_c", "deftax", "pay", "ocl"])
        assert abs(ta - tel) < 0.5, (YEARS[i], ta, tel)
        if i:
            d_cash = out["cash"][i] - out["cash"][i - 1]
            cf = sum(out[k][i] for k in ["cfo", "capex", "acq", "lease_pay", "div_paid", "fin_other"])
            assert abs(cf - d_cash) < 0.5, (YEARS[i], cf, d_cash)
        out.setdefault("rev", []).append(rev)
    return out


# ---- latest quarter / market data (Inputs sheet) ----------------------------------------------------------------
MARKET = dict(
    company="SATS ASA", ticker="SATS", exchange="Oslo Børs", sector="Fitness clubs",
    currency="NOK", unit="NOKm", team="[Case team name]",
    model_date=(2026, 10, 7), val_date=(2026, 10, 6), price_date=(2026, 10, 6), bs_date=(2026, 6, 30),
    share_price=39.75,                # close 6 Oct 2026 [YF]; 42.30 on 30 Sep 2026
    shares=191.1,                     # m, issued 197.2m less 6.1m treasury shares after the Q3 2026 buybacks [YF sharesOutstanding 7 Oct 2026]
    dilutive=1.1,                     # matching shares to be delivered 2027-29 under the share investment programmes [Q2-26]
    high52=47.45, low52=34.95,        # [YF]
    consensus_tp=51.4,                # mean of 5 analysts [YF 7 Oct 2026], range 45-60
    debt_q=1403.0, cash_q=326.0, leases_q=4968.0,    # 30 Jun 2026 [Q2-26]: borrowings 1 394 + 9; lease liabilities 3 998 + 970.
    # Not rolled forward to the valuation date: the H1 2026 dividend (NOK 0.72 x 192m = ~NOK 138m, paid Aug 2026) and the
    # Q3 buybacks (~NOK 50m) are offset by the seasonally strong Q3 free cash flow (~NOK 200m in Q3 2025) – net ~NOK 0/share.
    minority_q=0.0, associates_q=0.0, pension_q=0.0, other_adj=0.0,
    seg_a="Norway", seg_b="Sweden", seg_c="Finland & Denmark", vol_unit="Members ('000)",
    peer_lease=0,                     # peer multiples on a pre-IFRS 16 / lease-adjusted basis (engine comps)
    peer_year=2,                      # 2027E column = peers' NTM consensus multiples; 2026E column = LTM
    fictional=False,
    data_note="Company data: SATS ASA interim reports Q4 2019-Q2 2026 and the 2025 Capital Markets Day; market data and consensus: "
              "Yahoo Finance (7 Oct 2026). Sources line by line in sats_data.py.",
    beta_note="Adjusted beta = 0.67 x raw + 0.33 x 1.0. Raw betas: Yahoo Finance, 5y monthly (Sep 2026).",
    cons_note="Source: Yahoo Finance, 23 Sep 2026 (peer set from the equity-research-engine). 2026E columns = last twelve months; 2027E = "
              "next-twelve-months consensus; EV/EBIT 2027E derived (NTM EBITDA less LTM D&A). Pre-IFRS 16 multiples at 23 Sep 2026 prices.",
)

# ---- base case forecast drivers, 2026E-2033E ---------------------------------------------------------------------
BASE = dict(
    # segment mode (revenue build 1) – kept for the switch, not used in the base case
    volA=[0.020, 0.018, 0.016, 0.014, 0.012, 0.010, 0.010, 0.010],
    priceA=[0.055, 0.035, 0.030, 0.028, 0.025, 0.025, 0.025, 0.025],   # ARPM Norway +6% in H1 2026, +6% in 2025 [Q2-26]
    volB=[0.020, 0.018, 0.016, 0.014, 0.012, 0.010, 0.010, 0.010],
    priceB=[0.020, 0.030, 0.030, 0.025, 0.025, 0.025, 0.025, 0.025],   # 2026 held back by the weak SEK (ARPM +5% currency adjusted, -1% reported in Q2);
                                                                       # Swedish KPIF ~1.5-2% and Nordic Wellness/Fitness24Seven capacity leave less room than in Norway
    volC=[0.010, 0.012, 0.012, 0.010, 0.010, 0.008, 0.008, 0.008],
    priceC=[-0.010, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025],  # Denmark: VAT on group training/PT from 1 Jan 2026 (ARPM -4% in Q2)
    # location mode (revenue build 2): like-for-like growth in members per mature club and net new clubs
    lflA=[0.010, 0.008, 0.006, 0.005, 0.004, 0.003, 0.003, 0.003],     # Norway members per club +1.3% in 2025, +1% y/y in Q2 2026
    lflB=[0.015, 0.012, 0.010, 0.008, 0.006, 0.005, 0.004, 0.003],     # Sweden: members +2% y/y on three fewer clubs
    lflC=[0.000, 0.008, 0.008, 0.006, 0.005, 0.004, 0.003, 0.003],     # Denmark members -4% y/y in Q2 2026 offsets Finland +2%
    netA=[-1, 5, 5, 4, 4, 3, 3, 3],                                   # 2026: 3 openings, 3 closures (270 clubs at year end); committed pipeline 13 clubs
    netB=[-1, 1, 2, 2, 2, 2, 1, 1],                                    # through 2028 (5 in 2027, all Norway; 3 NO + 1 DK + 1 SE in 2028) [Q2-26 presentation p5/p13];
    netC=[-1, 1, 1, 2, 2, 1, 1, 1],                                    # company targets 8-12 a year from 2027 – we model 7-8 (lower end less slippage), 5 from 2031
    cogs=[0.0265] * 8,              # 2.65% of revenue in 2025 (retail and PT cost of sales)
    pers_var=[0.112] * 8,           # variable part = (1 - fixed share 70%) x 37.3% (2025A ratio): PT, sales and group-training hours
    oth_var=[0.087] * 8,            # variable part = (1 - fixed share 60%) x 21.8%: card fees, marketing, consumables
    cpi=[0.015, 0.0325, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030],       # fixed-cost inflation. 2026: ~4% local cost growth less the FX translation of SEK/DKK/EUR costs (total costs
                                                                       # +0% reported, +4% currency adjusted in Q2 2026). 2027: 3.25% = Norwegian wages 4.0% / Swedish 3.4% (Norges Bank
                                                                       # MPR 3/26, KI Sep 2026) on ~60% of the fixed base and CPI-indexed rent (NO 2.6%, SE ~2%) on the rest; 3.0% thereafter
    fix_real=[0.010] * 8,           # segment mode only
    lease=[0.226] * 8,              # segment mode only: lease payments 22.6% of revenue in 2025
    da=[0.040] * 8,                 # D&A owned assets 4.0% of revenue (2025: 219 / 5 509)
    mcapex=[0.050] * 8,             # maintenance and refurbishment ~1.25x D&A; total capex 5.6% of revenue in 2024-25 incl. openings
    s2c=[2.0] * 8,                  # segment mode only
    capex_loc=[9.0, 9.3, 9.6, 9.8, 10.1, 10.3, 10.6, 10.8],            # NOKm per new club, case team estimate; 2019: total capex 325 less maintenance 229 = 96 for 9 openings [Q4-19]
    nwc=[-0.160] * 8,               # prepaid memberships keep NWC at about -16% of revenue (2025: -16.4%)
    tax=[0.22] * 8,                 # Norwegian rate; effective 23% in 2025 (unrecognised losses in Finland/Denmark)
    payout=[0.50, 0.50, 0.55, 0.55, 0.60, 0.60, 0.60, 0.60],           # semi-annual dividends of NOK 0.72 (H1 2026) ~ 50% of 2026E net profit
    rate_debt=[0.050, 0.048, 0.045, 0.045, 0.045, 0.045, 0.045, 0.045],  # multi-currency facility: NIBOR ~4.6% + ~175bp on the NOK part, SEK/EUR tranches at ~3-4%;
                                                                       # net financial items ex leases were only NOK 25m in 2025 and NOK 8m in Q2 2026 [Q2-26]
    rate_cash=[0.030] * 8,
    lease_int=[0.20] * 8,           # 251 / 1 243 in 2025
    min_share=[0.0] * 8,
)

SCENARIO_ADJ = [  # key, label, bear, base, bull, comment
    # Bear = one story: low-cost chains (Nordic Wellness 450+ clubs, Fitness24Seven, EVO) cap price increases at about 2% while
    # Nordic wages keep growing ~3.5-4% – operating leverage runs in reverse and the EBIT adj. margin falls to ~9.5% by 2033
    # (DCF ~NOK 28, -30%). Bull = the CMD 2025 ambition delivered: ~10 openings a year, ARPM growth of 3-4% and Sweden's
    # margin closing in on Norway's (margin ~19%, DCF ~NOK 74). Probability-weighted value = base case.
    ("vol", "Volume / like-for-like growth, all segments (pp p.a.)", -0.0025, 0.0, 0.0025,
     "Churn rises as low-cost chains add capacity in the big cities / stronger member intake and utilisation"),
    ("price", "Price/mix growth, all segments (pp p.a.)", -0.0075, 0.0, 0.005,
     "ARPM growth falls to ~2% (Swedish price competition, Danish VAT) / premium mix and group training lift ARPM"),
    ("open", "Net new locations per segment per year (count, location mode)", -1, 0, 1,
     "Roll-out stays at the committed pipeline / reaches the upper half of the 8-12 target"),
    ("cogs", "COGS in % of revenue (pp)", 0.0, 0.0, 0.0, "Retail and PT cost of sales"),
    ("pers", "Personnel expenses, variable part (pp of revenue)", 0.002, 0.0, -0.002, "Wage inflation above ARPM growth vs. productivity"),
    ("oth", "Other opex, variable part (pp of revenue)", 0.001, 0.0, -0.001, "Marketing to defend the member base vs. scale"),
    ("capex", "Maintenance capex in % of revenue (pp)", 0.000, 0.0, 0.000, "Unchanged – the clubs are kept up in every scenario"),
    ("tg", "Terminal growth (pp)", 0.0, 0.0, 0.0025, "Long-term growth (Bear keeps 2.0% – the damage is in the margin)"),
    ("exit", "Exit multiple, EV/EBITDAaL (x)", -1.0, 0.0, 1.0, "Multiple de-/re-rating"),
    ("prob", "Scenario probability (for weighted value)", 0.25, 0.50, 0.25, "Must sum to 100%"),
]

TERMINAL = dict(tg=0.020, ronic=0.25, tax=0.22, exit=9.0)
# RONIC 25% (case team estimate): a new club costs NOK 7-8m [CMD-25] (we use NOK 9m) and pays back in about three years,
# i.e. ~30% a year before tax; the group ROIC on goodwill-laden invested capital is ~19% (2025). 25% assumes competition
# erodes the marginal return in perpetuity. Terminal growth 2.0% = the PwC/NFF 2025 survey median. Exit 9.0x EV/EBITDAaL
# vs. SATS at ~9.2x LTM Q2 2026 (EV ~8.7bn / EBITDA before IFRS 16 946m) at NOK 39.75.
# NOTE check 21 on the Checks sheet (return on new capital in the explicit period vs. the terminal RONIC) flags a WARNING for
# SATS: most of the growth comes from price increases and utilisation of existing clubs, which need no capital, and prepaid
# memberships make NWC a source of funds – be ready to explain this rather than tuning it away.

WACC_INPUTS = dict(rf=0.0471, erp=0.050, size=0.010, specific=0.0, spread=0.0175, target_dv=0.15, blume=1)
# rf = Norwegian 10-year government bond 7 Oct 2026 (4.71%; 4.62% on 30 Sep). ERP 5.0% = PwC/NFF Risikopremien 2025 median.
# Size/liquidity premium 1.0% for a NOK ~7.6bn market cap with ~NOK 20m daily turnover – above the survey median (0%) and
# about its average for market caps above NOK 5bn. Spread 175bp over NIBOR on the bank facility. Target D/(D+E) 15% =
# the 1.5x NIBD/EBITDAaL leverage target (~NOK 1.5bn) over EV at the current market cap.

# ---- cost structure and capital allocation (Drivers, section E) ----
COST_CAPITAL = dict(pers_fixsh=0.70, oth_fixsh=0.60, central=0.30, lev_t=1.25, bb_on=1, bb_g=0.06)
# Club staff, rent-related services and IT are fixed per club; total overhead costs NOK 646m in 2025 = 30% of the fixed base.
# Leverage: the company keeps NIBD/EBITDA before IFRS 16 'in the lower end of the 1.5x-2.0x target range' and returns >50% of
# net profit through semi-annual dividends and buybacks [Q2-26 presentation p6]; 1.1x at 30 Jun 2026 after NOK 318m of
# buybacks in H1 2026. We model 1.25x – midway between today's 1.1x and the 1.5x lower end: buybacks of ~NOK 400m in 2026
# (NOK 318m done in H1 plus the NOK 100m programme running in Q3) and NOK 350-400m a year thereafter. Going straight to
# 1.5x would need ~NOK 650m of buybacks in 2026, twice the actual pace; the DCF value per share is the same either way.

# ---- revenue build (Inputs) and location engine (Drivers, section F) ----
ENGINE = dict(rev_mode=2, ramp=(0.35, 0.75, 0.95), util_tol=0.15)   # new clubs reach ~3-year payback / mature volume in year three

# ---- consensus (Consensus sheet; reported IFRS 16 basis) ----
CONSENSUS = dict(  # Yahoo Finance has revenue and EPS consensus only; EBITDA, EBIT and DPS show as n.a.
    source="Yahoo Finance consensus (revenue and EPS)",
    date=(2026, 10, 7), n=5, buy=3, hold=2, sell=0,      # Yahoo: 1 strong buy, 2 buy, 2 hold
    rev=[5711, 6044, None], ebitda=[None, None, None], ebit=[None, None, None], eps=[2.90, 3.51, None], dps=[None, None, None],
)
VARIANT = [  # topic, our view, consensus view, why we differ (evidence), what proves it – and when, metric key, year (1-3)
    ("Operating leverage",
     "EBIT adj. margin rises from 11.7% (2025) to 15.1% by 2033 on a largely fixed cost base",
     "Close to us for 2026 and ~6% above us on 2027 EPS; the share price implies only ~12.3% in 2033 (11.7% today)",
     "~70% of personnel and ~60% of other opex are fixed per club. Q2 2026: ARPM +6% vs. costs +4% currency adjusted, EBITDA before IFRS 16 +18%, Norway margin 37% (+2pp)",
     "Q3 (27 Oct) and Q4 2026 (Feb 2027) reports: EBITDA before IFRS 16 above NOK 1.0bn for 2026", "eps", 2),
    ("Roll-out",
     "7-8 net openings a year in 2027-30 (the lower end of the 8-12 target), each reaching mature volume in its third year",
     "Roll-out stays at the committed 13 clubs and closures offset openings (net -3 clubs in 2026)",
     "13 clubs committed through 2028 and 'several processes in final stages' for the 8-12 run-rate (Q2 2026); a new club costs NOK 7-8m and pays back in ~3 years (CMD 2025)",
     "Q4 2026 report (Feb 2027): clubs opened in H2 2026 and the 2027 opening pipeline", "rev", 2),
    ("Capital returns",
     "Buybacks lift NIBD/EBITDAaL towards the 1.5x lower end of the target range (we model 1.25x) on top of a 50-60% dividend payout – the share count falls ~4% a year",
     "The market values SATS on its ~3.5% dividend yield and treats buybacks as one-offs (our reading)",
     "H1 2026 payout ratio 152% (NOK 318m buybacks + NOK 0.72 dividend), 4.0m shares cancelled and 2.5m approved for cancellation; leverage 1.1x vs. the 1.5-2.0x target (Q2 2026)",
     "Q4 2026 report (Feb 2027): size of the next buyback programme; AGM May 2027: renewed mandate", "eps", 1),
]
SCENARIO_STORIES = {  # story, what has to happen, signpost to watch (keep them short – they are printed on two slides)
    "bear": ("Low-cost chains cap price increases at ~1.5-2% while wages grow ~4%: operating leverage runs in reverse",
             "ARPM growth below +2% currency adjusted for two quarters and a falling member base",
             "ARPM and member growth per country; Swedish price points; the Danish member trend"),
    "base": ("Steady member growth, 7-8 net openings a year and ~3% price increases on a largely fixed cost base",
             "2026 EBITDAaL passes NOK 1.0bn and the 2027 openings are delivered on schedule",
             "Country EBITDA margins (Norway >32%); clubs opened vs. the committed pipeline"),
    "bull": ("The CMD ambition delivered: ~10 openings a year, ARPM growth of 3-4% and Sweden's margin closing in on Norway's",
             "Sweden's country EBITDA margin above 25% for a full year and a higher opening target",
             "Sweden's country EBITDA margin; the opening target"),
}
KILL = [  # KPI label, Model row key, kill if ('below'/'above'), threshold, watch buffer, format ('pct'/'mult')
    ("Price/mix growth, group", "g_pxc", "below", 0.015, 0.010, "pct"),
    ("Like-for-like volume growth, group", "g_lflc", "below", -0.010, 0.010, "pct"),
    ("EBIT adj. margin (pre-IFRS 16)", "ebit_adj_m", "below", 0.100, 0.010, "pct"),
    ("Cash conversion (FCFF / EBITDAaL)", "cconv", "below", 0.350, 0.100, "pct"),
    ("NIBD / EBITDAaL", "lev", "above", 2.00, 0.25, "mult"),
]

# Peers [YF via the equity-research-engine comps, 23 Sep 2026]. Market cap and EV in NOKm. Multiples on a lease-adjusted
# (pre-IFRS 16) basis: FY0 = LTM, FY1 = NTM consensus, FY2 not available (blank – the Comps statistics ignore blanks).
# EBIT margin = LTM; growth = NTM revenue growth; raw beta = 5y monthly; D/E at market values.
# EV/EBIT FY1 is DERIVED (Yahoo has no EBIT consensus): EV / (NTM EBITDA consensus less LTM D&A), i.e.
# 1 / (1/EV-EBITDA NTM - (1/EV-EBITDA LTM - 1/EV-EBIT LTM)).
PEERS = [  # name, country, mcap, ev, evs(3), evebitda(3), evebit(3), pe(3), ebit margin, growth, raw beta, D/E, tax
    ("Basic-Fit", "NL", 22723, 34222, (2.22, 1.74, None), (10.5, 8.2, None), (45.9, 20.7, None), (22.2, 14.3, None), 0.048, 0.115, 0.889, 0.58, 0.258),
    ("Planet Fitness", "US", 33255, 54488, (4.10, 3.86, None), (9.7, 9.1, None), (13.2, 12.2, None), (14.2, 12.7, None), 0.310, 0.070, 1.012, 0.70, 0.21),
    ("Life Time Group", "US", 84692, 96723, (3.22, 2.80, None), (13.8, 12.0, None), (23.9, 19.0, None), (22.9, 19.7, None), 0.134, 0.120, 1.481, 0.17, 0.21),
    ("The Gym Group", "UK", 4157, 4905, (1.59, 1.34, None), (8.4, 7.1, None), (30.3, 18.2, None), (36.4, 32.8, None), 0.052, 0.108, 0.835, 0.19, 0.25),
    ("Europris", "NO", 13780, 15454, (1.03, 0.97, None), (11.5, 10.8, None), (13.1, 12.2, None), (15.4, 12.3, None), 0.079, 0.054, 0.489, 0.13, 0.22),
    ("Kid", "NO", 4951, 6032, (1.48, 1.37, None), (11.8, 10.9, None), (15.7, 14.1, None), (14.9, 12.3, None), 0.094, 0.061, 0.561, 0.15, 0.22),
    ("Clas Ohlson", "SE", 26048, 23936, (1.92, 1.72, None), (14.0, 12.5, None), (15.5, 13.7, None), (19.0, 17.7, None), 0.124, 0.060, 0.934, 0.00, 0.206),
    ("Rusta", "SE", 11288, 10725, (0.87, 0.77, None), (10.9, 9.6, None), (13.7, 11.8, None), (17.3, 14.9, None), 0.063, 0.092, 0.902, 0.00, 0.206),
]

if __name__ == "__main__":
    d = simulate()
    for i, y in enumerate(YEARS):
        rev = d["rev"][i]
        ebitda = rev + d["cogs"][i] + d["pers"][i] + d["oth"][i]
        ebit = ebitda + d["da"][i] + d["rou_dep"][i] + d["special"][i]
        pbt = ebit + d["netfin"][i] + d["lease_int"][i]
        np_ = pbt + d["tax"][i]
        print(y, "rev", rev, "EBITDA", ebitda, "EBITDAaL", ebitda + d["lease_pay"][i], "EBIT", ebit, "PBT", pbt, "NP", np_,
              "EPS", round(np_ / d["shares"][i], 2))
