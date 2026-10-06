"""Chart library – part 2: bridges, valuation visuals, peer benchmarking, share price, KPI tiles and tables."""
import random
from cl_core import *
from cl_a1 import FOOT
from deck_data import HC, FC, pct, num, mult
from deck_slides2 import football

XS2, W2 = [0.47, 6.87], 6.0
YS2, H2 = [1.40, 4.18], 2.68


def _g2(i):
    return XS2[i % 2], YS2[i // 2]


# ------------------------------------------------------------------ bridges
def bridges(prs, d):
    s = std(prs, "Chart library #4", "Bridge (waterfall) charts",
            "Explain the move from A to B: what drives revenue, what lifts the margin and how enterprise value becomes equity value",
            FOOT + " Bridges are stacked columns with an invisible base series – edit the four series under Edit Data.")
    rev = d.row("Model", "is_rev", ["K"] + FC[:5])
    gn, gl, gp = (d.row("Model", k, FC[:5]) for k in ("g_newc", "g_lflc", "g_pxc"))
    y0, y1 = d.years(["K"])[0], d.years(["P"])[0]
    new = sum(rev[i] * gn[i] for i in range(5))
    lfl = sum(rev[i] * gl[i] for i in range(5))
    px = sum(rev[i] * gp[i] for i in range(5))
    # 1 revenue bridge
    x, y = _g2(0)
    box = cpanel(s, x, y, W2, H2, f"Revenue bridge {y0} – {y1} (NOKm)", "growth split into new locations, like-for-like and price/mix", 1)
    waterfall(s, box, [(f"Revenue {y0}", rev[0], "total"), ("New locations", new, "delta"), ("Like-for-like", lfl, "delta"),
                       ("Price / mix", px, "delta"), (f"Revenue {y1}", rev[5], "total")], vmax=rev[5] * 1.2)
    # 2 EBIT bridge
    x, y = _g2(1)
    ca, cb_ = "H", "K"                                  # 2022A -> 2025A: the period where margins moved
    ya, yb = d.years([ca])[0], d.years([cb_])[0]
    box = cpanel(s, x, y, W2, H2, f"EBIT bridge {ya} – {yb} (NOKm)", "margin story: what came from growth and what from cost ratios", 2)
    ratio = lambda k, c: -d.row("Model", k, [c])[0] / d.row("Model", "is_rev", [c])[0]
    ra, rb = d.row("Model", "is_rev", [ca])[0], d.row("Model", "is_rev", [cb_])[0]
    e0, e1 = d.row("Model", "ebit_adj", [ca])[0], d.row("Model", "ebit_adj", [cb_])[0]
    steps = [(f"EBIT adj. {ya}", e0, "total"), ("Revenue growth", (rb - ra) * e0 / ra, "delta")]
    for lab, keys in [("COGS ratio", ["cogs"]), ("Personnel ratio", ["pers"]), ("Other opex ratio", ["oth"]),
                      ("Leases and D&A", ["lease", "da"])]:
        steps.append((lab, -sum(ratio(k, cb_) - ratio(k, ca) for k in keys) * rb, "delta"))
    steps.append((f"EBIT adj. {yb}", e1, "total"))
    waterfall(s, box, steps, vmax=e1 * 1.25, size=7.5)
    # 3 EV to equity bridge
    x, y = _g2(2)
    box = cpanel(s, x, y, W2, H2, "From enterprise value to equity value (NOKm)", "the EV-to-equity bridge on the valuation slide", 3)
    D = lambda k: d.c("DCF", k)
    waterfall(s, box, [("Enterprise value", D("ev"), "total"), ("Net debt", D("b_nibd"), "delta"),
                       ("Minorities", D("b_min"), "delta"), ("Associates", D("b_assoc"), "delta"),
                       ("Pensions", D("b_pens"), "delta"), ("Equity value", D("eq"), "total")], vmax=D("ev") * 1.2)
    # 4 target price build
    x, y = _g2(3)
    box = cpanel(s, x, y, W2, H2, "Target price build-up (NOK per share)", "how DCF, peers and the 12-month roll-forward give the target price", 4)
    fair, dcf = D("tp_fair"), D("tp_dcf")
    waterfall(s, box, [("DCF value", dcf, "total"), ("Peer blend", fair - dcf, "delta"),
                       ("12m roll-forward", fair * (D("tp_roll") - 1), "delta"), ("Dividend", -D("tp_div"), "delta"),
                       ("Target price", D("tp_raw"), "total")], fmt="{:,.1f}", vmax=D("tp_raw") * 1.25)
    notes(s, "Waterfall recipe: series 1 'Base' has no fill and lifts the floating bars; totals, increases and decreases "
             "are separate series so each keeps its colour. Value labels are text boxes – retype them if you change data.")
    return s


# ------------------------------------------------------------------ valuation visuals
def valuation_visuals(prs, d):
    s = std(prs, "Chart library #5", "Valuation visuals",
            "Football field, sensitivity heat map, scenario values and the composition of enterprise value", FOOT)
    price, tp = d.c("Inputs", "price"), d.c("DCF", "tp")
    # 1 football field
    x, y = _g2(0)
    cpanel(s, x, y, W2, H2, "Football field (NOK per share)", "the summary of all valuation methods vs. share price and target", 1)
    football(s, d, x + 0.3, y + 0.62, 5.2, 1.62)
    # 2 sensitivity heat map
    x, y = _g2(1)
    box = cpanel(s, x, y, W2, H2, "Sensitivity heat map – WACC vs. terminal growth", "show that the conclusion survives other assumptions", 2)
    sn = d.reg["sens"]
    h0, (r0, r1) = sn["t1_hdr"], sn["t1_rows"]
    cols = list("DEFGHIJ")
    grid = [[d.v("Sensitivity", f"{c}{r}") for c in cols] for r in range(r0, r1 + 1)]
    flat = [v for row in grid for v in row]
    rows = [dict(cells=["g \\ WACC"] + [pct(d.v("Sensitivity", f"{c}{h0}"), 1) for c in cols], fill=NAVY, color=WHITE,
                 bold=True, size=8.5, h=0.28, align={j: "c" for j in range(8)})]
    for k, r in enumerate(range(r0, r1 + 1)):
        fills = {0: NAVY}
        for j, v in enumerate(grid[k]):
            fills[j + 1] = heat(v, min(flat), price, max(flat))
        rows.append(dict(cells=[pct(d.v("Sensitivity", f"C{r}"), 2)] + [f"{v:.0f}" for v in grid[k]], fills=fills,
                         colors={0: WHITE}, bolds={0: True, 4: k == 2}, size=8.5, h=0.27, align={j: "c" for j in range(8)}))
    table(s, box[0], box[1] + 0.05, box[2], rows, [1.0] + [0.72] * 7)
    text(s, box[0], box[1] + 1.72, box[2], 0.2, f"Green = above today's share price (NOK {price:.0f}), red = below. Centre = base case.",
         size=7.5, italic=True, color=MUTED)
    # 3 scenario bars
    x, y = _g2(2)
    box = cpanel(s, x, y, W2, H2, "Scenario values vs. share price", "risk/reward in one picture", 3)
    t4 = {k: c for c, k, _, _ in d.reg["t4"]}
    sr0 = sn["t4_rows"][0]
    vals = [d.v("Sensitivity", f"{t4['dcf_ps']}{sr0 + j}") for j in range(3)]
    vmax = max(vals) * 1.3
    cb = (box[0], box[1], 3.6, box[3])
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, *cb, ["Bear", "Base", "Bull"], [("DCF value", vals)], [NAVY], size=9,
                   labels=True, num_fmt="0", label_pos=XL_LABEL_POSITION.INSIDE_END, gap=70, val_min=0, val_max=vmax,
                   label_color=WHITE)
    color_points(gf.chart, [RED, NAVY, GREEN])
    manual_plot_layout(gf.chart, *PLOT)
    _, Y = geo(cb, n=3, vmax=vmax)
    line(s, cb[0] + PLOT[0] * cb[2], Y(price), cb[0] + (PLOT[0] + PLOT[2]) * cb[2], Y(price), color=RED, width=1.25,
         dash=MSO_LINE_DASH_STYLE.DASH)
    pw_ = d.c("Sensitivity", "pw_dcf_ps")
    items = [("Bear", vals[0], RED), ("Base", vals[1], NAVY), ("Bull", vals[2], GREEN)]
    for j, (nm, v, col) in enumerate(items):
        yy = box[1] + 0.12 + j * 0.36
        chip(s, box[0] + 3.85, yy, 0.62, nm, col)
        text(s, box[0] + 4.55, yy - 0.01, 1.4, 0.24, f"NOK {v:.0f}  ({v / price - 1:+.0%})", size=9, bold=True, anchor="m")
    text(s, box[0] + 3.85, box[1] + 1.25, 2.1, 0.5, [("Probability-weighted", {"size": 8, "color": MUTED}),
                                                     (f"NOK {pw_:.0f}", {"size": 13, "bold": True, "color": NAVY})])
    line(s, box[0] + 3.85, box[1] + 1.82, box[0] + 4.1, box[1] + 1.82, color=RED, width=1.25, dash=MSO_LINE_DASH_STYLE.DASH)
    text(s, box[0] + 4.15, box[1] + 1.71, 1.8, 0.2, f"Share price NOK {price:.0f}", size=7.5, color=DARK)
    # 4 EV composition
    x, y = _g2(3)
    box = cpanel(s, x, y, W2, H2, "What is the value made of?", "share of DCF value from the forecast period vs. the terminal value", 4)
    pv, tv = d.c("DCF", "sum_pv"), d.c("DCF", "pv_tv")
    pie(s, (box[0], box[1], 2.4, box[3]), ["Forecast period", "Terminal value"], [pv, tv], [LBLUE, NAVY], size=9,
        doughnut=True, hole=55, centre=["EV", f"{pv + tv:,.0f}"], label_colors=[NAVY, WHITE])
    pvs = d.row("DCF", "pv", FC)
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, box[0] + 2.5, box[1], 3.5, box[3], d.years(FC) + ["TV"],
                   [("Present value (NOKm)", pvs + [tv])], [LBLUE], size=7, labels=True, num_fmt="0",
                   label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=35)
    color_points(gf.chart, [LBLUE] * 8 + [NAVY])
    notes(s, "The football field and heat map read the Football and Sensitivity sheets of the model. The vertical lines "
             "in the football field are drawn shapes placed from the axis scale – rebuild with the deck generator or move "
             "them by hand if the ranges change.")
    return s


# ------------------------------------------------------------------ peers
def peer_charts(prs, d):
    s = std(prs, "Chart library #6", "Peer benchmarking charts",
            "Is the discount deserved? Put valuation next to the fundamentals that should explain it", FOOT)
    cr = d.reg["comps"]
    comp = d.c("Inputs", "company").replace(" ASA", "")
    short = lambda n: n.replace(" ASA", "").replace(" AB", "").replace(" A/S", "").replace(" Oyj", "").replace(" plc", "") \
        .replace(" SE", "").replace(" NV", "")
    rows = list(range(6, 14)) + [cr["company"]]
    nm = lambda r: comp if r == cr["company"] else short(d.v("Comps", f"B{r}"))
    # 1 scatter
    x, y = _g2(0)
    box = cpanel(s, x, y, W2, H2, "Scatter with trend line – EV/EBIT vs. EBIT margin", "is a high multiple explained by high margins or growth?", 1)
    pts = [(nm(r), d.v("Comps", f"R{r}"), d.v("Comps", f"M{r}")) for r in rows]
    scatter(s, box, pts, xfmt="0%", yfmt='0"x"', xtitle="EBIT margin 2027E", ytitle="EV/EBIT 2027E", highlight=comp,
            xlim=(0.08, 0.22), ylim=(8, 18))
    # 2 bubble
    x, y = _g2(1)
    box = cpanel(s, x, y, W2, H2, "Bubble chart – growth vs. margin (size = market cap)", "positioning of the company in its peer group", 2)
    pts = [(nm(r), d.v("Comps", f"S{r}"), d.v("Comps", f"R{r}"), d.v("Comps", f"D{r}")) for r in rows]
    bubble(s, box, pts, xtitle="Revenue growth 2027E", ytitle="EBIT margin 2027E", highlight=comp, xlim=(0.03, 0.10),
           ylim=(0.08, 0.23), scale=70)
    # 3 premium / discount bars
    x, y = _g2(2)
    box = cpanel(s, x, y, W2, H2, "Premium / (discount) to peer median", "one glance: where is the stock cheap or expensive?", 3)
    labs, vals = [], []
    yrs = [d.v("Comps", f"{c}5") for c in "IJLMOP"]
    for c, lab, yv in zip("IJLMOP", ["EV/EBITDA", "EV/EBITDA", "EV/EBIT", "EV/EBIT", "P/E", "P/E"], yrs):
        labs.append(f"{lab} {yv}")
        vals.append(d.v("Comps", f"{c}{cr['prem']}"))
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, *box, labs, [("Premium / (discount)", vals)], [NAVY], size=7.5,
                   labels=True, num_fmt="0%;-0%", label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=60, val_min=-0.25, val_max=0.10)
    color_points(gf.chart, [RED if v < 0 else GREEN for v in vals])
    gf.chart.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.HIGH
    # 4 radar
    x, y = _g2(3)
    box = cpanel(s, x, y, W2, H2, "Radar – company vs. peer median (peer median = 100)", "a quality profile across several metrics", 4)
    med = cr["median"]
    co = cr["company"]
    roic = d.row("Model", "roic", ["M"])[0]
    conv = d.row("Model", "cconv", ["M"])[0]
    metrics = [("Growth", d.v("Comps", f"S{co}") / d.v("Comps", f"S{med}")),
               ("EBIT margin", d.v("Comps", f"R{co}") / d.v("Comps", f"R{med}")),
               ("ROIC", roic / 0.15), ("Cash conversion", conv / 0.55), ("Balance sheet", 1.25),
               ("Valuation (cheapness)", d.v("Comps", f"M{med}") / d.v("Comps", f"M{co}"))]
    cd = CategoryChartData()
    cd.categories = [m[0] for m in metrics]
    cd.add_series(comp, [round(m[1] * 100) for m in metrics])
    cd.add_series("Peer median", [100] * len(metrics))
    gf = s.shapes.add_chart(XL_CHART_TYPE.RADAR_MARKERS, Inches(box[0] + 0.6), Inches(box[1] - 0.05), Inches(3.4),
                            Inches(box[3] + 0.1), cd)
    ch = gf.chart
    ch.font.name, ch.font.size = FONT, Pt(7.5)
    ch.has_legend = False
    for k, col in enumerate([NAVY, LBLUE]):
        srs = ch.plots[0].series[k]
        srs.format.line.color.rgb = rgb(col)
        srs.format.line.width = Pt(2 if k == 0 else 1.5)
        srs.marker.style = XL_MARKER_STYLE.CIRCLE
        srs.marker.size = 5
        srs.marker.format.fill.solid()
        srs.marker.format.fill.fore_color.rgb = rgb(col)
        srs.marker.format.line.fill.background()
    ch.value_axis.maximum_scale, ch.value_axis.minimum_scale = 160, 0
    ch.value_axis.major_gridlines.format.line.color.rgb = rgb("D5DADF")
    ch.value_axis.tick_label_position = XL_TICK_LABEL_POSITION.NONE
    ch.value_axis.format.line.fill.background()
    swatches(s, box[0] + 4.2, box[1] + 0.5, [(comp, NAVY), ("Peer median (= 100)", LBLUE)], vertical=True, size=8.5, dy=0.3)
    text(s, box[0] + 4.2, box[1] + 1.2, 1.8, 0.6, "Above 100 = better than peers on that metric.", size=7.5, italic=True, color=MUTED)
    notes(s, "Scatter and bubble labels are custom data labels – after Edit Data, retype the label of any new point. "
             "The trend line is a drawn line from an OLS regression on the example data.")
    return s


# ------------------------------------------------------------------ share price
def share_price(prs, d):
    s = std(prs, "Chart library #7", "Share price chart with events",
            "The classic opening chart of an equity story: what has moved the stock, and where do we think it is going?",
            FOOT + " The price series is randomly generated – paste weekly prices from Bloomberg/Yahoo under Edit Data.")
    price, tp = d.c("Inputs", "price"), d.c("DCF", "tp")
    rnd = random.Random(5)
    n, p, idx = 105, 96.0, 100.0
    ps, ix = [], []
    for i in range(n):
        p *= 1 + 0.0023 + rnd.gauss(0, 0.022)
        idx *= 1 + 0.0012 + rnd.gauss(0, 0.012)
        ps.append(p)
        ix.append(idx)
    ps = [v * price / ps[-1] for v in ps]
    ix = [v * ps[0] / ix[0] for v in ix]
    mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    labs = []
    for i in range(n):
        m = (8 + (i * 12) // 52) % 12
        yr = 24 + (8 + (i * 12) // 52) // 12
        labs.append(f"{mon[m]}-{yr}")
    x, y, w, h = 0.47, 1.40, 8.6, 5.45
    box = cpanel(s, x, y, w, h, "Share price vs. index (rebased), NOK", "share price history with numbered events and the target price", 1)
    lo, hi = int(min(ps + ix) / 10) * 10 - 10, int(max(ps + ix + [tp]) / 10) * 10 + 20
    plot = (0.06, 0.04, 0.80, 0.84)
    gf = add_chart(s, XL_CHART_TYPE.LINE, *box, labs, [(d.c("Inputs", "ticker"), [round(v, 1) for v in ps]),
                                                      ("OSEBX (rebased)", [round(v, 1) for v in ix])],
                   [NAVY, LBLUE], size=8, legend="t", labels=False, num_fmt="0", val_axis=True, gridlines=True, val_min=lo, val_max=hi)
    ch = gf.chart
    ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = "0", False
    ch.plots[0].series[1].format.line.width = Pt(1.25)
    label_skip(ch, 13)
    manual_plot_layout(ch, *plot)
    X, Y = geo(box, plot, n=n, vmax=hi, vmin=lo)
    xr = box[0] + (plot[0] + plot[2]) * box[2]
    line(s, X(n - 1), Y(tp), xr + 0.55, Y(tp), color=GREEN, width=1.5, dash=MSO_LINE_DASH_STYLE.DASH)
    text(s, xr + 0.05, Y(tp) - 0.42, 1.5, 0.4, [("Target price", {"size": 8, "color": GREEN}),
                                               (f"NOK {tp:.0f} ({tp / price - 1:+.0%})", {"size": 9, "bold": True, "color": GREEN})])
    text(s, xr + 0.05, Y(price) - 0.05, 1.5, 0.22, f"Last NOK {price:.0f}", size=8.5, bold=True, color=NAVY)
    line(s, X(n - 1), Y(price), X(n - 1), Y(tp), color=GREEN, width=1.25, arrow_end=True)
    events = [(9, "Q3'24 report: margins beat consensus by 8%"), (27, "Acquisition of Competitor D (Denmark) announced"),
              (44, "Profit warning from a low-cost peer hits the sector"), (62, "Capital markets day: 20% ROIC target"),
              (83, "Price increases of 5% implemented in all markets"), (97, "Q2'26 report: record subscriber intake")]
    for k, (i, _) in enumerate(events):
        circle(s, X(i) - 0.12, Y(ps[i]) - 0.42, 0.24, fill=NAVY, txt=str(k + 1), font_size=8, line_col=WHITE)
        line(s, X(i), Y(ps[i]) - 0.18, X(i), Y(ps[i]) - 0.03, color=NAVY, width=0.75)
    rx, rw = 9.35, 3.52
    panel_header(s, rx, y, rw, "Key events", None, size=11)
    panel(s, rx, y + 0.42, rw, 3.35)
    for k, (i, txt) in enumerate(events):
        yy = y + 0.55 + k * 0.53
        circle(s, rx + 0.12, yy, 0.26, fill=NAVY, txt=str(k + 1), font_size=8.5)
        text(s, rx + 0.48, yy - 0.04, rw - 0.6, 0.44, [(labs[i], {"size": 7.5, "color": MUTED}), (txt, {"size": 8.5})], anchor="m")
    panel_header(s, rx, y + 3.95, rw, "Performance", None, size=11)
    perf = lambda k: ps[-1] / ps[-1 - k] - 1
    iperf = lambda k: ix[-1] / ix[-1 - k] - 1
    prow = [dict(cells=["", "1M", "3M", "6M", "12M"], fill=NAVY, color=WHITE, bold=True, size=8.5, h=0.24)]
    for nm_, f in ((d.c("Inputs", "ticker"), perf), ("OSEBX", iperf)):
        prow.append(dict(cells=[nm_] + [f"{f(k):+.0%}" for k in (4, 13, 26, 52)], size=8.5, h=0.23, line_bottom="E1E5EA"))
    prow.append(dict(cells=["Relative"] + [f"{perf(k) - iperf(k):+.0%}" for k in (4, 13, 26, 52)], size=8.5, h=0.23, bold=True,
                     fill="E4EEF2"))
    table(s, rx, y + 4.40, rw, prow, [1.2, 0.58, 0.58, 0.58, 0.58])
    notes(s, "Event markers are shapes positioned from the chart scale. If you replace the price series, drag the numbered "
             "circles to the right dates. Keep 5-7 events – only the ones that matter for the thesis.")
    return s


# ------------------------------------------------------------------ KPI tiles & tables
def kpi_tables(prs, d):
    s = std(prs, "Chart library #8", "KPI tiles and scorecard tables",
            "When a number says more than a chart: headline tiles, Harvey-ball scorecards and estimate tables",
            "Tiles and the consensus table read the model; the scorecard is illustrative. Harvey balls are text symbols "
            "(○ ◔ ◑ ◕ ●) in Segoe UI Symbol – type over them to change a score.")
    comp = d.c("Inputs", "company").replace(" ASA", "")
    rev = d.row("Model", "is_rev", ["K", "P"])
    tiles = [(f"{d.c('DCF', 'tp'):.0f}", "Target price (NOK)", f"{d.c('DCF', 'rating')} · {d.c('DCF', 'tp_up'):+.0%} upside", NAVY),
             (f"{((rev[1] / rev[0]) ** 0.2 - 1) * 100:.1f}%", "Revenue CAGR 2025–30E", "volume + price/mix", MIDBLUE),
             (f"{d.row('Model', 'ebit_adj_m', ['P'])[0] * 100:.1f}%", "EBIT adj. margin 2030E", "from 17.5% in 2025", MIDBLUE),
             (f"{d.row('Model', 'roic', ['N'])[0] * 100:.0f}%", "ROIC 2028E", f"WACC {d.c('WACC', 'wacc') * 100:.1f}%", LBLUE),
             (f"{d.row('Model', 'evebit', ['M'])[0]:.1f}x", "EV/EBIT 2027E", f"peers {d.v('Comps', 'M' + str(d.reg['comps']['median'])):.1f}x", LBLUE)]
    tw = (12.40 - 4 * 0.18) / 5
    panel_header(s, 0.47, 1.40, 12.40, "Headline KPI tiles", 1, size=11)
    for j, (big, lab, sub, col) in enumerate(tiles):
        tx = 0.47 + j * (tw + 0.18)
        rect(s, tx, 1.88, tw, 1.22, fill=col)
        text(s, tx + 0.12, 1.92, tw - 0.24, 0.6, big, size=28, bold=True, color=WHITE, anchor="m")
        text(s, tx + 0.12, 2.52, tw - 0.24, 0.26, lab, size=9.5, bold=True, color=WHITE)
        text(s, tx + 0.12, 2.76, tw - 0.24, 0.24, sub, size=8.5, color=WHITE)
    # scorecard
    x, y, w = 0.47, 3.35, 6.0
    panel_header(s, x, y, w, "Harvey-ball scorecard vs. peers", 2, size=11)
    hdr = dict(cells=["", comp, "Peer A", "Peer B", "Peer E", "Peer F"], fill=NAVY, color=WHITE, bold=True, size=8.5, h=0.27,
               align={j: "c" for j in range(1, 6)})
    crit = [("Market position", "●◕◑◕●"), ("Pricing power", "●◑◔◕◕"), ("Growth outlook", "◕◑◑●◕"), ("Margins and ROIC", "●◕◑◕◕"),
            ("Balance sheet", "◕◑◕◑◔"), ("Management track record", "◕◕◑◕◑"), ("Valuation attractiveness", "●◑◕◔◑")]
    rows = [hdr]
    for lab, balls in crit:
        rows.append(dict(cells=[lab] + list(balls), size=9, h=0.30, line_bottom="E1E5EA", align={j: "c" for j in range(1, 6)},
                         colors={j: NAVY for j in range(1, 6)}, fills={1: "E4EEF2"}))
    gf = table(s, x, y + 0.47, w, rows, [2.3] + [0.74] * 5)
    for i in range(1, len(rows)):
        for j in range(1, 6):
            for r in gf.table.cell(i, j).text_frame.paragraphs[0].runs:
                r.font.name, r.font.size = "Segoe UI Symbol", Pt(13)
    text(s, x, y + 3.18, w, 0.2, "● strong   ◕ good   ◑ average   ◔ weak   ○ poor", size=8, color=MUTED, font="Segoe UI Symbol")
    # estimates vs consensus
    x2, w2 = 6.87, 6.0
    panel_header(s, x2, y, w2, "Our estimates vs. consensus", 3, size=11)
    cols = FC[:3]
    yrs = d.years(cols)
    hdr = dict(cells=["NOKm"] + [f"{yv} {k}" for yv in yrs for k in ("Our", "Cons.", "Diff.")], fill=NAVY, color=WHITE,
               bold=True, size=7.5, h=0.27)
    rows = [hdr]
    for lab, m, dec in [("Revenue", "rev", 0), ("EBITDA", "ebitda", 0), ("EBIT", "ebit", 0), ("EPS (NOK)", "eps", 2)]:
        cells, colors, bolds = [lab], {}, {}
        for j in range(3):
            o, cns = d.c("Consensus", f"our_{m}_{j + 1}"), d.c("Consensus", f"cons_{m}_{j + 1}")
            diff = o / cns - 1
            cells += [f"{o:,.{dec}f}", f"{cns:,.{dec}f}", f"{diff:+.1%}"]
            colors[3 + j * 3] = GREEN if diff > 0 else RED
            bolds[3 + j * 3] = True
        rows.append(dict(cells=cells, size=8.5, h=0.30, line_bottom="E1E5EA", colors=colors, bolds=bolds,
                         fills={k: "EEF4F7" for k in (3, 6, 9)}))
    table(s, x2, y + 0.47, w2, rows, [1.25] + [0.62, 0.62, 0.56] * 3)
    text(s, x2, y + 2.05, w2, 0.2, f"Green = we are above consensus. Consensus: {d.c('Consensus', 'cons_source')} (Consensus sheet).",
         size=7.5, italic=True, color=MUTED)
    panel(s, x2, y + 2.35, w2, 0.95)
    text(s, x2 + 0.15, y + 2.42, w2 - 0.3, 0.85, [
        ("How to use", {"bold": True, "color": NAVY, "size": 9.5, "space_after": 2}),
        ("Tiles: max five, one message each. Scorecards: be able to defend every ball. Estimate tables: highlight only the "
         "difference column – that is where your variant view shows.", {"size": 8.5})])
    notes(s, "All tables are native PowerPoint tables. Consensus comes from the Consensus sheet in the model (reported IFRS 16 "
             "basis) – type the latest consensus there and rebuild.")
    return s
