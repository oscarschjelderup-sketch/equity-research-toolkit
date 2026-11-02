"""The build gate: the report is not built unless the model passes.

Four checks, in order:
  1. the workbook's own Checks sheet reports no ERROR;
  2. `verify_dcf.py` reproduces the Excel DCF in Python and every reverse-DCF round trip returns the share price;
  3. the case audit (ANALYSE.md section 4) has no FAIL or FLAG and the case gate (reverse DCF, ≥ 10 % vs price) passes;
  4. `stress_test.py` (Excel, Windows) shows no ERROR on any switch; skipped with --skip-stress, which the report states.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

MB = Path(__file__).resolve().parents[2] / "model_builder"
TOL_PS, TOL_ROW, TOL_TRIP = 0.02, 1.0, 0.05


def _env(model, map_path, case, **extra):
    env = dict(os.environ, EQR_CASE=case, EQR_MAP=str(Path(map_path).resolve()), EQR_MODEL=str(Path(model).resolve()), PYTHONIOENCODING="utf-8")
    env.update(extra)
    return env


def run_verify(model, map_path, case) -> dict:
    res = subprocess.run([sys.executable, "verify_dcf.py"], cwd=MB, env=_env(model, map_path, case), capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    out = res.stdout + res.stderr
    item = dict(name="verify_dcf.py", ok=res.returncode == 0, detail="", output=out)
    if res.returncode != 0:
        item["detail"] = f"exit code {res.returncode}"
        return item
    py = re.search(r"python :.*value/share ([\d.]+)", out)
    xl = re.search(r"excel  :.*value/share ([\d.]+)", out)
    md = re.search(r"max diff\s+revenue ([\d.e+-]+)\s+fcff ([\d.e+-]+)\s+capex ([\d.e+-]+)", out)
    price = re.search(r"reverse DCF \(share price ([\d.]+)\)", out)
    trips = re.findall(r"-> python value (-?[\d.]+)", out)
    problems = []
    if not (py and xl and md and price):
        problems.append("could not parse the verification output")
    else:
        dps = abs(float(py.group(1)) - float(xl.group(1)))
        if dps > TOL_PS:
            problems.append(f"Python and Excel DCF differ by {dps:.3f} per share")
        diffs = [float(md.group(i)) for i in (1, 2, 3)]
        if max(diffs) > TOL_ROW:
            problems.append(f"row differences revenue/FCFF/capex {diffs}")
        p0 = float(price.group(1))
        bad = [t for t in trips if abs(float(t) - p0) > max(TOL_TRIP, 0.004 * p0)]
        if len(trips) < 4:
            problems.append(f"only {len(trips)} reverse-DCF round trips found")
        if bad:
            problems.append(f"reverse-DCF round trips off the share price {p0}: {bad}")
        item["detail"] = (f"Python {float(py.group(1)):.3f} vs Excel {float(xl.group(1)):.3f} per share; max row diff "
                          f"{max(diffs):.3f}; {len(trips)} round trips within {max(TOL_TRIP, 0.004 * p0):.2f} of {p0:.2f}")
    item["ok"] = not problems
    if problems:
        item["detail"] = "; ".join(problems)
    return item


def run_stress(model, map_path, case, out_json: Path) -> dict:
    if os.name != "nt":
        return dict(name="stress_test.py", ok=None, detail="not run – needs Excel on Windows", results=[])
    res = subprocess.run([sys.executable, "stress_test.py"], cwd=MB, env=_env(model, map_path, case, EQR_STRESS=str(out_json)),
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    item = dict(name="stress_test.py", ok=res.returncode == 0, detail="", output=res.stdout + res.stderr, results=[])
    if res.returncode != 0:
        item["detail"] = f"exit code {res.returncode}: {(res.stderr or res.stdout)[-300:]}"
        return item
    if out_json.exists():
        item["results"] = json.loads(out_json.read_text(encoding="utf8"))
    errs = [r["tag"] for r in item["results"] if r.get("kind") in ("base", "switch", "roundtrip") and "ERROR" in str(r.get("status", ""))]
    item["ok"] = not errs
    item["detail"] = (f"{len(item['results'])} runs; " + ("no ERROR on any switch" if not errs else "ERROR on: " + ", ".join(errs)))
    return item


def evaluate(rep, skip_stress=False, skip_verify=False) -> dict:
    """Run the gate on a `rb_data.Report`. Returns dict(ok, items=[...]) and writes gate.json in the output folder."""
    items = []
    master = rep.master()
    items.append(dict(name="Checks sheet", ok="ERROR" not in master.upper(), detail=master))
    if skip_verify:
        items.append(dict(name="verify_dcf.py", ok=None, detail="skipped (--skip-gate)"))
    else:
        items.append(run_verify(rep.model_path, rep.map_path, rep.case))
    try:
        res, _a = rep.audit()
        bad = [f"{r.id} {r.name}" for r in res if r.status in (_a.FAIL, _a.FLAG)]
        summ = _a.summary(res)
        items.append(dict(name="Case audit (ANALYSE.md §4)", ok=not bad, detail=", ".join(f"{k} {v}" for k, v in summ.items()) + (
            "; open: " + "; ".join(bad) if bad else "")))
    except Exception as e:  # noqa: BLE001 – the audit must never crash the build silently
        items.append(dict(name="Case audit (ANALYSE.md §4)", ok=False, detail=f"audit failed to run: {e}"))
    ok, problems, d = rep.case_gate()
    items.append(dict(name="Case gate (reverse DCF)", ok=ok, detail="; ".join(problems) if problems else
                      f"margin gap {(d['m_ours'] - d['m_implied']) * 100:+.1f}pp, growth gap {(d['g_ours'] - d['g_implied']) * 100:+.1f}pp, "
                      f"DCF {d['dcf'] / d['price'] - 1:+.0%} vs price"))
    if skip_stress:
        items.append(dict(name="stress_test.py", ok=None, detail="skipped (--skip-stress)", results=[]))
    else:
        items.append(run_stress(rep.model_path, rep.map_path, rep.case, rep.out / f"stress_{rep.case.replace('_data', '')}.json"))
    result = dict(ok=all(i["ok"] is not False for i in items), items=items, date=rep.today.isoformat())
    (rep.out / "gate.json").write_text(json.dumps({k: v for k, v in result.items()}, indent=1, default=str), encoding="utf8")
    return result


def render_text(result: dict) -> str:
    lines = ["BUILD GATE " + ("PASSED" if result["ok"] else "FAILED")]
    for i in result["items"]:
        st = {True: "ok  ", False: "FAIL", None: "skip"}[i["ok"]]
        lines.append(f"  [{st}] {i['name']}: {i['detail']}")
    return "\n".join(lines)
