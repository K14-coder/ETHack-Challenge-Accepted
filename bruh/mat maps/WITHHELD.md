# Bloomberg materiality maps — data withheld

**We do not share these indicators and values, because they require the proper
Bloomberg licensing. We are happy to show you the files in person, to prove that
the model is built on real data and that the approach is scalable and feasible.**

Everything else in this repository is here: the loader that reads these files,
the formula, the full specification run, every computed output, and the working
explorer. Only the licensed cell values are absent.

## What is withheld

18 Bloomberg Terminal materiality-map exports, one per company, each with an
`ES Materiality` and a `G Materiality` sheet, 2021–2025.

| | |
|---|---|
| `BKR mat map.xlsx` | Baker Hughes |
| `CTRA mat map.xlsx` | Coterra Energy |
| `Chevron mat map.xlsx` | Chevron |
| `Conoco mat map.xlsx` | ConocoPhillips |
| `DVN mat map.xlsx` | Devon Energy |
| `EOG mat map.xlsx` | EOG Resources |
| `EXE mat map.xlsx` | Expand Energy |
| `Exxon materiality map 2.xlsx` | Exxon Mobil |
| `FANG mat map.xlsx` | Diamondback Energy |
| `HAL mat map.xlsx` | Halliburton |
| `KMI mat map.xlsx` | Kinder Morgan |
| `MPC mat map.xlsx` | Marathon Petroleum |
| `OXY mat map.xlsx` | Occidental Petroleum |
| `PSX mat map.xlsx` | Phillips 66 |
| `SLB mat map.xlsx` | SLB |
| `TRGP mat map.xlsx` | Targa Resources |
| `VLO mat map.xlsx` | Valero Energy |
| `WMB mat map.xlsx` | Williams Companies |

And their faithful CSV dumps under `csv/`, produced by `to_csv.py`:

| File | Size | Rows |
|---|---|---|
| `csv/materiality_long.csv` | 2.4 MB | 15,950 — one per ticker × field × year |
| `csv/materiality_wide.csv` | 0.5 MB | 3,190 — years across the columns |
| `csv/raw/<TICKER>_ES.csv`, `csv/raw/<TICKER>_G.csv` | 288 KB | 36 files, per-sheet dumps |

## What is here, and why it is enough to evaluate the work

| Still committed | Why it is not licensed Bloomberg content |
|---|---|
| `Credit_Comps_Oil_Gas_FY2025.xlsx` and `csv/raw/credit_*.csv` | Our own workbook, built from SEC XBRL filings, published agency ratings and our own adjustments. |
| `csv/companies.csv`, `csv/coverage.csv` | Ticker → peer group, and per-company counts of how many fields are filled. Statistics about the data, not the data. |
| `csv/es_field_availability.csv` | Which Bloomberg field IDs exist for which peer group. Field identifiers, no values. Bloomberg's own published methodology names many of these IDs. |
| `to_csv.py`, `csv/README.md` | Our extraction code and its documentation. |
| `../../ETHack/model/out/*` | Every computed result: consensus, contestation, the variance decomposition, the dominance matrix. |
| `../../ETHack/web/data/model.json` | The pillar-score cube — our model's output, four numbers per company per specification. Derived scores, not Bloomberg indicators. |

So a reader can run the whole explorer, interrogate all 17,496 specifications,
reproduce every claim in the deck, and read every line of the pipeline. The one
thing they cannot do without a Terminal licence is re-run `model/load.py`, which
is the single step that reads the raw cells.

## To reproduce from source

With a Bloomberg Terminal licence, place the 18 exports in this folder and run:

```bash
python3 to_csv.py                       # xlsx -> csv/
cd ../../ETHack/model
python3 load.py && python3 run.py && python3 export_web.py
```

The committed outputs were generated exactly that way, on 13 September 2026.
