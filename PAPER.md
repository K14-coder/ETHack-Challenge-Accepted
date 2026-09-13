# CONTESTED

### A sustainability framework for the S&P 500 that publishes its own uncertainty

**Sector note — Initiating framework coverage**
**S&P 500 Energy · 18 companies · FY2021–FY2025**

ETHack 2026 · Challenge #1 · Citadel & Citadel Securities
13 September 2026

---

> **We do not publish an ESG score. We publish the distribution of every
> defensible ESG score, and the width of that distribution is the most useful
> number nobody reports.**

| | |
|---|---|
| **Universe** | 18 S&P 500 Energy constituents, five Bloomberg BECS peer groups |
| **Inputs** | 139 fields across four pillars — Environment, Social, Governance, Financial resilience |
| **Method** | Specification curve analysis (Simonsohn, Simmons & Nelson, 2020) applied to ESG scoring |
| **Grid** | 9 discretionary axes → **17,496 defensible specifications** per company, per weighting |
| **Headline** | Median company moves **7.0 places of 18** across its interquartile range |
| **Settled** | **2 of 153** pairwise comparisons survive every method. A published league table asserts all 153. |
| **Deliverable** | Consensus rank · contestation · the axis that decides it · the disclosure that would settle it |

---

## Executive summary

**1. The product the market buys is a point estimate of a quantity that has no
point estimate.** Berg, Kölbel & Rigobon (2022) measured an average correlation
of 0.61 between the major ESG raters, against 0.99 for credit ratings. Every
provider computes a distribution over method choices, publishes one draw from it,
and discards the rest. The discarded part is the information an allocator needs.

**2. We did not invent our uncertainty axes.** We read MSCI's and Bloomberg's
published methodologies end to end and identified thirteen points at which a
rater must make a discretionary call. **They differ at seven and agree at six.**
We vary the seven where they differ, fix the six where they agree, and declare
each fixed assumption. Two further axes are forced by the data itself. The result
is a 17,496-cell grid in which every cell is a method one of the two largest
providers in the market has published, or a documented variant of one.

**3. The disagreement is large and it is not an artefact.** The median company
moves 7.0 rank places of 18 across its interquartile range. Strip out every
branch a critic might call extreme — hold the question to *level*, raise the
evidence bar to *majority*, drop the worst-case missing rule, use sector peers —
and the median is still **3.6 places**. The spread survives the removal of its
own tail.

**4. Two negative results, published deliberately.** The aggregation function —
MSCI's arithmetic mean against Bloomberg's shifted power mean — explains **0.3%**
of rank variance. The governance-polarity question explains **0.5%**. We
implemented both specifically so that we could report they do not matter here.
What does matter is *direction* (18.2%) and *peer set* (13.1%): what question you
ask, and who you ask it against. Both are scope choices. Neither is a weight.

**5. The output is not a score.** Per company we publish four objects: what is
**settled** (comparisons that hold under every method), what is **contested**,
which single choice is the **pivot**, and which missing disclosure is the
**remedy**. That is a strict superset of a rating: an allocator who wants one
number can take the consensus and ignore the rest.

---

## Exhibit 1 · The ranking, and how much of it is a choice

Full grid, 17,496 specifications, equal pillar weights. Consensus is the median
rank percentile; contestation is the interquartile width, reported in **rank
places out of 18**.

| # | Ticker | BECS peer group | Consensus | Contestation (places) | Verdict | Decided by | Coverage |
|---:|---|---|---:|---:|---|---|---:|
| 1 | BKR | Oilfield Services | 82 | 6.0 | opinion | peer set (22%) | 78% |
| 2 | EXE | Exploration & Production | 82 | 6.0 | opinion | direction (34%) | 91% |
| 3 | CTRA | Exploration & Production | 76 | 7.0 | opinion | window (20%) | 81% |
| 4 | VLO | Refining & Marketing | 71 | 5.0 | opinion | missing data (11%) | 77% |
| 5 | EOG | Exploration & Production | 71 | 10.0 | opinion | direction (60%) | 90% |
| 6 | SLB | Oilfield Services | 65 | 7.0 | opinion | direction (26%) | 78% |
| 7 | COP | Exploration & Production | 53 | 6.0 | opinion | direction (20%) | 93% |
| 8 | OXY | Exploration & Production | 47 | 10.0 | opinion | direction (38%) | 92% |
| 9 | XOM | Integrated Oils | 47 | 6.0 | opinion | direction (29%) | 99% |
| 10 | MPC | Refining & Marketing | 41 | 9.0 | opinion | direction (49%) | 79% |
| 11 | PSX | Refining & Marketing | 41 | 8.0 | opinion | direction (9%) | 77% |
| 12 | TRGP | Midstream | 41 | 9.0 | opinion | peer set (26%) | 74% |
| 13 | WMB | Midstream | 41 | 11.0 | opinion | peer set (13%) | 75% |
| 14 | KMI | Midstream | 41 | 7.0 | opinion | peer set (11%) | 76% |
| 15 | DVN | Exploration & Production | 35 | 6.0 | opinion | peer set (32%) | 89% |
| 16 | CVX | Integrated Oils | 35 | 6.0 | opinion | missing data (8%) | 97% |
| 17 | HAL | Oilfield Services | 18 | 7.0 | opinion | direction (20%) | 78% |
| 18 | FANG | Exploration & Production | 18 | 4.0 | opinion | peer set (20%) | 91% |

*Verdict thresholds: robust < 1.5 places, contested < 3.0, opinion ≥ 3.0. Source:
`ETHack/model/out/summary.csv`, `pivot.csv`.*

**Read the table as a warning, not a ranking.** Under the full grid every company
is an opinion. That is the honest result for this sector on this data, and the
value is carried by the three columns to the right of the consensus, not by the
consensus itself.

---

## 1. The problem

### 1.1 A number that is a choice

Sustainability ratings are consumed as measurements. They are constructed as
opinions. The gap is measurable and it is large:

**Exhibit 2 · Inter-rater agreement**

| Domain | Average pairwise correlation | Source |
|---|---:|---|
| Credit ratings | 0.99 | Berg, Kölbel & Rigobon (2022) |
| ESG ratings, six major providers | 0.61 | Berg, Kölbel & Rigobon (2022) |
| ESG ratings, alternative estimate | 0.45 | Dimson, Marsh & Staunton (2020) |

Berg et al. decompose that divergence into three causes: **measurement** (the
same concept measured differently, 50.1%), **scope** (what counts at all, 36.7%)
and **weights** (13.2%). The finding that governs this paper's design is the last
one: **weights are the smallest of the three causes**, and a framework that
varies only weights attacks 13% of the problem while leaving 87% untouched.

### 1.2 Why this matters to an allocator

An allocator does not act on a score; they act on a decision rule — include or
exclude, overweight or underweight, engage or divest. A rating is useful exactly
insofar as it changes that decision reliably. A rating that moves seven places
out of eighteen depending on conventions the provider did not disclose does not
change the decision reliably; it changes it arbitrarily, and the arbitrariness is
invisible.

The framework in this paper makes it visible, and separates the companies about
which every defensible method agrees from the companies about which the rating is
an opinion. The first is investable information. The second is a warning label.

---

## 2. What we mean by sustainability

**This is the largest assumption in the framework and we state it first.**

MSCI rates a company's resilience to *financially relevant* ESG risk and frames
externalities by whether they become unanticipated costs **for the company**
(MSCI, p.3). Bloomberg defines financial materiality as impact on revenue,
operating costs, cost of capital, asset value and liabilities (Bloomberg, p.8).
Both measure **single materiality**, outside-in: the world's effect on the firm.
Neither measures the firm's effect on the world.

Our indicator set does not do this. Scope 1 emissions, embedded carbon in
reserves, gas flaring, freshwater withdrawal, spill volume and recordable
incident rates are **externality** measures, inside-out. Our financial pillar —
leverage, coverage, refinancing wall, reserve life — is closer to the providers'
frame, and is included on the grounds that a company which cannot survive its
capital structure cannot deliver on a 2050 commitment.

So the framework is a deliberate hybrid, and the challenge brief does not resolve
which of the two it wants. That ambiguity is itself a finding: **the single
question that determines every downstream choice is not settled by the mandate,
and the two incumbents resolved it the same way without being asked to.**

We fix this rather than varying it, for a structural reason. Switching the
direction of materiality changes the *indicator set*, not the arithmetic over a
fixed indicator set. A specification curve varies the method holding inputs
constant; two different indicator sets are two different studies.

---

## 3. Data

### 3.1 Sources

**Exhibit 3 · Data sources**

| Source | Provides | Licensed |
|---|---|---|
| Bloomberg materiality maps, 18 companies, FY2021–FY2025 | 135 requested fields plus 57 further delivered, across five BECS peer groups, ES and G sheets | **Yes — withheld** |
| Own FY2025 credit workbook | leverage, interest coverage, FCF/debt, capex/D&A, payout/FCF, maturities <24m, ROCE, reserve life, three agencies' adjusted leverage | No — SEC XBRL, published ratings |
| SEC XBRL frames · EPA GHGRP · EPA EEIO v1.3 | secondary pipeline, 30 companies across 10 GICS sectors (see §7.2) | No — free, government |

Bloomberg Terminal cell values are not redistributed. Everything derived from
them — the loader, the formula, every computed output and the working explorer —
is published. See `bruh/mat maps/WITHHELD.md`.

### 3.2 Universe

Eighteen of the twenty S&P 500 Energy constituents. **EQT and ONEOK have no
Bloomberg export and are absent**; we did not pad the sample to a round number.

| BECS peer group | n | Members |
|---|---:|---|
| Exploration & Production | 7 | COP, CTRA, DVN, EOG, EXE, FANG, OXY |
| Integrated Oils | 2 | CVX, XOM |
| Midstream | 3 | KMI, TRGP, WMB |
| Refining & Marketing | 3 | MPC, PSX, VLO |
| Oilfield Services & Equipment | 3 | BKR, HAL, SLB |

### 3.3 The disclosure constraint, which shapes everything downstream

**Exhibit 4 · Field coverage, by pillar and fiscal year (share of cells filled)**

| Pillar | Fields | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|---:|---:|---:|
| Environment | 37 | 59% | 59% | 60% | 61% | **36%** |
| Social | 14 | 65% | 65% | 65% | 66% | **39%** |
| Governance | 79 | 97% | 97% | 97% | 97% | 92% |
| Financial | 9 | 94% | 94% | 94% | 94% | 94% |

Two facts follow, and both became design decisions.

**First, FY2025 is barely reported for E and S.** Sustainability reporting runs a
year or more behind. Reading "the latest column" silently compares a company that
has published against one that has not. Bloomberg splits exactly this into two
products — *Latest Scores* and *Fiscal Year Scores* (Bloomberg, p.34) — and so do
we: the window axis has three options, not two, and one of them holds every
company to the last complete year.

**Second, the field set is not shared across peer groups.**

**Exhibit 5 · Fields by breadth of reporting**

| Reported by | Total | E | S | G | F |
|---|---:|---:|---:|---:|---:|
| all 18 companies | 75 | **3** | **1** | 63 | 8 |
| 12–17 companies | 40 | 18 | 8 | 14 | 0 |
| 9–11 companies | 12 | 7 | 3 | 1 | 1 |
| 1–8 companies | 11 | 9 | 2 | 0 | 0 |

Bloomberg builds the materiality map per peer group, so the five sub-industries
do not answer the same questions. **Requiring that every company in the sector
has answered the same question leaves three environmental fields and one social
field.** An eighteen-company comparison of environmental *performance* does not
exist in this export. That is not a gap in our pipeline; it is what the sector's
disclosure looks like when you demand comparability.

### 3.4 What is not in the data

**There is no revenue and no headcount anywhere in the export.** EBITDA is the
economic denominator available to us. Bloomberg's own methodology calls revenue a
*fallback* for when the physical activity metric is unavailable (Bloomberg,
p.17); we are one rung further down that ladder and say so. Production in MMboe/a
exists for the nine producers only — so **the correct denominator is unavailable
for half the sector**, which is Bloomberg's documented fork made literal.

The credit workbook is a single fiscal year. Under *change* the financial pillar
therefore has no trajectory and drops out, and the composite renormalises over
the pillars that remain. Holding one year flat and reporting a change of zero
would be a fabricated time series.

---

## 4. Method

### 4.1 Where the providers actually choose

We read both methodologies and located every point at which a rater must exercise
discretion. **Seven differ; six agree.** We vary the seven and fix the six.

**Exhibit 6 · Provider decision-point map**

| # | Decision | MSCI | Bloomberg | Same? | Our treatment |
|---:|---|---|---|---|---|
| 1 | What is measured | financially material risk **to the firm** | financially material risk **to the firm** | agree | **fix** — and declare our hybrid (§2) |
| 2 | Peer group | GICS Sub-Industry, 8-digit | **BECS**, a bespoke ESG classification | differ | **vary** |
| 3 | Size denominator | modelled 0–10 exposure, ~80 segment metrics | explicit activity metric; revenue as fallback | differ | **vary** |
| 4 | Raw value → grade | percentile benchmarks | **rejects percentiles in print**; log-log residual | differ | **vary** |
| 5 | Missing data | absence scores 0 on *management* | no imputation; drop, then cap by disclosure | differ | **vary** |
| 6 | Aggregation | weighted **arithmetic** mean | weighted **power mean**, p=½, s=1 | differ | **vary** |
| 7 | Pillar weights | impact × horizon; **G floored at 33%** | analyst rank 1–5; **G fixed at rank 3** | differ in mechanism | **fix** at presets + user slider |
| 8 | Relative or absolute | E,S relative; **G absolute** | mostly relative; **fatalities absolute** | both break their own rule | **fix** relative, pair with absolutes |
| 9 | Time window | 3-year controversy lookback | parameters over 3 most recent years | agree on 3 years | **vary** window and direction |
| 10 | Final discretisation | 0–10 into **7** letter grades | 0–10 into **7** bands | agree; neither justifies 7 | **fix** — we do not discretise |
| 11 | Human override | committee overrides and truncations | none; judgement is upstream | differ | **fix** — none |
| 12 | Controversies | central: severity matrix, 3-year lookback | **absent entirely** | differ | **fix** — absent, declared |
| 13 | Non-public data | refused outright | public only, limited regional estimation | near-agree | **fix** — public only |

Decision 11 is worth isolating. MSCI factors committee-level overrides into the
final industry-adjusted score and requires committee approval for exceptions,
truncations and two-notch rating changes. **A specification curve requires the
method to be a function of the data. You cannot enumerate a committee.** Our
model is Bloomberg-shaped by necessity as much as by preference.

### 4.2 The nine axes

**Exhibit 7 · The specification grid**

| Axis | Options | n | Provenance |
|---|---|---:|---|
| Exposure base | EBITDA · equity · production | 3 | Bloomberg activity metrics, p.17 |
| Window | latest · fiscal year · 3-year mean | 3 | Bloomberg Latest vs Fiscal Year, p.34 |
| Direction | level · change | 2 | Bloomberg Rate-Anchored model, p.18 |
| Polarity | orthodox · neutral · stability | 3 | 15 fields where the two governance conventions disagree |
| Normaliser | percentile · winsorised · log min–max · elasticity | 4 | MSCI p.12; Bloomberg pp.41, 45–46 |
| Peer set | BECS group · producers/downstream · all 18 | 3 | MSCI GICS vs Bloomberg BECS |
| Evidence bar | permissive · majority · strict | 3 | forced by this data, §4.4 |
| Missing data | excluded · worst case · capped | 3 | Bloomberg pp.23, 26 |
| Aggregation | arithmetic · power p=½ · geometric | 3 | MSCI p.10 vs Bloomberg p.25 |

**3 × 3 × 2 × 3 × 4 × 3 × 3 × 3 × 3 = 17,496 specifications**, evaluated at any
pillar weighting the user selects.

The **elasticity** normaliser deserves note because it is Bloomberg's actual
model rather than a variant we invented. They fit, per peer group,

```
log(Impact) = log(Intensity) + γ · log(Activity) + ε
Score       = 10 × [1 − Φ(ε / σ)]
```

and score the residual — how far a company sits from the emissions its peer
group's size-elasticity predicts. Their own text notes that when γ = 1, *the
traditional assumption*, ranking on the residual is equivalent to ranking on
intensity (Bloomberg, p.46). The entire difference between the market's headline
model and a naïve intensity ranking is one parameter that they estimate and
everyone else assumes.

### 4.3 The formula

Nine axes, eight steps. Steps 1–5 produce a grade tensor and do not involve the
pillar weights, which is what allows the last steps to run live in the browser.
Full statement in **Appendix A**.

```
1  exposure       divide by the base (quantities) or select the published variant (rates)
2  window         latest reported · fixed fiscal year · 3-year mean
3  direction      level or change
4  orientation    apply polarity; higher = worse, always
5  normalisation  raw value → 0–100 grade within the peer set
6  aggregation    fields → pillar → composite, under the missing-data rule
7  rank           percentile of the composite across the 18
8  distribution   median and interquartile width across the selected specifications
```

**The order of operations matters and must not be inverted.** Aggregate the
fields *inside* each specification (step 6), *then* take the distribution across
specifications (step 8). Reversing them averages 139 fields first, which
concentrates the result and collapses the spread — same inputs, opposite
conclusion, purely from the order.

Two rules are rules, not specifications, and are not varied: a peer group below
**three** members is graded against the sector (two members can only ever return
0 and 100), and the elasticity normaliser requires **eight** points to fit a
slope, below which that cell falls back to log min–max.

### 4.4 The evidence bar — an axis this data forced

The missing-data question has a second form that neither provider documents: not
*what do we do with an empty cell*, but *does this field belong in the model at
all*. We make it an axis, tightening two things together — how much of the peer
set must report a field, and how substantive a policy flag must be.

**Exhibit 8 · The inclusion ladder (fields in the model)**

| Level | Peer set must report | Boolean tier | E | S | G | F |
|---|---|---|---:|---:|---:|---:|
| permissive | ≥ 50% | any disclosed policy | 28 | 12 | 78 | 9 |
| majority | ≥ 67% | constrains an operating decision | 12 | 7 | 53 | 8 |
| strict | 100% | carries a quantified commitment | 2 | **0** | 47 | 8 |

*Sector peer set. Source: `spec.inclusion_mask`.*

**At the strict end the Social pillar has no fields left**, drops out, and the
weights renormalise over the three that remain.

Narrowing the peer group runs the other way. For an Exploration & Production
company the same strict setting leaves **13 environmental fields and 2 social**,
because its peers all report the same things. **Comparing fewer companies lets
you compare them on more.** That is the intra- versus inter-group trade, and in
our tool it is a control rather than a footnote.

### 4.5 What we deliberately do not vary

Pillar weights are not an axis. Varying them forms convex combinations of the
same indicators; every result lies in the convex hull of the indicator ranks and
many draws concentrate on the equal-weighted answer by the central limit theorem.
Berg et al. put weights at 13.2% of divergence. Our axes attack the other 86.8%.

Weights are instead handed to the user as a continuous slider with five named
presets — a capability, we note, that **neither MSCI nor Bloomberg ships**. Both
hand you one vector per industry and no way to change it.

---

## 5. Results

### 5.1 The spread is real and survives its own tail

**Exhibit 9 · Median contestation by stratum**

| Stratum | Specifications | Median IQR (pts) | Median IQR (places of 18) |
|---|---:|---:|---:|
| Full grid | 17,496 | 41.2 | **7.0** |
| Level only | 8,748 | 29.4 | 5.0 |
| Level + majority evidence bar | 2,916 | 35.3 | 6.0 |
| Level + majority + no worst-case | 1,944 | 32.4 | 5.5 |
| Level + majority + sector peers | 972 | 23.5 | 4.0 |
| Level + majority + no worst-case + sector | 648 | 21.3 | **3.6** |
| Level + strict evidence bar | 2,916 | 17.6 | 3.0 |

Remove every branch a critic could call extreme and the median company still
moves **3.6 places out of 18**. The contestation is not an artefact of one silly
option; it is a property of the evidence.

### 5.2 What is actually settled

A total ordering of eighteen companies is a claim this data cannot support. What
survives is a **partial order**: for each pair, the share of specifications in
which one company outranks the other.

**Exhibit 10 · Settled pairwise comparisons**

| Criterion | Settled | of 153 | Share |
|---|---:|---:|---:|
| Full grid, P > 0.99 | 1 | 153 | 1% |
| Full grid, P > 0.95 | 2 | 153 | 1% |
| Full grid, P > 0.90 | 3 | 153 | 2% |
| Full grid, P > 0.80 | 26 | 153 | 17% |
| Full grid, P > 0.75 | 42 | 153 | 27% |
| Level only, P > 0.95 | 33 | 153 | 22% |
| Level + strict, P > 0.95 | **56** | 153 | **37%** |

**A published league table asserts all 153 comparisons.** Under the full grid,
two of them hold. Narrow the question to *level* and raise the evidence bar to
*strict* and 56 hold — the same data, a narrower question, and a ranking that is
partly real emerges from one that was not.

This is the central deliverable. Not a score, but a map of which comparisons the
evidence can carry.

### 5.3 Where the disagreement lives

The grid is a complete balanced factorial, so the variance of a company's rank
decomposes into main effects with no design correction: η² = SS(axis) / SS(total).

**Exhibit 11 · Variance decomposition, mean across the 18 companies**

| Axis | Mean η² | Max for a single company | Companies for which it is the pivot |
|---|---:|---:|---:|
| Direction | **18.2%** | 60.2% (EOG) | 9 |
| Peer set | **13.1%** | 31.9% (DVN) | 6 |
| Evidence bar | 3.8% | 12.1% | 0 |
| Window | 3.8% | 20.2% | 1 |
| Normaliser | 3.3% | 12.6% | 0 |
| Missing data | 3.0% | 10.8% | 2 |
| Exposure base | 1.8% | 4.8% | 0 |
| Polarity | **0.5%** | 3.4% | 0 |
| Aggregation | **0.3%** | 2.2% | 0 |
| **Main effects** | **47.8%** | | |
| **Interaction** | **52.2%** | | |

Three readings.

**The two axes that matter are scope axes.** *Direction* is what question you are
asking — where a company stands, or how far it has moved. *Peer set* is who you
ask it against. Neither is a weight, and neither is a measurement refinement.
This is Berg et al.'s 36.7% scope bucket, reproduced from the bottom up on one
sector.

**More than half the variance is interaction.** Main effects account for 47.8%.
The remaining 52.2% consists of choices that only matter in combination — which
is precisely why sensitivity analysis one dimension at a time, the standard
industry practice, understates the problem.

**Two axes are negative results and we report them as such.** The aggregation
function explains 0.3%. This is the fork between MSCI's arithmetic mean and
Bloomberg's power mean, a genuine published disagreement with real conceptual
content — whether excellent governance can offset poor emissions — and on this
data it is worth a third of one percent. The governance-polarity question, to
which our own question set devotes an entire worksheet, explains 0.5%. Both were
implemented so that we could measure them rather than assume them.

### 5.4 The remedy — which silence costs the most

For a contested company we can identify the unreported field whose absence
carries the most spread, by removing that single silence from the model and
measuring how far the interquartile width falls.

**Exhibit 12 · Highest-value missing disclosures**

| Company | Field | Contestation removed (pts) |
|---|---|---:|
| TRGP | Total Recordable Incident Rate | 29.4 |
| TRGP | Physical Risk Identified | 29.4 |
| TRGP | Hazardous Waste Management Policy | 29.4 |
| SLB | Percentage of Hazardous Waste | 23.5 |
| SLB | Hazardous Waste | 23.5 |
| WMB | Total Recordable Incident Rate | 17.6 |
| DVN | Tier 1 Process Safety Event Rate | 17.6 |

This converts the framework from a scoring tool into a **targeted disclosure
demand**, and names the user the challenge asks us to name: an engagement team, a
regulator drafting a disclosure rule, or a company deciding what to publish next.

---

## 6. Risks to this analysis

Stated before anyone asks, and in descending order of how much they hurt.

**6.1 The grid is enumerated, not sampled.** The 17,496 specifications are a set
of conventions we constructed, not a random sample from a population of methods.
The spread is a *range*, and we never call it a confidence interval. Nor are the
cells independent: `change × latest` and `change × mean3` share most of their
underlying data, so the effective number of distinct methods is materially below
17,496.

**6.2 N = 18 quantises the output.** A rank percentile over 18 companies takes 18
values, 5.88 points apart. Any interquartile width quoted in percentile points is
a quantised quantity wearing a decimal, which is why every headline in this paper
is in rank places. The remedy is a larger universe, not a different statistic.

**6.3 The min–max range is not informative at the full grid.** Seventeen of
eighteen companies span 0 to 100. Those extremes are rare — 2.2% of cells for
XOM — and concentrated in `direction = change` crossed with the log-family
normalisers and the smallest peer groups. We therefore lead on the interquartile
width and report the range only for completeness.

**6.4 The economic denominator is a fallback of a fallback.** No revenue, no
headcount. EBITDA is a defensible scale proxy but it is volatile for this sector
and it is not what Bloomberg would use.

**6.5 Governance dominates by field count.** 79 of 139 fields are governance, and
63 of those are reported by all 18 companies. The G pillar score is consequently
far more stable across specifications than E or S, so the contestation we measure
is mostly environmental and social. That is a property of the disclosure regime,
not of the companies.

**6.6 We rank the energy sector against itself.** If every constituent is bad,
the best relative performer still scores well. Bloomberg names this failure mode
in its own methodology (p.42) and does not treat it; we pair every rank with an
absolute intensity for the same reason, but relative scoring remains relative.

**6.7 Controversies are absent.** A whole scoring component present in MSCI and
absent from Bloomberg is also absent from us. This is a scope boundary, declared,
not an oversight.

**6.8 One sector, one year of financials.** No cross-sector claim is available
from this run, and no trajectory claim is available for the financial pillar.

---

## 7. What this is, and what it is not

### 7.1 It is a framework, and a superset of a rating

The sharpest attack on this work is that it critiques ESG rather than delivering
the framework the challenge asked for. It delivers both. Per company the output
is a **consensus score** — the median across defensible methods, which is the
number the challenge asked for — and a **contestation figure**, which is the part
nobody else provides. Anyone who wants one number can take the consensus and
ignore the rest. Dropping the second number would not make this more of a
framework; it would make it a less honest one.

### 7.2 It scales

The method is O(cells) and the cells are cheap. The full 17,496-specification run
over 18 companies and 139 fields completes in **18 seconds** on a laptop. A
secondary pipeline in `ETHack/contested/` demonstrates the data path at sector
breadth: 30 companies across 10 GICS sectors, assembled from SEC XBRL frames, EPA
GHGRP facility emissions and EPA EEIO supply-chain factors — all free, all
government, no API key, roughly 39 API calls for the whole S&P 500 because the
bulk endpoints return every filer at once. The binding constraint on scaling is
parent-company name matching, not computation.

### 7.3 Section 8 — net-zero portfolio allocation

The bonus question is answered as an output of this framework rather than as a
separate opinion, and is treated in a companion section not included in this
draft.

---

## Appendix A · The formula

Indices: company *i* = 1…18, field *f* = 1…139, year *y* = 1…5, base slot *b* ∈
{1,2,3}, pillar *P* ∈ {E, S, G, F}.

**A.1 Inputs.** `VAR[i,f,y,b]` the reported number, NaN where not reported;
`BASE[i,b]` the exposure denominator; `type[f]` ∈ {Q quantity, R rate, P
percentage, B boolean, S structural}; `pol[f]` ∈ {+1, 0, −1} under each of three
polarity conventions; `pil[f]` the pillar.

**A.2 Step 1 — exposure.** One operator per type, so the divisor is applied
exactly once on every branch:

```
x[i,f,y] = VAR[i,f,y,b] / BASE[i,b]     if type = Q      APPLY the divisor
         = VAR[i,f,y,b]                 otherwise        SELECT the published variant
```

Slot meanings: for Q, EBITDA / equity / production; for a rate triple,
employees / contractors / total workforce; for agency-adjusted leverage,
Moody's / S&P / Fitch.

**A.3 Steps 2–3 — window and direction.** Reductions are taken over the years a
company actually reported, not over calendar columns:

```
level  · latest      q = last reported value
level  · fiscal year q = value at the last complete sector year (FY2024)
level  · mean3       q = mean of the last three reported values
change · w           q = (end − start) / |start|,  end and start per w
```

For booleans, *change* is the plain difference. For single-year fields (the
financial pillar) *change* returns NaN and the field drops out.

**A.4 Step 4 — orientation.** `u[i,f] = pol[f] · q[i,f]`, so higher *u* is worse,
always. A polarity of 0 means the field is deliberately neutral under that
convention: present in the model, discriminating nothing.

**A.5 Step 5 — normalisation.** Peer set *G(i,p)*; `U = { u[j,f] : j ∈ G,
reported }`; *m* = |U|. All four produce 0–100 with 100 = best.

```
percentile   r = average rank of u in U ascending;  s = 100 (m − r)/(m − 1)
winsorised   lo,hi = 5th,95th pct of U;             s = 100 (hi − clip(u,lo,hi))/(hi − lo)
log min–max  L = log(u shifted positive);           s = 100 (max L − L)/(max L − min L)
elasticity   log u = c + γ log(base) + ε;           s = 100 (1 − Φ(ε/σ))
```

**A.6 Step 6 — aggregation.** Fields → pillar → composite, both levels using the
same weighted shifted power mean with *p* = ½ and, on this 0–100 scale, *s* = 10:

```
M(x, w, p, s) = ( Σ wⱼ (xⱼ + s)^p )^(1/p) − s
```

*p* = 1 recovers MSCI's arithmetic mean; *p* → 0 the geometric mean. Missing-data
rules: **excluded** drops the field and redistributes weight; **worst case**
enters it as 0; **capped** drops it and then limits the pillar by its own
disclosure factor, `UT = 30 + √DF × 70`, which is Bloomberg's Issue Score on our
scale.

**A.7 Step 7 — rank.** `R = 100 (N − ρ)/(N − 1)` where ρ is the average rank of
the composite descending. 100 = best of those with a score.

**A.8 Step 8 — the two outputs.** Over the selected specifications: `consensus =
median R`, `contestation = P75(R) − P25(R)`, reported in rank places by dividing
by 100/(N − 1) = 5.88.

---

## Appendix B · Axis option definitions

| Axis | Option | Definition |
|---|---|---|
| Exposure base | ebitda | Q divided by FY2025 EBITDA; R takes the employee-population variant; leverage takes Moody's adjustment |
| | equity | Q divided by total equity incl. NCI; R takes the contractor variant; leverage takes S&P |
| | production | Q divided by MMboe/a; R takes total-workforce; leverage takes Fitch. Producers only (9/18) |
| Window | latest | each company's most recent reported year for that field |
| | fy_common | FY2024 for every company, the last year the sector reported at full rate |
| | mean3 | mean of the last three reported values |
| Direction | level | the reduced value itself |
| | change | relative change from three reported steps earlier; plain difference for booleans |
| Polarity | orthodox | governance orthodoxy: short tenure, low pay, board refreshment |
| | neutral | the 15 contested fields score 50 and discriminate nothing |
| | stability | the continuity reading: retained experience, institutional knowledge |
| Normaliser | percentile / winsorised / log min–max / elasticity | see A.5 |
| Peer set | subgroup | the five BECS peer groups, with the MIN_PEERS = 3 fallback |
| | chain | producers (9) vs midstream, refining and services (9) |
| | sector | all 18 |
| Evidence bar | permissive / majority / strict | see Exhibit 8 |
| Missing data | excluded / worst case / capped | see A.6 |
| Aggregation | arithmetic / power p=½ / geometric | see A.6 |

---

## Appendix C · Field registry

139 logical fields. Rate triples (TRIR, LTIR, fatality rate) are collapsed to one
logical field each so that safety is not counted three times, with the exposure
base selecting the published population.

| Pillar | Boolean | Percentage | Quantity | Rate | Structural | Total |
|---|---:|---:|---:|---:|---:|---:|
| Environment | 18 | 4 | 15 | 0 | 0 | 37 |
| Social | 9 | 0 | 0 | 5 | 0 | 14 |
| Governance | 25 | 0 | 0 | 0 | 54 | 79 |
| Financial | 0 | 0 | 0 | 9 | 0 | 9 |
| **Total** | **52** | **4** | **15** | **14** | **54** | **139** |

Boolean stringency tiers: 29 *all only*, 18 *substantive*, 5 *outcome-linked*;
the remaining 87 fields are non-boolean and unaffected. Fifteen fields carry a
contested polarity — the two conventions disagree about which direction is
better — and are concentrated in governance (CEO and chair tenure, board age,
pay, auditor tenure, ownership thresholds).

**Policy flags versus outcomes.** 52 of our 139 fields are yes/no policy flags,
or **37%**; the other 87 carry a number. The split is uneven by pillar —
environment 18 of 37, social 9 of 14, governance 25 of 79, financial 0 of 9 — so
the social pillar in particular leans on policy disclosure more than we would
like, and says so.

For comparison, MSCI's own front matter describes 150 policy/programme metrics
against **20 performance metrics** on the management side, a 7.5:1
policy-to-outcome ratio (MSCI p.2). Bloomberg pushes the other way and builds
machinery to enforce it: the disclosure factor exists to stop a perfect policy
score coexisting with zero quantitative disclosure, and an issue containing only
binary fields has its weight cut by 80% (Bloomberg pp.8, 24). Our 37% sits
between the two, closer to Bloomberg, and the *evidence bar* axis is the control
that lets a reader push it further — at the strict setting only the five
outcome-linked booleans survive.

---

## Appendix D · Provider citations

- **MSCI ESG Ratings Methodology, Executive Summary, November 2020**, 17pp.
  Cited as *MSCI p.N*. Key pages: p.2 data volumes; p.3 materiality definition;
  p.4 pillar/theme/key-issue hierarchy and WAKIS; p.5 key-issue weights and the
  33% governance floor; pp.6–8 exposure, management and the risk/opportunity
  combination; p.9 controversy severity matrix and the absolute governance model;
  p.10 GICS Sub-Industry weighting; p.12 industry benchmark percentiles, the
  November 2020 change, and the seven-band letter map; p.13 data sources.
- **Bloomberg ESG Scores Methodology, issued September 2023, updated December
  2025**, 58pp. Cited as *Bloomberg p.N*. Key pages: p.7 BECS; p.8 financial
  materiality and score structure; p.11 input data and imputation; p.17 field
  attributes, disclosure-factor ranks and activity metrics; p.18 ES scoring
  models; p.21 issue priority; p.23 fit/quality weights; pp.24–26 the disclosure
  factor and the Issue Score cap; p.28 the priority weight function; p.32 pillar
  weights and worked industry examples; p.34 Latest vs Fiscal Year; p.41
  parametric versus percentile; p.42 absolute versus relative and the
  best-in-class failure mode; pp.45–46 the intensity model and the γ = 1 remark;
  pp.47–49 the remaining field-scoring distributions.
- Berg, F., Kölbel, J. F. & Rigobon, R. (2022). *Aggregate Confusion: The
  Divergence of ESG Ratings.* Review of Finance 26(6).
- Simonsohn, U., Simmons, J. P. & Nelson, L. D. (2020). *Specification curve
  analysis.* Nature Human Behaviour 4, 1208–1214.
- Dimson, E., Marsh, P. & Staunton, M. (2020). *Divergent ESG Ratings.* Journal
  of Portfolio Management 47(1).

---

## Appendix E · Reproducibility

```bash
cd ETHack/model
python3 registry.py     # the field registry, printed for inspection
python3 load.py         # the arrays, with a coverage report
python3 run.py          # all 17,496 specifications -> out/
python3 export_web.py   # the pillar cube -> ../web/data/
python3 -m http.server 4173 --directory ../web
```

`numpy` and `pandas` only. Runtime 18s for the full grid.

| Output | Contents |
|---|---|
| `out/summary.csv` | consensus, contestation, verdict, coverage per company |
| `out/long.csv` | one row per company per specification — the audit trail |
| `out/pivot.csv` | variance decomposition per company, per axis |
| `out/dominance.csv` | P(i outranks j) for all 153 pairs |
| `out/remedy.csv` | highest-value missing disclosures |
| `out/claims.json` | every number quoted in this paper, computed |

The browser explorer reproduces `run.py` to 0.05 rank points on all 18 companies,
and the specification-index decode is verified against Python cell by cell, so
nothing in the interactive tool is precomputed toward a particular answer.

**Data withheld.** Bloomberg Terminal cell values are not redistributed; see
`bruh/mat maps/WITHHELD.md` for the manifest and the regeneration path. We do not
share these indicators and values because they require the proper licensing. We
are happy to show the files in person, to demonstrate that the model is built on
real data and that the approach is scalable and feasible. Every derived
output — the loader, the formula, all computed results, the explorer — is
published.

---

## Appendix F · Glossary

| Term | Meaning |
|---|---|
| **Consensus** | Median rank percentile across the specifications in view |
| **Contestation** | Interquartile width of that distribution, in rank places out of 18 |
| **Specification** | One complete set of choices across all nine axes |
| **Pivot** | The axis explaining the largest share of a company's rank variance |
| **Settled pair** | An ordered pair holding in >95% of specifications both companies score in |
| **Evidence bar** | The joint threshold on peer-set reporting share and boolean substantiveness |
| **Disclosure factor** | Share of expected fields a company reports; caps the pillar under the *capped* rule |
| **BECS** | Bloomberg ESG Industry Classification System, their purpose-built ESG peer grouping |
| **WAKIS** | Weighted Average Key Issue Score, MSCI's pre-normalisation composite |

---

### Disclosures

Prepared for ETHack 2026, Challenge #1, sponsored by Citadel and Citadel
Securities, by a student team over 24 hours. **This is not investment research,
it is not a recommendation to buy or sell any security, and it was not prepared
by a regulated entity.** Company names appear as data points in a methodological
demonstration and no view on any issuer is expressed or implied.

All computed figures derive from the committed pipeline and can be regenerated
from source. Bloomberg and MSCI methodology documents are cited as published by
their authors; the characterisations of their methods are ours and any error in
them is ours. Bloomberg Terminal data used under the licence held by a team
member and not redistributed.
