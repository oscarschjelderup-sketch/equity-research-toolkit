"""The eleven sections of the report (plus contents, disclosures and the checks appendix), each a function returning HTML.

Numbers come from `rb_data.Report`; narrative comes from the case text module's `report` dict. A section whose data the
case has not collected renders a visible gap (`placeholder`) – the template never fills a hole with an invented figure.
"""
from __future__ import annotations

import datetime as dt
import statistics

from rb_charts import bars, heat_table, hbars, line, pie, price_fan, range_bars, waterfall
from rb_core import (NA, box, cols, esc, est_header, exhibit, h2, h3, isnum, kv, md, mult, nok, num, p, pct, placeholder, pp,
                     section, table, ul)
from rb_data import fmt_date

SEG = ("a", "b", "c")


def _yrs(r, a, b):
    return [y for y in r.years if a <= y <= b]


def _hdr(r, years, first=""):
    return [esc(first)] + [est_header(r.ylabel(y), r.is_est(y)) for y in years]


def _fmt(kind):
    return {"n": lambda v: num(v), "n1": lambda v: num(v, 1), "n2": lambda v: num(v, 2), "p": lambda v: pct(v), "x": lambda v: mult(v),
            "p0": lambda v: pct(v, 0), "s": lambda v: esc(v) if v not in (None, "") else "–"}[kind]


def _rows(r, spec, years, sheet="Model"):
    """spec = [(label, key, kind, bold?)] -> table rows."""
    out, bold, rules = [], [], []
    for i, (lab, key, kind, *flags) in enumerate(spec):
        if key is None:
            out.append([f"<i>{esc(lab)}</i>"] + [""] * len(years))
            rules.append(i)
            continue
        vals = r.row(key, years, sheet)
        f = _fmt(kind)
        out.append([esc(lab)] + [f(v) for v in vals])
        if "b" in flags:
            bold.append(i)
    return out, bold, rules


def _tag(text, cls):
    return f"<span class='tag {cls}'>{esc(text)}</span>"


def _rating_cls(rating):
    return {"BUY": "buy", "SELL": "sell"}.get(str(rating).upper(), "hold")


def _date_str(d):
    return fmt_date(d) if d else "n.a."


def _src_model(r):
    return f"Company reports (history), case model (estimates, {r.ticker} workbook)"


def _src_date(r):
    return fmt_date(r.price_date)


def _seg_names(r):
    return [r.c("Inputs", f"seg_{s}", s.upper()) for s in SEG]


def _price_series(r):
    px = r.prices()
    if not px:
        return None
    dates = [dt.date.fromisoformat(d) for d in px["dates"]]
    close = px["close"]
    idx = px.get("index_close")
    keep = [i for i, v in enumerate(close) if v is not None]
    dates = [dates[i] for i in keep]
    close = [close[i] for i in keep]
    if idx:
        idx = [idx[i] for i in keep]
        base = next((v for v in idx if v), None)
        if base:
            idx = [close[0] * v / base if v else None for v in idx]
    return px, dates, close, idx


# ====================================================================== 1. front page
def front_page(r, prev):
    H = r.head()
    rep = r.rep
    nxt = r.next_event()
    hist = r.history()
    meta = r.meta()
    disc = meta.get("disclosures", {}) or {}
    rating = r.rating
    prev_rating = hist[-1][1] if hist else None
    prev_tp = hist[-1][2] if hist else None
    # ---- left column
    brand = ("<div class='brand'><div><div class='t1'>EQUITY RESEARCH TOOLKIT · RESEARCH REPORT</div>"
             f"<div class='t2'>{esc(r.c('Inputs', 'sector', ''))} · {esc(r.c('Inputs', 'exchange', ''))}: {esc(r.ticker)} · "
             f"{esc(rep.get('kind', 'Update'))}</div></div>"
             f"<div class='t2' style='text-align:right'>Published {esc(fmt_date(r.today))}<br>Prices as of {esc(_date_str(r.price_date))} close</div></div>")
    title = rep.get("title") or r.ct("cover_title", f"{r.company} – research report")
    abstract = rep.get("abstract") or (
        f"We rate {r.company} {rating} with a 12-month target price of {nok(H['tp'])} ({pct(H['tp_up'], 0, sign=True)} upside, "
        f"{pct(H['tp_tr'], 0)} expected total return). The target is {pct(H['w_dcf'], 0)} DCF ({nok(H['dcf_ps'])}) and "
        f"{pct(H['w_peers'], 0)} peer multiples ({nok(H['peer_val'])}), rolled forward twelve months.")
    memo = rep.get("memo")
    memo_html = "".join(f"<p><b class='h'>{md(h)}.</b> {md(t)}</p>" for h, t in memo) if memo else placeholder(
        "Front-page memo not written", "add `report['memo']` = [(heading, paragraph), ...] to the case text module – the quarter or event, "
        "the status against the company's own targets, what changed in the estimates, and the valuation argument.")
    left = (f"<div class='main'>{brand}<div class='co'>{esc(r.company)}</div><div class='title'>{esc(title)}</div>"
            f"<div class='abstract'>{md(abstract)}</div><div class='memo'>{memo_html}</div></div>")
    # ---- rail
    rec = (f"<div class='rec'><div class='r1'>{esc(rating)}</div><div class='r2'>TP {nok(H['tp'])} · {pct(H['tp_up'], 0, sign=True)}</div>"
           f"<div class='r3'>Share price {nok(H['price'], 2)} ({_date_str(r.price_date)}). Expected total return {pct(H['tp_tr'], 0)} "
           f"incl. dividend {nok(H['tp_div'], 2)}. Cost of equity {pct(H['ke'])}.</div></div>")
    chart = ""
    ps = _price_series(r)
    if ps:
        px, dates, close, idx = ps
        series = [("Share price", close)]
        chart = exhibit(f"{r.ticker} vs {px.get('index', 'index')} (rebased), 12 months",
                        line(dates, series + ([("OSEBX (rebased)", idx)] if idx else []), size=(3.1, 1.6), labels_last=False),
                        px.get("source", "Yahoo Finance"), px.get("dates", ["n.a."])[-1])
    else:
        chart = placeholder("Price chart not drawn", "no prices.json in the output folder – build with --refresh-prices")
    summ = kv([("Recommendation (previous)", f"{esc(rating)} ({esc(prev_rating) if prev_rating else 'first report'})"),
               ("Share price", nok(H["price"], 2)),
               ("Target price (previous)", f"{nok(H['tp'])} ({nok(prev_tp) if prev_tp else 'first report'})"),
               ("Upside / expected total return", f"{pct(H['tp_up'], 0)} / {pct(H['tp_tr'], 0)}"),
               ("Consensus target (Yahoo, mean)", nok(H["cons_tp"], 1) if isnum(H["cons_tp"]) else NA),
               ("Next event", f"{esc(nxt[1])} – {fmt_date(nxt[0])}" if nxt else "<span class='na'>not collected</span>")])
    y0 = r.last_act
    lev = r.val("lev", y0, "Analysis")
    cap = kv([("Shares outstanding / diluted (m)", f"{num(H['shares'], 1)} / {num(H['shares_dil'], 1)}"),
              ("Market capitalisation (NOKm)", num(H["mcap"])),
              (f"Net interest-bearing debt ({_date_str(r.bs_date)}, NOKm)", num(H["nibd"])),
              ("Lease liabilities (NOKm)", num(H["leases"])),
              ("Enterprise value excl. / incl. leases (NOKm)", f"{num(H['ev'])} / {num(H['ev_incl'])}"),
              (f"NIBD / EBITDA after leases ({r.ylabel(y0)})", mult(lev, 2)),
              ("52-week high / low", f"{num(H['high52'], 2)} / {num(H['low52'], 2)}"),
              ("Free float", esc(r.market().get("free_float", NA)))])
    # ---- estimate changes
    if prev:
        ys = [y for y in r.years if r.is_est(y)][:3]
        pyrs = prev.get("years", [])
        rows = []
        for lab, key, kind in (("Revenue (NOKm)", "rev", "n"), ("EBITDA after leases (NOKm)", "ebitdaal", "n"), ("EPS (NOK)", "eps", "n2")):
            new = r.row(key, ys)
            old = [prev["rows"][key][pyrs.index(y)] if y in pyrs else None for y in ys]
            f = _fmt(kind)
            rows.append([esc(lab + " – old")] + [f(v) for v in old])
            rows.append([esc(lab + " – new")] + [f(v) for v in new])
            rows.append([esc("Change")] + [pct(n / o - 1, 1, sign=True) if (isnum(n) and isnum(o) and o) else "–" for n, o in zip(new, old)])
        est = exhibit(f"Estimate changes since {fmt_date(prev['date'])}", table(_hdr(r, ys), rows, bold_rows=(2, 5, 8)), "Case model",
                      fmt_date(r.today))
    else:
        est = box("Estimate changes", "<div class='small'>First report – there are no previous estimates to compare with. "
                  "Each build stores its estimates; the next report shows old vs new.</div>", "grey")
    # ---- financial table 2021-2028
    ys = _yrs(r, 2021, 2028)
    spec = [("Revenue (NOKm)", "rev", "n"), ("EBITDA reported (NOKm)", "ebitda", "n"), ("EBITDA after leases (NOKm)", "ebitdaal", "n"),
            ("EBIT adj. (NOKm)", "ebit_adj", "n"), ("Net profit (NOKm)", "np", "n"), ("EPS (NOK)", "eps", "n2"), ("DPS (NOK)", "dps", "n2"),
            ("Revenue growth", "g_rev", "p"), ("EBITDA after leases margin", "ebitdaal_m", "p"), ("EBIT adj. margin", "ebit_adj_m", "p"),
            ("ROIC", "roic", "p"), ("EV / Sales (x)", "evs", "x"), ("EV / EBITDA after leases (x)", "evebitda", "x"), ("EV / EBIT adj. (x)", "evebit", "x"),
            ("P / E (x)", "pe", "x"), ("Dividend yield", "div_yield", "p"), ("FCF yield", "fcf_yield", "p")]
    rows, bold, rules = _rows(r, spec, ys, "Analysis")
    fin = exhibit(f"Key figures {ys[0]}–{ys[-1]}E (multiples at the current share price, pre-IFRS 16 basis)", table(_hdr(r, ys), rows),
                  _src_model(r), _src_date(r), cls="fin")
    author = disc.get("author", "Case author")
    discl = (f"<div class='disc'><b>A student case study and a process document – not investment research and not investment advice.</b> "
             f"Author: {esc(author)}. Prices: {esc(disc.get('price_datetime', _date_str(r.price_date)))}. Rating scale: "
             f"{esc(disc.get('rating_definitions', 'see disclosures'))}. Estimates are marked EST; every exhibit names its source and date. "
             f"See the disclosures on the last pages.</div>")
    rail = f"<div class='rail'>{rec}{chart}<h4>Summary</h4>{summ}<h4>Capital structure</h4>{cap}<h4>Estimate changes</h4>{est}</div>"
    body = f"<div class='front'>{left}{rail}</div><div class='fin'>{fin}</div>{discl}"
    return (f"<span class='runhead hidden'>Equity Research Toolkit | {esc(r.company)} ({esc(r.ticker)})</span>"
            f"<span class='rundate hidden'>{esc(fmt_date(r.today))}</span>"
            f"<section id='front' class='sec first'>{body}</section>")


def contents(titles):
    rows = "".join(f"<tr><td>{i}</td><td>{esc(t)}</td></tr>" for i, t in titles)
    return f"<div class='box grey' style='margin-top:0'><div class='bt'>Contents</div><table class='toc'>{rows}</table></div>"


# ====================================================================== 2. investment case
def investment_case(r):
    H = r.head()
    sc = r.scenarios()
    rep = r.rep
    parts = []
    # fan chart
    ps = _price_series(r)
    horizon = r.price_date + dt.timedelta(days=365) if r.price_date else r.today + dt.timedelta(days=365)
    if ps:
        px, dates, close, idx = ps
        sp = lambda v: f"{v * 100:+.0f}%"  # noqa: E731
        pts = [(f"Bull {nok(sc['bull']['tp'])} ({sp(sc['bull']['tp'] / H['price'] - 1)})", sc["bull"]["tp"], "#2E7D32"),
               (f"Target {nok(H['tp'])} ({sp(H['tp_up'])})", H["tp"], "#003255"),
               (f"Bear {nok(sc['bear']['tp'])} ({sp(sc['bear']['tp'] / H['price'] - 1)})", sc["bear"]["tp"], "#C00000")]
        fan = exhibit("Share price, target price and the bear and bull values twelve months out",
                      price_fan(dates, close, idx, horizon_date=horizon, points=pts, size=(3.6, 2.3)),
                      f"{px.get('source', 'Yahoo Finance')} (prices); case model (target and scenario values)", px["dates"][-1])
    else:
        fan = placeholder("Price chart with the target fan not drawn", "no prices.json – build with --refresh-prices")
    meth = box("Target price methodology", ul([
        f"Fair value today = {pct(H['w_dcf'], 0)} DCF ({nok(H['dcf_ps'], 1)}) + {pct(H['w_peers'], 0)} peer multiples ({nok(H['peer_val'], 1)}) = {nok(H['fair'], 1)}.",
        f"Rolled forward twelve months at the cost of equity ({pct(H['ke'])}) less the dividend ({nok(H['tp_div'], 2)}), rounded: target {nok(H['tp'])}.",
        f"Bull {nok(sc['bull']['tp'])} / bear {nok(sc['bear']['tp'])} are the same calculation on the bull and bear forecasts (probabilities "
        f"{pct(sc['bull']['prob'], 0)} / {pct(sc['bear']['prob'], 0)}); probability-weighted value {nok(H['pw_dcf'], 1)}.",
        f"WACC {pct(H['wacc'])}, terminal growth {pct(H['tg'])}, terminal value {pct(H['tv_share'], 0)} of EV.",
    ], "tight"), "grey")
    parts.append(cols(fan, meth, widths=["64%", "36%"]))
    # three boxes
    var = r.variant()
    differ = ul([f"**{v['topic']}:** {v['ours']} *(consensus: {v['cons']})* – {v['num']}" for v in var], "tight") if var else placeholder(
        "Variant perception not filled", "VARIANT in the data module")
    down = rep.get("risks_down") or [t for t, *_ in (r.ct("risks") or [])][:4]
    up = rep.get("risks_up") or []
    parts.append(cols(box("Downside risks to our case", ul(down, "tight") if down else placeholder("not written")),
                      box("Our case – and how we differ from consensus", differ, "grey"),
                      box("Upside risks to our case", ul(up, "tight") if up else placeholder("not written", "report['risks_up']"))))
    # thesis
    thesis = rep.get("thesis")
    if thesis:
        parts.append(h2("The investment case in four points") + ul(thesis))
    since = rep.get("since_last")
    if since:
        srows = [[md(a), md(b), md(c), _tag(d, {"confirmed": "ok", "on track": "ok", "weaker": "watch", "watch": "watch", "broken": "broken"}.get(str(d).lower(), "na"))]
                 for a, b, c, d in since]
        parts.append(exhibit("Since the last edition – what we said, what the company reported, where it leaves the thesis",
                             table(["Topic", "What we said", "What was reported since", "Verdict"], srows, cls="num wrap", widths=["14%", "34%", "40%", "12%"], left=(1, 2)),
                             rep.get("since_last_source", "Previous edition; company reports"), _src_date(r)))
    ev = r.events()
    if ev:
        sig = [sc["base"]["signpost"], sc["bear"]["signpost"], sc["bull"]["signpost"]]
        erows = [[esc(fmt_date(d)), esc(lab), md(sig[i % 3] if i < 3 else "–"), esc(src)] for i, (d, lab, src) in enumerate(ev[:6])]
        parts.append(exhibit("Signposts calendar – the next events and what each one has to show", table(["Date", "Event", "What to watch (scenario signposts)", "Source"], erows,
                                                                                                           cls="num wrap", widths=["12%", "22%", "44%", "22%"], left=(1, 2, 3)),
                             "Company financial calendar (data module EVENTS); Thesis sheet signposts", _src_date(r)))
    if var:
        vrows = [[md(v["topic"]), md(v["ours"]), md(v["cons"]), md(v["why"]), md(v["when"]), esc(v["num"])] for v in var]
        parts.append(exhibit("Where we differ from consensus – the evidence, and when we find out",
                             table(["Topic", "Our view", "Consensus / the market", "Why we differ – the evidence", "What proves it, and when", "In numbers"], vrows,
                                   cls="num wrap", widths=["10%", "20%", "18%", "24%", "16%", "12%"], left=range(6)), "Case model (Consensus sheet); consensus as stated there", _src_date(r)))
    # scenario table
    rows = []
    for s, lab in (("bear", "Bear"), ("base", "Base"), ("bull", "Bull")):
        x = sc[s]
        rows.append([f"<b>{lab}</b>", pct(x["prob"], 0), nok(x["value"], 1), pct(x["up"], 0, sign=True), nok(x["tp"]), _tag(x["rating"], _rating_cls(x["rating"])),
                     md(x["story"]), md(x["trigger"]), md(x["signpost"])])
    hdr = ["Scenario", "Probability", "DCF value", "vs price", "12m value", "Rating", "Story", "What has to happen", "Signpost"]
    parts.append(exhibit("Scenarios – value, story, trigger and signpost", table([esc(h) for h in hdr], rows, cls="num wrap",
                         widths=["6%", "6%", "7%", "6%", "6%", "5%", "24%", "20%", "20%"], left=(6, 7, 8)), "Case model (Thesis sheet)", _src_date(r)))
    adj = r.scenario_adj()
    if adj:
        arows = []
        for key, lab, bear, base, bull, comment in adj:
            f = (lambda v: f"{v:+.0f}") if key in ("open",) else ((lambda v: f"{v:+.1f}x") if key == "exit" else (
                (lambda v: pct(v, 0)) if key == "prob" else (lambda v: pp(v, 2) if abs(v) < 0.05 else pp(v, 1))))
            arows.append([esc(lab), f(bear), f(base), f(bull), md(comment)])
        parts.append(exhibit("Scenario assumptions (changes to the base-case drivers)",
                             table(["Driver", "Bear", "Base", "Bull", "What it stands for"], arows, cls="num wrap", widths=["30%", "8%", "8%", "8%", "46%"], left=(4,)),
                             "Case data module (SCENARIO_ADJ)", _src_date(r)))
    # scenario paths by year (Sensitivity table 4)
    try:
        ws = r.d.wb["Sensitivity"]
        sr0, sr1 = r.d.reg["sens"]["t4_rows"]
        t4 = {k: c for c, k, _, _ in r.d.reg["t4"]}
        fy = [y for y in r.years if r.is_est(y)]
        srows = []
        for rr, lab in zip(range(sr0, sr1 + 1), ("Bear", "Base", "Bull")):
            rv = [ws[f"{t4[f'rev{i}']}{rr}"].value for i in range(1, 9)]
            eb = [ws[f"{t4[f'ebit{i}']}{rr}"].value for i in range(1, 9)]
            srows.append([f"<b>{lab}</b> – revenue"] + [num(v) for v in rv])
            srows.append([f"{lab} – EBIT adj."] + [num(v) for v in eb])
            srows.append([f"{lab} – EBIT adj. margin"] + [pct(e / v) if (isnum(e) and isnum(v) and v) else "–" for e, v in zip(eb, rv)])
        parts.append(exhibit("Scenario paths – revenue and EBIT adj. by year (NOKm)", table(_hdr(r, fy, "NOKm"), srows, bold_rows=(0, 3, 6)),
                             "Case model (Sensitivity table 4)", _src_date(r)))
    except (KeyError, TypeError):
        pass
    # kill criteria
    kills = r.kills()
    if kills:
        krows = []
        for k in kills:
            f = (lambda v: pct(v)) if k["fmt"] == "pct" else (lambda v: mult(v, 2))
            st = str(k["status"] or "")
            cls = "ok" if "TRACK" in st.upper() or st.upper() == "OK" else ("broken" if "BREACH" in st.upper() or "KILL" in st.upper() else "watch")
            krows.append([esc(k["kpi"]), esc(k["dir"]), f(k["th"]), f(k["latest"]), esc(k["per"]), f(k["base"]), _tag(st, cls),
                          esc(k["basechk"])])
        parts.append(exhibit("Kill criteria – what would make us wrong, checked against the latest actuals",
                             table(["KPI", "Kill if", "Threshold", "Latest actual", "Period", "Base case next year", "Status", "Base case check"], krows, cls="num kill", left=(1, 6, 7)),
                             "Case model (Thesis sheet); latest actuals from the company's reports", _src_date(r)))
    return section("case", "Investment case overview", rep.get("case_lead"), "".join(parts), 1)


# ====================================================================== 3. company overview
def company_overview(r):
    rep = r.rep
    parts = []
    desc = rep.get("description") or [r.ct("ov_recurring", ""), r.ct("ov_pricing", ""), r.ct("ov_leverage", "")]
    desc = [d for d in desc if d]
    names = _seg_names(r)
    y0 = r.last_act
    segrev = [r.val(f"rev_{s}", y0, "Hist") for s in SEG]
    pies = exhibit(f"Revenue by segment, {r.ylabel(y0)}", pie(names, segrev), "Company reports (segment note)", f"FY {y0}")
    cat = rep.get("revenue_by_category")
    if cat:
        pies2 = exhibit(f"Revenue by category, {cat.get('year', r.ylabel(y0))}", pie([c[0] for c in cat["rows"]], [c[1] for c in cat["rows"]]),
                        cat["source"], cat["date"])
    else:
        pies2 = placeholder("Revenue by category not collected", "report['revenue_by_category'] = dict(rows=[(label, value)], source, date, year)")
    parts.append(cols(box("Company description", ul(desc) if desc else placeholder("not written")), pies, pies2, widths=["40%", "30%", "30%"]))
    # targets, management, owners
    targets = rep.get("targets")
    tg = ul([f"**{t[0]}:** {t[1]} *({t[2]})*" for t in targets], "tight") if targets else placeholder("Financial targets not collected",
                                                                                                           "report['targets'] = [(label, value, source)]")
    mg = rep.get("management") or r.ct("mgmt") or []
    mgmt = ul([f"**{m[1]}** – {m[2]}" for m in mg], "tight") if mg else placeholder("Management not listed", "report['management'] or mgmt in the case text module")
    own = rep.get("owners")
    if own:
        owners = table(["Shareholder", "Stake"], [[esc(n), pct(v) if isnum(v) else esc(v)] for n, v in own["rows"]]) + \
            f"<div class='legend'>Source: {md(own['source'])}, {esc(own['date'])}.</div>"
    else:
        owners = placeholder("Largest shareholders not collected", "report['owners'] = dict(rows=[(name, stake)], source, date)")
    parts.append(cols(box("Financial targets (company)", tg), box("Key management", mgmt), box("Largest shareholders", owners)))
    # KPI history
    ys = _yrs(r, r.years[0], y0)
    spec = []
    for s, n in zip(SEG, names):
        spec += [(f"{n} – revenue (NOKm)", f"rev_{s}", "n"), (f"{n} – {r.c('Inputs', 'vol_unit', 'volume')}", f"vol_{s}", "n"),
                 (f"{n} – locations", f"loc_{s}", "n"), (f"{n} – revenue per unit (NOK/month)", f"rpu_{s}", "n")]
    rows, bold, rules = _rows(r, spec, ys, "Hist")
    parts.append(exhibit("Operating history by segment", table(_hdr(r, ys), rows), "Company reports (country pages and segment note)", f"FY {y0}"))
    hy = [str(y) for y in ys]
    c1 = exhibit("Revenue by segment (NOKm)", bars(hy, [(n, r.row(f"rev_{s_}", ys, "Hist")) for s_, n in zip(SEG, names)], stacked=True, size=(3.4, 1.9)),
                 "Company reports (segment note)", f"FY {y0}")
    c2 = exhibit("Margins before IFRS 16", line(hy, [("EBITDA after leases margin", r.row("ebitdaal_m", ys, "Hist")), ("EBIT adj. margin", r.row("ebit_adj_m", ys, "Hist"))],
                                              unit="%", markers=True, size=(3.4, 1.9)), "Company reports; case model definitions", f"FY {y0}")
    parts.append(cols(c1, c2))
    swot = rep.get("swot")
    if swot:
        parts.append(h2("SWOT") + cols(box("Strengths", ul(swot.get("strengths", []), "tight")), box("Weaknesses", ul(swot.get("weaknesses", []), "tight")))
                     + cols(box("Opportunities", ul(swot.get("opportunities", []), "tight")), box("Threats", ul(swot.get("threats", []), "tight"))))
    else:
        parts.append(placeholder("SWOT not written", "report['swot'] = dict(strengths=[...], weaknesses=[...], opportunities=[...], threats=[...])"))
    return section("company", "Company overview", rep.get("company_lead"), "".join(parts), 2)


# ====================================================================== 4. quarter preview
def _q_sorted(q):
    def key(lbl):
        a, b = lbl.split()
        return (int(b), int(a[1]))
    return sorted(q["rows"].keys(), key=key)


def quarter_preview(r):
    q = r.quarters()
    rep = r.rep
    nxt = r.next_event()
    lead = rep.get("quarter_lead")
    if not q:
        return section("quarter", "Quarter preview", lead, placeholder("Quarterly data not collected",
                       "add `QUARTERS` to the data module: revenue, EBITDA, EBITDA after leases, EBIT adj., net profit, EPS and the segment "
                       "lines per quarter, with the source and date of each report. The preview, the seasonality split and the quarterly table in "
                       "the financial statements all read it."), 3, cont=True)
    labels = _q_sorted(q)
    last = labels[-1]
    yq, yy = last.split()
    nq = int(yq[1]) % 4 + 1
    ny = int(yy) + (1 if nq == 1 else 0)
    nxt_label = f"Q{nq} {ny}"
    parts = []
    # seasonality: share of each quarter in the full year, averaged over the full years available
    full_years = sorted({int(l_.split()[1]) for l_ in labels if all(f"Q{i} {l_.split()[1]}" in q["rows"] for i in (1, 2, 3, 4))})
    lines = [("Revenue", "rev", "n"), ("EBITDA reported", "ebitda", "n"), ("EBITDA after leases", "ebitdaal", "n"), ("EBIT adj.", "ebit_adj", "n"),
             ("Net profit", "np", "n"), ("EPS (NOK)", "eps", "n2")]
    ya = f"Q{nq} {ny - 1}"
    cons = (r.consensus().get("quarter") or {})
    rows = []
    est_note = ""
    if len(full_years) >= 1 and ny in r.col:
        yrs_used = full_years[-2:]
        est_note = (f"Our quarter EST = the full-year forecast for {ny}E × the average share of Q{nq} in the full year over {', '.join(map(str, yrs_used))} "
                    f"(a seasonality split of the annual model, not a separate quarterly forecast).")
        for lab, key, kind in lines:
            fy = r.val(key, ny)
            shares = []
            for y in yrs_used:
                tot = sum((q["rows"][f"Q{i} {y}"].get(key) or 0) for i in (1, 2, 3, 4))
                qv = q["rows"][f"Q{nq} {y}"].get(key)
                if tot and qv is not None and key != "eps":
                    shares.append(qv / tot)
            est = fy * statistics.mean(shares) if (shares and isnum(fy)) else None
            if key == "eps" and est is None:
                np_est = None
                for rr in rows:
                    if rr[0] == "Net profit":
                        np_est = rr[-1]
                est = None
            c = cons.get(key) if cons else None
            f = _fmt(kind)
            yago = (q["rows"].get(ya) or {}).get(key)
            d_cons = pct(est / c - 1, 0, sign=True) if (isnum(est) and isnum(c) and c) else "–"
            d_yoy = pct(est / yago - 1, 0, sign=True) if (isnum(est) and isnum(yago) and yago) else "–"
            rows.append([esc(lab), f(yago), f(est) if est is not None else "–", d_yoy, f(c) if isnum(c) else f"<span class='na'>{NA}</span>", d_cons, f(fy), est])
        rows = [rw[:-1] for rw in rows]
        hdr = [esc("NOKm"), esc(ya), est_header(f"{nxt_label} ours", True), esc("y/y"), esc("Consensus"), esc("vs cons."), est_header(f"FY {ny}", True)]
        src = f"Company reports ({q['source']}); case model; consensus: {cons.get('source', NA) if cons else NA}"
        parts.append(h2(f"{nxt_label} preview" + (f" – reported {fmt_date(nxt[0])}" if nxt else "")))
        if lead:
            parts.append(p(lead))
        parts.append(exhibit(f"{nxt_label} – our estimate against last year and consensus", table(hdr, rows), src, q["date"], note=est_note))
    else:
        parts.append(placeholder("Seasonality split not possible", "the preview needs at least one full year of quarters in QUARTERS"))
    show = labels[-8:]
    try:
        qx = [l_.replace(" 20", " ") for l_ in show]
        c1 = exhibit("Revenue and EBITDA after leases by quarter (NOKm)",
                     bars(qx, [("Revenue", [q["rows"][l_].get("rev") for l_ in show]), ("EBITDA after leases", [q["rows"][l_].get("ebitdaal") for l_ in show])], size=(3.4, 1.9)),
                     f"Company reports ({q['source']})", q["date"])
        c2 = exhibit("Margins by quarter (before IFRS 16)",
                     line(qx, [("EBITDA after leases margin", [(q["rows"][l_].get("ebitdaal") or 0) / q["rows"][l_]["rev"] if q["rows"][l_].get("rev") else None for l_ in show]),
                               ("EBIT adj. margin", [(q["rows"][l_].get("ebit_adj") or 0) / q["rows"][l_]["rev"] if (q["rows"][l_].get("rev") and q["rows"][l_].get("ebit_adj") is not None) else None for l_ in show])],
                          unit="%", markers=True, size=(3.4, 1.9)), f"Company reports ({q['source']})", q["date"])
        parts.append(cols(c1, c2))
    except (KeyError, ZeroDivisionError, TypeError):
        pass
    # last eight quarters
    hdr = [esc("NOKm")] + [esc(l_) for l_ in show]
    rows = []
    for lab, key, kind in lines:
        f = _fmt(kind)
        rows.append([esc(lab)] + [f((q["rows"][l_]).get(key)) for l_ in show])
    for lab, key in (("EBITDA after leases margin", None), ):
        rows.append([esc(lab)] + [pct((q["rows"][l_].get("ebitdaal") or 0) / q["rows"][l_]["rev"]) if q["rows"][l_].get("rev") else "–" for l_ in show])
    kp = [("Members ('000)", "members", "n"), ("Clubs", "clubs", "n"), ("ARPM (NOK/month)", "arpm", "n")]
    for lab, key, kind in kp:
        f = _fmt(kind)
        if any(q["rows"][l_].get(key) is not None for l_ in show):
            rows.append([esc(lab)] + [f(q["rows"][l_].get(key)) for l_ in show])
    parts.append(exhibit("The last quarters", table(hdr, rows), f"Company reports ({q['source']})", q["date"]))
    # segments
    segs = sorted({s for l_ in show for s in (q["rows"][l_].get("seg") or {})})
    if segs:
        rows = []
        for s in segs:
            rows.append([f"<b>{esc(s)}</b> – revenue"] + [num((q["rows"][l_].get("seg", {}).get(s) or {}).get("rev")) for l_ in show])
            rows.append([esc(f"{s} – country EBITDA before IFRS 16")] + [num((q["rows"][l_].get("seg", {}).get(s) or {}).get("cebitda")) for l_ in show])
            rows.append([esc(f"{s} – margin")] + [pct(((q["rows"][l_].get("seg", {}).get(s) or {}).get("cebitda") or 0) /
                                                       (q["rows"][l_].get("seg", {}).get(s) or {}).get("rev"))
                                                  if (q["rows"][l_].get("seg", {}).get(s) or {}).get("rev") else "–" for l_ in show])
        parts.append(exhibit("Segments by quarter", table(hdr, rows), f"Company reports ({q['source']}, segment note and country pages)", q["date"]))
    return section("quarter", "Quarter preview", None, "".join(parts), 3)


# ====================================================================== 5. deep dives
def _exhibit_from_spec(ex):
    kind = ex.get("kind", "bar")
    unit = ex.get("unit")
    if kind == "table":
        body = table([esc(h) for h in ex["headers"]], [[md(str(c)) if isinstance(c, str) else num(c, ex.get("dec", 0)) for c in row] for row in ex["rows"]],
                     cls="num wrap" if ex.get("wrap") else "num", left=ex.get("left", ()))
    elif kind == "bar":
        body = bars(ex["x"], ex["series"], unit=unit, stacked=ex.get("stacked", False), size=ex.get("size", (5.2, 2.2)), hline=ex.get("hline"))
    elif kind == "hbar":
        body = hbars(ex["labels"], ex["values"], unit=unit, highlight=ex.get("highlight"), size=ex.get("size", (5.2, 2.4)))
    elif kind == "line":
        body = line(ex["x"], ex["series"], unit=unit, avg=ex.get("avg"), markers=True, size=ex.get("size", (5.2, 2.2)))
    elif kind == "waterfall":
        body = waterfall(ex["labels"], ex["values"], unit=unit, totals=tuple(ex.get("totals", (0,))), size=ex.get("size", (5.2, 2.3)))
    else:
        raise ValueError(f"unknown exhibit kind {kind}")
    return exhibit(ex["title"], body, ex["source"], ex["date"], note=ex.get("note"))


def deep_dives(r):
    dd = r.rep.get("deep_dives") or []
    if not dd:
        return section("deep", "Deep dives", None, placeholder("Deep dives not written",
                       "report['deep_dives'] = [dict(title, question, text=[...], exhibits=[...], into_model=[(driver, value, model row)])] – two to "
                       "four themes that decide the case, each with data we collected ourselves and each ending in a number that enters the model."), 4, cont=True)
    parts = []
    for i, d in enumerate(dd):
        parts.append(h2(f"{i + 1}. {d['title']}"))
        if d.get("question"):
            parts.append(p(f"*{d['question']}*", "lead"))
        for t in d.get("text", []):
            parts.append(p(t))
        exs = [_exhibit_from_spec(e) for e in d.get("exhibits", [])]
        for j in range(0, len(exs), 2):
            pair = exs[j:j + 2]
            parts.append(cols(*pair) if len(pair) == 2 else pair[0])
        im = d.get("into_model")
        if im:
            parts.append(box("Into the model", table(["Driver", "Value used", "Where in the model"], [[md(a), md(b), esc(c)] for a, b, c in im],
                                                     cls="num wrap", left=(1, 2)), "grey"))
        if i < len(dd) - 1:
            parts.append("<div style='height:6px'></div>")
    return section("deep", "Deep dives – the themes that decide the case", r.rep.get("deep_lead"), "".join(parts), 4)


# ====================================================================== 6. competition
def competition(r):
    comp = r.rep.get("competition")
    if not comp:
        return section("competition", "Competition per market", None, placeholder("Competition tables not collected",
                       "report['competition'] = {market: dict(rows=[(operator, segment, units, price, binding, source, date)], takeaway, "
                       "prices=[(operator, monthly price)], price_note)}"), 5, cont=True)
    parts = []
    for market, m in comp.items():
        parts.append(h2(market))
        if m.get("intro"):
            parts.append(p(m["intro"]))
        rows = [[md(a), esc(b), esc(c), esc(d), esc(e), esc(f), esc(g)] for a, b, c, d, e, f, g in m["rows"]]
        tbl = exhibit(f"{market} – operators, units, prices and binding", table(["Operator", "Segment", "Units", "Price (monthly)", "Binding", "Source", "Observed"],
                                                                                  rows, cls="num wrap", widths=["17%", "13%", "8%", "17%", "11%", "22%", "12%"], left=range(7)),
                      m.get("source", "Operators' websites; see the Source column"), m.get("date", "see the Observed column"))
        if m.get("prices"):
            ch = exhibit(f"{market} – comparable monthly price", hbars([a for a, _ in m["prices"]], [b for _, b in m["prices"]], unit="nok",
                                                                        highlight=m.get("highlight", r.ticker), size=(3.4, 2.2)),
                         m.get("price_source", "Operators' websites"), m.get("date", "n.a."), note=m.get("price_note"))
            parts.append(cols(tbl, ch, widths=["62%", "38%"]))
        else:
            parts.append(tbl)
        if m.get("takeaway"):
            parts.append(box("What it means for the case", p(m["takeaway"]), "grey"))
    return section("competition", "Competition per market", r.rep.get("competition_lead"), "".join(parts), 5)


# ====================================================================== 7. macro
def macro(r):
    mc = r.rep.get("macro")
    if not mc:
        return section("macro", "Macro – the drivers that reach the P&L", None, placeholder("Macro block not collected",
                       "report['macro'] = dict(columns=[...], rows=[(indicator, v1, v2, source, date)], bullets=[...], exhibits=[...])"), 6, cont=True)
    parts = []
    hdr = ["Indicator"] + list(mc.get("columns", [])) + ["Source", "Date"]
    rows = [[md(x[0])] + [esc(v) for v in x[1:-2]] + [esc(x[-2]), esc(x[-1])] for x in mc["rows"]]
    tbl = exhibit("Macro drivers and where they enter the model", table([esc(h) for h in hdr], rows, cls="num wrap", left=range(len(hdr))), "See the Source column", "see the Date column")
    bl = box("How the macro reaches the P&L", ul(mc.get("bullets", []), "tight"), "grey") if mc.get("bullets") else ""
    parts.append(cols(tbl, bl, widths=["60%", "40%"]) if bl else tbl)
    exs = [_exhibit_from_spec(e) for e in mc.get("exhibits", [])]
    for j in range(0, len(exs), 2):
        pair = exs[j:j + 2]
        parts.append(cols(*pair) if len(pair) == 2 else pair[0])
    return section("macro", "Macro – the drivers that reach the P&L", r.rep.get("macro_lead"), "".join(parts), 6)


# ====================================================================== 8. estimate revisions
def revisions(r, prev):
    if not prev:
        body = box("First report", p("There are no stored previous estimates for this company. This build has written its estimates to the output "
                                      "folder; the next report will show old versus new line by line and explain the changes."), "grey")
        return section("revisions", "Estimate revisions", None, body, 7, cont=True)
    ys = [y for y in r.years if r.is_est(y)][:3]
    pyrs = prev.get("years", [])
    names = _seg_names(r)
    spec = [("Revenue", "rev", "n"), (f"– {names[0]}", "rev_a", "n"), (f"– {names[1]}", "rev_b", "n"), (f"– {names[2]}", "rev_c", "n"),
            ("EBITDA reported", "ebitda", "n"), ("EBITDA after leases", "ebitdaal", "n"), ("EBIT adj.", "ebit_adj", "n"), ("Net profit", "np", "n"),
            ("EPS (NOK)", "eps", "n2"), ("DPS (NOK)", "dps", "n2"), ("FCFF", "fcff", "n")]
    rows = []
    for lab, key, kind in spec:
        new = r.row(key, ys)
        old = [prev["rows"].get(key, [None] * len(pyrs))[pyrs.index(y)] if y in pyrs else None for y in ys]
        f = _fmt(kind)
        chg = [pct(n / o - 1, 1, sign=True) if (isnum(n) and isnum(o) and o) else "–" for n, o in zip(new, old)]
        rows.append([esc(lab)] + [f(v) for v in new] + [f(v) for v in old] + chg)
    hdr = [esc("NOKm")] + [est_header(f"{y}E new", True) for y in ys] + [est_header(f"{y}E old", True) for y in ys] + [esc(f"Δ {y}") for y in ys]
    parts = [exhibit(f"New estimates ({fmt_date(r.today)}) against the previous report ({fmt_date(prev['date'])})", table(hdr, rows), "Case model", fmt_date(r.today))]
    head = kv([("Share price then / now", f"{nok(prev.get('price'), 2)} / {nok(r.price, 2)}"), ("DCF value then / now", f"{nok(prev.get('dcf_ps'), 1)} / {nok(r.c('DCF', 'dcf_ps'), 1)}"),
               ("Target then / now", f"{nok(prev.get('tp'))} / {nok(r.tp)}"), ("Rating then / now", f"{esc(prev.get('rating'))} / {esc(r.rating)}")])
    notes = r.rep.get("revision_notes")
    why = box("Why the estimates changed", ul(notes) if notes else placeholder("not written", "report['revision_notes']"), "grey")
    parts.append(cols(box("Valuation then and now", head), why))
    return section("revisions", "Estimate revisions", None, "".join(parts), 7)


# ====================================================================== 9. valuation
def _implied_grid(r, H):
    tp = H["tp"]
    prices = [round(tp * f) for f in (0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5)]
    bridge = H["ev"] - H["mcap"]
    sh = H["shares_dil"]
    y0, y1, y2 = r.last_act, r.first_fc, r.first_fc + 1
    rows = []
    for lab, key, years, per_share in (("EV / Sales", "rev", (y0, y1, y2), False), ("EV / EBITDA after leases", "ebitdaal", (y0, y1, y2), False),
                                       ("EV / EBIT adj.", "ebit_adj", (y0, y1, y2), False), ("P / E", "eps", (y0, y1, y2), True)):
        for y in years:
            m = r.val(key, y)
            if not isnum(m) or m == 0:
                continue
            cells = []
            for px in prices:
                v = (px / m) if per_share else ((px * sh + bridge) / m)
                cells.append(mult(v))
            rows.append([f"{esc(lab)} {r.ylabel(y)}"] + cells)
    hdr = [esc("Share price (NOK)")] + [esc(str(px)) for px in prices]
    return exhibit("Implied multiples at different share prices (EV = price × diluted shares + net debt and other claims, pre-IFRS 16)",
                   table(hdr, rows), "Case model", _src_date(r))


def _peer_group_ranges(r, H):
    """Implied value per share by peer group and multiple (min / median / max of the group's NTM multiples)."""
    peers = r.peers()
    groups = r.peer_groups()
    y1 = r.first_fc + 1  # NTM ~ second forecast year column is FY1 consensus for peers; the Comps sheet uses peer_year
    yr = r.first_fc + int(r.c("Inputs", "peer_year", 2)) - 1
    rev, ebitdaal, ebit, eps = (r.val(k, yr) for k in ("rev", "ebitdaal", "ebit_adj", "eps"))
    bridge = H["ev"] - H["mcap"]
    sh = H["shares_dil"]
    rows, trows = [], []
    for g, members in groups.items():
        sel = [pz for pz in peers if pz[0] in members]
        if not sel:
            continue
        for lab, idx, metric, per_share in (("EV/EBITDA", 5, ebitdaal, False), ("EV/EBIT", 6, ebit, False), ("P/E", 7, eps, True)):
            vals = [pz[idx][1] for pz in sel if isnum(pz[idx][1])]
            if len(vals) < 2 or not isnum(metric):
                rows.append((f"{g} – {lab} {r.ylabel(yr)}", None, None, None))
                continue
            lo, mdn, hi = min(vals), statistics.median(vals), max(vals)
            conv = (lambda m: m * metric) if per_share else (lambda m: (m * metric - bridge) / sh)
            rows.append((f"{g} – {lab} {r.ylabel(yr)}", conv(lo), conv(mdn), conv(hi)))
            trows.append([esc(g), esc(lab), str(len(vals)), mult(lo), mult(mdn), mult(hi), nok(conv(lo)), nok(conv(mdn)), nok(conv(hi))])
    sc = r.scenarios()
    rows.append(("DCF – bear to bull", sc["bear"]["value"], sc["base"]["value"], sc["bull"]["value"]))
    waccs, gs, grid = r.sens1()
    inner = [grid[i][j] for i in (1, 2, 3) for j in (2, 3, 4) if isnum(grid[i][j])]
    if inner:
        rows.append(("DCF – WACC ±0.5pp / g ±0.25pp", min(inner), H["dcf_ps"], max(inner)))
    rows.append(("52-week trading range", H["low52"], None, H["high52"]))
    return rows, trows, yr


def valuation(r):
    H = r.head()
    rev_ = r.reverse()
    parts = []
    # summary
    fv = kv([("DCF value per share", nok(H["dcf_ps"], 1)), ("Peer multiples value per share (median)", nok(H["peer_val"], 1)),
             (f"Blended fair value today ({pct(H['w_dcf'], 0)} / {pct(H['w_peers'], 0)})", nok(H["fair"], 1)),
             ("Rolled forward 12m at Ke less dividend", f"× (1 + {pct(H['ke'])}) − {nok(H['tp_div'], 2)}"), ("12-month target price", f"<b>{nok(H['tp'])}</b>"),
             ("Upside / expected total return", f"{pct(H['tp_up'], 0)} / {pct(H['tp_tr'], 0)}"), ("Rating", _tag(r.rating, _rating_cls(r.rating)))])
    rows, trows, yr = _peer_group_ranges(r, H)
    chart = exhibit("Valuation summary – value per share by method (range and median; lines = price and target)",
                    range_bars(rows, H["price"], H["tp"], size=(4.6, 2.9)), "Case model (DCF, sensitivity, scenarios); peer multiples from the data module (Yahoo Finance)",
                    _src_date(r))
    parts.append(cols(box("From value to target", fv), chart, widths=["36%", "64%"]))
    # reverse DCF
    rd_rows = [["Final-year EBIT adj. margin", pct(rev_["m_last"]), pct(rev_["m_last_ours"]), pp(rev_["m_last_ours"] - rev_["m_last"]) if isnum(rev_["m_last"]) else "–", pct(rev_["m_ref"])],
               ["Revenue CAGR to the final year", pct(rev_["cagr"]), pct(rev_["cagr_ours"]), pp(rev_["cagr_ours"] - rev_["cagr"]) if isnum(rev_["cagr"]) else "–", pct(rev_["cagr_ref"])],
               ["WACC", pct(rev_["wacc"]), pct(rev_["wacc_ours"]), pp(rev_["wacc"] - rev_["wacc_ours"]) if isnum(rev_["wacc"]) else "–", "–"],
               ["Terminal growth", pct(rev_["g"]), pct(rev_["g_ours"]), pp(rev_["g"] - rev_["g_ours"]) if isnum(rev_["g"]) else "–", "–"]]
    ok, problems, gd = r.case_gate()
    gate_txt = ("Case gate passed: " if ok else "Case gate FAILED: ") + (
        f"the view differs from the market by {abs(gd['m_ours'] - gd['m_implied']) * 100:.1f}pp on the final-year margin and "
        f"{abs(gd['g_ours'] - gd['g_implied']) * 100:.1f}pp on growth; the DCF is {gd['dcf'] / gd['price'] - 1:+.0%} from the price (rules: ≥ 1pp and ≥ 10 %)."
        if ok else "; ".join(problems))
    rd = exhibit(f"What the share price of {nok(H['price'], 2)} implies – each driver solved alone, the others at our base case",
                 table(["Driver", "Market-implied", "Our base case", "Gap", "Latest actual"], rd_rows), "Case model (Reverse_DCF sheet)", _src_date(r), note=gate_txt)
    tx = r.rep.get("reverse_text")
    parts.append(cols(rd, box("Reading the reverse DCF", ul(tx, "tight") if tx else p(
        f"The market-implied margin ({pct(rev_['m_last'])}) is the final-year EBIT margin at which our cash flows, discounted at our WACC, are worth "
        f"exactly today's price. Everything above it is what the market does not pay for; everything below it is downside we would be ignoring."), "grey"),
                      widths=["58%", "42%"]))
    # DCF table
    ys = [y for y in r.years if r.is_est(y)]
    spec = [("Revenue", "rev", "n"), ("EBITDA after leases", "ebitdaal", "n"), ("EBIT adj.", "ebit", "n"), ("EBIT adj. margin", "ebit_m", "p"),
            ("Tax on EBIT", "tax", "n"), ("NOPAT", "nopat", "n"), ("+ D&A", "addda", "n"), ("– Capex", "capex", "n"), ("– Change in NWC", "dnwc", "n"),
            ("Free cash flow to the firm", "fcff", "n", "b"), ("ROIC", "roic", "p"), ("Discount factor", "df", "n2"), ("Present value", "pv", "n")]
    rows_, bold, rules = _rows(r, spec, ys, "DCF")
    dcf_tbl = exhibit("DCF – free cash flow after lease payments (pre-IFRS 16)", table(_hdr(r, ys, "NOKm"), rows_, bold_rows=bold), "Case model (DCF sheet)", _src_date(r))
    tv = kv([("Sum of PV, explicit period", num(r.c("DCF", "sum_pv"))), ("PV of terminal value", num(r.c("DCF", "pv_tv"))), ("Terminal value share of EV", pct(H["tv_share"], 0)),
             ("Terminal growth / RONIC", f"{pct(r.c('DCF', 'tv_g'))} / {pct(r.c('DCF', 'tv_ronic'))}"), ("Implied exit multiple (EV/EBITDA after leases)", mult(H["exit_impl"])),
             ("Enterprise value", num(H["ev_dcf"])), ("– Net debt and other claims", num(H["ev_dcf"] - r.c("DCF", "eq", 0))), ("Equity value", num(r.c("DCF", "eq"))),
             ("Diluted shares (m)", num(H["shares_dil"], 1)), ("DCF value per share", f"<b>{nok(H['dcf_ps'], 2)}</b>")])
    wt = kv([(lab, pct(v) if kind == "pct" else num(v, 2)) for lab, v, kind in r.wacc_table()])
    parts.append(dcf_tbl)
    parts.append(cols(box("From enterprise value to the share", tv), box("WACC", wt + f"<div class='legend'>{esc(r.market().get('beta_note', ''))}</div>")))
    # sensitivities
    waccs, gs, grid = r.sens1()
    s1 = exhibit("DCF value per share – WACC (columns) vs terminal growth (rows)",
                 heat_table([pct(g, 2) for g in gs], [pct(w, 2) for w in waccs], grid, center=(2, 3), size=(3.4, 1.8), title_c="WACC", title_r="g"),
                 "Case model (Sensitivity table 1)", _src_date(r))
    ms, gs3, grid3 = r.sens3()
    s3 = exhibit("DCF value per share – growth shift (rows) vs margin shift (columns), pp a year",
                 heat_table([pp(g, 0) for g in gs3], [pp(m, 0) for m in ms], grid3, center=(2, 2), size=(3.0, 1.8), title_c="EBITDA margin", title_r="growth"),
                 "Case model (Sensitivity table 3)", _src_date(r))
    parts.append(cols(s1, s3))
    # SOTP
    sotp, _p = r.sotp()
    if sotp:
        srows = [[esc(k), nok(v.get("dcf"), 1) if isinstance(v, dict) else nok(v, 1)] for k, v in (sotp.items() if isinstance(sotp, dict) else [])]
        parts.append(exhibit("Sum of the parts – the DCF rebuilt step by step", table(["Step", "Value per share"], srows), "Case model (sotp_runs.py)", _src_date(r)))
    # peers
    peers = r.peers()
    if peers:
        groups = r.peer_groups()
        prow = []
        for g, members in groups.items():
            prow.append([f"<b>{esc(g)}</b>"] + [""] * 10)
            for pz in peers:
                if pz[0] not in members:
                    continue
                name, ctry, mcap, ev, evs, evebitda, evebit, pe, margin, growth, *_ = pz
                prow.append([esc(name), esc(ctry), num(mcap), mult(evs[0], 2), mult(evs[1], 2), mult(evebitda[0]), mult(evebitda[1]), mult(evebit[0]), mult(evebit[1]),
                             mult(pe[0]), mult(pe[1])])
        st = r.peer_stats()
        prow.append([f"<b>Median, all peers</b>", "", num(st["median"]["evs"][0] if False else None)] + [mult(st["median"]["evs"][0], 2), mult(st["median"]["evs"][1], 2),
                     mult(st["median"]["evebitda"][0]), mult(st["median"]["evebitda"][1]), mult(st["median"]["evebit"][0]), mult(st["median"]["evebit"][1]),
                     mult(st["median"]["pe"][0]), mult(st["median"]["pe"][1])])
        prow.append([f"<b>{esc(r.company)} at {nok(H['price'], 2)}</b>", "", num(H["mcap"])] + [mult(st["company"]["evs"][0], 2), mult(st["company"]["evs"][1], 2),
                     mult(st["company"]["evebitda"][0]), mult(st["company"]["evebitda"][1]), mult(st["company"]["evebit"][0]), mult(st["company"]["evebit"][1]),
                     mult(st["company"]["pe"][0]), mult(st["company"]["pe"][1])])
        hdr = ["Peer", "Ctry", "Mcap (NOKm)", "EV/Sales LTM", "EV/Sales NTM", "EV/EBITDA LTM", "EV/EBITDA NTM", "EV/EBIT LTM", "EV/EBIT NTM", "P/E LTM", "P/E NTM"]
        parts.append(exhibit("Peer multiples by group (lease-adjusted; LTM = last twelve months, NTM = next-twelve-months consensus)",
                             table([esc(h) for h in hdr], prow, widths=["20%", "4%", "9%"] + ["8.4%"] * 8),
                             r.market().get("cons_note", "Yahoo Finance"), _src_date(r)))
        if trows:
            parts.append(exhibit(f"Implied value per share by peer group – {r.ylabel(yr)} metrics on the group's NTM multiples",
                                 table(["Group", "Multiple", "n", "Min", "Median", "Max", "Value @ min", "Value @ median", "Value @ max"], trows, left=(1,)),
                                 "Case model; peer multiples from Yahoo Finance (data module)", _src_date(r)))
    if peers:
        brows = []
        for pz in peers:
            name, ctry, mcap, ev, evs, evebitda, evebit, pe, margin, growth, beta, de, tax = pz[:13]
            bu = beta / (1 + (1 - tax) * de) if all(isnum(v) for v in (beta, de, tax)) else None
            brows.append([esc(name), esc(ctry), num(beta, 2), pct(de, 0), pct(tax, 0), num(bu, 2)])
        parts.append(exhibit("Peer betas – raw, debt-to-equity and unlevered (Blume-adjusted median feeds the WACC)",
                             table(["Peer", "Ctry", "Raw beta (5y monthly)", "D/E", "Tax", "Unlevered beta"], brows), r.market().get("beta_note", "Yahoo Finance"), _src_date(r)))
    # own history multiples
    hy = _yrs(r, r.years[0], r.last_act)
    px_ye = r.row("price_ye", hy, "Hist")
    eps_h = r.row("eps", hy, "Hist")
    ebitdaal_h = r.row("ebitdaal", hy, "Hist")
    nibd_h = r.row("nibd", hy, "Hist")
    sh_h = r.row("shares", hy, "Hist")
    pe_h = [(pz / e) if (isnum(pz) and isnum(e) and e > 0) else None for pz, e in zip(px_ye, eps_h)]
    evx_h = [((pz * s + n) / eb) if all(isnum(v) for v in (pz, s, n, eb)) and eb > 0 else None for pz, s, n, eb in zip(px_ye, sh_h, nibd_h, ebitdaal_h)]
    labels = [str(y) for y in hy] + ["Now (fwd)"]
    pe_now = H["price"] / r.val("eps", r.first_fc) if isnum(r.val("eps", r.first_fc)) and r.val("eps", r.first_fc) > 0 else None
    ev_now = (H["ev"]) / r.val("ebitdaal", r.first_fc) if isnum(r.val("ebitdaal", r.first_fc)) else None
    pe_vals = [v for v in pe_h if v is not None and v < 60]
    ev_vals = [v for v in evx_h if v is not None]
    own1 = exhibit("P/E at year-end prices on reported EPS, and today's price on our first forecast year",
                   bars(labels, [("P/E", pe_h + [pe_now])], unit="x", size=(3.4, 1.9), legend=False,
                        hline=(statistics.mean(pe_vals), f"avg {statistics.mean(pe_vals):.1f}x") if pe_vals else None),
                   "Company reports (EPS, shares); Yahoo Finance (year-end prices); case model", _src_date(r),
                   note="Trailing multiples on year-end prices. A consensus-based forward P/E history is not available without a paid terminal. Loss years are blank.")
    own2 = exhibit("EV / EBITDA after leases at year-end prices, and today's EV on our first forecast year",
                   bars(labels, [("EV/EBITDA after leases", evx_h + [ev_now])], unit="x", size=(3.4, 1.9), legend=False,
                        hline=(statistics.mean(ev_vals), f"avg {statistics.mean(ev_vals):.1f}x") if ev_vals else None),
                   "Company reports; Yahoo Finance (year-end prices); case model", _src_date(r))
    parts.append(cols(own1, own2))
    dps_h = r.row("dps", hy, "Hist")
    hv = [[esc(str(y)), num(pz, 2), num(e, 2), num(dv, 2), mult(pe_), mult(ev_), pct(dv / pz) if (isnum(dv) and isnum(pz) and pz) else "–"]
          for y, pz, e, dv, pe_, ev_ in zip(hy, px_ye, eps_h, dps_h, pe_h, evx_h)]
    parts.append(exhibit("Historical valuation at year-end prices", table(["Year", "Price (year end)", "EPS", "DPS", "P/E", "EV / EBITDA after leases", "Dividend yield"], hv),
                         "Company reports; Yahoo Finance (year-end prices)", _src_date(r)))
    parts.append(_implied_grid(r, H))
    # football
    fb = r.football()
    if fb:
        frows = [[esc(lab), nok(lo, 1), nok(mid, 1), nok(hi, 1)] for lab, lo, mid, hi in fb]
        parts.append(exhibit("Football field – ranges in value per share today", table(["Method", "Low", "Mid", "High"], frows), "Case model (Football sheet)", _src_date(r)))
    return section("valuation", "Valuation", r.rep.get("valuation_lead"), "".join(parts), 8)


# ====================================================================== 10. financial statements
def financials(r):
    names = _seg_names(r)
    parts = []
    hist = [y for y in r.years if not r.is_est(y)]
    fc = [y for y in r.years if r.is_est(y)]

    def two(title, spec, sheet, src):
        for ys_, tag in ((hist, "history"), (fc, "estimates")):
            rows, bold, rules = _rows(r, spec, ys_, sheet)
            parts.append(exhibit(f"{title} – {tag} {ys_[0]}–{ys_[-1]}", table(_hdr(r, ys_, "NOKm"), rows, bold_rows=bold, rules_before=rules), src, _src_date(r)))

    pl = [("Revenue", "rev", "n", "b"), (f"– {names[0]}", "rev_a", "n"), (f"– {names[1]}", "rev_b", "n"), (f"– {names[2]}", "rev_c", "n"),
          ("Cost of goods sold", "cogs", "n"), ("Personnel expenses", "pers", "n"), ("Other operating expenses", "oth", "n"), ("EBITDA (reported, IFRS 16)", "ebitda", "n", "b"),
          ("Depreciation of owned assets", "da", "n"), ("Depreciation of right-of-use assets", "rou_dep", "n"), ("Special items", "special", "n"), ("EBIT (reported)", "ebit", "n", "b"),
          ("Net financial items ex leases", "netfin", "n"), ("Interest on lease liabilities", "lease_int", "n"), ("Profit before tax", "pbt", "n"), ("Tax", "tax", "n"),
          ("Net profit", "np", "n", "b"), ("EPS (NOK)", "eps", "n2"), ("DPS (NOK)", "dps", "n2"), ("Lease-adjusted view", None, "s"),
          ("Lease payments", "lease", "n"), ("EBITDA after leases", "ebitdaal", "n", "b"), ("EBIT adj. (pre-IFRS 16)", "ebit_adj", "n", "b")]
    two("Income statement", pl, "Model", _src_model(r))
    bs = [("Goodwill", "gw", "n"), ("Property, plant and equipment", "ppe", "n"), ("Right-of-use assets", "rou", "n"), ("Other non-current assets", "other_nca", "n"),
          ("Net working capital", "nwc", "n"), ("Invested capital (ex leases)", "ic", "n", "b"), ("Net interest-bearing debt", "nibd", "n"), ("Lease liabilities", "leases", "n"),
          ("Deferred tax and other", "deftax", "n"), ("Equity", "equity", "n", "b"), ("Minority interests", "min_bs", "n")]
    two("Balance sheet (condensed, year end)", bs, "Output", _src_model(r))
    cf = [("EBITDA after leases", "cf_ebitdaal", "n"), ("Tax paid", "cf_tax", "n"), ("Net financial items", "cf_fin", "n"), ("Special items", "cf_special", "n"),
          ("Change in working capital", "cf_nwc", "n"), ("Other operating items", "cf_other_op", "n"), ("Cash flow from operations after leases", "cfo_al", "n", "b"),
          ("Capex", "cf_capex", "n"), ("Free cash flow to equity", "fcfe", "n", "b"), ("Acquisitions", "cf_acq", "n"), ("Dividends", "cf_div", "n"), ("Buybacks", "cf_bb", "n"),
          ("Other financing", "cf_other", "n"), ("Change in net debt", "d_nibd", "n", "b"), ("Free cash flow to the firm", "fcff", "n", "b")]
    two("Cash flow (lease-adjusted)", cf, "Output", _src_model(r))
    kr = [("Revenue growth", "g_rev", "p"), ("– of which new locations", "g_new", "p"), ("– of which like-for-like volume", "g_lfl", "p"), ("– of which price/mix", "g_px", "p"),
          ("EBITDA margin (reported)", "ebitda_m", "p"), ("EBITDA after leases margin", "ebitdaal_m", "p"), ("EBIT adj. margin", "ebit_adj_m", "p"), ("Net margin", "np_m", "p"),
          ("Effective tax rate", "tax_eff", "p"), ("ROIC", "roic", "p"), ("ROE", "roe", "p"), ("Cash conversion (FCFF / EBITDA after leases)", "cconv", "p"),
          ("Capex / sales", "capex_s", "p"), ("NWC / sales", "nwc_s", "p"), ("NIBD / EBITDA after leases (x)", "lev", "x"), ("Interest cover (x)", "int_cov", "x"),
          ("Payout ratio", "payout", "p"), ("Shares (m)", "shares", "n1"), ("Book value per share (NOK)", "bvps", "n1"), ("FCF per share (NOK)", "fcfps", "n2"),
          ("EV / Sales (x)", "evs", "x"), ("EV / EBITDA after leases (x)", "evebitda", "x"), ("EV / EBIT adj. (x)", "evebit", "x"), ("P / E (x)", "pe", "x"), ("P / B (x)", "pb", "x"),
          ("FCF yield", "fcf_yield", "p"), ("Dividend yield", "div_yield", "p")]
    two("Key ratios (multiples at the current share price)", kr, "Analysis", _src_model(r))
    # drivers
    dr = [("Like-for-like volume growth – " + names[0], "lfl_a", "p"), ("Like-for-like volume growth – " + names[1], "lfl_b", "p"), ("Like-for-like volume growth – " + names[2], "lfl_c", "p"),
          ("Price/mix growth – " + names[0], "px_a", "p"), ("Price/mix growth – " + names[1], "px_b", "p"), ("Price/mix growth – " + names[2], "px_c", "p"),
          ("Net new locations – " + names[0], "net_a", "n"), ("Net new locations – " + names[1], "net_b", "n"), ("Net new locations – " + names[2], "net_c", "n"),
          ("Fixed-cost inflation", "cpi", "p"), ("Maintenance capex / sales", "mcapex", "p"), ("Capex per new location (NOKm)", "capex_loc", "n1"), ("NWC / sales", "nwc", "p"),
          ("Tax rate", "tax", "p"), ("Payout ratio", "payout", "p")]
    fy = fc
    rows, bold, rules = _rows(r, dr, fy, "Drivers")
    parts.append(exhibit("Forecast drivers (base case)", table(_hdr(r, fy), rows), "Case data module (BASE)", _src_date(r)))
    q = r.quarters()
    if q:
        labels = _q_sorted(q)[-8:]
        lines = [("Revenue", "rev", "n"), ("EBITDA reported", "ebitda", "n"), ("EBITDA after leases", "ebitdaal", "n"), ("EBIT (reported)", "ebit", "n"), ("EBIT adj.", "ebit_adj", "n"),
                 ("Net profit", "np", "n"), ("EPS (NOK)", "eps", "n2")]
        rows = [[esc(lab)] + [_fmt(kind)(q["rows"][l_].get(key)) for l_ in labels] for lab, key, kind in lines]
        parts.append(exhibit("Quarterly numbers (reported)", table([esc("NOKm")] + [esc(l_) for l_ in labels], rows), f"Company reports ({q['source']})", q["date"]))
    return section("financials", "Financial statements", None, "".join(parts), 9)


# ====================================================================== 11. what we do not know
def unknowns(r, gate):
    H = r.head()
    rep = r.rep
    parts = []
    # data map
    dm = list(rep.get("data_map") or [])
    cons = r.consensus()
    missing_cons = [m for m in ("ebitda", "ebit", "dps") if all(not isnum(c) for _, c, _ in cons["rows"][m])]
    if missing_cons:
        dm.append(("Consensus " + ", ".join(m.upper() for m in missing_cons), "Missing", f"{cons['source']} has revenue and EPS only; Bloomberg/FactSet not used"))
    if not (cons.get("quarter")):
        dm.append(("Consensus for the next quarter by line and segment", "Missing", "Infront/Bloomberg not used; Yahoo gives one EPS and revenue mean"))
    if not r.quarters():
        dm.append(("Quarterly history by segment", "Not collected", "company reports – add QUARTERS"))
    if not r.prices():
        dm.append(("Price history", "Not fetched", "yfinance – build with --refresh-prices"))
    dm.append(("Web traffic for the company and its competitors", "Missing", "Similarweb (paid) – no free equivalent"))
    dm.append(("Peer operating estimates (units, members, revenue per unit)", "Missing", "Visible Alpha (paid); peers' own reports give history only"))
    rows = [[md(a), _tag(b, {"Have": "ok", "Collected": "ok"}.get(b, "watch" if b.lower().startswith("not") else "na")), md(c)] for a, b, c in dm]
    parts.append(exhibit("Data map – what this report could not use", table(["Input", "Status", "Source we lack / what we did instead"], rows, cls="num wrap",
                                                                            widths=["36%", "12%", "52%"], left=(1, 2)), "This report", fmt_date(r.today)))
    # assumptions that carry most
    wi, wpath = r.whatif()
    if wi:
        base = wi.get("Base case") or next(iter(wi.values()))
        items = [(k, v) for k, v in wi.items() if k != "Base case"]
        items.sort(key=lambda kv_: -abs((kv_[1].get("dcf") or 0) - (base.get("dcf") or 0)))
        wrows = [[md(k), nok(v.get("dcf"), 1), nok(v.get("dcf", 0) - base.get("dcf", 0), 1), nok(v.get("tp")), _tag(v.get("rating", ""), _rating_cls(v.get("rating", "")))]
                 for k, v in items]
        parts.append(exhibit(f"The assumptions that carry most – one change at a time from the base case (DCF {nok(base.get('dcf'), 1)}, TP {nok(base.get('tp'))} {esc(base.get('rating', ''))})",
                             table(["Change", "DCF value", "vs base", "Target", "Rating"], wrows, cls="num wrap", widths=["52%", "12%", "12%", "12%", "12%"], left=(4,)),
                             f"Case model, whatif_runs.py ({wpath.split(chr(92))[-1].split('/')[-1]})", _src_date(r)))
        flips = [k for k, v in items if v.get("rating") != base.get("rating")]
    else:
        parts.append(placeholder("What-if runs not found", "run model_builder/whatif_runs.py (Windows, Excel) – the table ranks the assumptions by their effect on value"))
        flips = []
    try:
        res, _a = r.audit()
        jrows = [[esc(x.id), esc(x.name), esc(x.detail), esc(x.reason or "–")] for x in res if x.status in (_a.JUSTIFIED, _a.WARN, _a.MISSING, _a.FLAG, _a.FAIL)]
        if jrows:
            parts.append(exhibit("The judgements on the record – audit items that are not a plain pass, and the answer given",
                                 table(["#", "Failure mode", "What the audit saw", "The case's answer"], jrows, cls="num wrap", widths=["5%", "18%", "40%", "37%"], left=(1, 2, 3)),
                                 "model_builder/audit.py on this workbook; reasons from META['reasons']", fmt_date(r.today)))
    except Exception:  # noqa: BLE001
        pass
    # what would flip the conclusion
    st, spath = r.stress()
    srows = []
    if st:
        for x in st:
            if x.get("kind") == "research" or x["tag"].startswith(("Scenario", "WACC override", "Share price")):
                srows.append([esc(x["tag"]), nok(x.get("dcf"), 1), nok(x.get("tp")), _tag(x.get("rating", ""), _rating_cls(x.get("rating", "")))])
    fl = rep.get("flips") or []
    fl_html = ul(fl) if fl else ""
    if flips:
        fl_html += p("One-at-a-time changes that flip the rating: " + "; ".join(flips) + ".")
    if srows:
        fl_html += exhibit("Stress tests (ANALYSE.md) – value and rating under each", table(["Stress", "DCF value", "Target", "Rating"], srows, left=(3,)), "Case model, stress_test.py", _src_date(r))
    elif gate and any(i["name"] == "stress_test.py" and i["ok"] is None for i in gate["items"]):
        fl_html += placeholder("Stress tests not run in this build", "the research-driven stresses (margin reversion, NWC held, WACC +1pp, RONIC = WACC) need Excel")
    parts.append(h2("What would change the conclusion") + (fl_html or placeholder("not written", "report['flips']")))
    unk = rep.get("unknowns")
    parts.append(h2("What we do not know") + (ul(unk) if unk else placeholder("not written", "report['unknowns'] – the questions we could not answer with public data")))
    return section("unknowns", "What we do not know", rep.get("unknowns_lead"), "".join(parts), 10)


# ====================================================================== disclosures + checks
def disclosures(r, gate):
    meta = r.meta()
    disc = meta.get("disclosures", {}) or {}
    rows = [("Status", disc.get("status", "Private student case study; not investment research or advice")), ("Author", disc.get("author", "Case author")),
            ("Prices used", disc.get("price_datetime", _date_str(r.price_date))), ("Balance sheet date", _date_str(r.bs_date)), ("Model date", _date_str(r.model_date)),
            ("Rating definitions", disc.get("rating_definitions", "")), ("Valuation method", disc.get("valuation_summary", "")),
            ("Update frequency", disc.get("update_frequency", "")), ("12-month history", disc.get("history_12m", "")),
            ("Conflicts of interest", meta.get("conflicts") or "Not stated by the author (META['conflicts'] is empty) – the author must fill this before any distribution"),
            ("Data", r.market().get("data_note", ""))]
    parts = [box("Disclosures (MAR art. 20 / 2016/958 and VPFF Standard 3 items, as applied to a student case)", kv([(k, md(v)) for k, v in rows]))]
    hist = r.history()
    if hist:
        hrows = [[esc(fmt_date(h[0])), _tag(h[1], _rating_cls(h[1])), nok(h[2]), nok(h[3], 2), esc(h[4]) if len(h) > 4 else ""] for h in hist]
        parts.append(exhibit("History of ratings and targets", table(["Date", "Rating", "Target", "Price at the call", "Note"], hrows, left=(1, 4)), "Judgement log (private) as copied to the case module", fmt_date(r.today)))
    else:
        parts.append(placeholder("No rating history", "HISTORY = [(date, rating, target, price, note)] in the data module; the first row is this report"))
    # gate
    if gate:
        grows = [[esc(i["name"]), _tag({True: "passed", False: "FAILED", None: "skipped"}[i["ok"]], {True: "ok", False: "broken", None: "na"}[i["ok"]]), esc(i["detail"])]
                 for i in gate["items"]]
        parts.append(exhibit("Build gate – the checks that must pass before this report is built", table(["Check", "Result", "Detail"], grows, cls="num wrap", widths=["22%", "10%", "68%"], left=(1, 2)),
                             "verify_dcf.py, stress_test.py, audit.py, case_gate.py", fmt_date(r.today)))
    ck = r.checks()
    crows = [[str(c["n"]), esc(c["check"]), esc(c["type"]), _tag(str(c["status"]), {"OK": "ok", "WARNING": "watch", "ERROR": "broken"}.get(str(c["status"]), "na"))] for c in ck]
    parts.append(exhibit(f"Workbook integrity checks – {esc(r.master())}", table(["#", "Check", "Type", "Status"], crows, cls="num wrap", widths=["5%", "70%", "12%", "13%"], left=(1, 2)), "Case model (Checks sheet)", _src_date(r)))
    srcs = r.rep.get("sources")
    if srcs:
        parts.append(exhibit("Sources used in this report", table(["Source", "Used for", "Date"], [[md(a), md(b), esc(c)] for a, b, c in srcs], cls="num wrap",
                                                                      widths=["38%", "44%", "18%"], left=(1, 2)), "This report", fmt_date(r.today)))
    gl = [("EBITDA after leases (EBITDAaL)", "EBITDA less the lease payments of the period – the pre-IFRS 16 operating cash margin the valuation is built on."),
          ("EBIT adj.", "EBITDA after leases less depreciation of owned assets; excludes special items. The margin the reverse DCF solves for."),
          ("FCFF", "NOPAT + D&A − capex − change in working capital, after lease payments; discounted at the WACC."),
          ("ROIC", "NOPAT over invested capital excluding right-of-use assets."),
          ("NIBD / EV", "Net interest-bearing debt excluding lease liabilities; enterprise value = market capitalisation + NIBD + other claims (pre-IFRS 16)."),
          ("Target price", "Blended fair value today (DCF and peer multiples), rolled forward twelve months at the cost of equity less the expected dividend, rounded."),
          ("Rating", str(disc.get("rating_definitions", "BUY / HOLD / SELL around the cost of equity"))),
          ("Reverse DCF", "The value of one driver (final-year margin, revenue CAGR, WACC or terminal growth) at which our model returns today's share price, the others held at our base case."),
          ("Case gate", "The report is only built if a driver differs from the market-implied value by at least 1pp and the DCF is at least 10 % from the price."),
          ("Kill criterion", "A KPI level at which the thesis is wrong; checked against the latest actual (status on track / watch / breached) and against the base case."),
          ("EST", "A case-team estimate (forecast, split or assumption), as opposed to a reported figure."),
          ("Not available", "A figure the sell side buys (Bloomberg, FactSet, Visible Alpha, Similarweb) and this toolkit does not have; never replaced by a guess.")]
    parts.append(exhibit("Definitions", table(["Term", "Meaning"], [[esc(a), esc(b)] for a, b in gl], cls="num wrap", widths=["22%", "78%"], left=(1,)),
                         "ANALYSE.md, model_builder/README.md", fmt_date(r.today)))
    try:
        res, _a = r.audit()
        arows = [[esc(x.id), esc(x.name), _tag(x.status, {"PASS": "ok", "JUSTIFIED": "ok", "WARN": "watch", "MISSING": "watch", "FLAG": "broken", "FAIL": "broken"}.get(x.status, "na")),
                  esc(x.detail) + (f" <i>Reason: {esc(x.reason)}</i>" if x.reason else "")] for x in res]
        parts.append(exhibit("Case audit – the 30 failure modes of ANALYSE.md section 4", table(["#", "Failure mode", "Status", "Detail"], arows, cls="num wrap", widths=["5%", "20%", "9%", "66%"], left=(1, 3)),
                             "model_builder/audit.py", fmt_date(r.today)))
    except Exception as e:  # noqa: BLE001
        parts.append(placeholder("Audit could not run", str(e)))
    return section("disclosures", "Disclosures, sources and checks", None, "".join(parts), 11)
