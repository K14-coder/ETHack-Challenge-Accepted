# Challenge Accepted

VISIT OUR WEBSITE: demo.mehro.ch

**ETHack 2026 · Challenge #1 · Citadel.** A data-driven framework to quantify and
compare the sustainability of companies in the S&P 500.

> There is no ESG score. There is a distribution of defensible scores, and the
> width of that distribution is the most useful number nobody reports.

We publish the ranking the challenge asked for. We publish three more things with
it: how much of that ranking is a choice, which single choice decides it, and
which missing disclosure would settle it.

**The submission is [`CONTESTED.pdf`](CONTESTED.pdf)**, 16 pages, with
[`CONTESTED.docx`](CONTESTED.docx) as the editable source. The live tool is in
[`ETHack/web/`](ETHack/web) and runs from a static folder with no licence and no
install.

---

## Have you ever measured a dog?

To the shoulder, or the top of the head. With the tail, or without. Same dog,
same tape measure, four different numbers, and every one of them is correct.

Now replace the dog with a company and the tape measure with an ESG rating. The
provider publishes one number, and never tells you which measurement it took.

This repository takes all 17,496 of the measurements at once.

## Why the industry disagrees

Berg, Kölbel and Rigobon (*Review of Finance*, 2022) decomposed the disagreement
between the major raters and found an average inter-rater correlation of **0.61**,
against 0.99 for credit ratings. The split:

| Source of divergence | Share | What it means |
|---|---:|---|
| **Measurement** | **56%** | the same thing, measured differently |
| **Scope** | **38%** | what counts at all |
| Weights | 6% | the slider everyone argues about |

Six percent is the only part any provider lets you change. So we went after the
other ninety-four. We read MSCI's and Bloomberg's published methodologies and
located **thirteen points where a rater must make a discretionary call. They
differ at seven of them and agree at six.** We vary the forks where they differ,
fix the ones where they agree, declare every fixed assumption, and report the
whole distribution instead of one point from it.

The method is specification curve analysis (Simonsohn, Simmons and Nelson,
*Nature Human Behaviour* 4, 2020), imported into ESG.

## Every company's score is a curve, not a number

Nine controls, every one a fork where the two largest providers published
different choices, or one this data forced.
**3 × 3 × 2 × 3 × 4 × 3 × 3 × 3 × 3 = 17,496 specifications**, all of them
defensible, run over 18 companies and 138 fields in 18 seconds.

| Control | Options in the tool | Where it comes from |
|---|---|---|
| Exposure base | EBITDA · equity · output | Bloomberg activity metrics. Output exists for the 9 producers only |
| Window | latest · fiscal year · 3-year mean | Bloomberg ships Latest and Fiscal Year as separate products |
| Direction | level · change | Curve A against Curve B. The two are scored separately |
| Polarity | orthodox · neutral · stability | 15 fields where the two governance conventions disagree |
| Normaliser | percentile · winsorised · log min-max · elasticity | MSCI uses percentile bands. Bloomberg rejects them in print and fits a log-log residual |
| Peer set | BECS group · producers · all 18 | MSCI uses GICS sub-industry. Bloomberg built BECS because GICS did not fit |
| Evidence bar | permissive · majority · strict | Forced by this data. At strict, Social has no fields left |
| Missing data | excluded · worst case · capped | Bloomberg's sub-issue rule and its Issue Score cap, `UT = 30 + √DF × 70` |
| Aggregation | arithmetic · power p=½ · geometric | MSCI's weighted mean against Bloomberg's shifted power mean |
| *Pillar weights* | *4 sliders, 5 presets* | *Not a grid axis. Handed to the user, and worth 3.0 places* |

Each control is defined in full in [`ETHack/provider-decision-points.md`](ETHack/provider-decision-points.md),
with the branch we take and the page citation. That file is the justification for
every axis.

## Five minutes, no licence, no install

```bash
python3 -m http.server 4173 --directory ETHack/web
```

Open <http://localhost:4173>. Everything is precomputed and committed. The page
needs no server-side anything and no Bloomberg licence. Move the four pillar
sliders, pin any of the nine controls, and the ranking of 18 S&P 500 energy
companies reorders live.

**The sequence to run.** Watch the settled counter, not the table.

| Do this | Specifications | Settled of 153 |
|---|---:|---:|
| Leave every control on *vary* | 17,496 | **2** |
| Move the Environment weight to 70% | 17,496 | **2**, unchanged. This is the 6%, live |
| Reset, then pin **Direction → level** | 8,748 | **33** |
| Add **Evidence bar → strict** | 2,916 | **56** |
| Flip **Direction → change** | 2,916 | **9**, and the podium changes completely |

That is the product. Not a league table that asserts all 153 comparisons, but a
map of which comparisons the evidence can actually carry.

## Why the energy sector

We picked the sector where the number does the most work. Raters disagree here
more than anywhere: **0.55 inter-provider agreement, against 0.77 in technology**,
the lowest of any sector. It is also the thinnest disclosure. Only 3 of 37
environmental fields are reported by all 18 companies, and Scope 3 is absent
entirely.

**Does the measure behave?** A contestation figure is only worth reporting if it
responds to the quality of the evidence underneath it. Scoring each pillar alone
gives a direct test.

| Pillar | Fields | Coverage | Contestation |
|---|---:|---:|---:|
| Financial | 9 | 94% | 3.0 places |
| Governance | 78 | 97% | 4.0 places |
| Environment | 37 | 61% | 5.0 places |
| Social | 14 | 66% | 6.0 places |
| *Random-rank control* | | | *8.5 to 9.0 places* |

Across all **72 company-pillar pairs**: **Spearman −0.35, p = 0.003** (Pearson
−0.28, p = 0.017). Where disclosure is dense the framework reports confidence.
Where it is thin it reports doubt.

We quote the 72-pair statistic and **not** a coefficient across the four pillars,
which would be n = 4 with p = 0.17, and where the relationship is not even
monotone.

**What we claim, and what we do not.** We do not claim this generalises to other
sectors. Our indicators are sector-specific by construction, which is why the
providers build a materiality map per industry. We claim the uncertainty we
report tracks the evidence underneath it, and sits far inside a random-rank
control. It separates what the data supports from what it does not.

## What we found

**Contestation, after every deflation.** Level and change are different questions,
not rival methods, so we score them separately and never pool them.

| Stratum | Cells | Median IQR |
|---|---:|---:|
| Both curves pooled *(we do not report this)* | 17,496 | 7.0 places |
| Curve A only, level | 8,748 | 5.0 places |
| Curve A × sector peers | 2,916 | 5.0 places |
| **Curve A × BECS peer groups** | 2,916 | **3.0 places** |
| Random-rank control | | 8.5 to 9.0 places |

The honest headline is **3.0 places of 18**. Pooling would report 7.0, barely
below noise, which is exactly why we refuse to pool. A third of the ranking is
still a methodological choice: smaller than the pooled figure suggests, and still
larger than any published score admits.

**What is settled**, with the threshold stated rather than hidden behind "every
method": **2 of 153** pairwise comparisons pooled, **33 of 153** within Curve A,
**56 of 153** at Curve A with a strict evidence bar. At the strict bar the
environmental pillar has two fields and Social none, so the 56-pair result is
largely a governance-and-credit ranking, and we label it as such.

**Where the disagreement lives.** `direction` explains 18.2% of rank variance and
`peer set` 13.1%: *what question you ask* and *who you ask it against*. Both are
scope choices. Neither is a weight. Main effects account for 47.8% and interaction
for 52.2%, so we deliberately do **not** publish a single "decided by" axis per
company.

**Two deliberate negative results.** The aggregation function, MSCI's arithmetic
mean against Bloomberg's power mean, explains **0.3%**. The governance-polarity
debate explains **0.5%**. We implemented both specifically so we could report that
they do not matter here.

**An 18-company comparison of environmental performance does not exist in this
data.** Requiring every company to have answered the same question leaves four
fields, all policy booleans. Narrow to one peer group and the same strict setting
leaves thirteen environmental fields. Comparing fewer companies lets you compare
them on more, and that trade is a slider in the tool rather than an argument in a
footnote.

## Risks to this analysis, and what we did about them

Listing a risk is not addressing it. Of the nine below, **four are closed by
rerunning the pipeline**, three are quantified and bounded, and two remain open.

| # | Risk | Status | Test and result |
|---|---|---|---|
| 1 | The denominator is EBITDA, single-year and cyclical. Revenue was available and we did not use it. | **CLOSED** | Reran the whole grid on CY2023 revenue from SEC XBRL frames for 16 of 18. **Median rank shift 0.0 places, maximum 1.0.** Our weakest input choice does not change the answer. |
| 2 | 17,496 cells are not independent. | **CLOSED** | 648 grade paths collapse to **606 distinct**. Kish effective N is **574**, so the effective grid is 16,362, a 6.5% inflation. Results are quoted on distinct cells. |
| 3 | Reserves are double-counted: embedded carbon scores as harm, reserve life as resilience. | **CLOSED** | Dropped reserve life and reran. **Median shift 0.0 places**, only OXY moves by 1.0. Real in principle, immaterial in this sample. |
| 4 | The settled count depends on the 95% cut-off. | **CLOSED** | Settled pairs by threshold: 7 at P>0.999, 12 at 0.99, **33 at 0.95**, 51 at 0.90, 79 at 0.80. Monotone, no cliff at our cut-off. |
| 5 | Contestation is partly thin data and small groups. | **BOUNDED** | Coverage against contestation is **−0.38**. Mean IQR by group size: 2 members 6.0, 3 members 7.7, 7 members 7.0. Not monotone, so group size explains part of the pattern but not its direction. |
| 6 | N = 18 quantises every statistic. | **BOUNDED** | A rank percentile takes 18 values 5.88 points apart. Every headline figure is in rank places for that reason. The fix is a larger universe, not a different statistic. |
| 7 | Governance dominates by field count, 78 of 138. | **BOUNDED** | The G pillar is stable because it is densely reported, so the contestation we measure is mostly environmental and social. A property of the disclosure regime, not of the companies. |
| 8 | Nothing is benchmarked against a real published rating. | **OPEN** | We had a Terminal and did not place Bloomberg's own ESG score inside our distribution. The highest-value missing test, and first on the roadmap. |
| 9 | Scope 3, controversies and transition capex are absent. | **OPEN** | Scope 3 is not in the export. Controversies are a declared scope boundary. Transition capex was not delivered. For an oil and gas universe these are the three most material omissions. |

Every CLOSED row was tested by rerunning the pipeline, not by argument. **The
denominator result is the one to notice:** our weakest defensible choice, rerun
against the obvious alternative, moves the median company zero places.

Four further constraints we state rather than wait to be asked. The 17,496
specifications are an **enumerated set of conventions, not a random sample of
methods**, so the spread is a range and we never call it a confidence interval.
The credit workbook is **one fiscal year**, so under *change* the financial pillar
has no trajectory and drops out rather than reporting a fabricated zero. **FY2025
is 36% complete** for environmental fields against 61% for FY2024, and that
reporting lag is why the window control has three options and not two. **EQT and
ONEOK have no Bloomberg export**, so the universe is eighteen companies and not
twenty.

## The bonus question: allocating $1 billion under a net-zero commitment

Commitment is not a press release, it is a causal chain. A **social agreement**
becomes **legislative regulation**. Regulation becomes **penalties and rewards**.
Penalties and rewards become **financial impact**. Environmental performance stops
being a reputational question and becomes a cash-flow question.

In this framework that is not a new model, it is a weighting: **50% environment,
50% financial resilience**, because under that scenario they are the same bet.

We tested the premise first, and the obvious version of the trade fails. The
market thesis is that crossing an ESG threshold unlocks capital. On our data
**there is no threshold: 15 of 18 companies sit between P = 0.2 and P = 0.8** of
passing a top-half screen, with mean |P − 0.5| = 0.17. A true cliff would give
0.5. Eligibility is a fog, not a line, because the score itself is contested. So
the tradeable quantity is not crossing a line, it is the gap between where a
company stands (Curve A) and where it is heading (Curve B). Section 8 of the paper
works the allocation through, with an exit rule: Pástor, Stambaugh and Taylor
(2021) show green assets earn lower expected returns once repriced, so this has an
endpoint.

## Who it is for

| | Gets | Stops doing |
|---|---|---|
| **Asset allocator** | The consensus rank a provider already sells, plus the 33 of 153 comparisons that hold under every specification | Making 120 relative calls the evidence cannot support |
| **Engagement team** | The remedy column names the single missing disclosure that would most reduce a company's contestation | Walking in with a generic score complaint |
| **Regulator or standard setter** | How much of a rating is convention rather than performance, per control | Aiming disclosure rules at the wrong convention |
| **Rating provider** | A quality-assurance lens: where is our published score fragile? | Publishing without knowing which issuers to re-review |
| **The company being rated** | Which of its own silences costs it the most rank | Disclosing the cheapest field instead of the decisive one |

We do not replace a rating. We tell you which parts of it you can act on.

## What is in the repo

| | |
|---|---|
| **[`CONTESTED.pdf`](CONTESTED.pdf)** | **The submission.** 16 pages: the decision-point map, results, the risk register above, the bonus, and six appendices covering the formula, the control definitions, the field registry, the provider citations, reproducibility and a glossary. Every figure is generated by the committed pipeline. |
| **[`ETHack/model/`](ETHack/model)** | **The framework.** 18 companies, 138 fields with data, 9 controls, 17,496 specifications. Start with its `README.md`. |
| **[`ETHack/web/`](ETHack/web)** | The explorer. No build step, no dependencies, no network. |
| [`ETHack/provider-decision-points.md`](ETHack/provider-decision-points.md) | Where MSCI and Bloomberg actually choose, read out of their own methodologies, with the branch we take and the page citation at each. |
| [`ETHack/methodology-next.md`](ETHack/methodology-next.md) | The four outputs (settled, contested, pivot, remedy) and what we would build next. |
| [`PITCH-SCRIPT.md`](PITCH-SCRIPT.md) · [`QA-PREP.md`](QA-PREP.md) | The three-minute pitch script and the Q&A preparation. |
| [`DEPLOY.md`](DEPLOY.md) | A password-gated Vercel deployment: edge middleware that returns 401 before any file is served, and a `.vercelignore` that uploads only the explorer, never the pipeline, the notes or the data. |
| `ETHack/contested/` | An earlier, independent pipeline on free US government data (SEC XBRL, EPA GHGRP, EPA EEIO), 30 companies across 10 sectors. `DEFENCE.md` answers ten likely attacks. |
| `ETHack/speccurve/` | The formula on synthetic data, kept as a reference implementation. |
| `bruh/mat maps/` | The Bloomberg export and our credit workbook. See `WITHHELD.md`. |
| `PAPER.md`, `PAPER.pdf` | An earlier draft, kept as working history. Where it and `CONTESTED.pdf` disagree, `CONTESTED.pdf` is current. |
| `ETHack/*.md` | The working notes, timestamped across the 24 hours. Kept deliberately: the reasoning is part of the submission. |

## Data

| Source | Gives | Licensed? |
|---|---|---|
| Bloomberg materiality maps, 18 companies, 2021 to 2025 | 135 planned fields plus 57 more, across five BECS peer groups | **Yes. Withheld, see `bruh/mat maps/WITHHELD.md`** |
| Our FY2025 credit workbook | leverage, coverage, FCF, payout, maturities, ROCE, reserve life, three agencies' adjusted leverage | No. SEC XBRL and published ratings |
| SEC XBRL frames, EPA GHGRP, EPA EEIO v1.3 | the `contested/` pipeline: revenue, facility emissions, supply-chain factors | No. Free, government, no API key |

**On the withheld data.** We do not share the Bloomberg indicators and values,
because they require the proper licensing. We are happy to show you the files in
person, to prove that the model is built on real data and that the approach is
scalable and feasible. Everything derived from them is committed: the loader, the
formula, every computed output, and the working explorer. The only step a reader
cannot rerun without a Terminal is `model/load.py`, the single function that
touches raw cells.

## Reproducing

```bash
cd ETHack/model
python3 registry.py     # the field registry, printed for eyeball checking
python3 load.py         # needs the Bloomberg export; fails with a clear message without it
python3 run.py          # all 17,496 specifications -> out/
python3 export_web.py   # the pillar cube -> ../web/data/
```

`numpy` and `pandas` only. The browser explorer reproduces `run.py` to 0.05 rank
points on all 18 companies, and the specification-index decode is verified against
Python cell by cell, so nothing in the page is precomputed toward a particular
answer.

---

**Challenge Accepted** · Aram Vartanian, Arthur Petrov, Khezan Irani, Shahbaz Irani
· ETH Zürich
