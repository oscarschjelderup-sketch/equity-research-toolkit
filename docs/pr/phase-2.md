# Phase 2: distil the research into rules and checks

**What**
- `ANALYSE.md`: rules that always apply (MAR art. 20 / 2016/958 / VPFF Standard 3 disclosures, conflicts, inside
  information; lease basis, EV bridge, shares, dates, PwC/FFN cost-of-capital parameters, terminal-value identities;
  the reverse-DCF gate), what separates the best (with the caveat that Norwegian rankings are votes, not accuracy),
  sector rules for salmon, E&P, oil service, shipping, banks, consumer and tech, the 30 failure modes as checks, and
  a writing template for the deck and the prep page.
- `model_builder/audit.py`: the 30 failure modes as checks with PASS/WARN/FLAG/FAIL/MISSING/N/A/JUSTIFIED; a case's
  META supplies sector, guidance, conflicts, disclosures and written reasons for judgement flags.
- `verify_dcf.py` prints the audit; `stress_test.py` adds research-driven stresses (margin reversion, NWC held,
  WACC +1pp, RONIC = WACC, +15pp tax for salmon/E&P).
- `model_builder/case_gate.py` + CI test: no reverse-DCF gap, no case.
- `sats_data.py` gets its META block.

**Evidence**
- `pytest`: 16 passed (incl. the audit on the committed SATS workbook: no FAIL, no unanswered FLAG).
- SATS and the private case: no hard failures; five judgement flags each, answered from the cases' text; both turn SELL at
  the last-3-year mean margin (SATS NOK 30.5).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
