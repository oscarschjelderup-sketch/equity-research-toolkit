"""Start a new case from the statements the dashboard already holds.

    python new_case.py ELK --name "Elkem ASA" --sector industrials [--segments "Silicon,Foundry Alloys,Carbon"]

Reads ``~/osloquant-home/cases/<CODE>.statements.json`` (written by ``oq case export CODE`` in oslo-quant: every annual
and quarterly statement line Yahoo Finance reports, the price, the share count and the reporting currency) and writes:

    model_builder/<slug>_data.py        the data module – history filled from the statements, drivers as template defaults
    deck_builder/<slug>_deck.py         the report narrative with every key present and empty
    examples/<CODE>/data/KILDER.md      the source register, with the statements as its first entries
    examples/<CODE>/data/FORSTAAELSE.md the understanding-before-the-model page with the sector checklist as questions

What the factory does NOT do: it invents nothing. Lines Yahoo does not split (personnel vs other opex, leases, inventories
vs receivables, current vs non-current debt) are put on one line and marked, the forecast drivers are the fictional Example
Company's and marked TEMPLATE, and the module carries ``SCAFFOLD = True`` – the report builder refuses to build while it
is set. The workbook builds (build_model.py) so the history can be read in Excel at once, but it is a scaffold, not a case,
until every TODO is replaced with a sourced figure and SCAFFOLD is removed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
YEARS = list(range(2019, 2026))                    # the workbook's seven history columns
SECTORS = {"consumer": "Consumer, retail and services", "salmon": "Salmon", "oilservice": "Oil service",
           "industrials": "Industrials and materials", "bank": "Banks"}
M = 1e6


# ------------------------------------------------------------------------------------------------ inputs
def home() -> Path:
    return Path(os.environ.get("OSLOQUANT_HOME") or (Path.home() / "osloquant-home"))


def load_statements(code: str, path: Path | None = None) -> dict | None:
    p = path or (home() / "cases" / f"{code.upper()}.statements.json")
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def checklist(sector: str, doc: Path | None = None) -> list[str]:
    """The sector's checklist items from docs/rapport/skalering.md (section 3), as plain lines."""
    doc = doc or (ROOT / "docs" / "rapport" / "skalering.md")
    if not doc.exists():
        return []
    want = SECTORS.get(sector, sector).lower()
    out, on = [], False
    for line in doc.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            on = line[4:].lower().startswith(want.split(" ")[0])
            continue
        if line.startswith("## ") and on:
            break
        if on and line.strip().startswith("- [ ]"):
            out.append(line.strip()[6:])
    return out


# ------------------------------------------------------------------------------------------------ history from the statements
def _by_year(rows: list[dict]) -> dict[int, dict]:
    out = {}
    for r in rows or []:
        y = int(str(r.get("report_date", ""))[:4] or 0)
        if y:
            out[y] = r                              # the newest report for a year wins (restatements come later in the list)
    return out


def _m(v) -> float | None:
    return None if v is None else round(float(v) / M, 1)


def history(st: dict | None) -> dict:
    """The HIST lines the workbook needs, per year of ``YEARS``, from Yahoo's statement lines; None where there is no
    year, and one marked line where Yahoo does not split what the workbook splits. Returns the dict plus notes."""
    inc = _by_year((st or {}).get("annual", {}).get("income", []))
    bal = _by_year((st or {}).get("annual", {}).get("balance", []))
    cf = _by_year((st or {}).get("annual", {}).get("cashflow", []))
    pye = (st or {}).get("prices_ye") or {}
    keys = ["revA", "revB", "revC", "cogs", "pers", "oth", "da", "rou_dep", "special", "netfin", "lease_int", "tax", "minority_pl", "lease_pay",
            "gw", "intang", "ppe", "rou", "other_nca", "inv", "rec", "oca", "cash", "equity", "minority_bs", "debt_nc", "debt_c", "lease_nc", "lease_c",
            "deftax", "pay", "ocl", "cfo", "capex", "acq", "div_paid", "fin_other", "volA", "volB", "volC", "locA", "locB", "locC", "ftes", "shares", "dps", "price"]
    H: dict[str, list] = {k: [None] * len(YEARS) for k in keys}
    notes: list[str] = []
    have = [y for y in YEARS if y in inc and y in bal]
    for y in [y for y in inc if y not in YEARS]:
        notes.append(f"{y}: outside the workbook's {YEARS[0]}-{YEARS[-1]} columns – not used")
    prev_cash = None
    for i, y in enumerate(YEARS):
        if y not in have:
            continue
        a, b, c = inc[y], bal[y], cf.get(y, {})
        g = lambda d, k: (float(d[k]) / M if d.get(k) is not None else None)  # noqa: E731
        rev, cogs, ebitda, ebit = g(a, "total_revenue"), g(a, "cost_of_revenue"), g(a, "ebitda"), g(a, "ebit")
        pbt, taxp, ni = g(a, "pretax_income"), g(a, "tax_provision"), g(a, "net_income")
        if rev is None:
            continue
        H["revA"][i] = round(rev, 1)
        H["cogs"][i] = round(-cogs, 1) if cogs is not None else 0.0
        gp = rev + H["cogs"][i]
        H["pers"][i] = 0.0                                                   # Yahoo does not split personnel from other opex
        H["oth"][i] = round((ebitda - gp), 1) if ebitda is not None else None  # one line: EBITDA - gross profit
        H["da"][i] = round(ebit - ebitda, 1) if None not in (ebit, ebitda) else None
        H["rou_dep"][i], H["special"][i], H["lease_int"][i], H["lease_pay"][i] = 0.0, 0.0, 0.0, 0.0
        H["netfin"][i] = round(pbt - ebit, 1) if None not in (pbt, ebit) else None
        H["tax"][i] = round(-taxp, 1) if taxp is not None else 0.0
        np_ = (pbt or 0) + H["tax"][i]
        H["minority_pl"][i] = round(ni - np_, 1) if ni is not None else 0.0
        # balance sheet: Yahoo's totals, split only where Yahoo splits
        ta, ca, cash = g(b, "total_assets"), g(b, "current_assets"), g(b, "cash_and_equivalents") or 0.0
        gwi, tl, cl, debt = g(b, "goodwill_and_intangibles") or 0.0, g(b, "total_liabilities"), g(b, "current_liabilities"), g(b, "total_debt") or 0.0
        te, mi = g(b, "total_equity"), g(b, "minority_interest") or 0.0
        if None in (ta, ca, tl, cl, te):
            notes.append(f"{y}: balance sheet incomplete at Yahoo – left blank")
            for k in keys:
                H[k][i] = None
            continue
        H["gw"][i], H["intang"][i], H["rou"][i], H["other_nca"][i] = round(gwi, 1), 0.0, 0.0, 0.0
        H["ppe"][i] = round(ta - ca - gwi, 1)                                # PPE incl. ROU and other non-current assets
        H["inv"][i], H["rec"][i] = 0.0, 0.0
        H["oca"][i] = round(ca - cash, 1)                                    # inventories + receivables + other current assets
        H["cash"][i] = round(cash, 1)
        H["equity"][i], H["minority_bs"][i] = round(te - mi, 1), round(mi, 1)
        ncl = tl - cl
        debt_nc = min(debt, max(ncl, 0.0))
        H["debt_nc"][i], H["debt_c"][i] = round(debt_nc, 1), round(debt - debt_nc, 1)
        H["lease_nc"][i], H["lease_c"][i] = 0.0, 0.0
        H["deftax"][i] = round(ncl - debt_nc, 1)
        H["pay"][i] = 0.0
        H["ocl"][i] = round(cl - (debt - debt_nc), 1)
        gap = round(ta - (te + tl), 1)
        if abs(gap) >= 0.5:
            H["oca"][i] = round(H["oca"][i] - gap, 1)                        # Yahoo's assets and equity+liabilities differ: absorbed in other current assets
            notes.append(f"{y}: Yahoo's total assets and equity + liabilities differ by {gap:+.1f}m – absorbed in other current assets")
        # cash flow: the lines Yahoo has; the financing line ties the cash flow to the balance sheet
        H["cfo"][i] = round(g(c, "operating_cash_flow"), 1) if c.get("operating_cash_flow") is not None else None
        H["capex"][i] = round(g(c, "capital_expenditure"), 1) if c.get("capital_expenditure") is not None else None
        H["acq"][i] = 0.0
        H["div_paid"][i] = round(g(c, "dividends_paid"), 1) if c.get("dividends_paid") is not None else 0.0
        if prev_cash is not None and None not in (H["cfo"][i], H["capex"][i]):
            H["fin_other"][i] = round((cash - prev_cash) - H["cfo"][i] - H["capex"][i] - H["acq"][i] - H["lease_pay"][i] - H["div_paid"][i], 1)
        else:
            H["fin_other"][i] = 0.0
        prev_cash = cash
        sh = b.get("shares_outstanding") or a.get("diluted_shares")
        H["shares"][i] = round(float(sh) / M, 1) if sh else None
        H["dps"][i] = round(-H["div_paid"][i] / H["shares"][i], 2) if H["shares"][i] and H["div_paid"][i] else 0.0
        px = pye.get(str(b.get("report_date", ""))[:10]) or pye.get(f"{y}-12-31")
        H["price"][i] = round(float(px["close"]), 2) if px else None
    start = next((i for i, v in enumerate(H["revA"]) if v is not None), len(YEARS))
    return {"hist": H, "start": start, "years_with_data": [YEARS[i] for i in range(len(YEARS)) if H["revA"][i] is not None], "notes": notes}


# ------------------------------------------------------------------------------------------------ the files
def _py(v) -> str:
    return "None" if v is None else repr(v)


def _rows(H: dict, keys: list[str], comment: dict[str, str]) -> str:
    out = []
    for k in keys:
        vals = ", ".join(_py(v) for v in H[k])
        out.append(f"    {k}=[{vals}],{'  # ' + comment[k] if k in comment else ''}")
    return "\n".join(out)


def data_module(code: str, name: str, sector: str, segs: list[str], st: dict | None, hist: dict, today: dt.date) -> str:
    H, start = hist["hist"], hist["start"]
    cur = ((st or {}).get("currency") or {}).get("reporting", "NOK")
    price = ((st or {}).get("price") or {})
    shares = (st or {}).get("shares")
    exported = str((st or {}).get("exported_at", ""))[:10]
    src = f"Yahoo Finance via the oslo-quant store, exported {exported} (oq case export {code})" if st else "no statements export found – every line is blank"
    last_bal = (_by_year((st or {}).get("annual", {}).get("balance", [])) or {None: {}})
    lb = last_bal[max(k for k in last_bal if k)] if any(last_bal) else {}
    debt_q, cash_q = _m(lb.get("total_debt")) or 0.0, _m(lb.get("cash_and_equivalents")) or 0.0
    mi_q = _m(lb.get("minority_interest")) or 0.0
    seg_a, seg_b, seg_c = (segs + ["", "", ""])[:3]
    cm = {"revA": f"group revenue on one segment ({seg_a}); split by segment from the annual report (TODO)", "revB": "TODO", "revC": "TODO",
          "cogs": "cost of revenue as Yahoo reports it", "pers": "TODO: Yahoo does not split personnel from other opex – both sit in oth",
          "oth": "EBITDA - gross profit (Yahoo): personnel + other opex on one line", "da": "EBIT - EBITDA (Yahoo); ROU depreciation not split (TODO)",
          "rou_dep": "TODO (IFRS 16 split from the annual report)", "special": "TODO: impairments and special items are inside EBIT here",
          "netfin": "pre-tax profit - EBIT (Yahoo)", "lease_int": "TODO", "tax": "tax provision (Yahoo)", "minority_pl": "net income to shareholders - net profit (Yahoo)",
          "lease_pay": "TODO (cash flow statement, lease payments incl. interest)", "gw": "goodwill and intangibles (Yahoo, one line)", "intang": "inside gw",
          "ppe": "total assets - current assets - goodwill/intangibles: PPE incl. ROU and other non-current assets (TODO split)", "rou": "inside ppe",
          "other_nca": "inside ppe", "inv": "inside oca", "rec": "inside oca", "oca": "current assets - cash (inventories, receivables, other)", "cash": "Yahoo",
          "equity": "total equity - minority (Yahoo)", "minority_bs": "Yahoo", "debt_nc": "total debt, non-current part (Yahoo; leases inside)", "debt_c": "the rest of total debt",
          "lease_nc": "TODO (inside debt)", "lease_c": "TODO", "deftax": "other non-current liabilities (total - current - debt)", "pay": "inside ocl",
          "ocl": "current liabilities less current debt", "cfo": "operating cash flow (Yahoo)", "capex": "Yahoo", "acq": "TODO",
          "div_paid": "Yahoo", "fin_other": "PLUG so that the cash flow ties to the change in cash (first year 0)", "volA": "TODO: volume per segment",
          "volB": "TODO", "volC": "TODO", "locA": "TODO: units per segment (or leave blank in segment mode)", "locB": "TODO", "locC": "TODO", "ftes": "TODO",
          "shares": "shares outstanding, m (Yahoo)", "dps": "DERIVED: dividends paid / shares (Yahoo); replace with the declared DPS", "price": "year-end close (oslo-quant store)"}
    is_rows = _rows(H, ["revA", "revB", "revC", "cogs", "pers", "oth", "da", "rou_dep", "special", "netfin", "lease_int", "tax", "minority_pl", "lease_pay"], cm)
    bs_rows = _rows(H, ["gw", "intang", "ppe", "rou", "other_nca", "inv", "rec", "oca", "cash", "equity", "minority_bs", "debt_nc", "debt_c", "lease_nc", "lease_c", "deftax", "pay", "ocl"], cm)
    cf_rows = _rows(H, ["cfo", "capex", "acq", "div_paid", "fin_other"], cm)
    kpi_rows = _rows(H, ["volA", "volB", "volC", "locA", "locB", "locC", "ftes", "shares", "dps", "price"], cm)
    notes = "\n".join(f"#   - {n}" for n in hist["notes"]) or "#   (none)"
    slug = code.lower()
    return f'''"""{name} ({code}) – SCAFFOLD written by model_builder/new_case.py on {today.isoformat()}.

History: {src}. Units: {cur} millions. Years with data: {hist["years_with_data"] or "none"}; earlier columns blank (HIST_START).
Every line marked TODO or PLUG must be replaced with a figure from the company's own reports (examples/{code}/data/KILDER.md),
and every driver block below is the fictional Example Company's TEMPLATE default until it is written for this company.
The report builder refuses to build while SCAFFOLD is True. Sector checklist: docs/rapport/skalering.md ({SECTORS.get(sector, sector)}).
Notes from the export:
{notes}
"""
import example_data as _T   # TEMPLATE defaults for the driver blocks – replace, then delete this import

SCAFFOLD = True              # remove when every TODO/PLUG/TEMPLATE below is replaced with sourced figures

YEARS = {YEARS!r}
HIST_START = {start}         # first year with data; columns before it are blank in the workbook

SEG_REV = {{"A": {H["revA"]!r}, "B": {H["revB"]!r}, "C": {H["revC"]!r}}}   # TODO: split revenue by segment
SEG_VOL = {{"A": {H["volA"]!r}, "B": {H["volB"]!r}, "C": {H["volC"]!r}}}   # TODO: volume per segment ({cur}m revenue needs a unit)
SEG_LOC = {{"A": {H["locA"]!r}, "B": {H["locB"]!r}, "C": {H["locC"]!r}}}
LOCATIONS = {[None] * len(YEARS)!r}

HIST = dict(
    # ---- income statement ({src}); costs negative ----
{is_rows}
    # ---- balance sheet ----
{bs_rows}
    # ---- cash flow (condensed) ----
{cf_rows}
    # ---- KPIs and per-share data ----
{kpi_rows}
)


def simulate():
    """The history dict; asserts that the balance sheet balances in every year with data (the factory's split keeps
    Yahoo's totals, so it does). The cash flow ties by construction through the fin_other plug."""
    out = {{k: list(v) for k, v in HIST.items()}}
    out["rev"] = []
    for i in range(len(YEARS)):
        if out["revA"][i] is None:
            out["rev"].append(None)
            continue
        out["rev"].append(sum(out[k][i] or 0 for k in ("revA", "revB", "revC")))
        ta = sum(out[k][i] or 0 for k in ["gw", "intang", "ppe", "rou", "other_nca", "inv", "rec", "oca", "cash"])
        tel = sum(out[k][i] or 0 for k in ["equity", "minority_bs", "debt_nc", "debt_c", "lease_nc", "lease_c", "deftax", "pay", "ocl"])
        assert abs(ta - tel) < 0.5, (YEARS[i], ta, tel)
    return out


# ---- latest quarter / market data (Inputs sheet) – TODO: the last interim report's balance sheet, not the last annual one ----
MARKET = dict(
    company="{name} – SCAFFOLD (drivers not set)", ticker="{code}", exchange="Oslo Børs", sector="{SECTORS.get(sector, sector)} (TODO: the company's own words)",
    currency="{cur}", unit="{cur}m", team="[Case team name]",
    model_date={(today.year, today.month, today.day)!r}, val_date={(today.year, today.month, today.day)!r},
    price_date={tuple(int(x) for x in str(price.get("date", today.isoformat())).split("-"))!r}, bs_date=None,   # TODO bs_date = last interim balance sheet
    share_price={price.get("value") if price else 0.0!r},      # {price.get("source", "TODO")} {price.get("date", "")}
    shares={round(float(shares) / M, 1) if shares else 0.0!r},  # m, Yahoo (TODO: issued less treasury at the balance-sheet date)
    dilutive=0.0,                     # TODO: options and RSUs
    high52=None, low52=None,          # TODO (oslo-quant store)
    consensus_tp=None,                # TODO: Yahoo Finance mean target, or "not available"
    debt_q={debt_q!r}, cash_q={cash_q!r}, leases_q=0.0,   # last ANNUAL balance sheet at Yahoo – TODO replace with the last interim report (note on borrowings)
    minority_q={mi_q!r}, associates_q=0.0, pension_q=0.0, other_adj=0.0,   # TODO
    seg_a="{seg_a or "Group"}", seg_b="{seg_b or "Segment B"}", seg_c="{seg_c or "Segment C"}", vol_unit="TODO (e.g. Sales volume (kt))",
    loc_label="TODO (e.g. production sites / stores)", rpu_label="TODO (e.g. revenue per tonne)",
    peer_lease=1, peer_year=1, fictional=False,
    data_note="SCAFFOLD: history from {src}; drivers are template defaults. Not a case until every TODO is replaced (new_case.py).",
    yahoo="{code}.OL", index_yahoo="OSEBX.OL", free_float="n.a. (TODO)",
    beta_note="TODO", cons_note="TODO",
)

# ---- TEMPLATE defaults (fictional Example Company) – every block must be rewritten for {name} ----
BASE = dict(_T.BASE)                      # TEMPLATE: eight years of drivers per segment, costs, capex, working capital, tax, payout
SCENARIO_ADJ = list(_T.SCENARIO_ADJ)      # TEMPLATE: bear/base/bull deltas and probabilities
TERMINAL = dict(_T.TERMINAL)              # TEMPLATE: terminal growth, RONIC, exit multiple
WACC_INPUTS = dict(_T.WACC_INPUTS)        # TEMPLATE: rf (Norges Bank), ERP (PwC/FFN), size, spread, target D/V
COST_CAPITAL = dict(_T.COST_CAPITAL)      # TEMPLATE: fixed-cost shares, central costs, leverage target, buybacks
ENGINE = dict(rev_mode=1, ramp=(0.35, 0.75, 0.95), util_tol=0.15)   # segment mode (volume x price); 2 = location engine
CONSENSUS = dict(source="TODO: company-compiled consensus or Yahoo Finance; «not available» where there is none", date={(today.year, today.month, today.day)!r},
                 n=None, buy=None, hold=None, sell=None, rev=[None, None, None], ebitda=[None, None, None], ebit=[None, None, None],
                 eps=[None, None, None], dps=[None, None, None])
CONSENSUS_Q = None
VARIANT = []                              # TODO: (topic, our view, consensus view, evidence, what proves it and when, metric, year)
SCENARIO_STORIES = {{"bear": ("TODO", "TODO", "TODO"), "base": ("TODO", "TODO", "TODO"), "bull": ("TODO", "TODO", "TODO")}}
KILL = [  # KPI label, Model row key, kill if ('below'/'above'), threshold, watch buffer, format – TODO: the sector checklist names the usual five
    ("EBIT adj. margin (pre-IFRS 16)", "ebit_adj_m", "below", None, 0.01, "pct"),
    ("Group volume growth", "g_volc", "below", None, 0.01, "pct"),
    ("Cash conversion (FCFF / EBITDAaL)", "cconv", "below", None, 0.10, "pct"),
    ("NIBD / EBITDAaL", "lev", "above", None, 0.25, "mult"),
    ("EBITDA margin (reported)", "ebitda_m", "below", None, 0.01, "pct"),
]
KILL_TEXT = []                            # criteria the workbook rows cannot carry (division margins, binary events) – plain sentences with the date they are judged
PEERS = []                                # TODO: name, country, mcap, ev, evs(3), evebitda(3), evebit(3), pe(3), ebit margin, growth, raw beta, D/E, tax – 6-10 peers
PEER_GROUPS = {{}}
QUARTERS = None                           # TODO: eight quarters of group lines and segment KPIs (see elkem_data.py / sats_data.py)
EVENTS = []                               # TODO: (date, event, source) from the financial calendar
HISTORY = []                              # first edition – no earlier calls
META = dict(
    sector="{sector}", cyclical=None, commodity=None, binary_event=None, reporting_currency="{cur}", last_share_issue=None,
    guidance=dict(ebit_margin=None), conflicts=None,
    disclosures=dict(author="Case author (private student case study)", price_datetime="TODO",
                     rating_definitions="BUY: 12-month expected total return above the cost of equity + 5pp; SELL: below Ke − 5pp; HOLD in between",
                     valuation_summary="70% DCF (FCFF after lease payments, value-driver terminal value) + 30% peer multiples, rolled forward 12 months",
                     update_frequency="After each quarterly report", history_12m="First edition – no earlier calls",
                     status="SCAFFOLD – not a case, not investment research or advice"),
    reasons=dict(),
)
'''


def deck_module(code: str, name: str, sector: str, items: list[str], today: dt.date) -> str:
    chk = "\n".join(f"#   [ ] {x}" for x in items) or "#   (no checklist found for this sector in docs/rapport/skalering.md)"
    d = today.strftime("%-d %b %Y") if os.name != "nt" else today.strftime("%d %b %Y").lstrip("0")
    return f'''"""{name} ({code}) – report narrative SCAFFOLD written by model_builder/new_case.py on {today.isoformat()}.

Every key build_report.py reads is present and empty. Fill each from sourced material (examples/{code}/data/KILDER.md); the
exhibit kinds are bar, hbar, line, waterfall and table (see example_deck.py and elkem_deck.py). Sector checklist ({SECTORS.get(sector, sector)}):
{chk}
"""

D = "{d}"
TODO = "TODO"

CT = dict(
    report=dict(
        kind="Initiation",
        title=TODO,
        memo=[("Why now", TODO), ("Against the company's own targets", TODO), ("What changed", "First edition – no previous estimates."), ("Valuation", TODO)],
        case_lead=TODO,
        thesis=[],                       # four bullets, **bold lead** – each pointing at a deep dive or an exhibit
        risks_down=[], risks_up=[],
        description=[],
        revenue_by_category=dict(year="TODO", rows=[], source=TODO, date=D),
        targets=[],                      # (target, value, source)
        management=[],                   # (role, name, note)
        owners=dict(rows=[], source=TODO, date=D),
        swot=dict(strengths=[], weaknesses=[], opportunities=[], threats=[]),
        quarter_lead=TODO,
        deep_dives=[],                   # dict(title, question, text=[...], exhibits=[...], into_model=[(driver, value, "Sheet | row")])
        competition={{}},                 # market -> dict(rows=[(name, format, units, price, binding, source, date)], prices=[...], price_note, takeaway)
        macro=dict(columns=[], rows=[], bullets=[], exhibits=[]),
        revision_notes=[],
        reverse_text=[],
        data_map=[],                     # (data set, status, note)
        flips=[],                        # from whatif_runs: what turns the rating
        unknowns=[],                     # what we do not know – honest, one line each
        events=[],                       # (date, event, source)
        history=[],
    ),
)
'''


def kilder_md(code: str, name: str, st: dict | None, hist: dict, today: dt.date) -> str:
    H = hist["hist"]
    yrs = hist["years_with_data"]
    cur = ((st or {}).get("currency") or {}).get("reporting", "NOK")
    exported = str((st or {}).get("exported_at", ""))[:10]

    def row(label, key, fmt="{:,.0f}"):
        vals = []
        for y in yrs:
            v = H[key][YEARS.index(y)]
            vals.append("–" if v is None else fmt.format(v).replace(",", " "))
        return f"| {label} | " + " | ".join(vals) + " |"

    annual = "\n".join([f"| {cur}m | " + " | ".join(str(y) for y in yrs) + " |", "|---|" + "---|" * len(yrs),
                        row("Revenue", "revA"), row("Cost of revenue", "cogs"), row("Opex (personnel + other, one line)", "oth"), row("D&A", "da"),
                        row("Net financial items", "netfin"), row("Tax", "tax"), row("Cash", "cash"), row("Debt (incl. leases)", "debt_nc"),
                        row("Equity to shareholders", "equity"), row("Operating cash flow", "cfo"), row("Capex", "capex"), row("Dividends paid", "div_paid"),
                        row("Shares (m)", "shares", "{:,.1f}"), row("Year-end close", "price", "{:,.2f}")]) if yrs else "_No statements export found._"
    q = (st or {}).get("quarterly", {}).get("income", [])
    quarters = "\n".join(["| Quarter end | Revenue | EBITDA | EBIT | Net income |", "|---|---|---|---|---|"] +
                         [f"| {r.get('report_date')} | " + " | ".join("–" if r.get(k) is None else f"{float(r[k]) / M:,.0f}".replace(",", " ")
                                                                      for k in ("total_revenue", "ebitda", "ebit", "net_income")) + " |" for r in q[-8:]]) if q else "_none_"
    return f"""# {name} ({code}) – kilder og råmateriale

Opprettet {today.isoformat()} av `model_builder/new_case.py` som stillas for caset i `examples/{code}/`. Alt er offentlig. Tall i {cur} millioner
der ikke annet står. Hver tabell skal oppgi dokument, dato og side. «Avledet» = regnet ut fra rapporterte tall (regnestykket vises).
«Ikke tilgjengelig» = finnes bare i betalte kilder eller er ikke publisert. **Radene fra Yahoo under er et utgangspunkt, ikke en kilde
god nok for rapporten: bytt hver av dem ut med selskapets egen rapport og sidetall.**

## 0. Det viktigste først: omfang og struktur

TODO: Hva eier selskapet i dag, hva er solgt eller holdt for salg de siste to årene, hvilke år finnes omregnet (industri-sjekklisten, punkt 1).

## 1. Selskapets egne dokumenter (primærkilder)

| Nr | Dokument | Dato | URL |
|---|---|---|---|
| D1 | TODO: siste kvartalsrapport | | |
| D2 | TODO: siste kvartalspresentasjon | | |
| D3 | TODO: årsrapport {yrs[-1] if yrs else "siste"} | | |
| D4 | TODO: kapitalmarkedsdag / strategioppdatering | | |
| D5 | TODO: finansiell kalender (NewsWeb) | | |

NewsWeb: `https://api3.oslo.oslobors.no/v1/newsreader/list?issuer={code}&fromDate=YYYY-MM-DD&toDate=YYYY-MM-DD` (POST);
enkeltmeldinger på `https://newsweb.oslobors.no/message/<id>`.

## 2. Årstall

### 2a. Slik Yahoo Finance rapporterer dem (via oslo-quant-lageret, eksportert {exported or "–"}; `oq case export {code}`)

{annual}

Yahoo deler ikke personal- og andre driftskostnader, leasing (IFRS 16), varelager/fordringer eller kortsiktig/langsiktig gjeld.
Stillaset legger dem på én linje hver (merket i `{code.lower()}_data.py`). TODO: erstatt med årsrapportens linjer, med sidetall.

### 2b. Segmenter

TODO: omsetning, EBITDA og volum per segment per år (note om segmenter i årsrapporten).

## 3. Kvartalstall

### 3a. Konsern – Yahoo Finance (samme eksport), siste åtte kvartaler

{quarters}

TODO: kvartalsrapportenes egne nøkkeltallstabeller (sidetall), åtte kvartaler, med segment-KPI-er.

## 4. Balanse ved siste kvartal

TODO: rentebærende gjeld, leasing, kontanter, minoriteter, tilknyttede selskaper, pensjon, eiendeler holdt for salg – fra siste kvartalsrapport med note.

## 5. Mål, utsikter og program

TODO: selskapets egne finansielle mål med kilde (side/lysark) og dato.

## 6. Eiere, ledelse, kalender

TODO: 20 største eiere (dato), ledelse og styre, finansiell kalender.

## 7. Bransjespesifikt

TODO: det sektorsjekklisten i `docs/rapport/skalering.md` ber om (priser, volum, kontrakter, reguleringer, råvarekurver – med dato).

## 8. Markedsdata

| Hva | Verdi | Kilde | Dato |
|---|---|---|---|
| Sluttkurs | {((st or {}).get("price") or {}).get("value", "TODO")} | oslo-quant-lageret (Yahoo, forsinket) | {((st or {}).get("price") or {}).get("date", "")} |
| Antall aksjer | {round(float(st["shares"]) / M, 1) if st and st.get("shares") else "TODO"} m | Yahoo (TODO: utstedte minus egne ved balansedato) | {exported} |
| Rapporteringsvaluta | {cur} | Yahoo quote summary | {exported} |
| Konsensus kursmål | TODO eller «ikke tilgjengelig» | | |
| Risikofri rente | TODO (Norges Bank, 10 år) | | |

## 9. Sektordata

TODO: åpne kilder bare; der en betalt indeks siteres i en åpen artikkel, oppgi artikkelen.
"""


def forstaaelse_md(code: str, name: str, sector: str, items: list[str], today: dt.date) -> str:
    chk = "\n".join(f"- [ ] {x}" for x in items) or "_(ingen sjekkliste funnet for denne sektoren i docs/rapport/skalering.md)_"
    return f"""# {name} – forståelse før modellen ({today.isoformat()}, stillas)

Skrives ferdig FØR driverne settes. Hvert avsnitt ender i en setning om hva det betyr for modellen. Kilder i `KILDER.md`.

## 0. Selskapet – hva det er i dag

TODO: Omfang, segmenter, hva som er solgt eller kjøpt, hvem som eier det, hva som er annerledes enn for to år siden.

## 1. Segmentene – hva de selger, til hvem, og hva som styrer marginen

TODO: per segment: produkt, kunde, pris-setting (kontrakt/spot/liste), volumdriver, faste vs variable kostnader.

## 2. Syklusen – hvor er vi

TODO: siste fem år av pris/volum/margin; er dagens nivå topp, bunn eller midt i syklusen? Hva sier selskapet selv?

## 3. Kostnadsbildet

TODO: de to–tre største kostnadslinjene, hva som driver dem, ±10 % på den styrende variabelen med oppgitte mengder.

## 4. Konkurranse, eiere og struktur

TODO: hvem konkurrerer, hvem eier, hva kan endre strukturen (handelstiltak, regulering, oppkjøp).

## 5. Kapitalallokering

TODO: balanse, forfall, covenants, utbyttepolitikk, capex-plan – mot selskapets egne mål.

## 6. Hva markedet priser inn

TODO: reverse DCF fra den lette casen (dashbordet) og fra modellen når den finnes: hvilken margin og vekst krever kursen?

## 7. Det vi ikke vet (og som avgjør caset)

TODO: tre ting, hver med datoen vi får vite mer.

## Sektorsjekkliste – {SECTORS.get(sector, sector)}

{chk}
"""


# ------------------------------------------------------------------------------------------------ main
def write_all(code: str, name: str, sector: str, segs: list[str], st: dict | None, root: Path, today: dt.date | None = None,
              force: bool = False, skalering: Path | None = None) -> list[Path]:
    today = today or dt.date.today()
    code = code.upper()
    slug = code.lower()
    hist = history(st)
    items = checklist(sector, skalering)
    targets = {root / "model_builder" / f"{slug}_data.py": data_module(code, name, sector, segs, st, hist, today),
               root / "deck_builder" / f"{slug}_deck.py": deck_module(code, name, sector, items, today),
               root / "examples" / code / "data" / "KILDER.md": kilder_md(code, name, st, hist, today),
               root / "examples" / code / "data" / "FORSTAAELSE.md": forstaaelse_md(code, name, sector, items, today)}
    clash = [p for p in targets if p.exists()]
    if clash and not force:
        raise FileExistsError("exists – pass --force to overwrite: " + ", ".join(str(p.relative_to(root)) for p in clash))
    for p, text in targets.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return list(targets)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("code", help="ticker, e.g. ELK")
    ap.add_argument("--name", required=True, help='company name, e.g. "Elkem ASA"')
    ap.add_argument("--sector", default="consumer", choices=sorted(SECTORS), help="sector checklist to attach")
    ap.add_argument("--segments", default="", help='up to three segment names, comma-separated (default: the group on segment A)')
    ap.add_argument("--statements", default=None, help="path to <CODE>.statements.json (default ~/osloquant-home/cases/)")
    ap.add_argument("--root", default=str(ROOT), help="repository root to write into (tests use a temporary one)")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    a = ap.parse_args(argv)
    st = load_statements(a.code, Path(a.statements) if a.statements else None)
    segs = [s.strip() for s in a.segments.split(",") if s.strip()]
    if not st:
        print(f"no statements export for {a.code.upper()} – run `oq case export {a.code.upper()}` in oslo-quant first; writing a blank scaffold", file=sys.stderr)
    try:
        files = write_all(a.code, a.name, a.sector, segs, st, Path(a.root), force=a.force)
    except FileExistsError as e:
        print(e, file=sys.stderr)
        return 2
    h = history(st)
    print(f"{a.code.upper()}: history {h['years_with_data'] or 'blank'} from {'the statements export' if st else 'nothing'}; SCAFFOLD = True")
    for n in h["notes"]:
        print(f"  note: {n}")
    for p in files:
        print(f"  wrote {p}")
    slug = a.code.lower()
    print("\nNext:\n"
          f"  1. examples/{a.code.upper()}/data/KILDER.md – replace the Yahoo rows with the annual and interim reports (page numbers)\n"
          f"  2. examples/{a.code.upper()}/data/FORSTAAELSE.md – write it before the drivers\n"
          f"  3. model_builder/{slug}_data.py – every TODO/PLUG/TEMPLATE, then delete `import example_data` and SCAFFOLD\n"
          f"  4. set EQR_CASE={slug}_data EQR_MAP=model_map_{slug}.json EQR_MODEL={slug}_final.xlsx; python build_model.py {slug}_raw.xlsx; "
          f"python excel_finalize.py {slug}_raw.xlsx {slug}_final.xlsx; python verify_dcf.py; python stress_test.py; python whatif_runs.py\n"
          f"  5. deck_builder/{slug}_deck.py, then build_report.py (it refuses while SCAFFOLD is True)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
