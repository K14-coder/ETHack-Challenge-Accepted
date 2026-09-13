# model — CONTESTED v2

The framework rebuilt on the data we actually have: **18 S&P 500 energy companies,
139 fields, 2021–2025, from the Bloomberg materiality maps and the FY2025 credit
workbook in `bruh/mat maps/`.** Nothing is fetched, nothing is imputed, and a cell
that was empty in the export is missing here.

```bash
python3 registry.py     # the field registry, printed for eyeball checking
python3 load.py         # the arrays, with a coverage report
python3 run.py          # all 17,496 specifications  (--quick for 5,832)
python3 export_web.py   # the pillar cube for ../web/
```

## What changed from v1, and why

v1 ran 72 specifications over 30 synthetic fields on three pillars. This is the
same method against the real export, and the data forced four changes.

| Change | Because |
|---|---|
| Four pillars, E / S / **G** / F | The governance sheet is the densest data we have: 79 fields, 63 of them reported by all 18 companies. Leaving it out threw away half the evidence. |
| Nine axes, not five | `provider-decision-points.md` located seven forks where MSCI and Bloomberg publish different choices. Two more were forced by the data. |
| Contestation in **rank places**, not percentile points | With N=18 a rank percentile takes 18 values 5.88 apart. An IQR quoted in points is a quantised quantity wearing a decimal. |
| An **evidence bar** axis | The single largest finding below. |

## The nine axes

| Axis | Options | Provenance |
|---|---|---|
| `base` | EBITDA · equity · production | Bloomberg's activity metrics, B p.17 |
| `window` | latest · fiscal year · 3-year mean | Bloomberg ships Latest and Fiscal Year as separate products, B p.34 |
| `direction` | level · change | Bloomberg's Rate-Anchored model scores YoY change, B p.18 |
| `polarity` | orthodox · neutral · stability | 15 fields where the two governance conventions disagree |
| `normalizer` | percentile · winsorised · log min–max · **elasticity** | MSCI normalises on percentile benchmarks (M p.12); Bloomberg rejects percentiles in print and fits the log-log residual (B pp.41, 45–46) |
| `peerset` | BECS group · producers/downstream · all 18 | MSCI uses GICS sub-industry; Bloomberg built BECS because it didn't fit |
| `inclusion` | permissive · majority · strict | forced by this data — see below |
| `missing` | excluded · worst case · **capped** | Bloomberg's sub-issue rule and its Issue Score cap, `UT = 30 + √DF × 70`, B p.26 |
| `aggregator` | arithmetic · power p=½ · geometric | MSCI's weighted mean vs Bloomberg's shifted power mean, B p.25 |

`3 × 3 × 2 × 3 × 4 × 3 × 3 × 3 × 3 = 17,496`, times whatever weighting you pick.

The exposure base has one operator per type, so the divisor is applied exactly
once on every branch: for a quantity it divides; for a rate triple it selects the
population the reporter already divided by (employees / contractors / workforce);
for agency-adjusted leverage it selects the agency (Moody's / S&P / Fitch).

## What the data will and will not support

**All 135 planned questions arrived, plus 57 unplanned. It changes nothing about
the central problem, which is that Bloomberg builds the materiality map per peer
group, so the five sub-industries do not share a field set.**

| Fields reported by | ES | G |
|---|---|---|
| all 18 companies | **4**, every one a yes/no policy flag | 64 |
| 12 or more | 32 | 77 |
| 10 or more | 38 | 78 |

An eighteen-company comparison of environmental *performance* is not available
from this export. What is available is four boolean policy flags. That is not a
gap in our pipeline; it is what the sector's disclosure looks like once you
require everyone to have answered the same question.

So the **evidence bar** is an axis rather than a setting, and it is the honest
form of the missing-data question asked one level up: not *what do we do with an
empty cell*, but *does this field belong in the model at all*. It tightens two
things together — how much of the peer set must report a field, and how
substantive a policy flag must be:

| Level | Share of peer set reporting | Boolean tier | Fields at sector level |
|---|---|---|---|
| permissive | ≥ 50% | any disclosed policy | E 28 · S 12 · G 78 · F 9 |
| majority | ≥ 67% | constrains an operating decision | E 12 · S 7 · G 53 · F 8 |
| strict | 100% | carries a quantified commitment | E 2 · **S 0** · G 47 · F 8 |

At the strict end the Social pillar has no fields left. Narrowing the peer group
goes the other way: for a Exploration & Production company the same strict setting
leaves 13 environmental fields, because its peers all report the same things.
**Comparing fewer companies lets you compare them on more.** That trade is the
whole intra- versus inter-group question, and it is a slider rather than an
argument.

## Two rules that are rules, not specifications

- `MIN_PEERS = 3`. A peer group below it is graded against the sector. Two members
  can only ever return 0 and 100. Only Exploration & Production (7) clears it
  comfortably, which is why the producers/downstream split exists.
- `ELAST_MIN = 8`. The elasticity normaliser needs enough points to fit a slope;
  below it that cell falls back to log min–max.

## What we found

Running the full grid at equal weights:

- **The median company moves 7 places out of 18** across its interquartile range.
  Strip out every extreme branch — level only, majority evidence bar, no
  worst-case missing rule, sector peers — and it is still **4 places**. The spread
  is not an artefact of one silly option.
- **2 of 153 pairwise comparisons survive every method.** At a 0.75 threshold,
  42 do. A published league table asserts all 153.
- The variance decomposition is unambiguous about where the disagreement lives:

  | Axis | Mean share of a company's rank variance |
  |---|---|
  | direction | 18.2% |
  | peer set | 13.1% |
  | evidence bar | 3.8% |
  | window | 3.8% |
  | normaliser | 3.3% |
  | missing data | 3.0% |
  | exposure base | 1.8% |
  | polarity | **0.5%** |
  | aggregator | **0.3%** |

  Main effects account for under half the variance; the rest is interaction.

**Two of those numbers are negative results and both are worth saying out loud.**
The aggregation function — MSCI's arithmetic mean against Bloomberg's power mean,
which `provider-decision-points.md` called the biggest hole in v1 — explains
0.3%. The governance polarity debate that the question set devotes a whole sheet
to explains 0.5%. Both were worth implementing precisely so that we can report
that they do not matter here.

What does matter is `direction` and `peerset`: *what question you are asking* and
*who you are asking it against*. Neither is a weight. Both are scope choices, the
bucket Berg, Kölbel & Rigobon put at 36.7%.

## Files

| File | What it is |
|---|---|
| `registry.py` | field types, polarity under three conventions, boolean stringency tier |
| `load.py` | the materiality maps and the credit workbook, as arrays |
| `spec.py` | the formula. Pure functions, no data, no plotting. |
| `run.py` | every specification; writes `out/` |
| `export_web.py` | the pillar cube for the browser explorer |

| Output | What it holds |
|---|---|
| `out/summary.csv` | consensus, contestation in places, verdict, coverage |
| `out/long.csv` | one row per company per specification. The audit trail. |
| `out/pivot.csv` | variance decomposition per company, per axis |
| `out/dominance.csv` | P(i outranks j) for all 153 pairs |
| `out/remedy.csv` | the disclosure that would remove the most contestation |
| `out/claims.json` | the slide numbers, computed |

## Honest limitations, stated before anyone asks

- **No revenue and no headcount** anywhere in the export. EBITDA is the economic
  denominator. Bloomberg's own methodology calls revenue a fallback for when the
  physical activity metric is unavailable; we are one rung further down.
- **The credit workbook is one fiscal year.** Under `direction = change` the
  financial pillar has no trajectory and drops out; the composite renormalises
  over E, S and G. Holding one year flat and reporting zero change would be a
  fabricated time series.
- **FY2025 is 36% complete** for environmental fields against 60% for FY2024.
  That is why `window` has three options rather than two.
- **EQT and ONEOK** have no export. Eighteen, not twenty.
- **Governance dominates by field count** — 79 of 139. Its pillar score is far
  more stable across specifications than E or S, so the contestation you see is
  mostly environmental and social. That is a property of the disclosure, not of
  the companies.
- We rank the **energy sector against itself**. If every company in it is bad,
  the best relative performer still scores well. Bloomberg names this failure
  mode in its own methodology (B p.42) and does not treat it either.
