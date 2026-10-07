# Model builder

Builds the Excel workbook from code. Change the model here, not by hand in Excel, so it can always be rebuilt.

| File | Contents |
|---|---|
| `example_data.py` | The fictional Example Company ASA: history, drivers, scenarios, consensus, stories and kill criteria |
| `sats_data.py` | SATS ASA from the company's quarterly reports and Yahoo Finance – every line sourced |
| `case_data.py` | Picks the data module with the environment variable `EQR_CASE` (default `example_data`) |
| `mb_core.py` | Styling, formula templates and the row/cell register |
| `mb_inputs.py` | Inputs, Hist and Drivers (sections A–F) |
| `mb_model.py` | Model (including the location engine), DCF and WACC |
| `mb_fin.py` | Output (income statement, balance sheet, cash flow) and Analysis |
| `mb_val.py` | Sensitivity (tables 1–5), Comps and Football |
| `mb_market.py` | Reverse_DCF, Consensus and Thesis |
| `mb_out.py` | Dashboard, Deck_Feed, Checks and the Guide sheet |
| `mb_nav.py` | Cover and the section divider sheets |
| `build_model.py` | Builds the workbook in two passes (layout, then formulas) and writes the cell map |
| `excel_finalize.py` | Opens the workbook in Excel, creates the data tables, recalculates and checks for errors (Windows) |
| `verify_dcf.py` | Recalculates the forecast and DCF in Python and runs the reverse-DCF round trips |
| `stress_test.py` | Flips switches and scenarios in Excel and reports the checks for each (Windows) |
| `whatif_runs.py` | One-at-a-time sensitivities: value, target price and rating (Windows); writes `EQR_WHATIF` (default `whatif_runs_sats.json`), which the deck's assumptions slide reads |

## Build

```bash
pip install -r ../requirements.txt
python build_model.py model_raw.xlsx
python excel_finalize.py model_raw.xlsx model_final.xlsx
python verify_dcf.py
python stress_test.py
```

`build_model.py` also writes `model_map.json` (every named row and cell), which the deck builder uses to find values –
copy it to `deck_builder/` after a layout change. Do not insert or delete rows in the workbook by hand: the map points
to fixed cells.

For a case, set the data module and keep its files apart from the template's:

```bash
export EQR_CASE=sats_data EQR_MAP=model_map_sats.json EQR_MODEL=sats_final.xlsx
python build_model.py sats_raw.xlsx
python excel_finalize.py sats_raw.xlsx sats_final.xlsx
python verify_dcf.py
python stress_test.py
python whatif_runs.py
```

On Windows `cmd` use `set EQR_CASE=sats_data` and so on. If Excel automation fails with `CLSIDToClassMap`, delete
`%LOCALAPPDATA%\Temp\gen_py` (a generated cache that temp clean-ups can corrupt) and run again.

## A new company

Copy `sats_data.py` to `<company>_data.py` and fill in the same keys:

- `HIST` – seven years of reported figures (costs negative), balance sheet and condensed cash flow, KPIs (volume and
  locations per segment), shares, dividends and year-end prices. `simulate()` asserts that every balance sheet balances
  and every cash flow ties to the change in cash.
- `MARKET` – share price, shares, net debt and leases from the latest report, dates, segment names, peer basis.
- `BASE` – forecast drivers for eight years; `SCENARIO_ADJ` – bear/base/bull adjustments; `TERMINAL`, `WACC_INPUTS`,
  `COST_CAPITAL` (fixed cost shares, leverage target, buybacks), `ENGINE` (revenue build, ramp-up curve).
- `CONSENSUS`, `VARIANT` – consensus inputs (`None` shows as n.a.) and where we differ; `SCENARIO_STORIES`, `KILL` –
  stories, signposts and kill criteria; `PEERS` – the peer table (blank multiples are ignored).

Slide text for the company goes in `deck_builder/<company>_deck.py`.

## Version history

- **3.0** – case data modules (`EQR_CASE`) and the SATS ASA case; dates, segment names and peer settings from the data
  module; blank history values, missing peer multiples and missing consensus years are handled; the verification scripts
  read their base values from the model.
- **2.2** – location engine; Reverse_DCF (margin in closed form, growth by interpolation, WACC and terminal growth by
  bisection); Consensus with the variant perception; Thesis with stories and kill criteria; 30 checks.
- **2.1** – growth capex, fixed and variable costs, a WACC that follows the balance sheet with buybacks, a rating
  against the cost of equity, a football field in values today.
