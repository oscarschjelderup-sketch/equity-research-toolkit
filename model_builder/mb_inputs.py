"""Inputs, Hist and Drivers sheets."""
from datetime import date
from openpyxl.worksheet.datavalidation import DataValidation
from mb_core import *
import case_data as ex

M = ex.MARKET


def _dt(v, dflt):
    return date(*v) if v else dflt
DATA = ex.simulate()

# ============================================================ INPUTS
INP = Scalars("Inputs", start_row=4)


def _inputs_spec():
    s = INP
    I = lambda k: S("Inputs", k, "Inputs")
    s.section("1. Company information")
    s.item("company", "Company name", M["company"], kind="text", note="Used in all headers")
    s.item("ticker", "Ticker", M["ticker"], kind="text")
    s.item("exchange", "Exchange", M["exchange"], kind="text")
    s.item("sector", "Sector", M["sector"], kind="text")
    s.item("currency", "Reporting currency", M["currency"], kind="text")
    s.item("unit", "Reporting unit", M["unit"], kind="text", note="All financial figures are in this unit")
    s.item("team", "Case team / analyst", M["team"], kind="text")
    s.item("model_date", "Model date", _dt(M.get("model_date"), date(2026, 9, 16)), fmt=F_DATE, kind="input")
    s.blank()
    s.section("2. Timeline")
    s.item("first_hist", "First historical year", 2019, fmt=F_INT, note="Seven historical years: first year + 6")
    s.item("last_act", "Last actual year", lambda: f"={I('first_hist')}+6", fmt=F_INT)
    s.item("first_fc", "First forecast year", lambda: f"={I('last_act')}+1", fmt=F_INT)
    s.item("last_fc", "Last explicit forecast year", lambda: f"={I('first_fc')}+7", fmt=F_INT,
           note="Eight explicit forecast years, then terminal value")
    s.item("val_date", "Valuation date", _dt(M.get("val_date"), date(2026, 9, 16)), fmt=F_DATE, kind="input",
           note="Normally the share price date")
    s.item("fye1", "Fiscal year end, first forecast year", lambda: f"=DATE({I('first_fc')},12,31)", fmt=F_DATE,
           note="Assumes December year end")
    s.item("stub", "Share of first forecast year remaining", lambda: f"=MAX(0,MIN(1,({I('fye1')}-{I('val_date')})/365))",
           fmt=F_PCT, note="Only this share of the first year's FCFF is valued (stub period)")
    s.blank()
    s.section("3. Market data")
    s.item("price", "Share price", M["share_price"], fmt=F_NOK, unit="NOK", note="Source: Oslo Børs / Bloomberg – update")
    s.item("price_date", "Share price date", _dt(M.get("price_date"), date(2026, 9, 16)), fmt=F_DATE, kind="input")
    s.item("shares", "Shares outstanding", M["shares"], fmt=F_NUM1, unit="m", note="Excl. treasury shares")
    s.item("dilutive", "Dilutive instruments (options, RSUs)", M["dilutive"], fmt=F_NUM1, unit="m",
           note="Treasury-stock method or face value")
    s.item("shares_dil", "Diluted shares", lambda: f"={I('shares')}+{I('dilutive')}", fmt=F_NUM1, unit="m")
    s.item("mcap", "Market capitalisation", lambda: f"={I('price')}*{I('shares')}", fmt=F_NUM, unit="NOKm")
    s.item("high52", "52-week high", M["high52"], fmt=F_NOK, unit="NOK")
    s.item("low52", "52-week low", M["low52"], fmt=F_NOK, unit="NOK")
    s.item("cons_tp", "Consensus target price (optional)", M["consensus_tp"], fmt=F_NOK, unit="NOK",
           note="Bloomberg consensus, if provided in the case material")
    s.blank()
    s.section("4. Net debt and EV bridge (latest reported balance sheet)")
    s.item("bs_date", "Balance sheet date", _dt(M.get("bs_date"), date(2026, 6, 30)), fmt=F_DATE, kind="input", note="Latest quarterly report")
    s.item("debt", "Interest-bearing debt", M["debt_q"], fmt=F_NUM, unit="NOKm", note="Excl. lease liabilities")
    s.item("cash", "Cash and cash equivalents", M["cash_q"], fmt=F_NUM, unit="NOKm")
    s.item("nibd", "Net interest-bearing debt excl. leases", lambda: f"={I('debt')}-{I('cash')}", fmt=F_NUM, unit="NOKm", bold=True)
    s.item("leases", "Lease liabilities (IFRS 16)", M["leases_q"], fmt=F_NUM, unit="NOKm",
           note="Not deducted in the DCF: FCFF is after lease payments (pre-IFRS 16)")
    s.item("minority", "Minority interests", M["minority_q"], fmt=F_NUM, unit="NOKm", note="Book value, or market value if available")
    s.item("associates", "Associates and financial investments", M["associates_q"], fmt=F_NUM, unit="NOKm",
           note="Non-operating assets not captured by FCFF")
    s.item("pension", "Pension deficit and other debt-like items", M["pension_q"], fmt=F_NUM, unit="NOKm")
    s.item("other_adj", "Other adjustments (+ adds to equity value)", M["other_adj"], fmt=F_NUM, unit="NOKm")
    s.item("ev_ex", "Enterprise value at current price, excl. leases",
           lambda: f"={I('mcap')}+{I('nibd')}+{I('minority')}-{I('associates')}+{I('pension')}-{I('other_adj')}",
           fmt=F_NUM, unit="NOKm", bold=True)
    s.item("ev_incl", "Enterprise value at current price, incl. leases", lambda: f"={I('ev_ex')}+{I('leases')}",
           fmt=F_NUM, unit="NOKm", bold=True)
    s.blank()
    s.section("5. Valuation settings")
    s.item("scenario", "Active scenario", "Base", kind="text", note="Drop-down: Bear / Base / Bull")
    s.item("scen_idx", "Scenario index (1 = Bear, 2 = Base, 3 = Bull)",
           lambda: f"=IF(N({S('Sensitivity', 'ovr_scen')})>0,{S('Sensitivity', 'ovr_scen')},MATCH({I('scenario')},$H$6:$H$8,0))",
           fmt=F_INT, note="Data tables on the Sensitivity sheet override this temporarily")
    s.item("midyear", "Mid-year discounting (1 = on, 0 = off)", 1, fmt=F_INT, note="Cash flows assumed to arrive evenly through the year")
    s.item("w_gordon", "Terminal value weight – Gordon growth", 1.0, fmt=F_PCT, note="Recommended: 100% Gordon, exit multiple as a cross-check")
    s.item("w_exit", "Terminal value weight – exit multiple", lambda: f"=1-{I('w_gordon')}", fmt=F_PCT)
    s.item("tv_method", "Terminal FCFF (1 = value driver / RONIC, 2 = last FCFF x (1+g))", 1, fmt=F_INT,
           note="Value driver: FCFF = NOPAT x (1 - g / RONIC) – avoids too little reinvestment")
    s.item("w_dcf", "Target price weight – DCF", 0.70, fmt=F_PCT)
    s.item("w_peers", "Target price weight – peer multiples", lambda: f"=1-{I('w_dcf')}", fmt=F_PCT)
    s.item("roll12", "Roll forward to 12-month target price (1 = yes)", 1, fmt=F_INT,
           note="TP = fair value x (1 + cost of equity) - dividend next 12m")
    s.item("round_to", "Round target price to nearest", 1, fmt=F_INT, unit="NOK")
    s.item("buy_th", "BUY if expected total return exceeds the cost of equity by at least", 0.05, fmt=F_PCT,
           note="A fairly priced share is expected to return its cost of equity – only the excess justifies a BUY")
    s.item("sell_th", "SELL if expected total return falls short of the cost of equity by at least", -0.05, fmt=F_PCT,
           note="Entered as a negative number. HOLD in between")
    s.item("ronic_tol", "Max ratio: explicit-period return on new capital / the higher of today's ROIC and the terminal RONIC",
           2.5, fmt=F_MULT,
           note="Sanity check on the DCF sheet: growth must be paid for with capex and NWC. Price increases on existing locations need no capital")
    s.item("util_tol", "Max volume per mature location above the historical peak (location mode)", ex.ENGINE["util_tol"], fmt=F_PCT,
           note="Utilisation check: like-for-like growth cannot fill locations far beyond anything seen historically")
    s.item("peer_lease", "Peer multiples include lease liabilities in EV (1 = yes)", M.get("peer_lease", 1), fmt=F_INT,
           note="1 = IFRS 16 basis (typical for Bloomberg consensus). Controls company metrics and EV bridge")
    s.item("peer_year", "Forecast year used for peer valuation (1 or 2)", M.get("peer_year", 2), fmt=F_INT,
           note="1 = first forecast year, 2 = second forecast year")
    s.blank()
    s.section("6. Revenue build and labels")
    s.item("rev_mode", "Revenue build (1 = segments: volume growth x price/mix, 2 = locations: like-for-like + new locations)",
           ex.ENGINE["rev_mode"], fmt=F_INT,
           note="Location mode ties revenue, fixed costs, rent and growth capex to the number of locations (Drivers A, E and F)")
    s.item("seg_a", "Segment A name", M.get("seg_a", "Norway"), kind="text")
    s.item("seg_b", "Segment B name", M.get("seg_b", "Sweden"), kind="text")
    s.item("seg_c", "Segment C name", M.get("seg_c", "Denmark & Finland"), kind="text")
    s.item("vol_unit", "Volume KPI (unit)", M.get("vol_unit", "Customers ('000)"), kind="text", note="E.g. members, FTEs, stores, tonnes")
    s.item("norm_tax", "Normalised tax rate (historical NOPAT)", 0.22, fmt=F_PCT, note="Norwegian corporate tax rate")


_inputs_spec()


def write_inputs(wb):
    ws = wb["Inputs"]
    sheet_title(ws, "Inputs & settings", "Blue cells on a yellow background are inputs. Start here.",
                company_ref=False)
    INP.write(ws)
    ws.column_dimensions["A"].width = 2
    ws.column_dimensions["B"].width = 52
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 9
    ws.column_dimensions["E"].width = 70
    ws.column_dimensions["G"].width = 2
    ws.column_dimensions["H"].width = 12
    put(ws, "H4", "Lists", kind="label", bold=True, color=GREY)
    for i, v in enumerate(["Bear", "Base", "Bull"]):
        put(ws, f"H{6 + i}", v, kind="note")
    dv = DataValidation(type="list", formula1="=$H$6:$H$8", allow_blank=False)
    dv.error, dv.errorTitle = "Choose Bear, Base or Bull", "Scenario"
    ws.add_data_validation(dv)
    dv.add(CELLS[("Inputs", "scenario")])
    dv01 = DataValidation(type="list", formula1='"1,0"', allow_blank=False)
    ws.add_data_validation(dv01)
    for k in ["midyear", "roll12", "peer_lease"]:
        dv01.add(CELLS[("Inputs", k)])
    dv12 = DataValidation(type="list", formula1='"1,2"', allow_blank=False)
    ws.add_data_validation(dv12)
    for k in ["tv_method", "peer_year", "rev_mode"]:
        dv12.add(CELLS[("Inputs", k)])
    dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="1")
    dvp.error = "Enter a weight between 0% and 100%"
    ws.add_data_validation(dvp)
    for k in ["w_gordon", "w_dcf"]:
        dvp.add(CELLS[("Inputs", k)])
    ws.freeze_panes = "A4"


# ============================================================ HIST
HIST = TS("Hist", start_row=7, last_col="K")


def _hist_spec():
    t = HIST
    d = DATA
    H = lambda k: ROWS[("Hist", k)]
    I = lambda k: S("Inputs", k)

    def inp(k):
        return lambda c, p, i: None if d[k][i] is None else round(float(d[k][i]), 2)

    def f(expr):
        """expr uses {k} for current-column cell of row k and [k] for previous column."""
        import re as _re

        def build(c, p, i):
            s = _re.sub(r"\{(\w+)\}", lambda m: f"{c}{H(m.group(1))}", expr)
            s = _re.sub(r"\[(\w+)\]", lambda m: f"{p}{H(m.group(1))}", s)
            return "=" + s
        return build

    seg = lambda k: (lambda: f'="Revenue – "&{I(k)}')
    vol = lambda k: (lambda: f'="Volume – "&{I(k)}&" ("&{I("vol_unit")}&")"')
    t.section("Income statement")
    t.row("rev_a", seg("seg_a"), "NOKm", hist=inp("revA"), indent=1)
    t.row("rev_b", seg("seg_b"), "NOKm", hist=inp("revB"), indent=1)
    t.row("rev_c", seg("seg_c"), "NOKm", hist=inp("revC"), indent=1)
    t.row("rev", "Total revenue", "NOKm", hist=f("SUM({rev_a}:{rev_c})"), bold=True, line=True)
    t.row("cogs", "Cost of goods sold", "NOKm", hist=inp("cogs"))
    t.row("gp", "Gross profit", "NOKm", hist=f("{rev}+{cogs}"), bold=True, line=True)
    t.row("pers", "Personnel expenses", "NOKm", hist=inp("pers"))
    t.row("oth", "Other operating expenses", "NOKm", hist=inp("oth"))
    t.row("ebitda", "EBITDA (reported, IFRS 16)", "NOKm", hist=f("{gp}+{pers}+{oth}"), bold=True, line=True)
    t.row("da", "D&A – owned assets", "NOKm", hist=inp("da"))
    t.row("rou_dep", "Depreciation – right-of-use assets", "NOKm", hist=inp("rou_dep"))
    t.row("special", "Impairments and special items", "NOKm", hist=inp("special"))
    t.row("ebit", "EBIT (reported)", "NOKm", hist=f("{ebitda}+{da}+{rou_dep}+{special}"), bold=True, line=True)
    t.row("netfin", "Net financial items excl. leases", "NOKm", hist=inp("netfin"))
    t.row("lease_int", "Interest on lease liabilities", "NOKm", hist=inp("lease_int"))
    t.row("pbt", "Profit before tax", "NOKm", hist=f("{ebit}+{netfin}+{lease_int}"), bold=True, line=True)
    t.row("tax", "Income tax", "NOKm", hist=inp("tax"))
    t.row("np", "Net profit", "NOKm", hist=f("{pbt}+{tax}"), bold=True, line=True)
    t.row("min_pl", "Minority interests", "NOKm", hist=inp("minority_pl"))
    t.row("np_sh", "Net profit to shareholders", "NOKm", hist=f("{np}+{min_pl}"), bold=True, line=True)
    t.blank()
    t.section("IFRS 16 adjustment and adjusted earnings")
    t.row("lease_pay", "Lease payments, total (from cash flow statement)", "NOKm", hist=inp("lease_pay"),
          note="Principal + interest. Enter as a negative number")
    t.row("ebitdaal", "EBITDAaL – EBITDA after leases (pre-IFRS 16)", "NOKm", hist=f("{ebitda}+{lease_pay}"), bold=True)
    t.row("ebit_adj", "EBIT adj. (pre-IFRS 16, excl. special items)", "NOKm", hist=f("{ebitdaal}+{da}"), bold=True)
    t.blank()
    t.section("Balance sheet")
    for k, lab, key in [("gw", "Goodwill", "gw"), ("intang", "Other intangible assets", "intang"),
                        ("ppe", "Property, plant and equipment", "ppe"), ("rou", "Right-of-use assets", "rou"),
                        ("other_nca", "Other non-current assets", "other_nca"), ("inv", "Inventories", "inv"),
                        ("rec", "Trade receivables", "rec"), ("oca", "Other current assets", "oca"),
                        ("cash", "Cash and cash equivalents", "cash")]:
        t.row(k, lab, "NOKm", hist=inp(key))
    t.row("ta", "Total assets", "NOKm", hist=f("SUM({gw}:{cash})"), bold=True, line=True)
    t.row("equity", "Equity to shareholders", "NOKm", hist=inp("equity"))
    t.row("min_bs", "Minority interests", "NOKm", hist=inp("minority_bs"))
    t.row("te", "Total equity", "NOKm", hist=f("{equity}+{min_bs}"), bold=True, line=True)
    for k, lab, key in [("debt_nc", "Interest-bearing debt – non-current", "debt_nc"),
                        ("debt_c", "Interest-bearing debt – current", "debt_c"),
                        ("lease_nc", "Lease liabilities – non-current", "lease_nc"),
                        ("lease_c", "Lease liabilities – current", "lease_c"),
                        ("deftax", "Deferred tax and other non-current liabilities", "deftax"),
                        ("pay", "Trade payables", "pay"),
                        ("ocl", "Other current liabilities (incl. deferred revenue)", "ocl")]:
        t.row(k, lab, "NOKm", hist=inp(key))
    t.row("tel", "Total equity and liabilities", "NOKm", hist=f("{te}+SUM({debt_nc}:{ocl})"), bold=True, line=True)
    t.row("bs_check", "Balance check (should be zero)", "NOKm", hist=f("ROUND({ta}-{tel},1)"), italic=True, fmt=F_NUM1)
    t.blank()
    t.section("Cash flow statement (condensed)")
    t.row("cfo", "Cash flow from operations (excl. lease payments)", "NOKm", hist=inp("cfo"))
    t.row("capex", "Capital expenditure", "NOKm", hist=inp("capex"))
    t.row("acq", "Acquisitions and disposals", "NOKm", hist=inp("acq"))
    t.row("cf_lease", "Lease payments", "NOKm", hist=f("{lease_pay}"))
    t.row("div_paid", "Dividends paid", "NOKm", hist=inp("div_paid"))
    t.row("fin_other", "Net change in debt and other financing", "NOKm", hist=inp("fin_other"))
    t.row("net_cash", "Net change in cash", "NOKm", hist=f("SUM({cfo}:{fin_other})"), bold=True, line=True)
    t.row("cf_check", "Cash flow vs. balance sheet (should be zero)", "NOKm",
          hist=f("ROUND({net_cash}-({cash}-[cash]),1)"), hist_from=1, italic=True, fmt=F_NUM1)
    t.blank()
    t.section("KPIs and per-share data")
    t.row("vol_a", vol("seg_a"), "#", hist=inp("volA"))
    t.row("vol_b", vol("seg_b"), "#", hist=inp("volB"))
    t.row("vol_c", vol("seg_c"), "#", hist=inp("volC"))
    loc = lambda k: (lambda: f'="Locations – "&{I(k)}')
    t.row("loc_a", loc("seg_a"), "#", hist=inp("locA"))
    t.row("loc_b", loc("seg_b"), "#", hist=inp("locB"))
    t.row("loc_c", loc("seg_c"), "#", hist=inp("locC"))
    t.row("locations", "Number of locations", "#", hist=f("{loc_a}+{loc_b}+{loc_c}"), bold=True, line=True)
    t.row("ftes", "Full-time employees (FTEs)", "#", hist=inp("ftes"))
    t.row("shares", "Shares outstanding, year-end", "m", hist=inp("shares"), fmt=F_NUM1)
    t.row("dps", "Dividend per share (for the fiscal year)", "NOK", hist=inp("dps"), fmt=F_NOK)
    t.row("price_ye", "Share price, year-end", "NOK", hist=inp("price"), fmt=F_NOK)
    t.blank()
    t.section("Key ratios (calculated – used as reference for the forecast)")
    t.row("g_rev", "Revenue growth", "%", hist=f("{rev}/[rev]-1"), hist_from=1, fmt=F_PCT, italic=True)
    for s_ in "abc":
        t.row(f"g_rev_{s_}", (lambda s_=s_: f'="  Revenue growth – "&{I("seg_" + s_)}'), "%",
              hist=f(f"{{rev_{s_}}}/[rev_{s_}]-1"), hist_from=1, fmt=F_PCT, italic=True)
    for s_ in "abc":
        t.row(f"g_vol_{s_}", (lambda s_=s_: f'="  Volume growth – "&{I("seg_" + s_)}'), "%",
              hist=f(f"{{vol_{s_}}}/[vol_{s_}]-1"), hist_from=1, fmt=F_PCT, italic=True)
    for s_ in "abc":
        t.row(f"px_{s_}", (lambda s_=s_: f'="  Price/mix growth – "&{I("seg_" + s_)}'), "%",
              hist=f(f"(1+{{g_rev_{s_}}})/(1+{{g_vol_{s_}}})-1"), hist_from=1, fmt=F_PCT, italic=True)
    for s_ in "abc":
        t.row(f"rpu_{s_}", (lambda s_=s_: f'="  Revenue per unit – "&{I("seg_" + s_)}'), "NOK '000",
              hist=f(f"IF({{vol_{s_}}}=0,0,{{rev_{s_}}}/{{vol_{s_}}})"), fmt=F_NOK, italic=True)
    for s_ in "abc":
        t.row(f"net_loc_{s_}", (lambda s_=s_: f'="  Net new locations – "&{I("seg_" + s_)}'), "#",
              hist=f(f"{{loc_{s_}}}-[loc_{s_}]"), hist_from=1, fmt=F_NUM, italic=True)
    for s_ in "abc":
        t.row(f"mpl_{s_}", (lambda s_=s_: f'="  Volume per location – "&{I("seg_" + s_)}'), "#",
              hist=f(f"IF({{loc_{s_}}}=0,0,{{vol_{s_}}}/{{loc_{s_}}})"), fmt=F_NOK, italic=True)
    for s_ in "abc":
        t.row(f"g_mpl_{s_}", (lambda s_=s_: f'="  Like-for-like growth in volume per location – "&{I("seg_" + s_)}'), "%",
              hist=f(f"IF([mpl_{s_}]=0,0,{{mpl_{s_}}}/[mpl_{s_}]-1)"), hist_from=1, fmt=F_PCT, italic=True)
    t.row("gm", "Gross margin", "%", hist=f("{gp}/{rev}"), fmt=F_PCT, italic=True)
    t.row("cogs_pct", "COGS in % of revenue", "%", hist=f("-{cogs}/{rev}"), fmt=F_PCT, italic=True)
    t.row("pers_pct", "Personnel expenses in % of revenue", "%", hist=f("-{pers}/{rev}"), fmt=F_PCT, italic=True)
    t.row("oth_pct", "Other opex in % of revenue", "%", hist=f("-{oth}/{rev}"), fmt=F_PCT, italic=True)
    t.row("ebitda_m", "EBITDA margin (reported)", "%", hist=f("{ebitda}/{rev}"), fmt=F_PCT, italic=True)
    t.row("lease_pct", "Lease payments in % of revenue", "%", hist=f("-{lease_pay}/{rev}"), fmt=F_PCT, italic=True)
    t.row("ebitdaal_m", "EBITDAaL margin", "%", hist=f("{ebitdaal}/{rev}"), fmt=F_PCT, italic=True)
    t.row("da_pct", "D&A (owned assets) in % of revenue", "%", hist=f("-{da}/{rev}"), fmt=F_PCT, italic=True)
    t.row("ebit_adj_m", "EBIT adj. margin", "%", hist=f("{ebit_adj}/{rev}"), fmt=F_PCT, italic=True)
    t.row("capex_pct", "Capex in % of revenue", "%", hist=f("-{capex}/{rev}"), fmt=F_PCT, italic=True)
    t.row("capex_da", "Capex / D&A", "x", hist=f("IF({da}=0,0,{capex}/{da})"), fmt=F_MULT2, italic=True)
    t.row("s2c_hist", "Incremental revenue per NOK of net investment (capex – D&A)", "x",
          hist=f('IF(-{capex}+{da}<=0,"n.m.",({rev}-[rev])/(-{capex}+{da}))'), hist_from=1, fmt=F_MULT, italic=True,
          note="Reference for the sales-to-capital driver. Organic investment only (acquisitions excluded)")
    t.row("tax_eff", "Effective tax rate", "%", hist=f("IF({pbt}=0,0,-{tax}/{pbt})"), fmt=F_PCT, italic=True)
    t.row("nwc", "Net working capital", "NOKm", hist=f("{inv}+{rec}+{oca}-{pay}-{ocl}"))
    t.row("nwc_pct", "NWC in % of revenue", "%", hist=f("{nwc}/{rev}"), fmt=F_PCT, italic=True)
    t.row("ic", "Invested capital (pre-IFRS 16)", "NOKm", hist=f("{nwc}+{ppe}+{intang}+{gw}"),
          note="NWC + PP&E + intangibles + goodwill")
    t.row("nopat", "NOPAT (pre-IFRS 16, normalised tax)", "NOKm",
          hist=lambda c, p, i: f"={c}{H('ebit_adj')}*(1-{I('norm_tax')})")
    t.row("roic", "ROIC (average invested capital)", "%", hist=f("{nopat}/AVERAGE([ic],{ic})"), hist_from=1,
          fmt=F_PCT, italic=True)
    t.row("nibd", "Net interest-bearing debt excl. leases", "NOKm", hist=f("{debt_nc}+{debt_c}-{cash}"))
    t.row("nibd_ebitdaal", "NIBD / EBITDAaL", "x", hist=f("IF({ebitdaal}=0,0,{nibd}/{ebitdaal})"), fmt=F_MULT, italic=True)
    t.row("eps", "EPS", "NOK", hist=f("{np_sh}/{shares}"), fmt=F_NOK)
    t.row("payout", "Payout ratio", "%", hist=f("IF({eps}<=0,0,{dps}/{eps})"), fmt=F_PCT, italic=True)
    t.row("fcff", "FCFF (pre-IFRS 16, before acquisitions)", "NOKm",
          hist=f("{nopat}-{da}+{capex}-({nwc}-[nwc])"), hist_from=1)
    t.row("lease_int_sh", "Interest share of lease payments", "%", hist=f("IF({lease_pay}=0,0,{lease_int}/{lease_pay})"),
          fmt=F_PCT, italic=True)
    t.row("min_sh", "Minority share of net profit", "%", hist=f("IF({np}=0,0,-{min_pl}/{np})"), fmt=F_PCT, italic=True)
    t.row("int_rate", "Net interest rate on opening net debt", "%",
          hist=f("IF([nibd]<=0,0,-{netfin}/[nibd])"), hist_from=1, fmt=F_PCT, italic=True)


_hist_spec()


def write_hist(wb):
    ws = wb["Hist"]
    sheet_title(ws, "Historical financials",
                "Paste reported figures into the blue cells (costs as negative numbers). Subtotals and ratios are calculated.",
                last_col="K")
    ts_header(ws, "Hist", hist=True, fc=False, last_col="K")
    HIST.write(ws)
    ws.column_dimensions["V"].width = 50


# ============================================================ DRIVERS
from openpyxl.formatting.rule import FormulaRule as _FR


def _seg(s_, pre, post=""):
    return lambda: f'="{pre}"&{S("Inputs", "seg_" + s_)}&"{post}"'


BASE_KEYS = [  # key, label, hist ratio key (Hist), base values key
    ("vol_a", _seg("a", "Volume growth – ", " (segment mode)"), "g_vol_a", "volA"),
    ("px_a", _seg("a", "Price/mix growth – "), "px_a", "priceA"),
    ("vol_b", _seg("b", "Volume growth – ", " (segment mode)"), "g_vol_b", "volB"),
    ("px_b", _seg("b", "Price/mix growth – "), "px_b", "priceB"),
    ("vol_c", _seg("c", "Volume growth – ", " (segment mode)"), "g_vol_c", "volC"),
    ("px_c", _seg("c", "Price/mix growth – "), "px_c", "priceC"),
    ("lfl_a", _seg("a", "Like-for-like growth per location – ", " (location mode)"), "g_mpl_a", "lflA"),
    ("lfl_b", _seg("b", "Like-for-like growth per location – ", " (location mode)"), "g_mpl_b", "lflB"),
    ("lfl_c", _seg("c", "Like-for-like growth per location – ", " (location mode)"), "g_mpl_c", "lflC"),
    ("net_a", _seg("a", "Net new locations – ", " (location mode)"), "net_loc_a", "netA"),
    ("net_b", _seg("b", "Net new locations – ", " (location mode)"), "net_loc_b", "netB"),
    ("net_c", _seg("c", "Net new locations – ", " (location mode)"), "net_loc_c", "netC"),
    ("cogs", "COGS in % of revenue", "cogs_pct", "cogs"),
    ("pers_var", "Personnel expenses – variable part, in % of revenue", "pers_pct", "pers_var"),
    ("oth_var", "Other opex – variable part, in % of revenue", "oth_pct", "oth_var"),
    ("cpi", "Cost inflation on the fixed cost base and rent", None, "cpi"),
    ("fix_real", "Real growth in the fixed cost base (segment mode)", None, "fix_real"),
    ("lease", "Lease payments in % of revenue (IFRS 16, segment mode)", "lease_pct", "lease"),
    ("da", "D&A (owned assets) in % of revenue", "da_pct", "da"),
    ("mcapex", "Maintenance capex in % of revenue", "da_pct", "mcapex"),
    ("s2c", "Sales-to-capital for growth capex (segment mode)", "s2c_hist", "s2c"),
    ("capex_loc", "Capex per new location, NOKm (location mode)", None, "capex_loc"),
    ("nwc", "NWC in % of revenue", "nwc_pct", "nwc"),
    ("tax", "Tax rate", "tax_eff", "tax"),
    ("payout", "Dividend payout ratio", "payout", "payout"),
    ("rdebt", "Interest rate on net debt (pre-tax)", "int_rate", "rate_debt"),
    ("rcash", "Interest rate on net cash", None, "rate_cash"),
    ("lint", "Interest share of lease payments", "lease_int_sh", "lease_int"),
    ("mins", "Minority share of net profit", "min_sh", "min_share"),
]
DRV_FMT = {"s2c": F_MULT, "net_a": F_NUM, "net_b": F_NUM, "net_c": F_NUM, "capex_loc": F_NUM1}


def _unit(key):
    return {"s2c": "x", "capex_loc": "NOKm"}.get(key, "#" if key.startswith("net_") else "%")


DRV_NOTE = {
    "vol_a": "Segment mode only (greyed out in location mode): total volume growth per segment",
    "lfl_a": "Location mode: growth in volume per MATURE location. History: growth in volume per location",
    "net_a": "Location mode: openings minus closures. New locations ramp up over three years (section F)",
    "pers_var": "History shows the TOTAL ratio. Only this part scales with revenue – the fixed part (section E) grows with inflation and locations",
    "oth_var": "History shows the TOTAL ratio – see personnel expenses",
    "cpi": "Wage and price inflation on the fixed cost base – and on rent per location in location mode",
    "fix_real": "Segment mode only. In location mode the fixed cost base grows with the number of locations (section C)",
    "lease": "Segment mode only. In location mode rent per location grows with cost inflation (Model)",
    "mcapex": "History shows D&A in % of revenue. Maintenance and refurbishment ≈ the historical capex/D&A ratio (~1.14x)",
    "s2c": "Segment mode only. History: incremental revenue / (capex – D&A), flattered by acquired revenue. Lower = more capital-intensive",
    "capex_loc": "Location mode: fit-out, equipment and pre-opening costs per new location",
}
MODE1_ONLY = ["vol_a", "vol_b", "vol_c", "fix_real", "lease", "s2c"]
MODE2_ONLY = ["lfl_a", "lfl_b", "lfl_c", "net_a", "net_b", "net_c", "capex_loc"]
ADJ_MAP = {"vol_a": "vol", "vol_b": "vol", "vol_c": "vol", "lfl_a": "vol", "lfl_b": "vol", "lfl_c": "vol",
           "px_a": "price", "px_b": "price", "px_c": "price", "net_a": "open", "net_b": "open", "net_c": "open",
           "cogs": "cogs", "pers_var": "pers", "oth_var": "oth", "mcapex": "capex"}
SKIP_FIRST = ("g_vol_a", "g_vol_b", "g_vol_c", "px_a", "px_b", "px_c", "int_rate", "s2c_hist",
              "g_mpl_a", "g_mpl_b", "g_mpl_c", "net_loc_a", "net_loc_b", "net_loc_c")
CAP_KEYS = ["pers_fixsh", "oth_fixsh", "central", "lev_t", "bb_on", "bb_g"]
ENG_KEYS = ["ramp1", "ramp2", "ramp3"]

NB = len(BASE_KEYS)
DRV_BASE = TS("Drivers", start_row=10)
ADJ_START = 10 + 2 + NB + 3                       # section B rows (band two rows above, header one row above)
LIVE_START = ADJ_START + len(ex.SCENARIO_ADJ) + 2
DRV_LIVE = TS("Drivers", start_row=LIVE_START)
TERM_START = LIVE_START + 2 + NB + 4              # section D rows
CAP_START = TERM_START + 5 + 4                    # section E rows
ENG_START = CAP_START + len(CAP_KEYS) + 4         # section F rows


def _drivers_spec():
    b = DRV_BASE
    b.section("A. Base case drivers – enter forecast assumptions in the blue cells (history shown for reference)")
    for key, lab, hkey, bkey in BASE_KEYS:
        hist = None
        if hkey:
            hist = (lambda hkey=hkey: (lambda c, p, i: None if (i == 0 and hkey in SKIP_FIRST)
                                       else f"=Hist!{c}{ROWS[('Hist', hkey)]}"))()
        vals = ex.BASE[bkey]
        b.row(f"b_{key}", lab, _unit(key), fmt=DRV_FMT.get(key, F_PCT), hist=hist,
              fc=(lambda vals=vals: (lambda c, p, i: vals[i]))(), input_fc=True, note=DRV_NOTE.get(key))
    live = DRV_LIVE
    live.section("C. Live drivers used by the model (base case + active scenario adjustment + sensitivity adjustment)")
    for key, lab, hkey, bkey in BASE_KEYS:
        def fc(c, p, i, key=key):
            base = f"{c}{ROWS[('Drivers', 'b_' + key)]}"
            extra = ""
            if key in ADJ_MAP:
                extra += f"+{S('Drivers', 'adj_' + ADJ_MAP[key], 'Drivers')}"
            if key.startswith(("vol_", "lfl_")):
                extra += f"+N({S('Sensitivity', 'ovr_growth')})"
            if key == "oth_var":
                extra += f"-N({S('Sensitivity', 'ovr_margin')})"
            if key == "fix_real":
                _ls = ex.ENGINE.get("lease_scale")
                if _ls == "new_locations":          # openings at last year's revenue per location (same driver as the rent row)
                    p_ = chr(ord(c) - 1)
                    r_ = lambda k: ROWS[("Model", k)]
                    _g = ("(" + "+".join(f"IF(Model!{p_}{r_('loc_' + x)}=0,0,Model!{p_}{r_('rev_' + x)}*(Model!{c}{r_('loc_' + x)}/Model!{p_}{r_('loc_' + x)}-1))"
                                         for x in "abc") + f")/Model!{p_}{r_('rev')}")
                else:
                    _grow = ROWS[("Model", "g_newc")] if _ls == "new_revenue" else ROWS[("Model", "loc_g")]
                    _g = f"Model!{c}{_grow}"
                return (f"=IF({S('Inputs', 'rev_mode')}=2,(1-{S('Drivers', 'central', 'Drivers')})*{_g},{base}{extra})")
            return f"={base}{extra}"
        if key == "fix_real":
            lab = "Real growth in the fixed cost base (location mode: from the locations)"
        live.row(key, lab, _unit(key), fmt=DRV_FMT.get(key, F_PCT), fc=fc)
    # scalar blocks
    for j, (k, lab, bear, base, bull, com) in enumerate(ex.SCENARIO_ADJ):
        r = ADJ_START + j
        CELLS[("Drivers", f"adj_{k}")] = f"H{r}"
        CELLS[("Drivers", f"adj_{k}_bear")] = f"E{r}"
        CELLS[("Drivers", f"adj_{k}_base")] = f"F{r}"
        CELLS[("Drivers", f"adj_{k}_bull")] = f"G{r}"
    for j, k in enumerate(["tg", "ty_margin", "ronic", "lt_tax", "exit"]):
        CELLS[("Drivers", k)] = f"H{TERM_START + j}"
        CELLS[("Drivers", k + "_in")] = f"E{TERM_START + j}"
    for j, k in enumerate(CAP_KEYS):
        CELLS[("Drivers", k)] = f"H{CAP_START + j}"
        CELLS[("Drivers", k + "_in")] = f"E{CAP_START + j}"
    for j, k in enumerate(ENG_KEYS):
        CELLS[("Drivers", k)] = f"H{ENG_START + j}"
        CELLS[("Drivers", k + "_in")] = f"E{ENG_START + j}"


_drivers_spec()


def _scalar_block(ws, start, title, rows):
    """Campari-style scalar block: label (B), input (E), active value (H), comment (J)."""
    band(ws, start - 2, "B", "T", title)
    hdr = start - 1
    for col, txt in [("B", "Assumption"), ("E", "Input"), ("H", "Active"), ("J", "Comment")]:
        put(ws, f"{col}{hdr}", txt, kind="label", bold=True, align="right" if col in "EH" else None)
    bottom_border(ws, hdr, "B", "T")
    for j, (k, lab, v, fmt, active, com) in enumerate(rows):
        r = start + j
        put(ws, f"B{r}", lab, kind="label")
        if v is None:
            style(ws[f"E{r}"], "input", fmt=fmt)
        else:
            put(ws, f"E{r}", v, fmt=fmt)
        put(ws, f"H{r}", active, fmt=fmt, bold=True, fill=PALE)
        put(ws, f"J{r}", com, kind="note", italic=True)


def write_drivers(wb):
    ws = wb["Drivers"]
    sheet_title(ws, "Forecast drivers & scenarios",
                "Base case per year (A), scenario adjustments (B), terminal value (D), cost structure and capital allocation (E), "
                "ramp-up of new locations (F). The model reads C–F.")
    ts_header(ws, "Drivers", hist=True, fc=True, ty=False)
    mode = S("Inputs", "rev_mode")
    put(ws, "B7", "Active scenario", kind="label", bold=True)
    put(ws, "E7", f"={S('Inputs', 'scenario')}", bold=True, color=NAVY, align="right")
    put(ws, "G7", f'="Revenue build: "&IF({mode}=2,"locations (like-for-like + new locations)","segments (volume x price/mix)")'
                  f'&" – greyed-out rows are not used (switch on Inputs)"', italic=True, color=NAVY)
    put(ws, "B8", "Scenario index (1 = Bear, 2 = Base, 3 = Bull)", kind="label")
    put(ws, "E8", f"={S('Inputs', 'scen_idx')}", fmt=F_INT, align="right")
    DRV_BASE.write(ws)
    put(ws, "T5", "Hist. avg (3y)", kind="label", bold=True, align="right", color=WHITE, fill=NAVY)
    ws.column_dimensions["T"].width = 12
    for key, *_ in BASE_KEYS:
        r = ROWS[("Drivers", "b_" + key)]
        put(ws, f"T{r}", f'=IFERROR(AVERAGE(I{r}:K{r}),"")', fmt=DRV_FMT.get(key, F_PCT), italic=True, color=GREY)
    # section B – scenario adjustments
    band(ws, ADJ_START - 2, "B", "T", "B. Scenario adjustments – added to every forecast year of the base case")
    hdr = ADJ_START - 1
    for col, txt in [("B", "Driver"), ("E", "Bear"), ("F", "Base"), ("G", "Bull"), ("H", "Active"), ("J", "Comment")]:
        put(ws, f"{col}{hdr}", txt, kind="label", bold=True, align="right" if col in "EFGH" else None)
    bottom_border(ws, hdr, "B", "T")
    for j, (k, lab, bear, base, bull, com) in enumerate(ex.SCENARIO_ADJ):
        r = ADJ_START + j
        fmt = F_MULT if k == "exit" else (F_NUM if k == "open" else F_PCT)
        put(ws, f"B{r}", lab, kind="label")
        put(ws, f"E{r}", bear, fmt=fmt)
        put(ws, f"F{r}", base, fmt=fmt)
        put(ws, f"G{r}", bull, fmt=fmt)
        if k == "prob":
            put(ws, f"H{r}", f"=SUM(E{r}:G{r})", fmt=F_PCT, bold=True)
            put(ws, f"J{r}", com + " (sum shown in Active column)", kind="note", italic=True)
        else:
            put(ws, f"H{r}", f"=CHOOSE({S('Inputs', 'scen_idx')},E{r},F{r},G{r})", fmt=fmt, bold=True, fill=PALE)
            put(ws, f"J{r}", com, kind="note", italic=True)
    DRV_LIVE.write(ws)
    # section D – terminal assumptions
    T = ex.TERMINAL
    ebit_m = X("Model", "ebit_adj_m", FC[-1], absc=True, absr=True)
    _scalar_block(ws, TERM_START, "D. Terminal value assumptions", [
        ("tg", "Terminal growth rate (nominal)", T["tg"], F_PCT,
         f"=E{TERM_START}+{S('Drivers', 'adj_tg', 'Drivers')}",
         "Long-run nominal growth; should not exceed long-term GDP growth (~2-3%)"),
        ("ty_margin", "Terminal EBIT adj. margin – override (blank = last forecast year)", None, F_PCT,
         f'=IF(E{TERM_START + 1}="",{ebit_m},E{TERM_START + 1})',
         "Leave blank to use the final forecast year's margin (already scenario-adjusted)"),
        ("ronic", "Return on new invested capital (RONIC)", T["ronic"], F_PCT, f"=E{TERM_START + 2}",
         "Set close to WACC for companies without a lasting competitive advantage"),
        ("lt_tax", "Long-term tax rate", T["tax"], F_PCT, f"=E{TERM_START + 3}", ""),
        ("exit", "Exit multiple, EV / EBITDAaL (pre-IFRS 16)", T["exit"], F_MULT,
         f"=E{TERM_START + 4}+{S('Drivers', 'adj_exit', 'Drivers')}",
         "Cross-check only unless given weight on the Inputs sheet"),
    ])
    # section E – cost structure and capital allocation
    C = ex.COST_CAPITAL
    _scalar_block(ws, CAP_START, "E. Cost structure and capital allocation", [
        ("pers_fixsh", "Fixed share of personnel expenses (last actual year)", C["pers_fixsh"], F_PCT, f"=E{CAP_START}",
         "Staffing per location is largely fixed. The fixed part grows with cost inflation and capacity (section C), not with revenue"),
        ("oth_fixsh", "Fixed share of other opex (last actual year)", C["oth_fixsh"], F_PCT, f"=E{CAP_START + 1}",
         "IT, admin and premises-related costs are fixed; marketing and variable services scale with revenue"),
        ("central", "Central share of fixed costs (inflation only, location mode)", C["central"], F_PCT,
         f"=E{CAP_START + 2}",
         "Head office, IT and brand costs do not grow with the number of locations – the source of operating leverage from openings"),
        ("lev_t", "Target leverage for buybacks (NIBD / EBITDAaL)", C["lev_t"], F_MULT2, f"=E{CAP_START + 3}",
         "Cash above this leverage is returned to shareholders when the switch below is on"),
        ("bb_on", "Return excess cash via share buybacks (1 = yes, 0 = let cash build up)", C["bb_on"], F_INT, f"=E{CAP_START + 4}",
         "Keeps the forecast capital structure close to the WACC assumption and lifts EPS; 0 = cash piles up at the cash rate"),
        ("bb_g", "Assumed annual share price growth for buybacks", C["bb_g"], F_PCT, f"=E{CAP_START + 5}",
         "Buyback price = current share price grown at this rate (deliberately not linked to the cost of equity – avoids a circular reference)"),
    ])
    # section F – location engine
    R = ex.ENGINE["ramp"]
    _scalar_block(ws, ENG_START, "F. Location engine – ramp-up of new locations (location mode)", [
        ("ramp1", "Opening year: volume in % of a mature location", R[0], F_PCT, f"=E{ENG_START}",
         "Opened during the year and still filling up – roughly half a year at ~70% of mature volume"),
        ("ramp2", "Second year: volume in % of a mature location", R[1], F_PCT, f"=E{ENG_START + 1}",
         "Most new locations reach 70-80% of mature volume in their first full year"),
        ("ramp3", "Third year: volume in % of a mature location (100% from the fourth year)", R[2], F_PCT, f"=E{ENG_START + 2}",
         "Check the curve against the company's own disclosures on club / store maturity"),
    ])
    # grey out the rows the active revenue build does not use
    grey = Font(name=FONT, color="A6A6A6", italic=True)
    for keys, cond in [(MODE1_ONLY, "RevenueMode=2"), (MODE2_ONLY, "RevenueMode=1")]:
        for key in keys:
            rows_ = [ROWS[("Drivers", "b_" + key)]]
            if key != "fix_real":
                rows_.append(ROWS[("Drivers", key)])
            for r in rows_:
                ws.conditional_formatting.add(f"B{r}:T{r}", _FR(formula=[cond], font=grey))
