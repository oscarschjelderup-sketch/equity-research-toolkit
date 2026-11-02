# Report generator, phase 2: the template

- `deck_builder/build_report.py` + `deck_builder/report/`: a 25–40-page research report (HTML → PDF through headless
  Chromium) built from the saved workbook, `<case>_data.py` and the `report` dict of `<case>_deck.py`. Eleven sections
  as specified: front page (rating, target, key figures, next event, estimate changes, key figures 2021–2028E),
  investment case (target fan, methodology, risks both ways, variant perception, scenarios as stories, kill criteria),
  company overview, quarter preview (seasonality split of the annual model, consensus where public), deep dives,
  competition per market, macro, estimate revisions (against the stored previous build), valuation (DCF, reverse DCF with
  the case gate, sensitivities, SOTP, peer groups, own-history multiples, implied multiples at ten prices, football
  field), full statements and drivers, what we do not know (data map, what-if ranking, stress tests), disclosures with
  the build gate, the 30 workbook checks and the 30-point audit.
- **Build gate** (`rb_gate.py`): Checks sheet, `verify_dcf.py` (parsed: Python = Excel value, row diffs, four reverse-DCF
  round trips), the audit and case gate, `stress_test.py` (now also writes `stress_<case>.json`). A failing gate stops the
  build with exit code 2; `--skip-gate` is visible as a banner on the page.
- **Rules in code:** every exhibit must carry a source and a date (`exhibit()` raises otherwise); estimate columns carry an
  EST mark; a value that is not in the workbook or the case module prints as *not available* / a dashed gap, never a
  number; consensus is shown only where it is public.
- `example_deck.py` and the `QUARTERS`, `PEER_GROUPS`, `CONSENSUS_Q`, `HISTORY`, `META` blocks of `example_data.py`:
  a fully fictional case that fills every section, so the template is tested in CI without SATS data.
- Tests (`tests/test_report.py`): every section present, every exhibit sourced and dated, EST marks, "not available", no
  NaN, the estimates store feeding the revisions table on a second build, the gate refusing a failing model, and the PDF
  page count where a browser exists.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
