"""What-if runs: change one input at a time in Excel and record the DCF, target price and rating (nothing is saved).

Windows with Excel. Model and map from EQR_MODEL / EQR_MAP (default: the SATS case); results in EQR_WHATIF
(default whatif_runs_sats.json – the deck's assumptions slide reads the personnel-cost run from it)."""
import json
import os

import win32com.client as w32

MB = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(MB, os.environ.get("EQR_MODEL", "sats_final.xlsx"))
OUT = os.path.join(MB, os.environ.get("EQR_WHATIF", "whatif_runs_sats.json"))
reg = json.load(open(os.path.join(MB, os.environ.get("EQR_MAP", "model_map_sats.json")), encoding="utf8"))
C = lambda sheet, key: reg["cells"][f"{sheet}|{key}"]
R = lambda sheet, key: reg["rows"][f"{sheet}|{key}"]
PERS_RUN = "Personnel ratio stays at the last actual level (all personnel costs variable)"

xl = w32.DispatchEx("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
res = {}
try:
    wb = xl.Workbooks.Open(MODEL, 0, True)
    ws = lambda n: wb.Worksheets(n)
    model = ws("Model")

    def snap(tag):
        xl.CalculateFull()
        d = ws("DCF")
        v = dict(dcf=d.Range(C("DCF", "dcf_ps")).Value, tp=d.Range(C("DCF", "tp")).Value,
                 rating=d.Range(C("DCF", "rating")).Value,
                 m33=model.Range(f"S{R('Model', 'ebit_adj_m')}").Value,
                 m30=model.Range(f"P{R('Model', 'ebit_adj_m')}").Value,
                 rev33=model.Range(f"S{R('Model', 'is_rev')}").Value,
                 status=ws("Checks").Range(C("Checks", "master")).Value)
        res[tag] = v
        print(f"{tag:70s} DCF {v['dcf']:6.1f}  TP {v['tp']:5.0f} {v['rating']:4s}  EBIT adj m 2030 {v['m30']:.1%} 2033 {v['m33']:.1%}  {v['status']}")

    def setc(sheet, key, val):
        ws(sheet).Range(C(sheet, key)).Value = val

    def setrow(sheet, key, vals, first="L"):
        r = R(sheet, key)
        cols = "LMNOPQRS"
        start = cols.index(first)
        for c, v in zip(cols[start:], vals):
            ws(sheet).Range(f"{c}{r}").Value = v

    def getrow(sheet, key):
        r = R(sheet, key)
        return [ws(sheet).Range(f"{c}{r}").Value for c in "LMNOPQRS"]

    def run(tag, changes):
        undo = []
        for kind, sheet, key, val in changes:
            if kind == "c":
                undo.append(("c", sheet, key, ws(sheet).Range(C(sheet, key)).Formula))
                setc(sheet, key, val)
            else:
                undo.append(("r", sheet, key, getrow(sheet, key)))
                setrow(sheet, key, val)
        snap(tag)
        for kind, sheet, key, val in reversed(undo):
            if kind == "c":
                rng = ws(sheet).Range(C(sheet, key))
                if val in ("", None):
                    rng.ClearContents()
                else:
                    rng.Formula = val
            else:
                setrow(sheet, key, val)

    snap("Base case")
    net = {k: getrow("Drivers", f"b_net_{k}") for k in "abc"}
    cpi = getrow("Drivers", "b_cpi")
    run("No new clubs (net openings = 0)", [("r", "Drivers", f"b_net_{k}", [0] * 8) for k in "abc"])
    run("Half the openings", [("r", "Drivers", f"b_net_{k}", [round(x / 2) for x in net[k]]) for k in "abc"])
    run("Committed pipeline only in 2027-28 (5 + 5 clubs), base case after",
        [("r", "Drivers", "b_net_a", net["a"][:1] + [5, 3] + net["a"][3:]),
         ("r", "Drivers", "b_net_b", net["b"][:1] + [0, 1] + net["b"][3:]),
         ("r", "Drivers", "b_net_c", net["c"][:1] + [0, 1] + net["c"][3:])])
    run("One more opening per country a year", [("r", "Drivers", f"b_net_{k}", [x + 1 for x in net[k]]) for k in "abc"])
    run("Price/mix -1pp a year", [("c", "Drivers", "adj_price_base", -0.01)])
    run("Price/mix -0.5pp a year", [("c", "Drivers", "adj_price_base", -0.005)])
    run("Price/mix +0.5pp a year", [("c", "Drivers", "adj_price_base", 0.005)])
    run("Like-for-like volume -1pp a year", [("c", "Drivers", "adj_vol_base", -0.01)])
    run("Cost inflation +0.5pp from 2027", [("r", "Drivers", "b_cpi", [cpi[0]] + [x + 0.005 for x in cpi[1:]])])
    run("Cost inflation -0.5pp from 2027", [("r", "Drivers", "b_cpi", [cpi[0]] + [x - 0.005 for x in cpi[1:]])])
    run("Cost inflation 4.0% also in 2026 (no FX relief)", [("r", "Drivers", "b_cpi", [0.040] + cpi[1:])])
    run("Price -0.5pp and cost inflation +0.5pp", [("c", "Drivers", "adj_price_base", -0.005),
                                                   ("r", "Drivers", "b_cpi", [cpi[0]] + [x + 0.005 for x in cpi[1:]])])
    pers_tot = ws("Hist").Range(f"K{R('Hist', 'pers_pct')}").Value          # last actual year's total cost ratios
    oth_tot = ws("Hist").Range(f"K{R('Hist', 'oth_pct')}").Value
    run(PERS_RUN, [("c", "Drivers", "pers_fixsh_in", 0.0), ("r", "Drivers", "b_pers_var", [pers_tot] * 8)])
    cogs_tot = ws("Hist").Range(f"K{R('Hist', 'cogs_pct')}").Value
    run("Gross margin stays at the last actual level", [("r", "Drivers", "b_cogs", [cogs_tot] * 8)])
    run("All costs variable (no operating leverage)", [("c", "Drivers", "pers_fixsh_in", 0.0), ("c", "Drivers", "oth_fixsh_in", 0.0),
                                                      ("r", "Drivers", "b_pers_var", [pers_tot] * 8),
                                                      ("r", "Drivers", "b_oth_var", [oth_tot] * 8)])
    run("EBIT margin -1pp in every year", [("c", "Sensitivity", "ovr_margin", -0.01)])
    run("WACC 10.0%", [("c", "WACC", "wacc_ovr", 0.100)])
    run("WACC 8.0%", [("c", "WACC", "wacc_ovr", 0.080)])
    run("Terminal growth 1.0%", [("c", "Drivers", "tg_in", 0.010)])
    run("Terminal growth 3.0%", [("c", "Drivers", "tg_in", 0.030)])
    wacc = ws("WACC").Range(C("WACC", "wacc")).Value
    run("RONIC = WACC (growth creates no value in the TV)", [("c", "Drivers", "ronic_in", round(wacc, 4))])
    run("RONIC 15%", [("c", "Drivers", "ronic_in", 0.15)])
    run("Capex per new club NOK 15m", [("r", "Drivers", "b_capex_loc", [15.0] * 8)])
    run("Maintenance capex 6% of revenue", [("r", "Drivers", "b_mcapex", [0.06] * 8)])
    run("Buybacks off", [("c", "Drivers", "bb_on_in", 0)])
    run("Leverage target 1.0x (less buybacks)", [("c", "Drivers", "lev_t_in", 1.0)])
    run("100% DCF (no peer weight)", [("c", "Inputs", "w_dcf", 1.0)])
    wb.Close(False)
finally:
    xl.Quit()
json.dump(res, open(OUT, "w", encoding="utf8"), indent=1, default=str)
print("saved", OUT)
