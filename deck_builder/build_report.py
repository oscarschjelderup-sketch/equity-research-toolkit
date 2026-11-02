"""Build the full research report (HTML and PDF) from the saved workbook and the case modules.

    EQR_CASE=sats_data python build_report.py --model ../examples/SATS/SATS_ASA_DCF_Model.xlsx \
        --map ../model_builder/model_map_sats.json --out-dir ../examples/SATS/report

Before anything is rendered the build gate runs (report/rb_gate.py): the Checks sheet, verify_dcf.py, the case audit and
case gate, and stress_test.py (Excel, Windows). If any check fails the report is not built and the script exits 2.
`--skip-gate` is for CI and layout work only – the HTML then carries a banner saying the gate was skipped.
"""
import argparse
import datetime as dt
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "report"))
sys.path.insert(0, str(HERE.parent / "model_builder"))

import rb_gate  # noqa: E402
import rb_pdf  # noqa: E402
import rb_sections as S  # noqa: E402
from rb_core import css, esc  # noqa: E402
from rb_data import Report, fmt_date  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--model", default=os.path.join(HERE, "..", "Equity_Research_DCF_Toolkit.xlsx"))
ap.add_argument("--map", default=os.path.join(HERE, "model_map.json"))
ap.add_argument("--case", default=os.environ.get("EQR_CASE", "example_data"), help="data module, e.g. sats_data (also read from EQR_CASE)")
ap.add_argument("--out-dir", default=None, help="output folder (default ../examples/<TICKER>/report)")
ap.add_argument("--name", default=None, help="file stem (default <TICKER>_Research_Report_<date>)")
ap.add_argument("--date", default=None, help="publication date YYYY-MM-DD (default today)")
ap.add_argument("--html-only", action="store_true", help="do not print to PDF")
ap.add_argument("--skip-gate", action="store_true", help="skip verify_dcf.py and stress_test.py (CI / layout work only)")
ap.add_argument("--skip-stress", action="store_true", help="skip stress_test.py only (no Excel)")
ap.add_argument("--refresh-prices", action="store_true", help="fetch the share and index prices from Yahoo Finance into prices.json")
ap.add_argument("--no-store", action="store_true", help="do not write the estimates snapshot (dry run)")
ap.add_argument("--no-publish", action="store_true", help="do not copy the PDF and estimates to the oslo-quant home (cases/reports_pdf/<TICKER>/)")
a = ap.parse_args()

today = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
tmp_out = a.out_dir or None
r = Report(a.model, a.map, a.case, tmp_out or str(HERE / "_tmp_report"), today=today)
if not tmp_out:
    r.out = HERE.parent / "examples" / str(r.ticker) / "report"
    r.out.mkdir(parents=True, exist_ok=True)
    try:
        (HERE / "_tmp_report").rmdir()
    except OSError:
        pass
if a.refresh_prices:
    px = r.fetch_prices()
    print(f"prices: {len(px['dates'])} days for {px['symbol']} and {px['index']} -> {r.out / 'prices.json'}")

# ---- gate
gate = rb_gate.evaluate(r, skip_stress=a.skip_stress or a.skip_gate, skip_verify=a.skip_gate)
print(rb_gate.render_text(gate))
if not gate["ok"]:
    print("\nThe report is NOT built: fix the model first.", file=sys.stderr)
    sys.exit(2)

# ---- sections
prev = r.previous_estimates()
titles = [(1, "Investment case overview"), (2, "Company overview"), (3, "Quarter preview"), (4, "Deep dives – the themes that decide the case"),
          (5, "Competition per market"), (6, "Macro – the drivers that reach the P&L"), (7, "Estimate revisions"), (8, "Valuation"),
          (9, "Financial statements"), (10, "What we do not know"), (11, "Disclosures, sources and checks")]
banner = ""
if a.skip_gate:
    banner = "<div class='gap'><b>Build gate skipped</b> – this file was built with --skip-gate for layout or CI purposes; it is not a verified report.</div>"
body = [S.front_page(r, prev), S.investment_case(r).replace("<section id='case' class='sec'>", "<section id='case' class='sec'>" + S.contents(titles) + banner, 1),
        S.company_overview(r), S.quarter_preview(r), S.deep_dives(r), S.competition(r), S.macro(r), S.revisions(r, prev), S.valuation(r),
        S.financials(r), S.unknowns(r, gate), S.disclosures(r, gate)]
title = f"{r.company} – research report – {today.isoformat()}"
html = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{esc(title)}</title><style>{css(f'Equity Research Toolkit | {r.company} ({r.ticker})', fmt_date(today))}</style></head>"
        f"<body>{''.join(body)}</body></html>")
stem = a.name or f"{r.ticker}_Research_Report_{today.isoformat()}"
html_path = r.out / f"{stem}.html"
html_path.write_text(html, encoding="utf-8")
print(f"html: {html_path} ({html_path.stat().st_size / 1e6:.1f} MB)")
if not a.no_store:
    print(f"estimates stored: {r.save_estimates()}")
if not a.html_only:
    pdf_path = rb_pdf.to_pdf(html_path, r.out / f"{stem}.pdf")
    n = rb_pdf.page_count(pdf_path)
    print(f"pdf: {pdf_path} – {n} pages")
    if n is not None and not (25 <= n <= 40):
        print(f"WARNING: {n} pages is outside the 25–40 page target", file=sys.stderr)
    if not a.no_publish and not a.no_store:
        # the dashboard (oslo-quant) lists reports from its private home: ~/osloquant-home/cases/reports_pdf/<TICKER>/
        import shutil
        home = Path(os.environ.get("OSLOQUANT_HOME") or (Path.home() / "osloquant-home"))
        if home.exists():
            dest = home / "cases" / "reports_pdf" / str(r.ticker).upper()
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(pdf_path, dest / pdf_path.name)
            shutil.copyfile(r.out / f"estimates_{today.isoformat()}.json", dest / f"estimates_{today.isoformat()}.json")
            import json as _json
            (dest / f"meta_{today.isoformat()}.json").write_text(_json.dumps({"kind": r.rep.get("kind", ""), "title": r.rep.get("title", ""), "pages": n,
                                                                              "gate_ok": bool(gate["ok"]), "built": today.isoformat(),
                                                                              "source": "Equity Research Toolkit build_report.py"}, indent=1, ensure_ascii=False), encoding="utf-8")
            print(f"published to the dashboard home: {dest}")
