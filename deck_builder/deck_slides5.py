"""Market overview built from company KPIs and sourced facts.

Used instead of the illustrative market slide when the case text module provides CT['market'] (see sats_deck.py)."""
from deck_core import *
from deck_data import num, pct, mult, HC, FC


def market_overview_kpi(prs, d, M, std):
    s = std(prs, M["chapter"], "Market overview", M["subtitle"], M["sources"])
    gx = [(0.47, 3.95), (4.67, 3.95)]
    y1, y2 = 1.40, 4.18
    # 1 locations and volume (members) from the model's history
    x, w = gx[0]
    panel_header(s, x, y1, w, M["p1_title"], 1)
    panel(s, x, y1 + 0.42, w, 2.30)
    yrs = d.years(HC)
    locs = d.row("Hist", "locations", HC)
    mem = [sum(v) for v in zip(*(d.row("Hist", k, HC) for k in ("vol_a", "vol_b", "vol_c")))]
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, x + 0.05, y1 + 0.50, w - 0.1, 2.2, yrs,
                   [("Clubs", locs), ("Members '000 (rhs)", mem)], [LBLUE, NAVY], size=7, legend="t", labels=True,
                   num_fmt="0", label_pos=XL_LABEL_POSITION.INSIDE_END, gap=40, val_min=0, val_max=max(locs) * 1.45,
                   label_color=NAVY)
    rg = (max(mem) - min(mem)) or 1.0                # keep the line in the band above the columns (no label collisions)
    to_combo(gf.chart, 1, color=NAVY, fmt="0", size=7, val_min=min(mem) - 4 * rg, val_max=max(mem) + 0.56 * rg)
    # 2 revenue per member per country
    x, w = gx[1]
    panel_header(s, x, y1, w, M["p2_title"], 2)
    panel(s, x, y1 + 0.42, w, 2.30)
    vmax = max(max(v) for _, v in M["arpm"])
    add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, x + 0.05, y1 + 0.50, w - 0.1, 2.2, M["arpm_years"],
              [(n, v) for n, v in M["arpm"]], [NAVY, MIDBLUE, LBLUE, "A9C8D3"], size=7, legend="t", labels=True,
              num_fmt="0", label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=60, overlap=-5, val_min=0, val_max=vmax * 1.2)
    # 3 market share and positions
    x, w = gx[0]
    panel_header(s, x, y2, w, M["p3_title"], 3)
    panel(s, x, y2 + 0.42, w, 2.30)
    sh = M["share"]
    gf = add_chart(s, XL_CHART_TYPE.DOUGHNUT, x + 0.02, y2 + 0.62, 1.60, 1.80, [a for a, _ in sh],
                   [("Share", [b for _, b in sh])], [NAVY], size=7, labels=True, num_fmt="0%")
    pl = gf.chart.plots[0]
    pl.vary_by_categories = True
    pl.data_labels.font.color.rgb = rgb(WHITE)
    pl.data_labels.font.bold = True
    for i, col in enumerate([NAVY, "C9D1D9", LBLUE, MIDBLUE][:len(sh)]):
        pt = pl.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(col)
        pt.data_label.font.size = Pt(8)
        pt.data_label.font.bold = True
        pt.data_label.font.color.rgb = rgb(WHITE if i == 0 else NAVY)
    doughnut_hole(gf.chart, 50)
    text(s, x + 0.02 + 0.40, y2 + 1.33, 0.80, 0.38, M["share_centre"], size=7, bold=True, color=NAVY, align="c", anchor="m")
    text(s, x + 1.68, y2 + 0.62, w - 1.78, 1.9, [(t, {"bullet": True, "space_after": 6}) for t in M["positions"]], size=9)
    # 4 tailwinds
    x, w = gx[1]
    panel_header(s, x, y2, w, M["p4_title"], 4)
    panel(s, x, y2 + 0.42, w, 2.30)
    for j, (stat, desc) in enumerate(M["tailwinds"]):
        yy = y2 + 0.55 + j * 0.70
        circle(s, x + 0.15, yy, 0.58, fill=NAVY if j != 1 else MIDBLUE, txt=stat, font_size=11 if len(stat) < 4 else 10)
        text(s, x + 0.88, yy + 0.02, w - 1.0, 0.56, desc, size=9.5, color=DARK, anchor="m")
    # right column: opportunities / disruption / threats
    rx, rw = 8.87, 4.00
    yy = y1
    heights = [1.95, 1.60, 1.60]
    for (title, items), col, hgt in zip(M["boxes"], [NAVY, MIDBLUE, LBLUE], heights):
        hb = rect(s, rx, yy, rw, 0.34, fill=col)
        shape_text(hb, title, size=12, color=WHITE, bold=True)
        panel(s, rx, yy + 0.38, rw, hgt - 0.45)
        text(s, rx + 0.12, yy + 0.47, rw - 0.24, hgt - 0.6, [(t, {"bullet": True, "space_after": 5}) for t in items],
             size=9.5)
        yy += hgt + 0.08
    notes(s, "Market overview from company KPIs: (1) more members per club, (2) revenue per member up in every country, "
             "(3) market share and positions, (4) demand evidence. Every figure is sourced in the footnote.\n\n"
             "TALKING POINTS: SATS grows without adding clubs – price and utilisation do the work; the roll-out is extra.")
    return s
