"""Elkem ASA – real case data for the Equity Research DCF toolkit (first edition, 3 November 2026).

Same interface as example_data.py / sats_data.py. All figures in NOKm unless stated. The company changed in 2026: the
Silicones division was transferred to Bluestar on 30 April 2026 against the redemption of Bluestar's 52.9 % stake, Elkem
Iceland and the retained silicones assets are held for sale, and the group reports three divisions – Silicon, Foundry
Alloys and Carbon – from the third quarter of 2026. Only 2025 exists on this perimeter (restated in the Q3 2026 report), so
the workbook history is one year (HIST_START = 6); the division history 2021-2025 from the Capital Markets Update is kept
in DIVISION_HISTORY for the report. Valuation date 2 November 2026 (last close before the model date 3 November 2026),
balance sheet 30 September 2026.

Sources (all public; every document is listed with URL and date in examples/ELKEM/data/KILDER.md)
  [Q3-26]  Elkem ASA third quarter results 2026, 29 Oct 2026: restated FY2025 and quarterly figures on the new perimeter,
           note 2 (segments), note 6 (debt), note 8 (shares), note 9 (held for sale), APM appendix (derivative adjustments)
  [Q2-26]  Second quarter and half year report 2026, 10 Jul 2026: Q2 and H1 2026/2025 on the same perimeter (Iceland excluded)
  [CMU-26] Capital Markets Update, 29 Oct 2026: financial targets, division history 2021-2025, plants and capacities, power
  [AR-25]  Integrated annual report 2025, 19 Mar 2026: key figures 2019-2025 as reported (old structure), CO2 compensation, power contracts
  [NW]     Oslo Børs NewsWeb, issuer ELK, 1 Nov 2025-3 Nov 2026 (87 messages): transaction, equity raise, calendar, insiders
  [YF]     Yahoo Finance via yfinance, 3 Nov 2026: peer market data, betas, FX; Elkem EPS/revenue estimates (3-6 analysts), target prices
  [OQ]     oslo-quant store (Yahoo Finance adjusted closes): ELK closes to 2 Nov 2026, 52-week range, year-end prices
  [NB]     Norges Bank: 10-year government bond yield 2 Nov 2026 (4.399 %); EUR/NOK and USD/NOK
  [NVE]    NVE Kraftsituasjonen (quarterly and weekly) and Rapport 17/2026: NO3/NO4 power prices
  [MACRO]  Norges Bank MPR 3/26 (Sep 2026) for CPI/wages; PwC/NFF Risikopremien 2025 (market risk premium, long-term growth)
EST marks a case team estimate; everything else is reported. No broker research or paid databases are used.
"""

YEARS = list(range(2019, 2026))
HIST_START = 6                       # index of the first year with data on the current perimeter (2025); 2019-2024 blank in the workbook
_B = [None] * HIST_START

# ---- segments: A = Silicon, B = Foundry Alloys, C = Carbon --------------------------------------------------------
# Revenue = operating income from EXTERNAL customers per division (note 2, Q3-26 p16) so that the segments sum to group
# revenue. "Other" (group functions: power sales, services; 403 external in 2025) is added to Silicon, whose plants the power
# function serves. Division total operating income incl. intersegment sales (Silicon 9 452, Foundry Alloys 4 181, Carbon
# 3 272) is used in the report where the company's own margins are quoted.
SEG_REV = {"A": _B + [8945 + 403], "B": _B + [2642], "C": _B + [2976]}
# Sales volume, thousand tonnes [Q3-26 p7-8]: Silicon excl. microsilica and quartz.
SEG_VOL = {"A": _B + [207], "B": _B + [131], "C": _B + [262]}
# "Locations" = production sites on the current perimeter [CMU-26 slides 24, 35, 45]: Silicon – Thamshavn, Salten, Rana,
# Bremanger (silicon line), Tana and Erimsa quarries; Foundry Alloys – Bremanger, Bjølvefossen, Chicoutimi, Limpio,
# Shizuishan, Nagpur, Dronfield; Carbon – Fiskaa, Zvolen, Shizuishan, eMalahleni, Vitória (two plants). Unchanged 2024-25
# (2024 is filled so that the Python verification can form an average).
SEG_LOC = {"A": [None] * 5 + [6, 6], "B": [None] * 5 + [7, 7], "C": [None] * 5 + [6, 6]}
LOCATIONS = _B + [19]

HIST = dict(
    # ---- income statement 2025, continuing operations as restated in Q3-26 (p9, p16, p26); costs negative ----
    revA=SEG_REV["A"], revB=SEG_REV["B"], revC=SEG_REV["C"],
    cogs=_B + [-6469],                   # raw materials and energy
    pers=_B + [-2604],                   # employee benefit expenses
    oth=_B + [-3327],                    # other operating expenses 3 592 less the realised hedging effects (derivative adjustments 265)
                                         # that the company's EBITDA includes: EBITDA (APM) 2 566 = 14 966 - 6 469 - 2 604 - 3 327
    da=_B + [-798],                      # amortisation and depreciation 873 less right-of-use depreciation 75 (note 3)
    rou_dep=_B + [-75],
    special=_B + [-11],                  # impairment 7 and other items (262) net of the derivative adjustments (266): EBIT = operating profit 1 682
    netfin=_B + [-748],                  # finance income 58, FX (285), finance expenses (542) = (769), less lease interest (21)
    lease_int=_B + [-21],
    tax=_B + [-239],
    minority_pl=_B + [-84],              # non-controlling interests' share (continuing + discontinued as reported; discontinued is small)
    lease_pay=_B + [-172],               # payment of lease liabilities 151 + lease interest 21 (cash flow statement, note 5)
    # ---- balance sheet 31 Dec 2025 (Q3-26 p11); assets held for sale (22 878) in other non-current assets, their liabilities (7 447) in "deferred tax and other" ----
    gw=_B + [305], intang=_B + [164], ppe=_B + [8568], rou=_B + [402],
    other_nca=_B + [26020],              # deferred tax assets 942 + equity-accounted 210 + derivatives 981 + other 1 011 + held for sale 22 878 (−2 rounding)
    inv=_B + [5959], rec=_B + [1852],
    oca=_B + [1517],                     # current derivatives 285 + other current assets 1 231 + restricted deposits 1
    cash=_B + [2694],                    # continuing operations (a further 1 112 sat in the held-for-sale group)
    equity=_B + [23922], minority_bs=_B + [104],
    debt_nc=_B + [9306], debt_c=_B + [2251],   # interest-bearing liabilities 9 648 / 2 322 less lease liabilities 342 / 71
    lease_nc=_B + [342], lease_c=_B + [71],
    deftax=_B + [8439],                  # deferred tax 129 + employee benefit obligations 238 + derivatives 350 + provisions 275 + liabilities held for sale 7 447
    pay=_B + [1818],
    ocl=_B + [1228],                     # income tax 43 + current employee benefit obligations 482 + derivatives 115 + provisions and other 588
    # ---- cash flow 2025 as reported (consolidated, incl. discontinued; Q3-26 p12) – one year, so no tie to the change in cash is tested ----
    cfo=_B + [1176], capex=_B + [-2247], acq=_B + [0], div_paid=_B + [-275], fin_other=_B + [-475],
    # ---- KPIs and per-share data ----
    volA=SEG_VOL["A"], volB=SEG_VOL["B"], volC=SEG_VOL["C"],
    locA=SEG_LOC["A"], locB=SEG_LOC["B"], locC=SEG_LOC["C"], locations=LOCATIONS,
    ftes=_B + [None],                    # about 2 300 in the three divisions (CMU-26: 1 050 + 800 + 425) plus group functions; group FTE total not published
    shares=_B + [634.2],                 # m, year-end 2025: 639 441 378 issued less 5 221 900 treasury shares (note 8)
    dps=_B + [0.0],                      # no dividend for 2025 (AGM 30 Apr 2026)
    price=_B + [30.48],                  # year-end 2025 close, Yahoo adjusted [OQ]
)


def simulate():
    """Return the historical data dict; assert the balance sheet balances in every year with data."""
    out = {k: list(v) for k, v in HIST.items()}
    for i in range(len(YEARS)):
        if out["revA"][i] is None:
            out.setdefault("rev", []).append(None)
            continue
        rev = out["revA"][i] + out["revB"][i] + out["revC"][i]
        ta = sum(out[k][i] for k in ["gw", "intang", "ppe", "rou", "other_nca", "inv", "rec", "oca", "cash"])
        tel = sum(out[k][i] for k in ["equity", "minority_bs", "debt_nc", "debt_c", "lease_nc", "lease_c", "deftax", "pay", "ocl"])
        assert abs(ta - tel) < 0.5, (YEARS[i], ta, tel)
        out.setdefault("rev", []).append(rev)
    return out


# ---- latest quarter / market data (Inputs sheet) ----------------------------------------------------------------
MARKET = dict(
    company="Elkem ASA", ticker="ELK", exchange="Oslo Børs", sector="Industrial materials – silicon, ferrosilicon, foundry alloys, carbon",
    currency="NOK", unit="NOKm", team="[Case team name]",
    model_date=(2026, 11, 3), val_date=(2026, 11, 2), price_date=(2026, 11, 2), bs_date=(2026, 9, 30),
    share_price=30.92,                # close 2 Nov 2026, the last close before the model date [OQ]
    shares=362.5,                     # m, 367 769 508 issued less 5 221 900 treasury shares at 30 Sep 2026 [Q3-26 note 8]
    dilutive=0.0,                     # the share option programme was terminated for cash on 11 Aug 2026; no options outstanding [Q3-26 p21]
    high52=36.84, low52=25.00,        # closing prices, 12 months to 2 Nov 2026 [OQ] (9 Sep 2026 / 13 Feb 2026)
    consensus_tp=38.4,                # mean target price, Yahoo Finance 3 Nov 2026 (low 31, high 46) [YF]; the company publishes no consensus
    debt_q=11584.0, cash_q=5459.0, leases_q=333.0,   # 30 Sep 2026 [Q3-26 note 6]: interest-bearing liabilities 11 917 less lease liabilities 333;
                                                     # the company's own NIBD of 6 459 includes the leases
    minority_q=130.0,                 # non-controlling interests, book value
    associates_q=3666.0,              # equity-accounted investments 243 + net assets held for sale 3 423 (4 213 - 790): Elkem Iceland (book ~1.3bn,
                                      # fair value less cost to sell estimated equal to book, range 0-3.0bn), Roussillon (book 1.7bn), Silicones India (0.1bn),
                                      # Yongdeng (0) [Q3-26 note 9; Q3-26 presentation slide 10]. Taken at book value; a what-if run halves it.
    pension_q=227.0,                  # non-current employee benefit obligations [Q3-26 p11]
    other_adj=1200.0,                 # 1.3 million surplus EU ETS allowances carried at zero; the company's estimate of fair value [Q3-26 note 1]
    equity_issue_fc1=1756.0,          # NOK 1 500m placement (8 May 2026) + NOK 300m subsequent offering (8 Jun 2026), net of costs [Q3-26 p21]: a 2026 financing
                                      # flow the annual model would otherwise miss (the workbook rolls net debt from the 31 Dec 2025 balance sheet)
    seg_a="Silicon", seg_b="Foundry Alloys", seg_c="Carbon", vol_unit="Sales volume (kt)",
    loc_label="production sites", rpu_label="revenue per tonne (NOK '000)",
    peer_lease=1,                     # Yahoo Finance enterprise values include lease liabilities (IFRS 16)
    peer_year=1,                      # peers' last-twelve-months multiples on our first forecast year; NTM EV multiples are not public
    fictional=False,
    data_note="Company data: Elkem ASA Q3 2026 report and presentation, Capital Markets Update 2026, Q2 2026 report and the 2025 annual "
              "report; prices: oslo-quant store (Yahoo adjusted closes); peers and EPS/revenue estimates: Yahoo Finance (3 Nov 2026); "
              "risk-free rate: Norges Bank. Sources line by line in elkem_data.py and examples/ELKEM/data/KILDER.md.",
    yahoo="ELK.OL", index_yahoo="OSEBX.OL", free_float="n.a. (not published)",
    beta_note="Adjusted beta = 0.67 x raw + 0.33 x 1.0. Raw betas: Yahoo Finance, 5y monthly (3 Nov 2026).",
    cons_note="Source: Yahoo Finance, 3 Nov 2026. 2026E columns = last twelve months (EV/Sales, EV/EBITDA, P/E trailing); 2027E = forward P/E only "
              "(next-twelve-months EV multiples are not public without a paid terminal). IFRS 16 basis. Yara and OM Holdings' Yahoo multiples mix "
              "reporting and listing currencies and are left blank.",
)

# ---- base case forecast drivers, 2026E-2033E ---------------------------------------------------------------------
# Segment mode: revenue = volume x price per division. Prices are realised prices in NOK incl. mix and currency.
# Silicon: 2026 volume +13.5 % (nine months +13 %: inventories were sold down after the Rana/Salten stops; 5 959 -> 4 433 of stock) and
#   price/mix -14.5 % (nine-month external income -4 % on +13 % volume; EU silicon and FeSi prices at historic lows, stronger NOK). 2027: no
#   inventory to sell and one Rana furnace out for 3-4 months (-2 % volume); price +10 % – EU reference prices rising since Q3 2026,
#   registration of Chinese imports from 27 Oct 2026 and an anti-dumping review due by Sep-Dec 2027 [Q3-26 p4; presentation slide 16].
#   2028 +5 %, then 2 % a year (inflation; no return to the 2021-22 cycle peak in the base case).
# Foundry Alloys: volume +3 % in 2026 (nine months +4 %), +2 % a year (India 7-8 %, mature markets 0-2 % [CMU-26 slide 37]); price -2 %
#   in 2026 (currency), then 2-2.5 % (value-based pricing, 22 % margin held).
# Carbon: 2026 price -9 % (nine-month income -12 % on flat volume), volume flat; 2027-28 recovery with furnace activity (+4 %/+3 % volume,
#   +4 %/+3 % price) towards the 2021-2024 margin band of 23-31 %, not back to it.
BASE = dict(
    volA=[0.135, -0.02, 0.02, 0.01, 0.01, 0.005, 0.005, 0.005],
    priceA=[-0.145, 0.10, 0.05, 0.02, 0.02, 0.02, 0.02, 0.02],
    volB=[0.03, 0.02, 0.02, 0.02, 0.015, 0.015, 0.01, 0.01],
    priceB=[-0.02, 0.025, 0.025, 0.02, 0.02, 0.02, 0.02, 0.02],
    volC=[0.0, 0.04, 0.03, 0.02, 0.02, 0.01, 0.01, 0.01],
    priceC=[-0.09, 0.04, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02],
    # location mode (not used; mirrors the segment drivers so that the stress test's mode switch stays sensible)
    lflA=[0.135, -0.02, 0.02, 0.01, 0.01, 0.005, 0.005, 0.005],
    lflB=[0.03, 0.02, 0.02, 0.02, 0.015, 0.015, 0.01, 0.01],
    lflC=[0.0, 0.04, 0.03, 0.02, 0.02, 0.01, 0.01, 0.01],
    netA=[0] * 8, netB=[0] * 8, netC=[0] * 8,
    cogs=None,                      # filled below from the unit-cost build (raw materials and energy per tonne x volume)
    pers_var=[0.0174] * 8,          # 10 % of personnel expenses scale with revenue (2025: 2 604 / 14 966 = 17.4 % x 10 %)
    oth_var=[0.0889] * 8,           # 40 % of other opex scale with revenue (freight, sales commissions, consumables): 22.2 % x 40 %
    cpi=[0.030, 0.030, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025],          # wage and price inflation on the fixed base (Norges Bank MPR 3/26: wages 4.4 %/4.0 %, CPI 3.3 %/2.6 %; ~45 % of the base is outside Norway)
    fix_real=[-0.070, -0.030, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],              # the cost programme: NOK 600m a year from Q3 2026, ~400 FTEs (11 Mar 2026; Q2-26 p4) – about 7 % of the
                                                                           # fixed personnel-and-other base in 2026 (half-year effect plus the Rana/Salten stops) and a further 3 % in 2027
    lease=[0.012] * 8,              # lease payments 172 / 14 966 in 2025
    da=[0.060, 0.057, 0.054, 0.052, 0.051, 0.050, 0.050, 0.050],           # D&A owned assets: nine months 2026 645 (684 less ROU 39) on lower revenue; falls with revenue growth
    mcapex=[0.052, 0.072, 0.060, 0.058, 0.057, 0.056, 0.055, 0.055],       # 2026 capped at NOK 1.0bn (nine months 510) ~750; 2027 ~850 reinvestments + Rana furnace 260
                                                                           # (Q3-26 p4); from 2028 ~100 % of D&A plus ~0.5 % strategic (CMU-26 slide 56)
    s2c=[50.0] * 8,                 # growth capex is NOT modelled through sales-to-capital: price-led revenue needs no capital, and all capex sits in mcapex
    capex_loc=[0.0] * 8,
    nwc=[0.36, 0.34, 0.33, 0.32, 0.32, 0.32, 0.32, 0.32],                  # 42 % of revenue at YE2025 (incl. derivatives), 36 % at 30 Sep 2026 after the NOK 1bn working-capital
                                                                           # programme; company's own definition targets a return towards the historic 23 % [Feb 2026 deck]
    tax=[0.25] * 8,                 # 24 % effective in Q3 2026; Norway 22 % plus China/Brazil/India/Canada; low payable tax in Norway on losses carried forward
    payout=[0.0, 0.35, 0.40, 0.40, 0.45, 0.45, 0.45, 0.45],               # dividend target 30-50 % of EPS (CMU-26); nothing for 2026 while leverage is above the <2.5x target
    rate_debt=[0.050, 0.048, 0.045, 0.045, 0.045, 0.045, 0.045, 0.045],   # EUR term loan EURIBOR + 1.25-2.30 %; NOK bonds 3mN + 1.20-1.75 % and 5.75 % fixed [Q3-26 note 6; financing page]
    rate_cash=[0.030] * 8,
    lease_int=[0.12] * 8,           # 21 / 172 in 2025
    min_share=[0.08] * 8,           # non-controlling interests 52 of 645 in nine months 2026
)


def _unit_cost_build():
    """Raw materials and energy per tonne grow with input inflation, not with the sales price – the source of operating leverage
    in a commodity producer. Returns the COGS share of revenue per year implied by the volume and price drivers above."""
    rev = {s: SEG_REV[s][-1] for s in "ABC"}
    vol = {s: SEG_VOL[s][-1] for s in "ABC"}
    # 2026: nine-month raw materials and energy 5 361 on income 10 956 = 48.9 % (low prices, full-cost inventories); FY2026E 47.5 % EST
    first_share = 0.475
    # unit cost inflation per year: coal/coke, quartz, electrodes and power. Power: ~85 % of the Norwegian volume is hedged short/medium
    # term and the "30-øringen" contract runs to 31 Dec 2030, so the step comes in 2031 (EST +4 %); otherwise 2-2.5 % a year.
    ucost = [0.010, 0.020, 0.025, 0.025, 0.025, 0.040, 0.025, 0.025]
    out, unit = [], None
    for i in range(8):
        for s in "ABC":
            vol[s] = vol[s] * (1 + BASE["vol" + s][i])
            rev[s] = rev[s] * (1 + BASE["vol" + s][i]) * (1 + BASE["price" + s][i])
        R, V = sum(rev.values()), sum(vol.values())
        if unit is None:
            unit = first_share * R / V
        else:
            unit = unit * (1 + ucost[i])
        out.append(round(unit * V / R, 4))
    return out


BASE["cogs"] = _unit_cost_build()

SCENARIO_ADJ = [  # key, label, bear, base, bull, comment
    # Bear = one story: Chinese overcapacity keeps EU silicon and ferrosilicon prices at the 2026 level, the anti-dumping review brings no
    # higher duty and power costs rise – Silicon stays at a mid-single-digit margin and the group never reaches 15 %. Bull = the review doubles
    # the duty and the ferroalloy safeguard bites: EU prices normalise towards the 2023-24 level, Silicon returns to a mid-teens margin and the
    # group passes the >20 % target. Probabilities 30/45/25: a cyclical with a fat downside tail (the base case is not the probability-weighted value).
    ("vol", "Volume growth, all segments (pp p.a.)", -0.010, 0.0, 0.010, "Lost share to imports and furnace stops / full utilisation"),
    ("price", "Price/mix growth, all segments (pp p.a.)", -0.030, 0.0, 0.020, "EU prices stay at the 2026 trough / trade defence lifts EU prices"),
    ("open", "Net new locations per segment per year (count, location mode)", 0, 0, 0, "Not used – the model runs in segment mode"),
    ("cogs", "Raw materials and energy in % of revenue (pp)", 0.010, 0.0, -0.005, "Power and coke costs vs. biocarbon and energy recovery"),
    ("pers", "Personnel expenses, variable part (pp of revenue)", 0.0, 0.0, 0.0, "Unchanged – the programme is delivered in every scenario"),
    ("oth", "Other opex, variable part (pp of revenue)", 0.0, 0.0, 0.0, ""),
    ("capex", "Maintenance capex in % of revenue (pp)", 0.0, 0.0, 0.0, "Reinvestment ~100 % of D&A in every scenario"),
    ("tg", "Terminal growth (pp)", 0.0, 0.0, 0.0, ""),
    ("exit", "Exit multiple, EV/EBITDAaL (x)", -1.0, 0.0, 1.0, "Multiple de-/re-rating"),
    ("prob", "Scenario probability (for weighted value)", 0.30, 0.45, 0.25, "Must sum to 100%"),
]

TERMINAL = dict(tg=0.020, ronic=0.10, tax=0.25, exit=6.5)
# RONIC 10 % (case team estimate): a commodity producer with leading cost positions earns a little above its cost of capital through the
# cycle (Elkem's own ROCE 2019-2025 as reported: 7 / 5 / 26 / 40 / 4 / 5 / 2 %; new-perimeter division ROCE 2025: Silicon 6 %, Foundry Alloys
# 18 %, Carbon 43 % [CMU-26]). Terminal growth 2.0 % = the PwC/NFF 2025 survey median. Exit 6.5x EV/EBITDAaL: between the peer median on
# trough earnings and Elkem's own 5.4x LTM (Yahoo, 3 Nov 2026).

WACC_INPUTS = dict(rf=0.04399, erp=0.050, size=0.0075, specific=0.0, spread=0.0225, target_dv=0.30, blume=1)
# rf = Norwegian 10-year government bond 2 Nov 2026 (Norges Bank). ERP 5.0 % = PwC/NFF Risikopremien 2025 median. Size/liquidity premium
# 0.75 % for a NOK ~11bn market cap after the shareholder base was rebuilt in May 2026. Spread 225bp: BBB- with a negative outlook (Scope,
# 19 Mar 2026); bank margin 1.25-2.30 % over EURIBOR, NOK bonds 1.20-1.75 % over NIBOR. Target D/(D+E) 30 % ~ the <2.5x leverage target on
# a mid-cycle EBITDA against the current market cap (35 % today at 3.3x).

COST_CAPITAL = dict(pers_fixsh=0.90, oth_fixsh=0.60, central=0.30, lev_t=2.0, bb_on=0, bb_g=0.05)
# Smelter staffing is fixed per furnace; 60 % of other opex (maintenance, insurance, IT, admin) is fixed. No buybacks are modelled: the
# authorisation exists (AGM 30 Apr 2026) but the company's priority is leverage below 2.5x and an investment-grade profile; excess cash
# reduces net debt at the cash rate.

ENGINE = dict(rev_mode=1, ramp=(0.35, 0.75, 0.95), util_tol=0.15)

# ---- consensus (Consensus sheet) ----
CONSENSUS = dict(
    # Elkem publishes no consensus (analyst-information page lists nine brokers). Yahoo Finance, 3 Nov 2026: revenue (5 and 6 analysts),
    # EPS (3 analysts; the 2026 figure may include discontinued operations – the basis is not stated). EBITDA, EBIT and DPS: not available.
    source="Yahoo Finance (3 Nov 2026): revenue 5-6 analysts, EPS 3 analysts; EBITDA, EBIT and DPS not available – Elkem publishes no consensus",
    date=(2026, 11, 3), n=6, buy=4, hold=2, sell=0,     # recommendation split: 1 strong buy, 3 buy, 2 hold
    rev=[14898, 16516, None], ebitda=[None, None, None], ebit=[None, None, None], eps=[0.94, 3.63, None], dps=[None, None, None],
)
CONSENSUS_Q = None  # no quarterly consensus is public
VARIANT = [  # topic, our view, consensus view, why we differ (evidence), what proves it – and when, metric key, year (1-3)
    ("Silicon price recovery",
     "2027 revenue +7 % (15.5bn): Silicon prices +10 % from the 2026 trough, volume -2 % (no inventory left to sell, one Rana furnace out)",
     "Revenue 2027E 16.5bn, +11 % (Yahoo, 6 analysts) – a faster normalisation",
     "EU reference prices rose only 'modestly' in Q3 2026; the anti-dumping review concludes between Sep and Dec 2027 and the ferroalloy safeguard has had "
     "'less positive market price impact than expected' [Q3-26 p4, p23]; nine-month volume +13 % came from stock (inventories 5 959 -> 4 433)",
     "Q4 2026 report (11 Feb 2027): Silicon EBITDA and the quarter-end inventory level; Q1 2027 report: realised prices after the import registration", "rev", 2),
    ("Earnings on the new cost base",
     "2027 EPS below the market: our EBITDA 2.6bn (17 %) carries a 25 % tax rate, 8 % minorities and NOK ~0.3bn of interest",
     "EPS 2027E NOK 3.63 (3 analysts) – requires EBITDA of about 3.0bn or a lower tax charge",
     "The NOK 600m programme is in the 2026 run-rate already (nine-month opex down 6 %); what is left is price. FX gains of 664 flatter the 2026 result and are not repeatable",
     "Q4 2026 report (11 Feb 2027): underlying EBIT and the tax rate; the 2026 annual report (19 Mar 2027): cost base by nature", "eps", 2),
    ("Assets the P&L does not show",
     "NOK 4.9bn of non-operating value: held-for-sale net assets 3.4bn (Iceland, Roussillon) at book and 1.3 million EU ETS allowances worth ~1.2bn",
     "Not in any public estimate; the share trades at 0.9x book (light case)",
     "Iceland's fair value is estimated equal to book with a 0-3.0bn range; Roussillon has a take-or-pay contract with Bluestar to 2031; the allowances are to be "
     "sold 'over time' and will be booked as revenue [Q3-26 note 1, note 9; presentation slide 10]",
     "Any sale announcement for Iceland or Roussillon; allowance sales in the Q4 2026 and Q1 2027 reports", "eps", 1),
]
SCENARIO_STORIES = {  # story, what has to happen, signpost to watch
    "bear": ("Chinese overcapacity keeps EU silicon and ferrosilicon prices at the 2026 trough, the anti-dumping review adds nothing and power costs rise",
             "EU silicon reference prices flat through 2027 and Silicon EBITDA margin below 5 % for two quarters",
             "Silicon division EBITDA margin; GFEX silicon futures; EU import registration volumes"),
    "base": ("Prices normalise slowly from the trough, the cost programme holds and Foundry Alloys and Carbon keep 20-30 % margins",
             "Silicon EBITDA margin back above 10 % during 2027 and group leverage below 3.0x by end-2027",
             "Division margins each quarter; NIBD/EBITDA against the <2.5x target"),
    "bull": ("The anti-dumping review raises the duty on Chinese silicon and the safeguard bites: EU prices return towards 2023-24 levels",
             "Commission proposal for a higher duty (within 12-15 months of 1 Sep 2026) and Silicon EBITDA margin above 15 %",
             "Commission decisions; EU silicon and ferrosilicon reference prices; Elkem Silicon realised prices"),
}
KILL = [  # KPI label, Model row key, kill if ('below'/'above'), threshold, watch buffer, format ('pct'/'mult')
    ("EBIT adj. margin (pre-IFRS 16)", "ebit_adj_m", "below", 0.030, 0.020, "pct"),
    ("Group volume growth", "g_volc", "below", -0.050, 0.020, "pct"),
    ("Cash conversion (FCFF / EBITDAaL)", "cconv", "below", 0.000, 0.100, "pct"),
    ("NIBD / EBITDAaL", "lev", "above", 4.00, 0.50, "mult"),
    ("EBITDA margin (reported)", "ebitda_m", "below", 0.080, 0.030, "pct"),
]
# Division-level kill criteria that the workbook rows cannot carry (measured in the quarterly report). They are exported with the report's
# estimates (kill_list) so the research-book row and the dashboard's reader are checked against the same list (oslo-quant D40).
KILL_TEXT = [
    "Elkem Silicon EBITDA margin below 5 % for two consecutive quarters (Q3 2026: 6 %)",
    "Elkem Foundry Alloys EBITDA margin below 18 % in any quarter (21-22 % for seven quarters)",
    "EU interim review on Chinese silicon ends without a higher duty (conclusion due 1 Sep-1 Dec 2027)",
]

# Peers [YF, 3 Nov 2026]. Market cap and EV in NOKm (Yahoo FX of the day: EUR 10.34, USD 9.24, SEK 0.944, JPY 0.0585, INR 0.0976, CNY 1.386,
# AUD 6.44). Multiples: FY0 = trailing twelve months (Yahoo), FY1 = forward P/E only; NTM EV multiples and EV/EBIT are not public (blank – the
# Comps statistics ignore blanks). EBIT margin and revenue growth = trailing; raw beta = 5y monthly; D/E at book debt over market equity (Yahoo).
# OM Holdings reports in USD and lists in AUD, so Yahoo's EV multiples are inconsistent and left blank; Yara (fertiliser) is not a peer.
PEERS = [  # name, country, mcap, ev, evs(3), evebitda(3), evebit(3), pe(3), ebit margin, growth, raw beta, D/E, tax
    ("Ferroglobe", "UK/US", 6632, 8141, (0.64, None, None), (16.0, None, None), (None, None, None), (None, 9.3, None), 0.150, -0.021, 1.200, 0.35, 0.25),
    ("Hoshine Silicon", "CN", 47018, 83732, (3.02, None, None), (11.9, None, None), (None, None, None), (None, 33.4, None), 0.161, -0.161, 0.360, 0.91, 0.25),
    ("Eramet", "FR", 11069, 41054, (1.32, None, None), (20.8, None, None), (None, None, None), (None, 22.7, None), 0.014, 0.157, 0.951, 2.16, 0.258),
    ("OM Holdings", "AU/SG", 1086, 2042, (None, None, None), (None, None, None), (None, None, None), (None, None, None), 0.001, -0.142, 0.220, 0.41, 0.30),
    ("Wacker Chemie", "DE", 41890, 47616, (0.82, None, None), (6.5, None, None), (None, None, None), (None, 27.6, None), 0.070, 0.094, 0.748, 0.53, 0.30),
    ("Tokai Carbon", "JP", 22079, 31761, (1.60, None, None), (8.6, None, None), (None, None, None), (21.1, 21.3, None), 0.095, 0.184, 0.632, 0.61, 0.306),
    ("HEG", "IN", 4680, 4836, (1.88, None, None), (8.6, None, None), (None, None, None), (13.3, 8.1, None), 0.148, 0.104, 0.688, 0.17, 0.252),
    ("Graphite India", "IN", 14233, 11920, (4.03, None, None), (40.4, None, None), (None, None, None), (71.2, 14.4, None), 0.144, 0.266, 0.894, 0.06, 0.252),
    ("Norsk Hydro", "NO", 129197, 152877, (0.74, None, None), (2.8, None, None), (None, None, None), (10.0, 8.7, None), 0.241, 0.031, 0.785, 0.31, 0.22),
    ("Borregaard", "NO", 15285, 17101, (2.18, None, None), (9.9, None, None), (None, None, None), (56.6, 15.1, None), 0.215, 0.053, 0.606, 0.36, 0.22),
    ("Boliden", "SE", 134549, 155032, (1.47, None, None), (5.7, None, None), (None, None, None), (10.3, 16.5, None), 0.178, 0.386, 1.175, 0.28, 0.206),
    ("SSAB", "SE", 90853, 83065, (0.88, None, None), (8.1, None, None), (None, None, None), (17.6, 16.3, None), 0.083, 0.116, 1.199, 0.15, 0.206),
]
PEER_GROUPS = {"Silicon, ferroalloys and manganese": ["Ferroglobe", "Hoshine Silicon", "Eramet", "OM Holdings", "Wacker Chemie"],
               "Carbon and graphite materials": ["Tokai Carbon", "HEG", "Graphite India"],
               "Nordic materials": ["Norsk Hydro", "Borregaard", "Boliden", "SSAB"]}

# ---- audit inputs (model_builder/audit.py; docs/research/03 failure modes) ----
META = dict(
    sector="materials", cyclical=True, commodity="silicon", reporting_currency="NOK",
    commodity_deck=dict(model=10230, forward=8530, date="3 Nov 2026",
                        note="Model: the 2027E Silicon price driver (+10 %) applied to the East China 553# spot of 9 300 CNY/t (Mysteel, 26 Oct 2026). "
                             "Forward: GFEX Si2707 settlement 8 530 CNY/t (metal.com, 3 Nov 2026). The gap is deliberate: the model price is an EU price behind a "
                             "16.8 % duty under review with import registration; the futures curve is Chinese domestic."),
    binary_event="EU anti-dumping interim review on Chinese silicon (initiated 1 Sep 2026; conclusion within 12-15 months)",
    last_share_issue="2026-06-08",     # NOK 300m subsequent offering registered; NOK 1 500m placement 8 May 2026 – both before the balance sheet date
    guidance=dict(ebit_margin=None),   # the CMU targets are an EBITDA margin >20 % over the cycle, leverage <2.5x, reinvestment ~100 % of D&A, payout 30-50 % – no EBIT or revenue guidance
    conflicts=None,                    # author's holdings and other conflicts – to be filled by the author (VPFF Standard 3)
    disclosures=dict(
        author="Case author (private student case study)",
        price_datetime="2 Nov 2026, close (Oslo Børs, via the oslo-quant store) – the last close before the model date 3 Nov 2026",
        rating_definitions="BUY: 12-month expected total return above the cost of equity + 5pp; SELL: below Ke − 5pp; HOLD in between",
        valuation_summary="70% DCF (FCFF after lease payments, value-driver terminal value) + 30% peer multiples, rolled forward 12 months",
        update_frequency="After each quarterly report",
        history_12m="First edition (3 Nov 2026) – no earlier calls",
        status="Private student case study; not investment research or advice",
    ),
    reasons=dict(
        A2="The bear case holds EU prices at the 2026 trough for eight years; its value is far below base by construction, and the revenue spread bull-bear is "
           "wide because price drives revenue in a commodity producer (SCENARIO_ADJ comment).",
        A3="The margin rises from a 2026 trough (13 % EBITDA, Silicon at 2 %) because unit costs are fixed per tonne while prices recover; the base case stays "
           "below the through-cycle average of 20 % and the company's >20 % target (CMU-26 slide 57; _unit_cost_build).",
        A4="The peer set mixes trough-earnings multiples (Ferroglobe 16x) with carbon-materials companies; the case's own reverse DCF is the anchor.",
        A5="RONIC 10 % against a WACC near 9 %: a cost-leading commodity producer earns a little above its cost of capital through the cycle; terminal RONIC = WACC "
           "is shown as a what-if (TERMINAL comment).",
        A8="One year of history on the current perimeter (2025, a trough year with a 10.7 % EBIT adj. margin). The through-cycle test is done on the Capital "
           "Markets Update series instead: group EBITDA margin 24/39/20/21/17 % in 2021-2025 (mean 24 %); the terminal EBITDA margin of the base case is below that mean.",
        A9="The GFEX contract is Chinese domestic 553# silicon; Elkem sells into the EU behind a 16.8 % anti-dumping duty that is under review with import "
           "registration since 27 Oct 2026, and into the US behind tariffs. The model assumes EU prices decouple upwards from the Chinese curve (deep dive 2).",
        B17="Working capital falls from 42 % of revenue (31 Dec 2025, incl. derivatives and full-cost inventories) to 36 % at 30 Sep 2026 already; the model takes it to 32 %, "
            "still above the company's own historic level of 23 % on its definition (Feb 2026 deck). The release is the company's NOK 1bn programme, 841 of which was done by June 2026.",
        B27="Leverage 3.3x at 30 Sep 2026 against covenants of 4.75x (to Mar 2027) and 4.25x, NOK 5.5bn of cash and NOK 4.5bn undrawn against NOK 0.9bn of 2027 maturities; the bear "
            "scenario (prices at the trough for eight years) is the distress case and is priced at NOK 3.6 per share – the refinancing of June 2026 runs to 2031 (deep dive 4).",
        B21="0.75 % size/liquidity premium for a NOK ~11bn market cap with a rebuilt shareholder base; between the PwC/NFF median (0 %) and the SATS case's 1.0 % (WACC_INPUTS comment).",
    ),
)

if __name__ == "__main__":
    d = simulate()
    i = HIST_START
    rev = d["rev"][i]
    ebitda = rev + d["cogs"][i] + d["pers"][i] + d["oth"][i]
    ebit = ebitda + d["da"][i] + d["rou_dep"][i] + d["special"][i]
    pbt = ebit + d["netfin"][i] + d["lease_int"][i]
    np_ = pbt + d["tax"][i]
    print(YEARS[i], "rev", rev, "EBITDA", ebitda, "EBITDAaL", ebitda + d["lease_pay"][i], "EBIT", ebit, "PBT", pbt, "NP", np_,
          "NP to owners", np_ + d["minority_pl"][i], "EPS", round((np_ + d["minority_pl"][i]) / d["shares"][i], 2))
    print("cogs % path", BASE["cogs"])
    # the segment build, for the record
    rv = {s: SEG_REV[s][-1] for s in "ABC"}
    vol = {s: SEG_VOL[s][-1] for s in "ABC"}
    pers_fix, oth_fix = 2604 * COST_CAPITAL["pers_fixsh"], 3327 * COST_CAPITAL["oth_fixsh"]
    for j, y in enumerate(range(2026, 2034)):
        for s in "ABC":
            vol[s] *= 1 + BASE["vol" + s][j]
            rv[s] *= (1 + BASE["vol" + s][j]) * (1 + BASE["price" + s][j])
        R = sum(rv.values())
        pers_fix *= (1 + BASE["cpi"][j]) * (1 + BASE["fix_real"][j])
        oth_fix *= (1 + BASE["cpi"][j]) * (1 + BASE["fix_real"][j])
        costs = R * BASE["cogs"][j] + pers_fix + R * BASE["pers_var"][j] + oth_fix + R * BASE["oth_var"][j]
        print(y, "rev", round(R), {s: round(v) for s, v in rv.items()}, "vol", {s: round(v) for s, v in vol.items()}, "EBITDA", round(R - costs),
              f"{(R - costs) / R:.1%}", "EBITDAaL", round(R - costs - R * BASE['lease'][j]))


# ---- research report blocks (deck_builder/build_report.py) --------------------------------------------------------
# Quarterly series on the current perimeter (continuing operations excl. Silicones, Iceland, Roussillon, Yongdeng, India) from the Q3 2026
# and Q2 2026 reports. Q1 and Q4 are differences of reported half-year, nine-month and full-year figures (KILDER.md 3a). ebitdaal = EBITDA less
# lease payments (quarterly split of the reported nine-month/full-year payments: EST); ebit_adj = EBITDAaL less D&A of owned assets (quarterly
# ROU depreciation of 13: EST). np = profit from continuing operations before minorities. EPS per quarter is not shown: it mixes continuing and
# discontinued operations across three share counts (634m, 301m, 363m). Division lines on the new basis exist for Q3 2025, Q4 2025 (derived)
# and Q3 2026 only; Carbon (unchanged division) for every quarter; Q1-Q2 show the old Silicon Products segment (Silicon + Foundry Alloys
# before internal eliminations, ex Iceland) in a separate line.
def _q(rev, ebitda, ebitdaal, ebit, ebit_adj, np_, seg, vol_si=None, vol_fa=None, vol_c=None):
    return dict(rev=rev, ebitda=ebitda, ebitdaal=ebitdaal, ebit=ebit, ebit_adj=ebit_adj, np=np_, eps=None,
                vol_si=vol_si, vol_fa=vol_fa, vol_c=vol_c,
                seg={n: dict(rev=r, cebitda=c, volume=v) for n, (r, c, v) in seg.items()})


_SP = "Silicon + Foundry Alloys (old Silicon Products segment, ex Iceland)"
QUARTERS = dict(
    source="Elkem ASA Q3 2026 report (29 Oct 2026) and Q2 2026 report (10 Jul 2026), restated continuing operations; Q1/Q4 derived", date="29 Oct 2026", unit="NOKm",
    seg_ebitda_label="division EBITDA", seg_volume_label="sales volume (kt)",
    kpis=[("Sales volume – Silicon (kt)", "vol_si", "n"), ("Sales volume – Foundry Alloys (kt)", "vol_fa", "n"), ("Sales volume – Carbon (kt)", "vol_c", "n")],
    rows={
        "Q1 2025": _q(3829, 724, 683, 512, 486, 207, {"Carbon": (861, 261, 65), _SP: (2988, 510, 79)}, vol_c=65),
        "Q2 2025": _q(3864, 645, 604, 435, 409, 20, {"Carbon": (854, 242, 68), _SP: (3066, 443, 88)}, vol_c=68),
        "Q3 2025": _q(3675, 646, 616, 435, 421, 318, {"Silicon": (2351, 224, 56), "Foundry Alloys": (1009, 220, 34), "Carbon": (822, 231, 69)}, vol_si=56, vol_fa=34, vol_c=69),
        "Q4 2025": _q(3598, 552, 513, 303, 279, 129, {"Silicon": (2287, 162, 50), "Foundry Alloys": (1034, 202, 32), "Carbon": (735, 174, 60)}, vol_si=50, vol_fa=32, vol_c=60),
        "Q1 2026": _q(3661, 316, 286, 101, 85, 263, {"Carbon": (722, 164, 65), _SP: (2918, 187, 95)}, vol_c=65),
        "Q2 2026": _q(3708, 523, 492, 300, 277, -69, {"Carbon": (741, 172, 65), _SP: (2946, 319, 96)}, vol_c=65),
        "Q3 2026": _q(3587, 554, 532, 312, 303, 451, {"Silicon": (2142, 127, 57), "Foundry Alloys": (1056, 235, 35), "Carbon": (782, 183, 69)}, vol_si=57, vol_fa=35, vol_c=69),
    },
)
# Division history on the current perimeter, NOK bn and EBITDA margin [CMU-26 slides 29, 39, 49, 57; values read from the chart labels]
DIVISION_HISTORY = dict(
    source="Elkem Capital Markets Update 2026, slides 29, 39, 49 and 57", date="29 Oct 2026",
    years=["2021", "2022", "2023", "2024", "2025", "LTM Q3 2026"],
    Silicon=dict(rev=[10.3, 17.6, 11.8, 10.7, 9.5, 9.1], margin=[0.23, 0.38, 0.13, 0.16, 0.09, 0.04], roce=[0.52, 1.18, 0.17, 0.19, 0.06, -0.02]),
    FoundryAlloys=dict(rev=[3.5, 6.0, 5.6, 4.4, 4.2, 4.2], margin=[0.18, 0.38, 0.26, 0.22, 0.21, 0.22], roce=[0.19, 0.65, 0.37, 0.23, 0.18, 0.20]),
    Carbon=dict(rev=[2.2, 3.8, 4.2, 3.6, 3.3, 3.0], margin=[0.23, 0.31, 0.31, 0.31, 0.28, 0.23], roce=[0.37, 0.82, 0.70, 0.58, 0.43, 0.29]),
    group_margin=[0.24, 0.39, 0.20, 0.21, 0.17, 0.13],
)
EVENTS = [  # date, event, source
    ("2027-02-11", "Q4 2026 report", "Elkem financial calendar (NewsWeb 679951, 17 Aug 2026)"),
    ("2027-03-19", "Annual report 2026", "Elkem financial calendar (17 Aug 2026)"),
    ("2027-03-31", "Rana furnace renewal – installation during Q1 2027, three to four months", "Q3 2026 report p4 (30 Sep 2026 announcement)"),
    ("2027-04-22", "Annual general meeting and Q1 2027 report", "Elkem financial calendar (17 Aug 2026)"),
    ("2027-07-13", "Half-year report 2027", "Elkem financial calendar (17 Aug 2026)"),
    ("2027-09-01", "EU anti-dumping interim review on Chinese silicon – earliest conclusion (12 months from 1 Sep 2026; at most 15)", "Q3 2026 report p4; Commission notice 1 Sep 2026"),
    ("2027-10-21", "Q3 2027 report", "Elkem financial calendar (17 Aug 2026)"),
]
HISTORY = []  # first edition – no earlier calls
