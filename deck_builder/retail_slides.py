"""Retail-case slides (used when the case text module provides the keys): market overview for a store chain, store
economics, company targets vs. the model (in place of the consensus slide) and the cash picture of a roll-out."""
from deck_core import *
from deck_data import num, pct, mult, HC, FC
from deck_slides1 import std
from deck_case import ct
from cl_core import waterfall

PALE = "D6E6EC"


def _isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _hdr(cells, h=0.24, size=8, first_grey=False, aligns=None):
    r = dict(cells=cells, fill=NAVY, color=WHITE, bold=True, size=size, h=h,
             align=aligns or {j: "c" for j in range(1, len(cells))})
    if first_grey:
        r["fills"] = {1: "8C96A0"}
    return r


# ------------------------------------------------------------------ 4 market overview (retail)
def market_overview_retail(prs, d):
    M = ct("market_retail")
    s = std(prs, M["chapter"], "Market overview", M["subtitle"], M["sources"])
    gx = [(0.47, 3.95), (4.67, 3.95)]
    y1, y2 = 1.40, 4.18
    # 1 sports retail market
    x, w = gx[0]
    panel_header(s, x, y1, w, "Norwegian sports retail market (NOKbn)", 1)
    panel(s, x, y1 + 0.42, w, 2.35)
    cats = [c for c, _ in M["sports"]]
    vals = [v for _, v in M["sports"]]
    add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, x + 0.1, y1 + 0.5, w - 0.2, 1.75, cats, [("Market", vals)],
              [LBLUE], size=7.5, legend=None, labels=True, num_fmt="0.0", label_pos=XL_LABEL_POSITION.OUTSIDE_END,
              gap=60, val_min=0, val_max=max(vals) * 1.25)
    gf = s.shapes[-1]
    color_points(gf.chart, [LBLUE] * (len(vals) - 1) + [NAVY])
    text(s, x + 0.1, y1 + 2.28, w - 0.2, 0.45, M["sports_note"], size=7, italic=True, color=MUTED)
    # 2 where Sport Outlet sits
    x, w = gx[1]
    panel_header(s, x, y1, w, "Where Sport Outlet sits", 2)
    panel(s, x, y1 + 0.42, w, 2.35)
    gf = add_chart(s, XL_CHART_TYPE.DOUGHNUT, x + 0.05, y1 + 0.5, 1.45, 1.45, [n for n, _ in M["share"]],
                   [("Share", [v for _, v in M["share"]])], [NAVY], size=7, legend=None, labels=True, num_fmt="0%")
    ch = gf.chart
    pl = ch.plots[0]
    pl.vary_by_categories = True
    dl = pl.data_labels
    dl.show_percentage = True
    dl.show_value = False
    dl.number_format = "0%"
    dl.font.color.rgb = rgb(WHITE)
    dl.font.bold = True
    for i, col in enumerate([NAVY, "D0D7DD"]):
        pt = pl.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(col)
    doughnut_hole(ch, 55)
    text(s, x + 0.33, y1 + 1.02, 0.9, 0.4, M["share_centre"], size=8, bold=True, color=NAVY, align="c", anchor="m")
    text(s, x + 1.55, y1 + 0.52, w - 1.65, 2.2, [(t, {"bullet": True, "space_after": 3}) for t in M["competitors"]], size=8)
    # 3 toys market
    x, w = gx[0]
    panel_header(s, x, y2, w, "Kids Outlet: a fragmented toy market", 3)
    panel(s, x, y2 + 0.42, w, 2.2)
    T = M["toys"]
    text(s, x + 0.12, y2 + 0.5, w - 0.24, 2.1, [
        (f"**Specialist toys, arts and crafts market:** {T['size']} (2025), growing {T['growth']}", {"bullet": True, "space_after": 4}),
        (f"**Players:** {T['players']}", {"bullet": True, "space_after": 4}),
        (f"**Why value works here:** {T['note']}", {"bullet": True}),
    ], size=8.5)
    # 4 store runway
    x, w = gx[1]
    panel_header(s, x, y2, w, "Store runway", 4)
    panel(s, x, y2 + 0.42, w, 2.2)
    cats = [r[0] for r in M["runway"]]
    today = [r[1] for r in M["runway"]]
    pot = [r[2] - r[1] for r in M["runway"]]
    gf = add_chart(s, XL_CHART_TYPE.BAR_STACKED, x + 0.1, y2 + 0.5, w - 0.2, 1.65, cats,
                   [("Stores today", today), ("Potential (midpoint)", pot)], [NAVY, PALE], size=7.5, legend="t", labels=True,
                   num_fmt="0", label_pos=XL_LABEL_POSITION.CENTER, gap=45, overlap=100, label_color=WHITE)
    series_labels_off(gf.chart, 1)
    set_cat_reverse(gf.chart)
    text(s, x + 0.1, y2 + 2.15, w - 0.2, 0.42, " · ".join(f"{r[0].split(',')[0]}: {r[3]}" for r in M["runway"]), size=7, italic=True, color=MUTED)
    # right-hand boxes
    bx, bw = 8.87, 4.00
    yy = 1.40
    for title, items, fill in zip([b[0] for b in M["boxes"]], [b[1] for b in M["boxes"]], [NAVY, MIDBLUE, LBLUE]):
        hb = rect(s, bx, yy, bw, 0.36, fill=fill)
        shape_text(hb, title, size=11, bold=True)
        n = len(items)
        h = 0.22 + 0.42 * n
        panel(s, bx, yy + 0.40, bw, h)
        text(s, bx + 0.12, yy + 0.46, bw - 0.24, h - 0.08, [(t, {"bullet": True, "space_after": 3}) for t in items], size=8)
        yy += 0.40 + h + 0.08
    notes(s, "TALKING POINT: the market grows 2-3% a year – the case does not need market growth. It needs share gains from the "
             "value position (Sport Outlet) and white space in a fragmented market (Kids Outlet). The runway chart is the roll-out "
             "thesis in one picture.")
    return s


# ------------------------------------------------------------------ store economics
def store_economics_slide(prs, d):
    E = ct("store_econ")
    yf = d.years(FC)
    opens_a = d.row("Model", "net_a", FC)
    opens_b = d.row("Model", "net_b", FC)
    opens_c = d.row("Model", "net_c", FC)
    rpu_a = d.row("Model", "rpu_a", [HC[-1]] + FC)
    rpu_b = d.row("Model", "rpu_b", FC)
    gm = d.row("Model", "gm", FC)
    rev30 = d.row("Model", "is_rev", [FC[4]])[0]
    m30 = d.row("Model", "ebit_m", [FC[4]])[0]
    pay = d.row("Drivers", "payout", FC)
    lev = d.row("Model", "lev", FC)
    mcap = d.row("Model", "capex_m", FC[:4])
    s = std(prs, "Appendix #4.7", "Store economics – Sport Outlet and Kids Outlet",
            f"A store costs NOK 1-1.5m to fit out and NOK 3-5m to stock; we open {sum(opens_a[:5]) + sum(opens_b[:5]) + sum(opens_c[:5]):.0f} "
            f"stores by {yf[4]} and stay below the company's targets", E["sources"])
    # left: unit economics table
    x, w = 0.47, 6.1
    panel_header(s, x, 1.38, w, "Unit economics per store", None)
    rows = [_hdr(["", "Sport Outlet", "Kids Outlet"], h=0.26, size=8.5, aligns={1: "l", 2: "l"})]
    for lab, a, b in E["unit"]:
        rows.append(dict(cells=[lab, a, b], size=8, h=0.245, line_bottom="E1E5EA", bolds={0: True}))
    table(s, x, 1.82, w, rows, [1.75, 2.15, 2.2], align=["l", "l", "l"])
    # right: revenue per store chart
    rx, rw = 6.77, 6.1
    panel_header(s, rx, 1.38, rw, "Revenue per store (NOKm) – base case", None)
    cats = [d.years([HC[-1]])[0]] + yf[:5]
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, rx, 1.80, rw, 2.2, cats,
                   [("Sport Outlet Norway", rpu_a[:6]), ("Kids Outlet", [None] + rpu_b[:5])], [NAVY, LBLUE], size=7.5,
                   legend="t", labels=True, num_fmt="0.0", label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=60, overlap=-10,
                   val_min=0, val_max=max(rpu_a[:6]) * 1.3)
    text(s, rx, 4.02, rw, 0.45, "Sport Outlet: revenue per store-year incl. online. Kids Outlet 2025 covered one quarter (nine stores opened "
                                "September-December); 2026E restates it to a full year and ramps new stores at 50% in the opening year.",
         size=7, italic=True, color=MUTED)
    # bottom: company guidance vs our model
    y0 = 4.48
    panel_header(s, 0.47, y0, 12.40, "The prospectus targets vs. our base case", None)
    G = E["guidance"]
    kids_pace = f"{opens_b[1]:.0f} in {yf[1]} falling to {opens_b[-1]:.0f} a year by {yf[-1]}"
    spec = [("Sport Outlet openings", G["openings_so"], f"{opens_a[0]:.0f} in {yf[0]}, then {opens_a[1]:.0f} a year – {d.row('Model', 'loc_a', [FC[-1]])[0]:.0f} stores by {yf[-1]}"),
            ("Kids Outlet openings", G["openings_kids"], f"{opens_b[0]:.0f} in {yf[0]}, {kids_pace} – {d.row('Model', 'loc_b', [FC[-1]])[0]:.0f} stores by {yf[-1]}"),
            ("Poland", G["poland"], f"{opens_c[2]:.0f} a year from {yf[2]} – {d.row('Model', 'loc_c', [FC[-1]])[0]:.0f} stores by {yf[-1]} at ~NOK {rpu_b[2]:.0f}m each (EST)"),
            ("Like-for-like / gross margin", f"{G['lfl']}; {G['brands']}", f"Revenue per store +{d.row('Model', 'px_a', [FC[1]])[0] * 100:.0f}% in {yf[1]} fading to 3%; gross margin {gm[0] * 100:.1f}% → {gm[3] * 100:.1f}%"),
            ("Revenue and EBIT margin", f"{G['revenue']}; {G['margin']}", f"NOK {rev30 / 1000:.1f}bn in {yf[4]} at a {m30 * 100:.1f}% EBIT margin (IFRS 16)"),
            ("Capital", f"{G['payout']}; {G['warehouse']}", f"Payout {pay[0] * 100:.0f}% → {pay[-1] * 100:.0f}%; warehouse capex NOK {-sum(mcap) - 0:,.0f}m incl. refurbishment 2026-29E; leverage peaks at {max(lev):.1f}x")]
    rows = [dict(cells=["", "Company (prospectus, September 2026)", "Our model (base case)"], fill=NAVY, color=WHITE, bold=True, size=8.5, h=0.26)]
    for lab, co, us in spec:
        rows.append(dict(cells=[lab, co, us], size=8, h=0.285, line_bottom="E1E5EA", bolds={0: True}))
    table(s, 0.47, y0 + 0.42, 12.40, rows, [1.7, 5.0, 5.7], align=["l", "l", "l"])
    notes(s, "TALKING POINT: the roll-out is cheap per store but not free – a Kids Outlet store needs NOK 2.5-3m of inventory for "
             "NOK 0.95m of fit-out. Growth is paid for in working capital, which is why free cash flow lags EBIT.")
    return s


# ------------------------------------------------------------------ targets vs model (in place of consensus)
def targets_slide(prs, d):
    Tg = ct("targets")
    C = lambda k: d.c("Consensus", k)
    yf = d.years(FC)
    s = std(prs, "Appendix #4.5", "What the company targets – and what we model", Tg["subtitle"], Tg["sources"])
    x, w = 0.47, 12.40
    panel_header(s, x, 1.38, w, "Prospectus financial targets vs. our base case", None)
    rev = d.row("Model", "is_rev", FC)
    ebit_m = d.row("Model", "ebit_m", FC)
    ebit_adj_m = d.row("Model", "ebit_adj_m", FC)
    gm = d.row("Model", "gm", FC)
    loc_a, loc_b, loc_c = (d.row("Model", k, FC) for k in ("loc_a", "loc_b", "loc_c"))
    lev = d.row("Model", "lev", FC)
    pay = d.row("Drivers", "payout", FC)
    px = d.row("Model", "px_a", FC)
    hdr = _hdr(["Target", "Company", f"Ours {yf[1]}", f"Ours {yf[4]}", f"Ours {yf[-1]}", "Comment"], h=0.27, size=8.5,
               aligns={1: "l", 2: "c", 3: "c", 4: "c", 5: "l"})
    rows = [hdr]
    spec = [("Revenue (mid-term)", "NOK 4.5-5.0bn", *(f"NOK {rev[i] / 1000:.2f}bn" for i in (1, 4, 7)), "We reach the lower end in 2031E"),
            ("EBIT margin (IFRS 16)", "High teens", *(f"{ebit_m[i] * 100:.1f}%" for i in (1, 4, 7)), "Pre-IFRS 16: " + " / ".join(f"{ebit_adj_m[i] * 100:.1f}%" for i in (1, 4, 7))),
            ("Like-for-like, Sport Outlet", "4-6% a year", *(f"{px[i] * 100:.1f}%" for i in (1, 4, 7)), "Revenue per store; fades to 3% by 2031E"),
            ("Gross margin (own brands to 65%)", "n.a.", *(f"{gm[i] * 100:.1f}%" for i in (1, 4, 7)), "47.8% in 2023, 52.3% in H1 2026"),
            ("Sport Outlet stores, Norway", "~5 openings a year", *(f"{loc_a[i]:.0f}" for i in (1, 4, 7)), "160-180 possible"),
            ("Kids Outlet stores", "15-20 openings a year", *(f"{loc_b[i]:.0f}" for i in (1, 4, 7)), "110-140 possible"),
            ("Sport Outlet stores, Poland", "5-10 a year if the pilot succeeds", *(f"{loc_c[i]:.0f}" for i in (1, 4, 7)), "Decision in 2027"),
            ("Dividend payout", "50-80% of net income", *(f"{pay[i] * 100:.0f}%" for i in (1, 4, 7)), "Lower while the warehouse is built"),
            ("Net debt / EBITDA (ex IFRS 16)", "< 1.0x at year end", *(f"{lev[i]:.1f}x" for i in (1, 4, 7)), "Breached in the build years in our numbers")]
    for cells in spec:
        rows.append(dict(cells=list(cells), size=8.5, h=0.27, line_bottom="E1E5EA", bolds={0: True},
                         align={1: "l", 2: "c", 3: "c", 4: "c", 5: "l"}))
    table(s, x, 1.82, w, rows, [2.3, 2.2, 1.15, 1.15, 1.15, 4.45], align=["l", "l", "c", "c", "c", "l"])
    text(s, x, 4.62, w, 0.4, Tg["note"], size=8, italic=True, color=MUTED)
    # variant perception cards (from the Consensus sheet)
    y0 = 5.05
    panel_header(s, x, y0, w, "Our variant perception – where we differ from the IPO story", None)
    n = sum(1 for j in range(1, 6) if f"Consensus|vp{j}_topic" in d.reg["cells"])
    bw = (w - 0.15 * (n - 1)) / n
    for j in range(1, n + 1):
        bx = x + (j - 1) * (bw + 0.15)
        hb = rect(s, bx, y0 + 0.44, bw, 0.3, fill=NAVY)
        shape_text(hb, f"{j}. {C(f'vp{j}_topic')}", size=9.5, bold=True, align="l", margin=0.1)
        panel(s, bx, y0 + 0.76, bw, 1.12)
        paras = [(f"**We:** {C(f'vp{j}_ours')}", {"space_after": 2}), (f"**IPO story:** {C(f'vp{j}_cons')}", {"space_after": 2}),
                 (f"**Proof – and when:** {C(f'vp{j}_when')}", {})]
        text(s, bx + 0.08, y0 + 0.8, bw - 0.16, 1.08, paras, size=7.5)
    notes(s, "TALKING POINT: with no consensus, the discipline is to compare against the company's own targets and the price. "
             "We are below the targets on margin and timing, not on the direction.")
    return s


# ------------------------------------------------------------------ cash picture of a roll-out
def cash_slide_retail(prs, d):
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
    ebitdaal = sum(O("ebitdaal", cols5))
    tax = sum(O("cf_tax", cols5)); fin = sum(O("cf_fin", cols5)); nwc = sum(O("cf_nwc", cols5))
    capex = sum(O("cf_capex", cols5)); div = sum(O("cf_div", cols5)); other = sum(O("cf_other", cols5)) + sum(O("cf_other_op", cols5)) + sum(O("cf_special", cols5))
    nibd0, nibd5 = O("nibd", [HC[-1]])[0], O("nibd", [FC[4]])[0]
    s = std(prs, "Appendix #4.8", "From revenue growth to cash – a roll-out eats cash first",
            f"Revenue +NOK {rev3 - rev0:,.0f}m by {y3} adds NOK {e3 - e0:,.0f}m of EBITDAaL; the build absorbs it – "
            f"net debt NOK {nibd0:,.0f}m → {nibd5:,.0f}m by {y5}",
            ct("cash_sources", "Sources: Case estimates (Excel model)."))
    x, w = 0.47, 6.1
    panel_header(s, x, 1.38, w, f"EBITDAaL bridge {ya} → {y3} (NOKm)", None)
    steps = [(f"EBITDAaL {ya}", e0, "total")] + [(lab, v, "delta") for lab, v in deltas] + [(f"EBITDAaL {y3}", e3, "total")]
    waterfall(s, (x, 1.80, w, 2.45), steps, size=7.5, plot=(0.02, 0.08, 0.96, 0.74))
    g_rev = (rev3 / rev0) ** (1 / 3) - 1
    text(s, x, 4.20, w, 0.25, f"Revenue CAGR {g_rev * 100:.1f}%; EBITDAaL margin {e0 / rev0 * 100:.1f}% → {e3 / rev3 * 100:.1f}% – store costs scale with "
                                f"sales, rent and the fixed base with inflation and new-store revenue", size=7.5, italic=True, color=MUTED)
    rx, rw = 6.77, 6.1
    panel_header(s, rx, 1.38, rw, f"Sources and uses of cash {str(y1)[:4]}–{str(y5)[2:4]}E (NOKm, cumulative)", None)
    debt_up = nibd5 - nibd0
    items = [("EBITDAaL", ebitdaal, 0.0, NAVY), ("Net debt raised", max(debt_up, 0.0), 0.0, MIDBLUE),
             ("Tax", 0.0, -tax, "C9D1D9"), ("Interest", 0.0, -fin, "A9C8D3"), ("Working capital", 0.0, -nwc, LBLUE),
             ("Capex incl. warehouse", 0.0, -capex, "4F7FA0"), ("Dividends", 0.0, -div, RED)]
    if abs(other) > 0.5:
        items.append(("Other", max(other, 0.0), max(-other, 0.0), "8C96A0"))
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_STACKED, rx, 1.80, rw, 2.45, ["Sources", "Uses"],
                   [(lab, [a, b]) for lab, a, b, _ in items], [c for _, _, _, c in items], size=7.5, legend="r", labels=True,
                   num_fmt="#,##0;-#,##0;", label_pos=XL_LABEL_POSITION.CENTER, gap=80, overlap=100, label_color=WHITE)
    text(s, rx, 4.20, rw, 0.25, f"Net debt rises by NOK {debt_up:,.0f}m over the five years; dividends are paid the year after they are earned.",
         size=7.5, italic=True, color=MUTED)
    # bottom table
    y0 = 4.55
    panel_header(s, 0.47, y0, 12.40, "Cash flow and leverage – base case", None)
    tcols = [HC[-1]] + cols5
    rows = [_hdr([""] + d.years(tcols), first_grey=True)]
    spec = [("EBITDAaL (NOKm)", O("ebitdaal", tcols), lambda v: f"{v:,.0f}", True),
            ("Change in working capital", O("cf_nwc", tcols), lambda v: f"{v:,.0f}", False),
            ("Capex incl. the new warehouse", O("cf_capex", tcols), lambda v: f"{v:,.0f}", False),
            ("Free cash flow to equity", O("fcfe", tcols), lambda v: f"{v:,.0f}", True),
            ("Dividends paid", O("cf_div", tcols), lambda v: f"{v:,.0f}", False),
            ("Net debt, year end (ex leases)", O("nibd", tcols), lambda v: f"{v:,.0f}", False),
            ("NIBD / EBITDAaL (x)", d.row("Model", "lev", tcols), lambda v: f"{v:.1f}x", True)]
    for lab, vals, f_, bold in spec:
        rows.append(dict(cells=[lab] + [("–" if not _isnum(v) else f_(v)) for v in vals], size=8.5, h=0.225, line_bottom="E1E5EA",
                         bolds={0: bold}, align={j: "c" for j in range(1, 7)}, fills={1: "F2F3F5"}))
    table(s, 0.47, y0 + 0.44, 8.4, rows, [3.0] + [0.9] * 6)
    panel(s, 9.10, y0 + 0.44, 3.77, 1.82)
    nwc_pct = d.row("Drivers", "nwc", [FC[0], FC[4]])
    text(s, 9.22, y0 + 0.50, 3.55, 1.75, [
        ("Why cash lags profit", {"bold": True, "color": NAVY, "size": 10, "space_after": 3}),
        (f"Inventory: working capital is {nwc_pct[0] * 100:.0f}% of revenue – every NOK 100m of growth ties up NOK {nwc_pct[0] * 100:.0f}m; "
         f"we take it to {nwc_pct[1] * 100:.0f}% as Kids Outlet (lighter stock) grows and the warehouse automates.", {"bullet": True, "space_after": 2}),
        ("The NOK ~1bn warehouse is 70% debt-financed per the prospectus; the IPO proceeds cover the equity part.", {"bullet": True, "space_after": 2}),
        ("Hence a payout at the lower end of 50-80% and leverage above the <1.0x target in 2027-29E – unless the roll-out slows.", {"bullet": True}),
    ], size=8.5)
    notes(s, "TALKING POINT: the equity story is high growth with high payout and low leverage. Our numbers say two of the three hold at a "
             "time while the warehouse is built. That is the tension to watch in the 2027 capex guidance and the dividend proposals.")
    return s
