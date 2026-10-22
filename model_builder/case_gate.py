"""Case gate: a case must say, in numbers, what the market prices in and where our view differs. No gap, no case.

Reads a finished workbook (values saved by Excel) and its cell map, prints the market-implied drivers from the
Reverse_DCF sheet next to ours, and fails (exit code 1) unless

- the reverse DCF was solved (implied EBIT margin and revenue CAGR are numbers), and
- at least one implied driver differs from ours by GAP_PP percentage points or more (final-year EBIT margin or
  revenue CAGR), and
- the DCF value differs from the share price by at least MIN_UPSIDE in either direction.

Runs without Excel, so CI checks the committed example workbooks; a private case is checked locally:

    python case_gate.py ../examples/SATS/SATS_ASA_DCF_Model.xlsx model_map_sats.json
    python case_gate.py <private>.xlsx model_map_<private>.json --json

Thresholds are set in DECISIONS.md (2026-10-22): 1.0pp and 10 %.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import openpyxl

GAP_PP = 0.010
MIN_UPSIDE = 0.10


def read(xlsx: str | Path, cell_map: str | Path) -> dict:
    cells = json.loads(Path(cell_map).read_text(encoding="utf8"))["cells"]
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    v = lambda key: wb[key.split("|")[0]][cells[key]].value  # noqa: E731
    return dict(company=v("Inputs|company"), price=v("Inputs|price"), dcf=v("DCF|dcf_ps"), tp=v("DCF|tp"), rating=v("DCF|rating"),
                m_implied=v("Reverse_DCF|rd_m_last"), m_ours=v("Reverse_DCF|rd_m_last_ours"), m_ref=v("Reverse_DCF|rd_m_last_ref"),
                g_implied=v("Reverse_DCF|rd_cagr"), g_ours=v("Reverse_DCF|rd_cagr_ours"),
                wacc_implied=v("Reverse_DCF|rd_wacc"), wacc_ours=v("Reverse_DCF|rd_wacc_ours"))


def gate(d: dict, gap_pp: float = GAP_PP, min_upside: float = MIN_UPSIDE) -> tuple[bool, list[str]]:
    num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)  # noqa: E731
    problems = []
    if not (num(d["m_implied"]) and num(d["g_implied"])):
        problems.append("the reverse DCF is not solved: no market-implied margin or growth")
        return False, problems
    gaps = {"EBIT margin, final year": d["m_ours"] - d["m_implied"], "revenue CAGR": d["g_ours"] - d["g_implied"]}
    if max(abs(x) for x in gaps.values()) < gap_pp:
        problems.append(f"no driver differs from the market by {gap_pp * 100:.1f}pp or more: "
                        + ", ".join(f"{k} {v * 100:+.2f}pp" for k, v in gaps.items()))
    upside = d["dcf"] / d["price"] - 1
    if abs(upside) < min_upside:
        problems.append(f"DCF value {d['dcf']:.2f} is within {min_upside * 100:.0f}% of the price {d['price']:.2f} ({upside * 100:+.1f}%)")
    return not problems, problems


def describe(d: dict) -> str:
    p = lambda x: f"{x * 100:.1f}%" if isinstance(x, (int, float)) else "n.a."  # noqa: E731
    return (f"{d['company']}: price {d['price']:.2f}, DCF {d['dcf']:.2f}, TP {d['tp']} {d['rating']}\n"
            f"  market prices in: EBIT margin {p(d['m_implied'])} (ours {p(d['m_ours'])}, today {p(d['m_ref'])}), "
            f"revenue CAGR {p(d['g_implied'])} (ours {p(d['g_ours'])}), WACC {p(d['wacc_implied'])} (ours {p(d['wacc_ours'])})")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xlsx")
    ap.add_argument("map")
    ap.add_argument("--gap", type=float, default=GAP_PP, help="Minimum driver gap (fraction, default 0.01 = 1pp).")
    ap.add_argument("--upside", type=float, default=MIN_UPSIDE, help="Minimum |DCF/price - 1| (default 0.10).")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    d = read(a.xlsx, a.map)
    ok, problems = gate(d, a.gap, a.upside)
    if a.json:
        print(json.dumps({**d, "ok": ok, "problems": problems}, indent=1, default=str))
    else:
        print(describe(d))
        print("CASE GATE: " + ("PASS" if ok else "FAIL – " + "; ".join(problems)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
