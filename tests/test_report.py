"""The research report builds from the committed workbooks, every exhibit carries a source and a date, estimates are
marked, missing data is printed as "not available", the estimates store feeds the revisions section, and the build gate
refuses a failing model. The PDF page count is checked only where a Chromium browser exists (locally; CI runs HTML)."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MB, DB = ROOT / "model_builder", ROOT / "deck_builder"
SATS_XLSX = ROOT / "examples" / "SATS" / "SATS_ASA_DCF_Model.xlsx"
EXAMPLE_XLSX = ROOT / "Equity_Research_DCF_Toolkit.xlsx"
SECTIONS = ["front", "case", "company", "quarter", "deep", "competition", "macro", "revisions", "valuation", "financials", "unknowns", "disclosures"]


def build(out, case, xlsx, cmap, date, extra=()):
    args = [sys.executable, "build_report.py", "--model", str(xlsx), "--map", str(MB / cmap), "--out-dir", str(out), "--skip-gate", "--html-only",
            "--date", date, *extra]
    res = subprocess.run(args, cwd=DB, env={**os.environ, "EQR_CASE": case, "PYTHONIOENCODING": "utf-8"}, capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + res.stderr
    html = next(out.glob(f"*_{date}.html")).read_text(encoding="utf-8")
    return html, res.stdout


def test_example_report_fills_every_section(tmp_path):
    html, out = build(tmp_path, "example_data", EXAMPLE_XLSX, "model_map.json", "2026-11-02")
    for sid in SECTIONS:
        assert f"id='{sid}'" in html, sid
    # every exhibit has a source line with a date; no exhibit is left without one
    figs = re.findall(r"<figure class='ex[^>]*>(.*?)</figure>", html, flags=re.S)
    assert len(figs) > 25
    for f in figs:
        assert "Source: " in f and "Data as of " in f, f[:120]
    assert "class='est'" in html                     # estimates marked EST
    assert not re.search(r">\s*nan\s*<", html, flags=re.I)  # no NaN leaked into a cell
    assert "not available" in html                  # missing consensus lines are stated, never estimated
    assert "not investment research" in html         # the front-page line
    assert "Build gate skipped" in html              # --skip-gate is visible on the page
    # the fictional case fills the optional blocks, so no placeholder should remain for the main sections
    for gap in ("Deep dives not written", "Competition tables not collected", "Macro block not collected", "Quarterly data not collected", "SWOT not written"):
        assert gap not in html, gap


def test_sats_report_builds_and_stores_estimates(tmp_path):
    html, out = build(tmp_path, "sats_data", SATS_XLSX, "model_map_sats.json", "2026-11-02")
    assert "SATS ASA" in html and "id='valuation'" in html
    est = json.loads(next(tmp_path.glob("estimates_2026-11-02.json")).read_text(encoding="utf-8"))
    assert est["rating"] == "BUY" and est["tp"] == 58 and len(est["rows"]["eps"]) == 8
    assert "First report" in html
    # a later build sees the stored estimates and renders the revisions table
    html2, _ = build(tmp_path, "sats_data", SATS_XLSX, "model_map_sats.json", "2026-12-01")
    assert "New estimates (1 Dec 2026) against the previous report (2 Nov 2026)" in html2
    assert "Estimate changes since 2 Nov 2026" in html2


def test_gate_refuses_a_failing_model(monkeypatch):
    sys.path.insert(0, str(DB / "report"))
    sys.path.insert(0, str(DB))
    try:
        import rb_gate
    finally:
        sys.path.remove(str(DB / "report"))
        sys.path.remove(str(DB))

    class Fake:
        model_path, map_path, case = str(SATS_XLSX), str(MB / "model_map_sats.json"), "sats_data"
        out = Path(os.environ.get("TMP", "/tmp"))
        import datetime as _dt
        today = _dt.date(2026, 11, 2)

        def master(self):
            return "2 ERROR(S)"

        def audit(self):
            import audit
            c = audit.Case(self.model_path, self.map_path, self.case)
            return audit.audit(c), audit

        def case_gate(self):
            return True, [], dict(m_ours=0.15, m_implied=0.12, g_ours=0.05, g_implied=0.045, dcf=50.7, price=39.75)

    res = rb_gate.evaluate(Fake(), skip_stress=True, skip_verify=True)
    assert res["ok"] is False
    assert [i for i in res["items"] if i["name"] == "Checks sheet"][0]["ok"] is False


@pytest.mark.skipif(not (DB / "report" / "rb_pdf.py").exists(), reason="report module missing")
def test_pdf_page_count_when_a_browser_exists(tmp_path):
    sys.path.insert(0, str(DB / "report"))
    try:
        import rb_pdf
    finally:
        sys.path.remove(str(DB / "report"))
    if not rb_pdf.find_browser():
        pytest.skip("no Chromium browser on this machine")
    html, _ = build(tmp_path, "example_data", EXAMPLE_XLSX, "model_map.json", "2026-11-02")
    src = next(tmp_path.glob("*.html"))
    pdf = rb_pdf.to_pdf(src, tmp_path / "report.pdf")
    n = rb_pdf.page_count(pdf)
    assert n is None or 18 <= n <= 40, n          # the fictional example is thinner than a real case (SATS: 25-40, tested in phase 3)
