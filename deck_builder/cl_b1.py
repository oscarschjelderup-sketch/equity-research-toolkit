"""Framework library – part 1: SWOT, Porter's five forces, positioning matrix, value chain, market sizing."""
from cl_core import *
from deck_data import HC, FC

FOOT_F = ("Frameworks are built from ordinary PowerPoint shapes and text boxes – click and type to edit. "
          "Content is illustrative for the fictional Example Company ASA.")
DGREEN, DRED = "407061", "A04040"


def _bullets(s, x, y, w, h, items, size=9.5, gap=4):
    text(s, x, y, w, h, [(t, {"bullet": True, "space_after": gap}) for t in items], size=size)


# ------------------------------------------------------------------ SWOT
def swot(prs, d):
    s = std(prs, "Framework library #1", "SWOT analysis",
            "Strengths and opportunities outweigh the weaknesses – the main threat is pricing pressure from low-cost players", FOOT_F)
    quads = [("Strengths", "S", NAVY, ["**#1 market position** in the Nordics with ~15% share", "**Pricing power:** price/mix +4-5% p.a. since 2022",
                                       "**Recurring revenue** (~90%) and negative working capital", "**ROIC of 19%** – more than twice the cost of capital"]),
             ("Weaknesses", "W", MIDBLUE, ["**High fixed cost base:** leases and personnel ~30% of sales", "**Dependent on Norway** (50% of revenue)",
                                           "Limited brand awareness in Finland"]),
             ("Opportunities", "O", DGREEN, ["**Bolt-on M&A** in a fragmented market", "**Premium tiers** and add-on sales lift revenue per customer",
                                             "**Digital onboarding** lowers customer acquisition cost", "Cash flow above target leverage funds buybacks on top of the dividend"]),
             ("Threats", "T", DRED, ["**Low-cost competitors** expanding in the big cities", "**Weaker consumer spending** if rates stay high",
                                     "Wage inflation above price increases"])]
    gx, gy, gw, gh = [1.05, 7.10], [1.45, 4.20], 5.77, 2.60
    for i, (title, letter, col, items) in enumerate(quads):
        x, y = gx[i % 2], gy[i // 2]
        hb = rect(s, x, y, gw, 0.42, fill=col)
        shape_text(hb, title, size=13, bold=True, align="l", margin=0.15)
        panel(s, x, y + 0.42, gw, gh - 0.42)
        text(s, x + gw - 0.85, y + 0.55, 0.7, 0.9, letter, size=44, bold=True, color="D5DADF", align="r", font="Cambria")
        _bullets(s, x + 0.15, y + 0.60, gw - 1.0, gh - 0.7, items, size=11.5, gap=9)
    for j, lab in enumerate(["Internal", "External"]):
        tb = text(s, 0.10, gy[j] + gh / 2 - 0.15, 1.3, 0.3, lab, size=11, bold=True, color=MUTED, align="c")
        tb.rotation = 270
        tb.left = Inches(0.05)
    notes(s, "Keep four bullets or fewer per box and start each with the point in bold. Finish with a 'so what' in the slide subtitle.")
    return s


# ------------------------------------------------------------------ Porter
def porter(prs, d):
    s = std(prs, "Framework library #2", "Porter's five forces",
            "Attractive industry structure: fragmented buyers and suppliers, moderate rivalry – watch the low-cost entrants", FOOT_F)
    lvl = {"Low": DGREEN, "Medium": AMBER, "High": DRED}
    bw, bh = 3.7, 1.55
    cx, cy = (SLIDE_W - bw) / 2, 3.32
    forces = [("Threat of new entrants", "Medium", cx, 1.42, ["Low-cost chains entering the big cities", "Prime locations and scale are barriers"]),
              ("Bargaining power of suppliers", "Low", 0.47, cy, ["Many landlords and equipment suppliers", "Long leases give cost visibility"]),
              ("Bargaining power of buyers", "Low", SLIDE_W - 0.47 - bw, cy, ["~780k individual subscribers – no concentration",
                                                                               "Low switching costs, but high habit value"]),
              ("Threat of substitutes", "Medium", cx, 5.22, ["Digital and at-home alternatives", "Bundled as an add-on in the company's own app"])]
    for title, rating, x, y, items in forces:
        hb = rect(s, x, y, bw, 0.36, fill=NAVY)
        shape_text(hb, title, size=10.5, bold=True, align="l", margin=0.1)
        chip(s, x + bw - 0.95, y + 0.07, 0.85, rating, lvl[rating], size=8)
        panel(s, x, y + 0.36, bw, bh - 0.36)
        _bullets(s, x + 0.1, y + 0.46, bw - 0.2, bh - 0.5, items, size=9.5, gap=4)
    hb = rect(s, cx, cy, bw, 0.36, fill=MIDBLUE)
    shape_text(hb, "Competitive rivalry", size=10.5, bold=True, align="l", margin=0.1)
    chip(s, cx + bw - 0.95, cy + 0.07, 0.85, "Medium", lvl["Medium"], size=8)
    rect(s, cx, cy + 0.36, bw, bh - 0.36, fill="DCEBF2")
    _bullets(s, cx + 0.1, cy + 0.46, bw - 0.2, bh - 0.5, ["Top-4 players hold ~42% of the market", "Competition on location and concept, less on price"],
             size=9.5, gap=4)
    mid_x, mid_y = SLIDE_W / 2, cy + bh / 2
    line(s, mid_x, 1.42 + bh + 0.04, mid_x, cy - 0.04, color=NAVY, width=1.75, arrow_end=True)
    line(s, mid_x, 5.22 - 0.04, mid_x, cy + bh + 0.04, color=NAVY, width=1.75, arrow_end=True)
    line(s, 0.47 + bw + 0.04, mid_y, cx - 0.04, mid_y, color=NAVY, width=1.75, arrow_end=True)
    line(s, SLIDE_W - 0.47 - bw - 0.04, mid_y, cx + bw + 0.04, mid_y, color=NAVY, width=1.75, arrow_end=True)
    # verdict
    rect(s, 0.47, 5.22, 3.7, 1.55, fill=NAVY)
    text(s, 0.62, 5.30, 3.4, 1.4, [("Industry attractiveness", {"size": 9.5, "color": "C9D1D9"}),
                                   ("Above average", {"size": 18, "bold": True, "color": WHITE, "space_after": 4}),
                                   ("Supports EBIT margins of 17-19% and pricing with CPI.", {"size": 9.5, "color": WHITE})])
    swatches(s, SLIDE_W - 0.47 - bw, 5.55, [("Low pressure", DGREEN), ("Medium pressure", AMBER), ("High pressure", DRED)],
             vertical=True, size=9, dy=0.32)
    notes(s, "Rate each force Low / Medium / High by changing the chip text and colour. The verdict box should tie back to "
             "your margin assumptions.")
    return s


# ------------------------------------------------------------------ positioning matrix
def positioning(prs, d):
    s = std(prs, "Framework library #3", "Competitive positioning matrix",
            "Example Company owns the premium, full-service corner – low-cost players compete for a different customer", FOOT_F)
    x0, y0, w, h = 1.35, 1.55, 6.6, 4.75
    panel(s, x0, y0, w, h, fill="F4F6F8")
    line(s, x0 + w / 2, y0, x0 + w / 2, y0 + h, color="C8CDD3", width=1, dash=MSO_LINE_DASH_STYLE.DASH)
    line(s, x0, y0 + h / 2, x0 + w, y0 + h / 2, color="C8CDD3", width=1, dash=MSO_LINE_DASH_STYLE.DASH)
    line(s, x0, y0 + h, x0 + w + 0.15, y0 + h, color=DARK, width=1.5, arrow_end=True)
    line(s, x0, y0 + h, x0, y0 - 0.15, color=DARK, width=1.5, arrow_end=True)
    text(s, x0, y0 + h + 0.08, w, 0.3, "Price level  →", size=10.5, bold=True, align="c")
    tb = text(s, x0 - 1.25, y0 + h / 2 - 0.15, 2.0, 0.3, "Service offering / quality  →", size=10.5, bold=True, align="c")
    tb.rotation = 270
    for (qx, qy, lab) in [(0.03, 0.03, "Value for money"), (0.53, 0.03, "Premium full-service"), (0.03, 0.90, "Low-cost / no frills"),
                          (0.53, 0.90, "Overpriced")]:
        text(s, x0 + qx * w, y0 + qy * h, 2.8, 0.3, lab, size=9.5, italic=True, color=MUTED)
    players = [("Example Company", 0.78, 0.80, 1.10, NAVY), ("Competitor A", 0.62, 0.62, 0.85, MIDBLUE), ("Competitor B", 0.30, 0.55, 0.75, LBLUE),
               ("Competitor C", 0.18, 0.22, 0.62, LBLUE), ("Boutique studios", 0.88, 0.45, 0.50, SOFT), ("Digital apps", 0.10, 0.40, 0.45, SOFT)]
    for name, px_, py_, sz, col in players:
        cxp, cyp = x0 + px_ * w, y0 + (1 - py_) * h
        circle(s, cxp - sz / 2, cyp - sz / 2, sz, fill=col, line_col=WHITE)
        text(s, cxp - 1.0, cyp + sz / 2 + 0.01, 2.0, 0.24, name, size=9, bold=name.startswith("Example"), align="c",
             color=NAVY if name.startswith("Example") else DARK)
    text(s, x0, y0 + h + 0.40, w, 0.22, "Bubble size = market share (illustrative)", size=8, italic=True, color=MUTED, align="c")
    rx, rw = 8.55, 4.32
    panel_header(s, rx, 1.45, rw, "What the matrix tells us", None, size=11)
    panel(s, rx, 1.87, rw, 2.55)
    _bullets(s, rx + 0.12, 1.98, rw - 0.24, 2.4, ["**Clear differentiation:** the only scaled player in the premium full-service corner",
                                                  "**Low-cost overlap is limited** – different customer, different locations",
                                                  "**Pricing headroom:** premium of ~25% to Competitor A is backed by service breadth",
                                                  "**White space:** mid-priced concept in smaller cities"], size=10, gap=6)
    panel_header(s, rx, 4.62, rw, "How to build it", None, size=11)
    _bullets(s, rx, 5.06, rw, 1.6, ["Pick two axes customers actually choose on", "Place peers first, then your company – be honest",
                                    "Use bubble size for a third dimension (share, revenue)", "Name the quadrants"], size=9.5, gap=3)
    notes(s, "Bubbles are ovals – drag to reposition and resize while holding Shift. Replace the axes with what matters in "
             "your industry (price vs. quality, growth vs. margin, scale vs. specialisation).")
    return s


# ------------------------------------------------------------------ value chain / business model
def value_chain(prs, d):
    s = std(prs, "Framework library #4", "Business model and value chain",
            "Where the company makes its money: a subscription engine with add-on sales and scale benefits in every step", FOOT_F)
    steps = [("Locations", "Prime sites on long leases", ["217 locations", "Cluster strategy in cities"]),
             ("Concept & product", "Tiered memberships", ["3 price tiers", "Own premium concepts"]),
             ("Customer acquisition", "Digital-first sales", ["70% join online", "Falling acquisition cost"]),
             ("Service delivery", "Staff and app", ["3,730 FTEs", "App included in all tiers"]),
             ("Retention & upsell", "Add-ons and loyalty", ["~90% recurring revenue", "Add-ons 8% of sales"])]
    n, x0, y0 = len(steps), 0.47, 1.50
    cw = (12.40 + 0.35 * (n - 1)) / n
    for i, (title, sub, items) in enumerate(steps):
        x = x0 + i * (cw - 0.35)
        shp = rect(s, x, y0, cw, 0.85, fill=NAVY if i % 2 == 0 else MIDBLUE, shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON)
        shape_text(shp, [title], size=10.5, bold=True, margin=0.05)
        bx = x + (0.0 if i == 0 else 0.30)
        text(s, bx + 0.05, y0 + 0.95, cw - 0.55, 0.26, sub, size=9.5, bold=True, color=NAVY)
        _bullets(s, bx + 0.05, y0 + 1.22, cw - 0.55, 0.7, items, size=9, gap=2)
    # revenue model
    y1 = 3.75
    panel_header(s, 0.47, y1, 6.0, "Revenue model (2025, % of revenue)", None, size=11)
    rm = [("Subscriptions", 0.90, NAVY, "Monthly fees, three tiers, 12-month average tenure 4.2 years"),
          ("Add-on services", 0.08, MIDBLUE, "Personal services, products and corporate agreements"),
          ("Other", 0.02, LBLUE, "Franchise fees and sub-letting")]
    for j, (lab, shr, col, desc) in enumerate(rm):
        yy = y1 + 0.55 + j * 0.78
        rect(s, 0.47, yy, 1.15, 0.62, fill=col)
        text(s, 0.47, yy, 1.15, 0.62, f"{shr * 100:.0f}%", size=18, bold=True, color=WHITE, align="c", anchor="m")
        text(s, 1.75, yy + 0.02, 4.7, 0.6, [(lab, {"bold": True, "size": 10.5, "color": NAVY}), (desc, {"size": 9})], anchor="m")
    # unit economics
    panel_header(s, 6.87, y1, 6.0, "Unit economics per location (NOKm, 2025)", None, size=11)
    locs = d.row("Hist", "locations", ["K"])[0]
    rev = d.row("Model", "is_rev", ["K"])[0]
    ebitdaal = d.row("Model", "ebitdaal", ["K"])[0]
    capex = -d.row("Model", "capex", ["K"])[0]
    tiles = [(f"{rev / locs:.1f}", "Revenue"), (f"{ebitdaal / locs:.1f}", "EBITDAaL"), (f"{ebitdaal / rev * 100:.0f}%", "Margin"),
             (f"{capex / locs:.1f}", "Capex")]
    tw = (6.0 - 3 * 0.15) / 4
    for j, (big, lab) in enumerate(tiles):
        tx = 6.87 + j * (tw + 0.15)
        panel(s, tx, y1 + 0.55, tw, 1.05, fill="DCEBF2")
        text(s, tx, y1 + 0.60, tw, 0.6, big, size=22, bold=True, color=NAVY, align="c", anchor="m")
        text(s, tx, y1 + 1.20, tw, 0.3, lab, size=9.5, color=DARK, align="c")
    r1, r2, r3 = (d.c("Drivers", k) for k in ("ramp1", "ramp2", "ramp3"))
    capl = d.row("Drivers", "capex_loc", [FC[0]])[0]
    rpl = d.row("Model", "rev_loc", [FC[0]])[0]
    _bullets(s, 6.87, y1 + 1.80, 6.0, 1.1, [f"New locations ramp up: {r1:.0%} / {r2:.0%} / {r3:.0%} of mature volume in years 1-3",
                                            f"Capex of NOK {capl:.0f}m per new location vs. revenue of NOK {rpl:.0f}m per location "
                                            f"({d.years([FC[0]])[0]})",
                                            "Scale benefits: purchasing, marketing and the digital platform"], size=9.5, gap=3)
    notes(s, "Chevrons are standard shapes. Unit economics tiles are calculated from the model (revenue, EBITDAaL and capex "
             "divided by the number of locations).")
    return s


# ------------------------------------------------------------------ market sizing
def market_sizing(prs, d):
    s = std(prs, "Framework library #5", "Market sizing – TAM, SAM and SOM",
            "A bottom-up view of the opportunity: the serviceable market is NOK 37bn and the company holds 15% of it", FOOT_F)
    levels = [("TAM", "Total addressable market", "NOK 95bn", "All spending on the category in the Nordics, incl. adjacent services", NAVY, 6.2),
              ("SAM", "Serviceable available market", "NOK 37bn", "Subscription-based services in cities where the concept works", MIDBLUE, 4.6),
              ("SOM", "Serviceable obtainable market", "NOK 8bn", "Realistic share within 5 years: 20% of SAM (15% today)", LBLUE, 3.0)]
    cx, y = 0.47 + 3.1, 1.55
    for i, (abbr, name, val, desc, col, w) in enumerate(levels):
        shp = rect(s, cx - w / 2, y + i * 1.12, w, 0.98, fill=col, shape=MSO_SHAPE.FLOWCHART_MANUAL_OPERATION)
        shape_text(shp, [f"{abbr}  ·  {val}"], size=15, bold=True, margin=0.05)
    for i, (abbr, name, val, desc, col, w) in enumerate(levels):
        yy = y + i * 1.12
        text(s, 6.95, yy + 0.08, 5.9, 0.85, [(name, {"bold": True, "size": 11.5, "color": NAVY, "space_after": 2}), (desc, {"size": 10})], anchor="m")
        line(s, cx + w / 2 - 0.15, yy + 0.49, 6.85, yy + 0.49, color=GRIDGREY, width=0.75)
    # bottom-up table
    ty = 5.05
    panel_header(s, 0.47, ty, 12.40, "Bottom-up build of the serviceable market (illustrative)", None, size=11)
    rows = [dict(cells=["Country", "Adult population (m)", "Urban share", "Penetration", "Customers (m)", "Revenue per customer (NOK)",
                        "Market (NOKbn)"], fill=NAVY, color=WHITE, bold=True, size=8.5, h=0.26)]
    data = [("Norway", 4.4, 0.83, 0.22, 17000), ("Sweden", 8.3, 0.88, 0.21, 8600), ("Denmark", 4.7, 0.88, 0.19, 7400), ("Finland", 4.5, 0.86, 0.17, 6100)]
    tot_c, tot_m = 0, 0
    for c, pop, urb, pen, arpu in data:
        cust = pop * urb * pen
        mkt = cust * arpu / 1000
        tot_c, tot_m = tot_c + cust, tot_m + mkt
        rows.append(dict(cells=[c, f"{pop:.1f}", f"{urb:.0%}", f"{pen:.0%}", f"{cust:.2f}", f"{arpu:,.0f}", f"{mkt:.1f}"], size=8.5,
                         h=0.23, line_bottom="E1E5EA"))
    rows.append(dict(cells=["Nordics", "", "", "", f"{tot_c:.2f}", "", f"{tot_m:.1f}"], size=8.5, h=0.25, bold=True, fill="E4EEF2",
                     line_top=NAVY))
    table(s, 0.47, ty + 0.45, 12.40, rows, [2.0, 1.7, 1.4, 1.4, 1.6, 2.4, 1.9])
    notes(s, "The funnel uses trapezoid shapes. Always show how the numbers are built (population x penetration x spend) – "
             "judges will ask. The table multiplies through to the SAM figure.")
    return s
