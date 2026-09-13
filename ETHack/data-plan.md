---
edit: owned
last_edited: 2026-09-12T12:53:18 CET
changes: 0
type: project-note
status: proposed
---
# The data plan

Every source here is **free, public, and government-published**. No paid feed, no scraping, no login. Verified from documentation on 12 Sep 2026, **not live-tested** (the session's network policy blocked direct API calls), so the first thing the data owner does is smoke-test every endpoint in section 5.

## 1. The insight that makes 24 hours enough

Two facts do most of the work.

**Revenue for every US filer is one HTTP request.** The SEC's XBRL **frames API** returns one fact per reporting entity for a whole period:

```
https://data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2024.json
```

Not 500 calls. One. Free, no API key, no auth.

**Emissions coverage can be 100% by construction.** EPA publishes **Supply Chain Greenhouse Gas Emission Factors**, an environmentally-extended input-output model giving kg CO2e per US dollar for 1,016 NAICS-6 commodities. Two CSVs, public domain. Multiply a company's spend by its industry factor and you get a modelled footprint for every company in the index, including the ones that disclose nothing.

So we never have a coverage hole. We have disclosed numbers where they exist and modelled numbers everywhere else, and **the gap between the two is itself a result.**

## 2. The stack

| Layer | Source | Gives | Cost | Notes |
|---|---|---|---|---|
| Index membership | Wikipedia "List of S&P 500 companies" | ticker, company, GICS sector, CIK | free | do this first, it is five minutes |
| Ticker to CIK | `sec.gov/files/company_tickers.json` | the join key | free | canonical, from the regulator |
| Revenue | SEC XBRL **frames** API | denominator, audited | free | see the tag trap, section 4 |
| Sector mapping | GICS from Wikipedia, NAICS from SEC submissions (SIC) | links companies to EEIO factors | free | SIC to NAICS crosswalk needed |
| **Scope 1, disclosed** | EPA GHGRP facility data + **Reported Parent Companies (xlsb)** | real reported US facility emissions rolled up to parent | free | mandatory reporting, the only hard US emissions data |
| **Scope 1/2/3, modelled** | EPA Supply Chain GHG Emission Factors v1.3, NAICS-6 | kg CO2e per 2022 USD, splits supply-chain from direct | free | this is the coverage guarantee |
| Market cap for EVIC | price × shares outstanding | second denominator | free-ish | the awkward one, first thing we cut |

## 3. What each boundary is built from

| Boundary | Disclosed path | Modelled path |
|---|---|---|
| A, Scope 1 | GHGRP parent rollup | EEIO direct factor × revenue |
| B, Scope 1+2 | GHGRP + company-reported purchased electricity (thin) | EEIO including electricity |
| C, Scope 1+2+3 | almost nobody discloses this freely | EEIO supply-chain factor × revenue |

**The weak link is Scope 2.** GHGRP captures the *generator's* emissions, not the buyer's purchased electricity, and few companies disclose theirs in a machine-readable way. Boundary B will lean modelled. Say so on the slide rather than letting a judge find it.

**Bonus dimension we get for free:** disclosed versus modelled is *itself* a specification choice. A company whose disclosed number sits far below its EEIO-modelled number is either genuinely efficient or reporting selectively, and the framework cannot tell you which. Naming that honestly is worth more than pretending it can.

## 4. Traps that will eat hours if nobody warns you

1. **The revenue tag is not one tag.** Companies use `Revenues`, `RevenueFromContractWithCustomerExcludingAssessedTax`, `SalesRevenueNet` and others depending on filing year and industry. Build a **fallback chain** of tags, take the first that resolves, and log which tag each company used. Budget 45 minutes for this alone.
2. **Parent-company name matching is the single biggest time sink.** "Exxon Mobil Corporation" in GHGRP versus "ExxonMobil" versus ticker XOM. Do **not** try to match all 500. Match the top ~100 emitters by hand or with fuzzy matching plus a manual review pass, and let EEIO cover the tail. Hard cap: two hours, then stop.
3. **GHGRP is US facilities only, above the reporting threshold.** A company's GHGRP total is a *lower bound* on its global Scope 1, not its footprint. This is a real limitation and, conveniently, another honest specification.
4. **`.xlsb` is not a normal Excel file.** `pandas.read_excel` needs the `pyxlsb` engine. Install it before you need it.
5. **SEC wants a real User-Agent** with contact details on every request, and rate-limits roughly 10 requests per second. The frames API means you will barely touch that.
6. **EEIO factors are per 2022 USD.** Deflate or state the assumption. Do not silently mix price years.

## 5. First 45 minutes, data owner only

Smoke-test in this order. Anything that fails twice gets dropped and the framework shrinks, per the cut ladder in [[Efforts/Active/ETHack/framework|framework]].

- [ ] Wikipedia S&P 500 table parses to 500 rows with tickers and sectors
- [ ] `company_tickers.json` downloads and maps our tickers to CIKs
- [ ] One frames API call returns thousands of entities for `Revenues/USD/CY2024`
- [ ] Coverage check: what fraction of our 500 CIKs appear in that frame? Try the fallback tags for the rest.
- [ ] EPA Supply Chain GHG Emission Factors CSV downloads and parses
- [ ] GHGRP parent company xlsb downloads and opens with `pyxlsb`

If the first four pass, the project is safe. Everything after that is upside.

## 6. The paywall answer, which is a feature not an excuse

The question a judge will ask: *what about the data you cannot afford?*

The wrong answer is to apologise. The right answer is that **the framework is data-source agnostic by design.** Each data source is just another specification. Paid data does not replace what we built, it adds specifications to the curve.

| Phase | Cost | What it adds | What changes |
|---|---|---|---|
| **Today** | zero | EPA EEIO modelled + GHGRP disclosed + SEC financials | 36 specifications, full index coverage |
| **Phase 2** | CDP data licence | company-disclosed Scope 3 at scale | replaces modelled with disclosed where available, narrows contestation |
| **Phase 3** | MSCI + Sustainalytics enterprise licences | two commercial ratings as additional specifications | lets us measure *their* divergence against ours, directly |
| **Phase 4** | free again, 10 Nov 2026 | California SB 253 mandatory Scope 1+2 filings | the first audited, mandatory US emissions data, and it arrives on its own |

We have not obtained quotes. MSCI and Sustainalytics licences are negotiated enterprise agreements and not publicly priced, and we will not invent a number on a slide.

Three things this architecture lets us say, all true:

1. **It works at zero cost today.** No pilot budget, no procurement, no vendor dependency.
2. **It improves monotonically with budget.** Every euro narrows contestation. Nothing has to be rebuilt.
3. **Phase 4 is free and already scheduled.** California's first mandatory filings land 10 November 2026. The framework gets materially better in eight weeks without anyone spending anything.

Contrast that with a framework built on a paid feed: it does not run at all until someone signs a contract. Ours runs tonight and gets better on its own.

## 7. Repo shape

```
data/raw/        downloaded once, cached to disk, committed if small
data/interim/    the join table: ticker | cik | naics | gics | revenue | scope1_disc | scope1_mod | ...
src/fetch_*.py   one file per source, each idempotent and cacheable
src/score.py     ONE parameterised function: score(boundary, denominator, missing_rule, peer_group)
src/specs.py     builds the 36 combinations, runs them, writes ranks
src/plot.py      the specification curve and the map
README.md        the methodology, so the repo stands alone
```

The judges said they will read the code. The thing they should see is one small scoring function called 36 times, not four people's notebooks.

## 8. Sources

- [SEC EDGAR APIs, including XBRL frames](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [EPA Supply Chain GHG Emission Factors v1.3 by NAICS-6](https://catalog.data.gov/dataset/supply-chain-greenhouse-gas-emission-factors-v1-3-by-naics-6)
- [USEEIO models, EPA](https://www.epa.gov/land-research/us-environmentally-extended-input-output-useeio-models)
- [EPA GHGRP data sets, including Reported Parent Companies](https://www.epa.gov/ghgreporting/data-sets)
- Regulatory status and the 10 Nov 2026 date: [[Efforts/Active/ETHack/data-landscape|data-landscape]]
