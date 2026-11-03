# Lærdom fra Elkem – første case utenfor konsum (3. november 2026)

Spørsmålet var om rapportmalen og sektorsjekklisten holder for et syklisk industriselskap. Svaret: malen holder
(alle elleve seksjoner fylles, porten passeres), men seks ting måtte endres eller omgås, og fire ting bør bygges før
neste industricase. Det som overrasket mest, var ikke sektoren, men at selskapet var et annet enn oppdraget beskrev.

## 1. Det som ikke passet – og hva som ble gjort

| # | Problem | Hva som ble gjort | Bør endres i malen |
|---|---|---|---|
| 1 | **Historikken finnes ikke på dagens omfang.** Elkem solgte Silicones og la Iceland til salgs i 2026; bare 2025 er omregnet. Arbeidsboken vil ha sju år; sju år med Silicones ville gitt en «omsetning» som falt fra 46 til 15 mrd. | `HIST_START = 6` (ett år). Divisjonsserien 2021–2025 fra Capital Markets Update ligger i `DIVISION_HISTORY` og brukes i dypdykk og makro. Revisjonssjekken A8 (syklisk topp) kjøres på CMU-serien i `META['reasons']`. | En `PERIMETER_HISTORY`-blokk som rapporten tegner som «historikk på dagens omfang, selskapets egne tall» – malen bør skille mellom *regnskapshistorikk* og *proforma-historikk*. |
| 2 | **Kostnader i prosent av inntekter undervurderer driftsgiringen i en råvareprodusent.** Råvarer og energi koster per tonn, ikke per krone solgt; en prisoppgang faller rett gjennom. | `_unit_cost_build()` i datamodulen regner enhetskostnad × volum og mater arbeidsboken med den avledede prosentbanen per år. Transparent, men utenfor Excel. | En «kostnad per enhet»-modus i Drivers (COGS = volum × enhetskostnad × (1+inflasjon)) ved siden av prosentmodusen. |
| 3 | **Ingen segmentkostnader i arbeidsboken.** Oppdraget ba om pris-, volum- og kostnadsdrivere per segment; arbeidsboken har pris og volum per segment, kostnader på konsernnivå. | Divisjonsøkonomien (marginer, ROCE, EBITDA per kvartal) står i dypdykkene; SOTP per divisjon er en tabell med EST-multipler, ikke `sotp_runs.py` (som bygger på lokasjoner). | Segment-EBITDA som egne rader (volum × pris − volum × enhetskostnad − faste kostnader per segment) og en SOTP-kjøring som leser dem. |
| 4 | **Finansieringshendelser etter balansedagen.** Emisjonen på NOK 1,8 mrd i mai–juni 2026 lå ikke i modellen, som ruller netto gjeld fra 31.12.2025; 2026E-gjeldsgraden brøt kill-kriteriet. | Ny Inputs-celle `eq_issue` (seksjon 7) som reduserer netto gjeld og øker egenkapitalen i første prognoseår. Generell endring, nullverdi for eldre case. | Ferdig. Neste: en rad for oppkjøp/salg av virksomhet i første prognoseår (Iceland og Roussillon). |
| 5 | **Peer-tabellen i WACC-arket var låst til åtte rader.** Tolv peers skrev over median-raden og Blume-cellen; Python og Excel ga ulik WACC. | Tabellen bruker `len(PEERS)`; medianer og notatrader flyttes med. Identisk layout for åtte peers (SATS/eksempel uendret, testene grønne). | Ferdig. |
| 6 | **Etiketter fra treningsstudio.** «Clubs», «members», «ARPM», «country EBITDA before IFRS 16», «revenue per unit (NOK/month)». | `QUARTERS['kpis']`, `seg_ebitda_label`, `seg_volume_label`, `MARKET['loc_label'/'rpu_label']`, `competition[...]['headers']` – med de gamle tekstene som standard. | Ferdig; resten av malen er allerede nøytral. |

Andre observasjoner:

- **Kvartalsserien skifter basis to ganger** (Silicones ut fra Q1 2026, Iceland ut fra Q2 2026, nye divisjoner fra Q3 2026).
  Sju kvartaler på dagens omfang lot seg avlede fra halvårs-, nimåneders- og årstall; divisjonstall finnes bare for tre av dem.
  Malen tåler hull (viser «–»), men sesongsplitten i kvartalsforhåndsvisningen hviler da på ett år.
- **Konsensus finnes ikke fra selskapet.** Yahoo gir omsetning (5–6 analytikere) og EPS (3), ikke EBITDA. Variant-tabellen
  måtte formuleres mot omsetningsvekst og EPS, og «EBITDA mot konsensus» står som ikke tilgjengelig.
- **Prisserier er betalt.** Fastmarkets/CRU/Argus-indeksene er ikke åpne; dypdykket bruker daterte punkter (SunSirs, Mysteel,
  Ferroglobes SEC-filinger, Argus sitert i nyheter). Grafen er ærlig merket «points, not a continuous series».
- **Kill-kriterier på modellrader måles mot siste regnskapsår og første prognoseår.** I et bunnår må tersklene settes så
  bunnåret selv ikke bryter dem; de viktigste kriteriene (Silicon-margin under 5 % i to kvartaler, utfallet av EU-revisjonen)
  er divisjons- eller hendelsesbaserte og står i teksten og i forslaget til research book, ikke i arkene.
- **Omvendt DCF med kurs langt under DCF:** terminalvekst-løseren trengte et bredere intervall (−15 %); verifiseringen måtte
  tåle «ikke løst».
- **Ikke-driftsmessige eiendeler avgjør konklusjonen.** Eiendeler holdt for salg (3,4 mrd) og CO2-kvoter (1,2 mrd) er NOK 13
  per aksje. Malen har felter for dem (associates, other_adj), men rapporten bør vise verdien uten dem like tydelig som med –
  det gjøres i what-if-kjøringene og i «flips».

## 2. Sjekkliste for industri og materialer (lagt inn i docs/rapport/skalering.md)

- [ ] Omfang først: hvilke enheter er solgt, holdt for salg eller omklassifisert de siste to årene, og hvilke år finnes omregnet
- [ ] Historikk: regnskapsår på dagens omfang (ofte 1–2) + selskapets egen divisjonsserie (CMD/CMU) med kilde per lysark
- [ ] Åtte kvartaler på dagens omfang; avled Q1/Q4 fra halvår/9M/år og merk avledningene
- [ ] Volum (tonn) og realisert pris per divisjon; indeksprisene som daterte punkter med kilde; futureskurve (GFEX/ZCE/LME) med dato
- [ ] Kostnad per tonn: råvarer, energi (TWh, sikringsgrad, kontraktenes løpetid), CO2 (kvoter mottatt, kompensasjon mottatt per år)
- [ ] ±10 % på den styrende kostnadsvariabelen regnet med oppgitte mengder; si tydelig når prisen ikke er oppgitt
- [ ] Handelstiltak med forordningsnummer og dato (antidumping, safeguard, CBAM, US AD/CVD)
- [ ] Balansen: covenants, forfall, rating, eiendeler holdt for salg med selskapets egen verdivurdering og følsomhet
- [ ] Kill-kriterier: divisjonsmargin under x % i to kvartaler, gjeldsgrad mot covenant, binær hendelse (tollvedtak) med dato
- [ ] Peers i to–tre grupper (samme råvare, samme kundeledd, nordiske materialer); bruk betaer fra alle, multipler bare der valutaene stemmer
- [ ] Scenarioer som prisbaner (bunn vedvarer / sakte normalisering / normalisering + toll), ikke ±pp på marginen
- [ ] Terminalmargin mot syklussnittet (A8) – på selskapets egen serie når regnskapshistorikken er kort

## 3. Hva som bør bygges før neste industricase

1. Enhetskostnadsmodus og segment-EBITDA i arbeidsboken (punkt 2–3 over).
2. En prisdekk-blokk i datamodulen (`PRICE_DECK`: råvare, enhet, kilde, dato, spot, kurve, modellbane) som revisjonen A9 leser
   direkte i stedet for `META['commodity_deck']`, og som rapporten tegner som «spot – kurve – vår bane».
3. En «perimeterhistorikk»-eksponent i selskapsoversikten (punkt 1).
4. Oppkjøp/salg i første prognoseår (Iceland, Roussillon) som kontant- og EV-effekt med dato.
