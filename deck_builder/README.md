# Deck builder

Builds PowerPoint files from a saved workbook, so every number on a slide is the number in the model.

| Script | Builds | Default output |
|---|---|---|
| `build_deck.py` | The pitch deck: cover, team, the four content slides and a nine-slide appendix | `../Equity_Research_Pitch_Generated.pptx` |
| `build_chartlib.py` | The chart and framework library (23 slides) | `../Equity_Research_Chart_Library_Generated.pptx` |

## Use

1. `pip install -r ../requirements.txt`
2. Save the workbook in Excel after changing it (Excel stores the calculated values the scripts read) with the
   scenario on Base.
3. Run `python build_deck.py` or `python build_chartlib.py` from this folder.

Options of `build_deck.py`: `--model` (workbook), `--map` (its `model_map.json`), `--out`, `--main-only` (cover, team and
the four content slides – the competition's slide limit), `--review` (neutral layout, no team slide and a neutral cover
subtitle – for readers outside the competition) and `--template`.

**Template.** With `--template path/to/case-template.pptx` (default: `../Equity_Research_Pitch_Template.pptx` if it
exists) the slides use the template's layouts and placeholders. With `--template none`, or when the file is missing, the
same layout is drawn on blank slides – same positions, fonts and colours, no logo. `build_chartlib.py` reads the template
path from `EQR_TEMPLATE`.

**Team.** The team slide reads `team/team.json` – `[[name, photo file or null, [line, ...]], ...]` with the photos in
the same folder. The folder is git-ignored; without it (or with `EQR_TEAM=none`) the slide shows placeholders.

## What comes from the model

- Every number, table and chart, including the reverse DCF, consensus comparison, scenario stories, signposts and kill
  criteria (sheets Reverse_DCF, Consensus and Thesis).
- Company text that cannot come from a model – description, management, market facts, risks – comes from a case text
  module chosen with `EQR_CASE` (`sats_data` → `sats_deck.py`). Without one, the template text for the fictional Example
  Company ASA is used.

| File | Contents |
|---|---|
| `deck_core.py` | Slide helpers, native charts and tables, the neutral layout |
| `deck_data.py` | Reads the workbook through `model_map.json` |
| `deck_slides1-3.py` | Cover, team, the four content slides; DCF, scenario, peer, assumption and risk appendix |
| `deck_slides4.py` | Market-view appendix: reverse DCF, thesis tracker, consensus, growth engine |
| `deck_slides3.py` (assumptions) | reads the personnel-cost what-if from `model_builder/whatif_runs*.json` when it exists |
| `deck_slides5.py` | Market overview from company KPIs and sourced facts (used when the case text module has `market`) |
| `deck_slides6.py` | Club economics (company guidance vs. the model), revenue-to-cash bridge and capital allocation, competition and macro (case module keys `unit`, `comp`, `macro`) |
| `retail_slides.py` | Store-chain cases (case module keys `market_retail`, `store_econ`, `targets`, `sotp`, `margin_slide`): market overview, store economics, company targets in place of consensus, sum-of-the-parts of the estate and the roll-out (`model_builder/sotp_runs.py`), margin bridge with inventory vs. peers and the latest half-year, sources and uses of cash |
| `deck_case.py`, `sats_deck.py` | Case text selection; the SATS text |

Optional case keys read by the generic slides: `ipo_price` (football-field marker), `peer_scatter` (EV/EBIT vs. growth with a peer regression instead of the bar chart), `peers_subtitle`, `risk_subtitle`, `growth_subtitle`, `growth_sources`, `cash_why`. Appendix slides are numbered in build order.
| `cl_a1-a3.py`, `cl_b1-b2.py` | The chart library (#1–#9) and the frameworks (#1–#10) |

```bash
EQR_CASE=sats_data python build_deck.py --model ../examples/SATS/SATS_ASA_DCF_Model.xlsx \
    --map ../model_builder/model_map_sats.json --out ../my_sats_deck.pptx
```
