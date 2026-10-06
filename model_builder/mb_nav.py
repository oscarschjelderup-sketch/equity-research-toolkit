"""Cover page and '>>>' section divider sheets (Campari-style navigation)."""
import case_data as ex
from openpyxl.formatting.rule import FormulaRule
from mb_core import *

D = lambda k: S("DCF", k)
I = lambda k: S("Inputs", k)

SECTIONS = [
    ("Inputs >>>", "Inputs", "FFC000", "Everything you type lives here. Blue figures are hard-coded inputs; yellow cells are forecast assumptions.", [
        ("Inputs", "General inputs", "Company info, timeline, market data, net debt bridge and valuation settings"),
        ("Hist", "As reported", "Seven years of reported income statement, balance sheet, cash flow and KPIs"),
        ("Drivers", "Assumptions cockpit", "Forecast drivers per year, Bear/Base/Bull adjustments, terminal assumptions, cost structure and capital allocation"),
    ]),
    ("Calculations >>>", "Calculations", "7F7F7F", "The calculation engine. No inputs except known one-off items.", [
        ("Model", "Operating model", "Revenue build (locations or volume x price), earnings build, investments, free cash flow and financing"),
    ]),
    ("Output >>>", "Output", "407061", "Link-only presentation of the results – what you would show in a report.", [
        ("Output", "Financial statements", "Income statement, balance sheet (capital employed) and cash flow with integrity checks"),
        ("Analysis", "Financial analysis", "Growth, margins, ROIC vs. WACC, leverage, per-share data and valuation multiples"),
    ]),
    ("Valuation >>>", "Valuation", "003255", "From cost of capital to target price, cross-checked with peers.", [
        ("WACC", "Cost of capital", "CAPM with peer-based beta, cost of debt and target capital structure"),
        ("DCF", "DCF valuation", "FCFF, stub period and mid-year discounting, terminal value, equity bridge and target price"),
        ("Sensitivity", "Sensitivity & scenarios", "WACC vs. growth, WACC vs. exit multiple, growth vs. margin and Bear/Base/Bull"),
        ("Comps", "Trading multiples", "Peer group statistics and implied value per share"),
        ("Football", "Football field", "Valuation summary across all methods, with chart"),
    ]),
    ("Market view >>>", "Market view", "4F7FA0", "What the share price implies, where we differ from consensus – and what would prove us wrong.", [
        ("Reverse_DCF", "Reverse DCF", "Market-implied EBIT margin, growth, WACC and terminal growth at today's share price"),
        ("Consensus", "Consensus vs. our estimates", "Consensus inputs, our estimates vs. consensus and our variant perception"),
        ("Thesis", "Thesis tracker", "Scenario stories, signposts and kill criteria with a live status"),
    ]),
    ("Summary >>>", "Summary", "81B0C0", "One-page overview, numbers for the pitch deck and the model health check.", [
        ("Dashboard", "Dashboard", "Recommendation, key financials and charts on one page"),
        ("Deck_Feed", "Deck feed", "Numbers and text lines ready to paste into the pitch deck"),
        ("Checks", "Integrity checks", "All checks must be OK before the model is submitted"),
    ]),
]
ORDER = ["Cover", "Guide"]
TABS = {"Cover": "003255", "Guide": "003255"}
for div, _, colr, _, sheets in SECTIONS:
    ORDER.append(div)
    TABS[div] = colr
    for sh, _, _ in sheets:
        ORDER.append(sh)
        TABS[sh] = colr


def _banner(ws, last="N"):
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 110
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 14
    for r in (2, 3, 4):
        fill_row(ws, r, "B", last, BANNER)
        ws.row_dimensions[r].height = 16


def _link(ws, addr, sheet, text, size=10):
    c = put(ws, addr, text, kind="label", bold=True, color="0563C1", size=size)
    c.hyperlink = f"#'{sheet}'!A1"
    return c


def write_dividers(wb):
    for div, title, colr, blurb, sheets in SECTIONS:
        ws = wb[div]
        _banner(ws)
        ws.column_dimensions["C"].width = 4
        ws.column_dimensions["D"].width = 24
        ws.column_dimensions["E"].width = 26
        ws.column_dimensions["F"].width = 90
        put(ws, "D8", f"={I('company')}", bold=True, size=16, color=NAVY)
        put(ws, "D9", "Financial Model", kind="label", bold=True, size=16, color=NAVY)
        ws.row_dimensions[8].height = 22
        ws.row_dimensions[9].height = 22
        put(ws, "D12", title, kind="label", bold=True, size=22)
        ws.row_dimensions[12].height = 30
        put(ws, "D14", blurb, kind="note", italic=True, size=10)
        for j, (sh, nice, desc) in enumerate(sheets):
            r = 17 + j
            ws.row_dimensions[r].height = 16
            _link(ws, f"D{r}", sh, sh)
            put(ws, f"E{r}", nice, kind="label", bold=True, size=10)
            put(ws, f"F{r}", desc, kind="note", size=10)
            bottom_border(ws, r, "D", "F")
        _link(ws, f"D{19 + len(sheets)}", "Cover", "← Back to cover", size=9)


def write_cover(wb):
    ws = wb["Cover"]
    _banner(ws, last="I")
    for k, v in dict(C=4, D=20, E=26, F=78, G=4).items():
        ws.column_dimensions[k].width = v
    put(ws, "D7", f"={I('company')}", bold=True, size=24, color=NAVY)
    ws.row_dimensions[7].height = 32
    put(ws, "D8", "DCF Valuation Model", kind="label", bold=True, size=22)
    ws.row_dimensions[8].height = 30
    put(ws, "D10", f'={I("ticker")}&"  |  "&{I("exchange")}&"  |  "&{I("sector")}&"  |  figures in "&{I("unit")}',
        italic=True, color=GREY, size=10)
    put(ws, "D12", f'={D("rating")}&"  –  target price NOK "&TEXT({D("tp")},"0")&"  ("&TEXT({D("tp_up")},"+0%;-0%")&" upside)  |  scenario: "&{I("scenario")}',
        bold=True, size=12, color=NAVY)
    put(ws, "D13", f'="Model status: "&{S("Checks", "master")}', bold=True, size=10)
    ws.conditional_formatting.add("D13", FormulaRule(formula=['ISNUMBER(SEARCH("ERROR",$D$13))'],
                                                     fill=PatternFill("solid", fgColor=ERRRED)))
    ws.conditional_formatting.add("D13", FormulaRule(formula=['NOT(ISNUMBER(SEARCH("ERROR",$D$13)))'],
                                                     fill=PatternFill("solid", fgColor=OKGREEN)))
    put(ws, "D14", ex.MARKET.get("data_note", "All company data in this file is FICTIONAL example data – replace the blue inputs with your case data."),
        kind="note", italic=True, color="C00000")
    put(ws, "D15", f'={I("team")}', kind="calc", color=GREY, size=9)

    band(ws, 17, "D", "F", "Model map (click a sheet name to open it)", size=9)
    r = 18
    _link(ws, f"D{r}", "Guide", "Guide")
    put(ws, f"E{r}", "How to use", kind="label", bold=True)
    put(ws, f"F{r}", "Step-by-step guide, method notes and mapping of Pareto case data", kind="note")
    r += 1
    for div, title, colr, blurb, sheets in SECTIONS:
        ws.row_dimensions[r].height = 6
        r += 1
        c = put(ws, f"D{r}", title.upper(), kind="label", bold=True, color=WHITE, fill=colr, size=8)
        c.hyperlink = f"#'{div}'!A1"
        c.font = Font(name=FONT, size=8, bold=True, color=WHITE if colr not in ("FFC000", "81B0C0") else "000000")
        put(ws, f"E{r}", blurb, kind="note", italic=True)
        r += 1
        for sh, nice, desc in sheets:
            _link(ws, f"D{r}", sh, sh, size=9)
            put(ws, f"E{r}", nice, kind="label", bold=True)
            put(ws, f"F{r}", desc, kind="note")
            bottom_border(ws, r, "D", "F")
            r += 1

    band(ws, 17, "H", "H", "Colour legend", size=9)
    legend = [("1,234", "inputh", None, "Hard-coded input (blue)"),
              ("1,234", "input", None, "Forecast assumption / switch (blue on yellow)"),
              ("1,234", "calc", None, "Formula (black)"),
              ("1,234", "link", None, "Direct link to another sheet (green)"),
              ("1,234", "calc", KEYFILL, "Key line / key output (light blue)"),
              ("0.0", "check", None, "Integrity check – should be zero (grey italic)")]
    ws.column_dimensions["H"].width = 9
    ws.column_dimensions["I"].width = 46
    fill_row(ws, 17, "H", "I", NAVY)
    for (v, kind, fill, txt), rr in zip(legend, [18, 20, 21, 22, 23, 25]):
        if kind == "check":
            put(ws, f"H{rr}", v, kind="calc", italic=True, color=GREY, align="right")
        else:
            put(ws, f"H{rr}", v, kind=kind, fill=fill, align="right", bold=fill is not None)
        put(ws, f"I{rr}", txt, kind="note", indent=1)
    for txt, rr in zip(["Sign convention: income positive, costs negative.",
                        "Units: NOKm unless stated; per share in NOK.",
                        "Historicals have grey year headers, forecasts navy.",
                        "Explanations sit in the Notes column on each sheet."], [28, 29, 30, 32]):
        put(ws, f"H{rr}", txt, kind="note", italic=True, size=8)
    put(ws, f"D{r + 2}", f"Version 3.0 – September 2026 · data set: {ex.MARKET['company']}. Recalculate fully (Ctrl+Alt+F9) after pasting new data; press F9 to refresh data tables.",
        kind="note", italic=True, size=8)
