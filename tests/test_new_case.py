"""The case factory (model_builder/new_case.py): from a statements export it writes a data module whose history balances
and builds into a workbook, a narrative skeleton, and the two markdown pages – all marked SCAFFOLD, which the report gate
refuses. Fictional fixture only."""
import importlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MB = ROOT / "model_builder"
FIX = ROOT / "tests" / "fixtures" / "XSC.statements.json"
sys.path.insert(0, str(MB))
import new_case as nc  # noqa: E402


def test_history_from_the_export_keeps_yahoos_totals_and_marks_what_it_cannot_split():
    st = json.loads(FIX.read_text(encoding="utf-8"))
    h = nc.history(st)
    H = h["hist"]
    assert h["start"] == 4 and h["years_with_data"] == [2023, 2024, 2025]            # 2019-2022 blank
    i = nc.YEARS.index(2025)
    assert H["revA"][i] == 1050.0 and H["revB"][i] is None and H["cogs"][i] == -640.0
    assert H["pers"][i] == 0.0 and H["oth"][i] == pytest.approx(140 - 410)           # EBITDA - gross profit on one line
    assert H["da"][i] == pytest.approx(85 - 140) and H["netfin"][i] == pytest.approx(60 - 85) and H["tax"][i] == -15.0
    assert H["minority_pl"][i] == pytest.approx(44 - 45)                              # net income to shareholders - (pbt + tax)
    # balance: assets = equity + liabilities, with Yahoo's split
    ta = sum(H[k][i] for k in ["gw", "intang", "ppe", "rou", "other_nca", "inv", "rec", "oca", "cash"])
    tel = sum(H[k][i] for k in ["equity", "minority_bs", "debt_nc", "debt_c", "lease_nc", "lease_c", "deftax", "pay", "ocl"])
    assert ta == pytest.approx(1580.0) and tel == pytest.approx(1580.0)
    assert H["debt_nc"][i] == 540.0 and H["debt_c"][i] == 0.0 and H["deftax"][i] == pytest.approx(600 - 540) and H["ocl"][i] == 330.0
    # the cash flow ties through the financing plug: cash 120 -> 90 in 2025
    assert H["cfo"][i] + H["capex"][i] + H["acq"][i] + H["div_paid"][i] + H["fin_other"][i] == pytest.approx(90 - 120)
    assert H["fin_other"][nc.YEARS.index(2023)] == 0.0                                 # no prior year: no plug
    assert H["shares"][i] == 100.0 and H["dps"][i] == 0.25 and H["price"][i] == 38.0
    blank = nc.history(None)
    assert blank["years_with_data"] == [] and blank["start"] == len(nc.YEARS)


def test_checklist_comes_from_the_scaling_document():
    items = nc.checklist("industrials")
    assert items and any("Perimeter first" in x for x in items)
    assert nc.checklist("salmon") != items and nc.checklist("nonsense") == []


def test_factory_writes_a_scaffold_that_imports_balances_and_builds(tmp_path):
    root = tmp_path / "repo"
    (root / "model_builder").mkdir(parents=True)
    (root / "deck_builder").mkdir()
    (root / "docs" / "rapport").mkdir(parents=True)
    shutil.copy(ROOT / "docs" / "rapport" / "skalering.md", root / "docs" / "rapport" / "skalering.md")
    st = json.loads(FIX.read_text(encoding="utf-8"))
    files = nc.write_all("XSC", "Scaffold Example ASA", "industrials", ["Alloys", "Carbon"], st, root, force=False)
    assert {p.name for p in files} == {"xsc_data.py", "xsc_deck.py", "KILDER.md", "FORSTAAELSE.md"}
    with pytest.raises(FileExistsError):
        nc.write_all("XSC", "Scaffold Example ASA", "industrials", [], st, root)
    text = (root / "model_builder" / "xsc_data.py").read_text(encoding="utf-8")
    assert "SCAFFOLD = True" in text and "TEMPLATE" in text and "PLUG" in text and 'seg_a="Alloys"' in text and "Yahoo Finance" in text
    kilder = (root / "examples" / "XSC" / "data" / "KILDER.md").read_text(encoding="utf-8")
    assert "| Revenue | 1 000 | 1 100 | 1 050 |" in kilder and "oq case export XSC" in kilder and "2026-09-30" in kilder
    forst = (root / "examples" / "XSC" / "data" / "FORSTAAELSE.md").read_text(encoding="utf-8")
    assert "Perimeter first" in forst and "## 6. Hva markedet priser inn" in forst
    deck = (root / "deck_builder" / "xsc_deck.py").read_text(encoding="utf-8")
    assert "CT = dict(" in deck and "deep_dives=[]" in deck
    # the module imports beside the template, balances, and the workbook builds from it
    sys.path.insert(0, str(root / "model_builder"))
    try:
        mod = importlib.import_module("xsc_data")
        d = mod.simulate()
        assert d["rev"][-1] == 1050.0 and d["rev"][0] is None and mod.SCAFFOLD is True and mod.KILL[0][3] is None
        spec = importlib.util.spec_from_file_location("xsc_deck", root / "deck_builder" / "xsc_deck.py")
        dm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dm)
        assert dm.CT["report"]["kind"] == "Initiation" and "Perimeter first" in dm.__doc__
    finally:
        sys.path.remove(str(root / "model_builder"))
        sys.modules.pop("xsc_data", None)
    out, cell_map = tmp_path / "model.xlsx", tmp_path / "map.json"
    env = {**os.environ, "EQR_CASE": "xsc_data", "EQR_MAP": str(cell_map), "PYTHONPATH": str(root / "model_builder") + os.pathsep + os.environ.get("PYTHONPATH", "")}
    res = subprocess.run([sys.executable, "build_model.py", str(out)], cwd=MB, env=env, capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + res.stderr
    assert out.exists() and json.loads(cell_map.read_text(encoding="utf8"))["rows"]


def test_the_cli_runs_and_names_the_next_steps(tmp_path):
    root = tmp_path / "repo"
    for d in ("model_builder", "deck_builder"):
        (root / d).mkdir(parents=True)
    res = subprocess.run([sys.executable, "new_case.py", "XSC", "--name", "Scaffold Example ASA", "--sector", "salmon", "--statements", str(FIX), "--root", str(root)],
                         cwd=MB, capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "SCAFFOLD = True" in res.stdout and "Next:" in res.stdout and "refuses while SCAFFOLD" in res.stdout
    res2 = subprocess.run([sys.executable, "new_case.py", "XSC", "--name", "X", "--statements", str(FIX), "--root", str(root)], cwd=MB, capture_output=True, text=True)
    assert res2.returncode == 2 and "--force" in res2.stderr
    blank = subprocess.run([sys.executable, "new_case.py", "NOPE", "--name", "No Export AS", "--statements", str(tmp_path / "missing.json"), "--root", str(root)],
                           cwd=MB, capture_output=True, text=True)
    assert blank.returncode == 0 and "no statements export" in blank.stderr and "history blank" in blank.stdout


def test_the_report_gate_refuses_a_scaffold():
    sys.path.insert(0, str(ROOT / "deck_builder" / "report"))
    try:
        import rb_gate

        class Mod:
            SCAFFOLD = True

        class Rep:
            mod = Mod()

        msg = rb_gate.scaffold_block(Rep())
        assert msg and "SCAFFOLD" in msg
        Mod.SCAFFOLD = False
        assert rb_gate.scaffold_block(Rep()) is None
    finally:
        sys.path.remove(str(ROOT / "deck_builder" / "report"))
