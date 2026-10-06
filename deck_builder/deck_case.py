"""Case selector for the deck: company-specific narrative text.

Set the environment variable EQR_CASE to the data module used for the model (e.g. EQR_CASE=sats_data). The deck then
reads its texts from <case>_deck.py in this folder (sats_data -> sats_deck.py). Without a case module the template texts
for the fictional Example Company ASA are used.
"""
import importlib
import os

CASE = os.environ.get("EQR_CASE", "example_data")
try:
    CT = importlib.import_module(CASE.replace("_data", "") + "_deck").CT
except ImportError:
    CT = {}


def ct(key, default=None):
    """Case text for `key`, or the template default."""
    return CT.get(key, default)


def case_fn(t):
    """Apply the case's footnote substitutions (e.g. replace 'Figures are illustrative.' with real sources)."""
    if not t:
        return t
    for old, new in CT.get("footnote_subs", []):
        t = t.replace(old, new)
    return t
