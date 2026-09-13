---
edit: owned
last_edited: 2026-09-13T01:45:00 CET
changes: 0
type: project-note
status: proposed
---
# Where the methodology goes next

Written at T+15h with the pitch today. Everything in Tier 1 is **post-processing
over the grade tensor that already exists**. Nothing below changes `01_fetch` →
`02_score`, and nothing below needs new data. That is the only reason any of it
is proposable at this hour.

## The reframe

Version 1 of the argument: *a score is a scalar; we publish a distribution.*

That is correct and it is not enough. A distribution is still a complaint. An
allocator reading "42 ± 18" has been told their number is unreliable and given
nothing to do about it. That is the opening for the sharpest attack in
`DEFENCE.md` — *this is a critique, not a framework*.

Version 2: **the output is not a number and not a distribution. It is a
decomposition of a disagreement.** Per company, four objects:

| Output | Question it answers | Machinery |
|---|---|---|
| **Settled** | Which comparisons hold under *every* defensible method? | pairwise dominance |
| **Contested** | Which do not? | the spread we already compute |
| **Pivot** | Which single choice decides it? | variance decomposition over the axes |
| **Remedy** | What would end the disagreement? | the missing-data main effect, per field |

*We do not give you a score. We give you the comparisons that are settled, the
one question that decides the rest, and the disclosure that would close it.*

That is a product. It is a strict superset of a rating. And it turns the thing we
are accused of — refusing to publish a point estimate — into the reason the output
is more useful than a point estimate.

---

## Fix these two first. They are cheap and they are load-bearing.

**1. The contestation numbers are quantised and it shows.**
With N = 20, a rank percentile can only take 20 values, spaced 100/19 = 5.263
apart. Every number in `out/summary.csv` is a multiple of 5.263 — 10.5, 15.8,
21.1, 26.3, 36.8. An IQR of 10.5 *is* "two rank positions", dressed up as a
continuous quantity. A quant judge will see this in about four seconds.

Two-line fix: report contestation in **rank positions** alongside the percentile,
and state the resolution. "CO-14 moves 5 positions out of 20 between defensible
methods" is both honest and more legible than 26.3. Alternatively raise N — with
the full S&P 500 the granularity problem disappears.

**2. The 72 specifications are not 72 independent draws.**
`direction=change × window=latest` uses years 3→5; `change × mean3` uses
(1–3)→(3–5). Those two share most of their data. The full factorial treats all 72
as exchangeable, so the IQR is a real description of the grid but the *grid* is
not a random sample of methods. Say so before someone says it for you: the spread
is the range over an enumerated set of conventions, not a confidence interval, and
we never call it one.

---

## Tier 1 — tonight. All four are post-processing.

### 1. Locate MSCI and Bloomberg as points inside our own space

The payoff of `provider-decision-points.md`. If the grid contains the axes where
the providers differ, then each provider's documented method is (approximately) a
**cell** in our grid. So mark them.

| Axis | MSCI-like cell | Bloomberg-like cell |
|---|---|---|
| normaliser | percentile | elasticity residual (else log min–max) |
| peer set | sub-group (GICS 8-digit) | sub-group (BECS) |
| aggregator | arithmetic mean | p-mean, p = 0.5 |
| missing | worst / management penalty | disclosure cap |
| window | latest | 3-year mean |
| base | revenue | output |

Draw both on the specification curve as two labelled vertical lines. The gap
between them, per company, is **the divergence Berg, Kölbel & Rigobon measured at
0.61 correlation — reproduced, on one screen, as a distance in method space.**

This single change reframes the entire project. We stop being a rival rating and
become **the space that contains the ratings**. Attack #10 dies.

Label them **MSCI-like** and **Bloomberg-like**, never MSCI and Bloomberg. We
cannot reproduce their indicator sets, their analyst priorities, or MSCI's
committee. The claim is only: *these are the cells our grid assigns to their
published choices.* Say that out loud; it costs nothing and it is unattackable.

**Cost:** ~30 min without the elasticity normaliser, ~2h with it.

### 2. The pivot: which axis decides this company's rating

The grid is a **complete balanced factorial design**, which means the variance in
a company's rank decomposes cleanly into main effects and interactions. Standard
ANOVA, ~20 lines of numpy, no new data:

```
η²(axis) = SS(axis) / SS(total)      per company, over the 72 (or 864) cells
```

Output, per company, one sentence: *"78% of the disagreement about Nucor is the
denominator. Answer that one question and its rating is settled."*

This is the difference between a warning label and a diagnostic, and I think it is
the strongest single idea available. Nobody in ESG publishes it. It is also the
most Citadel-legible thing here: it is a factor attribution.

Panel: a small stacked bar per company, one segment per axis. Sorted, it doubles
as a sector-level finding — *"across the sector, the denominator explains more
disagreement than the normaliser and the weighting combined."*

**Cost:** ~45 min including the UI panel.

### 3. Pairwise dominance: publish the partial order, not the ranking

A total ordering of 20 companies is a claim we cannot support. What survives the
grid is a **partial order**. For every pair:

```
D[i,j] = share of specifications in which i outranks j
```

`D > 0.95` is a settled comparison. `D ≈ 0.5` means the two are **incomparable** —
and saying so is more honest and more useful than forcing them into adjacent rows
of a table.

Render as a matrix heatmap ordered by consensus: the settled block structure will
be visible as solid corners, and the mush in the middle is the part of the league
table that is fictional. Then state the headline: *"of 190 pairwise comparisons,
X are settled under every defensible method and 190 − X are not. A published
ranking asserts all 190."*

That number — how much of a league table is actually supported — is a genuinely
new statistic about ESG ratings.

**Cost:** ~40 min as a matrix. A Hasse diagram is prettier and not worth the hours.

### 4. Decision stability, which is also the $1bn answer

Nobody acts on a score; they act on a decision rule. So evaluate the *rule* over
the grid, not the score:

```
P_exclude[i] = share of specifications under which i falls in the excluded set
```

For "exclude the worst quintile", every company gets a number between 0 and 1.
`0.0` and `1.0` are decisions the method does not affect. Anything between is a
coin flip currently being reported as a fact.

This makes the bonus question an **output of the framework rather than a separate
opinion**, which is exactly what `challenge.md` says they want:

> Allocate to what is settled. Engage on what is contested. The pivot analysis
> tells you precisely what to demand in that engagement.
>
> Concretely: full weight where `P_exclude` is 0 under every method; zero weight
> where it is 1; and for the middle, hold at benchmark weight with a disclosure
> demand attached — because we can name the exact datum that would resolve them.

That is a portfolio construction rule derived from the uncertainty structure, not
bolted on. It also gives the honest answer to "what if the whole sector is bad":
`P_exclude` is relative, so we pair it with the absolute-intensity panel.

**Cost:** ~20 min.

---

## Tier 2 — if the clock allows

### 5. Minimum disclosure to resolve

Falls out of the same ANOVA as the pivot. The missing-data axis only bites on
fields a company did not report, so the missing-rule main effect, computed
leave-one-field-out, ranks each silence by how much contestation it causes:

*"Walmart's contestation drops from 44 to 12 rank points the moment it discloses
Scope 1. Nothing else it could disclose comes close."*

This is a **targeted disclosure demand**, and it names the user the Impact
criterion asks for: an engagement team, a regulator writing a disclosure rule, a
company deciding what to publish next. It converts the framework from a scoring
tool into a policy instrument. If Tier 1 lands and there is time, this is the next
one.

**Cost:** ~1h on top of the ANOVA.

### 6. The adversarial score, free of charge

You already compute the minimum over specifications. Label it: **the score your
critic will use.** An allocator defending a position to a regulator or an IC does
not care about the median, they care about the worst defensible construction of
their own portfolio. Reporting `min` as a named output rather than a whisker end
costs zero code and reframes it as risk management.

Same move on the whisker itself: with the missing-data rules spanning
drop / worst / cap, the min–max range is close to a **partial-identification
bound** in Manski's sense — the interval guaranteed to contain the score under
stated assumptions about the unreported values. Two academics on the panel will
recognise the term. Do not overclaim it as a formal bound unless the assumptions
are written down; "bound-like" with the assumptions stated is enough.

**Cost:** 10 minutes of relabelling, plus one careful sentence.

---

## Tier 3 — the roadmap slide. Say it, do not build it.

- **Is contestation priced?** Test whether high-contestation companies subsequently
  show more ESG-related surprises, more rating migration, or higher realised
  volatility. If contestation predicts anything, it stops being uncertainty and
  becomes a **signal** — which is the language the sponsor speaks. Needs data and
  time we do not have, and a null result would be honest but unhelpful today.
- **Contestation dynamics.** Falling contestation = improving disclosure. Needs the
  panel we do not have on one fiscal year.
- **Weighting the specifications.** A judge will ask: are all 72 equally defensible?
  Answer on stage — *no, and we deliberately do not weight them, because a prior
  over methods is exactly the hidden judgement we are objecting to. If you want
  one, ours is a flat prior and it is stated.* Mentioning and rejecting this is
  worth more than implementing it.
- **Reproduce the provider correlation.** With the full S&P 500 and both provider
  cells located, we could report the correlation between MSCI-like and
  Bloomberg-like scores in our own space and compare it to the published 0.61.
  That is a validation of the whole approach. It needs the index, not 20 rows.

---

## The honest novelty claim

None of this is new mathematics. Factorial variance decomposition, partial orders,
value-of-information, partial identification — all standard, all decades old. The
claim is not that we invented a technique.

The claim is: **ESG rating is a field where the central object is a contested
aggregation, and nobody has applied the standard tools for contested aggregations
to it.** Providers publish one point from a distribution they could compute and
discard the rest. We compute the distribution and then do the ordinary, boring,
correct thing with it.

State it that way. It is stronger than a novelty claim we would have to defend, and
it is the version that survives a question from an academic.

## Related

- [[Efforts/Active/ETHack/provider-decision-points|provider-decision-points]] — the axes, and why they are the right ones. Tier 1 item 1 is its payoff.
- [[Efforts/Active/ETHack/critique-weights|critique-weights]] — §4 (two panels) is the absolute-intensity companion the `P_exclude` rule needs.
- [[Efforts/Active/ETHack/quantitative-claims|quantitative-claims]] — the settled-pairs count is a new claim to add here.
- [[Efforts/Active/ETHack/challenge|challenge]] — Tier 1 item 4 is the bonus answer, derived rather than asserted.
