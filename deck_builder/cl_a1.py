"""Chart library – part 1: columns/bars, combos/lines, pies/doughnuts."""
import math
import random
from cl_core import *
from deck_data import HC, FC

XS3, W3 = [0.47, 4.67, 8.87], 4.0
YS2, H2 = [1.40, 4.18], 2.68
FOOT = ("All charts are native PowerPoint charts – right-click a chart and choose Edit Data to change the numbers. "
        "Example data: fictional Example Company ASA (from the DCF toolkit) and illustrative market data.")


def _grid(i):
    return XS3[i % 3], YS2[i // 3]


# ------------------------------------------------------------------ columns and bars
def columns_bars(prs, d):
    s = std(prs, "Chart library #1", "Column and bar charts",
            "The workhorses: levels over time, comparisons between companies and the composition of a total", FOOT)
    seg = [d.c("Inputs", k) for k in ("seg_a", "seg_b", "seg_c")]
    # 1 simple column + CAGR arrow
    x, y = _grid(0)
    box = cpanel(s, x, y, W3, H2, "Column with CAGR arrow", "revenue, EBITDA, members – history vs. forecast", 1)
    cols = HC[2:] + FC[:3]
    vals = d.row("Model", "is_rev", cols)
    vmax = max(vals) * 1.5
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, *box, d.years(cols), [("Revenue (NOKm)", vals)], [NAVY], size=7,
                   labels=True, num_fmt="0", label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=45, val_min=0, val_max=vmax)
    color_points(gf.chart, [NAVY] * 5 + [LBLUE] * 3)
    manual_plot_layout(gf.chart, *PLOT)
    X, Y = geo(box, n=len(cols), vmax=vmax)
    cg = (vals[-1] / vals[4]) ** (1 / 3) - 1
    cagr_arrow(s, X, Y, 4, vals[4], 7, vals[7], f"CAGR {cg * 100:+.1f}%")
    # 2 clustered
    x, y = _grid(1)
    box = cpanel(s, x, y, W3, H2, "Clustered column", "company vs. market / peers / consensus", 2)
    cols2 = HC[4:] + FC[:3]
    comp = d.row("Model", "grev", cols2)
    mkt = [0.070, 0.048, 0.045, 0.041, 0.039, 0.040]
    add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, *box, d.years(cols2), [("Company growth", comp), ("Market growth", mkt)],
              [NAVY, LBLUE], size=7, legend="t", labels=True, num_fmt="0%", label_pos=XL_LABEL_POSITION.OUTSIDE_END,
              gap=55, overlap=-5)
    # 3 stacked
    x, y = _grid(2)
    box = cpanel(s, x, y, W3, H2, "Stacked column", "revenue or EBIT by segment over time", 3)
    cols3 = HC[3:] + FC[:3]
    series = [(seg[i], d.row("Model", f"rev_{k}", cols3)) for i, k in enumerate("abc")]
    add_chart(s, XL_CHART_TYPE.COLUMN_STACKED, *box, d.years(cols3), series, [NAVY, MIDBLUE, LBLUE], size=7, legend="t",
              labels=True, num_fmt="0", label_pos=XL_LABEL_POSITION.CENTER, gap=40, overlap=100, label_color=WHITE)
    # 4 100% stacked
    x, y = _grid(3)
    box = cpanel(s, x, y, W3, H2, "100% stacked column", "how the mix shifts over time", 4)
    tot = [sum(v) for v in zip(*[sr[1] for sr in series])]
    shares = [(n, [v / t for v, t in zip(vs, tot)]) for n, vs in series]
    add_chart(s, XL_CHART_TYPE.COLUMN_STACKED_100, *box, d.years(cols3), shares, [NAVY, MIDBLUE, LBLUE], size=7,
              legend="t", labels=True, num_fmt="0%", label_pos=XL_LABEL_POSITION.CENTER, gap=40, overlap=100,
              label_color=WHITE)
    # 5 horizontal ranking with median line
    x, y = _grid(4)
    box = cpanel(s, x, y, W3, H2, "Ranked bar with median line", "multiples, margins or growth across the peer group", 5)
    cr = d.reg["comps"]
    peers = [(d.v("Comps", f"B{r}"), d.v("Comps", f"M{r}")) for r in range(6, 14)]
    peers.append((d.c("Inputs", "company").replace(" ASA", ""), d.v("Comps", f"M{cr['company']}")))
    peers.sort(key=lambda p: -p[1])
    vmax = max(p[1] for p in peers) * 1.22
    plot = (0.30, 0.03, 0.66, 0.94)
    gf = add_chart(s, XL_CHART_TYPE.BAR_CLUSTERED, *box, [p[0] for p in peers], [("EV/EBIT", [p[1] for p in peers])],
                   [LBLUE], size=7, labels=True, num_fmt='0.0"x"', label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=35,
                   val_min=0, val_max=vmax)
    color_points(gf.chart, [NAVY if "Example" in p[0] else LBLUE for p in peers])
    set_cat_reverse(gf.chart)
    manual_plot_layout(gf.chart, *plot)
    gf.chart.category_axis.format.line.fill.background()
    med = d.v("Comps", f"M{cr['median']}")
    Xh, _ = geo(box, plot, n=len(peers), vmax=vmax, horizontal=True)
    line(s, Xh(med), box[1] + 0.02, Xh(med), box[1] + box[3] - 0.02, color=DARK, width=1, dash=MSO_LINE_DASH_STYLE.DASH)
    text(s, Xh(med) + 0.55, box[1] + box[3] - 0.24, 1.2, 0.2, f"Median {med:.1f}x", size=7, bold=True)
    # 6 positive / negative columns
    x, y = _grid(5)
    box = cpanel(s, x, y, W3, H2, "Positive / negative columns", "share price performance, estimate revisions, surprises", 6)
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, *box, ["1M", "3M", "6M", "12M", "YTD"],
                   [("Company", [-0.031, 0.064, 0.118, 0.196, 0.142]), ("OSEBX", [0.012, 0.035, -0.024, 0.087, 0.061])],
                   [NAVY, LBLUE], size=7, legend="t", labels=True, num_fmt="0%;-0%", label_pos=XL_LABEL_POSITION.OUTSIDE_END,
                   gap=60, overlap=-5, val_min=-0.10, val_max=0.25)
    gf.chart.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    notes(s, "Copy a chart: click it, Ctrl+C, paste into your deck with 'Keep source formatting'. Edit Data opens the "
             "embedded worksheet. Colours: navy 003255 = company / history, light blue 81B0C0 = peers / forecast.")
    return s


# ------------------------------------------------------------------ combos and lines
def combos_lines(prs, d):
    s = std(prs, "Chart library #2", "Combination, line and area charts",
            "Two measures in one picture (level + ratio), developments over time and scenario paths", FOOT)
    # 1 revenue + margin
    x, y = _grid(0)
    box = cpanel(s, x, y, W3, H2, "Columns + line on secondary axis", "revenue and margin, volume and price", 1)
    cols = HC[2:] + FC[:3]
    rev, ebit, marg = (d.row("Model", k, cols) for k in ("is_rev", "ebit_adj", "ebit_adj_m"))
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, *box, d.years(cols),
                   [("Revenue", rev), ("EBIT adj.", ebit), ("EBIT adj. margin", marg)], [NAVY, LBLUE, NAVY], size=7,
                   legend="t", labels=True, num_fmt="0", label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=40, overlap=-5,
                   val_min=0, val_max=max(rev) * 1.55)
    lo, hi = min(marg), max(marg)
    rng = (hi - lo) / 0.12
    to_combo(gf.chart, 2, color=AMBER, fmt="0%", size=7, label_color="7A6A10", val_min=round(lo - 0.78 * rng, 4),
             val_max=round(lo + 0.22 * rng, 4))
    manual_plot_layout(gf.chart, 0.02, 0.17, 0.96, 0.70)
    # 2 FCFF + conversion
    x, y = _grid(1)
    box = cpanel(s, x, y, W3, H2, "Single column + line", "cash flow and cash conversion, capex and capex/sales", 2)
    cols2 = HC[3:] + FC[:4]
    fcf, conv = d.row("Model", "fcff", cols2), d.row("Model", "cconv", cols2)
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, *box, d.years(cols2), [("FCFF (NOKm)", fcf), ("Cash conversion", conv)],
                   [LBLUE, NAVY], size=7, legend="t", labels=True, num_fmt="0", label_pos=XL_LABEL_POSITION.INSIDE_END,
                   gap=45, val_min=0, val_max=max(fcf) * 1.6, label_color=WHITE)
    to_combo(gf.chart, 1, color=NAVY, fmt="0%", size=7, val_min=-0.6, val_max=0.75)
    manual_plot_layout(gf.chart, 0.02, 0.17, 0.96, 0.70)
    # 3 scenario lines
    x, y = _grid(2)
    box = cpanel(s, x, y, W3, H2, "Multi-line – scenario paths", "bear / base / bull, or company vs. peers over time", 3)
    t4 = {k: c for c, k, _, _ in d.reg["t4"]}
    r0 = d.reg["sens"]["t4_rows"][0]
    last = d.row("Model", "is_rev", ["K"])[0]
    paths = [(nm, [last] + [d.v("Sensitivity", f"{t4[f'rev{i + 1}']}{r0 + j}") for i in range(8)])
             for j, nm in enumerate(["Bear", "Base", "Bull"])]
    gf = add_chart(s, XL_CHART_TYPE.LINE, *box, d.years(["K"]) + d.years(FC), paths, [RED, NAVY, GREEN], size=7, legend="t",
                   labels=False, num_fmt="0", val_axis=True, gridlines=True, val_min=round(last * 0.9, -3))
    gf.chart.value_axis.tick_labels.number_format = "0"
    gf.chart.value_axis.tick_labels.number_format_is_linked = False
    # 4 margin vs peers lines
    x, y = _grid(3)
    box = cpanel(s, x, y, W3, H2, "Line – company vs. peer average", "margin, ROIC or leverage against the peer group", 4)
    cols4 = HC[1:] + FC[:3]
    cm = d.row("Model", "ebit_adj_m", cols4)
    pm = [0.118, 0.121, 0.127, 0.131, 0.136, 0.139, 0.141, 0.142, 0.143]
    gf = add_chart(s, XL_CHART_TYPE.LINE_MARKERS, *box, d.years(cols4), [("Company EBIT margin", cm), ("Peer average", pm)],
                   [NAVY, LBLUE], size=7, legend="t", labels=False, num_fmt="0%", val_axis=True, gridlines=True, val_min=0.06,
                   val_max=0.20)
    gf.chart.value_axis.tick_labels.number_format = "0%"
    gf.chart.value_axis.tick_labels.number_format_is_linked = False
    # 5 stacked area
    x, y = _grid(4)
    box = cpanel(s, x, y, W3, H2, "Stacked area", "market size by segment or channel", 5)
    yrs = [str(2019 + i) for i in range(7)] + [f"{2026 + i}E" for i in range(5)]
    tot = [29.0, 26.5, 28.0, 31.4, 33.6, 35.2, 36.8, 38.3, 39.8, 41.4, 42.9, 44.5]
    sh = [(0.62, 0.30, 0.08), (0.60, 0.30, 0.10), (0.58, 0.31, 0.11), (0.57, 0.31, 0.12), (0.55, 0.32, 0.13),
          (0.54, 0.32, 0.14), (0.53, 0.32, 0.15), (0.52, 0.32, 0.16), (0.51, 0.32, 0.17), (0.50, 0.32, 0.18),
          (0.49, 0.32, 0.19), (0.48, 0.32, 0.20)]
    ser = [(nm, [round(t * q[j], 1) for t, q in zip(tot, sh)]) for j, nm in enumerate(["Premium", "Mid-market", "Low-cost"])]
    gf = add_chart(s, XL_CHART_TYPE.AREA_STACKED, *box, yrs, ser, [NAVY, MIDBLUE, LBLUE], size=7, legend="t", labels=False,
                   num_fmt="0", val_axis=True, gridlines=True, gap=None)
    gf.chart.value_axis.tick_labels.number_format = "0"
    gf.chart.value_axis.tick_labels.number_format_is_linked = False
    # 6 forward P/E band
    x, y = _grid(5)
    box = cpanel(s, x, y, W3, H2, "Multiple over time with average ± 1 std. dev.", "is the stock cheap vs. its own history?", 6)
    rnd = random.Random(11)
    pe, v = [], 15.5
    for i in range(60):
        v += 0.35 * (14.8 - v) * 0.2 + rnd.uniform(-0.7, 0.7)
        pe.append(round(v, 1))
    avg = sum(pe) / len(pe)
    sd = math.sqrt(sum((p - avg) ** 2 for p in pe) / len(pe))
    months = [f"{['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][(9 + i) % 12]}-{21 + (9 + i) // 12}"
              for i in range(60)]
    gf = add_chart(s, XL_CHART_TYPE.LINE, *box, months,
                   [("12m fwd P/E", pe), ("Average", [round(avg, 1)] * 60), ("+1 std", [round(avg + sd, 1)] * 60),
                    ("−1 std", [round(avg - sd, 1)] * 60)], [NAVY, DARK, MUTED, MUTED], size=7, legend="t", labels=False,
                   num_fmt='0"x"', val_axis=True, gridlines=False, val_min=math.floor(min(pe) - 2), val_max=math.ceil(max(pe) + 2))
    gf.chart.value_axis.tick_labels.number_format = '0"x"'
    gf.chart.value_axis.tick_labels.number_format_is_linked = False
    label_skip(gf.chart, 12)
    for k in (1, 2, 3):
        series_dash(gf.chart, k, "sysDash" if k > 1 else "dash", 1.0)
    notes(s, "Combination charts: the line sits on a hidden secondary axis – change its scale under Format Axis if your "
             "margins are very different. The P/E history is randomly generated example data.")
    return s


# ------------------------------------------------------------------ pies and doughnuts
def pies(prs, d):
    s = std(prs, "Chart library #3", "Pie and doughnut charts",
            "Composition at one point in time – keep to five slices or fewer and put the most important slice in navy", FOOT)
    seg = [d.c("Inputs", k) for k in ("seg_a", "seg_b", "seg_c")]
    rev = [d.row("Hist", k, ["K"])[0] for k in ("rev_a", "rev_b", "rev_c")]
    # 1 pie with outside labels
    x, y = _grid(0)
    box = cpanel(s, x, y, W3, H2, "Pie with labels", "shareholder structure, customer mix", 1)
    own = [("Founder family", 0.28), ("Folketrygdfondet", 0.09), ("Nordic funds", 0.21), ("International funds", 0.27),
           ("Retail & other", 0.15)]
    pie(s, (box[0] + 0.3, box[1], box[2] - 0.6, box[3]), [o[0] for o in own], [o[1] for o in own],
        [NAVY, MIDBLUE, LBLUE, SOFT, LGREY], size=7, labels="name")
    # 2 doughnut with centre
    x, y = _grid(1)
    box = cpanel(s, x, y, W3, H2, "Doughnut with total in the centre", "revenue by segment or geography", 2)
    pie(s, (box[0], box[1], 2.3, box[3]), seg, rev, [NAVY, MIDBLUE, LBLUE], size=8, doughnut=True, hole=52,
        centre=["NOKm", f"{sum(rev):,.0f}"])
    swatches(s, box[0] + 2.4, box[1] + 0.55, list(zip(seg, [NAVY, MIDBLUE, LBLUE])), vertical=True, size=8.5, dy=0.3)
    # 3 market share
    x, y = _grid(2)
    box = cpanel(s, x, y, W3, H2, "Market share doughnut", "highlight the company, grey out the rest", 3)
    ms = [("Example Company", 0.15), ("Competitor A", 0.12), ("Competitor B", 0.09), ("Competitor C", 0.06), ("Others", 0.58)]
    cols = [NAVY, MIDBLUE, LBLUE, SOFT, LGREY]
    pie(s, (box[0], box[1], 2.3, box[3]), [m[0] for m in ms], [m[1] for m in ms], cols, size=8, doughnut=True, hole=50,
        centre=["2025", "NOK 37bn"], label_colors=[WHITE, WHITE, WHITE, NAVY, NAVY])
    swatches(s, box[0] + 2.4, box[1] + 0.25, [(m[0], c) for m, c in zip(ms, cols)], vertical=True, size=8.5, dy=0.3)
    # 4 twin doughnuts
    x, y = _grid(3)
    box = cpanel(s, x, y, W3, H2, "Twin doughnuts", "revenue vs. profit mix – where is the money made?", 4)
    ebit = [0.58, 0.31, 0.11]
    for j, (vals, lab, ctr) in enumerate([(rev, "Revenue", "Revenue"), (ebit, "EBIT", "EBIT")]):
        pie(s, (box[0] + j * 2.0, box[1] + 0.05, 2.0, box[3] - 0.35), seg, vals, [NAVY, MIDBLUE, LBLUE], size=7.5,
            doughnut=True, hole=50, centre=[ctr])
    swatches(s, box[0] + 0.3, box[1] + box[3] - 0.27, list(zip(seg, [NAVY, MIDBLUE, LBLUE])), dx=1.15, size=7.5)
    # 5 KPI rings
    x, y = _grid(4)
    box = cpanel(s, x, y, W3, H2, "KPI rings", "one number that matters: recurring revenue, utilisation, payout", 5)
    for j, (v, lab) in enumerate([(0.90, "Recurring revenue"), (0.62, "Cash conversion"), (0.68, "Payout ratio")]):
        bx = (box[0] + j * 1.33, box[1] + 0.02, 1.33, 1.45)
        pie(s, bx, ["Value", "Rest"], [v, 1 - v], [NAVY, "E3E8EC"], size=9, doughnut=True, hole=68,
            centre=[f"{v * 100:.0f}%"], labels=None)
        text(s, bx[0], box[1] + 1.48, 1.33, 0.4, lab, size=8.5, bold=True, color=NAVY, align="c")
    # 6 single 100% bar
    x, y = _grid(5)
    box = cpanel(s, x, y, W3, H2, "100% bar – the space-saving alternative", "a mix in one line, e.g. cost base or funding", 6)
    costs = [("COGS", 0.366), ("Personnel", 0.218), ("Other opex", 0.119), ("Leases", 0.078), ("D&A", 0.044), ("EBIT adj.", 0.175)]
    gf = add_chart(s, XL_CHART_TYPE.BAR_STACKED_100, box[0], box[1] + 0.25, box[2], 1.05, ["% of revenue 2025"],
                   [(c[0], [c[1]]) for c in costs], [LGREY, SOFT, LBLUE, MIDBLUE, "6B7480", NAVY], size=7.5, labels=True,
                   num_fmt="0%", label_pos=XL_LABEL_POSITION.CENTER, gap=30, overlap=100, cat_axis=False)
    for k, srs in enumerate(gf.chart.plots[0].series):
        srs.data_labels.font.size = Pt(7.5)
        srs.data_labels.font.bold = True
        srs.data_labels.font.color.rgb = rgb(WHITE if k >= 3 else NAVY)
        srs.data_labels.number_format, srs.data_labels.number_format_is_linked = "0%", False
        srs.data_labels.show_value = True
        srs.data_labels.position = XL_LABEL_POSITION.CENTER
    swatches(s, box[0] + 0.05, box[1] + 1.38, [(c[0], col) for c, col in zip(costs[:3], [LGREY, SOFT, LBLUE])], dx=1.3, size=7.5)
    swatches(s, box[0] + 0.05, box[1] + 1.62, [(c[0], col) for c, col in zip(costs[3:], [MIDBLUE, "6B7480", NAVY])], dx=1.3, size=7.5)
    notes(s, "Doughnut centre labels are text boxes on top of the chart – move them together with the chart (select both, "
             "Ctrl+G to group). Ownership and EBIT mix are illustrative.")
    return s
