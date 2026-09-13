# CSV export of the Bloomberg materiality maps

Produced by `../to_csv.py`. Re-run it after adding or replacing any `.xlsx` in the
parent folder; it overwrites everything here.

```bash
cd "/Users/avartanian/Desktop/mat maps"
python3 to_csv.py
```

## Files

| File | Rows | What it is |
|---|---|---|
| `materiality_long.csv` | 15,950 | **The one to load.** One row per ticker × field × year. |
| `materiality_wide.csv` | 3,190 | Same data, years across the columns, plus `years_reported`. |
| `companies.csv` | 18 | ticker → peer group → source file, and the field count per sheet. |
| `coverage.csv` | 36 | Per ticker per sheet: fields, how many have 3+ years, % of cells filled. |
| `es_field_availability.csv` | 61 | Every E/S field ID and which peer groups can actually use it. Read this before choosing fields. |
| `raw/<TICKER>_ES.csv`, `raw/<TICKER>_G.csv` | — | Faithful dumps, header rows and all. Use them only to check something by eye. |
| `raw/credit_*.csv` | — | The six sheets of `Credit_Comps_Oil_Gas_FY2025.xlsx`, dumped as-is. |

## Schema of `materiality_long.csv`

| Column | Notes |
|---|---|
| `ticker` | XOM, CVX, COP, … |
| `peer_group` | Bloomberg's own peer group. **The field set depends on it** (see below). |
| `sheet` | `ES` or `G`. The ES sheet carries `units` and no `theme`; the G sheet the reverse. |
| `pillar` | ENVIRONMENTAL / SOCIAL / GOVERNANCE, forward-filled down each block |
| `theme`, `issue`, `sub_issue` | Bloomberg's hierarchy, also forward-filled |
| `field` | human-readable name |
| `field_id` | the stable Bloomberg ID. **Join on this, never on `field`.** |
| `units` | ES sheet only |
| `year` | 2021 … 2025 |
| `value_raw` | exactly what the cell held, as text. Empty when not reported. |
| `value` | the same cell parsed to a number, empty when it is not numeric |

Booleans arrive as `Y`/`N` in `value_raw` and empty in `value`. Percentages are
already percentages, not fractions. Everything is UTF-8 with a BOM, comma
separated, so Excel and `pandas.read_csv` both open it without arguments.

## The thing to know before writing any code against this

**Bloomberg builds the materiality map per peer group, so the five sub-industries
do not share a field set.**

| Peer group | Companies | ES fields offered | ES fields with 3+ years for *every* member |
|---|---|---|---|
| Exploration & Production | 7 | 78 | 33 |
| Integrated Oils | 2 | 99 | 53 |
| Refining & Marketing | 3 | 50 | 26 |
| Oilfield Services & Equipment | 3 | 44 | 26 |
| Midstream | 3 | 37 | 21 |

Across all five groups, **exactly four E/S fields are usable everywhere**, and all
four are yes/no policy flags:

```
SA086  Emergency Response and Preparedness Policy
SA162  Air Pollution Reduction Policy
SA558  Company Claims Science-Based Emissions Targets
SA559  Company Claims Net Zero Emissions Target
```

`F0947 Scope 1 GHG` works in four groups out of five. Governance is the opposite
case: 88 fields, present for all 18 companies, 91–94% filled.

So there are two honest comparison modes, and they are a specification choice,
not a bug to engineer around:

- **intra-group** — compare inside one peer group on its full field set. Rich, but
  only 2 to 7 companies per group.
- **inter-group** — compare all 18 on the fields their groups share. All 18
  companies, but on very few environmental measures.

`es_field_availability.csv` has the per-field, per-group answer so the choice can
be made in code rather than by hand.

## Missing from the twenty

Two S&P 500 energy names have no export here: **EQT** and **OKE** (ONEOK). Everything
downstream currently runs on eighteen.

## The credit workbook

`Credit_Comps_Oil_Gas_FY2025.xlsx` is a different animal: FY2025 financials from SEC
XBRL, agency adjustments, and ratings. Its sheets are in German and its headers wrap
across two lines, so the raw dumps flatten them to one line.

| Raw file | Contents |
|---|---|
| `raw/credit_input_finanzen.csv` | debt, cash, EBIT, D&A, EBITDA, interest, CFO, capex, FCF, dividends, buybacks, equity, maturities under 24m, tax rate, reserves (MMboe), production (MMboe/a) |
| `raw/credit_input_adjustments.csv` | operating and finance leases, pensions and OPEB, ARO, hybrids, adjusted EBITDA |
| `raw/credit_input_ratings.csv` | Moody's, S&P and Fitch with outlooks, as at September 2026 |
| `raw/credit_agentur_bruecke.csv` | each agency's adjusted debt and leverage, computed |
| `raw/credit_kennzahlen.csv` | **the ready-made ratios**: Net Debt/EBITDA, interest coverage, FCF/debt, Capex/D&A, payout/FCF, maturities under 24m, the three agency leverage figures, ROCE, reserve life |
| `raw/credit_legende.csv` | the source and method notes |

`credit_kennzahlen.csv` is the financial pillar of the framework, already computed.
Header row is row 5 of that file; rows above it are the sheet title and the source note.
