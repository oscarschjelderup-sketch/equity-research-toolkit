"""Everything the report needs, gathered in one object: the recalculated workbook (through model_map.json), the case
data module (`<case>_data.py`), the case text module (`<case>_deck.py`, key `report`), stored earlier estimates,
cached prices and the result files of the verification scripts.

Nothing here invents a number: a value that is not in the workbook or the case module comes back as None and the
section renders it as "not available" or "not collected".
"""
from __future__ import annotations

import datetime as dt
import glob
import importlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DECK = HERE.parent
MB = DECK.parent / "model_builder"
for p in (str(DECK), str(MB)):
    if p not in sys.path:
        sys.path.insert(0, p)

from deck_data import ModelData  # noqa: E402

HC = list("EFGHIJK")
FC = list("LMNOPQRS")
ALL = HC + FC
EST_ROWS = ["rev", "rev_a", "rev_b", "rev_c", "ebitda", "ebitdaal", "ebit_adj", "np", "eps", "dps", "fcff"]


def _num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _date(v) -> dt.date | None:
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if isinstance(v, (tuple, list)) and len(v) == 3:
        return dt.date(*v)
    if isinstance(v, str) and len(v) >= 10:
        try:
            return dt.date.fromisoformat(v[:10])
        except ValueError:
            return None
    return None


def fmt_date(d) -> str:
    d = _date(d)
    return d.strftime("%-d %b %Y") if (d and os.name != "nt") else (d.strftime("%#d %b %Y") if d else "n.a.")


class Report:
    def __init__(self, model: str, map_path: str, case: str, out_dir: str, today: dt.date | None = None):
        os.environ["EQR_CASE"] = case
        self.case = case
        self.d = ModelData(model, map_path)
        self.model_path, self.map_path = str(model), str(map_path)
        self.mod = importlib.import_module(case)
        import deck_case  # noqa: E402  (reads EQR_CASE at import time)
        importlib.reload(deck_case)
        self.ct = deck_case.ct
        self.rep = self.ct("report", {}) or {}
        self.out = Path(out_dir)
        self.out.mkdir(parents=True, exist_ok=True)
        self.today = today or dt.date.today()
        ys = self.d.years(ALL)
        self.ylabels = [str(y) for y in ys]
        self.years = [int(str(y)[:4]) for y in ys]
        self.col = dict(zip(self.years, ALL))
        self.last_act = int(self.c("Inputs", "last_act"))
        self.first_fc = int(self.c("Inputs", "first_fc"))

    # ---------------------------------------------------------------- workbook access
    def c(self, sheet, key, default=None):
        try:
            v = self.d.c(sheet, key)
        except KeyError:
            return default
        return default if v is None else v

    def row(self, key, years=None, sheet="Model"):
        years = years or self.years
        cols = [self.col[y] for y in years]
        for sh in (sheet, "Model", "Output", "Analysis", "Hist", "DCF", "Drivers"):
            if f"{sh}|{key}" in self.d.reg["rows"]:
                r = self.d.reg["rows"][f"{sh}|{key}"]
                return [self.d.wb[sh][f"{c}{r}"].value for c in cols]
        return [None] * len(cols)

    def val(self, key, year, sheet="Model"):
        return self.row(key, [year], sheet)[0]

    def is_est(self, year) -> bool:
        return year >= self.first_fc

    def ylabel(self, year) -> str:
        return f"{year}{'E' if self.is_est(year) else 'A'}"

    # ---------------------------------------------------------------- headline values
    @property
    def company(self):
        return self.c("Inputs", "company")

    @property
    def ticker(self):
        return self.c("Inputs", "ticker")

    @property
    def currency(self):
        return self.c("Inputs", "currency", "NOK")

    @property
    def price(self):
        return self.c("Inputs", "price")

    @property
    def price_date(self):
        return _date(self.c("Inputs", "price_date"))

    @property
    def val_date(self):
        return _date(self.c("Inputs", "val_date"))

    @property
    def bs_date(self):
        return _date(self.c("Inputs", "bs_date"))

    @property
    def model_date(self):
        return _date(self.c("Inputs", "model_date"))

    @property
    def tp(self):
        return self.c("DCF", "tp")

    @property
    def rating(self):
        return str(self.c("DCF", "rating", ""))

    def head(self) -> dict:
        I, D, W = (lambda k: self.c("Inputs", k)), (lambda k: self.c("DCF", k)), (lambda k: self.c("WACC", k))
        return dict(
            price=I("price"), shares=I("shares"), dilutive=I("dilutive"), shares_dil=I("shares_dil"), mcap=I("mcap"),
            nibd=I("nibd"), leases=I("leases"), ev=I("ev_ex"), ev_incl=I("ev_incl"), high52=I("high52"), low52=I("low52"),
            cons_tp=I("cons_tp"), w_dcf=I("w_dcf"), w_peers=I("w_peers"), tp=D("tp"), tp_up=D("tp_up"), tp_tr=D("tp_tr"),
            tp_excess=D("tp_excess"), tp_div=D("tp_div"), fair=D("tp_fair"), dcf_ps=D("dcf_ps"), dcf_up=D("dcf_up"), ev_dcf=D("ev"),
            tv_share=D("tv_share"), tg=D("tv_g"), wacc=W("wacc"), ke=W("ke"), rf=W("rf"), erp=W("erp"), beta=W("bl"), size=W("size"),
            specific=W("specific"), kd=W("kd"), kd_at=W("kd_at"), dv=W("dv"), rating=self.rating, peer_val=self.c("Comps", "peer_val"),
            pw_dcf=self.c("Sensitivity", "pw_dcf_ps"), pw_tp=self.c("Sensitivity", "pw_tp"), exit_impl=self.c("Deck_Feed", "exit_impl"),
        )

    # ---------------------------------------------------------------- scenarios, kill criteria, variant perception
    def scenarios(self) -> dict:
        T = lambda k: self.c("Thesis", k)  # noqa: E731
        out = {}
        for s in ("bear", "base", "bull"):
            out[s] = dict(prob=T(f"sc_{s}_prob"), value=T(f"sc_{s}_value"), up=T(f"sc_{s}_up"), tp=T(f"sc_{s}_tp"), rating=T(f"sc_{s}_rating"),
                          story=T(f"sc_{s}_story"), trigger=T(f"sc_{s}_trigger"), signpost=T(f"sc_{s}_signpost"))
        return out

    def scenario_adj(self):
        return getattr(self.mod, "SCENARIO_ADJ", [])

    def kills(self) -> list[dict]:
        T = lambda k: self.c("Thesis", k)  # noqa: E731
        out = []
        for i in range(1, 6):
            if not T(f"kc{i}_kpi"):
                continue
            out.append(dict(kpi=T(f"kc{i}_kpi"), dir=T(f"kc{i}_dir"), th=T(f"kc{i}_th"), latest=T(f"kc{i}_latest"), per=T(f"kc{i}_per"),
                            base=T(f"kc{i}_base"), buf=T(f"kc{i}_buf"), status=T(f"kc{i}_status"), basechk=T(f"kc{i}_basechk"),
                            fmt=(getattr(self.mod, "KILL", [None] * 5)[i - 1] or [None] * 6)[5] if len(getattr(self.mod, "KILL", [])) >= i else "pct"))
        return out

    def variant(self) -> list[dict]:
        C = lambda k: self.c("Consensus", k)  # noqa: E731
        out = []
        for i in range(1, 4):
            if not C(f"vp{i}_topic"):
                continue
            out.append(dict(topic=C(f"vp{i}_topic"), ours=C(f"vp{i}_ours"), cons=C(f"vp{i}_cons"), why=C(f"vp{i}_why"), when=C(f"vp{i}_when"),
                            num=C(f"vp{i}_num"), metric=C(f"vp{i}_metric"), year=C(f"vp{i}_year")))
        return out

    def consensus(self) -> dict:
        C = lambda k: self.c("Consensus", k)  # noqa: E731
        rows = {}
        for m in ("rev", "ebitda", "ebit", "eps", "dps", "ebitm"):
            rows[m] = [(C(f"our_{m}_{i}"), C(f"cons_{m}_{i}"), C(f"diff_{m}_{i}")) for i in (1, 2, 3)]
        return dict(source=C("cons_source"), date=_date(C("cons_date")), n=C("cons_n"), buy=C("cons_buy"), hold=C("cons_hold"), sell=C("cons_sell"),
                    tp=C("cons_tp"), tp_up=C("cons_tp_up"), rows=rows, years=[self.first_fc, self.first_fc + 1, self.first_fc + 2],
                    quarter=getattr(self.mod, "CONSENSUS_Q", None))

    def reverse(self) -> dict:
        R = lambda k: self.c("Reverse_DCF", k)  # noqa: E731
        return dict(m_last=R("rd_m_last"), m_last_ours=R("rd_m_last_ours"), m_ref=R("rd_m_last_ref"), m_avg=R("rd_m_avg"), m_avg_ours=R("rd_m_avg_ours"),
                    cagr=R("rd_cagr"), cagr_ours=R("rd_cagr_ours"), cagr_ref=R("rd_cagr_ref"), m_at_g=R("rd_m_at_g"), wacc=R("rd_wacc"),
                    wacc_ours=R("rd_wacc_ours"), g=R("rd_g"), g_ours=R("rd_g_ours"), ok=(R("rd_wacc_ok"), R("rd_g_ok")))

    # ---------------------------------------------------------------- valuation detail
    def sens1(self):
        """Table 1: DCF value vs WACC (columns) and terminal growth (rows)."""
        sn = self.d.reg["sens"]
        ws = self.d.wb["Sensitivity"]
        hdr = sn["t1_hdr"]
        r0, r1 = sn["t1_rows"]
        cols = list("DEFGHIJ")
        waccs = [ws[f"{c}{hdr}"].value for c in cols]
        gs, grid = [], []
        for r in range(r0, r1 + 1):
            gs.append(ws[f"C{r}"].value)
            grid.append([ws[f"{c}{r}"].value for c in cols])
        return waccs, gs, grid

    def sens3(self):
        """Table 3: value vs growth shift (rows) and margin shift (columns) – an Excel data table."""
        sn = self.d.reg["sens"]
        ws = self.d.wb["Sensitivity"]
        hdr = sn["t3_hdr"]
        r0, r1 = sn["t3_rows"]
        cols = list("DEFGH")
        ms = [ws[f"{c}{hdr}"].value for c in cols]
        gs, grid = [], []
        for r in range(r0, r1 + 1):
            gs.append(ws[f"C{r}"].value)
            grid.append([ws[f"{c}{r}"].value for c in cols])
        return ms, gs, grid

    def football(self):
        ws = self.d.wb["Football"]
        out = []
        for k in ("w52", "dcf_wg", "dcf_sc", "evebitda", "evebit", "pe", "evs"):
            r = self.d.reg["rows"].get(f"Football|{k}")
            if r:
                out.append((ws[f"B{r}"].value, ws[f"C{r}"].value, ws[f"F{r}"].value, ws[f"D{r}"].value))
        return out

    def peers(self):
        """The peer table from the data module (name, country, mcap, ev, evs, evebitda, evebit, pe, margin, growth, beta, de, tax)."""
        return list(getattr(self.mod, "PEERS", []))

    def peer_groups(self) -> dict:
        pg = getattr(self.mod, "PEER_GROUPS", None)
        if pg:
            return dict(pg)
        return {"All peers": [p[0] for p in self.peers()]}

    def peer_stats(self):
        ws = self.d.wb["Comps"]
        cm = self.d.reg["comps"]
        out = {}
        for k in ("mean", "median", "q1", "q3", "high", "low", "company", "prem"):
            r = cm[k]
            out[k] = dict(evs=[ws[f"{c}{r}"].value for c in "FGH"], evebitda=[ws[f"{c}{r}"].value for c in "IJK"],
                          evebit=[ws[f"{c}{r}"].value for c in "LMN"], pe=[ws[f"{c}{r}"].value for c in "OPQ"],
                          margin=ws[f"R{r}"].value, growth=ws[f"S{r}"].value)
        out["bridge"] = self.c("Comps", "bridge")
        out["year"] = self.c("Comps", "year")
        return out

    def comps_implied(self):
        ws = self.d.wb["Comps"]
        cm = self.d.reg["comps"]
        out = []
        for k in ("evs", "evebitda", "evebit", "pe"):
            r = cm[k]
            out.append(dict(label=ws[f"B{r}"].value, metric=ws[f"C{r}"].value, q1=ws[f"D{r}"].value, med=ws[f"E{r}"].value, q3=ws[f"F{r}"].value,
                            v1=ws[f"G{r}"].value, vm=ws[f"H{r}"].value, v3=ws[f"I{r}"].value, incl=ws[f"J{r}"].value))
        return out

    def wacc_table(self):
        W = lambda k: self.c("WACC", k)  # noqa: E731
        return [("Risk-free rate", W("rf"), "pct"), ("Equity risk premium", W("erp"), "pct"), ("Unlevered peer beta (median)", W("bu"), "x2"),
                ("Levered beta", W("bl"), "x2"), ("Size / liquidity premium", W("size"), "pct"), ("Specific premium", W("specific"), "pct"),
                ("Cost of equity", W("ke"), "pct"), ("Pre-tax cost of debt", W("kd"), "pct"), ("After-tax cost of debt", W("kd_at"), "pct"),
                ("Debt / (debt + equity)", W("dv"), "pct"), ("WACC", W("wacc"), "pct")]

    def checks(self):
        ws = self.d.wb["Checks"]
        out = []
        for r in range(7, 60):
            n = ws[f"B{r}"].value
            if not _num(n):
                if r > 10:
                    break
                continue
            out.append(dict(n=int(n), check=ws[f"C{r}"].value, value=ws[f"D{r}"].value, status=ws[f"E{r}"].value, type=ws[f"F{r}"].value))
        return out

    def master(self) -> str:
        return str(self.c("Checks", "master", ""))

    def audit(self):
        import audit as _audit
        case = _audit.Case(self.model_path, self.map_path, self.case)
        res = _audit.audit(case)
        return sorted(res, key=lambda r: (_audit.ORDER[r.status], r.id)), _audit

    def case_gate(self):
        import case_gate as cg
        d = cg.read(self.model_path, self.map_path)
        ok, problems = cg.gate(d)
        return ok, problems, d

    # ---------------------------------------------------------------- result files of the Windows scripts
    def _json_near(self, env, default_name):
        for cand in (os.environ.get(env), MB / default_name, self.out / default_name):
            if cand and Path(cand).exists():
                return json.loads(Path(cand).read_text(encoding="utf8")), str(cand)
        return None, None

    def whatif(self):
        short = self.case.replace("_data", "")
        return self._json_near("EQR_WHATIF", f"whatif_runs_{short}.json")

    def stress(self):
        short = self.case.replace("_data", "")
        return self._json_near("EQR_STRESS", f"stress_{short}.json")

    def sotp(self):
        short = self.case.replace("_data", "")
        return self._json_near("EQR_SOTP", f"sotp_{short}.json")

    # ---------------------------------------------------------------- estimates store (for the revisions section)
    def estimates(self) -> dict:
        yrs = [y for y in self.years if self.is_est(y)]
        rows = {k: self.row(k, yrs) for k in EST_ROWS}
        return dict(date=self.today.isoformat(), price=self.price, price_date=str(self.price_date), tp=self.tp, rating=self.rating,
                    dcf_ps=self.c("DCF", "dcf_ps"), years=yrs, rows=rows, model_date=str(self.model_date))

    def save_estimates(self) -> Path:
        p = self.out / f"estimates_{self.today.isoformat()}.json"
        p.write_text(json.dumps(self.estimates(), indent=1, default=str), encoding="utf8")
        return p

    def previous_estimates(self) -> dict | None:
        files = sorted(glob.glob(str(self.out / "estimates_*.json")))
        files = [f for f in files if Path(f).stem.split("_")[-1] < self.today.isoformat()]
        if not files:
            return None
        return json.loads(Path(files[-1]).read_text(encoding="utf8"))

    # ---------------------------------------------------------------- prices
    def prices(self) -> dict | None:
        p = self.out / "prices.json"
        if p.exists():
            return json.loads(p.read_text(encoding="utf8"))
        return None

    def fetch_prices(self, months=14) -> dict:
        """One call to Yahoo Finance for the share and the index. Cached in the output folder."""
        import yfinance as yf
        m = getattr(self.mod, "MARKET", {})
        sym = m.get("yahoo", f"{self.ticker}.OL")
        idx = m.get("index_yahoo", "OSEBX.OL")
        px = yf.download([sym, idx], period=f"{months}mo", interval="1d", auto_adjust=False, progress=False)["Close"].dropna(how="all")
        out = dict(symbol=sym, index=idx, fetched=dt.date.today().isoformat(), source="Yahoo Finance (daily close)",
                   dates=[d.strftime("%Y-%m-%d") for d in px.index],
                   close=[None if v != v else round(float(v), 3) for v in px[sym]],
                   index_close=[None if v != v else round(float(v), 3) for v in px[idx]])
        (self.out / "prices.json").write_text(json.dumps(out), encoding="utf8")
        return out

    # ---------------------------------------------------------------- case blocks (all optional)
    def quarters(self):
        return getattr(self.mod, "QUARTERS", None)

    def events(self):
        ev = getattr(self.mod, "EVENTS", None) or self.rep.get("events") or []
        out = []
        for e in ev:
            d = _date(e[0])
            if d:
                out.append((d, e[1], e[2] if len(e) > 2 else ""))
        return sorted(out)

    def next_event(self):
        for d, label, src in self.events():
            if d >= self.today:
                return d, label, src
        return None

    def history(self):
        return getattr(self.mod, "HISTORY", None) or self.rep.get("history") or []

    def meta(self):
        return getattr(self.mod, "META", {}) or {}

    def market(self):
        return getattr(self.mod, "MARKET", {}) or {}
