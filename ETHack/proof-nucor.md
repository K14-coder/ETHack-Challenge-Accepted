---
edit: owned
last_edited: 2026-09-12T13:30:03 CET
changes: 0
type: project-note
status: verified
---
# Feasibility proof: Nucor, FY2023, end to end

**All four data layers pulled live from free public APIs on 12 Sep 2026.** No paid feed, no key, no login, no scraping. Data files in `data/`.

Company: **NUCOR CORPORATION (NUE)**, CIK `0000073309`, GICS Materials, NAICS `331110`.

## The joined record

| | Value | Source |
|---|---|---|
| Revenue FY2023 | **$34,713,501,000** | SEC XBRL, 10-K, audited |
| Disclosed Scope 1, 100% consolidation | **5,762,209 tCO2e** | EPA GHGRP, 26 facilities |
| Disclosed Scope 1, equity share | **5,497,858 tCO2e** | same, weighted by ownership |
| Modelled footprint (EEIO) | **27,319,525 tCO2e** | EPA supply-chain factor 0.787 kg CO2e per 2022 USD |
| Modelled ÷ disclosed | **4.74 ×** | derived |
| Boundary A intensity | **166.0 t / $M revenue** | derived |
| Boundary C intensity | **787.0 t / $M revenue** | derived |

## Layer by layer, with the exact calls

**1. Index membership.** S&P 500 constituent list gives ticker `NUE` and GICS sector Materials.

**2. Ticker to CIK.** CIK `0000073309`. The SEC API echoed back `entityName: "NUCOR CORPORATION"`, confirming the join.

**3. Revenue.**
```
https://data.sec.gov/api/xbrl/companyconcept/CIK0000073309/us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax.json
```
FY2023, form 10-K, fp FY, frame CY2023: **34,713,501,000 USD**. Also returned FY2022 (41,512,467,000) and FY2024 (30,734,000,000).

**4. Disclosed Scope 1.** Facility list, then emissions:
```
https://data.epa.gov/dmapservice/ghg.pub_dim_facility/parent_company/contains/NUCOR/year/equals/2023/0:100/JSON
https://data.epa.gov/dmapservice/ghg.pub_facts_sector_ghg_emission/facility_id/in/<ids>/year/equals/2023/0:100/JSON
```
26 facilities, every one returning non-null `co2e_emission`, split by gas. Largest: Nucor Steel Louisiana, 1,086,837 tCO2e. Full list in `data/nucor_ghgrp_2023.csv`.

**5. Modelled footprint.**
```
https://pasteur.epa.gov/uploads/10.23719/1531143/SupplyChainGHGEmissionFactors_v1.3.0_NAICS_CO2e_USD2022.csv
```
NAICS 331110, "Iron and Steel Mills and Ferroalloy Manufacturing": **0.787** kg CO2e per 2022 USD with margins, **0.769** without. Unit string verbatim: `kg CO2e/2022 USD, purchaser price`.

## What the proof taught us that the plan did not

Four things we only learned by touching the data.

### 1. A fifth specification dimension, straight out of the GHG Protocol

Two of Nucor's 26 facilities are jointly owned: Nucor-Yamato Steel (51%) and California Steel Industries (51%). EPA publishes the ownership percentages, so we can roll up either way, and the GHG Protocol formally defines these as different **consolidation approaches** (operational control versus equity share).

**5,762,209 versus 5,497,858 tCO2e. A 4.59% swing from a convention choice, with nothing else changed.**

This is not our invention. It is a documented accounting choice that companies genuinely make, and it is invisible in any published single number. Adding it doubles the specification count: 36 → 72.

### 2. EEIO alone destroys within-sector variation

Boundary C intensity came out at exactly 787.0 t per $M revenue, which is the EEIO factor restated. That is not a coincidence, it is arithmetic: `revenue × factor ÷ revenue = factor`.

So a purely modelled boundary gives **every company in the same NAICS an identical intensity.** It differentiates on total emissions (via size) but not at all on efficiency.

The consequence is sharp and worth a slide: **the disclosed data is the only thing that creates within-sector variation.** So the missing-data rule does not merely shift levels, it determines whether within-sector comparison is possible at all. That is a much stronger claim than "the rule changes the ranking".

### 3. The revenue-tag trap is real, and we hit it

`us-gaap/Revenues` for Nucor returns exactly one annual 10-K value: **FY2018**. Everything recent sits under `RevenueFromContractWithCustomerExcludingAssessedTax`.

A team that queried only `Revenues` would have concluded Nucor has no recent revenue. The fallback chain is mandatory, not optional.

### 4. The disclosed number is a lower bound, and the gap is large

5.76 Mt disclosed against 27.3 Mt modelled. The 4.74× gap is not evidence of dishonesty. GHGRP covers **US facilities above the reporting threshold only**, and the EEIO figure is cradle-to-gate including the entire supply chain. They are measuring different things, which is the point.

## Caveats to state before any of this goes on a slide

1. **Price-year mismatch.** The EEIO factor is per 2022 USD; revenue is 2023 USD. Not deflated in these figures. Deflate, or state the assumption.
2. **Revenue is the wrong activity variable, strictly.** The EEIO factor is per dollar of purchaser price of the commodity. Applying it to revenue is a standard screening approximation, not an accounting result. Say "screening estimate".
3. **GHGRP is US-only and threshold-limited.** 5.76 Mt is a floor on global Scope 1, not a measurement of it.
4. **Two facilities carry a different NAICS** (California Steel 331221, Nucor Fastener 332312) than the parent's 331110. Rolling a parent up to one NAICS is itself an approximation.
5. **Everything here is one fiscal year.** No trajectory claim is available from it.

## What this settles

The pipeline runs. Four independent free sources, joined on ticker, CIK, parent name and NAICS, producing real tonnes and real dollars for a real S&P 500 company, inside one afternoon of API calls.

Scaling from one company to 500 is the same code in a loop plus the parent-name matching problem, which is already scoped and time-capped in [[Efforts/Active/ETHack/data-plan|data-plan]].

## Related

[[Efforts/Active/ETHack/data-plan|data-plan]] · [[Efforts/Active/ETHack/framework|framework]] · [[Efforts/Active/ETHack/finding-walmart|finding-walmart]] · [[Efforts/Active/ETHack/sustainability-definition|sustainability-definition]]
