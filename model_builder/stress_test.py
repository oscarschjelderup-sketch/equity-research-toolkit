"""Flip model switches in Excel (without saving) and confirm checks stay clean and outputs react sensibly."""
import json
import os
import win32com.client as w32

reg = json.load(open(os.environ.get("EQR_MAP", "model_map.json"), encoding="utf8"))
C = lambda sheet, key: reg["cells"][f"{sheet}|{key}"]
xl = w32.DispatchEx("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
try:
    wb = xl.Workbooks.Open(os.path.abspath(os.environ.get("EQR_MODEL", "model_final.xlsx")), 0, True)
    inp, dcf, chk, sens = (wb.Worksheets(n) for n in ("Inputs", "DCF", "Checks", "Sensitivity"))

    def snap(tag):
        xl.CalculateFull()
        vals = dict(dcf=dcf.Range(C("DCF", "dcf_ps")).Value, tp=dcf.Range(C("DCF", "tp")).Value,
                    rating=dcf.Range(C("DCF", "rating")).Value, ctr=sens.Range(C("Sensitivity", "center1")).Value,
                    status=chk.Range(C("Checks", "master")).Value)
        errs = [chk.Range(f"C{r}").Value for r in range(7, 40) if chk.Range(f"E{r}").Value == "ERROR"]
        warns = [chk.Range(f"B{r}").Value for r in range(7, 40) if chk.Range(f"E{r}").Value == "WARNING"]
        print(f"{tag:38s} DCF {vals['dcf']:7.2f}  centre {vals['ctr']:7.2f}  TP {vals['tp']:6.1f}  "
              f"{vals['rating']:4s}  {vals['status']}  {errs if errs else ''}"
              + (f"  warnings: check {', '.join(str(int(w)) for w in warns)}" if warns else ""))
        return vals

    base = snap("Base (as delivered)")
    # round trips: put each market-implied value back into the model – the DCF must equal the share price
    rd = wb.Worksheets("Reverse_DCF")
    price = inp.Range(C("Inputs", "price")).Value
    # base values of the inputs the tests change – restored from the model, not hard-coded
    vd0 = inp.Range(C("Inputs", "val_date")).Value
    vd0 = f"{vd0.year:04d}-{vd0.month:02d}-{vd0.day:02d}"
    pl0, py0 = inp.Range(C("Inputs", "peer_lease")).Value, inp.Range(C("Inputs", "peer_year")).Value
    capl0 = wb.Worksheets("Drivers").Range(f"L{reg['rows']['Drivers|b_capex_loc']}").Value
    hist = wb.Worksheets("Hist")
    pers_tot = hist.Range(f"K{reg['rows']['Hist|pers_pct']}").Value
    oth_tot = hist.Range(f"K{reg['rows']['Hist|oth_pct']}").Value
    trips = [("margin shift -> EBITDA margin override", "Sensitivity", "ovr_margin", rd.Range(C("Reverse_DCF", "rd_dm")).Value),
             ("growth shift -> growth override", "Sensitivity", "ovr_growth", rd.Range(C("Reverse_DCF", "rd_dg")).Value),
             ("WACC -> WACC override", "WACC", "wacc_ovr", rd.Range(C("Reverse_DCF", "rd_wacc")).Value)]
    for tag, sheet, key, v in trips:
        cell = wb.Worksheets(sheet).Range(C(sheet, key))
        cell.Value = v
        xl.CalculateFull()
        print(f"Round trip: {tag:40s} value {v:.5f}  DCF {dcf.Range(C('DCF', 'dcf_ps')).Value:8.3f}  share price {price:.2f}")
        cell.ClearContents()
    g_in = wb.Worksheets("Drivers").Range(C("Drivers", "tg_in"))
    g0 = g_in.Value
    g_in.Value = rd.Range(C("Reverse_DCF", "rd_g")).Value
    xl.CalculateFull()
    print(f"Round trip: {'terminal growth -> Drivers D':40s} value {g_in.Value:.5f}  DCF {dcf.Range(C('DCF', 'dcf_ps')).Value:8.3f}  "
          f"share price {price:.2f}")
    g_in.Value = g0
    xl.CalculateFull()
    tests = [
        ("Scenario = Bear", [("Inputs", "scenario", "Bear")]),
        ("Scenario = Bull", [("Inputs", "scenario", "Bull")]),
        ("Revenue mode 1 (segments)", [("Inputs", "scenario", "Base"), ("Inputs", "rev_mode", 1)]),
        ("Mid-year off", [("Inputs", "rev_mode", 2), ("Inputs", "midyear", 0)]),
        ("Terminal FCFF method 2", [("Inputs", "midyear", 1), ("Inputs", "tv_method", 2)]),
        ("50/50 Gordon / exit multiple", [("Inputs", "tv_method", 1), ("Inputs", "w_gordon", 0.5)]),
        ("Peer basis ex leases, FY1", [("Inputs", "w_gordon", 1.0), ("Inputs", "peer_lease", 0), ("Inputs", "peer_year", 1)]),
        ("No 12m roll-forward, 100% DCF", [("Inputs", "peer_lease", pl0), ("Inputs", "peer_year", py0), ("Inputs", "roll12", 0),
                                           ("Inputs", "w_dcf", 1.0)]),
        ("WACC override 10%", [("Inputs", "roll12", 1), ("Inputs", "w_dcf", 0.7), ("WACC", "wacc_ovr", 0.10)]),
        ("Valuation date 01.03.2026", [("WACC", "wacc_ovr", None), ("Inputs", "val_date", "2026-03-01")]),
        ("Share price +25%", [("Inputs", "val_date", vd0), ("Inputs", "price", round(price * 1.25, 2))]),
        ("WACC on modelled capital structure", [("Inputs", "price", price), ("WACC", "cs_mode", 2)]),
        ("Buybacks off (cash builds up)", [("WACC", "cs_mode", 1), ("Drivers", "bb_on_in", 0)]),
        ("Sales-to-capital 1.0x (capital-heavy growth)", [("Drivers", "bb_on_in", 1), ("Drivers", "row:b_s2c", 1.0)]),
        ("Capex per new location +50%", [("Drivers", "row:b_capex_loc", round(capl0 * 1.5, 1))]),
        ("Fixed cost shares 0% (all costs variable)", [("Drivers", "row:b_s2c", 2.0), ("Drivers", "pers_fixsh_in", 0.0),
                                                       ("Drivers", "oth_fixsh_in", 0.0), ("Drivers", "row:b_pers_var", round(pers_tot, 4)),
                                                       ("Drivers", "row:b_oth_var", round(oth_tot, 4))]),
    ]
    for tag, changes in tests:
        for sheet, key, v in changes:
            if key.startswith("row:"):
                rr = reg["rows"][f"{sheet}|{key[4:]}"]
                rng = wb.Worksheets(sheet).Range(f"L{rr}:S{rr}")
            else:
                rng = wb.Worksheets(sheet).Range(C(sheet, key))
            if v is None:
                rng.ClearContents()
            elif isinstance(v, str) and v[:2] == "20":
                rng.Formula = f"=DATE({v[:4]},{int(v[5:7])},{int(v[8:10])})"
            else:
                rng.Value = v
        snap(tag)
    wb.Close(False)
finally:
    xl.Quit()
