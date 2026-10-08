"""Generate the Pareto-style pitch deck from the Excel model.

Usage (from any folder):
    python build_deck.py
    python build_deck.py --model ../Equity_Research_DCF_Toolkit.xlsx --out ../My_Pitch.pptx
    python build_deck.py --review --out ../My_Pitch_Review.pptx      # neutral layout, no team slide, neutral cover

Requires: pip install python-pptx openpyxl
The model must be saved by Excel (so all formula values are stored) and keep the original sheet layout.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from deck_core import open_template  # noqa: E402
from deck_data import ModelData  # noqa: E402
import deck_slides1 as s1  # noqa: E402
import deck_slides2 as s2  # noqa: E402
import deck_slides3 as s3  # noqa: E402
import deck_slides4 as s4  # noqa: E402
import deck_slides6 as s6  # noqa: E402
import retail_slides as s7  # noqa: E402
import deck_case  # noqa: E402
from deck_case import ct  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--model", default=os.path.join(HERE, "..", "Equity_Research_DCF_Toolkit.xlsx"))
ap.add_argument("--template", default=os.path.join(HERE, "..", "Equity_Research_Pitch_Template.pptx"),
                help="A deck built on the case template (its slides are removed, masters kept). If the file does not "
                     "exist, or with --template none, the deck is drawn on a neutral layout without any logo")
ap.add_argument("--out", default=os.path.join(HERE, "..", "Equity_Research_Pitch_Generated.pptx"))
ap.add_argument("--map", default=os.path.join(HERE, "model_map.json"), help="model_map.json written by build_model.py")
ap.add_argument("--main-only", action="store_true",
                help="Submission version: cover, team and the four content slides only (Pareto rule: max four slides)")
ap.add_argument("--review", action="store_true",
                help="Review edition for readers outside the competition: neutral layout, no team slide, neutral cover subtitle")
args = ap.parse_args()

model, template, out, map_path = (os.path.abspath(p) for p in (args.model, args.template, args.out, args.map))
if args.review:
    template = "none"
    deck_case.CT["cover_sub"] = "Equity research case study – review edition"
os.chdir(HERE)                       # team photos and model_map.json are read relative to this folder
prs = open_template(template)
print("Layout:", "neutral (no template)" if getattr(prs, "_eqr_neutral", False) else template)
d = ModelData(model, map_path)
# company-specific appendix slides need their text block in the case module (sats_deck.py: unit, comp/macro;
# outlet_deck.py: store_econ, targets, market_retail)
case_slides = {s6.unit_economics_slide: "unit", s6.cash_slide: None, s6.competition_macro_slide: "comp",
               s7.store_economics_slide: "store_econ", s7.targets_slide: "targets", s7.cash_slide_retail: "store_econ"}
for fn in (s1.cover, s1.team, s1.company_overview, s1.market_overview, s2.financials, s2.valuation,
           s3.divider, s3.dcf_slide, s4.reverse_dcf_slide, s3.scenario_slide, s4.thesis_slide, s4.consensus_slide, s7.targets_slide,
           s4.growth_engine_slide, s6.unit_economics_slide, s7.store_economics_slide, s6.cash_slide, s7.cash_slide_retail,
           s3.peers_slide, s3.assumptions_slide, s6.competition_macro_slide, s3.risks_slide, s3.guide_slide):
    if fn is s3.guide_slide and ct("skip_guide"):      # a case deck does not need the template guide
        continue
    if fn is s1.team and args.review:                  # no names and photos in the review edition
        continue
    if fn in case_slides and case_slides[fn] and not ct(case_slides[fn]):
        continue
    if fn is s4.consensus_slide and ct("targets"):     # no consensus: the targets slide takes its place
        continue
    if fn is s6.cash_slide and (not ct("unit") or ct("store_econ")):   # the model-only cash slide belongs to a real case too
        continue
    if args.main_only and fn is s3.divider:            # the appendix is Q&A back-up, not part of the submission
        break
    fn(prs, d)
prs.save(out)
print(f"Saved {out} ({len(prs.slides)} slides)")
