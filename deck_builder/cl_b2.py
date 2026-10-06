"""Framework library – part 2: thesis pillars, timeline, risk matrix, scenario tree, value driver tree."""
from cl_core import *
from cl_b1 import FOOT_F, DGREEN, DRED, _bullets
from deck_data import HC, FC
from deck_slides3 import RISKS


# ------------------------------------------------------------------ thesis pillars
def thesis(prs, d):
    rating, tp, up = d.c("DCF", "rating"), d.c("DCF", "tp"), d.c("DCF", "tp_up")
    s = std(prs, "Framework library #6", "Investment thesis in three pillars",
            f"{rating} – target price NOK {tp:.0f} ({up:+.0%}): quality compounder, underestimated margins and a valuation gap", FOOT_F)
    rev = d.row("Model", "is_rev", ["K", "P"])
    e2, e3 = d.c("Consensus", "diff_ebit_2"), d.c("Consensus", "diff_ebit_3")
    y2, y3 = d.years(FC[1:3])
    m_imp = d.c("Reverse_DCF", "rd_m_last")
    price = d.c("Inputs", "price")
    up_d, up_p = d.c("DCF", "dcf_ps") / price - 1, d.c("Comps", "peer_val") / price - 1
    newl = sum(d.row("Model", "open", FC[:5]))
    pillars = [("Growth engine intact", f"{((rev[1] / rev[0]) ** 0.2 - 1) * 100:.1f}%", "revenue CAGR 2025–30E",
                [f"{newl:.0f} new locations over 2026–30E", "Like-for-like and price/mix on top", "Bolt-on M&A is pure upside"],
                "Proof point: outgrew the market every year since 2022"),
               ("Margins are underestimated", f"{d.row('Model', 'ebit_adj_m', ['P'])[0] * 100:.1f}%", "EBIT adj. margin 2030E",
                ["Fixed costs and rent grow with locations, not sales",
                 f"The price implies {m_imp * 100:.1f}% in {d.years([FC[-1]])[0]}" if isinstance(m_imp, (int, float)) else "See Reverse_DCF",
                 f"We are {e2:+.0%} / {e3:+.0%} vs. consensus EBIT {y2[:4]}-{y3[2:4]}E"], "Proof point: margin up 5pp 2021–25"),
               ("Valuation gap", f"{abs(d.v('Comps', 'M' + str(d.reg['comps']['prem']))) * 100:.0f}%", "EV/EBIT discount to peers",
                ["Higher margins and ROIC than peers", f"DCF NOK {d.c('DCF', 'dcf_ps'):.0f}, peers NOK {d.c('Comps', 'peer_val'):.0f}",
                 f"Dividend yield {d.row('Analysis', 'div_yield', [FC[2]])[0] * 100:.1f}% in {y3}"],
                f"Proof point: both methods point {min(up_d, up_p) * 100:.0f}-{max(up_d, up_p) * 100:.0f}% higher")]
    xs, w = [0.47, 4.67, 8.87], 4.0
    for i, (title, big, sub, items, proof) in enumerate(pillars):
        x = xs[i]
        rect(s, x, 1.45, w, 0.95, fill=NAVY)
        circle(s, x + 0.15, 1.63, 0.58, fill=WHITE, txt=str(i + 1), font_size=16, color=NAVY)
        text(s, x + 0.9, 1.45, w - 1.0, 0.95, title, size=13, bold=True, color=WHITE, anchor="m")
        panel(s, x, 2.40, w, 2.95)
        text(s, x + 0.15, 2.48, w - 0.3, 0.62, big, size=30, bold=True, color=NAVY, anchor="m")
        text(s, x + 0.15, 3.08, w - 0.3, 0.26, sub, size=10, color=MUTED)
        _bullets(s, x + 0.15, 3.45, w - 0.3, 1.4, items, size=11, gap=7)
        rect(s, x, 4.88, w, 0.47, fill="DCEBF2")
        text(s, x + 0.15, 4.88, w - 0.3, 0.47, proof, size=9, italic=True, color=NAVY, anchor="m")
    panel_header(s, 0.47, 5.55, 12.40, "Catalysts next 12 months", None, size=11)
    cats = [("Q3 report · Oct", "Price increases visible in revenue per customer"), ("Capital markets day · Nov", "New margin and ROIC targets"),
            ("Q4 report · Feb", "Dividend proposal and buyback mandate"), ("H1 2027", "Closing of bolt-on acquisitions")]
    cw = (12.40 - 3 * 0.15) / 4
    for j, (when, what) in enumerate(cats):
        cxp = 0.47 + j * (cw + 0.15)
        chip(s, cxp, 6.02, 1.75, when, MIDBLUE, size=8.5, h=0.26)
        text(s, cxp, 6.32, cw, 0.45, what, size=9.5)
    notes(s, "Three pillars, one number each. The numbers on this slide come from the model (CAGR, margin, discount, DCF).")
    return s


# ------------------------------------------------------------------ timeline
def timeline(prs, d):
    s = std(prs, "Framework library #7", "Timeline and catalyst calendar",
            "Where the company comes from – and the dated events that can close the valuation gap", FOOT_F)
    panel_header(s, 0.47, 1.40, 12.40, "Company history", None, size=11)
    ms = [("1998", "Founded in Oslo"), ("2006", "Entered Sweden"), ("2014", "Private equity owner; roll-out accelerates"),
          ("2019", "IPO on Oslo Børs"), ("2022", "Acquired Danish peer (NOK 800m)"), ("2024", "Bolt-on in Finland"),
          ("2026", "780k subscribers, 217 locations")]
    ly, x0, x1 = 2.95, 1.0, 11.95
    line(s, x0 - 0.3, ly, x1 + 0.3, ly, color=NAVY, width=2.5, arrow_end=True)
    n = len(ms)
    for i, (yr, txt) in enumerate(ms):
        cxp = x0 + (x1 - x0) * i / (n - 1)
        up = i % 2 == 0
        circle(s, cxp - 0.11, ly - 0.11, 0.22, fill=NAVY if i < n - 1 else DGREEN, line_col=WHITE)
        line(s, cxp, ly - (0.42 if up else -0.11), cxp, ly + (0.42 if not up else -0.11), color=GRIDGREY, width=0.75)
        ty = ly - 1.10 if up else ly + 0.45
        text(s, cxp - 0.85, ty, 1.7, 0.66, [(yr, {"bold": True, "size": 11, "color": NAVY, "align": "c"}), (txt, {"size": 8.5, "align": "c"})],
             anchor="b" if up else "t")
    # catalyst calendar (Gantt style)
    gy = 4.35
    panel_header(s, 0.47, gy, 12.40, "Catalyst calendar – next four quarters", None, size=11)
    qs = ["Q4 2026", "Q1 2027", "Q2 2027", "Q3 2027"]
    lx, lw = 0.47, 3.2
    qw = (12.40 - lw) / 4
    for j, qn_ in enumerate(qs):
        hb = rect(s, lx + lw + j * qw, gy + 0.47, qw - 0.04, 0.28, fill=NAVY)
        shape_text(hb, qn_, size=9, bold=True)
    rows = [("Quarterly reports", [(0.30, 0.18, "Q3"), (1.40, 0.18, "Q4"), (2.35, 0.18, "Q1"), (3.55, 0.18, "Q2")], MIDBLUE),
            ("Price increases take effect", [(0.95, 1.10, "+5% all markets")], DGREEN),
            ("Capital markets day", [(0.55, 0.22, "CMD")], NAVY),
            ("Dividend and buyback decision", [(1.35, 0.95, "Proposal → AGM")], LBLUE),
            ("Bolt-on M&A closing", [(2.10, 1.50, "Two targets in due diligence")], MIDBLUE)]
    for k, (lab, bars, col) in enumerate(rows):
        yy = gy + 0.85 + k * 0.36
        text(s, lx, yy, lw - 0.1, 0.3, lab, size=9.5, anchor="m")
        line(s, lx, yy + 0.33, lx + 12.40, yy + 0.33, color="E1E5EA", width=0.5)
        for start, length, txt in bars:
            b = rect(s, lx + lw + start * qw, yy + 0.04, max(length * qw, 0.5), 0.25, fill=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
            shape_text(b, txt, size=8, bold=True, color=WHITE if col != LBLUE else NAVY, margin=0.02)
    notes(s, "Timeline markers and Gantt bars are shapes – duplicate (Ctrl+D) and drag. Keep history to 6-8 milestones.")
    return s


# ------------------------------------------------------------------ risk matrix with mitigants
def risk_matrix(prs, d):
    s = std(prs, "Framework library #8", "Risk matrix with mitigating factors",
            "Show that you know what can go wrong – and why it does not break the case", FOOT_F)
    mx, my, cell = 1.25, 1.55, 1.45
    colors = {2: "7DBB7E", 3: "C7D66D", 4: "F2C94C", 5: "F0994A", 6: "D9534F"}
    for pi in range(3):
        for ii in range(3):
            rect(s, mx + ii * (cell + 0.05), my + pi * (cell + 0.05), cell, cell, fill=colors[(3 - pi) + (ii + 1)])
    for i, (title, desc, prob, imp) in enumerate(RISKS):
        same = [j for j, r in enumerate(RISKS) if (r[2], r[3]) == (prob, imp)]
        k = same.index(i)
        cxp = mx + (imp - 1) * (cell + 0.05) + cell / 2 - 0.21 + (k - (len(same) - 1) / 2) * 0.5
        cyp = my + (3 - prob) * (cell + 0.05) + cell / 2 - 0.21
        circle(s, cxp, cyp, 0.42, fill=NAVY, txt=str(i + 1), font_size=12, line_col=WHITE)
    gw = 3 * cell + 0.1
    for ii, lab in enumerate(["Low", "Medium", "High"]):
        text(s, mx + ii * (cell + 0.05), my + gw + 0.04, cell, 0.22, lab, size=9, color=MUTED, align="c")
        text(s, mx - 0.72, my + (2 - ii) * (cell + 0.05) + cell / 2 - 0.11, 0.65, 0.22, lab, size=9, color=MUTED, align="r")
    text(s, mx, my + gw + 0.30, gw, 0.3, "Impact →", size=11, bold=True, align="c")
    tb = text(s, mx - 1.75, my + gw / 2 - 0.15, 1.6, 0.3, "Probability →", size=11, bold=True, align="c")
    tb.rotation = 270
    mit = ["Premium concept and locations differ from low-cost; bear case assumes −1pp price/mix p.a.",
           "Subscriptions are sticky; 2020 shows the downside (−8.5% revenue) and the recovery",
           "Annual price increases and 30% variable staffing; +0.5pp cost ratio in the bear case",
           "24-month ramp-up assumed; digital sales already 70% of new customers",
           "NIBD/EBITDAaL 0.8x; bolt-ons only, funded from cash flow"]
    rx, rw = 6.35, 6.52
    rows = [dict(cells=["#", "Risk", "Prob.", "Impact", "Mitigating factors"], fill=NAVY, color=WHITE, bold=True, size=9, h=0.30,
                 align={0: "c", 2: "c", 3: "c", 4: "l"})]
    lv = {1: "Low", 2: "Med.", 3: "High"}
    lc = {1: DGREEN, 2: "9A7B0A", 3: DRED}
    for i, (title, desc, prob, imp) in enumerate(RISKS):
        rows.append(dict(cells=[str(i + 1), title, lv[prob], lv[imp], mit[i]], size=9, h=0.80, line_bottom="E1E5EA",
                         align={0: "c", 1: "l", 2: "c", 3: "c", 4: "l"}, bolds={0: True, 1: True, 2: True, 3: True},
                         colors={0: NAVY, 1: NAVY, 2: lc[prob], 3: lc[imp]}))
    table(s, rx, 1.55, rw, rows, [0.35, 1.55, 0.6, 0.65, 3.35])
    bear = d.v("Sensitivity", f"{[c for c, k, _, _ in d.reg['t4'] if k == 'dcf_ps'][0]}{d.reg['sens']['t4_rows'][0]}")
    rect(s, rx, 5.95, rw, 0.62, fill=NAVY)
    text(s, rx + 0.15, 5.95, rw - 0.3, 0.62,
         f"Bottom line: with all major risks in play, our bear case DCF is NOK {bear:.0f} ({bear / d.c('Inputs', 'price') - 1:+.0%}) – "
         f"against {d.c('DCF', 'tp_up'):+.0%} to the target price.", size=10, color=WHITE, anchor="m")
    notes(s, "Risks are shared with the pitch deck appendix. Link every high-impact risk to a number in the bear case.")
    return s


# ------------------------------------------------------------------ scenario tree
def scenario_tree(prs, d):
    s = std(prs, "Framework library #9", "Scenario tree and expected value",
            "Three scenarios, explicit probabilities – the probability-weighted value is still above today's share price", FOOT_F)
    t4 = {k: c for c, k, _, _ in d.reg["t4"]}
    r0 = d.reg["sens"]["t4_rows"][0]
    sv = lambda k, j: d.v("Sensitivity", f"{t4[k]}{r0 + j}")
    probs = [d.c("Drivers", f"adj_prob_{k}") for k in ("bear", "base", "bull")]
    price, pw = d.c("Inputs", "price"), d.c("Sensitivity", "pw_dcf_ps")
    x_root, x_sc, x_val, x_ev = 0.47, 4.05, 7.75, 10.75
    ys = [1.75, 3.45, 5.15]
    bh = 1.25
    root = rect(s, x_root, ys[1], 2.2, bh, fill=NAVY)
    text(s, x_root + 0.1, ys[1], 2.0, bh, [("Share price today", {"size": 10, "color": "C9D1D9", "align": "c"}),
                                          (f"NOK {price:.0f}", {"size": 22, "bold": True, "color": WHITE, "align": "c"})], anchor="m")
    names = [(n.capitalize(), col, d.c("Thesis", f"sc_{n}_story")) for n, col in (("bear", DRED), ("base", NAVY), ("bull", DGREEN))]
    for j, (nm, col, story) in enumerate(names):
        y = ys[j]
        elbow(s, x_root + 2.2, ys[1] + bh / 2, x_sc, y + bh / 2, color=MUTED, width=1.25)
        chip(s, (x_root + 2.2 + x_sc) / 2 + 0.07, y + bh / 2 - 0.29, 0.55, f"{probs[j]:.0%}", col, size=9, h=0.24)
        hb = rect(s, x_sc, y, 3.2, 0.36, fill=col)
        shape_text(hb, f"{nm} case", size=11, bold=True, align="l", margin=0.1)
        panel(s, x_sc, y + 0.36, 3.2, bh - 0.36)
        text(s, x_sc + 0.1, y + 0.40, 3.0, bh - 0.44, [(story, {"size": 8.5, "space_after": 2}),
                                                       (f"Revenue CAGR {sv('cagr', j):.1%} · EBIT margin {sv('ebit_m', j):.1%}",
                                                        {"size": 9, "color": MUTED})], anchor="m")
        line(s, x_sc + 3.2, y + bh / 2, x_val, y + bh / 2, color=MUTED, width=1.25, arrow_end=True)
        v = sv("dcf_ps", j)
        rect(s, x_val, y, 2.3, bh, fill="DCEBF2")
        text(s, x_val + 0.1, y, 2.1, bh, [("DCF value per share", {"size": 9, "color": MUTED, "align": "c"}),
                                          (f"NOK {v:.0f}", {"size": 20, "bold": True, "color": col, "align": "c"}),
                                          (f"{v / price - 1:+.0%} vs. today", {"size": 9.5, "align": "c"})], anchor="m")
        elbow(s, x_val + 2.3, y + bh / 2, x_ev, ys[1] + bh / 2, color=MUTED, width=1.25)
    ev = rect(s, x_ev, ys[1] - 0.2, 2.12, bh + 0.4, fill=NAVY)
    text(s, x_ev + 0.08, ys[1] - 0.2, 1.96, bh + 0.4, [("Probability-weighted value", {"size": 9.5, "color": "C9D1D9", "align": "c"}),
                                                      (f"NOK {pw:.0f}", {"size": 24, "bold": True, "color": WHITE, "align": "c"}),
                                                      (f"{pw / price - 1:+.0%} vs. today", {"size": 10, "color": WHITE, "align": "c"})], anchor="m")
    text(s, x_ev - 0.3, ys[2] + 0.35, 2.6, 0.7, " + ".join(f"{p:.0%} × {sv('dcf_ps', j):.0f}" for j, p in enumerate(probs)), size=9,
         italic=True, color=MUTED, align="c")
    notes(s, "All numbers come from the scenario data table in the model (Sensitivity sheet), the probabilities on Drivers and "
             "the stories on the Thesis sheet.")
    return s


# ------------------------------------------------------------------ value driver tree
def driver_tree(prs, d):
    s = std(prs, "Framework library #10", "Value driver tree (ROIC decomposition)",
            "What has to be true for the returns to hold? Break ROIC into margin and capital turnover, then into operating drivers",
            FOOT_F + " Figures: 2025A → 2028E from the DCF toolkit.")
    ca, cb_ = "K", "N"
    M = lambda k, c: d.row("Model", k, [c])[0]
    A = lambda k, c: d.row("Analysis", k, [c])[0]
    ratio = lambda k, c: -M(k, c) / M("is_rev", c)
    p = lambda v: f"{v * 100:.1f}%"
    x_ = lambda v: f"{v:.2f}x"

    def node(x, y, title, v0, v1, fill=PANEL, w=2.75, h=0.70, strong=False):
        rect(s, x, y, w, h, fill=NAVY if strong else fill)
        col = WHITE if strong else DARK
        text(s, x + 0.1, y + 0.03, w - 0.2, 0.3, title, size=9.5, bold=True, color=WHITE if strong else NAVY)
        text(s, x + 0.1, y + 0.32, w - 0.2, 0.34, f"{v0}  →  **{v1}**", size=11, color=col)
        return x, y, w, h

    xs = [0.47, 3.75, 7.00, 10.12]
    roic = node(xs[0], 3.55, "ROIC", p(M("roic", ca)), p(M("roic", cb_)), strong=True, h=0.78)
    nm = node(xs[1], 2.25, "NOPAT margin", p(A("nopat_m", ca)), p(A("nopat_m", cb_)), fill="DCEBF2")
    ct = node(xs[1], 5.05, "Capital turnover", x_(A("ic_turn", ca)), x_(A("ic_turn", cb_)), fill="DCEBF2")
    em = node(xs[2], 1.75, "EBIT adj. margin", p(M("ebit_adj_m", ca)), p(M("ebit_adj_m", cb_)))
    tx = node(xs[2], 2.75, "Tax rate", p(A("tax_eff", ca)), p(A("tax_eff", cb_)))
    nwc = node(xs[2], 4.55, "NWC / revenue", p(A("nwc_s", ca)), p(A("nwc_s", cb_)))
    fa = node(xs[2], 5.55, "Fixed capital / revenue", p((M("ppe", ca) + M("gw", ca)) / M("is_rev", ca)),
              p((M("ppe", cb_) + M("gw", cb_)) / M("is_rev", cb_)))
    leaves = [("Gross margin", p(M("gm", ca)), p(M("gm", cb_))), ("Personnel / revenue", p(ratio("pers", ca)), p(ratio("pers", cb_))),
              ("Other opex / revenue", p(ratio("oth", ca)), p(ratio("oth", cb_))),
              ("Leases + D&A / revenue", p(ratio("lease", ca) + ratio("da", ca)), p(ratio("lease", cb_) + ratio("da", cb_)))]
    lys = [1.45, 2.22, 2.99, 3.76]
    for (t, v0, v1), ly in zip(leaves, lys):
        lf = node(xs[3], ly, t, v0, v1, fill="F4F6F8", h=0.66)
        elbow(s, em[0] + em[2], em[1] + em[3] / 2, lf[0], ly + 0.33)
    capx = node(xs[3], 4.85, "Capex / revenue", p(A("capex_s", ca)), p(A("capex_s", cb_)), fill="F4F6F8", h=0.66)
    capd = node(xs[3], 5.62, "Capex / D&A", x_(A("capex_da", ca)), x_(A("capex_da", cb_)), fill="F4F6F8", h=0.66)
    for lf in (capx, capd):
        elbow(s, fa[0] + fa[2], fa[1] + fa[3] / 2, lf[0], lf[1] + 0.33)
    for parent, kids in ((roic, (nm, ct)), (nm, (em, tx)), (ct, (nwc, fa))):
        for k in kids:
            elbow(s, parent[0] + parent[2], parent[1] + parent[3] / 2, k[0], k[1] + k[3] / 2)
    circle(s, xs[1] + 1.15, 3.72, 0.44, fill=WHITE, txt="×", font_size=16, color=NAVY, line_col=NAVY)
    wacc = d.c("WACC", "wacc")
    rect(s, 0.47, 5.75, 2.75, 0.95, fill="DCEBF2")
    text(s, 0.57, 5.78, 2.55, 0.9, [(f"WACC {wacc * 100:.1f}%", {"bold": True, "size": 11, "color": NAVY}),
                                    (f"Spread to ROIC: {(M('roic', cb_) - wacc) * 100:.0f}pp in {d.years([cb_])[0]} – growth creates value.",
                                     {"size": 9})], anchor="m")
    text(s, 0.47, 1.45, 2.9, 0.5, [("How to read", {"bold": True, "size": 10, "color": NAVY}),
                                   (f"{d.years([ca])[0]} → {d.years([cb_])[0]} for each driver", {"size": 9, "color": MUTED})])
    notes(s, "Every box reads the model (Model and Analysis sheets). Connectors are straight lines; move boxes and lines together.")
    return s
