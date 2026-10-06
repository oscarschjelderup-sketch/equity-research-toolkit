"""Output (linked financial statements) and Analysis (ratios) sheets – Campari style."""
from mb_core import *

OUTPUT = TS("Output", start_row=7)
ANALYSIS = TS("Analysis", start_row=7)


def _output_spec():
    t = OUTPUT
    o = lambda e: fx("Output", e)
    L = lambda k: o(f"~{k}~")                      # plain link to the Model row with the same key
    t.section("Income statement")
    t.row("rev", "Revenue", "NOKm", bold=True, hist=L("is_rev"), fc=L("is_rev"))
    t.row("g_rev", "Growth", "%", fmt=F_PCT, italic=True, hist_from=1, hist=o("{rev}/[rev]-1"), fc=o("{rev}/[rev]-1"))
    t.blank()
    t.row("cogs", "Cost of goods sold", "NOKm", hist=L("cogs"), fc=L("cogs"))
    t.row("gp", "Gross profit", "NOKm", bold=True, line=True, hist=L("gp"), fc=L("gp"))
    t.row("gm", "Margin", "%", fmt=F_PCT, italic=True, hist=o("{gp}/{rev}"), fc=o("{gp}/{rev}"))
    t.blank()
    t.row("pers", "Personnel expenses", "NOKm", hist=L("pers"), fc=L("pers"))
    t.row("oth", "Other operating expenses", "NOKm", hist=L("oth"), fc=L("oth"))
    t.row("ebitda", "EBITDA", "NOKm", bold=True, line=True, hist=L("ebitda"), fc=L("ebitda"))
    t.row("ebitda_m", "Margin", "%", fmt=F_PCT, italic=True, hist=o("{ebitda}/{rev}"), fc=o("{ebitda}/{rev}"))
    t.blank()
    t.row("da", "D&A – owned assets", "NOKm", hist=L("da"), fc=L("da"))
    t.row("rou_dep", "Depreciation – right-of-use assets", "NOKm", hist=L("rou_dep"), fc=L("rou_dep"))
    t.row("special", "Impairments and special items", "NOKm", hist=L("special"), fc=L("special"))
    t.row("ebit", "EBIT", "NOKm", bold=True, line=True, hist=L("ebit"), fc=L("ebit"))
    t.row("ebit_m", "Margin", "%", fmt=F_PCT, italic=True, hist=o("{ebit}/{rev}"), fc=o("{ebit}/{rev}"))
    t.blank()
    t.row("netfin", "Net financial items excl. leases", "NOKm", hist=L("netfin"), fc=L("netfin"))
    t.row("lease_int", "Interest on lease liabilities", "NOKm", hist=L("lease_int"), fc=L("lease_int"))
    t.row("pbt", "Profit before tax", "NOKm", bold=True, line=True, hist=L("pbt"), fc=L("pbt"))
    t.blank()
    t.row("tax", "Income tax", "NOKm", hist=L("tax"), fc=L("tax"))
    t.row("np", "Net profit", "NOKm", bold=True, line=True, hist=L("np"), fc=L("np"))
    t.row("min_pl", "Minority interests", "NOKm", hist=L("min_pl"), fc=L("min_pl"))
    t.row("np_sh", "Net profit to shareholders", "NOKm", key_row=True, hist=L("np_sh"), fc=L("np_sh"))
    t.row("np_m", "Margin", "%", fmt=F_PCT, italic=True, hist=o("{np_sh}/{rev}"), fc=o("{np_sh}/{rev}"))
    t.blank()
    t.sub("Memo: pre-IFRS 16 earnings used in the valuation")
    t.row("ebitdaal", "EBITDAaL (EBITDA after lease payments)", "NOKm", hist=L("ebitdaal"), fc=L("ebitdaal"))
    t.row("ebit_adj", "EBIT adj. (pre-IFRS 16, excl. special items)", "NOKm", bold=True, hist=L("ebit_adj"), fc=L("ebit_adj"))
    t.row("ebit_adj_m", "Margin", "%", fmt=F_PCT, italic=True, hist=o("{ebit_adj}/{rev}"), fc=o("{ebit_adj}/{rev}"))
    t.row("eps", "EPS", "NOK", fmt=F_NOK, hist=L("eps"), fc=L("eps"))
    t.row("dps", "DPS", "NOK", fmt=F_NOK, hist=L("dps"), fc=L("dps"))
    t.blank()
    # ------------------------------------------------------------------ balance sheet
    t.section("Balance sheet – capital employed format")
    t.row("nwc", "Net working capital", "NOKm", hist=L("nwc"), fc=L("nwc"))
    t.row("ppe", "PP&E and intangibles excl. goodwill", "NOKm", hist=L("ppe"), fc=L("ppe"))
    t.row("gw", "Goodwill", "NOKm", hist=L("gw"), fc=L("gw"))
    t.row("ic", "Invested capital (pre-IFRS 16)", "NOKm", key_row=True, hist=o("{nwc}+{ppe}+{gw}"), fc=o("{nwc}+{ppe}+{gw}"))
    t.blank()
    t.row("rou", "Right-of-use assets", "NOKm", hist=L("rou"), fc=L("rou"))
    t.row("other_nca", "Other non-current assets", "NOKm", hist=L("other_nca"), fc=L("other_nca"))
    t.row("nce", "Net capital employed", "NOKm", key_row=True,
          hist=o("{ic}+{rou}+{other_nca}"), fc=o("{ic}+{rou}+{other_nca}"))
    t.blank()
    t.row("nibd", "Net interest-bearing debt excl. leases", "NOKm", hist=L("nibd"), fc=L("nibd"))
    t.row("leases", "Lease liabilities", "NOKm", hist=L("leases"), fc=L("leases"))
    t.row("nibd_incl", "Net debt incl. leases", "NOKm", bold=True, line=True,
          hist=o("{nibd}+{leases}"), fc=o("{nibd}+{leases}"))
    t.blank()
    t.row("deftax", "Deferred tax and other non-current liabilities", "NOKm", hist=L("deftax"), fc=L("deftax"))
    t.blank()
    t.row("equity", "Equity to shareholders", "NOKm", hist=L("equity"), fc=L("equity"))
    t.row("min_bs", "Minority interests", "NOKm", hist=L("min_bs"), fc=L("min_bs"))
    t.row("tot_eq", "Total equity", "NOKm", bold=True, line=True, hist=o("{equity}+{min_bs}"), fc=o("{equity}+{min_bs}"))
    t.blank()
    t.row("tfi", "Total funds invested", "NOKm", key_row=True,
          hist=o("{nibd_incl}+{deftax}+{tot_eq}"), fc=o("{nibd_incl}+{deftax}+{tot_eq}"))
    t.row("bs_check", "Check (capital employed – funds invested)", "NOKm", fmt=F_NUM1, check=True,
          hist=o("ROUND({nce}-{tfi},1)"), fc=o("ROUND({nce}-{tfi},1)"))
    t.blank()
    # ------------------------------------------------------------------ cash flow
    t.section("Cash flow statement")
    t.row("cf_ebitdaal", "EBITDAaL", "NOKm", hist_from=1, hist=o("{ebitdaal}"), fc=o("{ebitdaal}"))
    t.row("cf_tax", "Income tax", "NOKm", hist_from=1, hist=o("{tax}"), fc=o("{tax}"))
    t.row("cf_fin", "Net financial items excl. leases", "NOKm", hist_from=1, hist=o("{netfin}"), fc=o("{netfin}"))
    t.row("cf_special", "Special items", "NOKm", hist_from=1, hist=o("{special}"), fc=o("{special}"))
    t.row("cf_nwc", "Change in net working capital", "NOKm", hist_from=1, hist=o("-~dnwc~"), fc=o("-~dnwc~"))
    t.row("cf_other_op", "Other operating items (reported history)", "NOKm", hist_from=1,
          hist=o("%cfo%+%lease_pay%-SUM({cf_ebitdaal}:{cf_nwc})"), fc=lambda c, p, i: "=0",
          note="History: difference between reported cash flow from operations and the lines above")
    t.row("cfo_al", "Cash flow from operations after leases", "NOKm", bold=True, line=True, hist_from=1,
          hist=o("SUM({cf_ebitdaal}:{cf_other_op})"), fc=o("SUM({cf_ebitdaal}:{cf_other_op})"))
    t.blank()
    t.row("cf_capex", "Capital expenditure", "NOKm", hist_from=1, hist=o("~capex~"), fc=o("~capex~"))
    t.row("fcfe", "Free cash flow (after leases, interest and tax)", "NOKm", key_row=True, hist_from=1,
          hist=o("{cfo_al}+{cf_capex}"), fc=o("{cfo_al}+{cf_capex}"))
    t.blank()
    t.row("cf_acq", "Acquisitions and disposals", "NOKm", hist_from=1, hist=o("%acq%"), fc=lambda c, p, i: "=0")
    t.row("cf_div", "Dividends paid", "NOKm", hist_from=1, hist=o("~div_paid~"), fc=o("~div_paid~"))
    t.row("cf_bb", "Share buybacks", "NOKm", hist_from=1, hist=lambda c, p, i: "=0", fc=o("~buyback~"),
          note="Forecast: cash above the target leverage on Drivers (section E) when the buyback switch is on")
    t.row("cf_other", "Other items (reported history)", "NOKm", hist_from=1,
          hist=o("([nibd]-{nibd})-({fcfe}+{cf_acq}+{cf_div}+{cf_bb})"), fc=lambda c, p, i: "=0",
          note="History: balancing item so the statement ties to the reported change in net debt")
    t.row("d_nibd", "Decrease / (increase) in net interest-bearing debt", "NOKm", bold=True, line=True, hist_from=1,
          hist=o("{fcfe}+{cf_acq}+{cf_div}+{cf_bb}+{cf_other}"), fc=o("{fcfe}+{cf_acq}+{cf_div}+{cf_bb}+{cf_other}"))
    t.blank()
    t.row("nibd_open", "Net interest-bearing debt – opening", "NOKm", hist_from=1, hist=o("[nibd]"), fc=o("[nibd]"))
    t.row("nibd_close", "Net interest-bearing debt – closing", "NOKm", key_row=True, hist_from=1,
          hist=o("{nibd_open}-{d_nibd}"), fc=o("{nibd_open}-{d_nibd}"))
    t.row("cf_check", "Check (closing NIBD – balance sheet)", "NOKm", fmt=F_NUM1, check=True, hist_from=1,
          hist=o("ROUND({nibd_close}-{nibd},1)"), fc=o("ROUND({nibd_close}-{nibd},1)"))
    t.blank()
    t.sub("Memo")
    t.row("fcff", "Free cash flow to firm (unlevered – used in the DCF)", "NOKm", hist_from=1, hist=L("fcff"), fc=L("fcff"))


def _analysis_spec():
    t = ANALYSIS
    a = lambda e: fx("Analysis", e)
    L = lambda k: a(f"~{k}~")
    sw = "@peer_lease=1"
    gro = lambda k: a(f'IF(^{k}^<=0,"n.m.",~{k}~/^{k}^-1)')
    t.section("Growth (year on year)")
    t.row("g_rev", "Revenue", "%", fmt=F_PCT, bold=True, hist_from=1, hist=L("grev"), fc=L("grev"))
    t.row("g_vol", "– of which volume", "%", fmt=F_PCT, italic=True, indent=1, hist_from=1, hist=L("g_volc"), fc=L("g_volc"))
    t.row("g_new", "of which new locations (capacity)", "%", fmt=F_PCT, italic=True, indent=2, hist_from=1,
          hist=L("g_newc"), fc=L("g_newc"))
    t.row("g_lfl", "of which like-for-like volume", "%", fmt=F_PCT, italic=True, indent=2, hist_from=1,
          hist=L("g_lflc"), fc=L("g_lflc"))
    t.row("g_px", "– of which price/mix", "%", fmt=F_PCT, italic=True, indent=1, hist_from=1, hist=L("g_pxc"), fc=L("g_pxc"))
    t.row("g_ebitda", "EBITDA", "%", fmt=F_PCT, hist_from=1, hist=gro("ebitda"), fc=gro("ebitda"))
    t.row("g_ebit", "EBIT adj.", "%", fmt=F_PCT, hist_from=1, hist=gro("ebit_adj"), fc=gro("ebit_adj"))
    t.row("g_eps", "EPS", "%", fmt=F_PCT, hist_from=1, hist=L("g_eps"), fc=L("g_eps"))
    t.row("g_dps", "DPS", "%", fmt=F_PCT, hist_from=1, hist=gro("dps"), fc=gro("dps"))
    t.row("g_fcff", "Free cash flow to firm", "%", fmt=F_PCT, hist_from=2, hist=gro("fcff"), fc=gro("fcff"))
    t.blank()
    t.section("Profitability")
    t.row("gm", "Gross margin", "%", fmt=F_PCT, hist=L("gm"), fc=L("gm"))
    t.row("ebitda_m", "EBITDA margin (reported)", "%", fmt=F_PCT, hist=L("ebitda_m"), fc=L("ebitda_m"))
    t.row("ebitdaal_m", "EBITDAaL margin", "%", fmt=F_PCT, hist=L("ebitdaal_m"), fc=L("ebitdaal_m"))
    t.row("ebit_adj_m", "EBIT adj. margin", "%", fmt=F_PCT, bold=True, hist=L("ebit_adj_m"), fc=L("ebit_adj_m"))
    t.row("np_m", "Net profit margin", "%", fmt=F_PCT, hist=L("np_m"), fc=L("np_m"))
    t.row("tax_eff", "Effective tax rate", "%", fmt=F_PCT, hist=a("IF(~pbt~=0,0,-~tax~/~pbt~)"), fc=a("IF(~pbt~=0,0,-~tax~/~pbt~)"))
    t.blank()
    t.section("Returns and capital efficiency (DuPont: ROIC = NOPAT margin x capital turnover)")
    t.row("nopat_m", "NOPAT margin", "%", fmt=F_PCT, hist=a("~nopat~/~is_rev~"), fc=a("~nopat~/~is_rev~"))
    t.row("ic_turn", "Capital turnover (revenue / average invested capital)", "x", fmt=F_MULT2, hist_from=1,
          hist=a("~is_rev~/AVERAGE(^ic^,~ic~)"), fc=a("~is_rev~/AVERAGE(^ic^,~ic~)"))
    t.row("roic", "ROIC", "%", fmt=F_PCT, key_row=True, hist_from=1, hist=L("roic"), fc=L("roic"))
    wacc = lambda c, p, i: f"={S('WACC', 'wacc')}"
    t.row("wacc", "WACC", "%", fmt=F_PCT, hist_from=1, hist=wacc, fc=wacc)
    t.row("spread", "ROIC – WACC spread", "%", fmt=F_PCT, bold=True, hist_from=1, hist=a("{roic}-{wacc}"), fc=a("{roic}-{wacc}"),
          note="Positive spread = value creation")
    t.row("roe", "Return on equity", "%", fmt=F_PCT, hist_from=1, hist=L("roe"), fc=L("roe"))
    t.blank()
    t.section("Cash flow quality and investment intensity")
    t.row("cconv", "Cash conversion (FCFF / EBITDAaL)", "%", fmt=F_PCT, hist_from=1, hist=L("cconv"), fc=L("cconv"))
    t.row("fcff_m", "FCFF margin", "%", fmt=F_PCT, hist_from=1, hist=L("fcff_m"), fc=L("fcff_m"))
    t.row("capex_s", "Capex / revenue", "%", fmt=F_PCT, hist=a("-~capex~/~is_rev~"), fc=a("-~capex~/~is_rev~"))
    t.row("capex_da", "Capex / D&A", "x", fmt=F_MULT2, hist=a("IF(~da~=0,0,~capex~/~da~)"), fc=a("IF(~da~=0,0,~capex~/~da~)"))
    t.row("net_inv_s", "Net reinvestment / revenue (capex – D&A + increase in NWC)", "%", fmt=F_PCT, hist_from=1,
          hist=a("~net_inv~/~is_rev~"), fc=a("~net_inv~/~is_rev~"))
    t.row("nwc_s", "Net working capital / revenue", "%", fmt=F_PCT, hist=a("~nwc~/~is_rev~"), fc=a("~nwc~/~is_rev~"))
    t.row("rev_loc", "Revenue per average location (NOKm)", "NOKm", fmt=F_NUM1, hist_from=1, hist=L("rev_loc"), fc=L("rev_loc"))
    t.blank()
    t.section("Leverage and coverage")
    t.row("lev", "NIBD / EBITDAaL", "x", fmt=F_MULT, bold=True, hist=L("lev"), fc=L("lev"))
    t.row("lev_incl", "Net debt incl. leases / EBITDA", "x", fmt=F_MULT,
          hist=a("IF(~ebitda~=0,0,~nibd_incl~/~ebitda~)"), fc=a("IF(~ebitda~=0,0,~nibd_incl~/~ebitda~)"))
    t.row("int_cov", "Interest cover (EBIT adj. / net financial expense)", "x", fmt=F_MULT,
          hist=a('IF(~netfin~>=0,"n.m.",-~ebit_adj~/~netfin~)'), fc=a('IF(~netfin~>=0,"n.m.",-~ebit_adj~/~netfin~)'))
    t.row("gearing", "NIBD / equity", "x", fmt=F_MULT2, hist=a("~nibd~/~equity~"), fc=a("~nibd~/~equity~"))
    t.blank()
    t.section("Per share data (NOK)")
    t.row("eps", "EPS", "NOK", fmt=F_NOK, bold=True, hist=L("eps"), fc=L("eps"))
    t.row("dps", "DPS", "NOK", fmt=F_NOK, hist=L("dps"), fc=L("dps"))
    t.row("payout", "Payout ratio", "%", fmt=F_PCT, italic=True, hist=L("payout"), fc=L("payout"))
    t.row("shares", "Diluted shares (m)", "m", fmt=F_NUM1, hist=L("shares"), fc=L("shares"), note="Reduced by buybacks in the forecast")
    t.row("bvps", "Book value per share", "NOK", fmt=F_NOK, hist=a("~equity~/~shares~"), fc=a("~equity~/~shares~"))
    fps = lambda c, p, i: None if i == 0 else f"=Output!{c}{ROWS[('Output', 'fcfe')]}/Model!{c}{ROWS[('Model', 'shares')]}"
    fps_fc = lambda c, p, i: f"=Output!{c}{ROWS[('Output', 'fcfe')]}/Model!{c}{ROWS[('Model', 'shares')]}"
    t.row("fcfps", "Free cash flow per share", "NOK", fmt=F_NOK, hist=fps, fc=fps_fc)
    t.blank()
    t.section("Valuation multiples at the current share price")
    t.row("mcap", "Market capitalisation", "NOKm", hist=a("@mcap"), fc=a("@mcap"))
    t.row("ev_ex", "Enterprise value excl. leases", "NOKm", hist=a("@ev_ex"), fc=a("@ev_ex"))
    t.row("ev_incl", "Enterprise value incl. leases", "NOKm", hist=a("@ev_incl"), fc=a("@ev_incl"))
    evs = f"IF({sw},{{ev_incl}},{{ev_ex}})/~is_rev~"
    eve = f"IF({sw},{{ev_incl}}/~ebitda~,{{ev_ex}}/~ebitdaal~)"
    evb = f"IF({sw},{{ev_incl}}/(~ebit_adj~-~lease_int~),{{ev_ex}}/~ebit_adj~)"
    pe = 'IF(~eps~<=0,"n.m.",@price/~eps~)'
    t.row("evs", "EV / Sales", "x", fmt=F_MULT2, hist=a(evs), fc=a(evs), note="EV basis follows the peer-multiple switch on Inputs")
    t.row("evebitda", "EV / EBITDA", "x", fmt=F_MULT, hist=a(eve), fc=a(eve),
          note="IFRS 16 basis: EV incl. leases / reported EBITDA; otherwise EV excl. leases / EBITDAaL")
    t.row("evebit", "EV / EBIT", "x", fmt=F_MULT, bold=True, hist=a(evb), fc=a(evb))
    t.row("pe", "P / E", "x", fmt=F_MULT, bold=True, hist=a(pe), fc=a(pe))
    t.row("pb", "P / B", "x", fmt=F_MULT, hist=a("@price/{bvps}"), fc=a("@price/{bvps}"))
    t.row("fcf_yield", "FCF yield (FCFE / market cap)", "%", fmt=F_PCT, hist_from=1,
          hist=a("(~fcff~+~netfin~*(1-@norm_tax))/{mcap}"), fc=a("(~fcff~+~netfin~*(1-<tax>))/{mcap}"))
    t.row("div_yield", "Dividend yield", "%", fmt=F_PCT, hist=a("~dps~/@price"), fc=a("~dps~/@price"))
    t.blank()
    t.section("Company metrics on peer basis (used by Comps – basis follows the Inputs switch)")
    t.row("pm_rev", "Revenue", "NOKm", hist=a("~is_rev~"), fc=a("~is_rev~"))
    t.row("pm_ebitda", "EBITDA (peer basis)", "NOKm", hist=a(f"IF({sw},~ebitda~,~ebitdaal~)"), fc=a(f"IF({sw},~ebitda~,~ebitdaal~)"))
    t.row("pm_ebit", "EBIT (peer basis, excl. special items)", "NOKm",
          hist=a(f"IF({sw},~ebit_adj~-~lease_int~,~ebit_adj~)"), fc=a(f"IF({sw},~ebit_adj~-~lease_int~,~ebit_adj~)"))
    t.row("pm_np", "Net profit to shareholders", "NOKm", hist=a("~np_sh~"), fc=a("~np_sh~"))
    t.row("pm_eps", "EPS", "NOK", fmt=F_NOK, hist=a("~eps~"), fc=a("~eps~"))
    t.row("pm_ebit_m", "EBIT margin (peer basis)", "%", fmt=F_PCT, italic=True,
          hist=a("{pm_ebit}/{pm_rev}"), fc=a("{pm_ebit}/{pm_rev}"))


_output_spec()
_analysis_spec()


def write_output(wb):
    ws = wb["Output"]
    sheet_title(ws, "Output Financial Statements",
                "Link-only presentation of the income statement, balance sheet and cash flow – no assumptions are entered here.")
    ts_header(ws, "Output")
    OUTPUT.write(ws)


def write_analysis(wb):
    ws = wb["Analysis"]
    sheet_title(ws, "Financial Analysis",
                "Growth, profitability, returns, leverage, per-share data and valuation multiples.")
    ts_header(ws, "Analysis")
    ANALYSIS.write(ws)
