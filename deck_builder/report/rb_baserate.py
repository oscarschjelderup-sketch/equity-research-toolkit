"""Base rates for the model's estimates (DECISIONS: base rates in the report), after Mauboussin's Base Rate Book and
Kahneman's outside view: before the estimate is trusted, ask how often companies have actually done it.

The model's revenue growth a year over the first three estimate years is looked up in the Base Rate Book's
distribution of three-year sales growth (Mauboussin, Callahan and Majd, Credit Suisse, 26 Sep 2016, Exhibit 2, p. 22:
the top 1,000 global companies 1950–2015, real growth in 2015 dollars). The forecast is nominal, so it is deflated
by 2 % a year (Norges Bank's inflation target, EST) before the lookup, as the book itself warns (p. 26). The share of
companies that grew at least as fast is printed; below 20 % – outside the 80th percentile – the report flags it and
the build gate marks it (a flag, not a failure: the case may well be the exception, and then the report must say why).
The book has no distribution of margin changes; its persistence figure (r = 0.79 over three years, p. 59) is quoted
beside the margin path. The distribution is in base_rates.yaml beside this file, transcribed with its source.
"""

from __future__ import annotations

from pathlib import Path

import yaml

TABLE = Path(__file__).with_name("base_rates.yaml")
FLAG_SHARE = 0.20
INFLATION_EST = 0.02
YEARS = 3


def table() -> dict:
    return yaml.safe_load(TABLE.read_text(encoding="utf-8"))


def share_at_least(value: float, buckets: list) -> float:
    """Share of the distribution at or above ``value`` (uniform within the bucket that holds it)."""
    tot = sum(b[2] for b in buckets)
    s = 0.0
    for lo, hi, share in buckets:
        lo_ = -1e9 if lo is None else lo
        hi_ = 1e9 if hi is None else hi
        if value <= lo_:
            s += share
        elif value < hi_:
            s += share * ((hi_ - value) / (hi_ - lo_) if hi_ - lo_ < 1e8 else 0.5)
    return s / tot if tot else 0.0


def forecast(est: dict) -> dict | None:
    """Revenue CAGR and EBITDA margin over the first three estimate years of ``Report.estimates()``."""
    yrs, rows = est.get("years") or [], est.get("rows") or {}
    rev, ebitda = rows.get("rev") or [], rows.get("ebitda") or []
    if len(yrs) <= YEARS or len(rev) <= YEARS or not rev[0] or not rev[YEARS] or rev[0] <= 0 or rev[YEARS] <= 0:
        return None
    out = {"from": yrs[0], "to": yrs[YEARS], "rev_cagr": (rev[YEARS] / rev[0]) ** (1 / YEARS) - 1, "m_from": None, "m_to": None}
    if len(ebitda) > YEARS and ebitda[0] is not None and ebitda[YEARS] is not None:
        out["m_from"], out["m_to"] = ebitda[0] / rev[0], ebitda[YEARS] / rev[YEARS]
    return out


def check(est: dict) -> dict | None:
    fc = forecast(est)
    if not fc:
        return None
    t = table()
    dist = next(d for d in t["distributions"] if d["metric"] == "rev_cagr")
    real = (1 + fc["rev_cagr"]) / (1 + INFLATION_EST) - 1
    share = share_at_least(real, dist["buckets"])
    return fc | {"real": real, "share": share, "flag": share < FLAG_SHARE, "source": f'{dist["source"]}, {dist["page"]}', "sample": dist["sample"],
                 "median": dist.get("median"), "margin_note": t.get("notes", {}).get("margin", "")}


def gate_item(rep) -> dict:
    """The build gate's line: a flag (ok stays True) when the growth estimate is outside the 80th percentile."""
    try:
        res = check(rep.estimates())
    except Exception as e:  # noqa: BLE001 – the base-rate line must never stop the gate
        return dict(name="Base rates (Mauboussin)", ok=True, flag=False, detail=f"not computed: {type(e).__name__}: {e}")
    if not res:
        return dict(name="Base rates (Mauboussin)", ok=True, flag=False, detail="fewer than four estimate years: not computed")
    det = (f"revenue {res['rev_cagr'] * 100:+.1f} % a year {res['from']}–{res['to']} (real {res['real'] * 100:+.1f} %, EST): "
           f"{res['share'] * 100:.0f} % of companies grew at least as fast ({res['source']})")
    return dict(name="Base rates (Mauboussin)", ok=True, flag=res["flag"], detail=("outside the 80th percentile – say why in the report; " if res["flag"] else "") + det)
