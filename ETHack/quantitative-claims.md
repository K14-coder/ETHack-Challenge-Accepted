---
edit: owned
last_edited: 2026-09-12T14:11:58 CET
changes: 0
type: project-note
status: active
---
# The provider objection, the quantitative claims, and scalability

Three questions raised at team level on 12 Sep. All three have clean answers.

## 1. "We only have 8 to 10 rating providers, that is not enough"

**Correct objection, wrong design.** It kills an approach we already rejected, and does not touch the one we chose.

| | Provider-based divergence study | **Our specification-based study** |
|---|---|---|
| Where the variation comes from | different companies' ratings | **different method choices, ours** |
| n per company | 5 to 10, whatever you can license | **72, because we generate them** |
| Data needed | MSCI + LSEG + Sustainalytics licences | **none. free government data only** |
| Is n a constraint? | yes, hard ceiling | **no. n is a design parameter** |

We are not averaging other people's scores. We build **one** score and compute it 72 ways.

**n is something we choose, not something we are given.** We picked 72 because that is the full factorial of five defensible dimensions and because it puts P10 safely at the 8th order statistic. We could run 144 by adding a sixth dimension. The ceiling is imagination and defensibility, not licensing.

This is also why the colleague's instinct was right in general: **that ceiling is exactly why we abandoned the rating-comparison angle at 11:45 this morning.** Same reasoning, already applied.

### "But there might be a lot of contested companies"

If 60% of the index turns out contested, that is not a failure. That is a **bigger** finding, and a more alarming one.

The only real failure mode is different: **no variance in contestation.** If every company moves by roughly the same amount, contestation stops discriminating and the map in Figure 2 is a horizontal smear.

We already have evidence against that, from real data:

- **Nucor.** 5.76 Mt disclosed across 26 facilities. Its emissions are its own electric-arc furnaces, so widening the boundary changes the picture relatively little. Low sensitivity.
- **Walmart.** No emissions figure in the mandatory dataset at all. Every missing-data rule sends it somewhere completely different. Maximum sensitivity.

Two real S&P 500 companies, same index, same year, same free dataset, at opposite ends of the contestation axis. **The variance exists and we have already measured both ends of it.**

## 2. The quantitative claims

Six, all falsifiable, all computable from what we can get. Ranked by what they are worth on stage.

### Claim 1, the headline: benchmark our divergence against theirs

> **Spearman rank correlation between the kindest and the harshest defensible specification: ρ = ___**

Compare directly to **0.61**, the average inter-rater correlation in Berg, Kölbel and Rigobon.

If ours comes in **below 0.61**, the sentence is:

> *The disagreement we generate from our own defensible method choices is larger than the disagreement between commercial rating agencies. The industry's credibility problem is not that the agencies differ. It is that the measurement itself is underdetermined.*

That is the most quotable result available to us, it is benchmarked against a published number, and it is one line of `scipy.stats.spearmanr`.

If it comes in **above 0.61**, that is also publishable and honest: our five dimensions capture less variation than the full set of choices real raters make, which bounds our own claim. Either direction is a result. **State both branches before computing it, so we are not accused of picking the flattering one.**

### Claim 2, the depth: our own variance decomposition

> **Of total rank variance across specifications, ___% is attributable to boundary choice, ___% to denominator, ___% to missing-data rule, ___% to peer group, ___% to consolidation approach.**

This is our version of the paper's 36.7 / 50.1 / 13.2 table, computed on the S&P 500 from free data. Nobody has this number. It requires the full factorial, which is the real reason to run all 72 rather than sample.

### Claim 3, the scale

> **___ of 500 companies have a full rank range exceeding ___ places across 72 defensible methods.**

The headline count. Pick the threshold *before* looking (100 places, i.e. a fifth of the index, is a defensible round number).

### Claim 4, the disclosure gap

> **The median S&P 500 company's modelled footprint is ___× its disclosed footprint.**

We already have one data point: **Nucor, 4.74×.**

### Claim 5, the single-convention claim

> **___ companies change quartile on the consolidation convention alone**, with boundary, denominator, missing-data rule and peer group all held fixed.

Powerful because it isolates one accounting choice that no published score discloses. Nucor moves 4.59% on this dimension.

### Claim 6, the sector claim

> **Median contestation by GICS sector.** Expect Financials and Consumer Discretionary high, Energy and Utilities low.

Flag n for the thin sectors (Energy ~23, Materials ~28).

## 3. Is it scalable, and is it feasible today

Yes to both, and the numbers are measured rather than guessed.

### Compute is not the constraint

500 companies × 72 specifications = **36,000 score computations**. Vectorised in numpy, the whole matrix plus 72 full rankings plus all three spread statistics: **12 milliseconds**, measured.

There is no scaling problem. Not at 500, not at the Russell 3000.

### The API budget, and the one mistake that would kill us

| Step | Calls |
|---|---|
| Wikipedia constituents | 1 |
| SEC `company_tickers.json` | 1 |
| SEC frames API, 4 revenue tags × 1 year | **4** (each returns *every* filer) |
| GHGRP facility table, ~8,000 rows at 1,000/page | 8 |
| GHGRP emissions table, ~24,000 rows at 1,000/page | 24 |
| EPA EEIO factor CSV | 1 |
| **Total** | **~39** |

**The mistake that would sink the project: querying per company.** `parent_company/contains/NUCOR` is perfect for one company and catastrophic for 500. That is 500+ calls and hours of wall-clock.

**Pull each table once, join locally.** ~40 calls, minutes. Verify the actual row counts with one probe call before committing to the page size.

### What is actually hard

Not compute. Not API volume. **Name matching**, and it is the only real risk:

- three spellings of Walmart inside its own twelve rows
- `EXXONMOBIL CORP` and `EXXON MOBIL CORP` in the same dataset
- ownership percentages embedded in the same string as the name
- the pre-2018 legal name still in use

Mitigation is unchanged from [[Efforts/Active/ETHack/data-plan|data-plan]]: match the top ~100 emitters properly with a manual review pass, let EEIO cover the tail, **hard cap two hours**. Every company still gets a modelled number, so the index is always complete.

### Honest limit for tonight

Coverage of *disclosed* Scope 1 will be partial. That is fine and it is on-thesis: an incomplete disclosure match raises contestation, and contestation is the output. We report the match rate as a number rather than hiding it.

## Related

[[Efforts/Active/ETHack/how-many-specs|how-many-specs]] · [[Efforts/Active/ETHack/data-plan|data-plan]] · [[Efforts/Active/ETHack/proof-nucor|proof-nucor]] · [[Efforts/Active/ETHack/finding-walmart|finding-walmart]] · [[Efforts/Active/ETHack/aggregate-confusion|aggregate-confusion]]
