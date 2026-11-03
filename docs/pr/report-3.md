# Report generator, phase 3: SATS with today's numbers

- `model_builder/sats_data.py`: second edition of the case after the Q3 2026 report (27 Oct 2026) – price NOK 43.95
  (30 Oct close), balance sheet 30 Sep 2026, 192.1m shares, consensus from the table SATS publishes (Modular Finance,
  7 contributors, 28 Oct 2026) plus Yahoo EPS; Norway price/mix 2026E 7.5 % (5.5 %) and fixed-cost inflation 2026E 1.0 %
  (1.5 %) to the nine-month run-rate; `QUARTERS` (Q4 2024–Q3 2026 by group and country), `PEER_GROUPS`, `CONSENSUS_Q`,
  `EVENTS`, `HISTORY`. Workbook rebuilt and finalised in Excel: DCF 54.4, target NOK 58 BUY (was 50.7 / 54), bear–bull
  38–78; verify_dcf, stress (21 runs, no error) and what-if runs rerun.
- `deck_builder/sats_deck.py`: the `report` dict – memo, thesis, risks, deep dives (price vs cost, utilisation, targets
  vs delivery, capital returns), competition with dated observations, macro, revisions, data map, flips, unknowns,
  sources, since-last-edition table.
- `examples/SATS/report/`: the 25-page PDF built through the full gate, `prices.json`, both estimate snapshots
  (7 Oct and 2 Nov), `gate.json`, `stress_sats.json`. Screenshots in `docs/img/sats_report_p01/p02.png`.
- `docs/rapport/sats-sammenligning.md`: page by page against the DNB note – as good (spine), better (scenarios, kill
  criteria, reverse DCF, revisions, what we do not know, checks on the record), less good (multi-year KPI series, target
  bridges, city-level competition), not possible (paid consensus and traffic data, price tracker not yet collected).
- Template additions found necessary on a real case: since-last-edition table, signposts calendar, full variant table,
  quarterly charts, peer betas, historical valuation, judgements on the record, sources table; type size up one step.
- The research-book row is not written by the build; a proposed row sits in the private case folder.
- Not redone here: the SATS pitch decks in `examples/SATS` are still the 6 October edition (they build from the new
  workbook in the tests, but the committed PPTX/PDF files were not regenerated); the README figures and the case text
  strings that name dates were updated.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
