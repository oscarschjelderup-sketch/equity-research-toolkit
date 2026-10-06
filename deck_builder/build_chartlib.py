"""Build the chart & framework library from the saved Excel model.

Usage:  python build_chartlib.py [output.pptx]
Requires: pip install python-pptx openpyxl
"""
import sys

import os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
from deck_core import *
from deck_data import ModelData
from deck_slides1 import std
import cl_a1, cl_a2, cl_a3, cl_b1, cl_b2
TPL = os.environ.get("EQR_TEMPLATE", os.path.join(HERE, "..", "Equity_Research_Pitch_Template.pptx"))  # optional case template
NEUTRAL = not os.path.exists(TPL)                  # no template: neutral layout without any logo
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "Equity_Research_Chart_Library_Generated.pptx")
MODEL = os.path.join(HERE, "..", "Equity_Research_DCF_Toolkit.xlsx")
MAP = os.path.join(HERE, "model_map.json")

CHARTS = [("1", "Column and bar charts", "column + CAGR, clustered, stacked, 100% stacked, ranked bar, +/- columns"),
          ("2", "Combination, line and area", "columns + margin line, scenario paths, vs. peers, stacked area, P/E band"),
          ("3", "Pie and doughnut charts", "pie, doughnut with total, market share, twin doughnuts, KPI rings, 100% bar"),
          ("4", "Bridge (waterfall) charts", "revenue bridge, EBIT bridge, EV-to-equity bridge, target price build-up"),
          ("5", "Valuation visuals", "football field, sensitivity heat map, scenario values, EV composition"),
          ("6", "Peer benchmarking", "scatter with trend line, bubble chart, premium/discount bars, radar"),
          ("7", "Share price chart with events", "price vs. index, numbered events, target price, performance table"),
          ("8", "KPI tiles and scorecards", "headline tiles, Harvey-ball scorecard, estimates vs. consensus"),
          ("9", "Market-view charts", "reverse DCF, growth by source, consensus gap, locations")]
FRAMES = [("1", "SWOT analysis", ""), ("2", "Porter's five forces", ""), ("3", "Competitive positioning matrix", ""),
          ("4", "Business model and value chain", ""), ("5", "Market sizing – TAM / SAM / SOM", ""),
          ("6", "Investment thesis in three pillars", ""), ("7", "Timeline and catalyst calendar", ""),
          ("8", "Risk matrix with mitigants", ""), ("9", "Scenario tree and expected value", ""),
          ("10", "Value driver tree (ROIC)", "")]


def cover(prs, d):
    s = new_slide(prs, "Title slide - blue", ph_text={0: "Chart and framework library", 1: "Ready-made visuals for equity research pitch decks",
                                                     12: "Native PowerPoint charts · " + ("neutral layout" if NEUTRAL else "Pareto template") + " · example data"})
    notes(s, "Copy what you need into your pitch deck. Delete this cover.")
    return s


def how_to(prs, d):
    s = std(prs, "Start here", "How to use this library",
            "19 slides with more than 45 editable charts, tables and frameworks – copy, paste, change the data, tell your story",
            ("Neutral layout" if NEUTRAL else "Built on the Pareto case template") + " (Cambria headings, Arial body, navy 003255 / light blue 81B0C0). "
            "Example data: fictional Example Company ASA from the DCF toolkit.")
    x, w = 0.47, 3.9
    panel_header(s, x, 1.40, w, "Three steps", None, size=11)
    steps = [("Copy", "Select the chart (and any labels on top of it), Ctrl+C, then paste into your deck with 'Keep source formatting'."),
             ("Edit data", "Right-click the chart → Edit Data. Type or paste your numbers from the Excel model (Deck_Feed, Output, Analysis)."),
             ("Tell the story", "Rewrite the panel title as a message ('Margins have expanded five years in a row'), not a label ('EBIT margin').")]
    for i, (t, dsc) in enumerate(steps):
        yy = 1.95 + i * 1.12
        circle(s, x, yy, 0.5, fill=NAVY if i != 1 else MIDBLUE, txt=str(i + 1), font_size=14)
        text(s, x + 0.65, yy - 0.05, w - 0.7, 1.0, [(t, {"bold": True, "size": 11.5, "color": NAVY, "space_after": 2}), (dsc, {"size": 9.5})])
    panel(s, x, 5.35, w, 1.45)
    text(s, x + 0.12, 5.42, w - 0.24, 1.35, [("Colour rules", {"bold": True, "size": 10, "color": NAVY, "space_after": 3}),
                                             ("Navy = the company / history. Light blue = peers / forecast. Green and red only for "
                                              "up/down, bull/bear and above/below. Max three colours per chart.", {"size": 9})])
    for col, (title, items, xx) in enumerate([("Charts", CHARTS, 4.67), ("Frameworks", FRAMES, 8.95)]):
        ww = 4.05 if col == 0 else 3.92
        panel_header(s, xx, 1.40, ww, title, None, size=11)
        rows = []
        for num, name, desc in items:
            cells = [f"#{num}", name]
            rows.append(dict(cells=cells, size=9.5, h=0.30, line_bottom="E1E5EA", bolds={0: True, 1: True},
                             colors={0: MIDBLUE, 1: NAVY}, align={0: "l", 1: "l"}))
        table(s, xx, 1.85, ww, rows, [0.5, 3.4])
        if col == 0:
            text(s, xx, 1.97 + 0.30 * len(items), ww, 2.2, [(f"#{n_}  {dsc}", {"size": 8, "color": MUTED, "space_after": 1})
                                                          for n_, _, dsc in items])
    notes(s, "Overview slide – delete before using the library as a source for your own deck.")
    return s


def divider(title, sub):
    def f(prs, d):
        return new_slide(prs, "Chapter slide - dark blue", ph_text={0: title, 1: sub})
    return f


prs = open_template(TPL)
d = ModelData(MODEL, MAP)
for fn in (cover, how_to, divider("Charts", "Native, editable PowerPoint charts"),
           cl_a1.columns_bars, cl_a1.combos_lines, cl_a1.pies, cl_a2.bridges, cl_a2.valuation_visuals, cl_a2.peer_charts,
           cl_a2.share_price, cl_a2.kpi_tables, cl_a3.market_view_charts,
           divider("Frameworks", "Strategy and valuation frameworks built from shapes"),
           cl_b1.swot, cl_b1.porter, cl_b1.positioning, cl_b1.value_chain, cl_b1.market_sizing,
           cl_b2.thesis, cl_b2.timeline, cl_b2.risk_matrix, cl_b2.scenario_tree, cl_b2.driver_tree):
    fn(prs, d)
prs.core_properties.title = "Chart and framework library – equity research"
prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
