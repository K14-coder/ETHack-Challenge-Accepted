# CONTESTED

**ETHack 2026, Challenge #1.** A sustainability framework for the S&P 500 that publishes its own uncertainty.

> There is no ESG score. There is a distribution of defensible scores, and the width of that distribution is the most useful number nobody reports.

## Run it

```bash
pip install -r requirements.txt      # optional; steps 1 and 2 need only the stdlib
python3 01_fetch.py                  # pulls everything, caches to data/raw/
python3 02_score.py                  # 24 specifications  (--peer for 48)
python3 03_plots.py                  # three PNGs into out/
```

Needs internet for step 1 only. Everything is cached, so a second run is free and it is safe to interrupt.

If you want to see it work before fetching anything:

```bash
cp seed/companies_verified4.csv data/interim/companies.csv
python3 02_score.py && python3 03_plots.py
```

That seed holds four companies whose every number was pulled and hand-checked on 12 Sep 2026.

## The 24 specifications

`2 × 3 × 2 × 2 = 24`. Each is a real choice a real analyst makes. **None of them is the correct one.** That is the whole point.

| Dimension | Options | What the choice is |
|---|---|---|
| **boundary** | `A_disclosed` · `C_modelled` | only what the company reported to EPA, or its whole supply chain estimated from its industry |
| **missing rule** | `exclude` · `worst_case` · `modelled` | no reported number: drop it, rank it last (what MSCI actually does), or substitute the estimate |
| **eeio margins** | `with` · `without` | does the emission factor include transport and retail mark-up |
| **denominator** | `revenue` · `market_cap` | tonnes per million dollars of sales, or of company value |

`--peer` adds `absolute` vs `within_sector` and doubles it to 48. The 30 companies are 10 GICS sectors × 3, so within-sector ranking is meaningful.

Two dimensions from the original design are **deliberately absent**, because the data for them does not exist for free:

- **Scope 2** (purchased electricity) as a third boundary. Needs per-company electricity data, only in voluntary sustainability reports.
- **Consolidation approach** (100% vs equity share). `01_fetch.py` *does* capture ownership shares from EPA and writes `disclosed_equity`, so this is one dimension away from 48 → 96. It is wired but not switched on, because it only varies for companies with jointly-owned facilities.

Say 24. Not 72. Claim what you ran.

## The 30 companies

Ten GICS sectors, three each. Chosen to span the **contestation axis**, not just to list industries: a retailer with no disclosed number, a steelmaker whose emissions sit in its own furnaces, a bank with zero rows, automakers whose footprint is customers driving. See `companies.csv`.

## Output

| File | What |
|---|---|
| `data/interim/companies.csv` | one row per company, every input with its source |
| `data/interim/facilities.csv` | every EPA facility, its ownership share and emissions |
| `out/long.csv` | one row per company per specification |
| `out/summary.csv` | consensus rank, contestation IQR, full range, disclosure ratio |
| `out/claims.json` | the quantitative claims, computed |
| `out/fig1_specification_curve.png` | one company across every specification, with the choice dashboard |
| `out/fig2_contestation_map.png` | consensus rank against contestation, all companies |
| `out/fig3_disclosure_gap.png` | reported versus estimated, per company, log scale |

## Data sources. All free, all government, no API key.

| Source | Gives |
|---|---|
| SEC `company_tickers.json` | ticker → CIK |
| SEC XBRL **frames** API | revenue, audited, from 10-K filings. One call returns every filer. |
| EPA GHGRP via `data.epa.gov/dmapservice` | reported facility emissions, rolled up to parent, with ownership shares |
| EPA Supply Chain GHG Emission Factors v1.3 | kg CO2e per 2022 USD by NAICS |
| yfinance *(optional)* | market cap |

## Three traps this code already handles

1. **`us-gaap/Revenues` misses most modern filers.** Nucor's only 10-K value under that tag is FY2018. `01_fetch.py` walks a five-tag fallback chain and records which tag each company hit.
2. **Parent-company names are not normalised.** Walmart appears three ways inside its own twelve rows, one with a double space. `WALMART` returns nothing; the string is `WAL-MART`. Hence the curated `ghgrp_search` and `ghgrp_alt` columns.
3. **NAICS codes drift and the EPA table mixes aggregation levels.** The factor lookup tries progressively shorter prefixes.

## Honest limitations, stated before anyone asks

- Disclosed figures are **floors**. GHGRP covers US facilities above a 25,000 tCO2e threshold only.
- Modelled figures are **screening estimates**. The EPA factor is per dollar of commodity purchaser price; applying it to revenue is standard first-pass practice, not an accounting result.
- The factor is per **2022** USD, revenue is 2023 USD. Not deflated. Roughly a 3% effect against differences of 5× to 85×.
- EEIO gives every company in a NAICS code the **same intensity**, so the modelled layer differentiates on size, not efficiency. Disclosed data is the only source of within-sector variation.
- One fiscal year. No trajectory claim is available.

## What we claim, and what we do not

We claim the ranking **can** invert between defensible conventions. Verified on real data: Nucor is worst by disclosed intensity, Walmart is worst by modelled total.

We do **not** claim what share of the S&P 500 inverts. That is a prevalence claim and it needs the full index.

See `DEFENCE.md` for ten likely attacks and the answer to each.

## Method

Specification curve analysis — Simonsohn, Simmons & Nelson, *Nature Human Behaviour* 4 (2020) — applied to corporate sustainability scoring. Motivated by the rating divergence documented in Berg, Kölbel & Rigobon, *Review of Finance* (2022), which found an average inter-rater correlation of 0.61 against 0.99 for credit ratings.
