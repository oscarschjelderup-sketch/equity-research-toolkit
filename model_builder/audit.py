"""Case audit: the 30 documented failure modes of sell-side valuation (docs/research/03) and the Norwegian rules
(docs/research/04) as checks on a finished workbook. Run by verify_dcf.py after the DCF replica, or on its own:

    python audit.py <private>.xlsx model_map_<private>.json <private>_data
    python audit.py ../examples/SATS/SATS_ASA_DCF_Model.xlsx model_map_sats.json sats_data --json

Statuses
  PASS      the check ran and the case passes
  WARN      a soft warning: worth a look, not a blocker
  FLAG      the check needs a written reason in the case's META to clear (Auto + judgement in 03); with a reason it
            reports JUSTIFIED and shows the reason, so the judgement is on the record
  FAIL      a hard error (a broken identity, a rule with no exception)
  MISSING   the input the check needs is not in the case yet – it is not passed silently
  N/A       the check does not apply to this case (e.g. no commodity exposure)

Case inputs come from the workbook (values saved by Excel) and from an optional ``META`` dict in the case data
module: sector, cyclical, reporting currency, commodity deck, resource-rent tax, guidance, conflicts block, and
``reasons`` – a dict from check id to the written justification. Thresholds are proposals recorded in DECISIONS.md.
"""
from __future__ import annotations

import argparse
import importlib
import json
import statistics
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import openpyxl

HC = list("EFGHIJK")
FC = list("LMNOPQRS")
PASS, WARN, FLAG, FAIL, MISSING, NA, JUSTIFIED = "PASS", "WARN", "FLAG", "FAIL", "MISSING", "N/A", "JUSTIFIED"
ORDER = {FAIL: 0, FLAG: 1, MISSING: 2, WARN: 3, JUSTIFIED: 4, PASS: 5, NA: 6}

# PwC/FFN "Risikopremien i det norske markedet" 2025 (docs/research/04, section 2): size premium medians by equity
# value in NOK bn -> premium; market risk premium median 5.0 %
SIZE_PREMIUM = [(5.0, 0.00), (2.0, 0.01), (1.0, 0.02), (0.5, 0.02), (0.1, 0.03), (0.0, 0.04)]
ERP_BAND = (0.04, 0.06)
SECTOR_TAX = {"salmon": 0.22 + 0.25 * (1 - 0.22), "eandp": 0.78}      # ground-rent 25 % effective on top; NCS 78 % marginal


@dataclass
class Result:
    id: str
    name: str
    status: str
    detail: str
    source: str
    reason: str | None = None


def _num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


class Case:
    def __init__(self, xlsx, cell_map, data_module: str | None = None):
        self.reg = json.loads(Path(cell_map).read_text(encoding="utf8"))
        self.wb = openpyxl.load_workbook(xlsx, data_only=True)
        self.meta, self.data = {}, None
        if data_module:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            self.data = importlib.import_module(data_module)
            self.meta = dict(getattr(self.data, "META", {}) or {})
        self.reasons = dict(self.meta.get("reasons", {}))

    def c(self, key):
        sheet = key.split("|")[0]
        return self.wb[sheet][self.reg["cells"][key]].value

    def has(self, key) -> bool:
        return key in self.reg["cells"] or key in self.reg["rows"]

    def row(self, key, cols=FC):
        sheet = key.split("|")[0]
        r = self.reg["rows"][key]
        return [self.wb[sheet][f"{col}{r}"].value for col in cols]

    def hist(self, key):
        return [v for v in self.row(key, HC) if _num(v)]

    def years(self, cols):
        return [self.wb["Model"][f"{c}5"].value for c in cols]


def _p(x, d=1, sign=False):
    return f"{x * 100:{'+' if sign else ''}.{d}f}%" if _num(x) else "n.a."


def _flag(case: Case, cid: str, name: str, detail: str, source: str, warn_only=False) -> Result:
    if cid in case.reasons:
        return Result(cid, name, JUSTIFIED, detail, source, case.reasons[cid])
    return Result(cid, name, WARN if warn_only else FLAG, detail + " – add META['reasons']['" + cid + "'] if this is intended", source)


def audit(case: Case, price_now: float | None = None, today: datetime | None = None) -> list[Result]:
    R: list[Result] = []
    m = case.meta
    add = R.append
    rev_h, rev_f = case.hist("Model|is_rev"), case.row("Model|is_rev")
    marg_h, marg_f = case.hist("Model|ebit_adj_m"), case.row("Model|ebit_adj_m")
    cpi = [v for v in case.row("Drivers|b_cpi")] if case.has("Drivers|b_cpi") else []
    infl = statistics.mean(cpi) if cpi and all(_num(v) for v in cpi) else 0.02
    price, dcf, tp = case.c("Inputs|price"), case.c("DCF|dcf_ps"), case.c("DCF|tp")
    ke, wacc = case.c("WACC|ke"), case.c("WACC|wacc")
    g, ronic = case.c("DCF|tv_g"), case.c("DCF|tv_ronic")
    t4 = {k: col for col, k, _, _ in case.reg["t4"]}
    r0 = case.reg["sens"]["t4_rows"][0]
    sc = lambda key, j: case.wb["Sensitivity"][f"{t4[key]}{r0 + j}"].value  # noqa: E731

    # ---------------------------------------------------------------- A. forecast optimism and bias
    n = len(rev_f)
    cagr = (rev_f[-1] / rev_h[-1]) ** (1 / n) - 1
    real = cagr - infl
    detail = f"revenue CAGR {_p(cagr)} nominal, {_p(real)} real over {n} years"
    if real > 0.20:
        add(_flag(case, "A1", "Growth above base rates", detail + "; a real CAGR above 20% over a decade was reached by 18% of "
                  "small firms and 0.2% of large ones (Base Rate Book)", "03 #1, A20"))
    else:
        add(Result("A1", "Growth above base rates", PASS, detail, "03 #1, A20"))

    bear, base, bull = sc("dcf_ps", 0), sc("dcf_ps", 1), sc("dcf_ps", 2)
    g_bear, g_bull = sc("cagr", 0), sc("cagr", 2)
    probs = [case.c(f"Drivers|adj_prob_{s}") for s in ("bear", "base", "bull")]
    spread = g_bull - g_bear
    d = f"bear {bear:.1f} / base {base:.1f} / bull {bull:.1f} per share; revenue CAGR spread bull-bear {_p(spread)}"
    if bear > 0.75 * base or spread < 0.05:
        add(_flag(case, "A2", "Forecast range too narrow", d + "; bear should be ≥25% below base and the growth spread wide "
                  "(consensus SD 8.3% vs realised 18.7%)", "03 #2, A20"))
    else:
        add(Result("A2", "Forecast range too narrow", PASS, d, "03 #2, A20"))

    hist_max = max(marg_h)
    d = f"final-year EBIT adj. margin {_p(marg_f[-1])} vs historical max {_p(hist_max)}"
    if marg_f[-1] > hist_max + 0.02:
        add(_flag(case, "A3", "Hockey-stick margins", d + " (+2pp limit)", "03 #3, A4, A20"))
    else:
        add(Result("A3", "Hockey-stick margins", PASS, d, "03 #3"))

    cr = case.reg["comps"]
    peer_m = case.wb["Comps"][f"R{cr['median']}"].value
    now_m = marg_h[-1]
    if _num(peer_m) and now_m > peer_m and marg_f[-1] >= now_m:
        add(_flag(case, "A4", "No mean reversion", f"margin today {_p(now_m)} above the peer median {_p(peer_m)} and still rising "
                  f"to {_p(marg_f[-1])}" + (" (peer margins on an IFRS 16 basis: not like-for-like with EBIT adj.)" if case.c("Inputs|peer_lease") else ""), "03 #4, A20, A23"))
    else:
        add(Result("A4", "No mean reversion", PASS, f"margin {_p(now_m)} vs peer median {_p(peer_m)}", "03 #4"))

    ratio = ronic / wacc
    d = f"terminal RONIC {_p(ronic)} / WACC {_p(wacc)} = {ratio:.2f}x"
    if ratio > 2.0:
        add(_flag(case, "A5", "Terminal returns not faded", d + " (>2.0x)", "03 #5; 04 R14"))
    elif ratio > 1.5:
        add(Result("A5", "Terminal returns not faded", WARN, d + " (>1.5x)", "03 #5; 04 R14"))
    elif ratio < 1.0:
        add(Result("A5", "Terminal returns not faded", WARN, d + ": growth destroys value in the TV", "03 #5"))
    else:
        add(Result("A5", "Terminal returns not faded", PASS, d, "03 #5"))

    rf = case.c("WACC|rf")
    nopat, reinv = case.c("DCF|tv_nopat"), case.c("DCF|tv_reinv")
    implied = -reinv / nopat if nopat else None
    if g > rf:
        add(Result("A6", "Terminal growth not paid for", FAIL, f"g {_p(g)} above rf {_p(rf)}", "03 #6; 04 R10"))
    elif implied is None or abs(implied - g / ronic) > 0.01:
        add(Result("A6", "Terminal growth not paid for", FAIL, f"TV reinvestment {_p(implied)} of NOPAT vs g/RONIC {_p(g / ronic)}", "03 #6; 04 R12"))
    else:
        add(Result("A6", "Terminal growth not paid for", PASS, f"g {_p(g)} ≤ rf {_p(rf)}; reinvestment {_p(implied)} of NOPAT = g/RONIC", "03 #6; 04 R10-R13"))

    tvs = case.c("DCF|tv_share")
    rd_ok = _num(case.c("Reverse_DCF|rd_m_last"))
    if tvs > 0.90 and not rd_ok:
        add(Result("A7", "Terminal value dominance", FAIL, f"TV {_p(tvs, 0)} of EV and no reverse DCF", "03 #7"))
    elif tvs > 0.80:
        add(Result("A7", "Terminal value dominance", WARN, f"TV {_p(tvs, 0)} of EV (>80%); reverse DCF solved: {rd_ok}", "03 #7; 04 R17"))
    else:
        add(Result("A7", "Terminal value dominance", PASS, f"TV {_p(tvs, 0)} of EV", "03 #7; 04 R17"))

    if m.get("cyclical") is None:
        add(Result("A8", "Peak-cycle earnings capitalised", MISSING, "META['cyclical'] not set", "03 #8; 04 R15, R21-R22"))
    elif m["cyclical"]:
        sd = statistics.pstdev(marg_h) if len(marg_h) > 1 else 0
        lim = statistics.mean(marg_h) + sd
        st = PASS if marg_f[-1] <= lim else FLAG
        r = Result("A8", "Peak-cycle earnings capitalised", st, f"terminal margin {_p(marg_f[-1])} vs through-cycle mean+1SD {_p(lim)} "
                   f"({len(marg_h)} years of history)", "03 #8; 04 R15")
        add(_flag(case, "A8", r.name, r.detail, r.source) if st == FLAG else r)
    else:
        add(Result("A8", "Peak-cycle earnings capitalised", NA, "not cyclical (META)", "03 #8"))

    deck = m.get("commodity_deck")
    if m.get("commodity"):
        if not deck:
            add(Result("A9", "Commodity deck vs forward curve", MISSING, f"commodity '{m['commodity']}' but no dated price deck in META", "03 #9; 04 R23-R24"))
        else:
            gap = deck["model"] / deck["forward"] - 1
            r = Result("A9", "Commodity deck vs forward curve", PASS if abs(gap) <= 0.10 else FLAG,
                       f"model price {deck['model']} vs forward {deck['forward']} ({deck.get('date', '?')}): {_p(gap, sign=True)}", "03 #9; 04 R24")
            add(r if r.status == PASS else _flag(case, "A9", r.name, r.detail, r.source))
    else:
        add(Result("A9", "Commodity deck vs forward curve", NA, "no commodity exposure in META", "03 #9"))

    guide = {k: v for k, v in (m.get("guidance") or {}).items() if v}
    if not guide:
        add(Result("A10", "Anchoring to management guidance", MISSING, "no company guidance in META['guidance']", "03 #10"))
    else:
        notes, st = [], PASS
        if "revenue" in guide:
            yr, (lo, hi) = guide["revenue"]["year"], guide["revenue"]["range"]
            ours = rev_f[case.years(FC).index(f"{yr}E")] if f"{yr}E" in case.years(FC) else None
            if ours is not None:
                notes.append(f"revenue {yr}E {ours:,.0f} vs guidance {lo:,.0f}-{hi:,.0f}")
                if ours > hi:
                    st = FLAG
                elif lo <= ours <= hi and abs(ours / ((lo + hi) / 2) - 1) < 0.01:
                    st = FLAG
        if "ebit_margin" in guide:
            lo, hi = guide["ebit_margin"]
            ebm = case.row("Model|ebit_m")[4]
            notes.append(f"EBIT margin (IFRS 16) {_p(ebm)} vs guidance {_p(lo, 0)}-{_p(hi, 0)}")
            if ebm > hi:
                st = FLAG
        d = "; ".join(notes)
        add(Result("A10", "Anchoring to management guidance", PASS, d + " – independent of and not above guidance", "03 #10") if st == PASS
            else _flag(case, "A10", "Anchoring to management guidance", d + ": above the top of, or equal to, guidance", "03 #10"))

    cons = [case.c(f"Consensus|diff_{k}_{y}") for k in ("rev", "ebit", "eps") for y in (1, 2, 3)]
    rating = case.c("DCF|rating")
    if not any(_num(x) for x in cons):
        add(Result("A11", "Herding on consensus", MISSING, "no consensus in the workbook (case_gate.py tests the market-implied gap instead)", "03 #11"))
    elif all(_num(x) and abs(x) <= 0.02 for x in cons) and rating in ("BUY", "SELL"):
        add(Result("A11", "Herding on consensus", FAIL, f"{rating} while revenue, EBIT and EPS are within ±2% of consensus in all years", "03 #11"))
    else:
        add(Result("A11", "Herding on consensus", PASS, "estimates differ from consensus: " + ", ".join(_p(x, sign=True) for x in cons if _num(x)), "03 #11"))

    val_date = case.c("Inputs|val_date")
    today = today or datetime.now()
    age = (today - val_date).days
    if price_now is not None and price_now < price * 0.75:
        add(Result("A12", "Stale target after bad news", FAIL, f"price {price_now:.2f} is {_p(price_now / price - 1)} since the model date – update before publishing", "03 #12"))
    elif age > 120:
        add(Result("A12", "Stale target after bad news", WARN, f"model is {age} days old", "03 #12"))
    else:
        add(Result("A12", "Stale target after bad news", PASS if price_now is not None else WARN,
                   f"model {age} days old" + (f"; price {price_now:.2f} vs {price:.2f} at the model date" if price_now is not None else "; current price not given (--price-now)"), "03 #12"))

    tr = case.c("DCF|tp_tr")
    d = f"expected total return {_p(tr)} vs Ke {_p(ke)}"
    if tr > ke + 0.40:
        add(Result("A13", "Target-price optimism", WARN, d + " (>Ke+40pp)", "03 #13, A1-A4"))
    elif tr > ke + 0.15:
        ok = rd_ok and bear < price
        add(Result("A13", "Target-price optimism", PASS if ok else FLAG, d + f" (>Ke+15pp): reverse DCF {'shown' if rd_ok else 'MISSING'}, "
                   f"bear {bear:.1f} {'below' if bear < price else 'NOT below'} the price", "03 #13, A1, A4"))
    else:
        add(Result("A13", "Target-price optimism", PASS, d, "03 #13"))

    buy, sell = case.c("Inputs|buy_th"), case.c("Inputs|sell_th")
    sym = abs(buy + sell) < 1e-9
    add(Result("A14", "Skewed rating scale", PASS if sym and buy >= 0.05 else WARN,
               f"BUY above Ke{_p(buy, 0, True)}, SELL below Ke{_p(sell, 0, True)} (expected total return vs cost of equity)", "03 #14"))

    if m.get("binary_event"):
        ok = all(_num(p) for p in probs) and abs(sum(probs) - 1) < 1e-6
        add(Result("A15", "Binary event not weighted", PASS if ok else FAIL, f"binary event '{m['binary_event']}': scenario probabilities {probs}", "03 #15"))
    else:
        add(Result("A15", "Binary event not weighted", NA if "binary_event" in m else MISSING,
                   "no binary event (META)" if "binary_event" in m else "META['binary_event'] not set", "03 #15"))

    sector = m.get("sector")
    tax = case.row("Drivers|b_tax")[-1] if case.has("Drivers|b_tax") else None
    if sector in SECTOR_TAX:
        need = SECTOR_TAX[sector]
        add(Result("A16", "Tax and regulatory regime", PASS if _num(tax) and tax >= need - 0.01 else FAIL,
                   f"{sector}: model tax {_p(tax)} vs required ≥ {_p(need)}", "03 #16; 04 R33-R34"))
    elif sector:
        add(Result("A16", "Tax and regulatory regime", PASS, f"sector '{sector}': ordinary corporate tax {_p(tax)}", "03 #16"))
    else:
        add(Result("A16", "Tax and regulatory regime", MISSING, "META['sector'] not set", "03 #16"))

    # ---------------------------------------------------------------- B. technical valuation errors
    nwc_h = [n_ / r_ for n_, r_ in zip(case.hist("Model|nwc")[-3:], rev_h[-3:], strict=False)]
    nwc_f = [n_ / r_ for n_, r_ in zip(case.row("Model|nwc"), rev_f, strict=True)]
    drop = statistics.mean(nwc_h) - min(nwc_f)
    # a release = the NWC/sales ratio falls by more than 1pp in a growth year (a negative-NWC business releasing cash
    # as it grows, at a stable ratio, is the business model, not a forecast error)
    ratios = [nwc_h[-1]] + nwc_f
    revs = [rev_h[-1]] + rev_f
    grow_years_release = sum(1 for i in range(1, len(ratios)) if revs[i] > revs[i - 1] and ratios[i] < ratios[i - 1] - 0.01)
    d = f"NWC {_p(statistics.mean(nwc_h))} of revenue (3y avg) → low of {_p(min(nwc_f))} in the forecast"
    if drop > 0.05 or grow_years_release:
        add(_flag(case, "B17", "Working capital", d + (f"; NWC released in {grow_years_release} growth year(s)" if grow_years_release else "") + " (>5pp fall)", "03 #17"))
    else:
        add(Result("B17", "Working capital", PASS, d, "03 #17"))

    capex = [-x for x in case.row("Model|capex")]
    da = [-x for x in case.row("Model|da")]
    short = [y for y, cx, dd, (a, b) in zip(case.years(FC), capex, da, zip([rev_h[-1]] + rev_f[:-1], rev_f, strict=True), strict=True) if b > a and cx < dd]
    add(Result("B18", "Capex below depreciation while growing", WARN if short else PASS,
               ("capex < D&A (owned assets) in growth years " + ", ".join(short)) if short else "capex ≥ D&A (owned assets) in every growth year", "03 #18; 04 R13"))

    chk = case.wb["Checks"]
    found = None
    for row in chk.iter_rows(min_row=1, max_row=chk.max_row):
        texts = [str(c.value) for c in row if c.value is not None]
        if any("new capital" in t.lower() for t in texts):
            found = texts
            break
    if found:
        st = PASS if any(t.strip().upper() == "OK" for t in found) else WARN
        add(Result("B19", "Growth not paid for", st, "workbook check: " + " | ".join(found[1:4]), "03 #19"))
    else:
        add(Result("B19", "Growth not paid for", MISSING, "return-on-new-capital check not found on the Checks sheet", "03 #19"))

    dv, de = case.c("WACC|dv"), case.c("WACC|de")
    ok = abs(de - dv / (1 - dv)) < 1e-6
    dv_model = case.c("WACC|dv_model")
    d = f"relevering D/E {_p(de)} = D/V {_p(dv)} / (1 − D/V): {ok}" + (f"; forecast D/V {_p(dv_model)}" if _num(dv_model) else "")
    st = FAIL if not ok else (WARN if _num(dv_model) and abs(dv_model - dv) > 0.05 else PASS)
    add(Result("B20", "Inconsistent leverage in WACC", st, d, "03 #20"))

    erp, size, spec = case.c("WACC|erp"), case.c("WACC|size") or 0, case.c("WACC|specific") or 0
    mcap_bn = price * case.c("Inputs|shares") / 1000
    size_ref = next(p for lo, p in SIZE_PREMIUM if mcap_bn >= lo)
    cur = case.c("Inputs|currency")
    rcur = m.get("reporting_currency")
    probs_ = []
    if not ERP_BAND[0] <= erp <= ERP_BAND[1]:
        probs_.append(f"ERP {_p(erp)} outside {_p(ERP_BAND[0], 0)}-{_p(ERP_BAND[1], 0)}")
    if size + spec > 0.03:
        probs_.append(f"size + specific premia {_p(size + spec)} > 3pp")
    if abs(size - size_ref) > 0.0051:
        probs_.append(f"size premium {_p(size)} vs PwC/FFN median {_p(size_ref, 0)} for NOK {mcap_bn:.1f}bn equity")
    d = f"rf {_p(rf, 2)}, ERP {_p(erp)}, size {_p(size)}, specific {_p(spec)}; equity NOK {mcap_bn:.1f}bn"
    if rcur and rcur != cur:
        add(Result("B21", "rf / ERP / currency", FAIL, d + f"; cash flows in {rcur}, rf for {cur}", "03 #21; 04 R1-R7"))
    elif probs_:
        add(_flag(case, "B21", "rf / ERP / currency", d + "; " + "; ".join(probs_), "03 #21; 04 R2-R6"))
    else:
        add(Result("B21", "rf / ERP / currency", PASS, d, "03 #21; 04 R1-R6"))

    if not rcur:
        add(Result("B22", "Reporting vs listing currency", MISSING, "META['reporting_currency'] not set", "03 #22"))
    elif rcur == cur:
        add(Result("B22", "Reporting vs listing currency", PASS, f"reports and lists in {cur}", "03 #22"))
    else:
        fx = m.get("fx")
        add(Result("B22", "Reporting vs listing currency", PASS if fx and fx.get("date") else FAIL,
                   f"reports in {rcur}, lists in {cur}; FX {fx}", "03 #22; 04 R7"))

    leases, b_nibd, nibd = case.c("Inputs|leases"), case.c("DCF|b_nibd"), case.c("Inputs|nibd")
    pre16 = abs(-b_nibd - nibd) < 0.5
    peer_lease = case.c("Inputs|peer_lease")
    d = (f"FCFF after lease payments (pre-IFRS 16); bridge deducts NIBD {nibd:,.0f} ex leases; lease liabilities "
         f"{leases:,.0f} shown as memo only; peers on {'an IFRS 16 basis (EV incl. leases)' if peer_lease else 'a pre-IFRS 16 basis'}")
    add(Result("B23", "IFRS 16 double count / omission", PASS if pre16 else FAIL, d if pre16 else f"bridge {b_nibd} ≠ −NIBD {nibd}: leases may be double counted", "03 #23; 04 R30-R32"))

    mins_pl = case.hist("Hist|min_pl") if case.has("Hist|min_pl") else []
    b_min = case.c("DCF|b_min")
    probs_ = []
    if mins_pl and mins_pl[-1] and not b_min and not case.c("Inputs|minority"):
        probs_.append("minority profit in the last year but no minority deduction")
    for k in ("b_pens", "b_assoc", "b_other"):
        if not _num(case.c(f"DCF|{k}")) and case.c(f"DCF|{k}") not in (None, "–", "-"):
            probs_.append(f"{k} not a number")
    add(Result("B24", "Incomplete EV-to-equity bridge", FAIL if probs_ else PASS,
               "; ".join(probs_) or f"bridge: NIBD, minorities {b_min}, associates {case.c('DCF|b_assoc')}, pensions/other filled", "03 #24"))

    sh, shd = case.c("Inputs|shares"), case.c("Inputs|shares_dil")
    last_issue = m.get("last_share_issue")
    bs_date = case.c("Inputs|bs_date")
    probs_ = []
    if shd < sh:
        probs_.append("diluted shares below basic")
    if last_issue and datetime.fromisoformat(last_issue) > bs_date and not m.get("issue_in_shares"):
        probs_.append(f"a share issue on {last_issue} after the balance sheet date: confirm the share count and net debt include it")
    add(Result("B25", "Share count and dilution", FLAG if probs_ else (PASS if last_issue is not None or "last_share_issue" in m else MISSING),
               "; ".join(probs_) or f"basic {sh}m, diluted {shd}m" + ("" if "last_share_issue" in m else "; META['last_share_issue'] not set"), "03 #25"))

    gap = (val_date - bs_date).days
    add(Result("B26", "Stale balance sheet / dates", WARN if gap > 120 else PASS, f"balance sheet {bs_date:%d %b %Y}, valuation {val_date:%d %b %Y}: {gap} days", "03 #26"))

    lev = [x for x in case.row("Model|lev") if _num(x)]
    ebit = case.row("Model|ebit_adj")
    fin = [-x for x in case.row("Model|netfin")]
    cover = min(e / f for e, f in zip(ebit, fin, strict=True) if f > 0) if any(f > 0 for f in fin) else None
    fcfe = case.row("Output|fcfe") if case.has("Output|fcfe") else None
    divs = [-x for x in case.row("Output|cf_div")] if case.has("Output|cf_div") else None
    debt_div = [y for y, fe, dv_ in zip(case.years(FC), fcfe, divs, strict=True) if dv_ > fe] if fcfe and divs else []
    run = max((sum(1 for _ in grp) for k, grp in __import__("itertools").groupby(case.years(FC), key=lambda y: y in debt_div) if k), default=0)
    d = f"peak NIBD/EBITDAaL {max(lev):.1f}x, min interest cover {cover:.1f}x" + (f"; dividends above FCFE in {', '.join(debt_div)}" if debt_div else "")
    if max(lev) > 4 or (cover is not None and cover < 2):
        add(_flag(case, "B27", "Leverage, refinancing, dividends", d + ": needs a distress/refinancing scenario", "03 #27"))
    elif run >= 2:
        add(_flag(case, "B27", "Leverage, refinancing, dividends", d + ": dividends funded by debt for 2+ years", "03 #27", warn_only=True))
    else:
        add(Result("B27", "Leverage, refinancing, dividends", PASS, d, "03 #27"))

    s_exit, exit_ = case.c("DCF|s_exit"), case.c("Drivers|exit")
    dev = s_exit / exit_ - 1
    add(Result("B28", "Exit multiple vs Gordon TV", WARN if abs(dev) > 0.25 else PASS,
               f"Gordon TV implies {s_exit:.1f}x EV/EBITDAaL vs the exit cross-check {exit_:.1f}x ({_p(dev, 0, True)})", "03 #28; 04 R16"))

    w_dcf = case.c("Inputs|w_dcf")
    conf = m.get("conflicts")
    st = PASS if w_dcf >= 0.5 and conf else (FAIL if w_dcf < 0.5 else MISSING)
    add(Result("B29", "Heuristic target / conflicts", st, f"DCF weight {_p(w_dcf, 0)}; conflicts block: {conf if conf else 'not in META'}", "03 #29; VPFF 3"))

    disc = m.get("disclosures") or {}
    need = ("author", "price_datetime", "rating_definitions", "valuation_summary", "update_frequency", "history_12m", "status")
    missing = [k for k in need if not disc.get(k)]
    add(Result("B30", "MAR / 2016/958 disclosures", PASS if not missing else MISSING,
               "all disclosure fields present" if not missing else "missing: " + ", ".join(missing), "03 #30; 04 R37-R40"))
    return R


def summary(results: list[Result]) -> dict:
    out = {}
    for r in results:
        out[r.status] = out.get(r.status, 0) + 1
    return out


def render(results: list[Result], title: str = "") -> str:
    lines = [f"CASE AUDIT {title}".rstrip()]
    for r in sorted(results, key=lambda r: (ORDER[r.status], r.id)):
        lines.append(f"  [{r.status:9s}] {r.id:4s} {r.name}: {r.detail}  ({r.source})")
        if r.reason:
            lines.append(f"              reason: {r.reason}")
    s = summary(results)
    lines.append("  " + ", ".join(f"{k} {v}" for k, v in sorted(s.items(), key=lambda kv: ORDER[kv[0]])))
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xlsx")
    ap.add_argument("map")
    ap.add_argument("data", nargs="?", help="case data module (e.g. sats_data) with an optional META dict")
    ap.add_argument("--price-now", type=float)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any FAIL or unjustified FLAG")
    a = ap.parse_args(argv)
    case = Case(a.xlsx, a.map, a.data)
    res = audit(case, a.price_now)
    if a.json:
        print(json.dumps([asdict(r) for r in res], indent=1, ensure_ascii=False))
    else:
        print(render(res, f"– {case.c('Inputs|company')}"))
    bad = any(r.status in (FAIL, FLAG) for r in res)
    return 1 if (a.strict and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
