"""Build the Equity Research DCF template (openpyxl). Excel finalisation happens in excel_finalize.py."""
import json
import os
import sys
import openpyxl
from openpyxl.workbook.defined_name import DefinedName
from mb_core import ROWS, CELLS, S
import mb_inputs
import mb_model
import mb_fin
import mb_val
import mb_out
import mb_nav
import mb_market

OUT = sys.argv[1] if len(sys.argv) > 1 else "model_raw.xlsx"

ORDER = ["Cover", "Guide", "Inputs", "Hist", "Drivers", "Model", "WACC", "DCF", "Sensitivity",
         "Comps", "Football", "Dashboard", "Deck_Feed", "Checks"]
TABS = {"Cover": "003255", "Guide": "003255", "Inputs": "FFC000", "Hist": "FFC000", "Drivers": "FFC000",
        "Model": "7F7F7F", "WACC": "7F7F7F", "DCF": "7F7F7F", "Sensitivity": "81B0C0", "Comps": "81B0C0",
        "Football": "81B0C0", "Dashboard": "407061", "Deck_Feed": "407061", "Checks": "C00000"}


def main():
    # layout pass (row numbers / scalar cells for every sheet)
    mb_inputs.INP.layout()
    mb_inputs.HIST.layout()
    mb_inputs.DRV_BASE.layout()
    mb_inputs.DRV_LIVE.layout()
    mb_model.MODEL.layout()
    mb_fin.OUTPUT.layout()
    mb_fin.ANALYSIS.layout()
    mb_model._dcf_spec()
    mb_model._wacc_spec()
    mb_market.layout()

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name in mb_nav.ORDER:
        ws = wb.create_sheet(name)
        ws.sheet_properties.tabColor = mb_nav.TABS[name]

    # write pass (dependency order)
    mb_inputs.write_inputs(wb)
    mb_inputs.write_hist(wb)
    mb_inputs.write_drivers(wb)
    mb_model.write_model(wb)
    mb_fin.write_output(wb)
    mb_fin.write_analysis(wb)
    mb_model.write_wacc(wb)
    mb_model.write_dcf(wb)
    mb_val.write_sens(wb)
    mb_val.write_comps(wb)
    mb_val.write_football(wb)
    mb_market.write_all(wb)
    mb_out.write_checks(wb)
    mb_out.write_dashboard(wb)
    mb_out.write_feed(wb)
    mb_nav.write_cover(wb)
    mb_nav.write_dividers(wb)
    mb_out.chart_football(wb["Football"], "B22")
    mb_out.write_guide(wb)

    names = {
        "Scenario": ("Inputs", "scenario"), "SharePrice": ("Inputs", "price"), "WACC_used": ("WACC", "wacc"),
        "CostOfEquity": ("WACC", "ke"), "TerminalGrowth": ("Drivers", "tg"), "EV_DCF": ("DCF", "ev"),
        "DCF_ValuePerShare": ("DCF", "dcf_ps"), "TargetPrice": ("DCF", "tp"), "Recommendation": ("DCF", "rating"),
        "PeerValuePerShare": ("Comps", "peer_val"), "ModelStatus": ("Checks", "master"),
        "RevenueMode": ("Inputs", "rev_mode"), "ImpliedMargin": ("Reverse_DCF", "rd_m_last"),
    }
    for nm, (sh, key) in names.items():
        wb.defined_names[nm] = DefinedName(nm, attr_text=S(sh, key))

    for ws in wb.worksheets:
        ws.page_setup.orientation = "landscape"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_options.horizontalCentered = True
        ws.page_margins.left = ws.page_margins.right = 0.4
    wb.active = 0
    wb.calculation.fullCalcOnLoad = True
    wb.save(OUT)

    reg = {"rows": {f"{s}|{k}": v for (s, k), v in ROWS.items()},
           "cells": {f"{s}|{k}": v for (s, k), v in CELLS.items()},
           "sens": mb_val.SENS, "t4": mb_val.T4_OUT, "comps": mb_val.CR}
    with open(os.environ.get("EQR_MAP", "model_map.json"), "w", encoding="utf8") as f:
        json.dump(reg, f, indent=1)
    print("saved", OUT, "rows", len(ROWS), "cells", len(CELLS))


if __name__ == "__main__":
    main()
