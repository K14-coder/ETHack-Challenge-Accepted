# speccurve

The score is not a number, it is a distribution over every defensible way of
computing it. 72 specifications x 4 weightings = 288 scores per company.

`FORMULA.md` is the whole method on one page. Every symbol matches the code.

## Run

```bash
pip install -r requirements.txt
python3 run.py                # dummy data, seed 7
python3 run.py --seed 12      # a different draw
```

## Files

| File | What it is |
|---|---|
| `spec.py` | the formula. Pure functions, no data, no plotting. |
| `dummy.py` | synthetic data with the exact shape the Bloomberg export has. |
| `run.py` | runs all 288, writes the CSVs and the three figures. |
| `export_web.py` | writes the grade tensor for the browser explorer in `../web/`. |
| `FORMULA.md` | the method, one page. |

## Outputs in `out/`

| File | What it shows |
|---|---|
| `fig1_curves.png` | all 20 companies' 288 scores, sorted best to worst, overlaid. Flat = robust, steep = contested. |
| `fig2_small_multiples.png` | the same curve one panel per company against the sector median, so the shapes are comparable. |
| `fig3_scatter.png` | consensus against spread. Four quadrants: robustly strong, robustly weak, and the two "only under some methods" corners. |
| `summary.csv` | one row per company: consensus, spread, quartiles, min, max, coverage, verdict. |
| `scores_long.csv` | 20 x 288 rows, one per company x specification x weighting. The audit trail. |

## The explorer

Steps 1 to 5 do not involve the pillar weights, so the whole weighting question
can be answered in a browser from one tensor:

```bash
python3 export_web.py                  # -> ../web/data/speccurve.{json,js}
python3 -m http.server 4173 --directory ../web
```

`../web/` then runs steps 6 to 8 live: move the weights, pin a specification
axis, flip the missing-data rule, and the ranking reorders in front of you. It
reproduces `out/summary.csv` to 0.05 rank points. See `../web/README.md`.

## Swapping in real data

`dummy.build()` returns a dict. Replace it with a loader that returns the same
keys and nothing else changes:

```python
{
  "names":  [20 company labels],
  "groups": np.array of 20 sub-group labels,
  "ftype":  np.array of 30 values from {"Q","R","P","B"},
  "pol":    np.array of 30 values from {+1.0, -1.0},
  "pillar": np.array of 30 values from {"E","S","F"},
  "RAW":    np.array (20, 30, 5, 3), np.nan where not reported,
  "BASE":   np.array (20, 5, 3)  -- revenue, volume, headcount,
  "fields": [30 field names],
  "years":  [2021, 2022, 2023, 2024, 2025],
}
```

`RAW[:, :, :, b]`: for `Q`, `P` and `B` fields put the same number in all three
`b` slices. For `R` fields put the three published rate variants in
`b = 0, 1, 2`.

The 30 fields and their Bloomberg IDs are listed in `dummy.py: FIELDS`. The E and
S ones come from the materiality map; the F ones come from Bloomberg fundamentals
and Moody's and have to be requested separately.

## Two rules that are rules, not specifications

- `MIN_PEERS = 4` in `spec.py`. A sub-group smaller than that is graded against
  the whole sector, because a 2-member percentile can only return 0 or 100.
- Missing fields do not enter the pillar mean. The alternative branch, missing =
  0 = worst, is one line in `composite()` and the gap between the two runs is
  the disclosure penalty. Coverage is reported separately in `summary.csv` and is
  never folded into the score.
