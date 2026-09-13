---
edit: owned
last_edited: 2026-09-12T13:23:35 CET
changes: 0
type: project-note
status: verified
---
# Finding: the GHGRP has no emissions number for Walmart

Pulled live from EPA Envirofacts on 12 Sep 2026. **This is real data, not synthetic.** It is the strongest single example we have and it should probably be the hero of the pitch.

## The working API

The `efservice` path returns empty arrays. The one that works is **`dmapservice`**, with schema-qualified lowercase table names:

```
https://data.epa.gov/dmapservice/ghg.pub_dim_facility/parent_company/contains/WAL-MART/0:100/JSON
```

Operators: `equals notEquals lessThan lessThanEqual greaterThan greaterThanEqual beginsWith endsWith contains excludes like notLike in notIn`. Row range as `first:last`. Format appended as `/JSON`. No key, no auth.

## What Walmart's entire GHGRP footprint is

**One facility_id: 1010779. "Wal-Mart Stores, Inc.", Bentonville, Arkansas.** That is its corporate headquarters.

Twelve rows, one per year, 2012 through 2023. Reported subparts **OO** and **QQ** every year (2018: QQ only).

| Subpart | What it is | Emitter or supplier |
|---|---|---|
| **OO** | Suppliers of Industrial Greenhouse Gases | **supplier.** Reporters document the quantity of industrial gases they produce, destroy, import or export. Not their own emissions. |
| **QQ** | Importers and Exporters of Fluorinated Greenhouse Gases Contained in Pre-Charged Equipment or Closed-Cell Foams | **supplier/importer.** Equipment that arrives already charged with F-gases: air conditioners, refrigerators, heat pumps, foam insulation. |

Walmart is in the US mandatory greenhouse gas reporting system **because it imports fridges and air conditioners.** Not because of anything it burns.

## The emissions field is null, every year

Querying `ghg.pub_facts_sector_ghg_emission` for facility 1010779 returns 24 rows, two sector/subsector combinations across 2012 to 2023.

**`co2e_emission` is `null` in all 24 rows.**

Not small. Not zero. Absent.

### State this precisely, or a judge will take it apart

The defensible claim is: *the GHGRP emitter-emissions field carries no value for Walmart in any year, and Walmart is registered only under supplier subparts.*

The claim we must **not** make is that Walmart emits nothing, or that EPA holds no Walmart data anywhere. Supplier quantities may sit in subpart-specific tables (`ghg.qq_*`, `ghg.oo_*`) that we have not yet queried. **Someone checks those before this goes on a slide.**

## Why there is no number, which is the actual point

Three structural reasons, none of them a data error:

1. **GHGRP is facility-level with a 25,000 tCO2e threshold.** Walmart's footprint is spread across thousands of stores and distribution centres. No single one crosses the line.
2. **Purchased electricity is legally the utility's Scope 1, not Walmart's.** The emissions from powering every Walmart store are reported by power plants, under those power companies' names.
3. **Everything else is Scope 3.** Suppliers, freight, the products on the shelves. Outside the boundary entirely.

So one of the largest companies on earth is, in the eyes of the only mandatory US emissions dataset, **an importer of air conditioners.**

## Why this is the hero

One real company demonstrates the whole framework, because all three of our missing-data rules give a different answer from the same query:

| Missing-data rule | What happens to Walmart |
|---|---|
| **Exclude** | Walmart disappears from the ranking. Non-disclosure becomes a way to avoid being scored at all. |
| **Worst case** (what MSCI actually does) | Walmart drops to the bottom of the index. |
| **Modelled** (EPA EEIO × revenue) | Walmart gets a very large footprint, because retail revenue is enormous. |

Three defensible conventions. One company. Three completely different positions in the S&P 500, from identical source data.

That is the specification curve, in one slide, with real numbers instead of a hypothetical.

**Recommendation: make Walmart the hero of Figure 1, not a bank.** Everyone in the room knows Walmart, the mechanism is intuitive (thousands of small stores, nothing big enough to report), and we can show the actual API response on screen. A bank requires explaining financed emissions first.

## Two traps, now confirmed with real evidence

Both were predictions in [[Efforts/Active/ETHack/data-plan|data-plan]]. Both are real.

**Parent-company strings are not normalised, even within one company.** Across Walmart's twelve rows: `Wal-Mart Stores, Inc. (100%)`, `WAL-MART STORES INC (100%)`, and `WAL-MART STORES INC  (100%)` with a double space. Exxon appears as both `EXXONMOBIL CORP` and `EXXON MOBIL CORP` in the same dataset. Also note the legal name has been **Walmart Inc.** since 2018; EPA still carries the pre-2018 string, so searching "WALMART" returns nothing and "WAL-MART" is required.

**NAICS codes drift across years for the same facility.** Walmart's rows move `452112` → `452311` → `455211` as retail classifications were revised between NAICS vintages. Since we join emissions to EEIO factors *by NAICS*, this silently changes a company's emission factor over time. Pin one NAICS vintage and say which.

## Reproduce it

```bash
# Walmart's facilities
curl -s "https://data.epa.gov/dmapservice/ghg.pub_dim_facility/parent_company/contains/WAL-MART/0:100/JSON"
# the emissions rows
curl -s "https://data.epa.gov/dmapservice/ghg.pub_facts_sector_ghg_emission/facility_id/equals/1010779/0:40/JSON"
# still to check: supplier quantities
curl -s "https://data.epa.gov/dmapservice/ghg.qq_subpart_level_information/facility_id/equals/1010779/0:40/JSON"
```

## Sources

- [Envirofacts web services syntax](https://www.epa.gov/enviro/web-services)
- [Subpart OO, Suppliers of Industrial Greenhouse Gases](https://www.epa.gov/ghgreporting/subpart-oo-suppliers-industrial-greenhouse-gases)
- [40 CFR Part 98 Subpart QQ](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-98/subpart-QQ)
- Queried live, 12 Sep 2026.
