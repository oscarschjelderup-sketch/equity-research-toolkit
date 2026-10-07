"""Appendix slides and the template guide."""
import json
import os

from deck_core import *
from deck_data import num, pct, mult, HC, FC
from deck_slides1 import std
from deck_case import ct, CASE


def _whatif():
    """The what-if runs for this case (model_builder/whatif_runs*.json written by whatif_runs.py), if present."""
    name = os.environ.get("EQR_WHATIF") or ("whatif_runs_sats.json" if CASE == "sats_data" else "whatif_runs.json")
    for folder in (os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "model_builder"), "."):
        try:
            with open(os.path.join(folder, name), encoding="utf8") as f:
                return json.load(f)
        except (OSError, ValueError):
            continue
    return {}


def divider(prs, d):
    s = new_slide(prs, "Chapter slide - dark blue", ph_text={0: "Appendix", 1: "Supporting analysis and model details"})
    notes(s, "TEMPLATE: Check the case rules before including an appendix – Pareto's 2026 rules allowed a maximum of four "
             "content slides. Keep the appendix as back-up for Q&A if it cannot be submitted.")
    return s


def _kv_rows(items, size=8.5, h=0.205):
    rows = []
    for it in items:
        lab, val = it[0], it[1]
        style = it[2] if len(it) > 2 else None
        r = dict(cells=[lab, val], size=size, h=h, line_bottom="E1E5EA")
        if style == "bold":
            r.update(bold=True, fill="E4EEF2", line_top=NAVY)
        elif style == "head":
            r.update(bold=True, fill=NAVY, color=WHITE, line_bottom=None)
        elif style == "muted":
            r.update(italic=True, color=MUTED)
        rows.append(r)
    return rows


# ------------------------------------------------------------------ A1 DCF
def dcf_slide(prs, d):
    ev, dcf, tvs = d.c("DCF", "ev"), d.c("DCF", "dcf_ps"), d.c("DCF", "tv_share")
    s = std(prs, "Appendix #4.1", "DCF model – base case",
            f"Base case DCF value of NOK {dcf:.0f} per share – the terminal value accounts for {tvs * 100:.0f}% of "
            f"enterprise value",
            "Sources: Case team estimates (Excel model, DCF and WACC sheets). FCFF on a pre-IFRS 16 basis: lease payments "
            "are treated as operating costs, so lease liabilities are not deducted. Figures are illustrative.")
    x, w = 0.47, 8.55
    panel_header(s, x, 1.38, w, "Free cash flow to firm and discounting (NOKm)", None)
    cols = ["K"] + FC
    yrs = d.years(cols) + ["TY"]
    R = lambda k, f=num: [f(v) for v in d.row("DCF", k, cols)]
    T = lambda k, f=num: f(d.v("DCF", f"T{d.reg['rows']['DCF|' + k]}"))
    blank = lambda: [""]
    fc_fill = {j: "EEF4F7" for j in range(2, 11)}
    rows = [dict(cells=[""] + yrs, fill=NAVY, color=WHITE, bold=True, size=8, h=0.24,
                 fills={10: MIDBLUE})]
    spec = [
        ("Revenue", R("rev") + [T("rev")], "bold"),
        ("  Growth", R("grev", pct) + [T("grev", pct)], "italic"),
        ("EBITDAaL", R("ebitdaal") + blank(), None),
        ("  Margin", R("ebitdaal_m", pct) + blank(), "italic"),
        ("EBIT adj.", R("ebit") + [T("ebit")], "bold"),
        ("  Margin", R("ebit_m", pct) + [T("ebit_m", pct)], "italic"),
        ("Taxes on EBIT", [num(v, paren=True) for v in d.row("DCF", "tax", cols)] + [num(d.v("DCF", f"T{d.reg['rows']['DCF|tax']}"), paren=True)], None),
        ("NOPAT", R("nopat") + [T("nopat")], "bold"),
        ("+ D&A", R("addda") + blank(), None),
        ("– Capex", [num(v, paren=True) for v in d.row("DCF", "capex", cols)] + blank(), None),
        ("– Increase in NWC", [num(v, paren=True) for v in d.row("DCF", "dnwc", cols)] + blank(), None),
        ("Free cash flow to firm", R("fcff") + [T("fcff")], "fcff"),
        ("Share of year included", [""] + [pct(v, 0) for v in d.row("DCF", "share", FC)] + blank(), "italic"),
        ("Discount period (years)", [""] + [f"{v:.2f}" for v in d.row("DCF", "period", FC)] + blank(), "italic"),
        ("Discount factor", [""] + [f"{v:.3f}" for v in d.row("DCF", "df", FC)] + blank(), "italic"),
        ("PV of FCFF", [""] + [num(v) for v in d.row("DCF", "pv", FC)] + blank(), "bold"),
    ]
    for lab, vals, style in spec:
        r = dict(cells=[lab] + vals, size=8, h=0.205, fills=dict(fc_fill))
        if style == "bold":
            r.update(bold=True, line_top=GRIDGREY)
        elif style == "italic":
            r.update(italic=True, color=MUTED)
        elif style == "fcff":
            r.update(bold=True, line_top=NAVY, fills={j: "D6E6EC" for j in range(0, 11)})
        r["fills"][10] = "DCE9EF" if style != "fcff" else "D6E6EC"
        rows.append(r)
    table(s, x, 1.82, w, rows, [1.75] + [0.68] * 10)
    # assumptions box
    panel(s, x, 5.55, w, 1.33)
    g, ronic, stub = d.c("DCF", "tv_g"), d.c("DCF", "tv_ronic"), d.c("Inputs", "stub")
    sn = d.reg["sens"]
    rc = sn["t1_rows"][0] + 2
    ctr = d.v("Sensitivity", f"G{rc}")
    sens_w = abs(d.v("Sensitivity", f"H{rc}") - ctr)
    sens_w2 = abs(d.v("Sensitivity", f"F{rc}") - ctr)
    sens_g = abs(d.v("Sensitivity", f"G{rc - 1}") - ctr)
    sens_g2 = abs(d.v("Sensitivity", f"G{rc + 1}") - ctr)
    sens_w, sens_w2 = sorted((sens_w, sens_w2))
    sens_g, sens_g2 = sorted((sens_g, sens_g2))
    text(s, x + 0.15, 5.62, w - 0.3, 1.2, [
        ("Key DCF assumptions", {"bold": True, "color": NAVY, "size": 10, "space_after": 3}),
        (f"**Valuation date** {d.c('Inputs', 'val_date'):%d.%m.%Y} – only {stub * 100:.0f}% of {d.years(FC[:1])[0]} FCFF is "
         f"included (stub); **mid-year** discounting", {"bullet": True, "space_after": 2}),
        (f"**Terminal value:** Gordon growth with g = {g * 100:.1f}% and value-driver reinvestment (RONIC {ronic * 100:.0f}%) "
         f"– implied exit multiple {mult(d.c('DCF', 's_exit'))} EV/EBITDAaL", {"bullet": True, "space_after": 2}),
        ("**Lease consistency:** FCFF after lease payments, WACC and net debt excl. leases (pre-IFRS 16 basis)", {"bullet": True, "space_after": 2}),
        (f"**Sensitivity:** ±0.5pp WACC moves the value by NOK {sens_w:.1f}–{sens_w2:.1f} per share; "
         f"±0.25pp terminal growth by only NOK {sens_g:.1f}–{sens_g2:.1f} (RONIC above WACC)", {"bullet": True}),
    ], size=9)
    # right column tables
    rx, rw = 9.25, 3.62
    panel_header(s, rx, 1.38, rw, "WACC", None)
    W = lambda k: d.c("WACC", k)
    wacc_rows = _kv_rows([
        ("Risk-free rate", pct(W("rf"), 2)), ("Equity risk premium", pct(W("erp"), 2)),
        ("Relevered beta", f"{W('bl'):.2f}"), ("Size premium", pct(W("size"), 2)),
        ("Cost of equity", pct(W("ke"), 2), "bold"),
        ("After-tax cost of debt", pct(W("kd_at"), 2)), ("Target D / (D+E)", pct(W("dv"), 0)),
        ("WACC", pct(W("wacc"), 2), "bold"),
    ], size=8.5, h=0.2)
    table(s, rx, 1.82, rw, wacc_rows, [2.2, 1.4])
    panel_header(s, rx, 3.60, rw, "Valuation summary (NOKm)", None)
    D = lambda k: d.c("DCF", k)
    vs = _kv_rows([
        ("PV of FCFF 2026E–2033E", num(D("sum_pv"))), ("PV of terminal value", num(D("pv_tv"))),
        ("Enterprise value", num(D("ev")), "bold"),
        ("Net interest-bearing debt", num(D("b_nibd"), paren=True)), ("Minority interests", num(D("b_min"), paren=True)),
        ("Associates & investments", num(D("b_assoc"))), ("Pensions & other", num(D("b_pens"), paren=True)),
        ("Equity value", num(D("eq")), "bold"),
        ("Diluted shares (m)", f"{D('shares'):.1f}"),
        ("DCF value per share (NOK)", f"{D('dcf_ps'):.1f}", "bold"),
        ("Current share price (NOK)", f"{D('price'):.1f}"), ("Upside", pct(D("dcf_up"), 1, sign=True)),
    ], size=8.5, h=0.2)
    table(s, rx, 4.04, rw, vs, [2.2, 1.4])
    notes(s, "TEMPLATE: Copy from the DCF sheet. Be ready to explain the stub period, the mid-year convention and why "
             "leases are handled pre-IFRS 16 – judges often ask about terminal value and WACC.")
    return s


# ------------------------------------------------------------------ A2 scenarios
def scenario_slide(prs, d):
    t4 = {k: c for c, k, _, _ in d.reg["t4"]}
    r0, r1 = d.reg["sens"]["t4_rows"]
    sv = lambda k, j: d.v("Sensitivity", f"{t4[k]}{r0 + j}")
    price = d.c("Inputs", "price")
    pw = d.c("Sensitivity", "pw_dcf_ps")
    lo, hi = sv("dcf_ps", 0), sv("dcf_ps", 2)
    s = std(prs, "Appendix #4.3", "Scenario analysis",
            f"Bear-to-bull DCF range of NOK {lo:.0f}–{hi:.0f} per share; probability-weighted value of NOK {pw:.0f}",
            "Sources: Case team estimates (Excel model, Drivers and Sensitivity sheets – Bear/Base/Bull data table). "
            "Scenario adjustments are applied to every forecast year. Figures are illustrative.")
    x, w = 0.47, 6.35
    panel_header(s, x, 1.38, w, "Scenario assumptions and outcomes", None)
    adj = {k: tuple(d.c("Drivers", f"adj_{k}_{sc}") or 0.0 for sc in ("bear", "base", "bull"))
           for k in ("vol", "price", "open", "cogs", "pers", "oth", "capex", "tg", "exit", "prob")}
    rows = [dict(cells=["", "Bear", "Base", "Bull"], fill=NAVY, color=WHITE, bold=True, size=9, h=0.24,
                 fills={1: RED, 3: GREEN}, align={1: "c", 2: "c", 3: "c"})]
    sec = lambda t: dict(cells=[t, "", "", ""], bold=True, color=NAVY, size=9, h=0.22, line_bottom=NAVY)
    rowf = lambda lab, vals, **kw: dict(cells=[lab] + vals, size=8.5, h=0.205, line_bottom="E1E5EA",
                                        align={1: "c", 2: "c", 3: "c"}, **kw)
    ppf = lambda v: "–" if abs(v) < 1e-9 else f"{v * 100:+.1f}pp".replace("-", "\u2212")
    rows.append(sec("Assumptions (vs. base case, p.a.)"))
    cnt = lambda v: "–" if abs(v) < 1e-9 else f"{v:+.0f}".replace("-", "\u2212")
    for k, lab in [("vol", "Volume / like-for-like growth"), ("price", "Price/mix growth"),
                   ("open", "Net new locations per segment p.a."), ("cogs", "COGS in % of revenue"),
                   ("pers", "Personnel, variable part (% of rev.)"), ("oth", "Other opex, variable part (% of rev.)"),
                   ("capex", "Maintenance capex (% of revenue)"), ("tg", "Terminal growth")]:
        rows.append(rowf(lab, [cnt(v) if k == "open" else ppf(v) for v in adj[k]]))
    rows.append(rowf("Probability", [pct(v, 0) for v in adj["prob"]], bold=True))
    rows.append(sec("Outcomes"))
    rows.append(rowf(f"Revenue CAGR 2025–{str(d.years(['S'])[0])[:4]}E", [pct(sv("cagr", j)) for j in range(3)]))
    rows.append(rowf(f"EBIT adj. margin {d.years(['S'])[0]}", [pct(sv("ebit_m", j)) for j in range(3)]))
    rows.append(rowf("Enterprise value (NOKm)", [num(sv("ev", j)) for j in range(3)]))
    rows.append(rowf("DCF value per share (NOK)", [f"{sv('dcf_ps', j):.0f}" for j in range(3)], bold=True))
    rows.append(rowf("Upside vs. current price", [pct(sv("dcf_up", j), 0, sign=True) for j in range(3)]))
    rows.append(rowf("Target price (NOK)", [f"{sv('tp', j):.0f}" for j in range(3)], bold=True))
    rows.append(rowf("Implied recommendation", [sv("rating", j) for j in range(3)], bold=True))
    table(s, x, 1.82, w, rows, [2.95, 1.13, 1.13, 1.13])
    # chart
    rx, rw = 7.07, 5.80
    panel_header(s, rx, 1.38, rw, "DCF value per share by scenario (NOK)", None)
    vals = [sv("dcf_ps", j) for j in range(3)]
    vmax = max(vals) * 1.25
    cx, cy, cw, chh = rx, 1.85, rw, 2.55
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, cx, cy, cw, chh, ["Bear", "Base", "Bull"],
                   [("DCF value", vals)], [NAVY], size=9, labels=True, num_fmt="0",
                   label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=90, val_min=0, val_max=vmax)
    color_points(gf.chart, [RED, NAVY, GREEN])
    px, py, pw_, ph = 0.03, 0.05, 0.94, 0.80
    manual_plot_layout(gf.chart, px, py, pw_, ph)
    Y = lambda v: cy + (py + ph * (1 - v / vmax)) * chh
    for v, col, lab, dash in [(price, RED, f"Current price NOK {price:.0f}", MSO_LINE_DASH_STYLE.DASH),
                              (pw, NAVY, f"Probability-weighted NOK {pw:.0f}", MSO_LINE_DASH_STYLE.SQUARE_DOT)]:
        line(s, cx + px * cw, Y(v), cx + (px + pw_) * cw, Y(v), color=col, width=1.25, dash=dash)
    for k, (col, lab, dash) in enumerate([(RED, f"Current share price NOK {price:.0f}", MSO_LINE_DASH_STYLE.DASH),
                                          (NAVY, f"Probability-weighted value NOK {pw:.0f}", MSO_LINE_DASH_STYLE.SQUARE_DOT)]):
        lx = cx + 0.9 + k * 2.6
        line(s, lx, cy + chh + 0.08, lx + 0.35, cy + chh + 0.08, color=col, width=1.5, dash=dash)
        text(s, lx + 0.42, cy + chh - 0.02, 2.1, 0.2, lab, size=8.5, bold=True, color=col)
    # narratives
    ny = 4.62
    tg0 = d.c("Drivers", "tg_in") if d.c("Drivers", "tg_in") is not None else d.c("DCF", "tv_g")
    cost = lambda j: sum(adj[k][j] for k in ("cogs", "pers", "oth"))
    yr_last = d.years(["S"])[0]
    story = lambda n: d.c("Thesis", f"sc_{n}_story")
    watch = lambda n: d.c("Thesis", f"sc_{n}_signpost")
    boxes = [(name.capitalize(), col, [f"**Story:** {story(name)}", f"**Watch:** {watch(name)}",
                                       f"EBIT margin {sv('ebit_m', j) * 100:.1f}% in {yr_last}; revenue CAGR {sv('cagr', j) * 100:.1f}%"])
             for j, (name, col) in enumerate([("bear", RED), ("base", NAVY), ("bull", GREEN)])]
    bw = (rw - 0.3) / 3
    for j, (name, col, items) in enumerate(boxes):
        bx = rx + j * (bw + 0.15)
        hb = rect(s, bx, ny, bw, 0.32, fill=col)
        shape_text(hb, name, size=10, bold=True)
        panel(s, bx, ny + 0.36, bw, 1.62)
        text(s, bx + 0.08, ny + 0.42, bw - 0.16, 1.55, [(t, {"bullet": True, "space_after": 2}) for t in items],
             size=7.5)
    notes(s, "TEMPLATE: Scenario adjustments and probabilities live on the Drivers sheet (section B); outcomes come "
             "from the scenario data table on the Sensitivity sheet; stories and signposts from the Thesis sheet.")
    return s


# ------------------------------------------------------------------ A3 peers
def peers_slide(prs, d):
    cr = d.reg["comps"]
    comp = d.c("Inputs", "company").split(" ASA")[0]
    prem = d.v("Comps", f"M{cr['prem']}")
    mdiff = d.v("Comps", f"R{cr['prem']}")
    s = std(prs, "Appendix #4.9", "Peer group and multiples",
            f"{comp} trades at a {abs(prem) * 100:.0f}% {'discount' if prem < 0 else 'premium'} to peers on 2027E EV/EBIT "
            f"{'despite' if (prem < 0) == (mdiff > 0) else 'with'} a "
            f"{abs(mdiff) * 100:.0f}pp {'higher' if mdiff > 0 else 'lower'} EBIT margin",
            "Sources: Bloomberg consensus as provided in the case material (example data – replace), case team estimates. "
            "Multiples at current share prices; EV incl. lease liabilities (IFRS 16 basis).")
    x, w = 0.47, 12.40
    V = lambda c, r: d.v("Comps", f"{c}{r}")
    y5 = [d.v("Comps", f"{c}5") for c in "IJLMOP"]
    hdr = dict(cells=["Company", "Country", "Mcap (NOKm)", "EV/EBITDA " + y5[0], "EV/EBITDA " + y5[1],
                      "EV/EBIT " + y5[2], "EV/EBIT " + y5[3], "P/E " + y5[4], "P/E " + y5[5],
                      "EBIT margin " + str(d.v('Comps', 'R5')), "Growth " + str(d.v('Comps', 'S5'))],
               fill=NAVY, color=WHITE, bold=True, size=8.5, h=0.34, align={1: "c"})
    rows = [hdr]
    fx = lambda v: mult(v)
    for r in range(6, 14):
        rows.append(dict(cells=[V("B", r), V("C", r), num(V("D", r))] + [fx(V(c, r)) for c in "IJLMOP"] +
                          [pct(V("R", r)), pct(V("S", r))], size=8.5, h=0.215, line_bottom="E1E5EA",
                         align={1: "c"}))
    for key, lab in [("median", "Peer median"), ("mean", "Peer mean")]:
        r = cr[key]
        rows.append(dict(cells=[lab, "", num(V("D", r))] + [fx(V(c, r)) for c in "IJLMOP"] +
                          [pct(V("R", r)), pct(V("S", r))], size=8.5, h=0.22, bold=key == "median",
                         fill="E4EEF2" if key == "median" else None, line_top=NAVY if key == "median" else None))
    r = cr["company"]
    rows.append(dict(cells=[d.c("Inputs", "company"), "NO", num(V("D", r))] + [fx(V(c, r)) for c in "IJLMOP"] +
                      [pct(V("R", r)), pct(V("S", r))], size=8.5, h=0.24, bold=True, fill=PALEBLUE,
                     color=NAVY, line_top=NAVY, align={1: "c"}))
    r = cr["prem"]
    rows.append(dict(cells=["Premium / (discount) vs. median", "", ""] +
                      [pct(V(c, r), 0, paren=True) for c in "IJLMOP"] +
                      [f"{V('R', r) * 100:+.1f}pp", f"{V('S', r) * 100:+.1f}pp"], size=8.5, h=0.22, italic=True,
                     color=MUTED))
    table(s, x, 1.40, w, rows, [2.4, 0.8, 1.1, 1.0, 1.0, 1.0, 1.0, 0.9, 0.9, 1.1, 1.0])
    # chart: EV/EBIT FY2 per company
    by = 4.72
    panel_header(s, x, by, 6.1, "EV/EBIT 2027E – peers vs. " + comp, None)
    names = [V("B", r).replace(" ASA", "").replace(" AB", "").replace(" A/S", "").replace(" Oyj", "")
             .replace(" plc", "").replace(" SE", "").replace(" NV", "") for r in range(6, 14)]
    vals = [V("M", r) for r in range(6, 14)]
    order = sorted(range(8), key=lambda i: -vals[i])
    cats = [names[i] for i in order] + [comp]
    series = [vals[i] for i in order] + [V("M", cr["company"])]
    vmax = max(series) * 1.25
    cx, cy, cw, chh = x, by + 0.42, 6.1, 1.75
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, cx, cy, cw, chh, cats, [("EV/EBIT", series)], [LBLUE],
                   size=8, labels=True, num_fmt='0.0"x"', label_pos=XL_LABEL_POSITION.INSIDE_BASE, gap=40,
                   val_min=0, val_max=vmax, label_color=WHITE)
    color_points(gf.chart, [LBLUE] * 8 + [NAVY])
    px, py, pw_, ph = 0.02, 0.05, 0.96, 0.72
    manual_plot_layout(gf.chart, px, py, pw_, ph)
    med = V("M", cr["median"])
    ymed = cy + (py + ph * (1 - med / vmax)) * chh
    line(s, cx + px * cw, ymed, cx + (px + pw_) * cw, ymed, color=DARK, width=1, dash=MSO_LINE_DASH_STYLE.DASH)
    text(s, cx + cw - 1.6, ymed - 0.22, 1.55, 0.2, f"Peer median {mult(med)}", size=8, bold=True, align="r")
    # implied valuation table
    ix, iw = 6.82, 6.05
    panel_header(s, ix, by, iw, "Implied value per share from peer multiples (NOK)", None)
    yr = d.v("Comps", f"D{cr['yr']}")
    irows = [dict(cells=[f"Multiple ({yr})", "Company metric", "25th pct", "Median", "75th pct", "Included"],
                  fill=NAVY, color=WHITE, bold=True, size=8.5, h=0.26, align={5: "c"})]
    for key, lab in [("evs", "EV / Sales"), ("evebitda", "EV / EBITDA"), ("evebit", "EV / EBIT"), ("pe", "P / E")]:
        r = cr[key]
        metric = V("C", r)
        irows.append(dict(cells=[lab, (f"NOK {metric:.2f}" if key == "pe" else f"NOKm {num(metric)}"),
                                 f"{V('G', r):.0f}", f"{V('H', r):.0f}", f"{V('I', r):.0f}",
                                 "Yes" if V("J", r) else "No"], size=8.5, h=0.23, line_bottom="E1E5EA",
                          align={5: "c"}, colors={5: GREEN if V("J", r) else MUTED}, bolds={3: True}))
    r = cr["avg"]
    irows.append(dict(cells=["Average (included)", "", f"{V('G', r):.0f}", f"{V('H', r):.0f}",
                             f"{V('I', r):.0f}", ""], size=8.5, h=0.25, bold=True, fill=PALEBLUE, line_top=NAVY))
    table(s, ix, by + 0.45, iw, irows, [1.75, 1.3, 0.75, 0.75, 0.75, 0.75])
    text(s, ix, by + 2.0, iw, 0.2, "EV/Sales excluded: ignores the company's superior margins.", size=7.5,
         italic=True, color=MUTED)
    notes(s, "TEMPLATE: Paste the case peer table into the Comps sheet (rows 6-13). Choose the multiples to include "
             "(column J) and the forecast year (Inputs). Explain why the peers are comparable.")
    return s


# ------------------------------------------------------------------ A4 WACC & assumptions
def assumptions_slide(prs, d):
    s = std(prs, "Appendix #4.10", "WACC and key forecast assumptions",
            f"{d.c('WACC', 'wacc') * 100:.1f}% WACC from a peer-based beta; forecast drivers anchored in the historical "
            f"track record",
            "Sources: Norges Bank (risk-free rate), NFF/PwC risk premium survey, Bloomberg (peer betas), case team "
            "estimates. Example values – update before use.")
    x, w = 0.47, 4.85
    panel_header(s, x, 1.38, w, "Cost of capital build-up", None)
    W = lambda k: d.c("WACC", k)
    rows = _kv_rows([
        ("Cost of equity", "", "head"),
        ("Risk-free rate (10y NGB)", pct(W("rf"), 2)), ("Equity risk premium", pct(W("erp"), 2)),
        ("Unlevered beta (peer median)", f"{W('bu'):.2f}"), ("Target D/E", pct(W("de"), 1)),
        ("Relevered beta", f"{W('bl'):.2f}"), ("Size premium", pct(W("size"), 2)),
        ("Cost of equity", pct(W("ke"), 2), "bold"),
        ("Cost of debt", "", "head"),
        ("Pre-tax cost of debt (rf + spread)", pct(W("kd"), 2)), ("Tax rate", pct(W("tax"), 0)),
        ("After-tax cost of debt", pct(W("kd_at"), 2), "bold"),
        ("Capital structure", "", "head"),
        ("Target D / (D+E)", pct(W("dv"), 0)), ("Target E / (D+E)", pct(W("ev_w"), 0)),
        ("WACC", pct(W("wacc"), 2), "bold"),
    ], size=8.5, h=0.215)
    table(s, x, 1.82, w, rows, [3.2, 1.6])
    text(s, x, 5.35, w, 0.2, ct("beta_header", "Peer betas (2y weekly, Blume-adjusted)"), size=9, bold=True, color=NAVY)
    brows = [dict(cells=["Peer", "Raw β", "Adj. β", "D/E", "Unlev. β"], fill=NAVY, color=WHITE, bold=True, size=8,
                  h=0.2)]
    peers = [(d.v("WACC", f"G{r}"), d.v("WACC", f"I{r}"), d.v("WACC", f"J{r}"), d.v("WACC", f"K{r}"),
              d.v("WACC", f"M{r}")) for r in range(6, 14)]
    for i in range(0, 8, 2):
        pair = peers[i:i + 2]
        for p in pair:
            pass
    # compact: show median row plus 4 peers with the most weight on the story
    for p in peers[:4]:
        brows.append(dict(cells=[p[0], f"{p[1]:.2f}", f"{p[2]:.2f}", pct(p[3], 0), f"{p[4]:.2f}"], size=8, h=0.19,
                          line_bottom="E1E5EA"))
    brows.append(dict(cells=["Median (8 peers)", f"{d.v('WACC', 'I14'):.2f}", f"{d.v('WACC', 'J14'):.2f}",
                             pct(d.v('WACC', 'K14'), 0), f"{d.v('WACC', 'M14'):.2f}"], size=8, h=0.2, bold=True,
                      fill="E4EEF2"))
    table(s, x, 5.58, w, brows, [1.6, 0.8, 0.8, 0.8, 0.85])
    # drivers table
    rx, rw = 5.62, 7.25
    panel_header(s, rx, 1.38, rw, "Base case forecast drivers", None)
    yrs = d.years(FC)
    rows = [dict(cells=["", "Hist. 3y"] + yrs, fill=NAVY, color=WHITE, bold=True, size=8, h=0.24,
                 fills={1: "8C96A0"})]
    segs = [d.c("Inputs", k) for k in ("seg_a", "seg_b", "seg_c")]
    if d.c("Inputs", "rev_mode") == 2:
        rev_spec = ([("Revenue drivers (location mode)", None)]
                    + [(f"Like-for-like – {sg}", f"b_lfl_{k}") for sg, k in zip(segs, "abc")]
                    + [(f"Net new locations – {sg}", f"b_net_{k}") for sg, k in zip(segs, "abc")]
                    + [(f"Price/mix – {sg}", f"b_px_{k}") for sg, k in zip(segs, "abc")])
        inv_spec = [("Maintenance capex (% of revenue)", "b_mcapex"), ("Capex per new location (NOKm)", "b_capex_loc")]
        cost_spec = [("Cost inflation, fixed costs and rent", "b_cpi")]
    else:
        rev_spec = ([("Revenue drivers (segment mode)", None)]
                    + [(f"Volume growth – {sg}", f"b_vol_{k}") for sg, k in zip(segs, "abc")]
                    + [(f"Price/mix – {sg}", f"b_px_{k}") for sg, k in zip(segs, "abc")])
        inv_spec = [("Maintenance capex (% of revenue)", "b_mcapex"), ("Sales-to-capital, growth capex (x)", "b_s2c")]
        cost_spec = [("Cost inflation, fixed cost base", "b_cpi"), ("Real growth, fixed cost base", "b_fix_real"),
                     ("Lease payments (IFRS 16)", "b_lease")]
    spec = (rev_spec + [("Costs", None), ("COGS (% of revenue)", "b_cogs"), ("Personnel, variable (% of rev.)¹", "b_pers_var"),
                        ("Other opex, variable (% of rev.)¹", "b_oth_var")] + cost_spec + [("D&A (owned assets)", "b_da"),
                        ("Investments and other", None)] + inv_spec + [("NWC (% of revenue)", "b_nwc"), ("Tax rate", "b_tax"),
                        ("Dividend payout ratio", "b_payout")])
    for lab, key in spec:
        if key is None:
            rows.append(dict(cells=[lab] + [""] * 9, bold=True, color=NAVY, size=7.5, h=0.18, line_bottom=NAVY))
            continue
        r = d.reg["rows"][f"Drivers|{key}"]
        hist = d.v("Drivers", f"T{r}")                       # 3-year historical average (column T on Drivers)
        vals = [d.v("Drivers", f"{c}{r}") for c in FC]
        f_ = ((lambda v: f"{v:.1f}x") if key == "b_s2c" else (lambda v: f"{v:.0f}") if key.startswith("b_net_")
              else (lambda v: f"{v:.1f}") if key == "b_capex_loc" else pct)
        rows.append(dict(cells=[lab, f_(hist) if isinstance(hist, (int, float)) else "–"] + [f_(v) for v in vals],
                         size=7.5, h=0.163, line_bottom="EEF0F3", fills={1: "F2F3F5"}))
    table(s, rx, 1.82, rw, rows, [2.0, 0.62] + [0.58] * 8)
    tg, ronic, ex_ = d.c("DCF", "tv_g"), d.c("DCF", "tv_ronic"), d.c("DCF", "tv_mult")
    pw = 3.0
    panel(s, rx, 5.95, pw, 0.9)
    text(s, rx + 0.12, 5.99, pw - 0.24, 0.84, [
        ("Terminal assumptions", {"bold": True, "color": NAVY, "size": 9, "space_after": 2}),
        (f"Growth {tg * 100:.1f}% • RONIC {ronic * 100:.0f}% • EBIT margin {d.row('DCF', 'ebit_m', ['S'])[0] * 100:.1f}% "
         f"(final year) • Tax 22% • Exit cross-check {mult(ex_)} EV/EBITDAaL", {"size": 8}),
    ], size=8)
    # the personnel-cost ratio is the judgement the forecast hinges on – show it and what it costs if we are wrong
    px, pxw = rx + pw + 0.1, rw - pw - 0.1
    pr = d.reg["rows"]
    pers_h = [d.v("Hist", f"{c}{pr['Hist|pers_pct']}") for c in ("I", "K")]
    pers_f = [-a / b for a, b in zip(d.row("Model", "pers", [FC[0], FC[-1]]), d.row("Model", "is_rev", [FC[0], FC[-1]]))]
    y1, yl = d.years([FC[0]])[0], d.years([FC[-1]])[0]
    ya3, ya = d.years([HC[-3]])[0], d.years([HC[-1]])[0]
    line1 = (f"{pers_h[0] * 100:.1f}% of revenue in {ya3}, {pers_h[1] * 100:.1f}% in {ya}; base case {pers_f[0] * 100:.1f}% in {y1} "
             f"falling to {pers_f[1] * 100:.1f}% by {yl} as ~{d.c('Drivers', 'pers_fixsh') * 100:.0f}% of it is fixed per club.")
    wi = _whatif()
    key = next((k for k in wi if k.startswith("Personnel ratio stays")), None)
    paras = [("Personnel costs – the key judgement", {"bold": True, "color": NAVY, "size": 9, "space_after": 2}), (line1, {"size": 8})]
    if key and isinstance(wi[key].get("dcf"), (int, float)):
        dv = wi[key]["dcf"] - d.c("DCF", "dcf_ps")
        paras.append((f"If the {ya} ratio persisted (all personnel costs variable): DCF NOK {wi[key]['dcf']:.0f} per share "
                      f"({dv:+.0f}), rating {wi[key]['rating']}.", {"size": 8, "bold": True}))
    panel(s, px, 5.95, pxw, 0.9, fill="FFF4D6")
    text(s, px + 0.12, 5.99, pxw - 0.24, 0.84, paras, size=8)
    text(s, rx, 5.72, rw, 0.2, "¹ History shows the total cost ratio; the fixed part (Drivers E) grows with inflation and "
                                "the number of locations instead of with revenue.", size=7, italic=True, color=MUTED)
    notes(s, "TEMPLATE: Drivers come from the Drivers sheet (section A) with the 3-year historical average for "
             "reference. Explain any driver that deviates from history.")
    return s


# ------------------------------------------------------------------ A5 risks
RISKS = [
    ("Pricing pressure", "Low-cost competitors could cap price increases and raise churn.", 3, 3),
    ("Consumer slowdown", "Higher rates and inflation could reduce discretionary spending.", 2, 3),
    ("Cost inflation", "Wage and energy inflation could delay margin expansion.", 3, 2),
    ("Execution on growth", "New locations and digital products may ramp up slower than planned.", 2, 2),
    ("Leverage and M&A", "Large acquisitions could add integration risk and debt.", 1, 2),
]
RISKS = ct("risks", RISKS)


def risks_slide(prs, d):
    t4 = {k: c for c, k, _, _ in d.reg["t4"]}
    r0 = d.reg["sens"]["t4_rows"][0]
    bear = d.v("Sensitivity", f"{t4['dcf_ps']}{r0}")
    price = d.c("Inputs", "price")
    s = std(prs, "Appendix #4.12", "Key risks",
            f"{'Risks are manageable' if abs(bear / price - 1) < d.c('DCF', 'tp_up') else 'Operating leverage cuts both ways'}"
            f" – our bear case DCF of NOK {bear:.0f} is {abs(bear / price - 1) * 100:.0f}% below "
            f"today's share price, against {d.c('DCF', 'tp_up') * 100:.0f}% upside to our target price",
            "Sources: Case team assessment. Probability and impact are qualitative (1 = low, 3 = high).")
    x, w = 0.47, 5.9
    panel(s, x, 1.45, w, 5.35)
    for i, (title, desc, prob, imp) in enumerate(RISKS):
        yy = 1.70 + i * 1.0
        circle(s, x + 0.25, yy, 0.46, fill=NAVY, txt=str(i + 1), font_size=13)
        text(s, x + 0.9, yy - 0.04, w - 1.1, 0.3, title, size=12.5, bold=True, color=NAVY)
        text(s, x + 0.9, yy + 0.26, w - 1.1, 0.55, desc, size=10, color=DARK)
    # risk matrix
    mx, my, cell = 7.60, 1.60, 1.55
    colors = {2: "7DBB7E", 3: "C7D66D", 4: "F2C94C", 5: "F0994A", 6: "D9534F"}
    for pi in range(3):          # probability rows (top = high)
        for ii in range(3):      # impact columns (right = high)
            prob, imp = 3 - pi, ii + 1
            rect(s, mx + ii * (cell + 0.05), my + pi * (cell + 0.05), cell, cell, fill=colors[prob + imp])
    for i, (title, desc, prob, imp) in enumerate(RISKS):
        same = [j for j, r in enumerate(RISKS) if (r[2], r[3]) == (prob, imp)]
        k = same.index(i)
        cxp = mx + (imp - 1) * (cell + 0.05) + cell / 2 - 0.23 + (k - (len(same) - 1) / 2) * 0.55
        cyp = my + (3 - prob) * (cell + 0.05) + cell / 2 - 0.23
        circle(s, cxp, cyp, 0.46, fill=NAVY, txt=str(i + 1), font_size=13, line_col=WHITE)
    gw = 3 * cell + 0.1
    for ii, lab in enumerate(["Low", "Medium", "High"]):
        text(s, mx + ii * (cell + 0.05), my + gw + 0.04, cell, 0.22, lab, size=9, color=MUTED, align="c")
    text(s, mx, my + gw + 0.30, gw, 0.3, "Impact →", size=11, bold=True, color=DARK, align="c")
    tb = text(s, mx - 1.85, my + gw / 2 - 0.15, 1.6, 0.3, "Probability →", size=11, bold=True, color=DARK, align="c")
    tb.rotation = 270
    for pi, lab in enumerate(["High", "Medium", "Low"]):
        text(s, mx - 0.62, my + pi * (cell + 0.05) + cell / 2 - 0.11, 0.55, 0.22, lab, size=9, color=MUTED, align="r")
    notes(s, "TEMPLATE: Replace with company-specific risks and place them on the matrix (probability, impact). Link "
             "each major risk to the bear case so the audience sees it is priced in.")
    return s


# ------------------------------------------------------------------ guide
def guide_slide(prs, d):
    s = std(prs, "Delete this slide before submission", "How to use this template",
            "From case files to a finished pitch – every number flows from the Excel model (Equity_Research_DCF_Toolkit.xlsx)",
            "Built for Pareto-style equity research cases. Example Company ASA and all market data are fictional.")
    x, w = 0.47, 7.0
    panel_header(s, x, 1.38, w, "Workflow", None)
    steps = [
        ("Fill the model", "Inputs → Hist (paste the case 'Model' sheet using the mapping on the Guide tab) → WACC → Comps."),
        ("Set your view", "Drivers: base case per year, Bear/Bull adjustments, probabilities and terminal assumptions."),
        ("Check the model", "Checks tab must show ALL CHECKS OK. Understand every warning and switch back to Base."),
        ("Update the deck numbers", "Re-run the deck builder, or copy from the Deck_Feed tab into the tables and charts "
                                    "(right-click chart → Edit Data)."),
        ("Write the story", "Replace headlines with your own action titles – one message per slide, backed by numbers."),
        ("Final polish", "Sources on every slide, consistent units, speaker notes rehearsed, appendix ready for Q&A."),
    ]
    for i, (t, dsc) in enumerate(steps):
        yy = 1.95 + i * 0.80
        circle(s, x + 0.05, yy, 0.46, fill=NAVY if i % 2 == 0 else MIDBLUE, txt=str(i + 1), font_size=13)
        text(s, x + 0.7, yy - 0.03, w - 0.8, 0.26, t, size=11.5, bold=True, color=NAVY)
        text(s, x + 0.7, yy + 0.22, w - 0.8, 0.5, dsc, size=9.5, color=DARK)
    rx, rw = 7.85, 5.02
    panel_header(s, rx, 1.38, rw, "Submission checklist", None)
    panel(s, rx, 1.82, rw, 5.0)
    checks = [
        "Presentation in **English**",
        "**Headings unchanged:** Company overview, Market overview, Financials and estimates, Valuation and "
        "recommendation",
        "**Max 4 content slides** (cover and case-team slide not counted)",
        "**Buy / Hold / Sell** and a **target price** clearly stated",
        "**Excel model attached** – Checks tab shows ALL CHECKS OK",
        "Every number in the deck **matches the model** (scenario = Base)",
        "**Sources** cited on every slide",
        "Delete this slide and all [placeholders]",
    ]
    for i, c in enumerate(checks):
        yy = 2.00 + i * 0.58
        box = rect(s, rx + 0.2, yy + 0.03, 0.22, 0.22, fill=WHITE, line=NAVY, line_w=1.25)
        text(s, rx + 0.55, yy, rw - 0.75, 0.5, c, size=10, color=DARK)
    notes(s, "Delete this slide before submitting.")
    return s
