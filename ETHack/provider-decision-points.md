---
edit: owned
last_edited: 2026-09-13T01:20:00 CET
changes: 0
type: project-note
status: active
---
# Where MSCI and Bloomberg actually choose, and what we do at each fork

Read from the two primary sources the sponsor handed us:

- **MSCI ESG Ratings Methodology, Executive Summary, November 2020** (17 pp). Cited `M p.N`.
- **Bloomberg ESG Scores Methodology, issued Sep 2023, last updated Dec 2025** (58 pp). Cited `B p.N`.

The purpose of this note is narrow. Our whole contribution is that a sustainability
score is a **choice among defensible methods**, and we publish the distribution
instead of one point. That argument is only as good as the claim that the branches
we vary are *real* branches. This note establishes that claim from the providers'
own documents: at every axis we vary, the two largest providers in the market
made **different** choices and each published a rationale.

Where they agree, we do not vary — we fix, and say so. That asymmetry is the
discipline that stops the multiverse from becoming a toy.

---

## The map

`VARY` = becomes a specification axis. `FIX` = held constant, declared as an
assumption. `ADD` = a branch we do not currently have and should.

| # | Decision | MSCI | Bloomberg | Same? | Us |
|---|---|---|---|---|---|
| 1 | What is being measured | Financially material risk **to the company** | Financially material risk **to the company** | **agree** | `FIX` — and we differ from both. Declare it. |
| 2 | Peer group definition | GICS Sub-Industry, 8-digit | **BECS**, a bespoke ESG classification they built because BICS/GICS didn't fit | **differ** | `VARY` — `peerset` |
| 3 | Size / exposure denominator | Modelled 0–10 exposure score from ~80 segment metrics | Explicit **activity metric** per field: production, employees, revenue as fallback | **differ** | `VARY` — `base` |
| 4 | Raw value → grade | Percentile band vs industry min/max benchmarks | **Rejects percentiles.** Log-log regression residual through a normal CDF | **differ, in print** | `VARY` — `normalizer`, and `ADD` elasticity |
| 5 | Missing data | Absence of evidence scores 0 on *management* | **No imputation.** Drop the field, then cap the Issue Score by a disclosure factor | **differ** | `VARY` — `ADD` the disclosure-cap branch |
| 6 | Aggregation function | Weighted **arithmetic** mean | Weighted **shifted power mean, p = 0.5, s = 1**, at every level | **differ** | `ADD` — `aggregator`. Biggest gap in our model. |
| 7 | Pillar weights | Derived from impact × time horizon; **G floored at 33%** | Ranked 1–5 per industry by analysts; **G fixed at rank 3** | differ in mechanism, agree on ≈⅓ G | `FIX` at four presets + user slider |
| 8 | Relative or absolute | E, S relative; **G absolute** (10 minus deductions) | Mostly relative; **fatalities and binaries absolute** | both break their own rule | `FIX` relative, `ADD` absolute panel |
| 9 | Time window | 3-year controversy lookback, annual review | Parameters averaged over 3 most recent years; a whole field model scores YoY change | **agree on 3 years** | `VARY` — `window`, `direction` |
| 10 | Final discretisation | 0–10 into **7** equal parts, AAA–CCC | 0–10 into **7** bands, A–G | **agree**, neither justifies 7 | `FIX` — we do not discretise. |
| 11 | Human override | Committee overrides, exceptions, truncations | None. Judgement is upstream in parameters only | **differ** | `FIX` — none, like Bloomberg |
| 12 | Controversies / events | Central. Severity matrix, deduction from management | **Absent entirely** | **differ** | `FIX` — absent. Declare as scope. |
| 13 | Non-public data | Refuses it outright | Public only, plus limited regional-average estimation | near-agree | `FIX` — public only |

Seven forks where they differ, six where they agree. **We vary exactly the forks
where they differ.** That sentence is the defence of the whole design.

---

## The forks in detail

### 1. What the score measures — the assumption we must declare first

Both providers measure the **same** thing, and it is not what a layperson thinks
"sustainability" means. MSCI rates resilience to financially relevant ESG risk
and frames externalities by whether they become unanticipated costs *for the
company* (M p.3). Bloomberg defines financial materiality as impact on revenue,
operating costs, cost of capital, asset value, liabilities (B p.8).

This is **single materiality**, outside-in: the world's effect on the company.
Neither rates the company's effect on the world.

Our field set does not do this. Scope 1 GHG, carbon in reserves, spill volume,
freshwater withdrawal, hazardous waste, TRIR — these are **externality**
measures, inside-out. Our F pillar is financial resilience, which is closer to
the providers' frame.

**So we are a hybrid, and we must say so in the first thirty seconds.** The
Citadel brief is genuinely ambiguous ("quantify and compare the sustainability of
companies"), which is itself the point: the brief does not resolve the single
question that determines every downstream choice, and the two incumbents resolved
it the same way without being asked to.

This is a `FIX`, not a `VARY`, for a hard reason: switching materiality direction
changes the *indicator set*, not the arithmetic over a fixed indicator set. A
specification curve varies the method holding the inputs fixed. Two different
indicator sets are two different studies, not two specifications.

### 2. Peer group — Bloomberg built its own classification rather than use the standard one

MSCI sets Key Issues and weights at the GICS Sub-Industry 8-digit level (M p.10).
Bloomberg built **BECS**, a purpose-built ESG classification assembled from
different BICS nodes and levels, precisely because standard industry buckets
group companies that don't share ESG exposure (B p.7).

Bloomberg then goes further and admits the grouping is often unresolvable
empirically: they test whether industries differ statistically, pool them when
they can't show a difference, and where there is inadequate data they defer to
analyst judgement (B p.41).

> A provider with the whole Terminal behind it says the peer group frequently
> cannot be settled from data. Ours is two options. Theirs is a judgement call
> made silently, per industry, by a person.

Directly justifies `peerset` ∈ {sub-group, sector}. Our `MIN_PEERS = 4` fallback
rule is the same species of pragmatic fix as their pooling rule.

### 3. The denominator — Bloomberg names our three options and admits revenue is a fallback

MSCI does not use a denominator at all in the naive sense. Exposure is a modelled
0–10 score built from a granular breakdown of business segments, geography,
outsourced production, government contracts — roughly 80 segment metrics (M pp.2, 6).

Bloomberg does use denominators, calls them **activity metrics**, and states the
principle explicitly: GHG scales with the economics of production, worker training
spend scales with headcount, and where the precise scaling quantity is unavailable
they fall back to revenue (B p.17). Already-normalised fields (percentages, TRIR)
get no activity metric at all.

Two things follow for us:

1. **Our three bases are their three families**, not our invention: production/output,
   headcount, revenue.
2. **Revenue is documented as a fallback, not the right answer.** When we say
   "tonnes per million dollars of revenue is one convention among several," we are
   restating Bloomberg's own caveat.

Bloomberg's design v4 abstraction (apply a divisor for quantities, *select* a
pre-divided variant for rates) matches their treatment exactly: they assign no
activity metric to already-normalised fields.

### 4. The normaliser — the one place the two providers argue with each other on paper

This is the strongest fork we have.

**MSCI** normalises the Weighted Average Key Issue Score against industry peers
using benchmark values. As of November 2020 the top benchmark sits between the
95th and 100th percentile of modelled WAKIS in the rating industry and the bottom
between the 0th and 5th (M p.12). **Before November 2020 the same company was
normalised against a rolling three-year average of the 2.5th and 97.5th
percentiles.** MSCI changed its own normaliser and every score moved. That is a
specification change, documented, by the market leader.

**Bloomberg explicitly rejects percentile bucketing** and publishes a comparison
table listing its drawbacks: it needs most of the peer group to have reported, it
degrades in small peer groups and low-disclosure industries, it obscures trends
over time, and it is sensitive to outliers (B p.41). Instead they fit, per peer
group,

```
log Impact = log Intensity + γ · log Activity + ε
Score      = 10 × [1 − Φ(ε / σ)]
```

and score the **residual** — how far a company sits from the emissions its peer
group's size-elasticity predicts (B pp.45–46). Percentages get a beta CDF,
episodic rates an exponential, fatality rates a gamma with hand-set parameters,
zero-inflated amounts a Tweedie, counts a negative binomial (B pp.47–49).

And the sentence that matters most to us, from B p.46: when the elasticity γ = 1,
the traditional assumption, ranking on intensity is **equivalent** to ranking on
the residual.

> So the entire difference between Bloomberg's headline model and a naive
> intensity ranking is one parameter, γ, that they estimate and everyone else
> assumes. That is a specification axis with a citation.

**What we do.** Keep `normalizer` ∈ {percentile, winsorised min–max, log min–max}
— we can now say percentile is MSCI's family and log min–max is the log-scale
family Bloomberg argues for. **`ADD` a fourth option, `elasticity`:** regress
log(field) on log(base) within the peer set, score `1 − Φ(ε/σ)`. It is Bloomberg's
published model, it is ~15 lines in `spec.py`, and it turns the axis from three
things we thought of into three things we thought of plus the one the market
actually uses.

### 5. Missing data — and a claim of ours that this document does not support

**Correct this before the pitch.** `design-v4-fixes.md` and the web UI both assert
that scoring missing data as worst case is "what MSCI does." **The MSCI executive
summary does not say that.** What it says is that the *management* score runs 0–10
where 0 means no evidence of management efforts (M p.6). That supports "absence of
evidence scores badly on the management axis." It does not document a global
missing-data imputation rule, and if a judge has read the same 17 pages we handed
them, the stronger claim is where we get caught.

Safe wording: *"grading silence as worst-case is the convention behind MSCI's
management score, where zero means no evidence of management effort."* Attribute
the strong version to a source we can produce, or drop it.

**Bloomberg is explicit and does something more interesting.** They state a
no-imputation principle: scores reflect self-reported public information or its
absence, because imputing would remove the incentive to disclose (B p.24). A field
a company does not report is simply ignored at the Sub-Issue level and the weights
redistribute (B p.23) — that is exactly our `exclude`.

But disclosure comes back as a **separate multiplicative cap**. Every field carries
a Disclosure Factor point value (A = 5, A− = 1.25, B = 2, B− = 0.5, C = 0), the
Issue DF is points earned over points available, and the Issue Score is capped at

```
UT = 3 + √DF × 7
```

so a company disclosing no quantitative data cannot exceed 3 out of 10 no matter
how good its policies look (B pp.24–26). There is also a floor that rewards
disclosing a bad number over disclosing nothing.

**What we do.** Our missing-data switch has two states. Bloomberg's is a third,
and it is the best of the three:

| Branch | Rule | Provenance |
|---|---|---|
| `exclude` | field drops out of the pillar mean | Bloomberg sub-issue aggregation, B p.23 |
| `worst` | field enters as grade 0 | the strict reading; attribute carefully |
| `cap` **(add)** | drop from the mean, then scale the pillar by `(3 + √coverage × 7) / 10` | Bloomberg Issue Score, B p.26 |

`cap` costs about five lines and it resolves a real tension in our own design. The
v4 note argued missing should be neutral because coverage is reported separately
and one fact belongs in one place. Bloomberg's answer is better: keep performance
and disclosure separate all the way up, then combine them with a **stated, visible
formula** instead of either double-counting or ignoring. We should say we adopted
their resolution.

### 6. Aggregation — the biggest hole in our model

MSCI takes a weighted **arithmetic** mean of Key Issue scores to get WAKIS (M p.10).

Bloomberg uses a weighted **shifted power mean** at every level of the hierarchy —
sub-issue to issue, issue to pillar, pillar to overall ESG:

```
M(x, w, p, s) = ( Σ wⱼ (xⱼ + s)^p )^(1/p) − s      with p = 0.5, s = 1
```

Their stated reason is that a power mean rewards consistency and penalises uneven
performance, and that E, S and G cannot compensate for one another (B pp.25, 32).
Their footnote concedes p = 0.5 is simply the midpoint between the arithmetic mean
(p = 1) and the geometric mean (p = 0), and s = 1 avoids large penalties near zero.

This matters more than it looks. It is the **compensability** question: can a
company's excellent governance offset its terrible emissions? Arithmetic mean says
yes, fully and linearly. Geometric mean says barely. Bloomberg picked a number
halfway between and admits that's what they did.

We currently use the arithmetic mean everywhere and never vary it. That means:

- we silently take MSCI's side of a live disagreement, and
- we omit the axis with the clearest ethical content in the whole model.

**`ADD` `aggregator` ∈ {arithmetic (p = 1, MSCI), pmean (p = 0.5, s = 1, Bloomberg),
geometric (p → 0)}.**

Cost: near zero. Both `aggregator` and the missing-data rule act at **step 6**,
downstream of the grade tensor — so the export does not change at all and the
browser computes them for free. `spec.composite()` gains one parameter.

### 7. Pillar weights — neither provider lets the user touch them

MSCI derives Key Issue weights from contribution to externality (High/Medium/Low)
crossed with time horizon (Short <2y / Long 5y+); a High-impact short-term issue
weighs three times a Low-impact long-term one. Each Key Issue lands between 5% and
30%, and since November 2020 the Governance pillar is **floored at 33%** (M p.5).

Bloomberg ranks E and S 1–5 per industry from analyst research, fixes **G at rank 3
for every industry** because governance is driven more by market and region than by
sector, then converts ranks to percentages. Published examples: Tobacco is
11.1 / 55.6 / 33.3 E/S/G; Oil & Gas E&P is 45.5% E and 27.3% S (B p.32). Issue-level
weights come from `w̃ = 1 + e^(0.5(3−k))` on the priority rank k — deliberately
non-linear so top-ranked issues dominate (B p.28).

Two observations worth a slide:

1. **Both effectively pin governance at about one third**, by two unrelated
   mechanisms. That is either convergent wisdom or convergent convention, and
   neither document argues for the number.
2. **Neither provider exposes the weights to the user.** You get the industry's
   vector or nothing. Our slider is not a gimmick relative to the market — it is a
   capability neither incumbent ships.

This is why the weights stay presets-plus-slider rather than a specification axis,
and it is now empirically as well as theoretically justified: Berg, Kölbel &
Rigobon put weights at 13.2% of divergence, and both providers treat the weight
vector as fixed per industry, so varying it does not reproduce anything either
provider actually does.

### 8. Relative versus absolute — both providers break their own rule, in different places

MSCI is emphatic that ratings are relative to industry peers and not absolute
(M pp.4, 12) — and then scores the **Governance pillar absolutely**, starting every
company at a perfect 10 and applying deductions (M p.9).

Bloomberg is best-in-class relative — and scores **fatalities against one universal
standard regardless of industry or size**, on the reasoning that a human life has
the same value everywhere (B p.42). Binary policy fields are absolute by nature.

Then Bloomberg names the failure mode themselves: if every participant in an
industry pollutes heavily, the best relative performer still scores well (B p.42).

This is the strongest external support for the two-panel output argued in
`critique-weights.md` §4: publish the **rank distribution** and the **absolute
intensity against a peer median** side by side. Bloomberg diagnoses the disease in
its own methodology document and does not treat it. We should, and we should quote
them diagnosing it.

### 9, 10, 11, 12, 13 — the short ones

**Window and direction.** Both use three years somewhere: MSCI's controversy
lookback (M p.6), Bloomberg averaging parameters over the three most recent years
(B p.46). Bloomberg has an entire field model, Rate-Anchored, that scores
year-over-year percent change with the anchor at roughly zero change (B p.18). Our
`window` ∈ {latest, mean3} and `direction` ∈ {level, change} are both conventional
and both contested. Keep.

**Discretisation.** MSCI cuts 0–10 into seven equal parts for AAA–CCC (M p.12).
Bloomberg cuts its standardised score into seven bands A–G (B p.33). Two
independent teams both chose seven and neither says why. We do not discretise at
all, and that is a deliberate choice: bucketing destroys precisely the resolution
our contestation figure is made of. Worth one line on the slide.

**Human override.** MSCI factors in committee-level overrides before the final
industry-adjusted score and requires committee approval for exceptions,
truncations and rating changes of two notches or more (M pp.4, 14). Bloomberg does
not incorporate analyst opinion in assigning or adjusting scores (B p.11) —
judgement enters upstream, in priorities, fit/quality, and thresholds.

We are Bloomberg-shaped. This is not just a preference: **you cannot enumerate a
committee.** A specification curve requires the method to be a function of the
data. MSCI's model, as documented, is not one. That is a legitimate and quite
sharp thing to say out loud.

**Controversies.** A whole scoring component present in MSCI (severity matrix over
scale × nature of impact, three-year lookback, deduction from the management score,
M pp.6–9) and entirely absent from Bloomberg. And absent from ours. This is a
textbook **scope** difference — the 36.7% bucket in Berg et al. — and we declare it
as a boundary rather than pretend to cover it.

**Data sources.** MSCI takes company disclosure, 3,400+ media sources, and
government/NGO/academic datasets, naming the **US EPA** among them (M pp.2, 13),
and refuses non-public issuer data outright. Bloomberg uses public company-reported
data and, in limited cases, regional averages where a company has not reported
(B p.11).

Useful for the feasibility criterion: **the EPA GHGRP layer in `contested/` is a
source MSCI itself lists.** And our modelled EEIO layer has the same status as
Bloomberg's regional-average estimation — a screening substitute where disclosure
is absent, which one of the two providers already does in production.

---

## What changes in the model

Everything below is downstream of the grade tensor except the elasticity
normaliser, so the web explorer gets most of it for free.

| Change | Where | Effect on spec count | Cost |
|---|---|---|---|
| `aggregator` ∈ {arithmetic, pmean 0.5, geometric} | `spec.composite()`, step 6 | ×3 | one parameter, no export change |
| missing rule gains `cap` | `spec.composite()`, step 6 | ×3 (from ×2 as a switch) | ~5 lines, no export change |
| `normalizer` gains `elasticity` | `spec.grade()`, step 5 | 3 → 4 options | ~15 lines, export regenerates |

Current grid is 3 × 2 × 2 × 3 × 2 = **72**. With the elasticity normaliser it is
**96**. Multiply by 3 aggregators and 3 missing-data rules and the browser explores
**864** specifications per weighting — every one of which we can name a provider for.

Do the two step-6 additions first. They are nearly free, they close the most
embarrassing gap (we had silently adopted MSCI's arithmetic mean), and the
`aggregator` axis is the best demo in the set: drag nothing, just switch
"can good governance offset bad emissions" from *yes* to *no*, and watch the table
turn over.

## What to say on stage

Three sentences, in this order:

1. **"We did not invent our uncertainty axes. We read MSCI's and Bloomberg's
   methodologies and varied the seven things they do differently."**
2. **"Bloomberg publishes a table explaining why MSCI's percentile approach is
   wrong. MSCI changed its own normaliser in November 2020. Both of them cap
   governance at a third of the score by two completely different arguments.
   Nobody reports what that costs you."**
3. **"Where they agree, we fixed the choice and wrote down the assumption. That
   list is on the slide too."**

## Corrections to make in the repo

- [ ] `design-v4-fixes.md` §1: soften the MSCI missing-data claim to what M p.6
      actually supports, or cite a different MSCI source.
- [ ] `web/index.html`, missing-data control note: same wording fix.
- [ ] `sustainability-definition.md`: add the single-vs-double materiality
      declaration from §1 above. It is currently the largest undeclared assumption
      in the framework.
- [ ] `framework.md`: cite B p.41 for the peer-group axis and B p.46 for the
      normaliser axis. They are free credibility.

## Related

- [[Efforts/Active/ETHack/critique-weights|critique-weights]] — §4 (two panels) and §5 (slider as second view) are both now backed by provider documents.
- [[Efforts/Active/ETHack/design-v4-fixes|design-v4-fixes]] — the exposure-base abstraction matches Bloomberg's activity-metric rule exactly.
- [[Efforts/Active/ETHack/aggregate-confusion|aggregate-confusion]] — Berg, Kölbel & Rigobon's scope/measurement/weights split is the frame this note fills in with specifics.
- [[Efforts/Active/ETHack/framework|framework]] — the axes this note defends.
