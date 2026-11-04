"""Base rates in the report: the model's three-year revenue growth looked up in the Base Rate Book (deflated), the
80th-percentile flag, and the gate line that flags without failing. Fictional estimates only; the table is the
committed base_rates.yaml."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "deck_builder" / "report"))
import rb_baserate as br  # noqa: E402
import rb_gate  # noqa: E402


def _est(g, m0=0.20, m3=0.22):
    rev = [100 * (1 + g) ** i for i in range(5)]
    return {"years": [2026, 2027, 2028, 2029, 2030], "rows": {"rev": rev, "ebitda": [rev[0] * m0, None, None, rev[3] * m3, None]}}


def test_the_table_is_the_books_and_sums_to_one_hundred():
    t = br.table()
    d = t["distributions"][0]
    assert d["page"] == "p. 22" and d["real"] is True and sum(b[2] for b in d["buckets"]) == pytest.approx(100.0, abs=0.2)
    assert br.share_at_least(0.054, d["buckets"]) == pytest.approx(0.5, abs=0.03)          # the book's median


def test_growth_outside_the_80th_percentile_is_flagged_after_deflation():
    hi = br.check(_est(0.20))
    assert hi["rev_cagr"] == pytest.approx(0.20) and hi["real"] == pytest.approx(1.20 / 1.02 - 1) and hi["flag"] and hi["share"] < 0.2
    mid = br.check(_est(0.05))
    assert not mid["flag"] and mid["m_from"] == pytest.approx(0.20) and mid["m_to"] == pytest.approx(0.22)
    assert br.check({"years": [2026], "rows": {"rev": [1]}}) is None


def test_the_gate_flags_without_failing():
    class Rep:
        def __init__(self, est):
            self.est = est

        def estimates(self):
            return self.est
    item = br.gate_item(Rep(_est(0.20)))
    assert item["ok"] is True and item["flag"] and "outside the 80th percentile" in item["detail"]
    assert "[flag] Base rates" in rb_gate.render_text({"ok": True, "items": [item]})
    assert br.gate_item(Rep(_est(0.05)))["flag"] is False

    class Broken:
        def estimates(self):
            raise RuntimeError("no workbook")
    assert br.gate_item(Broken())["ok"] is True and "not computed" in br.gate_item(Broken())["detail"]
