"""Case selector: the builder imports its company data from here.

Set the environment variable EQR_CASE to the name of a data module with the same interface as example_data
(e.g. EQR_CASE=sats_data). Default: example_data (the fictional Example Company ASA).
"""
import importlib
import os

CASE = os.environ.get("EQR_CASE", "example_data")
_mod = importlib.import_module(CASE)
globals().update({k: getattr(_mod, k) for k in dir(_mod) if not k.startswith("_")})
