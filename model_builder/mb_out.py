"""Checks, Dashboard, Deck_Feed, Cover and Guide sheets (+ charts)."""
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from mb_core import *
from mb_val import SENS, CR, t4_col, FB_METHODS
from mb_market import RD_ROWS
import case_data as ex

D = lambda k: S("DCF", k)
I = lambda k: S("Inputs", k)


# ============================================================ CHECKS
CHK0 = 7


def check_list():
    mr = lambda k: ROWS[("Model", k)]
    hr = lambda k: ROWS[("Hist", k)]
    s1 = SENS["t1_rows"][0]
    return [
        ("Historical balance sheet balances", f"=MAX(ABS(MAX(Hist!E{hr('bs_check')}:K{hr('bs_check')})),ABS(MIN(Hist!E{hr('bs_check')}:K{hr('bs_check')})))",
         "abs(x)<=0.5", "Error", F_NUM1, "Check the balance sheet inputs on Hist (costs negative, totals complete)"),
        ("Historical cash flow ties to change in cash", f"=MAX(ABS(MAX(Hist!F{hr('cf_check')}:K{hr('cf_check')})),ABS(MIN(Hist!F{hr('cf_check')}:K{hr('cf_check')})))",
         "abs(x)<=0.5", "Warning", F_NUM1, "Condensed cash flow may omit FX and other items – fine if explained"),
        ("Revenue build equals reported revenue (history)", f"=SUMPRODUCT(ABS(Model!E{mr('is_rev')}:K{mr('is_rev')}-Hist!E{hr('rev')}:K{hr('rev')}))",
         "abs(x)<=0.5", "Error", F_NUM1, "Segment revenues must add up to total revenue"),
        ("Model EBIT equals reported EBIT (history)", f"=SUMPRODUCT(ABS(Model!E{mr('ebit')}:K{mr('ebit')}-Hist!E{hr('ebit')}:K{hr('ebit')}))",
         "abs(x)<=0.5", "Error", F_NUM1, "Check the mapping of D&A, right-of-use depreciation and special items"),
        ("Forecast balance sheet balances (Output)",
         f"=MAX(ABS(MAX(Output!E{ROWS[('Output', 'bs_check')]}:S{ROWS[('Output', 'bs_check')]})),ABS(MIN(Output!E{ROWS[('Output', 'bs_check')]}:S{ROWS[('Output', 'bs_check')]})))",
         "abs(x)<=0.5", "Error", F_NUM1, "Capital employed must equal funds invested in every year"),
        ("Cash flow statement ties to net debt (Output)",
         f"=MAX(ABS(MAX(Output!F{ROWS[('Output', 'cf_check')]}:S{ROWS[('Output', 'cf_check')]})),ABS(MIN(Output!F{ROWS[('Output', 'cf_check')]}:S{ROWS[('Output', 'cf_check')]})))",
         "abs(x)<=0.5", "Error", F_NUM1, "Opening NIBD less the change in NIBD must equal the balance sheet"),
        ("No Excel errors in calculation sheets",
         "=SUMPRODUCT(--ISERROR(Hist!E7:K180))+SUMPRODUCT(--ISERROR(Drivers!E7:V120))+SUMPRODUCT(--ISERROR(Model!E7:T250))"
         "+SUMPRODUCT(--ISERROR(Output!E7:T160))+SUMPRODUCT(--ISERROR(Analysis!E7:T160))"
         "+SUMPRODUCT(--ISERROR(DCF!E7:T160))+SUMPRODUCT(--ISERROR(WACC!C4:M30))+SUMPRODUCT(--ISERROR(Comps!C6:S40))"
         "+SUMPRODUCT(--ISERROR(Sensitivity!C12:AE90))+SUMPRODUCT(--ISERROR(Football!C5:F17))"
         "+SUMPRODUCT(--ISERROR(Reverse_DCF!C5:K135))+SUMPRODUCT(--ISERROR(Consensus!C5:K50))+SUMPRODUCT(--ISERROR(Thesis!C5:K40))",
         "x=0", "Error", F_INT, "Find the #-error and fix its inputs (often a blank or zero denominator)"),
        ("WACC above terminal growth", f"={D('s_wg')}", "x>0", "Error", F_PCT2, "Gordon growth requires WACC > g"),
        ("Terminal growth at most 3%", f"={D('tv_g')}", "x<=0.03", "Warning", F_PCT2, "Long-run growth above nominal GDP is hard to defend"),
        ("Terminal value at most 80% of EV", f"={D('tv_share')}", "x<=0.8", "Warning", F_PCT, "Extend the forecast or revisit terminal assumptions"),
        ("RONIC at least WACC", f"={D('s_spread')}", "x>=0", "Warning", F_PCT2, "Growth destroys value if RONIC < WACC – deliberate?"),
        ("Stub fraction between 0% and 100%", f"={I('stub')}", "and(x>=0,x<=1)", "Error", F_PCT, "Valuation date must be in the first forecast year"),
        ("Weights between 0% and 100%", f"=MIN({I('w_gordon')},{I('w_dcf')},1-{I('w_gordon')},1-{I('w_dcf')})", "x>=0", "Error", F_PCT,
         "Terminal value and target price weights on Inputs"),
        ("Sensitivity centre equals DCF value", f"=ABS({S('Sensitivity', 'center1')}-{D('dcf_ps')})", "x<0.01", "Error", F_NOK,
         "Closed-form sensitivity must reproduce the model value"),
        ("Data-table input cells are blank", "=COUNT(Sensitivity!$D$4:$D$6)", "x=0", "Error", F_INT, "Clear cells D4:D6 on the Sensitivity sheet"),
        ("Scenario probabilities sum to 100%", f"={S('Drivers', 'adj_prob')}", "abs(x-1)<0.0001", "Error", F_PCT, "Drivers sheet, section B"),
        ("PP&E stays positive in the forecast", f"=MIN(Model!L{mr('ppe')}:S{mr('ppe')})", "x>0", "Error", F_NUM,
         "Capex too low relative to D&A"),
        ("Share price and share count positive", f"=MIN({I('price')},{I('shares')})", "x>0", "Error", F_NOK, "Inputs sheet"),
        ("Implied exit multiple within peer EV/EBITDA range", f"={D('s_exit')}",
         f"and(x>=Comps!$J${CR['low']}*0.8,x<=Comps!$J${CR['high']}*1.2)", "Warning", F_MULT,
         "Implied multiple is EV/EBITDAaL (pre-IFRS 16) – compare with care"),
        ("DCF within ±30% of peer multiples value", f"={D('tp_dcf')}/{S('Comps', 'peer_val')}-1", "abs(x)<=0.3", "Warning", F_PCT,
         "Large gaps need an explanation in the pitch"),
        ("Growth is paid for: return on new capital (explicit period) vs. today's ROIC", f"={D('s_ronic_ratio')}",
         f"x<={I('ronic_tol')}", "Warning", F_MULT,
         "Growth is almost free in the forecast – check growth capex (capex per new location or sales-to-capital), "
         "maintenance capex vs. D&A and NWC on Drivers"),
        ("Net reinvestment positive in every year with revenue growth",
         f"=SUMPRODUCT((Model!L{mr('grev')}:S{mr('grev')}>0)*(Model!L{mr('net_inv')}:S{mr('net_inv')}<0))", "x=0", "Warning", F_INT,
         "Number of forecast years in which revenue grows while net investment is negative"),
        ("WACC capital structure consistent with the forecast balance sheet",
         f"=ABS({S('WACC', 'dv')}-{S('WACC', 'dv_model')})", "x<=0.10", "Warning", F_PCT,
         "D/(D+E) in the WACC is more than 10pp from the modelled average – use the modelled basis (WACC sheet) or change leverage / buybacks (Drivers E)"),
        ("Locations positive in every forecast year", f"=MIN(Model!L{mr('loc')}:S{mr('loc')})", "x>0", "Error", F_NUM,
         "Net new locations on Drivers (section A) close more locations than exist"),
        ("Ramp-up curve between 0% and 100% and rising",
         f"=IF(AND({S('Drivers', 'ramp1')}>=0,{S('Drivers', 'ramp1')}<={S('Drivers', 'ramp2')},"
         f"{S('Drivers', 'ramp2')}<={S('Drivers', 'ramp3')},{S('Drivers', 'ramp3')}<=1),1,0)", "x=1", "Error", F_INT,
         "Drivers, section F"),
        ("Utilisation: volume per mature location vs. the historical peak (location mode)",
         f"=IF({I('rev_mode')}=2,MAX(" + ",".join(
             f"MAX(Model!L{mr(f'mpl_{x}')}:S{mr(f'mpl_{x}')})/MAX(Model!E{mr(f'mpl_{x}')}:K{mr(f'mpl_{x}')})" for x in "abc")
         + ")-1,0)", f"x<={I('util_tol')}", "Warning", F_PCT,
         "Like-for-like growth fills locations far beyond anything seen historically – add openings or lower like-for-like growth"),
        ("Reverse DCF solved for all market-implied drivers",
         f"={len(RD_ROWS)}-COUNT(Reverse_DCF!$C${RD_ROWS['m_last']}:$C${RD_ROWS['g']})", "x=0", "Warning", F_INT,
         "The share price is outside a solver range – see the Reverse_DCF sheet (press F9 to refresh Sensitivity table 5)"),
        ("Thesis tracker: no kill criterion breached on the latest actuals", f"={S('Thesis', 'n_broken')}", "x=0", "Warning", F_INT,
         "A kill criterion is breached – revisit the investment case (Thesis sheet)"),
        ("Base case consistent with its own kill criteria", f"={S('Thesis', 'n_incons')}", "x=0", "Warning", F_INT,
         "Our base case breaches a kill criterion next year – change the forecast or the threshold (Thesis sheet)"),
        ("Active scenario is Base (for the pitch)", f"={I('scenario')}", 'x="Base"', "Info", F_GEN, "Switch back to Base before copying numbers to the deck"),
    ]


def _cond(expr, cell):
    return "=" + expr.replace("x", cell).replace("abs(", "ABS(").replace("and(", "AND(")


def write_checks(wb):
    ws = wb["Checks"]
    sheet_title(ws, "Model integrity checks", "Errors must be fixed. Warnings must be understood (and ideally explained in the pitch).",
                company_ref=False, last_col="G")
    for k, v in dict(A=2, B=5, C=48, D=13, E=12, F=10, G=70).items():
        ws.column_dimensions[k].width = v
    checks = check_list()
    n = len(checks)
    last = CHK0 + n - 1
    put(ws, "C3", "Overall status", kind="label", bold=True, size=11)
    put(ws, "D3", f'=IF(COUNTIF(E{CHK0}:E{last},"ERROR")>0,COUNTIF(E{CHK0}:E{last},"ERROR")&" ERROR(S)",'
                  f'IF(COUNTIF(E{CHK0}:E{last},"WARNING")>0,"OK – "&COUNTIF(E{CHK0}:E{last},"WARNING")&" WARNING(S)","ALL CHECKS OK"))',
        bold=True, size=11)
    CELLS[("Checks", "master")] = "D3"
    put(ws, "C4", "Errors / warnings", kind="label")
    put(ws, "D4", f'=COUNTIF(E{CHK0}:E{last},"ERROR")&" / "&COUNTIF(E{CHK0}:E{last},"WARNING")', align="right")
    for c, txt in zip("BCDEFG", ["#", "Check", "Value", "Status", "Type", "What to do if it fails"]):
        put(ws, f"{c}{CHK0 - 1}", txt, kind="label", bold=True, color=WHITE, fill=NAVY)
    for j, (lab, val, cond, typ, fmt, todo) in enumerate(checks):
        r = CHK0 + j
        put(ws, f"B{r}", j + 1, kind="calc", fmt=F_INT, align="center")
        put(ws, f"C{r}", lab, kind="label")
        put(ws, f"D{r}", val, fmt=fmt, align="right")
        ok = _cond(cond, f"D{r}")[1:]
        bad = "ERROR" if typ == "Error" else ("WARNING" if typ == "Warning" else "INFO")
        put(ws, f"E{r}", f'=IF(ISERROR(D{r}),"ERROR",IF({ok},"OK","{bad}"))', bold=True, align="center")
        put(ws, f"F{r}", typ, kind="note")
        put(ws, f"G{r}", todo, kind="note", italic=True)
    rng = f"E{CHK0}:E{last}"
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"OK"'], fill=PatternFill("solid", fgColor=OKGREEN)))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"ERROR"'], fill=PatternFill("solid", fgColor=ERRRED)))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"WARNING"'], fill=PatternFill("solid", fgColor=WARNAMB)))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"INFO"'], fill=PatternFill("solid", fgColor=PALE)))
    ws.conditional_formatting.add("D3", FormulaRule(formula=['ISNUMBER(SEARCH("ERROR",$D$3))'], fill=PatternFill("solid", fgColor=ERRRED)))
    ws.conditional_formatting.add("D3", FormulaRule(formula=['NOT(ISNUMBER(SEARCH("ERROR",$D$3)))'], fill=PatternFill("solid", fgColor=OKGREEN)))
    ws.freeze_panes = f"A{CHK0}"


# ============================================================ charts
def _style_axes(ch):
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    if ch.legend is not None:
        ch.legend.position = "t"


def chart_rev_margin(ws, anchor):
    mr = ROWS[("Model", "is_rev")]
    mm = ROWS[("Model", "ebit_adj_m")]
    m = ws.parent["Model"]
    bar = BarChart()
    bar.type, bar.grouping = "col", "clustered"
    data = Reference(m, min_col=5, max_col=19, min_row=mr, max_row=mr)
    cats = Reference(m, min_col=5, max_col=19, min_row=5, max_row=5)
    bar.add_data(data, from_rows=True, titles_from_data=False)
    bar.set_categories(cats)
    bar.series[0].tx = None
    from openpyxl.chart.series import SeriesLabel
    bar.series[0].tx = SeriesLabel(v="Revenue")
    bar.series[0].graphicalProperties.solidFill = NAVY
    bar.gapWidth = 60
    line = LineChart()
    line.add_data(Reference(m, min_col=5, max_col=19, min_row=mm, max_row=mm), from_rows=True, titles_from_data=False)
    line.series[0].tx = SeriesLabel(v="EBIT adj. margin (rhs)")
    line.series[0].smooth = False
    line.series[0].graphicalProperties.line.solidFill = LBLUE
    line.series[0].graphicalProperties.line.width = 28000
    line.y_axis.axId = 200
    line.y_axis.number_format = "0%"
    line.y_axis.crosses = "max"
    line.y_axis.majorGridlines = None
    line.y_axis.delete = False
    bar.y_axis.number_format = "#,##0"
    bar.y_axis.majorGridlines = None
    _style_axes(bar)
    bar += line
    bar.height, bar.width = 7.5, 16
    ws.add_chart(bar, anchor)


def chart_fcff_roic(ws, anchor):
    fr = ROWS[("Model", "fcff")]
    rr = ROWS[("Model", "roic")]
    m = ws.parent["Model"]
    from openpyxl.chart.series import SeriesLabel
    bar = BarChart()
    bar.type = "col"
    bar.add_data(Reference(m, min_col=6, max_col=19, min_row=fr, max_row=fr), from_rows=True, titles_from_data=False)
    bar.set_categories(Reference(m, min_col=6, max_col=19, min_row=5, max_row=5))
    bar.series[0].tx = SeriesLabel(v="FCFF")
    bar.series[0].graphicalProperties.solidFill = LBLUE
    bar.gapWidth = 60
    line = LineChart()
    line.add_data(Reference(m, min_col=6, max_col=19, min_row=rr, max_row=rr), from_rows=True, titles_from_data=False)
    line.series[0].tx = SeriesLabel(v="ROIC (rhs)")
    line.series[0].smooth = False
    line.series[0].graphicalProperties.line.solidFill = NAVY
    line.series[0].graphicalProperties.line.width = 28000
    line.y_axis.axId = 200
    line.y_axis.number_format = "0%"
    line.y_axis.crosses = "max"
    line.y_axis.majorGridlines = None
    line.y_axis.delete = False
    bar.y_axis.number_format = "#,##0"
    bar.y_axis.majorGridlines = None
    _style_axes(bar)
    bar += line
    bar.height, bar.width = 7.5, 16
    ws.add_chart(bar, anchor)


def chart_football(ws, anchor):
    from openpyxl.chart.series import SeriesLabel
    from openpyxl.chart.marker import DataPoint
    from mb_val import FB_CHART
    f = ws.parent["Football"]
    r0, r1 = FB_CHART
    ch = BarChart()
    ch.type, ch.grouping, ch.overlap = "bar", "stacked", 100
    ch.add_data(Reference(f, min_col=10, max_col=10, min_row=r0, max_row=r1), titles_from_data=False)
    ch.add_data(Reference(f, min_col=11, max_col=11, min_row=r0, max_row=r1), titles_from_data=False)
    ch.set_categories(Reference(f, min_col=9, max_col=9, min_row=r0, max_row=r1))
    ch.series[0].tx = SeriesLabel(v="Offset")
    ch.series[0].graphicalProperties.noFill = True
    ch.series[0].graphicalProperties.line.noFill = True
    ch.series[1].tx = SeriesLabel(v="Range")
    ch.series[1].graphicalProperties.solidFill = NAVY
    n = r1 - r0 + 1
    for idx, col in [(n - 3, "C00000"), (n - 2, "2E7D32"), (n - 1, LBLUE)]:
        pt = DataPoint(idx=idx)
        pt.graphicalProperties.solidFill = col
        pt.graphicalProperties.line.solidFill = col
        ch.series[1].dPt.append(pt)
    ch.gapWidth = 45
    ch.x_axis.scaling.orientation = "maxMin"
    ch.x_axis.delete = False
    ch.y_axis.delete = True
    ch.y_axis.majorGridlines = None
    ch.legend = None
    ch.height, ch.width = 7.5, 16
    ws.add_chart(ch, anchor)


def chart_scenarios(ws, anchor):
    s = ws.parent["Sensitivity"]
    from openpyxl.utils import column_index_from_string as ci
    from openpyxl.chart.series import SeriesLabel
    col = ci(t4_col("dcf_ps"))
    r0, r1 = SENS["t4_rows"]
    ch = BarChart()
    ch.type = "col"
    ch.add_data(Reference(s, min_col=col, max_col=col, min_row=r0, max_row=r1), titles_from_data=False)
    ch.set_categories(Reference(s, min_col=2, max_col=2, min_row=r0, max_row=r1))
    ch.series[0].tx = SeriesLabel(v="DCF value per share")
    ch.series[0].graphicalProperties.solidFill = NAVY
    ch.series[0].dLbls = DataLabelList()
    ch.series[0].dLbls.showVal = True
    ch.series[0].dLbls.showSerName = False
    ch.series[0].dLbls.showCatName = False
    ch.series[0].dLbls.showLegendKey = False
    ch.series[0].dLbls.showPercent = False
    ch.series[0].dLbls.numFmt = "0"
    ch.y_axis.number_format = "0"
    ch.y_axis.majorGridlines = None
    _style_axes(ch)
    ch.legend = None
    ch.gapWidth = 80
    ch.height, ch.width = 7.5, 16
    ws.add_chart(ch, anchor)


# ============================================================ DASHBOARD
DASH_YEARS = HC[4:] + FC[:5]          # 2023A..2030E (3 hist + 5 fc) -> 8 columns


def write_dashboard(wb):
    ws = wb["Dashboard"]
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 85
    for k, v in dict(A=2, B=34, C=3, D=14, E=3, F=30).items():
        ws.column_dimensions[k].width = v
    for c in "GHIJKLMN":
        ws.column_dimensions[c].width = 10
    put(ws, "B1", f'={I("company")}&" ("&{I("ticker")}&") – equity research summary"', bold=True, size=15, color=TITLE)
    ws.row_dimensions[1].height = 24
    vd = I("val_date")
    put(ws, "B2", f'="Valuation date "&TEXT(DAY({vd}),"00")&"."&TEXT(MONTH({vd}),"00")&"."&YEAR({vd})&"  |  Scenario: "&{I("scenario")}&"  |  Figures in "&{I("unit")}',
        italic=True, color=GREY)
    band(ws, 4, "B", "D", "Investment summary")
    items = [
        ("Recommendation", f"={D('rating')}", F_GEN),
        ("Target price (NOK)", f"={D('tp')}", F_NOK),
        ("Share price (NOK)", f"={I('price')}", F_NOK),
        ("Upside to target price", f"={D('tp_up')}", F_PCT),
        ("Expected total return (incl. dividend)", f"={D('tp_tr')}", F_PCT),
        ("Excess return vs. cost of equity", f"={D('tp_excess')}", F_PCT),
        ("DCF value per share (NOK)", f"={D('dcf_ps')}", F_NOK),
        ("Peer multiples value per share (NOK)", f"={S('Comps', 'peer_val')}", F_NOK),
        ("Blended fair value per share (NOK)", f"={D('tp_fair')}", F_NOK),
        ("Probability-weighted DCF value (NOK)", f"={S('Sensitivity', 'pw_dcf_ps')}", F_NOK),
        ("Market capitalisation (NOKm)", f"={I('mcap')}", F_NUM),
        ("Enterprise value, excl. leases (NOKm)", f"={I('ev_ex')}", F_NUM),
        ("WACC", f"={S('WACC', 'wacc')}", F_PCT2),
        ("Terminal growth", f"={D('tv_g')}", F_PCT2),
        ("Terminal value share of DCF EV", f"={D('tv_share')}", F_PCT),
        ("Implied exit multiple (EV/EBITDAaL)", f"={D('s_exit')}", F_MULT),
        ("Market-implied EBIT adj. margin, final year", f"={S('Reverse_DCF', 'rd_m_last')}", F_PCT),
        ("EBIT (reported) vs. consensus, second forecast year", f"={S('Consensus', 'diff_ebit_2')}", '+0.0%;-0.0%;0.0%'),
        ("Model checks", f"={S('Checks', 'master')}", F_GEN),
    ]
    for j, (lab, f, fmt) in enumerate(items):
        r = 5 + j
        put(ws, f"B{r}", lab, kind="label", bold=j == 0)
        put(ws, f"D{r}", f, fmt=fmt, bold=j in (0, 1, 3), align="right")
        bottom_border(ws, r, "B", "D")
    ws["D5"].font = Font(name=FONT, size=12, bold=True, color=WHITE)
    ws["D5"].fill = PatternFill("solid", fgColor=NAVY)
    ws["D5"].alignment = Alignment(horizontal="center")
    ws.conditional_formatting.add("D5", FormulaRule(formula=['$D$5="BUY"'], fill=PatternFill("solid", fgColor="2E7D32")))
    ws.conditional_formatting.add("D5", FormulaRule(formula=['$D$5="HOLD"'], fill=PatternFill("solid", fgColor="B7950B")))
    ws.conditional_formatting.add("D5", FormulaRule(formula=['$D$5="SELL"'], fill=PatternFill("solid", fgColor="C62828")))
    ck = 4 + len(items)
    ws.conditional_formatting.add(f"D{ck}", FormulaRule(formula=[f'ISNUMBER(SEARCH("ERROR",$D${ck}))'],
                                                        fill=PatternFill("solid", fgColor=ERRRED)))

    band(ws, 4, "F", "N", "Key financials")
    put(ws, "F5", f'={I("unit")}', kind="calc", italic=True, color=GREY)
    for c, mc in zip("GHIJKLMN", DASH_YEARS):
        put(ws, f"{c}5", f"=Model!{mc}5", bold=True, align="right",
            fill=FCFILL if mc in FC else None)
    bottom_border(ws, 5, "F", "N", MED)
    lines = [("Revenue", "is_rev", F_NUM, True), ("  growth", "grev", F_PCT, False),
             ("EBITDA (reported)", "ebitda", F_NUM, True), ("  margin", "ebitda_m", F_PCT, False),
             ("EBIT adj.", "ebit_adj", F_NUM, True), ("  margin", "ebit_adj_m", F_PCT, False),
             ("Net profit to shareholders", "np_sh", F_NUM, True), ("EPS (NOK)", "eps", F_NOK, False),
             ("DPS (NOK)", "dps", F_NOK, False), ("FCFF", "fcff", F_NUM, True), ("ROIC", "roic", F_PCT, False),
             ("NIBD / EBITDAaL (x)", "lev", F_MULT, False), ("P / E (x)", "pe", F_MULT, False),
             ("EV / EBITDA (x)", "evebitda", F_MULT, False)]
    for j, (lab, key, fmt, bold) in enumerate(lines):
        r = 6 + j
        put(ws, f"F{r}", lab, kind="label", bold=bold, italic=lab.startswith("  "))
        for c, mc in zip("GHIJKLMN", DASH_YEARS):
            put(ws, f"{c}{r}", "=" + MREF(key, mc), fmt=fmt, bold=bold, italic=lab.startswith("  "))
    put(ws, "F21", "Charts below update automatically. Revenue/EBIT and FCFF/ROIC cover the full history and forecast.",
        kind="note", italic=True)
    for addr, txt in [("B26", "Revenue (NOKm) and EBIT adj. margin"), ("H26", "Free cash flow to firm (NOKm) and ROIC"),
                      ("B44", "Valuation range (NOK per share)"), ("H44", "DCF value per share by scenario (NOK)")]:
        put(ws, addr, txt, kind="label", bold=True, color=NAVY, size=10)
    chart_rev_margin(ws, "B27")
    chart_fcff_roic(ws, "H27")
    chart_football(ws, "B45")
    chart_scenarios(ws, "H45")


# ============================================================ DECK FEED
FEED_KEYS = []   # (key, label, formula, fmt, text_fmt)


def write_feed(wb):
    ws = wb["Deck_Feed"]
    sheet_title(ws, "Deck feed – numbers ready for the pitch deck",
                "Copy these cells into PowerPoint (Paste Special > Keep text only) after the final model run.",
                company_ref=False, last_col="N")
    for k, v in dict(A=2, B=44, C=14, D=58, E=3, F=30).items():
        ws.column_dimensions[k].width = v
    for c in "GHIJKLMN":
        ws.column_dimensions[c].width = 10
    mr = lambda k, c: MREF(k, c)
    keys = [
        ("rating_line", "Headline", f'="We initiate with a "&{D("rating")}&" and a target price of NOK "&FIXED({D("tp")},0)&" ("&TEXT({D("tp_up")},"+0%;-0%")&" upside)"', F_GEN),
        ("rating_box", "Recommendation box", f'={D("rating")}&" – TP NOK "&FIXED({D("tp")},0)', F_GEN),
        ("val_split", "Target price build-up", f'="TP based on "&FIXED({I("w_dcf")}*100,0)&"% DCF (NOK "&FIXED({D("tp_dcf")},0)&") and "&FIXED({I("w_peers")}*100,0)&"% peer multiples (NOK "&FIXED({D("tp_peer")},0)&"), rolled forward 12 months"', F_GEN),
        ("dcf_line", "DCF summary", f'="DCF value NOK "&FIXED({D("dcf_ps")},0)&" per share (WACC "&FIXED({S("WACC", "wacc")}*100,1)&"%, g "&FIXED({D("tv_g")}*100,1)&"%)"', F_GEN),
        ("snapshot", "Market snapshot", f'="Share price NOK "&FIXED({I("price")},1)&" | Market cap NOKm "&FIXED({I("mcap")},0)&" | EV NOKm "&FIXED({I("ev_ex")},0)', F_GEN),
        ("company", "Company", f"={I('company')}", F_GEN),
        ("ticker", "Ticker", f"={I('ticker')}", F_GEN),
        ("rating", "Recommendation", f"={D('rating')}", F_GEN),
        ("tp", "Target price (NOK)", f"={D('tp')}", F_NOK),
        ("tp_up", "Upside to target price", f"={D('tp_up')}", F_PCT),
        ("tp_tr", "Expected total return", f"={D('tp_tr')}", F_PCT),
        ("tp_excess", "Excess return vs. cost of equity", f"={D('tp_excess')}", F_PCT),
        ("price", "Share price (NOK)", f"={I('price')}", F_NOK),
        ("mcap", "Market cap (NOKm)", f"={I('mcap')}", F_NUM),
        ("ev_ex", "EV excl. leases (NOKm)", f"={I('ev_ex')}", F_NUM),
        ("nibd", "NIBD excl. leases (NOKm)", f"={I('nibd')}", F_NUM),
        ("dcf_ps", "DCF value per share (NOK)", f"={D('dcf_ps')}", F_NOK),
        ("peer_val", "Peer value per share (NOK)", f"={S('Comps', 'peer_val')}", F_NOK),
        ("fair", "Blended fair value (NOK)", f"={D('tp_fair')}", F_NOK),
        ("pw_dcf", "Probability-weighted DCF value (NOK)", f"={S('Sensitivity', 'pw_dcf_ps')}", F_NOK),
        ("wacc", "WACC", f"={S('WACC', 'wacc')}", F_PCT2),
        ("ke", "Cost of equity", f"={S('WACC', 'ke')}", F_PCT2),
        ("tg", "Terminal growth", f"={D('tv_g')}", F_PCT2),
        ("tv_share", "Terminal value share of EV", f"={D('tv_share')}", F_PCT),
        ("exit_impl", "Implied exit multiple", f"={D('s_exit')}", F_MULT),
        ("rev_cagr", "Revenue CAGR, last actual to 5th forecast year",
         f"=({mr('is_rev', FC[4])}/{mr('is_rev', HC[-1])})^(1/5)-1", F_PCT),
        ("ebit_m_last", "EBIT adj. margin, last actual year", f"={mr('ebit_adj_m', HC[-1])}", F_PCT),
        ("ebit_m_f5", "EBIT adj. margin, 5th forecast year", f"={mr('ebit_adj_m', FC[4])}", F_PCT),
        ("roic_f3", "ROIC, 3rd forecast year", f"={mr('roic', FC[2])}", F_PCT),
        ("pe_f1", "P/E, first forecast year", f"={mr('pe', FC[0])}", F_MULT),
        ("evebit_f2", "EV/EBIT, second forecast year", f"={mr('evebit', FC[1])}", F_MULT),
        ("dy_f1", "Dividend yield, first forecast year", f"={mr('div_yield', FC[0])}", F_PCT),
        ("market_line", "Reverse DCF – headline", f"={S('Reverse_DCF', 'rd_line1')}", F_GEN),
        ("rd_m_last", "Market-implied EBIT adj. margin, final year", f"={S('Reverse_DCF', 'rd_m_last')}", F_PCT),
        ("rd_cagr", "Market-implied revenue CAGR", f"={S('Reverse_DCF', 'rd_cagr')}", F_PCT),
        ("rd_wacc", "Market-implied WACC", f"={S('Reverse_DCF', 'rd_wacc')}", F_PCT2),
        ("cons_ebit_2", "EBIT (reported) vs. consensus, second forecast year", f"={S('Consensus', 'diff_ebit_2')}", F_PCT),
        ("cons_eps_2", "EPS vs. consensus, second forecast year", f"={S('Consensus', 'diff_eps_2')}", F_PCT),
    ]
    band(ws, 3, "B", "D", "A. Key numbers and text lines")
    for j, (k, lab, f, fmt) in enumerate(keys):
        r = 4 + j
        CELLS[("Deck_Feed", k)] = f"C{r}"
        put(ws, f"B{r}", lab, kind="label")
        if fmt == F_GEN and (j < 5 or k == "market_line"):
            put(ws, f"C{r}", f, fmt=fmt, wrap=False)
            ws.merge_cells(f"C{r}:D{r}")
        else:
            put(ws, f"C{r}", f, fmt=fmt, align="right")
    # B. financial summary table (same as Dashboard)
    band(ws, 3, "F", "N", "B. Financial summary (copy to 'Financials and estimates')")
    for c, mc in zip("GHIJKLMN", DASH_YEARS):
        put(ws, f"{c}4", f"=Model!{mc}5", bold=True, align="right")
    rows = [("Revenue", "is_rev", F_NUM), ("Growth", "grev", F_PCT), ("EBITDA", "ebitda", F_NUM),
            ("EBITDA margin", "ebitda_m", F_PCT), ("EBIT adj.", "ebit_adj", F_NUM), ("EBIT adj. margin", "ebit_adj_m", F_PCT),
            ("Net profit", "np_sh", F_NUM), ("EPS (NOK)", "eps", F_NOK), ("DPS (NOK)", "dps", F_NOK),
            ("FCFF", "fcff", F_NUM), ("ROIC", "roic", F_PCT), ("NIBD / EBITDAaL", "lev", F_MULT),
            ("EV / Sales", "evs", F_MULT2), ("EV / EBITDA", "evebitda", F_MULT), ("EV / EBIT", "evebit", F_MULT),
            ("P / E", "pe", F_MULT), ("FCF yield", "fcf_yield", F_PCT), ("Dividend yield", "div_yield", F_PCT)]
    for j, (lab, key, fmt) in enumerate(rows):
        r = 5 + j
        put(ws, f"F{r}", lab, kind="label")
        for c, mc in zip("GHIJKLMN", DASH_YEARS):
            put(ws, f"{c}{r}", "=" + MREF(key, mc), fmt=fmt)
    put(ws, "F24", "Multiples are at the current share price.", kind="note", italic=True)


# ============================================================ COVER & GUIDE
SHEETS_INFO = [
    ("Cover", "This page – contents, status and colour legend"),
    ("Guide", "Step-by-step guide, method notes and how to map Pareto case data"),
    ("Inputs", "Company info, timeline, market data, net debt bridge and valuation settings"),
    ("Hist", "Historical income statement, balance sheet, cash flow, KPIs and ratios"),
    ("Drivers", "Base case drivers per year, Bear/Bull adjustments and terminal assumptions"),
    ("Model", "Revenue build (volume x price), P&L, invested capital, net debt and multiples"),
    ("WACC", "CAPM, peer beta (unlevered/relevered), cost of debt and WACC"),
    ("DCF", "FCFF, discounting with stub/mid-year, terminal value, EV-to-equity bridge, target price"),
    ("Sensitivity", "WACC/growth, WACC/exit multiple, growth/margin and Bear/Base/Bull tables"),
    ("Comps", "Peer multiples, statistics and implied valuation"),
    ("Football", "Valuation summary – football field data"),
    ("Dashboard", "One-page summary with charts"),
    ("Deck_Feed", "Numbers and text lines ready for the pitch deck"),
    ("Checks", "Integrity checks – fix all errors before submitting"),
]


def write_cover(wb):
    ws = wb["Cover"]
    ws.sheet_view.showGridLines = False
    for k, v in dict(A=3, B=22, C=70, D=3, E=18, F=30).items():
        ws.column_dimensions[k].width = v
    band(ws, 2, "B", "F", "EQUITY RESEARCH TOOLKIT", size=10)
    ws.row_dimensions[3].height = 34
    put(ws, "B3", "DCF valuation model", kind="label", bold=True, size=24, color=NAVY)
    put(ws, "B4", f'={I("company")}&"  ("&{I("ticker")}&", "&{I("exchange")}&")"', bold=True, size=14)
    put(ws, "B5", f'={D("rating")}&"  |  Target price NOK "&TEXT({D("tp")},"0")&"  |  "&TEXT({D("tp_up")},"+0%;-0%")&" upside  |  Scenario: "&{I("scenario")}',
        size=12, color=NAVY)
    put(ws, "B6", f'="Model status: "&{S("Checks", "master")}', bold=True, size=10)
    ws.conditional_formatting.add("B6", FormulaRule(formula=['ISNUMBER(SEARCH("ERROR",$B$6))'], fill=PatternFill("solid", fgColor=ERRRED)))
    ws.conditional_formatting.add("B6", FormulaRule(formula=['NOT(ISNUMBER(SEARCH("ERROR",$B$6)))'], fill=PatternFill("solid", fgColor=OKGREEN)))
    put(ws, "B7", ex.MARKET.get("data_note", "All company data in this file is FICTIONAL example data. Replace the blue input cells with your case data."),
        kind="note", italic=True, color="C00000")
    band(ws, 9, "B", "C", "Contents (click to open)")
    for j, (name, desc) in enumerate(SHEETS_INFO):
        r = 10 + j
        c = put(ws, f"B{r}", name, kind="label", bold=True, color="0563C1")
        c.hyperlink = f"#'{name}'!A1"
        put(ws, f"C{r}", desc, kind="note")
    band(ws, 9, "E", "F", "Colour legend")
    legend = [("1,234", "input", "Input – hard-coded number (blue on yellow)"),
              ("1,234", "calc", "Formula on the same sheet (black)"),
              ("1,234", "link", "Direct link to another sheet (green)"),
              ("1,234", "fc", "Forecast column (light blue background)"),
              ("1,234", "ty", "Terminal year / key output (pale blue)")]
    for j, (v, kind, txt) in enumerate(legend):
        r = 10 + j
        if kind == "fc":
            put(ws, f"E{r}", v, kind="calc", fill=FCFILL, align="center")
        elif kind == "ty":
            put(ws, f"E{r}", v, kind="calc", fill=PALE, align="center")
        else:
            put(ws, f"E{r}", v, kind=kind, align="center")
        put(ws, f"F{r}", txt, kind="note")
    put(ws, "E16", "Sign convention: income positive, costs negative.", kind="note", italic=True)
    put(ws, "E17", "Units: NOKm unless stated; per-share figures in NOK.", kind="note", italic=True)
    put(ws, "B26", "Version 1.0 – built September 2026. Recalculate fully (Ctrl+Alt+F9) after pasting new data.",
        kind="note", italic=True)


GUIDE = [
    ("h", "How to use the model – 8 steps"),
    ("1", "Inputs: company name, ticker, first historical year, valuation date, share price, shares, and net debt from the latest quarterly report."),
    ("2", "Hist: paste seven years of reported figures. Costs are negative numbers. Map Pareto's 'Model' sheet lines using the table below."),
    ("3", "Check the Hist balance check and cash flow check rows (should be zero) before moving on."),
    ("4", "Choose the revenue build on Inputs (1 = segments, 2 = locations). Drivers (section A): price/mix growth per segment, then either volume growth (segment mode) or like-for-like growth, net new locations and capex per new location (location mode); the variable cost ratios, cost inflation, maintenance capex, NWC and tax per year. Rows the active build does not use are greyed out."),
    ("5", "Drivers (section B/D/E/F): Bear/Bull adjustments and probabilities, terminal assumptions (g, RONIC, exit multiple), the fixed and central share of costs, capital allocation (target leverage, buybacks) and the ramp-up curve for new locations."),
    ("6", "WACC: update risk-free rate, equity risk premium and peer betas. Comps: paste the peer table from the case material."),
    ("7", "Review Output (the balance sheet and cash flow checks must be zero), Analysis, Dashboard, Sensitivity and Football. Resolve every ERROR on Checks and be ready to explain each WARNING."),
    ("8", "Set the scenario back to Base, then copy numbers from Deck_Feed into the pitch deck."),
    ("", ""),
    ("h", "How the workbook is organised"),
    ("•", "Inputs >>> (Inputs, Hist, Drivers) is the only place you type. Calculations >>> (Model) is the engine. Output >>> (Output, Analysis) presents the results link-only. Valuation >>> (WACC, DCF, Sensitivity, Comps, Football) values the company. Summary >>> (Dashboard, Deck_Feed, Checks) wraps it up."),
    ("•", "Blue = hard-coded input, blue on yellow = forecast assumption or switch, black = formula, green = link to another sheet, light blue row = key line, grey italic = check."),
    ("", ""),
    ("h", "Method notes"),
    ("•", "FCFF is on a pre-IFRS 16 basis: lease payments are treated as operating costs (EBITDAaL). Lease liabilities are therefore NOT deducted in the equity bridge. This avoids the classic mismatch of IFRS 16 EBITDA margins in history vs. pre-IFRS 16 margins in the forecast."),
    ("•", "Stub period: only the remaining share of the first forecast year is valued; cash flows are discounted from the valuation date (mid-year convention optional)."),
    ("•", "Terminal value uses the value-driver formula: FCFF = NOPAT x (1 – g / RONIC). This forces reinvestment consistent with growth. With RONIC = WACC, growth adds no value."),
    ("•", "Growth is paid for: capex = maintenance capex + growth capex. Location mode: openings x capex per new location; segment mode: incremental revenue / sales-to-capital. The DCF sanity checks compare the return on new capital in the explicit period with the higher of today's ROIC and the terminal RONIC – a forecast that grows almost for free is flagged."),
    ("•", "Location engine (revenue build 2): volume = mature-equivalent locations x volume per mature location. New locations ramp up over three years (Drivers F); volume per location grows with like-for-like growth. Fixed costs grow with inflation and the number of locations (except the central share) and rent per location grows with inflation – so openings dilute margins at first and add to them as they mature."),
    ("•", "Operating leverage is a result, not an input: personnel and other opex are split into a fixed part (grows with cost inflation and capacity) and a variable part (% of revenue). Margin expansion therefore follows from the growth you assume."),
    ("•", "Capital structure: the WACC uses either a target D/(D+E) or the average modelled from the forecast balance sheet. With the buyback switch on, cash above the target leverage is returned so the forecast structure stays close to the WACC assumption; a gap above 10pp is flagged."),
    ("•", "Target price = blended fair value (DCF and peers) rolled forward 12 months at the cost of equity, less the expected dividend. Rating: BUY only if the expected total return exceeds the cost of equity by the threshold on Inputs – a fairly priced share returns Ke, not zero."),
    ("•", "The football field shows values today (fair value marker). The 12-month target price is drawn separately because it is rolled forward at the cost of equity and is not comparable with the ranges."),
    ("•", "Reverse_DCF solves the DCF for today's share price: the EBIT margin (exact closed form – the DCF is linear in a uniform margin shift), growth (interpolated in Sensitivity table 5, a data table), WACC and terminal growth (bisection on the closed-form DCF). Use it to say what the market prices in – and where you differ."),
    ("•", "Consensus: type the latest consensus (reported IFRS 16 basis) and your variant perception – topic, our view, consensus view, evidence and the catalyst that proves it. Thesis: scenario stories and kill criteria with a live status on the latest actuals."),
    ("•", "Sensitivity tables 1-2 are live formulas. Tables 3-4 are Excel data tables – if they look stale, press F9 (File > Options > Formulas > Automatic)."),
    ("•", "Interest in the forecast is calculated on opening net debt, so the model has no circular references."),
    ("", ""),
    ("h", "Mapping Pareto case data ('Model' sheet) to Hist"),
    ("map", "Revenues / Membership fees / Other | Revenue – segment A/B/C (use A only if there is no split)"),
    ("map", "COGS | Cost of goods sold (negative)"),
    ("map", "Salaries and personnel costs | Personnel expenses (negative)"),
    ("map", "Other expenses / Operating expenses | Other operating expenses (negative)"),
    ("map", "Depreciation & amortization | D&A – owned assets + Depreciation – right-of-use assets (split using the lease note)"),
    ("map", "Impairments | Impairments and special items"),
    ("map", "Net interest / Financial income + expenses | Net financial items excl. leases + Interest on lease liabilities"),
    ("map", "Tax expense | Income tax (negative)"),
    ("map", "Non-controlling interest | Minority interests (negative)"),
    ("map", "Installments + interests on lease liabilities / Rent payments | Lease payments, total (negative)"),
    ("map", "Balance sheet lines | Same names on Hist – put anything else in 'Other' lines so totals match"),
    ("map", "Members / FTEs / Clubs / Stores | Volume KPIs and Locations per segment"),
    ("map", "Number of shares outstanding / DPS | Shares outstanding, Dividend per share"),
    ("map", "Peer table (EV/Sales, EV/EBITDA, EV/EBIT, P/E for three years) | Comps rows 6-13"),
]


def write_guide(wb):
    ws = wb["Guide"]
    ws.sheet_view.showGridLines = False
    for k, v in dict(A=3, B=6, C=62, D=80).items():
        ws.column_dimensions[k].width = v
    put(ws, "B1", "Guide", kind="label", bold=True, size=15, color=TITLE)
    ws.row_dimensions[1].height = 24
    r = 3
    for tag, txt in GUIDE:
        if tag == "h":
            band(ws, r, "B", "D", txt)
        elif tag == "map":
            a, b = [x.strip() for x in txt.split("|")]
            put(ws, f"C{r}", a, kind="label")
            put(ws, f"D{r}", b, kind="note")
            bottom_border(ws, r, "C", "D")
        elif tag:
            put(ws, f"B{r}", tag, kind="label", bold=True, color=NAVY, align="center")
            ws.merge_cells(f"C{r}:D{r}")
            put(ws, f"C{r}", txt, kind="label", wrap=True)
            ws.row_dimensions[r].height = 26 if len(txt) > 120 else 15
        r += 1
    r += 1
    put(ws, f"C{r}", "Pareto 'Model' line", kind="label", bold=True) if False else None
