"""Financials and estimates, valuation and recommendation."""
from deck_core import *
from deck_data import num, pct, mult, HC, FC
from deck_slides1 import std
from deck_case import ct

FIN_COLS = HC[4:] + FC[:5]          # 2023A..2030E


def fin_table_rows(d, cols, lines, size=8.5, h=0.2, fc_start=3):
    yrs = d.years(cols)
    rows = [dict(cells=[""] + yrs, fill=NAVY, color=WHITE, bold=True, size=size, h=h + 0.03,
                 fills={j + 1: (MIDBLUE if j >= fc_start else NAVY) for j in range(len(cols))})]
    for lab, key, f, style in lines:
        vals = d.row("Model", key, cols) if key else [None] * len(cols)
        cells = [lab] + [f(v) if key else "" for v in vals]
        r = dict(cells=cells, size=size, h=h)
        if style == "bold":
            r.update(bold=True, line_top=GRIDGREY)
        elif style == "italic":
            r.update(italic=True, color=MUTED)
        r["fills"] = {j + 1: "EEF4F7" for j in range(fc_start, len(cols))}
        rows.append(r)
    return rows


def financials(prs, d):
    comp = d.c("Inputs", "company").split(" ASA")[0]
    rev = d.row("Model", "is_rev", ["K", "P"])
    cagr = (rev[1] / rev[0]) ** (1 / 5) - 1
    m25, m30 = d.row("Model", "ebit_adj_m", ["K", "P"])
    s = std(prs, "#3 Historical analysis and forecasts", "Financials and estimates",
            f"New locations, like-for-like and price drive a {cagr * 100:.1f}% revenue CAGR 2025–30E, with EBIT margins "
            f"expanding to {m30 * 100:.0f}%",
            "Sources: Company reports, case team estimates (see Excel model: Model, DCF and Comps sheets). Peer multiples: "
            "Bloomberg consensus as provided in the case material. Figures are illustrative.")
    # 1 financial summary table
    x, w = 0.47, 8.25
    panel_header(s, x, 1.38, w, "Financial summary (NOKm)", 1)
    lines = [("Revenue", "is_rev", num, "bold"), ("  Growth", "grev", pct, "italic"),
             ("EBITDA (reported)", "ebitda", num, "bold"), ("  Margin", "ebitda_m", pct, "italic"),
             ("EBIT adj.", "ebit_adj", num, "bold"), ("  Margin", "ebit_adj_m", pct, "italic"),
             ("Net profit to shareholders", "np_sh", num, None), ("EPS (NOK)", "eps", lambda v: num(v, 2), None),
             ("DPS (NOK)", "dps", lambda v: num(v, 2), None), ("Free cash flow to firm", "fcff", num, "bold"),
             ("ROIC", "roic", pct, None), ("NIBD / EBITDAaL (x)", "lev", lambda v: f"{v:.1f}x", None)]
    rows = fin_table_rows(d, FIN_COLS, lines, size=8.5, h=0.205)
    band_y = 1.80
    table(s, x, band_y + 0.22, w, rows, [1.9] + [0.79] * 8)
    colw = (w / (1.9 + 0.79 * 8)) * 0.79
    x0 = x + (w / (1.9 + 0.79 * 8)) * 1.9
    hb = rect(s, x0, band_y, colw * 3 - 0.02, 0.19, fill="8C96A0")
    shape_text(hb, "Historical", size=8, bold=True)
    fb = rect(s, x0 + colw * 3, band_y, colw * 5, 0.19, fill=LBLUE)
    shape_text(fb, "Forecast", size=8, bold=True)

    # 2 growth decomposition
    y2 = 4.78
    panel_header(s, 0.47, y2, 4.0, "Growth: new locations, like-for-like, price", 2)
    gcols = HC[4:] + FC[:5]
    gfg = add_chart(s, XL_CHART_TYPE.COLUMN_STACKED, 0.47, y2 + 0.42, 4.0, 1.72, d.years(gcols),
                    [("New locations", d.row("Model", "g_newc", gcols)), ("Like-for-like", d.row("Model", "g_lflc", gcols)),
                     ("Price/mix", d.row("Model", "g_pxc", gcols))],
                    [NAVY, MIDBLUE, LBLUE], size=7, legend="t", labels=True, num_fmt="0%",
                    label_pos=XL_LABEL_POSITION.CENTER, gap=45, overlap=100, label_color=WHITE)
    series_labels_off(gfg.chart, 1)
    hide_small_labels(gfg.chart, 0)
    hide_small_labels(gfg.chart, 2)
    # 3 scenario revenue paths
    panel_header(s, 4.72, y2, 4.0, "Revenue by scenario (NOKm)", 3)
    last = d.row("Model", "is_rev", ["K"])[0]
    yrs = [d.years(["K"])[0]] + d.years(FC)
    t4 = {k: c for c, k, _, _ in d.reg["t4"]}
    r0 = d.reg["sens"]["t4_rows"][0]
    paths = []
    for j, name in enumerate(["Bear", "Base", "Bull"]):
        vals = [last] + [d.v("Sensitivity", f"{t4[f'rev{i + 1}']}{r0 + j}") for i in range(8)]
        paths.append((name, vals))
    gf = add_chart(s, XL_CHART_TYPE.LINE, 4.72, y2 + 0.42, 4.0, 1.72, yrs, paths, [RED, NAVY, GREEN], size=7,
                   legend="t", labels=False, num_fmt="0", val_axis=True, gridlines=True,
                   val_min=round(last * 0.9, -3))
    ch = gf.chart
    ch.value_axis.tick_labels.number_format = "0"
    ch.value_axis.tick_labels.number_format_is_linked = False

    # 4 commentary
    rx, rw = 8.97, 3.90
    panel_header(s, rx, 1.38, rw, "Financial commentary", 4)
    panel(s, rx, 1.80, rw, 2.95)
    gn = d.row("Model", "g_newc", FC[:5])
    gl = d.row("Model", "g_lflc", FC[:5])
    gp = d.row("Model", "g_pxc", FC[:5])
    opens = sum(d.row("Model", "open", FC[:5]))
    capl = d.row("Drivers", "capex_loc", [FC[0]])[0]
    cx26 = -d.row("Model", "capex", [FC[0]])[0] / d.row("Model", "is_rev", [FC[0]])[0]
    cx25 = -d.row("Model", "capex", ["K"])[0] / d.row("Model", "is_rev", ["K"])[0]
    roic30 = d.row("Model", "roic", ["P"])[0]
    conv = d.row("Model", "cconv", FC[:5])
    bb = d.row("Model", "buyback", FC[:5])
    lev_t = d.c("Drivers", "lev_t")
    pay_l, pay_p = d.row("Model", "payout", ["L", "P"])
    mcap = d.c("Inputs", "mcap")
    wacc = d.c("WACC", "wacc")
    bullets = ct("fin_bullets")(d) if ct("fin_bullets") else [
        f"**{cagr * 100:.1f}% revenue CAGR** 2025–30E: new locations add ~{sum(gn) / 5 * 100:.1f}pp, like-for-like "
        f"~{sum(gl) / 5 * 100:.1f}pp and price/mix ~{sum(gp) / 5 * 100:.1f}pp p.a.",
        f"**Operating leverage** lifts EBIT adj. margin from {m25 * 100:.1f}% to {m30 * 100:.1f}% as fixed costs and rent grow "
        f"with inflation and locations, not with sales",
        f"**Growth is paid for:** {opens:.0f} openings at ~NOK {capl:.0f}m each lift capex to {cx26 * 100:.1f}% of sales "
        f"({cx25 * 100:.1f}% in 2025A)",
        f"**Highly cash generative:** ~{sum(conv) / 5 * 100:.0f}% of EBITDAaL converts to FCFF; negative working capital funds growth",
        f"**ROIC of {roic30 * 100:.0f}% by 2030E** – far above our {wacc * 100:.1f}% WACC",
        f"**Shareholder returns:** payout from {pay_l * 100:.0f}% to {pay_p * 100:.0f}%; cash above {lev_t:.2f}x "
        f"NIBD/EBITDAaL funds buybacks – NOK {-sum(bb):,.0f}m over 2026–30E",
    ]
    text(s, rx + 0.12, 1.88, rw - 0.24, 2.85, [(b, {"bullet": True, "space_after": 4}) for b in bullets], size=9)

    # 5 our estimates vs. consensus (or vs. the company's targets when there is no consensus)
    panel_header(s, rx, y2, rw, ct("fin_panel5", "Our estimates vs. consensus"), 5)
    if ct("targets_box"):
        trows = [dict(cells=["", "Ours", "Company"], fill=NAVY, color=WHITE, bold=True, size=8.5, h=0.25, align={1: "c", 2: "c"})]
        for lab, ours, tgt in ct("targets_box")(d):
            trows.append(dict(cells=[lab, ours, tgt], size=8, h=0.235, line_bottom="DDE1E5", align={1: "c", 2: "c"}, bolds={0: True}))
        table(s, rx, y2 + 0.45, rw, trows, [1.35, 1.3, 1.25])
        text(s, rx, y2 + 1.68, rw, 0.6, [(ct("fin_differ", ""), {})], size=7.5, color=DARK)
    else:
        yrs3 = d.years(FC[:3])
        crows = [dict(cells=["vs. consensus"] + yrs3, fill=NAVY, color=WHITE, bold=True, size=8.5, h=0.25,
                      align={1: "c", 2: "c", 3: "c"})]
        for m, lab in [("rev", "Revenue"), ("ebitda", "EBITDA"), ("ebit", "EBIT"), ("eps", "EPS")]:
            diffs = [d.c("Consensus", f"diff_{m}_{y}") for y in (1, 2, 3)]
            dtxt = [f"{v * 100:+.1f}%" if isinstance(v, (int, float)) else "n.a." for v in diffs]     # no consensus for the year
            diffs = [v if isinstance(v, (int, float)) else 0.0 for v in diffs]
            crows.append(dict(cells=[lab] + dtxt, size=8.5, h=0.235, line_bottom="DDE1E5",
                              align={1: "c", 2: "c", 3: "c"}, bolds={j: m in ("ebit", "eps") for j in range(4)},
                              colors={j + 1: (GREEN if v > 0.005 else RED if v < -0.005 else DARK) for j, v in enumerate(diffs)}))
        table(s, rx, y2 + 0.45, rw, crows, [1.2, 0.9, 0.9, 0.9])
        vt, vo, vc = (d.c("Consensus", f"vp1_{k}") for k in ("topic", "ours", "cons"))
        text(s, rx, y2 + 1.68, rw, 0.55, [(f"**Where we differ – {vt.lower()}.** Consensus: {vc.rstrip('.')}. "
                                          f"We: {vo.rstrip('.')}.", {})], size=7.5, color=DARK)
    notes(s, "TEMPLATE: Keep the heading 'Financials and estimates'. Tables and charts are generated from the model – "
             "re-run the deck builder or copy from the Deck_Feed sheet after changing the model.\n\n"
             "TALKING POINTS: (1) History proves the model works. (2) Growth from new locations, like-for-like and price. "
             "(3) Margin expansion from operating leverage – and it is paid for with capex. (4) Strong cash conversion and "
             "ROIC. (5) We are above consensus, and the gap widens – that is our edge.")
    return s


# ------------------------------------------------------------------ valuation
def football(s, d, x, y, w, h):
    rows = d.reg["rows"]
    methods = ["w52", "dcf_wg", "dcf_sc", "evebitda", "evebit", "pe"]
    labels = {"w52": "52-week range", "dcf_wg": "DCF (WACC ±0.5pp, g ±0.25pp)", "dcf_sc": "DCF (bear – bull)",
              "evebitda": "EV/EBITDA (peers 25-75th pct)", "evebit": "EV/EBIT (peers 25-75th pct)",
              "pe": "P/E (peers 25-75th pct)"}
    lows = [d.v("Football", f"C{rows['Football|' + k]}") for k in methods]
    highs = [d.v("Football", f"D{rows['Football|' + k]}") for k in methods]
    price, tp, fair = d.c("Inputs", "price"), d.c("DCF", "tp"), d.c("DCF", "tp_fair")
    base = int(min(lows + [price]) * 0.85 / 10) * 10
    vmax = (max(highs + [tp]) - base) * 1.10
    px, py, pw, ph = 0.42, 0.10, 0.50, 0.86
    gf = add_chart(s, XL_CHART_TYPE.BAR_STACKED, x, y, w, h, [labels[k] for k in methods],
                   [("Offset", [lo - base for lo in lows]), ("Range", [hi - lo for lo, hi in zip(lows, highs)])],
                   [NAVY, NAVY], size=8, labels=False, gap=55, overlap=100, val_min=0, val_max=vmax)
    ch = gf.chart
    hide_series(ch, 0)
    set_cat_reverse(ch)
    manual_plot_layout(ch, px, py, pw, ph)
    ch.category_axis.format.line.fill.background()
    X = lambda v: x + (px + pw * (v - base) / vmax) * w
    band = ph * h / len(methods)
    lw_ = 0.30                                   # approximate label width (inches)
    for i, (lo, hi) in enumerate(zip(lows, highs)):
        cy = y + py * h + band * (i + 0.5)
        right = X(lo) - 0.03
        for v in (price, fair, tp):                    # a vertical line inside the label area -> move label left of it
            if right - lw_ - 0.02 < X(v) < right + 0.02:
                right = X(v) - 0.05
        text(s, right - 0.42, cy - 0.1, 0.42, 0.2, f"{lo:.0f}", size=8, align="r", anchor="m", color=DARK)
        left = X(hi) + 0.03
        for v in (price, fair, tp):
            if left - 0.02 < X(v) < left + lw_ + 0.02:
                left = X(v) + 0.05
        text(s, left, cy - 0.1, 0.42, 0.2, f"{hi:.0f}", size=8, align="l", anchor="m", color=DARK)
    top, bot = y + py * h - 0.02, y + (py + ph) * h
    line(s, X(price), top, X(price), bot, color=RED, width=1.5, dash=MSO_LINE_DASH_STYLE.DASH)
    line(s, X(fair), top, X(fair), bot, color=NAVY, width=1.5)
    line(s, X(tp), top, X(tp), bot, color=GREEN, width=1.25, dash=MSO_LINE_DASH_STYLE.DASH_DOT)
    text(s, X(price) - 0.57, top - 0.24, 0.55, 0.2, f"{price:.0f}", size=8, bold=True, color=RED, align="r")
    text(s, X(fair) - 0.57, top - 0.24, 0.55, 0.2, f"{fair:.0f}", size=8, bold=True, color=NAVY, align="r")
    text(s, X(tp) + 0.02, top - 0.24, 0.55, 0.2, f"{tp:.0f}", size=8, bold=True, color=GREEN, align="l")
    ipo = ct("ipo_price")                        # a recent listing: mark the offer price
    if ipo:
        line(s, X(ipo), top + 0.02, X(ipo), bot, color=MUTED, width=1, dash=MSO_LINE_DASH_STYLE.ROUND_DOT)
        text(s, X(ipo) - 0.5, top - 0.43, 1.0, 0.18, f"IPO NOK {ipo:.0f}", size=7, color=MUTED, align="c")
    # legend: values today (price, fair value) vs. the 12-month target price
    lx = x + 0.1
    line(s, lx, y + h + 0.08, lx + 0.25, y + h + 0.08, color=RED, width=1.5, dash=MSO_LINE_DASH_STYLE.DASH)
    text(s, lx + 0.3, y + h - 0.02, 1.1, 0.2, "Share price", size=7.5, color=DARK)
    line(s, lx + 1.25, y + h + 0.08, lx + 1.5, y + h + 0.08, color=NAVY, width=1.5)
    text(s, lx + 1.55, y + h - 0.02, 1.2, 0.2, "Fair value today", size=7.5, color=DARK)
    line(s, lx + 2.75, y + h + 0.08, lx + 3.0, y + h + 0.08, color=GREEN, width=1.25, dash=MSO_LINE_DASH_STYLE.DASH_DOT)
    text(s, lx + 3.05, y + h - 0.02, 2.1, 0.2, "12m target price (rolled forward)", size=7.5, color=DARK)


def mini_bars(s, x, y, w, h, cats, vals, colors, bubbles):
    """Small 'current vs value' bar chart with % bubbles (KID style)."""
    vmax = max(vals) * 1.35
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, w, h, cats, [("NOK", vals)], [NAVY], size=8,
                   labels=True, num_fmt="0", label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=25, val_min=0,
                   val_max=vmax, cat_axis=True)
    color_points(gf.chart, colors)
    px, py, pw, ph = 0.05, 0.05, 0.90, 0.80
    manual_plot_layout(gf.chart, px, py, pw, ph)
    n = len(vals)
    for (i, j, label) in bubbles:
        bxc = x + (px + pw * (j + 0.5) / n) * w
        top = y + (py + ph * (1 - vals[j] / vmax)) * h
        b = rect(s, bxc - 0.28, top - 0.52, 0.56, 0.22, fill=WHITE, line=DARK, shape=MSO_SHAPE.OVAL)
        shape_text(b, label, size=8, color=DARK, bold=True, margin=0)
        line(s, bxc, top - 0.30, bxc, top - 0.20, color=DARK, width=1, arrow_end=True)


def valuation(prs, d):
    comp = d.c("Inputs", "company").split(" ASA")[0]
    rating, tp, up, tr = d.c("DCF", "rating"), d.c("DCF", "tp"), d.c("DCF", "tp_up"), d.c("DCF", "tp_tr")
    price, dcf, peer = d.c("Inputs", "price"), d.c("DCF", "dcf_ps"), d.c("Comps", "peer_val")
    wd, wp = d.c("Inputs", "w_dcf"), d.c("Inputs", "w_peers")
    s = std(prs, "#4 Valuation and concluding thoughts", "Valuation and recommendation",
            f"We recommend {rating} with a target price of NOK {tp:.0f} – {up * 100:.0f}% upside and "
            f"{tr * 100:.0f}% expected total return",
            f"Sources: Case team DCF and peer analysis; peer multiples from Bloomberg consensus (case material). (1) TP = "
            f"{wd * 100:.0f}% DCF + {wp * 100:.0f}% peer multiples, rolled forward 12 months at the cost of equity less "
            f"next year's dividend. Figures are illustrative.")
    rd = lambda k: d.c("Reverse_DCF", k)
    m_imp, m_our, m_ref = rd("rd_m_last"), rd("rd_m_last_ours"), rd("rd_m_last_ref")
    yl, ya = d.years([FC[-1]])[0], d.years(["K"])[0]
    if isinstance(m_imp, (int, float)):
        rel = "below" if m_imp < m_ref else "above"
        take = (f"Our take: at NOK {price:.0f} the market prices in an EBIT margin of **{m_imp * 100:.1f}%** in {yl} – {rel} the "
                f"{m_ref * 100:.1f}% {comp} earns today. We see **{m_our * 100:.1f}%** {ct('take_reason', 'as fixed costs are spread over more locations')}. "
                f"DCF NOK {dcf:.0f} and peers NOK {peer:.0f} both point higher: **12-month target price NOK {tp:.0f}**(1), **{rating}**.")
    else:
        take = (f"Our take: {comp} is a **high-quality compounder** trading at a **discount to peers**. Our DCF (NOK {dcf:.0f}) "
                f"and peer valuation (NOK {peer:.0f}) both point higher – **12-month target price NOK {tp:.0f}**(1), **{rating}**.")
    key_box(s, 1.36, take, h=0.55, size=10.5)
    # left column
    lx, lw = 0.47, 4.70
    y1, y2 = 2.02, 4.50
    panel_header(s, lx, y1, lw, f"{rating} – TP NOK {tp:.0f}", None)
    panel(s, lx, y1 + 0.42, lw, 1.90)
    ev_ebit_disc = d.v("Comps", f"M{d.reg['comps']['prem']}")
    t4 = {k: c for c, k, _, _ in d.reg["t4"]}
    sr0, sr1 = d.reg["sens"]["t4_rows"]
    bear_ps = d.v("Sensitivity", f"{t4['dcf_ps']}{sr0}")
    bull_ps = d.v("Sensitivity", f"{t4['dcf_ps']}{sr1}")
    thesis = [
        (ct("thesis_quality", "").format(m_imp=m_imp * 100, m_our=m_our * 100, yl=yl, price=d.c("Inputs", "price"))
         if ct("thesis_quality") and isinstance(m_imp, (int, float)) else f"**Quality at a discount:** trades at {mult(d.row('Model', 'evebit', ['M'])[0])} 2027E EV/EBIT, "
        f"{abs(ev_ebit_disc) * 100:.0f}% below peers despite higher margins"),
        ct("thesis_growth", "**Growth engine intact:** new locations, like-for-like and pricing all contribute; bolt-on M&A is upside"),
        ct("thesis_cash") or f"**Cash machine:** FCF yield rising to {d.row('Model', 'fcf_yield', ['O'])[0] * 100:.0f}% by 2029E funds rising dividends",
        f"**Asymmetric risk/reward:** bull NOK {bull_ps:.0f} vs. bear NOK {bear_ps:.0f} per share (DCF)",
        ct("thesis_catalysts", "**Catalysts:** next quarterly report (price increases), capital markets day, bolt-on M&A"),
    ]
    text(s, lx + 0.12, y1 + 0.50, lw - 0.24, 1.80, [(t, {"bullet": True, "space_after": 3}) for t in thesis], size=9.5)
    panel_header(s, lx, y2, lw, "Valuation summary – football field (NOK/share)", None)
    football(s, d, lx, y2 + 0.62, lw, 1.70)
    line(s, 5.40, 2.05, 5.40, 6.85, color="C8CDD3", width=0.75)
    # right column: sensitivity
    rx, rw = 5.62, 7.25
    panel_header(s, rx, y1, rw, "DCF valuation – sensitivity analysis (NOK per share)", None)
    sn = d.reg["sens"]
    h0, (r0, r1) = sn["t1_hdr"], sn["t1_rows"]
    wacc_cols = list("DEFGHIJ")
    rows = [dict(cells=["", "", "WACC", "", "", "", "", "", ""], fill=NAVY, color=WHITE, bold=True, size=10, h=0.26,
                 align={2: "c"}),
            dict(cells=["", ""] + [pct(d.v("Sensitivity", f"{c}{h0}"), 2) for c in wacc_cols], fill=NAVY,
                 color=WHITE, bold=True, size=9, h=0.24, align={j: "c" for j in range(2, 9)})]
    for k, r in enumerate(range(r0, r1 + 1)):
        vals = [d.v("Sensitivity", f"{c}{r}") for c in wacc_cols]
        fills = {0: NAVY, 1: NAVY}
        colors, bolds = {0: WHITE, 1: WHITE}, {1: True}
        for j in range(7):
            if 2 <= j <= 4 and 1 <= k <= 3:
                fills[j + 2] = PALEBLUE
            if j == 3 and k == 2:
                fills[j + 2], bolds[j + 2] = "9EC3D1", True
        rows.append(dict(cells=["Terminal growth" if k == 0 else "", pct(d.v("Sensitivity", f"C{r}"), 2)] +
                         [f"{v:.1f}" for v in vals], fills=fills, colors=colors, bolds=bolds, size=9, h=0.24,
                         align={j: "c" for j in range(1, 9)}))
    tw = 5.25
    gft = table(s, rx, y1 + 0.47, tw, rows, [0.38, 0.62] + [0.61] * 7)
    tbl = gft.table
    tbl.cell(0, 2).merge(tbl.cell(0, 8))
    tbl.cell(2, 0).merge(tbl.cell(6, 0))
    c = tbl.cell(2, 0)
    c._tc.get_or_add_tcPr().set("vert", "vert270")
    c.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    tbl.cell(0, 0).merge(tbl.cell(1, 1))
    # small chart: current vs DCF
    cxp = rx + tw + 0.15
    panel(s, cxp, y1 + 0.47, rw - tw - 0.15, 1.72, fill=WHITE)
    rect(s, cxp, y1 + 0.47, rw - tw - 0.15, 1.72, fill=None, line="C8CDD3")
    mini_bars(s, cxp + 0.08, y1 + 0.70, rw - tw - 0.31, 1.45, ["Current", "DCF"], [price, dcf], [BLACK, LBLUE],
              [(0, 1, pct(dcf / price - 1, 0, sign=True))])
    # what the market is pricing in (reverse DCF)
    panel_header(s, rx, y2, rw, "What the market is pricing in (reverse DCF)", None)
    panel(s, rx, y2 + 0.42, tw, 1.98)
    isn = lambda v: isinstance(v, (int, float))
    fp = lambda v, k=1: f"{v * 100:.{k}f}%" if isn(v) else "n.a."
    rrows = [dict(cells=["", "Market", "Ours", ya], fill=NAVY, color=WHITE, bold=True, size=8.5, h=0.24,
                  align={1: "c", 2: "c", 3: "c"})]
    for lab, k, ref, dec in [(f"EBIT adj. margin {yl}", "m_last", rd("rd_m_last_ref"), 1),
                             (f"Revenue CAGR {ya[:4]}–{yl[2:]}", "cagr", rd("rd_cagr_ref"), 1),
                             ("WACC", "wacc", None, 1)]:
        rrows.append(dict(cells=[lab, fp(rd(f"rd_{k}"), dec), fp(rd(f"rd_{k}_ours"), dec), fp(ref, dec) if ref is not None else "–"],
                          size=8.5, h=0.235, line_bottom="DDE1E5", align={1: "c", 2: "c", 3: "c"},
                          bolds={1: True, 2: True}, colors={1: RED, 2: NAVY}))
    table(s, rx + 0.1, y2 + 0.52, tw - 0.2, rrows, [2.0, 0.95, 0.95, 0.95])
    kpp = rd("rd_k")
    _pin = isn(m_imp) and isn(m_ref) and m_imp > m_ref
    items = [(f"**Little operating leverage priced in:** the market's {yl} margin is only "
              f"{(m_imp - m_ref) * 100:.1f}pp above today's and {abs(m_our - m_imp) * 100:.1f}pp below ours") if _pin else
             (f"**No operating leverage priced in:** the market's {yl} margin is "
              f"{abs(m_our - m_imp) * 100 if isn(m_imp) else 0:.1f}pp below ours"),
             f"**Each 1pp of margin is worth NOK {kpp:.1f} per share** – our upside rests on margins, not on multiples"]
    text(s, rx + 0.12, y2 + 1.55, tw - 0.24, 0.85, [(t, {"bullet": True, "space_after": 3}) for t in items], size=9)
    rect(s, cxp, y2 + 0.42, rw - tw - 0.15, 1.98, fill=None, line="C8CDD3")
    tiles = [(fp(m_imp), f"Market-implied, {yl}", RED), (fp(m_our), f"Our base case, {yl}", NAVY), (fp(m_ref), f"Today ({ya})", MUTED)]
    for j, (big, lab, col) in enumerate(tiles):
        ty = y2 + 0.50 + j * 0.62
        text(s, cxp + 0.1, ty, rw - tw - 0.35, 0.34, big, size=17, bold=True, color=col, align="c")
        text(s, cxp + 0.1, ty + 0.33, rw - tw - 0.35, 0.22, lab, size=7.5, color=DARK, align="c")
    r0, r1 = d.reg["sens"]["t1_rows"]
    hdr = d.reg["sens"]["t1_hdr"]
    grid = {c: [d.v("Sensitivity", f"{c}{r}") for r in range(r0, r1 + 1)] for c in "DEFGHIJ"}
    above = sum(1 for c in grid for v in grid[c] if v > price)
    bad_cols = [c for c in "DEFGHIJ" if min(grid[c]) < price]
    wacc_break = f"{d.v('Sensitivity', f'{bad_cols[0]}{hdr}') * 100:.1f}% or more" if bad_cols else "no level in the grid"
    notes(s, "TEMPLATE: Keep the heading 'Valuation and recommendation'. The sensitivity table, football field and bar "
             "charts come from the Sensitivity, Football and Comps sheets.\n\n"
             f"TALKING POINTS: (1) Recommendation and target price first. (2) DCF: NOK {dcf:.0f} with WACC "
             f"{d.c('WACC', 'wacc') * 100:.1f}% and g {d.c('DCF', 'tv_g') * 100:.1f}%; {above} of 35 cells in the sensitivity "
             f"grid are above today's price (the value falls below it only at a WACC of {wacc_break}). "
             f"(3) What the market prices in: an EBIT margin of {m_imp * 100 if isinstance(m_imp, (int, float)) else 0:.1f}% in "
             f"{yl} vs. our {m_our * 100:.1f}% – the debate is margins. (4) Peers confirm the gap; target price = blend rolled "
             "forward 12 months. (5) Close with the risk/reward: bear vs. bull.")
    return s
