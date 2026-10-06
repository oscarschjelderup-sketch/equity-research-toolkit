"""Open the openpyxl-built model in Excel, add data tables, recalculate, scan for errors, save, export PDF."""
import json
import os
import sys
import time
import pythoncom
import win32com.client as w32
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


src = os.path.abspath(sys.argv[1])
dst = os.path.abspath(sys.argv[2])
pdf = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else None
reg = json.load(open("model_map.json", encoding="utf8"))

xl = w32.DispatchEx("Excel.Application")
xl.Visible = False
xl.DisplayAlerts = False
xl.AskToUpdateLinks = False
try:
    log("open")
    wb = xl.Workbooks.Open(src, 0, False, None, None, None, True)
    xl.Calculation = -4105                    # automatic (incl. data tables)
    ws = wb.Worksheets("Sensitivity")
    s = reg["sens"]
    h, (a0, a1) = s["t3_hdr"], s["t3_rows"]
    log("table 3")
    ws.Range(f"C{h}:H{a1}").Table(ws.Range("D6"), ws.Range("D5"))
    frm, (b0, b1) = s["t4_frm"], s["t4_rows"]
    last = reg["t4"][-1][0]
    log("table 4")
    ws.Range(f"C{frm}:{last}{b1}").Table(pythoncom.Empty, ws.Range("D4"))   # positional: works with and without the makepy cache
    f5, (e0, e1) = s["t5_frm"], s["t5_rows"]
    log("table 5")
    ws.Range(f"C{f5}:F{e1}").Table(pythoncom.Empty, ws.Range("D5"))
    log("calc")
    xl.CalculateFull()

    report = {}
    for sh in wb.Worksheets:
        try:
            rng = sh.UsedRange.SpecialCells(-4123, 16)     # formulas returning errors
            report[sh.Name] = [c.Address for c in rng][:40]
        except Exception:
            pass
    log("scan")
    print("ERRORS:", json.dumps(report) if report else "none")

    def val(sheet, key):
        return wb.Worksheets(sheet).Range(reg["cells"][f"{sheet}|{key}"]).Value

    for sheet, key in [("DCF", "ev"), ("DCF", "dcf_ps"), ("DCF", "tv_share"), ("DCF", "s_exit"), ("DCF", "s_roic"),
                       ("Comps", "peer_val"), ("DCF", "tp_fair"), ("DCF", "tp"), ("DCF", "tp_up"), ("DCF", "tp_tr"),
                       ("DCF", "rating"), ("WACC", "wacc"), ("WACC", "ke"), ("WACC", "bl"), ("Checks", "master"),
                       ("Sensitivity", "pw_dcf_ps"), ("Sensitivity", "center1"),
                       ("Reverse_DCF", "rd_m_last"), ("Reverse_DCF", "rd_m_last_ours"), ("Reverse_DCF", "rd_dm"),
                       ("Reverse_DCF", "rd_dm_check"), ("Reverse_DCF", "rd_cagr"), ("Reverse_DCF", "rd_cagr_ours"),
                       ("Reverse_DCF", "rd_m_at_g"), ("Reverse_DCF", "rd_dg"), ("Reverse_DCF", "rd_wacc"), ("Reverse_DCF", "rd_g"),
                       ("Consensus", "diff_ebit_1"), ("Consensus", "diff_ebit_2"), ("Consensus", "diff_ebit_3"),
                       ("Thesis", "n_broken"), ("Thesis", "n_watch"), ("Thesis", "n_incons")]:
        print(f"  {sheet}.{key} = {val(sheet, key)}")
    sc = wb.Worksheets("Sensitivity")
    print("  table3:", [[round(sc.Cells(r, c).Value or 0, 1) for c in range(4, 9)] for r in range(a0, a1 + 1)])
    print("  scenario rows:", [[sc.Range(f"{col}{r}").Value for col in "DEFGHIJKLMN"] for r in range(b0, b1 + 1)])
    ck = wb.Worksheets("Checks")
    for r in range(7, 40):
        v = ck.Range(f"C{r}").Value
        if v:
            print(f"  check {r}: {v} | {ck.Range(f'D{r}').Text} | {ck.Range(f'E{r}').Value}")

    dash = wb.Worksheets("Dashboard")
    for i in range(1, dash.ChartObjects().Count + 1):
        ch = dash.ChartObjects(i).Chart
        if ch.SeriesCollection().Count == 1 and ch.SeriesCollection(1).Points().Count == 3:
            dl = ch.SeriesCollection(1).DataLabels()
            dl.NumberFormatLinked = False
            dl.NumberFormat = "0"
            log("scenario chart labels formatted")
    wb.Worksheets("Cover").Activate()
    wb.Worksheets("Cover").Range("A1").Select()
    if os.path.exists(dst):
        os.remove(dst)
    wb.SaveAs(dst, 51)
    log("saved xlsx")
    if pdf:
        wb.ExportAsFixedFormat(0, pdf)
        log("pdf")
    wb.Close(False)
finally:
    xl.Quit()
print("saved", dst)
