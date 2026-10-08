"""Sum-of-the-parts of the DCF: what the existing estate is worth and what each roll-out block adds (nothing is saved).

Windows with Excel. The model is opened read-only and rebuilt step by step: (1) no new locations in any segment and, if
the case module defines SOTP['estate'], expansion capex and D&A reset to a no-expansion level; (2) expansion capex back;
(3)-(5) the openings of segment A, B and C back (= the base case). Each step records the DCF value per share, EV, equity
value, final-year revenue, EBIT adj. margin and locations, and the peak leverage. Model/map from EQR_MODEL / EQR_MAP, the
case module from EQR_CASE, output EQR_SOTP (default sotp_<case>.json – the deck's SOTP slide reads it).

Case module (optional):
    SOTP = dict(estate=dict(mcapex=[...8 values], da=[...8 values]),      # no-expansion level of these Drivers rows
                capex_label="New central warehouse", order="abc",
                labels={"a": "Sport Outlet openings", "b": "Kids Outlet roll-out", "c": "Poland"})
"""
import importlib
import json
import os
import sys

import win32com.client as w32

MB = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MB)
CASE = os.environ.get("EQR_CASE", "example_data")
MODEL = os.path.join(MB, os.environ.get("EQR_MODEL", "model_final.xlsx"))
OUT = os.path.join(MB, os.environ.get("EQR_SOTP", f"sotp_{CASE.replace('_data', '')}.json"))
reg = json.load(open(os.path.join(MB, os.environ.get("EQR_MAP", "model_map.json")), encoding="utf8"))
C = lambda sheet, key: reg["cells"][f"{sheet}|{key}"]
R = lambda sheet, key: reg["rows"][f"{sheet}|{key}"]
cfg = getattr(importlib.import_module(CASE), "SOTP", None) or {}
order = cfg.get("order", "abc")
labels = cfg.get("labels", {})
FCOLS = "LMNOPQRS"

xl = w32.DispatchEx("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
steps = []
out = {}
try:
    wb = xl.Workbooks.Open(MODEL, 0, True)
    ws = lambda n: wb.Worksheets(n)
    model, dcf = ws("Model"), ws("DCF")
    seg_name = {k: ws("Inputs").Range(C("Inputs", f"seg_{k}")).Value for k in "abc"}

    def getrow(sheet, key):
        r = R(sheet, key)
        return [ws(sheet).Range(f"{c}{r}").Value for c in FCOLS]

    def setrow(sheet, key, vals):
        r = R(sheet, key)
        for c, v in zip(FCOLS, vals):
            ws(sheet).Range(f"{c}{r}").Value = v

    def snap(tag, kind, seg, stores=0.0):
        xl.CalculateFull()
        lev = [v for v in getrow("Model", "lev") if isinstance(v, (int, float))]
        v = dict(tag=tag, kind=kind, seg=seg, stores=stores,
                 dcf=dcf.Range(C("DCF", "dcf_ps")).Value, ev=dcf.Range(C("DCF", "ev")).Value, eq=dcf.Range(C("DCF", "eq")).Value,
                 rev_last=model.Range(f"S{R('Model', 'is_rev')}").Value,
                 ebit_m_last=model.Range(f"S{R('Model', 'ebit_adj_m')}").Value,
                 loc_last=model.Range(f"S{R('Model', 'loc')}").Value, lev_max=max(lev) if lev else None,
                 status=ws("Checks").Range(C("Checks", "master")).Value)
        steps.append(v)
        print(f"{tag:40s} DCF {v['dcf']:6.1f}  EV {v['ev']:7,.0f}  rev {v['rev_last']:6,.0f}  EBIT adj m {v['ebit_m_last']:.1%}  "
              f"loc {v['loc_last']:.0f}  lev {v['lev_max']:.1f}x  {v['status']}")

    base_net = {k: getrow("Drivers", f"b_net_{k}") for k in "abc"}
    est = cfg.get("estate") or {}
    base_rows = {key: getrow("Drivers", f"b_{key}") for key in est}
    for k in "abc":
        setrow("Drivers", f"b_net_{k}", [0] * 8)
    for key, vals in est.items():
        setrow("Drivers", f"b_{key}", list(vals))
    snap("Existing estate", "total", "estate")
    if est:
        for key in est:
            setrow("Drivers", f"b_{key}", base_rows[key])
        snap(cfg.get("capex_label", "Expansion capex"), "delta", "capex")
    for k in order:
        setrow("Drivers", f"b_net_{k}", base_net[k])
        n = sum(v for v in base_net[k] if isinstance(v, (int, float)) and v > 0)
        snap(labels.get(k, f"{seg_name[k]} openings"), "delta", k, stores=n)
    out = dict(case=CASE, price=ws("Inputs").Range(C("Inputs", "price")).Value, shares=dcf.Range(C("DCF", "shares")).Value,
               last_year=model.Range("S5").Value, steps=steps)
    wb.Close(False)
finally:
    xl.Quit()
json.dump(out, open(OUT, "w", encoding="utf8"), indent=1, default=str)
print("saved", OUT)
