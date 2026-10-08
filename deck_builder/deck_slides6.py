"""Company-specific appendix slides built from the model and the case text module: club economics, the path from revenue
to cash and shareholder returns, and the competitive and macro backdrop. Each slide needs its text block in the case
module (`unit`, `cash_sources`, `comp`, `macro`); without one the slide is skipped by build_deck.py."""
from deck_core import *
from deck_data import num, pct, mult, HC, FC
from deck_slides1 import std
from deck_case import ct
from cl_core import waterfall

PALE = "D6E6EC"


def _isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _hdr(cells, h=0.24, size=8, first_grey=False):
    r = dict(cells=cells, fill=NAVY, color=WHITE, bold=True, size=size, h=h, align={j: "c" for j in range(1, len(cells))})
    if first_grey:
        r["fills"] = {1: "8C96A0"}
    return r


# ------------------------------------------------------------------ A7 club economics
def unit_economics_slide(prs, d):
    U = ct("unit")
    ya, yf = d.years([HC[-1]])[0], d.years(FC)
    loc = d.row("Model", "loc", [HC[-1]] + FC)
    ebitdaal = d.row("Model", "ebitdaal", [HC[-1]] + FC)
    per_club = ebitdaal[0] / loc[0]                                   # NOKm EBITDAaL per club, last actual year
    capl = d.row("Drivers", "capex_loc", FC)
    opens = d.row("Model", "open", FC)
    payback = capl[0] / per_club
    mcapex = d.row("Drivers", "mcapex", FC)[0]
    fcfe = d.row("Output", "fcfe", FC)
    conv = [f / e for f, e in zip(fcfe, ebitdaal[1:])]
    lev_t = d.c("Drivers", "lev_t")
    payout = d.row("Drivers", "payout", FC)
    bb = d.row("Output", "cf_bb", FC)
    best = max(U["margins"], key=lambda m: m[1][-2])
    s = std(prs, "Appendix #4.7", "Club economics – country margins and the cost of a new club",
            f"{best[0]}'s country margin is {best[1][2] * 100:.0f}% ({best[1][3] * 100:.0f}% in Q2 2026); a new club costs NOK 7-9m "
            f"and pays back in ~3 years – we stay below guidance",
            U["sources"])
    # left: country margins
    x, w = 0.47, 6.1
    panel_header(s, x, 1.38, w, "Country EBITDA margin before IFRS 16", None)
    cats = [m[0] for m in U["margins"]]
    series = [(yr, [m[1][i] for m in U["margins"]]) for i, yr in enumerate(U["margin_years"])]
    add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, x, 1.80, w, 2.05, cats, series, [PALE, LBLUE, MIDBLUE, NAVY], size=7.5,
              legend="t", labels=True, num_fmt="0%", label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=60, overlap=-10,
              val_min=0, val_max=max(v for m in U["margins"] for v in m[1]) * 1.3)
    text(s, x, 3.86, w, 0.3, U["margin_note"], size=7.5, italic=True, color=MUTED)
    # right: country snapshot
    rx, rw = 6.77, 6.1
    panel_header(s, rx, 1.38, rw, "Country snapshot – Q2 2026", None)
    rows = [_hdr(["", "Clubs", "Members ('000)", "Members per club", "ARPM (NOK/month)", "EBITDA margin"], h=0.3)]
    for name, clubs, mem, arpm, m in U["snapshot"]:
        grp = name == "Group"
        rows.append(dict(cells=[name, f"{clubs:,}", f"{mem:,}", f"{mem * 1000 / clubs:,.0f}", f"{arpm:,}", pct(m, 0)], size=9,
                         h=0.3, line_bottom="E1E5EA", bold=grp, fill="E4EEF2" if grp else None, line_top=NAVY if grp else None,
                         align={j: "c" for j in range(1, 6)}))
    table(s, rx, 1.82, rw, rows, [1.3, 0.75, 1.1, 1.15, 1.2, 1.0])
    text(s, rx, 3.62, rw, 0.5, [
        ("Group EBITDA margin after overhead (pre-IFRS 16); country margins before group overhead. Norway (incl. Fresh Fitness) "
         "earns ~60% of country EBITDA with 44% of the clubs.", {"size": 7.5, "italic": True, "color": MUTED})], size=7.5)
    # bottom: company guidance vs model
    y0 = 4.22
    panel_header(s, 0.47, y0, 12.40, "A new club and the group's financial framework – company guidance vs. our base case", None)
    G = U["guidance"]
    o27, o28 = opens[1], opens[2]
    o2930 = sum(opens[3:5]) / 2
    spec = [("Openings per year", G["openings"], f"{o27:.0f} in {yf[1]}, {o28:.0f} in {yf[2]}, {o2930:.0f} a year in {yf[3]}-{yf[4]} – net of closures"),
            ("Expansion capex per club", G["capex"], f"NOK {capl[0]:.1f}m in {yf[0]}, indexed to NOK {capl[-1]:.1f}m by {yf[-1]} (buffer for conversions and relocations)"),
            ("Payback", G["payback"], f"~{payback:.1f} years at mature volume: NOK {capl[0]:.1f}m / NOK {per_club:.1f}m EBITDAaL per club ({ya})"),
            ("Maintenance capex", G["mcapex"], f"{mcapex * 100:.1f}% of revenue every year; new clubs reach {d.c('Drivers', 'ramp1') * 100:.0f}/"
                                              f"{d.c('Drivers', 'ramp2') * 100:.0f}/{d.c('Drivers', 'ramp3') * 100:.0f}% of mature volume in years 1-3"),
            ("Cash conversion", G["fcf"], f"Free cash flow to equity {conv[0] * 100:.0f}% of EBITDAaL in {yf[0]}, {conv[2] * 100:.0f}% in {yf[2]} "
                                          f"(22% cash tax, all capex)"),
            ("Leverage", G["leverage"], f"Buybacks lift NIBD/EBITDAaL to {lev_t:.2f}x and hold it there"),
            ("Distribution", G["payout"], f"{payout[0] * 100:.0f}-{payout[-1] * 100:.0f}% dividend payout plus buybacks of NOK "
                                          f"{min(abs(v) for v in bb[1:5]):,.0f}-{max(abs(v) for v in bb[1:5]):,.0f}m a year from {yf[1]}")]
    rows = [dict(cells=["", "SATS – Capital Markets Day 2025 / Q2 2026", "Our model (base case)"], fill=NAVY, color=WHITE, bold=True,
                 size=8.5, h=0.26)]
    for lab, co, us in spec:
        rows.append(dict(cells=[lab, co, us], size=8.5, h=0.25, line_bottom="E1E5EA", bolds={0: True}))
    table(s, 0.47, y0 + 0.44, 12.40, rows, [1.7, 4.9, 5.8], align=["l", "l", "l"])
    notes(s, "TALKING POINT: every operating assumption sits at or below the company's own framework – openings at the lower "
             "end of 8-12, capex per club above the NOK 7-8m guidance, maintenance capex at 5%, cash conversion below the LTM "
             "run-rate because we tax every krone at 22%. The upside case is the company delivering what it said at the CMD.")
    return s


# ------------------------------------------------------------------ A8 from revenue to cash
def cash_slide(prs, d):
    ya, y3 = d.years([HC[-1]])[0], d.years([FC[2]])[0]
    k, n = HC[-1], FC[2]
    O = lambda key, cols: d.row("Output", key, cols)
    rev0, rev3 = O("rev", [k, n])
    e0, e3 = O("ebitdaal", [k, n])
    deltas = [(lab, b - a) for lab, (a, b) in (("Revenue growth", O("rev", [k, n])), ("COGS", O("cogs", [k, n])),
                                               ("Personnel", O("pers", [k, n])), ("Other opex", O("oth", [k, n])),
                                               ("Lease payments", d.row("Model", "lease", [k, n])))]
    cols5 = FC[:5]
    y1, y5 = d.years([FC[0]])[0], d.years([FC[4]])[0]
    fcfe = O("fcfe", cols5)
    div = [-v for v in O("cf_div", cols5)]
    bb = [-v for v in O("cf_bb", cols5)]
    capg = [-v for v in d.row("Model", "capex_g", cols5)]
    cum = sum(fcfe)
    s = std(prs, "Appendix #4.8", "From revenue growth to cash and shareholder returns",
            f"Revenue +NOK {rev3 - rev0:,.0f}m by {y3} adds NOK {e3 - e0:,.0f}m of EBITDAaL; NOK {cum / 1000:.1f}bn of free cash flow "
            f"in {str(y1)[:4]}-{str(y5)[2:4]}E funds payouts and new clubs",
            ct("cash_sources", "Sources: Case team estimates (Excel model)."))
    # left: EBITDAaL bridge
    x, w = 0.47, 6.1
    panel_header(s, x, 1.38, w, f"EBITDAaL bridge {ya} → {y3} (NOKm)", None)
    steps = [(f"EBITDAaL {ya}", e0, "total")] + [(lab, v, "delta") for lab, v in deltas] + [(f"EBITDAaL {y3}", e3, "total")]
    waterfall(s, (x, 1.80, w, 2.45), steps, size=7.5, plot=(0.02, 0.08, 0.96, 0.74))
    g_rev = (rev3 / rev0) ** (1 / 3) - 1
    text(s, x, 4.20, w, 0.25, f"Revenue CAGR {g_rev * 100:.1f}%; EBITDAaL margin {e0 / rev0 * 100:.1f}% → {e3 / rev3 * 100:.1f}% – costs grow "
                                f"with inflation and clubs, not with revenue", size=7.5, italic=True, color=MUTED)
    # right: FCFE and its uses
    rx, rw = 6.77, 6.1
    panel_header(s, rx, 1.38, rw, f"Free cash flow to equity and its uses {y1}–{y5} (NOKm)", None)
    top = max(max(fcfe), max(a + b + c for a, b, c in zip(div, bb, capg))) * 1.25
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_STACKED, rx, 1.80, rw, 2.45, d.years(cols5),
                   [("Dividends paid", div), ("Buybacks", bb), ("Growth capex", capg), ("Free cash flow to equity", fcfe)],
                   [NAVY, MIDBLUE, LBLUE, GREEN], size=7.5, legend="t", labels=True, num_fmt="#,##0;-#,##0;",
                   label_pos=XL_LABEL_POSITION.CENTER, gap=55, overlap=100, label_color=WHITE, val_min=0, val_max=top)
    series_labels_off(gf.chart, 2)                    # growth capex is small – the table has the numbers
    to_combo(gf.chart, 3, color=GREEN, fmt="#,##0", size=7.5, val_min=0, val_max=top)
    text(s, rx, 4.20, rw, 0.25, "Dividends are paid the year after they are earned; growth capex is shown as a use of cash before "
                                  "free cash flow to equity", size=7.5, italic=True, color=MUTED)
    # bottom: capital allocation table
    y0 = 4.55
    panel_header(s, 0.47, y0, 12.40, "Capital allocation – base case", None)
    tcols = [HC[-1]] + cols5
    rows = [_hdr([""] + d.years(tcols), first_grey=True)]
    np_ = O("np", tcols)
    sh = d.row("Model", "shares", tcols)
    spec = [("Free cash flow to equity (NOKm)", O("fcfe", tcols), lambda v: f"{v:,.0f}", True),
            ("Dividends paid (NOKm)", [-v if _isnum(v) else None for v in O("cf_div", tcols)], lambda v: f"{v:,.0f}", False),
            ("Share buybacks (NOKm)", [-v if _isnum(v) else None for v in O("cf_bb", tcols)], lambda v: f"{v:,.0f}", False),
            ("Total distribution in % of net profit", [((-a - b) / c if _isnum(a) and _isnum(b) and c else None)
                                                       for a, b, c in zip(O("cf_div", tcols), O("cf_bb", tcols), np_)], lambda v: f"{v * 100:.0f}%", False),
            ("Dividend per share (NOK)", O("dps", tcols), lambda v: f"{v:.2f}", False),
            ("Shares outstanding, year end (m)", sh, lambda v: f"{v:,.0f}", False),
            ("NIBD / EBITDAaL (x)", d.row("Model", "lev", tcols), lambda v: f"{v:.1f}x", True)]
    for lab, vals, f_, bold in spec:
        rows.append(dict(cells=[lab] + [("–" if not _isnum(v) else f_(v)) for v in vals], size=8.5, h=0.225, line_bottom="E1E5EA",
                         bolds={0: bold}, align={j: "c" for j in range(1, 7)}, fills={1: "F2F3F5"}))
    table(s, 0.47, y0 + 0.44, 8.4, rows, [3.0] + [0.9] * 6)
    panel(s, 9.10, y0 + 0.44, 3.77, 1.82)
    bb1 = -O("cf_bb", [FC[1]])[0]
    text(s, 9.22, y0 + 0.50, 3.55, 1.75, [
        ("Why cash matters here", {"bold": True, "color": NAVY, "size": 10, "space_after": 3}),
        (f"Members prepay: NWC is {abs(d.row('Drivers', 'nwc', [FC[0]])[0]) * 100:.0f}% of revenue and a source of funds as revenue grows.",
         {"bullet": True, "space_after": 2}),
        (f"Maintenance capex {d.row('Drivers', 'mcapex', [FC[0]])[0] * 100:.0f}% of revenue and growth capex NOK "
         f"{d.row('Drivers', 'capex_loc', [FC[0]])[0]:.0f}m per club leave most of EBITDAaL for shareholders.",
         {"bullet": True, "space_after": 2}),
        (f"Buybacks of ~NOK {bb1:,.0f}m a year at our modelled prices retire ~{(sh[2] / sh[1] - 1) * -100:.0f}% of the shares a year – "
         f"EPS compounds faster than profit.", {"bullet": True}),
    ], size=8.5)
    notes(s, "TALKING POINT: the bridge shows where the margin comes from – revenue grows NOK ~1bn while personnel, other opex "
             "and rent grow with inflation and the number of clubs. The right-hand chart is the capital allocation story: free "
             "cash flow covers dividends, buybacks and the roll-out with leverage held at the company's target.")
    return s


# ------------------------------------------------------------------ A11 competition and macro
def competition_macro_slide(prs, d):
    Cp, Mc = ct("comp"), ct("macro")
    s = std(prs, "Appendix #4.11", "Competitive landscape and macro backdrop", Cp["subtitle"], Cp["sources"])
    # left: operators
    x, w = 0.47, 7.35
    panel_header(s, x, 1.38, w, Cp.get("title", "Nordic fitness operators – positioning and indicative list prices"), None)
    rows = [dict(cells=Cp.get("headers", ["Operator", "Segment", "Markets", "Clubs", "Monthly price", "Note"]), fill=NAVY, color=WHITE, bold=True, size=8, h=0.26)]
    for i, r in enumerate(Cp["rows"]):
        sats = i < 2
        rows.append(dict(cells=list(r), size=8, h=0.33, line_bottom="E1E5EA", bolds={0: True}, fill="E4EEF2" if sats else None,
                         align={2: "c", 3: "c"}))
    table(s, x, 1.82, w, rows, [1.55, 1.3, 1.0, 0.7, 1.45, 1.6], align=["l"] * 6)
    panel(s, x, 4.62, w, 0.78)
    text(s, x + 0.12, 4.66, w - 0.24, 0.72, Cp["takeaway"], size=8.5)
    # right: macro
    rx, rw = 8.02, 4.85
    panel_header(s, rx, 1.38, rw, Mc.get("title", "Macro backdrop – what drives price and cost"), None)
    mh = Mc.get("headers", ["", "Norway", "Sweden"])
    wide = len(mh[2]) > 8                              # a comment column instead of a second country
    rows = [dict(cells=mh, fill=NAVY, color=WHITE, bold=True, size=8, h=0.26, align={1: "c", 2: "l" if wide else "c"})]
    for lab, no, se in Mc["rows"]:
        rows.append(dict(cells=[lab, no, se], size=8, h=0.3, line_bottom="E1E5EA", align={1: "c", 2: "l" if wide else "c"}))
    table(s, rx, 1.82, rw, rows, [2.0, 1.0, 1.85] if wide else [2.45, 1.15, 1.25])
    text(s, rx, 4.0, rw, 0.25, Mc.get("footnote", "Norway = 45% of revenue, Sweden 34%, Finland and Denmark 21% (2025)."), size=7.5, italic=True, color=MUTED)
    # bottom: implications
    y0 = 5.55
    panel_header(s, 0.47, y0, 12.40, "What it means for the forecast", None)
    xs = [0.47, 4.67, 8.87]
    for (bx, b) in zip(xs, Mc["bullets"]):
        panel(s, bx, y0 + 0.44, 3.95, 0.95)
        text(s, bx + 0.1, y0 + 0.48, 3.75, 0.9, b, size=8.5)
    notes(s, "TALKING POINT: the competitive question is whether SATS can keep raising prices ~3% a year with low-cost chains "
             "at half the price. The answer so far is yes (ARPM +6%, members +1% in Q2 2026); the bear case is the year that "
             "stops. The macro table shows why the cost line matters more in Norway (wages 4%+) than in Sweden (KPIF ~2%).")
    return s
