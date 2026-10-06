"""Fictional example company used to populate the DCF template.

All numbers are invented. The history is simulated with consistent accounting
(balance sheet balances, cash flow ties to the change in cash) so the template's
integrity checks pass out of the box.
"""

YEARS = list(range(2019, 2026))

SEG_REV = {
    "A": [1950, 1790, 1880, 2150, 2340, 2505, 2690],
    "B": [1240, 1130, 1190, 1400, 1545, 1665, 1785],
    "C": [600, 548, 598, 712, 802, 875, 958],
}
SEG_VOL = {
    "A": [300, 281, 289, 316, 329, 337, 347],
    "B": [228, 212, 219, 247, 259, 267, 274],
    "C": [118, 110, 117, 132, 143, 150, 158],
}
COGS_PCT = [0.365, 0.378, 0.372, 0.381, 0.376, 0.370, 0.366]
PERS_PCT = [0.230, 0.246, 0.238, 0.229, 0.224, 0.221, 0.218]
OTH_PCT = [0.128, 0.135, 0.131, 0.126, 0.123, 0.121, 0.119]
LEASE_PCT = [0.084, 0.093, 0.089, 0.082, 0.080, 0.079, 0.078]
DA_PCT = [0.046, 0.051, 0.049, 0.046, 0.045, 0.045, 0.044]
CAPEX_PCT = [0.052, 0.036, 0.044, 0.056, 0.054, 0.051, 0.050]
NWC_PCT = [-0.060, -0.052, -0.056, -0.061, -0.063, -0.064, -0.065]
SPECIAL = [0.0, -45.0, 0.0, 0.0, -20.0, 0.0, 0.0]
DEBT = [1600, 1750, 1700, 1650, 1550, 1500, 1450]
DEBT_CURRENT = [120, 150, 100, 100, 100, 100, 100]
NETFIN_RATE = [0.040, 0.035, 0.032, 0.042, 0.055, 0.058, 0.056]
CASH_RATE = 0.015
OPEN_CASH = 300.0
TAX_RATE = 0.22
TAX_ADJ = [5.0, 8.0, 0.0, 0.0, 0.0, 0.0, 0.0]
MIN_SHARE = 0.01
DPS = [0.00, 0.00, 2.50, 3.50, 4.20, 4.80, 5.40]
DPS_2018 = 2.40
SHARES = 85.0
PRICE_YE = [78.0, 64.0, 82.0, 88.0, 95.0, 104.0, 112.0]
LOCATIONS = [182, 184, 188, 201, 206, 211, 217]
SEG_LOC = {  # locations per segment at year end (sums to LOCATIONS; 2022 and 2024 include acquired locations)
    "A": [82, 83, 85, 88, 89, 91, 94],
    "B": [68, 69, 70, 73, 75, 76, 77],
    "C": [32, 32, 33, 40, 42, 44, 46],
}
assert all(sum(SEG_LOC[k][i] for k in "ABC") == LOCATIONS[i] for i in range(7))
FTES = [3150, 2980, 3050, 3420, 3560, 3640, 3730]
ACQ = [0, 0, 0, 800, 0, 450, 0]        # cash paid
ACQ_GW = [0, 0, 0, 600, 0, 330, 0]
ACQ_INT = [0, 0, 0, 140, 0, 90, 0]
ACQ_PPE = [0, 0, 0, 60, 0, 30, 0]
LEASE_LIAB_MULT = 4.2
ROU_SHARE = 0.80                        # share of lease payments that is ROU depreciation
INV_PCT, REC_PCT, OCA_PCT, PAY_PCT = 0.040, 0.035, 0.020, 0.070
LEASE_CURRENT_SHARE = 0.20


def r1(x):
    return round(x, 1)


def simulate():
    n = len(YEARS)
    rev2018 = 3650.0
    # opening balance sheet (end of 2018)
    gw, intang, ppe, other_nca = 1800.0, 230.0, 820.0, 55.0
    lease_liab = 1300.0
    rou = 1230.0
    nwc_items = dict(inv=INV_PCT * rev2018, rec=REC_PCT * rev2018, oca=OCA_PCT * rev2018,
                     pay=PAY_PCT * rev2018)
    nwc2018 = -0.058 * rev2018
    ocl = nwc_items["inv"] + nwc_items["rec"] + nwc_items["oca"] - nwc_items["pay"] - nwc2018
    debt, cash, deftax, minority = 1620.0, OPEN_CASH, 180.0, 28.0
    assets = gw + intang + ppe + rou + other_nca + nwc_items["inv"] + nwc_items["rec"] + nwc_items["oca"] + cash
    liab = debt + lease_liab + deftax + nwc_items["pay"] + ocl
    equity = assets - liab - minority     # opening equity is the plug
    prev_nwc = nwc2018
    prev_dps = DPS_2018

    out = {k: [] for k in [
        "revA", "revB", "revC", "rev", "cogs", "pers", "oth", "ebitda", "da", "rou_dep", "special",
        "ebit", "netfin", "lease_int", "pbt", "tax", "np", "minority_pl", "np_sh", "lease_pay",
        "gw", "intang", "ppe", "rou", "other_nca", "inv", "rec", "oca", "cash", "total_assets",
        "equity", "minority_bs", "total_equity", "debt_nc", "debt_c", "lease_nc", "lease_c",
        "deftax", "pay", "ocl", "total_el", "cfo", "capex", "acq", "div_paid", "fin_other",
        "net_change_cash", "volA", "volB", "volC", "locA", "locB", "locC", "locations", "ftes", "shares", "dps", "price",
    ]}
    for i in range(n):
        ra, rb, rc = SEG_REV["A"][i], SEG_REV["B"][i], SEG_REV["C"][i]
        rev = ra + rb + rc
        cogs = -r1(COGS_PCT[i] * rev)
        pers = -r1(PERS_PCT[i] * rev)
        oth = -r1(OTH_PCT[i] * rev)
        ebitda = rev + cogs + pers + oth
        lp = r1(LEASE_PCT[i] * rev)                      # lease payments (positive magnitude)
        rd = r1(ROU_SHARE * lp)
        li = r1(lp - rd)
        da = r1(DA_PCT[i] * rev)
        special = SPECIAL[i]
        ebit = ebitda - da - rd + special
        netfin = r1(-debt * NETFIN_RATE[i] + cash * CASH_RATE)
        pbt = ebit + netfin - li
        tax = -r1(TAX_RATE * pbt + TAX_ADJ[i])
        np_ = pbt + tax
        min_pl = -r1(MIN_SHARE * np_)
        np_sh = np_ + min_pl

        # balance sheet roll-forward
        capex = r1(CAPEX_PCT[i] * rev)
        ppe = ppe + capex - da + ACQ_PPE[i]
        gw += ACQ_GW[i]
        intang += ACQ_INT[i]
        lease_target = LEASE_LIAB_MULT * lp
        new_leases = lease_target - lease_liab - li + lp
        lease_liab = lease_liab + new_leases + li - lp
        rou = rou + new_leases - rd
        nwc = NWC_PCT[i] * rev
        inv, rec, oca, pay = INV_PCT * rev, REC_PCT * rev, OCA_PCT * rev, PAY_PCT * rev
        ocl = inv + rec + oca - pay - nwc
        d_nwc = nwc - prev_nwc
        div_paid = r1(prev_dps * SHARES)
        d_debt = DEBT[i] - debt
        cfo = ebitda + special + netfin + tax - d_nwc
        cfi = -capex - ACQ[i]
        cff = -lp + d_debt - div_paid
        cash = cash + cfo + cfi + cff
        debt = DEBT[i]
        equity = equity + np_sh - div_paid
        minority = minority - min_pl

        total_assets = gw + intang + ppe + rou + other_nca + inv + rec + oca + cash
        total_el = equity + minority + debt + lease_liab + deftax + pay + ocl
        assert abs(total_assets - total_el) < 1e-6, (YEARS[i], total_assets, total_el)

        vals = dict(
            revA=ra, revB=rb, revC=rc, rev=rev, cogs=cogs, pers=pers, oth=oth, ebitda=ebitda,
            da=-da, rou_dep=-rd, special=special, ebit=ebit, netfin=netfin, lease_int=-li, pbt=pbt,
            tax=tax, np=np_, minority_pl=min_pl, np_sh=np_sh, lease_pay=-lp,
            gw=gw, intang=intang, ppe=ppe, rou=rou, other_nca=other_nca, inv=inv, rec=rec, oca=oca,
            cash=cash, total_assets=total_assets, equity=equity, minority_bs=minority,
            total_equity=equity + minority, debt_nc=debt - DEBT_CURRENT[i], debt_c=DEBT_CURRENT[i],
            lease_nc=lease_liab * (1 - LEASE_CURRENT_SHARE), lease_c=lease_liab * LEASE_CURRENT_SHARE,
            deftax=deftax, pay=pay, ocl=ocl, total_el=total_el, cfo=cfo, capex=-capex, acq=-ACQ[i],
            div_paid=-div_paid, fin_other=d_debt, net_change_cash=cfo + cfi + cff,
            volA=SEG_VOL["A"][i], volB=SEG_VOL["B"][i], volC=SEG_VOL["C"][i],
            locA=SEG_LOC["A"][i], locB=SEG_LOC["B"][i], locC=SEG_LOC["C"][i],
            locations=LOCATIONS[i], ftes=FTES[i], shares=SHARES, dps=DPS[i], price=PRICE_YE[i],
        )
        for k, v in vals.items():
            out[k].append(v)
        prev_nwc = nwc
        prev_dps = DPS[i]

    # round balance sheet items to one decimal while keeping the balance exact:
    bs_assets = ["gw", "intang", "ppe", "rou", "other_nca", "inv", "rec", "oca", "cash"]
    bs_liab = ["equity", "minority_bs", "debt_nc", "debt_c", "lease_nc", "lease_c", "deftax", "pay", "ocl"]
    for k in bs_assets + bs_liab + ["cfo"]:
        out[k] = [r1(v) for v in out[k]]
    for i in range(n):
        ta = sum(out[k][i] for k in bs_assets)
        te = sum(out[k][i] for k in bs_liab)
        out["ocl"][i] = r1(out["ocl"][i] + (ta - te))           # absorb rounding in other current liabilities
    # cash flow: make CFO the residual so the statement ties to the rounded cash balances
    prev_cash = OPEN_CASH
    for i in range(n):
        d_cash = out["cash"][i] - prev_cash
        other = out["capex"][i] + out["acq"][i] + out["lease_pay"][i] + out["div_paid"][i] + out["fin_other"][i]
        out["cfo"][i] = r1(d_cash - other)
        prev_cash = out["cash"][i]
    return out


# ---- latest quarter / market data (Inputs sheet) ----
MARKET = dict(
    company="Example Company ASA", ticker="EXMPL", exchange="Oslo Børs", sector="Consumer services",
    currency="NOK", unit="NOKm", team="[Case team name]",
    share_price=122.00, shares=85.0, dilutive=0.6, high52=134.60, low52=101.20, consensus_tp=135.0,
    debt_q=1420.0, cash_q=395.0, leases_q=1805.0, minority_q=70.0, associates_q=40.0, pension_q=20.0,
    other_adj=0.0,
)

# ---- base case forecast drivers, 2026E-2033E ----
BASE = dict(
    volA=[0.026, 0.024, 0.022, 0.020, 0.018, 0.016, 0.014, 0.012],
    priceA=[0.034, 0.030, 0.028, 0.026, 0.025, 0.024, 0.023, 0.022],
    volB=[0.030, 0.028, 0.026, 0.023, 0.020, 0.018, 0.015, 0.013],
    priceB=[0.032, 0.030, 0.028, 0.026, 0.025, 0.024, 0.023, 0.022],
    volC=[0.055, 0.050, 0.045, 0.040, 0.035, 0.030, 0.025, 0.020],
    priceC=[0.030, 0.028, 0.027, 0.026, 0.025, 0.024, 0.023, 0.022],
    # location mode (revenue build 2): like-for-like growth in volume per mature location and net new locations
    lflA=[0.008, 0.007, 0.006, 0.005, 0.004, 0.003, 0.003, 0.003],
    lflB=[0.010, 0.009, 0.008, 0.007, 0.006, 0.005, 0.004, 0.003],
    lflC=[0.015, 0.014, 0.012, 0.010, 0.009, 0.008, 0.006, 0.005],
    netA=[2, 2, 2, 2, 2, 1, 1, 1],
    netB=[2, 2, 2, 2, 1, 1, 1, 1],
    netC=[3, 3, 3, 2, 2, 2, 1, 1],
    cogs=[0.366] * 8,
    pers_var=[0.0872] * 8,          # variable part = (1 - fixed share 60%) x 21.8% (2025A ratio)
    oth_var=[0.0595] * 8,           # variable part = (1 - fixed share 50%) x 11.9%
    cpi=[0.030, 0.027, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025],
    fix_real=[0.015] * 8,           # capacity additions (new locations) grow the fixed cost base in real terms
    lease=[0.078, 0.078, 0.077, 0.077, 0.077, 0.077, 0.077, 0.077],
    da=[0.044, 0.044, 0.044, 0.044, 0.044, 0.044, 0.044, 0.044],
    mcapex=[0.050] * 8,             # maintenance + refurbishment ~1.14x D&A (the historical capex/D&A ratio)
    s2c=[2.0] * 8,                  # segment mode: NOK 1 of growth capex supports NOK 2 of new revenue
    capex_loc=[22.0, 22.6, 23.1, 23.7, 24.3, 24.9, 25.5, 26.1],   # location mode: capex per new location, NOKm (fit-out, equipment, pre-opening)
    nwc=[-0.065] * 8,
    tax=[0.22] * 8,
    payout=[0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.90, 0.90],
    rate_debt=[0.055, 0.052, 0.050, 0.050, 0.050, 0.050, 0.050, 0.050],
    rate_cash=[0.015] * 8,
    lease_int=[0.20] * 8,
    min_share=[0.01] * 8,
)

SCENARIO_ADJ = [  # key, label, bear, base, bull, comment
    ("vol", "Volume / like-for-like growth, all segments (pp p.a.)", -0.015, 0.0, 0.010,
     "Weaker customer intake / churn in Bear"),
    ("price", "Price/mix growth, all segments (pp p.a.)", -0.010, 0.0, 0.005, "Pricing power tested by low-cost competition"),
    ("open", "Net new locations per segment per year (count, location mode)", -1, 0, 1, "Slower / faster roll-out"),
    ("cogs", "COGS in % of revenue (pp)", 0.010, 0.0, -0.005, "Input-cost inflation vs. procurement gains"),
    ("pers", "Personnel expenses, variable part (pp of revenue)", 0.005, 0.0, -0.003, "Wage inflation vs. productivity"),
    ("oth", "Other opex, variable part (pp of revenue)", 0.005, 0.0, -0.002, "Marketing / service cost pressure vs. scale"),
    ("capex", "Maintenance capex in % of revenue (pp)", 0.003, 0.0, 0.000, "Higher maintenance capex in Bear"),
    ("tg", "Terminal growth (pp)", -0.005, 0.0, 0.0025, "Long-term growth"),
    ("exit", "Exit multiple, EV/EBITDAaL (x)", -1.0, 0.0, 1.0, "Multiple de-/re-rating"),
    ("prob", "Scenario probability (for weighted value)", 0.25, 0.50, 0.25, "Must sum to 100%"),
]

TERMINAL = dict(tg=0.020, ronic=0.12, tax=0.22, exit=8.5)

WACC_INPUTS = dict(rf=0.040, erp=0.050, size=0.010, specific=0.0, spread=0.020, target_dv=0.10, blume=1)
# The 10% target D/(D+E) matches the modelled capital structure: buybacks hold NIBD at 0.75x EBITDAaL (Drivers, section E)

# ---- cost structure and capital allocation (Drivers, section E) ----
COST_CAPITAL = dict(pers_fixsh=0.60, oth_fixsh=0.50, central=0.25, lev_t=0.75, bb_on=1, bb_g=0.08)

# ---- revenue build (Inputs) and location engine (Drivers, section F) ----
ENGINE = dict(rev_mode=2, ramp=(0.35, 0.75, 0.95), util_tol=0.15)

# ---- consensus (Consensus sheet; reported IFRS 16 basis; example data – replace with Bloomberg / Infront / Modular Finance) ----
CONSENSUS = dict(
    source="Bloomberg consensus (example data – replace)", date=(2026, 9, 15), n=6, buy=4, hold=2, sell=0,
    rev=[5698, 5994, 6321], ebitda=[1684, 1775, 1881], ebit=[1073, 1131, 1197], eps=[8.40, 9.03, 9.68], dps=[5.52, 6.38, 7.36],
)
VARIANT = [  # topic, our view, consensus view, why we differ (evidence), what proves it – and when, metric key (rev/ebitda/ebit/eps/dps), year (1-3)
    ("Margins", "EBIT margin expands as fixed costs are spread over more locations and revenue per location grows with price",
     "Flat margins: cost inflation eats the price increases",
     "About 60% of personnel and 50% of other opex are fixed; rent grows with inflation and the number of locations, not with revenue",
     "Q4 report (February): 2027 margin guidance. Capital markets day (November): margin target", "ebit", 3),
    ("Roll-out", "Around seven openings a year that reach mature volume in their third year",
     "Four to five openings a year, no step-up in the pipeline",
     "Signed leases for 2026-27 and the integration of the 2024-25 bolt-ons free up management capacity",
     "Capital markets day (November): opening target and pipeline", "rev", 3),
    ("Capital returns", "Cash above 0.75x NIBD/EBITDAaL goes to buybacks – EPS grows faster than net profit",
     "Dividends only; leverage drifts down",
     "Stated leverage target and a stable, cash-generative subscription model",
     "AGM (spring 2027): buyback mandate", "eps", 3),
]
SCENARIO_STORIES = {  # story, what has to happen, signpost to watch
    "bear": ("Low-cost chains take share in the big cities: price increases stall, churn rises and the roll-out slows",
             "Two or more low-cost openings per quarter in our core cities and price/mix below +1.5% for two quarters",
             "Group price/mix growth and churn in the quarterly reports"),
    "base": ("Steady like-for-like growth, around seven openings a year and operating leverage from a largely fixed cost base",
             "Annual price increases of ~3% stick and new locations reach 75% of mature volume in their second year",
             "Revenue per location and the ramp-up of the 2026 openings"),
    "bull": ("Faster roll-out and premium tiers: more openings at similar returns and higher revenue per member",
             "The capital markets day lifts the opening target and premium tiers pass 25% of members",
             "Opening pipeline and premium share at the capital markets day"),
}
KILL = [  # KPI label, Model row key, kill if ('below'/'above'), threshold, watch buffer, format ('pct'/'mult')
    ("Price/mix growth, group", "g_pxc", "below", 0.015, 0.010, "pct"),
    ("Like-for-like volume growth, group", "g_lflc", "below", -0.005, 0.005, "pct"),
    ("EBIT adj. margin", "ebit_adj_m", "below", 0.160, 0.010, "pct"),
    ("Cash conversion (FCFF / EBITDAaL)", "cconv", "below", 0.400, 0.100, "pct"),
    ("NIBD / EBITDAaL", "lev", "above", 1.50, 0.25, "mult"),
]

PEERS = [  # name, country, mcap, ev, evs(3), evebitda(3), evebit(3), pe(3), ebit margin fy2, growth fy2, raw beta, D/E, tax
    ("Peer A ASA", "NO", 18500, 21400, (2.3, 2.1, 2.0), (8.9, 8.2, 7.6), (15.1, 13.6, 12.4), (18.2, 16.4, 14.9), 0.152, 0.071, 1.05, 0.28, 0.22),
    ("Peer B AB", "SE", 24300, 27900, (2.0, 1.9, 1.8), (8.1, 7.6, 7.1), (14.2, 12.9, 11.9), (17.1, 15.5, 14.2), 0.146, 0.058, 0.98, 0.35, 0.206),
    ("Peer C A/S", "DK", 9800, 11900, (1.6, 1.5, 1.4), (7.2, 6.7, 6.3), (12.8, 11.6, 10.8), (15.0, 13.7, 12.6), 0.128, 0.049, 1.12, 0.42, 0.22),
    ("Peer D Oyj", "FI", 6400, 8300, (1.3, 1.2, 1.2), (6.5, 6.0, 5.7), (11.6, 10.6, 9.9), (13.4, 12.1, 11.2), 0.112, 0.041, 1.21, 0.55, 0.20),
    ("Peer E AB", "SE", 31200, 33800, (2.6, 2.4, 2.2), (10.2, 9.3, 8.6), (17.4, 15.6, 14.2), (21.3, 19.0, 17.1), 0.171, 0.083, 0.92, 0.18, 0.206),
    ("Peer F plc", "UK", 42000, 47700, (2.2, 2.0, 1.9), (9.4, 8.7, 8.1), (16.0, 14.5, 13.3), (19.4, 17.5, 15.9), 0.158, 0.064, 1.01, 0.26, 0.25),
    ("Peer G SE", "DE", 27700, 32900, (1.8, 1.7, 1.6), (7.8, 7.3, 6.9), (13.6, 12.4, 11.5), (16.2, 14.8, 13.6), 0.137, 0.052, 1.08, 0.38, 0.30),
    ("Peer H NV", "NL", 15100, 18200, (1.5, 1.4, 1.3), (7.0, 6.5, 6.1), (12.5, 11.3, 10.5), (14.6, 13.2, 12.1), 0.121, 0.046, 1.15, 0.47, 0.258),
]

if __name__ == "__main__":
    d = simulate()
    for k in ["rev", "ebitda", "ebit", "pbt", "np_sh", "cash", "equity", "minority_bs", "cfo", "ocl", "rou", "ppe"]:
        print(f"{k:12s}", [round(v, 1) for v in d[k]])
    eps = [d["np_sh"][i] / SHARES for i in range(7)]
    print("eps", [round(e, 2) for e in eps])
    print("payout", [round(DPS[i] / eps[i], 2) for i in range(7)])
    lease_liab = [d["lease_nc"][i] + d["lease_c"][i] for i in range(7)]
    print("lease liab", [round(v, 1) for v in lease_liab])
    nwc = [d["inv"][i] + d["rec"][i] + d["oca"][i] - d["pay"][i] - d["ocl"][i] for i in range(7)]
    print("nwc%", [round(nwc[i] / d["rev"][i], 4) for i in range(7)])
