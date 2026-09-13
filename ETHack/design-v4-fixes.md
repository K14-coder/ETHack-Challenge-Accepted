---
edit: owned
last_edited: 2026-09-12T18:00:58 CET
changes: 0
type: project-note
status: proposed
---
# Design v4: the two fixes, and the hidden weighting they also solve

Two problems to solve: booleans have no magnitude, and rates cannot take a denominator. Both fixes turn out to be the same move, and applying it removes a third problem nobody had noticed.

## 0. The problem nobody had noticed

In v3 each field type produced a different number of specifications: Q and R gave 18, S gave 9, P and B gave 6.

That is **an implicit weighting by measurement type.** When field distributions roll up to sub-issue and pillar, a quantity field contributes three times as many observations as a policy field. So the pillar distribution is silently weighted 3:1 toward whichever fields happen to be physical quantities.

We claim our whole contribution is refusing to hide weights. An unequal spec count per type is a hidden weight.

**So the design target is not "make booleans work". It is: every field type must yield exactly the same number of specifications.** Fix that and the roll-up is unweighted by construction.

**Target: 18 specifications per field, every type.**

## 1. Fix one: the boolean becomes a signed tally

### The operation

For a boolean field `f` with reported value `v`:

```
ι(f,v) =  +1   if v is the favourable state
          -1   if v is the unfavourable state
           0   if v is missing

b(f)   = ι(f,v)
```

For a set `S` of boolean fields at a given stringency level:

```
B_score(S) = ( Σ_{f ∈ S} b(f) ) / |S|        ∈ [-1, +1]
```

### Why it is legitimate, not a hack

1. **It is ordinal and unit-free.** A signed sum of ±1 needs no denominator, which is exactly the objection to booleans. The division by `|S|` is not a normalisation by an external quantity, it is an average of a bounded variable.
2. **It has a meaningful zero.** `0` means as many favourable as unfavourable. That is a real interpretive anchor, unlike a raw count of policies where zero just means "no data".
3. **`|S|` is the size of the peer-group expected set, not the number the company reported.** So a company that reports nothing scores `0/|S| = 0`. It sits below a company at `+0.5` and above one at `−0.5`.

### Why missing should score 0 rather than −1

MSCI's rule is that missing data is scored as worst case. Ours is that it scores neutral, and the justification is structural rather than generous:

**We publish the coverage count separately and visibly.** A company reporting 4 of 18 expected booleans carries a coverage flag saying so. If the score *also* punished the absence, the same fact would be counted twice: once in the score, once in the coverage statistic. **One fact, one place.**

Scoring missing as −1 is a defensible alternative, and we say so in the paper. It belongs in the sign dimension below, not silently in the tally.

### The third dimension: sign convention

Many booleans have a contested direction. `CEO Duality = Y` is a governance failure to a governance purist and neutral to someone who values unified leadership. `Arctic Drilling = Y` is a liability to one reader and a reserve base to another.

| Convention | Contested booleans score |
|---|---|
| **strict** | the sustainability-negative reading (−1) |
| **neutral** | 0. Only unambiguous fields carry a sign |
| **charitable** | the company's own framing (+1 where it presents the item as a control) |

This is a real disagreement, and it is the entire substance of the governance-rating argument. Running all three is the honest response to it.

**Booleans: stringency (3) × persistence (2) × sign convention (3) = 18.** ✓

## 2. Fix two: one abstract dimension, two instantiations

### The insight

Q and R are answering the same question. **"Per what unit of exposure?"**

For a quantity, you choose a denominator and apply it. For a rate, the reporter has already divided, and your choice is **which population's divisor they used.**

So define one dimension, **exposure base**, with a type-specific operator:

```
B(x, base) =   x / d(base)        if τ(f) = Q     APPLY the divisor
               x_base             if τ(f) = R     SELECT the pre-divided variant
```

| Type | base = 1 | base = 2 | base = 3 |
|---|---|---|---|
| **Q** | ÷ revenue | ÷ physical output (boe produced) | ÷ employees |
| **R** | per employee-hours | per contractor-hours | per total-workforce-hours |

**No double normalisation, because for R the operator selects rather than divides.** The divisor is applied exactly once in both branches. Formally: `B` has the same signature for every type and a type-specific implementation. An interface with per-type instances, which is the same pattern as a typeclass.

### Why this is the right abstraction and not a dodge

Bloomberg **already reports the three population variants** of TRIR, LTIR and fatality rate as separate field IDs. The three cells exist in the data. We are not inventing a divisor, we are selecting among divisors the reporter already chose and published.

And the two instantiations are semantically the same operation: both produce *harm per unit of exposure to harm*. For a quantity, exposure is measured in dollars or barrels or headcount. For a rate, exposure is measured in hours worked by a defined population.

## 3. Bringing every type to 18

| Type | Dimensions | Count |
|---|---|---|
| **Q** quantity | exposure base (3) × window (3) × direction (2) | **18** |
| **R** rate | exposure base (3) × window (3) × direction (2) | **18** |
| **P** percentage | window (3) × direction (2) × **reference (3)** | **18** |
| **B** boolean | stringency (3) × persistence (2) × **sign convention (3)** | **18** |
| **S** structural | reference (3) × window (3) × **polarity (2)** | **18** |

Two dimensions were added to close the gap. Both are real choices, not padding.

### Reference, added to P (and already in S)

A percentage carries no meaning without a comparison. Exxon recycled **16.67%** of hazardous waste in 2025, down from 33.33% in 2023. Is 16.67% good? Unanswerable in isolation.

- **absolute** — the raw 16.67%
- **peer median gap** — distance from the Integrated Oils median
- **frontier gap** — distance from the best performer in the peer group

The three give different rankings whenever the peer distribution is skewed, which for this field it certainly is.

### Polarity, added to S

For many governance counts the direction of "better" is genuinely contested in the literature, not just in politics.

- **governance-orthodox** — independence good, long tenure bad, refreshment good, CEO duality bad
- **stability-orthodox** — experience good, continuity good, churn bad, unified leadership decisive

Exxon: board size 13, independent directors 12, chairperson tenure **9 years**, CEO duality **Y**, independent chairperson **N**. Under governance-orthodox the 9-year chair and the duality are failures. Under stability-orthodox the tenure is accumulated expertise.

**This is also how we handle the ideology problem without asserting a view.** We do not claim one polarity is correct. We run both and report that the answer depends on which you hold. That is a stronger and more honest position than picking a side, and it is the same move the whole framework makes everywhere else.

## 4. The resulting arithmetic

```
135 usable fields × 18 specifications = 2,430 spec-field combinations per company
```

Every field type contributes 18. Every field contributes equally to its sub-issue. Every sub-issue contributes equally to its issue, because Bloomberg's tree defines the membership. **No weight anywhere is ours.**

| Companies | Observations |
|---|---|
| 12 | 29,160 |
| 15 | 36,450 |
| 20 | 48,600 |

Compute is irrelevant at any of these.

## 5. Which companies to request, and why

### First, do not let me guess the peer set

**Export Bloomberg's own `Integrated Oils` peer group membership.** One screen. Three obvious names were acquired inside the 2021-2025 window and would appear as companies that stopped existing mid-sample:

- **Pioneer Natural Resources** — acquired by Exxon, 2024
- **Hess** — acquired by Chevron
- **Marathon Oil** — acquired by ConocoPhillips, 2024

Using Bloomberg's definition also removes one more thing for us to have chosen. The peer group, the field set, the materiality judgment and the aggregation tree then all come from Bloomberg, and the only thing we choose is the dimension set per measurement type.

### Second, take the true peer group even if it is under 20

**Recommendation: whatever Bloomberg's Integrated Oils group contains, even if it is 12 to 15 names. Do not pad to 20.**

Padding to 20 means adding pure exploration-and-production companies and pure refiners. Those are **different sub-industries with different materiality maps.** EOG has no refining fields; Valero has no reserves or Arctic drilling fields. The moment the field sets differ, the "constant field set" argument that makes intra-industry comparison valid is gone, and that argument is our strongest defence.

**12 companies with an identical field set beats 20 with three different ones.** 29,160 observations is plenty.

### If Bloomberg's group is small, here is the priority order

Ranked by what each adds to the *design*, not by size.

| Priority | Ticker | Why it earns a slot |
|---|---|---|
| 1 | **XOM** | already have it. The reference case. |
| 2 | **CVX** | closest US peer. Isolates company effects from jurisdiction effects. |
| 3 | **SHEL** | European supermajor, under CSRD. Tests whether mandatory disclosure lifts coverage. |
| 4 | **BP** | European, and the one with a publicly reversed transition strategy. Direction dimension should light up. |
| 5 | **TTE** | European, heavy renewables capex. Tests the reserves-versus-operations divergence in the other direction. |
| 6 | **COP** | US, upstream-weighted. Reserve-heavy, so embedded carbon dominates. |
| 7 | **EQNR** | state-influenced, best-disclosing major. Likely the coverage frontier. Sets the benchmark for what is reportable. |
| 8 | **ENI** | European, and it reports produced-water fields Exxon leaves blank. Directly tests the non-disclosure finding. |
| 9 | **OXY** | US, carbon-capture positioned. The "clean-oil" claim tested against the boolean tally. |
| 10 | **SU** or **CNQ** | Canadian oil sands. Highest carbon intensity per barrel in the peer group. The upper bound. |
| 11 | **PBR** | emerging-market supermajor. Tests whether the framework survives a weaker disclosure regime. |
| 12 | **IMO** or **OMV** | fills the group. |

**EQNR and ENI are the two I would fight for after Chevron.** Equinor because it probably marks the disclosure frontier, which tells us what "fully reported" even looks like and makes every gap elsewhere measurable rather than merely absent. Eni because it populates the produced-water fields Exxon leaves empty, which converts our non-disclosure claim from an assertion into a comparison.

## 6. Export settings — get these identical or nothing joins

### The currency bug, and it is a real one

Row 3 of the Exxon export reads **`Currency: LCL`**, meaning local currency.

Export Shell, BP, Eni or Equinor on that setting and the currency fields come back in **GBP, EUR and NOK.** Environmental fines, CEO pay and revenue would then be in four different currencies with no conversion, and every financial denominator silently breaks.

**Set currency to USD on every export.** Check row 3 of each file says USD before you send it.

### Everything else that must match

- **Same peer group** stamped on row 2 for every company. If Bloomberg assigns a different peer group to Equinor, the field set changes and that file cannot be used in the same grid.
- **Same five fiscal years**, 2021 to 2025, actual reported.
- **Same two sheets**, ES Materiality and G Materiality.
- **Same field template.** Export one, then reuse the template rather than rebuilding the screen per company.

### Two extra fields the materiality map does not contain

The exposure-base dimension needs denominators that are not in these sheets:

1. **Revenue** for each company, FY2021-2025, in USD.
2. **Production in barrels of oil equivalent per day or per year**, FY2021-2025. This is the physical denominator and the single most valuable thing you can add, because it is what makes intra-industry comparison better than cross-industry comparison.
3. **Employee headcount**, FY2021-2025, for the third base.

If production is hard to get, say so early. Without it the exposure-base dimension drops from 3 to 2 and every type falls from 18 specs to 12, which still balances, but we lose the industry-native denominator that is the whole argument for working inside one industry.

## 7. What to send me, in order

1. **Bloomberg's `Integrated Oils` peer group membership list.** Before anything else.
2. **One more materiality map**, Chevron, exported with **USD** currency, so I can verify the field IDs line up across companies before you export ten more.
3. Then the rest of the peer group, same template.
4. **Revenue, production (boe) and headcount** for all of them, FY2021-2025, USD.

Step 2 matters more than it looks. If Chevron's export has different field IDs or a different peer-group stamp, we find out after one export instead of after twelve.

## Related

[[Efforts/Active/ETHack/design-v3-full-materiality|design-v3-full-materiality]] · [[Efforts/Active/ETHack/framework|framework]] · [[Efforts/Active/ETHack/how-many-specs|how-many-specs]]
