"""Recompute the base-case DCF independently in Python (both revenue builds) and verify the reverse DCF.

Reads the finalised model (model_final.xlsx + model_map.json) and compares:
  * revenue, capex and FCFF paths, WACC, EV and value per share (Python vs. Excel)
  * the market-implied margin shift, growth shift, WACC and terminal growth: each one, put back into the
    Python model, must reproduce today's share price.
"""
import json
import os
import statistics
import datetime as dt
import openpyxl
import case_data as ex

reg = json.load(open(os.environ.get("EQR_MAP", "model_map.json"), encoding="utf8"))
wb = openpyxl.load_workbook(os.environ.get("EQR_MODEL", "model_final.xlsx"), data_only=True)
FC = list("LMNOPQRS")


def cell(sheet, key):
    return wb[sheet][reg["cells"][f"{sheet}|{key}"]].value


def row(sheet, key, cols):
    for sh in (sheet, "Model", "Analysis", "Output"):
        if f"{sh}|{key}" in reg["rows"]:
            return [wb[sh][f"{c}{reg['rows'][f'{sh}|{key}']}"].value for c in cols]
    raise KeyError(key)


d = ex.simulate()
B, C, M = ex.BASE, ex.COST_CAPITAL, ex.MARKET
SEG = "ABC"
KEY = {"A": "a", "B": "b", "C": "c"}


def forecast(mode, dm=0.0, dg=0.0):
    """Operating forecast 2026E-2033E. dm = uniform EBIT margin shift, dg = uniform volume / like-for-like growth shift."""
    r1, r2, r3 = ex.ENGINE["ramp"]
    rev = {s: ex.SEG_REV[s][-1] for s in SEG}
    vol = {s: ex.SEG_VOL[s][-1] for s in SEG}
    loc = {s: ex.SEG_LOC[s][-1] for s in SEG}
    meq = dict(loc)
    mpl = {s: vol[s] / loc[s] for s in SEG}
    opens = {s: [0.0, 0.0, 0.0] for s in SEG}               # openings in t-3, t-2, t-1 (history = 0)
    L_prev = float(sum(loc.values()))
    avg_prev = (L_prev + sum(ex.SEG_LOC[s][-2] for s in SEG)) / 2
    pers_fix = -d["pers"][-1] * C["pers_fixsh"]
    oth_fix = -d["oth"][-1] * C["oth_fixsh"]
    lease = -d["lease_pay"][-1]
    nwc_prev = d["inv"][-1] + d["rec"][-1] + d["oca"][-1] - d["pay"][-1] - d["ocl"][-1]
    R_prev = sum(rev.values())
    o = {k: [] for k in ["rev", "ebit", "ebitdaal", "nopat", "capex", "fcff", "net_inv", "loc", "tax"]}
    for i in range(8):
        opened, L_tot, newc = 0.0, 0.0, 0.0
        for s in SEG:
            k = KEY[s]
            if mode == 2:
                net = B["net" + s][i]
                op = max(0.0, net)
                loc[s] += net
                o3, o2, o1 = opens[s]
                meq_prev = meq[s]
                meq[s] = meq[s] + min(0.0, net) + op * r1 + o1 * (r2 - r1) + o2 * (r3 - r2) + o3 * (1 - r3)
                if meq_prev:
                    newc += rev[s] * (meq[s] / meq_prev - 1)        # revenue growth from new locations (Model: g_newc)
                opens[s] = [o2, o1, op]
                mpl[s] *= 1 + B["lfl" + s][i] + dg
                v = meq[s] * mpl[s]
                opened += op
            else:
                v = vol[s] * (1 + B["vol" + s][i] + dg)
            L_tot += loc[s]
            rev[s] = rev[s] * v / vol[s] * (1 + B["price" + s][i])
            vol[s] = v
        R = sum(rev.values())
        cpi = B["cpi"][i]
        avg = (L_prev + L_tot) / 2
        loc_g = avg / avg_prev - 1
        grow = newc / R_prev if ex.ENGINE.get("lease_scale") == "new_revenue" else loc_g   # rent and the fixed base: store count or new-store revenue
        fix_real = (1 - C["central"]) * grow if mode == 2 else B["fix_real"][i]
        pers_fix *= (1 + cpi) * (1 + fix_real)
        oth_fix *= (1 + cpi) * (1 + fix_real)
        lease = lease * (1 + cpi) * (1 + grow) if mode == 2 else R * B["lease"][i]
        costs = R * B["cogs"][i] + pers_fix + R * B["pers_var"][i] + oth_fix + R * (B["oth_var"][i] - dm) + lease
        eal = R - costs
        da = R * B["da"][i]
        ebit = eal - da
        nop = ebit * (1 - B["tax"][i])
        nwc = R * B["nwc"][i]
        growth = opened * B["capex_loc"][i] if mode == 2 else max(0.0, R - R_prev) / B["s2c"][i]
        capex = R * B["mcapex"][i] + growth
        for key, v in [("rev", R), ("ebit", ebit), ("ebitdaal", eal), ("nopat", nop), ("capex", capex),
                       ("fcff", nop + da - capex - (nwc - nwc_prev)), ("net_inv", capex - da + (nwc - nwc_prev)),
                       ("loc", L_tot), ("tax", B["tax"][i])]:
            o[key].append(v)
        nwc_prev, R_prev, L_prev, avg_prev = nwc, R, L_tot, avg
    return o


def wacc_ke():
    bu = statistics.median([(0.67 * p[10] + 0.33) / (1 + (1 - p[12]) * p[11]) for p in ex.PEERS])
    w = ex.WACC_INPUTS
    dv = w["target_dv"]
    bl = bu * (1 + (1 - ex.TERMINAL["tax"]) * dv / (1 - dv))
    ke = w["rf"] + bl * w["erp"] + w["size"] + w["specific"]
    return (1 - dv) * ke + dv * (w["rf"] + w["spread"]) * (1 - ex.TERMINAL["tax"]), ke


def dcf(o, wacc=None, g=None):
    wacc = wacc if wacc is not None else wacc_ke()[0]
    g = g if g is not None else ex.TERMINAL["tg"]
    stub = float(wb["Inputs"][reg["cells"]["Inputs|stub"]].value)      # share of the first forecast year remaining (from the model)
    per = [stub / 2 if n == 1 else stub + n - 1.5 for n in range(1, 9)]
    pv = sum(o["fcff"][i] * (stub if i == 0 else 1) / (1 + wacc) ** per[i] for i in range(8))
    nop_ty = o["rev"][-1] * (1 + g) * (o["ebit"][-1] / o["rev"][-1]) * (1 - ex.TERMINAL["tax"])
    tv = nop_ty * (1 - g / ex.TERMINAL["ronic"]) / (wacc - g)
    pvtv = tv / (1 + wacc) ** per[-1]
    eq = pv + pvtv - (M["debt_q"] - M["cash_q"]) - M["minority_q"] + M["associates_q"] - M["pension_q"] + M["other_adj"]
    return dict(pv=pv, pvtv=pvtv, ev=pv + pvtv, ps=eq / (M["shares"] + M["dilutive"]))


mode = cell("Inputs", "rev_mode")
o = forecast(mode)
w, ke = wacc_ke()
v = dcf(o)
print(f"revenue build: {'locations' if mode == 2 else 'segments'}")
print(f"python : WACC {w:.5%}  Ke {ke:.5%}  PV {v['pv']:,.1f}  PV(TV) {v['pvtv']:,.1f}  EV {v['ev']:,.1f}  value/share {v['ps']:.3f}")
print(f"excel  : WACC {cell('WACC', 'wacc'):.5%}  Ke {cell('WACC', 'ke'):.5%}  PV {cell('DCF', 'sum_pv'):,.1f}  "
      f"PV(TV) {cell('DCF', 'pv_tv'):,.1f}  EV {cell('DCF', 'ev'):,.1f}  value/share {cell('DCF', 'dcf_ps'):.3f}")
xr, xf, xc = row("Model", "is_rev", FC), row("DCF", "fcff", FC), row("Model", "capex", FC)
print("max diff  revenue", max(abs(a - b) for a, b in zip(o["rev"], xr)),
      " fcff", max(abs(a - b) for a, b in zip(o["fcff"], xf)),
      " capex", max(abs(a + b) for a, b in zip(o["capex"], xc)))
print("revenue   ", [round(x) for x in xr])
print("locations ", [round(x) for x in row("Model", "loc", FC)])
print("g new/lfl/px", [(round(a, 3), round(b, 3), round(c, 3)) for a, b, c in
                       zip(row("Model", "g_newc", FC), row("Model", "g_lflc", FC), row("Model", "g_pxc", FC))])
print("ebit adj m", [round(x, 4) for x in row("Model", "ebit_adj_m", FC)])
print("capex     ", [round(-x) for x in xc])
print("fcff      ", [round(x) for x in xf])
print("roic      ", [round(x, 3) for x in row("Model", "roic", FC)])
print("eps       ", [round(x, 2) if isinstance(x, (int, float)) else None for x in row("Model", "eps", list("HIJK") + FC)])
print("sanity    : return on new capital", round(cell("DCF", "s_ronic_fc"), 3), " benchmark", round(cell("DCF", "s_ronic_ref"), 3),
      " ratio", round(cell("DCF", "s_ronic_ratio"), 2))
print("rating    :", cell("DCF", "rating"), " TP", cell("DCF", "tp"), " TSR", round(cell("DCF", "tp_tr"), 4),
      " excess vs Ke", round(cell("DCF", "tp_excess"), 4), " fair", round(cell("DCF", "tp_fair"), 2))

# ---- reverse DCF: every market-implied value must reproduce the share price in the independent Python model
price = cell("Inputs", "price")
dm, dg, iw, ig = (cell("Reverse_DCF", k) for k in ("rd_dm", "rd_dg", "rd_wacc", "rd_g"))
print(f"\nreverse DCF (share price {price:.2f}):")
print(f"  margin shift {dm * 100:+.3f}pp -> python value {dcf(forecast(mode, dm=dm))['ps']:.4f}   "
      f"(implied EBIT margin {cell('Reverse_DCF', 'rd_m_last'):.2%} vs. ours {cell('Reverse_DCF', 'rd_m_last_ours'):.2%})")
print(f"  growth shift {dg * 100:+.3f}pp -> python value {dcf(forecast(mode, dg=dg))['ps']:.4f}   "
      f"(implied revenue CAGR {cell('Reverse_DCF', 'rd_cagr'):.2%} vs. ours {cell('Reverse_DCF', 'rd_cagr_ours'):.2%}; interpolated)")
print(f"  WACC {iw:.4%}          -> python value {dcf(o, wacc=iw)['ps']:.4f}")
print(f"  terminal growth {ig:.4%} -> python value {dcf(o, g=ig)['ps']:.4f}")
