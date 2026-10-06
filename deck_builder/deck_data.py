"""Read every number for the deck from the recalculated model (single source of truth)."""
import json
import openpyxl

HC = list("EFGHIJK")
FC = list("LMNOPQRS")
ALL = HC + FC


class ModelData:
    def __init__(self, path="model_final.xlsx", map_path="model_map.json"):
        self.reg = json.load(open(map_path, encoding="utf8"))
        self.wb = openpyxl.load_workbook(path, data_only=True)

    def c(self, sheet, key):
        return self.wb[sheet][self.reg["cells"][f"{sheet}|{key}"]].value

    def row(self, sheet, key, cols=ALL):
        # rows may live on another sheet in newer model versions (e.g. multiples moved from Model to Analysis)
        if f"{sheet}|{key}" not in self.reg["rows"]:
            for alt in ("Model", "Analysis", "Output"):
                if f"{alt}|{key}" in self.reg["rows"]:
                    sheet = alt
                    break
        r = self.reg["rows"][f"{sheet}|{key}"]
        return [self.wb[sheet][f"{c}{r}"].value for c in cols]

    def v(self, sheet, addr):
        return self.wb[sheet][addr].value

    def years(self, cols=ALL):
        return [self.wb["Model"][f"{c}5"].value for c in cols]


# ------------------------------------------------------------------ formatting (English deck)
def num(x, d=0, paren=False):
    if x is None or x == "":
        return "–"
    if isinstance(x, str):
        return x
    if abs(x) < 0.5 * 10 ** (-d) and d == 0:
        return "–" if paren else "0"
    s = f"{abs(x):,.{d}f}"
    if x < 0:
        return f"({s})" if paren else f"-{s}"
    return s


def pct(x, d=1, sign=False, paren=False):
    if x is None or x == "" or isinstance(x, str):
        return "n.m." if isinstance(x, str) else "–"
    s = f"{abs(x) * 100:.{d}f}%"
    if x < 0:
        return f"({s})" if paren else f"-{s}"
    return ("+" if sign and x > 0 else "") + s


def mult(x, d=1):
    if x is None or isinstance(x, str):
        return "n.m."
    if x < 0:
        return "n.m."
    return f"{x:.{d}f}x"


def nok(x, d=0):
    return f"NOK {x:,.{d}f}"
