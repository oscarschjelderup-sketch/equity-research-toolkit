"""Cover, case team, company overview and market overview."""
import json
import os

from deck_core import *
from deck_data import num, pct, mult, HC, FC
from deck_case import ct, case_fn

TEAM_DIR = "team"

# illustrative market data (fictional – replace with sourced data)
MKT_YEARS = ["2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026E", "2027E", "2028E", "2029E", "2030E"]
MKT_SIZE = [29.0, 26.5, 28.0, 31.4, 33.6, 35.2, 36.8, 38.3, 39.8, 41.4, 42.9, 44.5]
SHARES = [("Example Company", 0.15), ("Competitor A", 0.12), ("Competitor B", 0.09), ("Competitor C", 0.06),
          ("Others", 0.58)]


def std(prs, chapter, title, subtitle, footnote):
    return new_slide(prs, "No objects", title=title, subtitle=subtitle, chapter=chapter, footnote=case_fn(footnote))


# ------------------------------------------------------------------ 1 cover
def cover(prs, d):
    s = new_slide(prs, "Title slide - blue", ph_text={
        0: ct("cover_title", f"{d.c('Inputs', 'company')} – Compounding quality at a discount"),
        1: ct("cover_sub", "Pareto Equity Research Competition 2026"),
        12: ct("cover_dates", "[Case dates, e.g. 09 – 12.02.26]")})
    notes(s, "TEMPLATE: Replace the title with your own equity story in 4-6 words (e.g. 'SATS – Healthy body, healthy "
             "margins'). Keep the competition name. Update the date line.\n\n"
             "TALKING POINT: One sentence on who we are and our recommendation: 'We recommend BUY with a target price of "
             f"NOK {d.c('DCF', 'tp'):.0f}.'")
    return s


# ------------------------------------------------------------------ 2 team
def _load_team():
    """Team members from team/team.json – [[name, photo file or null, [line, ...]], ...]. The team folder is kept out of
    version control (names and photos of real people); without it the slide shows placeholders."""
    try:
        if os.environ.get("EQR_TEAM", "").lower() == "none":       # build with placeholders even if team.json exists
            raise OSError
        with open(os.path.join(TEAM_DIR, "team.json"), encoding="utf8") as f:
            return [tuple(m) for m in json.load(f)]
    except (OSError, ValueError):
        return [(f"Team member {i}", None, ["University: [your university]", "Year of study: [year]",
                                            "Experience: [relevant experience]"]) for i in (1, 2, 3)]


TEAM = _load_team()


def team(prs, d):
    s = std(prs, None, "Case-team",
            "CBS case team with a passion for equity research – presenting a model-driven investment case", None)
    xs = [0.47, 4.67, 8.87]
    for (name, img, lines), x in zip(ct("team", TEAM), xs):
        y = 1.75
        photo = os.path.join(TEAM_DIR, img) if img else None
        if photo and os.path.exists(photo):
            picture(s, photo, x, y, w=1.52, h=1.90)
        else:
            ph = rect(s, x, y, 1.52, 1.90, fill=PANEL)
            shape_text(ph, "".join(p[0] for p in name.split()[:2]).upper(), size=22, color=MUTED, bold=True)
        text(s, x + 1.70, y + 0.05, 2.25, 1.8,
             [(ln, {"space_after": 5}) for ln in lines], size=10.5, color=DARK)
        bar = rect(s, x, y + 2.02, 3.95, 0.40, fill=LBLUE)
        shape_text(bar, name, size=12, color=WHITE, bold=True, align="l", margin=0.12)
    panel(s, 0.47, 4.80, 12.40, 1.55, fill=PANEL)
    text(s, 0.72, 4.95, 5.6, 0.3, "Why we chose this company", size=12, bold=True, color=NAVY)
    text(s, 0.72, 5.30, 5.7, 1.0, [
        ("Clear equity story: **market leader** with pricing power and a scalable cost base", {"bullet": True, "space_after": 4}),
        ("A market that underestimates **margin expansion and cash generation**", {"bullet": True, "space_after": 4}),
        ("Valuation gap we can **quantify and stress-test** in scenarios", {"bullet": True}),
    ], size=10.5)
    n_checks = sum(1 for r in range(7, 80) if d.v("Checks", f"C{r}"))
    text(s, 6.87, 4.95, 5.6, 0.3, "How we worked", size=12, bold=True, color=NAVY)
    text(s, 6.87, 5.30, 5.8, 1.0, [
        ("Bottom-up model: **locations x volume x price** per segment, IFRS 16-consistent DCF", {"bullet": True, "space_after": 4}),
        (f"Reverse DCF, **consensus gap**, peers, scenarios and {n_checks} integrity checks", {"bullet": True, "space_after": 4}),
        ("Every number in this deck ties back to **one Excel model**", {"bullet": True}),
    ], size=10.5)
    notes(s, "TEMPLATE: Update year of study, experience and photos if the team changes. The Pareto rules do not count "
             "this slide or the cover towards the 4-slide limit.\n\nTALKING POINT: Keep the introduction under 30 seconds.")
    return s


# ------------------------------------------------------------------ 3 company overview
def company_overview(prs, d):
    comp = d.c("Inputs", "company")
    s = std(prs, ct("ov_chapter", "#1 The equity story of a Nordic market leader"), "Company overview",
            ct("ov_subtitle", f"{comp} – the Nordic leader in subscription-based consumer services"),
            ct("ov_sources", "Sources: Company reports, case team estimates. Example Company ASA is a fictional company – all figures are "
            "illustrative.  (1) EBIT adjusted: pre-IFRS 16 and excl. special items."))
    vol_tot = sum(d.row("Hist", k, ["K"])[0] for k in ["vol_a", "vol_b", "vol_c"])
    locs = d.row("Hist", "locations", ["K"])[0]
    m_fc = d.row("Model", "ebit_adj_m", ["P"])[0]
    _kb = ct("ov_key")
    key_box(s, 1.36, _kb.format(comp=comp, vol=num(vol_tot), locs=num(locs), m=m_fc * 100) if _kb else f"{comp} is the **#1 operator in the Nordics** with ~{SHARES[0][1] * 100:.0f}% market share, "
                     f"**{num(vol_tot)}k subscribers** and {num(locs)} locations. A **recurring revenue model**, proven "
                     f"**pricing power** and a scalable cost base support **~{m_fc * 100:.0f}% EBIT margins** and "
                     f"**ROIC well above WACC**.", h=0.55)
    cols = [(0.47, 3.95), (4.67, 3.95), (8.87, 4.00)]
    y1, y2 = 2.02, 4.55
    # 1 snapshot
    x, w = cols[0]
    panel_header(s, x, y1, w, "Company snapshot", 1)
    panel(s, x, y1 + 0.42, w, 2.0)
    vol = sum(d.row("Hist", k, ["K"])[0] for k in ["vol_a", "vol_b", "vol_c"])
    rows = [("Sector", d.c("Inputs", "sector")), ("Headquarters", ct("ov_hq", "Oslo, Norway")),
            ("Listing", f"{d.c('Inputs', 'exchange')} ({d.c('Inputs', 'ticker')})"),
            (ct("vol_label", "Subscribers") + " (2025)", f"{num(vol)}{ct('vol_suffix', 'k')}"),
            ct("ov_loc_row") or ("Locations (2025)", num(d.row("Hist", "locations", ["K"])[0])),
            ct("employees_row") or ("Employees (FTE)", num(d.row("Hist", "ftes", ["K"])[0])),
            ("Market cap (NOKm)", num(d.c("Inputs", "mcap"))),
            ("Enterprise value (NOKm)", num(d.c("Inputs", "ev_ex")))]
    table(s, x + 0.12, y1 + 0.52, w - 0.24,
          [dict(cells=[a, b], bolds={0: True}, size=9.5, h=0.225) for a, b in rows], [1.9, 1.8])
    # 2 business model
    x, w = cols[1]
    panel_header(s, x, y1, w, ct("ov_panel2", "Scalable model with pricing power"), 2)
    panel(s, x, y1 + 0.42, w, 2.0)
    pxc = d.row("Model", "g_pxc", ["H", "I", "J", "K"])
    m21, m25 = d.row("Model", "ebit_adj_m", ["G", "K"])
    capex25 = d.row("Hist", "capex_pct", ["K"])[0]
    y21, y25 = d.years(["G", "K"])
    text(s, x + 0.12, y1 + 0.52, w - 0.24, 1.85, [
        (ct("ov_recurring", "**Recurring revenue:** ~90% of sales from monthly subscriptions"), {"bullet": True, "space_after": 5}),
        (ct("ov_pricing") or f"**Pricing power:** price/mix has added {min(pxc) * 100:.0f}-{max(pxc) * 100:.0f}% p.a. since {d.years(['H'])[0][:4]}",
         {"bullet": True, "space_after": 5}),
        (ct("ov_leverage") or f"**Operating leverage:** EBIT adj. margin up from {m21 * 100:.1f}% ({y21}) to {m25 * 100:.1f}% ({y25})",
         {"bullet": True, "space_after": 5}),
        (ct("ov_fourth") or f"**Capital light:** capex {capex25 * 100:.1f}% of sales and negative working capital", {"bullet": True}),
    ], size=9.5)
    # 3 management
    x, w = cols[2]
    panel_header(s, x, y1, w, "Experienced management team", 3)
    panel(s, x, y1 + 0.42, w, 2.0)
    mgmt = ct("mgmt") or [("KN", "CEO – Kari Nordmann", "Joined 2018; former COO of a Nordic retailer"),
            ("ON", "CFO – Ola Nordmann", "Joined 2020; 15 years in corporate finance"),
            ("MN", "COO – Mari Nordmann", "Joined 2016; led the Nordic roll-out")]
    for j, (ini, role, desc) in enumerate(mgmt):
        yy = y1 + 0.55 + j * 0.62
        circle(s, x + 0.18, yy, 0.50, fill=NAVY if j == 0 else MIDBLUE, txt=ini, font_size=11)
        text(s, x + 0.85, yy + 0.02, w - 1.0, 0.25, role, size=10.5, bold=True, color=DARK)
        text(s, x + 0.85, yy + 0.25, w - 1.0, 0.25, desc, size=9, color=MUTED)
    # 4 revenue mix doughnuts
    x, w = cols[0]
    panel_header(s, x, y2, w, f"Revenue and {ct('vol_word', 'subscriber')} mix (2025)", 4)
    panel(s, x, y2 + 0.42, w, 1.93)
    segs = [d.c("Inputs", k) for k in ("seg_a", "seg_b", "seg_c")]
    rev = [d.row("Hist", k, ["K"])[0] for k in ("rev_a", "rev_b", "rev_c")]
    vols = [d.row("Hist", k, ["K"])[0] for k in ("vol_a", "vol_b", "vol_c")]
    for j, (vals, lab, centre) in enumerate([(rev, "Revenue", f"NOKm\n{num(sum(rev))}"),
                                             (vols, ct("vol_label", "Subscribers"), f"{num(sum(vols))}{ct('vol_suffix', 'k')}")]):
        cx = x + 0.05 + j * 1.95
        gf = add_chart(s, XL_CHART_TYPE.DOUGHNUT, cx, y2 + 0.62, 1.85, 1.45, segs, [(lab, vals)],
                       [NAVY], size=7, legend=None, labels=True, num_fmt="0%")
        ch = gf.chart
        pl = ch.plots[0]
        pl.vary_by_categories = True
        dl = pl.data_labels
        dl.show_percentage = True
        dl.show_value = False
        dl.number_format = "0%"
        dl.font.color.rgb = rgb(WHITE)
        dl.font.bold = True
        for i, col in enumerate([NAVY, MIDBLUE, LBLUE]):
            pt = pl.series[0].points[i]
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = rgb(col)
        doughnut_hole(ch, 52)
        text(s, cx + 0.45, y2 + 1.14, 0.95, 0.42, centre.split("\n"), size=8, bold=True, color=NAVY, align="c", anchor="m")
        text(s, cx, y2 + 0.45, 1.85, 0.2, lab, size=9, bold=True, color=NAVY, align="c")
    # legend
    for i, (sg, col) in enumerate(zip(segs, [NAVY, MIDBLUE, LBLUE])):
        lx = x + 0.25 + i * 1.25
        rect(s, lx, y2 + 2.13, 0.12, 0.12, fill=col)
        text(s, lx + 0.16, y2 + 2.08, 1.1, 0.22, sg, size=8, color=DARK)
    # 5 revenue & margin combo
    x, w = cols[1]
    panel_header(s, x, y2, w, ct("ov_panel5", "Consistent growth with margin expansion"), 5)
    cols5 = HC[ct("ov_hist_from", 2):] + FC[:3]
    yrs = d.years(cols5)
    revs = d.row("Model", "is_rev", cols5)
    ebit = d.row("Model", "ebit_adj", cols5)
    marg = d.row("Model", "ebit_adj_m", cols5)
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, x, y2 + 0.45, w, 1.95, yrs,
                   [("Revenue", revs), ("EBIT adj.(1)", ebit), ("EBIT adj. margin", marg)],
                   [NAVY, LBLUE, NAVY], size=7, legend="t", labels=True, num_fmt="0",
                   label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=40, overlap=-5, val_min=0, val_max=max(revs) * 1.55)
    lo, hi = min(marg), max(marg)
    rng = (hi - lo) / (0.90 - 0.78)
    to_combo(gf.chart, 2, color=AMBER, fmt="0%", size=7, label_color="7A6A10",
             val_min=round(lo - 0.78 * rng, 4), val_max=round(lo - 0.78 * rng + rng, 4))
    manual_plot_layout(gf.chart, 0.02, 0.17, 0.96, 0.70)
    # 6 returns table
    x, w = cols[2]
    panel_header(s, x, y2, w, "…and returns well above the cost of capital", 6)
    cols6 = HC[4:] + FC[:3]
    yrs6 = d.years(cols6)
    wacc = d.c("WACC", "wacc")
    hdr = dict(cells=[""] + yrs6, fill=NAVY, color=WHITE, bold=True, size=8.5, h=0.26)
    body = [
        ("Profitability", None, None),
        ("EBITDA margin", "ebitda_m", pct), ("EBIT adj. margin", "ebit_adj_m", pct),
        ("Returns & cash", None, None),
        ("ROIC", "roic", pct), ("WACC", "_wacc", pct), ("FCF yield", "fcf_yield", pct), ("Dividend yield", "div_yield", pct),
    ]
    rows = [hdr]
    for lab, key, f in body:
        if key is None:
            rows.append(dict(cells=[lab] + [""] * 6, bold=True, color=NAVY, size=8.5, h=0.22))
        elif key == "_wacc":
            rows.append(dict(cells=[lab] + [pct(wacc)] * 6, size=8.5, h=0.21, color=MUTED))
        else:
            vals = d.row("Model", key, cols6)
            rows.append(dict(cells=[lab] + [f(v) for v in vals], size=8.5, h=0.21,
                             bold=key == "roic", fills={j + 1: "E4EEF2" for j in range(3, 6)}))
    panel(s, x, y2 + 0.42, w, 1.93, fill=WHITE)
    table(s, x, y2 + 0.45, w, rows, [1.35] + [0.44] * 6)
    notes(s, "TEMPLATE: Keep the heading 'Company overview' (Pareto rule). Replace the key message, snapshot facts, "
             "management and segment names. Charts read from the model (Model sheet).\n\n"
             "TALKING POINTS: (1) What the company does and why it wins. (2) Growth has been driven by both volume and "
             "price. (3) Margins have expanded and returns are far above WACC – quality at a reasonable price.")
    return s


# ------------------------------------------------------------------ 4 market overview
def market_overview(prs, d):
    comp = d.c("Inputs", "company")
    if ct("market"):                     # case module supplies a sourced market slide
        from deck_slides5 import market_overview_kpi
        return market_overview_kpi(prs, d, ct("market"), std)
    if ct("market_retail"):              # store chain: market size, share, runway
        from retail_slides import market_overview_retail
        return market_overview_retail(prs, d)
    cagr = (MKT_SIZE[-1] / MKT_SIZE[6]) ** (1 / 5) - 1
    s = std(prs, "#2 Attractive market supported by structural tailwinds", "Market overview",
            f"A NOK {MKT_SIZE[6]:.0f}bn Nordic market growing ~{cagr * 100:.0f}% p.a. – {comp.split(' ASA')[0]} is positioned to keep outgrowing it",
            "Sources: Illustrative market data for the template (replace with e.g. SSB, Eurostat, industry reports and "
            "company reports). Company growth from the case team model.")
    gx = [(0.47, 3.95), (4.67, 3.95)]
    y1, y2 = 1.40, 4.18
    # 1 market size
    x, w = gx[0]
    panel_header(s, x, y1, w, "Nordic market size (NOKbn)", 1)
    panel(s, x, y1 + 0.42, w, 2.30)
    cx0, cy0, cw, chh = x + 0.05, y1 + 0.72, w - 0.1, 1.98
    px, py, pw, ph = 0.02, 0.04, 0.96, 0.84
    gf = add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, cx0, cy0, cw, chh, MKT_YEARS,
                   [("Market", MKT_SIZE)], [NAVY], size=7, labels=True, num_fmt="0",
                   label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=45, val_min=0, val_max=60)
    manual_plot_layout(gf.chart, px, py, pw, ph)
    color_points(gf.chart, [NAVY] * 7 + [LBLUE] * 5)
    n = len(MKT_YEARS)
    bx = lambda i: cx0 + (px + pw * (i + 0.5) / n) * cw
    by = lambda v: cy0 + (py + ph * (1 - v / 60)) * chh
    ax1, ay1 = bx(6), by(MKT_SIZE[6]) - 0.30
    ax2, ay2 = bx(11), by(MKT_SIZE[11]) - 0.30
    line(s, ax1, ay1, ax2, ay2, color=DARK, width=1.25, arrow_end=True)
    b = rect(s, (ax1 + ax2) / 2 - 0.48, (ay1 + ay2) / 2 - 0.40, 0.96, 0.26, fill=WHITE, line=DARK,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    shape_text(b, f"CAGR +{cagr * 100:.1f}%", size=8, color=DARK, bold=True, margin=0)
    text(s, x + 0.12, y1 + 0.50, 2.0, 0.22, "Actual (navy) and forecast (light blue)", size=7.5, italic=True, color=MUTED)
    # 2 company vs market
    x, w = gx[1]
    panel_header(s, x, y1, w, "Consistently outgrowing the market", 2)
    panel(s, x, y1 + 0.42, w, 2.30)
    cols2 = HC[max(3, ct("hist_first", 0)):] + FC[:3]
    yrs2 = d.years(cols2)
    comp_g = d.row("Model", "grev", cols2)
    mkt_g = [MKT_SIZE[i] / MKT_SIZE[i - 1] - 1 for i in range(3, 10)]
    add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, x + 0.05, y1 + 0.50, w - 0.1, 2.2, yrs2,
              [(comp.split(" ASA")[0], comp_g), ("Market", mkt_g)], [NAVY, LBLUE], size=7, legend="t",
              labels=True, num_fmt="0%", label_pos=XL_LABEL_POSITION.OUTSIDE_END, gap=50, overlap=-5)
    # 3 market share
    x, w = gx[0]
    panel_header(s, x, y2, w, "Fragmented market – #1 with ~15% share", 3)
    panel(s, x, y2 + 0.42, w, 2.30)
    gf = add_chart(s, XL_CHART_TYPE.DOUGHNUT, x + 0.1, y2 + 0.55, 2.0, 2.05, [a for a, _ in SHARES],
                   [("Share", [b for _, b in SHARES])], [NAVY], size=7, labels=True, num_fmt="0%")
    pl = gf.chart.plots[0]
    pl.vary_by_categories = True
    pl.data_labels.font.color.rgb = rgb(WHITE)
    pl.data_labels.font.bold = True
    cols3 = [NAVY, MIDBLUE, LBLUE, "A9C8D3", "C9D1D9"]
    for i, col in enumerate(cols3):
        pt = pl.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(col)
        pt.data_label.font.size = Pt(8)
        pt.data_label.font.bold = True
        pt.data_label.font.color.rgb = rgb(WHITE if i < 3 else NAVY)
    doughnut_hole(gf.chart, 50)
    text(s, x + 0.72, y2 + 1.38, 0.76, 0.4, ["2025", "NOK 37bn"], size=7.5, bold=True, color=NAVY, align="c", anchor="m")
    for i, ((lab, v), col) in enumerate(zip(SHARES, cols3)):
        ly = y2 + 0.78 + i * 0.30
        rect(s, x + 2.25, ly + 0.04, 0.13, 0.13, fill=col)
        text(s, x + 2.43, ly, 1.45, 0.22, f"{lab}", size=8.5, color=DARK, bold=i == 0)
    # 4 tailwinds
    x, w = gx[1]
    panel_header(s, x, y2, w, "Structural tailwinds support demand", 4)
    panel(s, x, y2 + 0.42, w, 2.30)
    tw = [("+3%", "Real disposable income growth p.a. supports willingness to pay"),
          ("70%", "of new subscribers now join via digital channels – lower acquisition cost"),
          ("M&A", "Fragmented market gives room for bolt-on acquisitions")]
    for j, (stat, desc) in enumerate(tw):
        yy = y2 + 0.55 + j * 0.70
        circle(s, x + 0.15, yy, 0.58, fill=NAVY if j != 1 else MIDBLUE, txt=stat, font_size=11 if len(stat) < 4 else 10)
        text(s, x + 0.88, yy + 0.02, w - 1.0, 0.56, desc, size=9.5, color=DARK, anchor="m")
    # right column: opportunities / disruption / threats
    rx, rw = 8.87, 4.00
    boxes = [
        ("Opportunities", NAVY, ["**Price increases above CPI** backed by product tiers",
                                 "**Premium concepts** lift revenue per subscriber",
                                 "**Bolt-on M&A** in Denmark & Finland"]),
        ("Disruption", MIDBLUE, ["**Digital-only offerings** – countered with an app included in all tiers",
                                 "**Data-driven pricing** to reduce churn"]),
        ("Threats", LBLUE, ["**Low-cost competitors** could cap pricing power",
                            "**Weaker consumer spending** if interest rates stay high"]),
    ]
    yy = y1
    heights = [1.95, 1.60, 1.60]
    for (title, col, items), hgt in zip(boxes, heights):
        hb = rect(s, rx, yy, rw, 0.34, fill=col)
        shape_text(hb, title, size=12, color=WHITE, bold=True)
        panel(s, rx, yy + 0.38, rw, hgt - 0.45)
        text(s, rx + 0.12, yy + 0.47, rw - 0.24, hgt - 0.6, [(t, {"bullet": True, "space_after": 5}) for t in items],
             size=9.5)
        yy += hgt + 0.08
    notes(s, "TEMPLATE: All market data on this slide is illustrative. Replace with sourced data (cite every source in "
             "the footnote). Keep the heading 'Market overview'.\n\n"
             "TALKING POINTS: (1) Market size and growth. (2) The company has taken share every year. (3) Fragmented "
             "market = consolidation optionality. (4) Opportunities outweigh threats; name the one threat that matters most.")
    return s
