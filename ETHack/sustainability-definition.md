---
edit: owned
last_edited: 2026-09-12T11:28:03 CET
changes: 0
type: project-note
status: draft
---
# What we mean by sustainability

The challenge says: *define what sustainability means, identify and justify the most relevant indicators*. This file is that answer. Everything the code computes traces back to a line in here, and every number in the deck traces back to this file.

Written as a position we defend, not a survey of options.

## 1. The definition

> **A company is sustainable to the degree that the economic activity it is responsible for causes little environmental damage, relative to the economic value it produces.**

Three deliberate commitments inside that sentence.

**Present tense.** We measure what is happening now, not pledges, targets or trajectories. A 2050 net-zero commitment is a press release until it shows up in the numbers. We are scoring behaviour, not intention.

**"Responsible for", not "emitted by".** A company that stops making a thing itself and buys it from a supplier has not reduced any damage. It has moved it off its own books. Where we draw this line is the central question of the whole project, see section 3.

**Relative to value produced.** Walmart emits more than a small software firm by being enormous. Without a denominator the ranking is just a list of large companies.

## 2. Why environmental only, and not the S and the G

We deliberately score **E** and leave out social and governance. This is a narrowing, and we defend it rather than apologise for it.

Environmental damage has physical units. Tonnes of CO2 equivalent, cubic metres of water, tonnes of hazardous waste. Two honest analysts measuring the same company's emissions with the same boundary get close to the same number.

Social and governance have no physical units. "Labour practices" gets measured as staff turnover by one rating agency and as lawsuit counts by another. That is not a small difference in emphasis, it is a different variable wearing the same label.

This matters because **measurement divergence is 50.1% of why the world's ESG rating agencies disagree with each other** ([[Efforts/Active/ETHack/aggregate-confusion|aggregate-confusion]]). By restricting ourselves to quantities with agreed physical definitions, we are removing the single largest source of noise in ESG scoring by construction, not by cleverness.

The cost: our score says nothing about a company that treats its workers badly. We state that plainly rather than hiding it.

## 3. The boundary ladder

The core of the project. "Damage the company is responsible for" is not one number, it is a choice, and almost nobody states which choice they made.

The GHG Protocol already gives the vocabulary.

| Boundary | Includes | In plain words |
|---|---|---|
| **A** | Scope 1 | What the company burns itself. Its own furnaces, boilers, vehicles. |
| **B** | Scope 1 + 2 | Plus the electricity, heat and steam it buys. |
| **C** | Scope 1 + 2 + 3 | Plus its supply chain upstream and its products being used downstream. Cars being driven, fuel being burned, cement being poured. |

We compute the full score **three times**, once at each boundary, and publish all three rankings.

**The output is not a ranking. It is the movement between rankings.**

- A company that holds its position across A, B and C is genuinely clean.
- A company that ranks near the top under A and collapses under C has not reduced damage. It has relocated it past the reporting boundary.

We call that movement **boundary sensitivity**, and it is our headline variable.

### Why this is the right thing to measure

**Scope divergence is 36.7%** of ESG rating disagreement. It is the second largest cause and the one almost never made visible to the person reading the score. We are not discovering a new problem. We are taking a known, published, quantified problem and showing what it does to the most-watched equity index in the world.

## 4. The denominator

Damage per unit of what, exactly. This is also a choice and we treat it as one.

| Denominator | Case for | Case against |
|---|---|---|
| **Revenue** (primary) | universally available, audited, intuitive | inflated for low-margin pass-through businesses; a commodity trader looks efficient purely by booking huge revenue |
| **Enterprise Value Including Cash, EVIC** (robustness check) | what PCAF and EU regulation use for financed emissions, so it is the regulator's choice not ours | moves with the stock price, so a company gets greener in a bull market |

We lead with revenue and re-run on EVIC as a robustness check.

### Why we run both

Changing the denominator while holding the boundary fixed is **measurement divergence**, the 50.1% cause. Changing the boundary while holding the denominator fixed is **scope divergence**, the 36.7% cause.

So the project is not a loose analogy to the paper. It reproduces its two dominant causes, deliberately and separately, on the S&P 500, using only free data.

And we explicitly **refuse to argue about weights**, which is the 13.2% cause and the thing every other team in the room will spend their day on.

## 5. Indicators

Small on purpose. Every indicator we cannot defend individually is a liability in Q&A.

**Core, in the scored model**

| Indicator | Unit | Why it is in |
|---|---|---|
| GHG emissions, Scope 1 | tCO2e | the only environmental quantity with broad, standardised, comparable corporate reporting |
| GHG emissions, Scope 2 | tCO2e | same standard; separates operational burn from purchased energy |
| GHG emissions, Scope 3 | tCO2e | usually the largest share and the one that reveals boundary games |
| Revenue | USD | denominator |
| EVIC | USD | robustness denominator |
| GICS sector | category | for the within-sector view, section 7 |

**Considered and left out, with reasons**

- *Water withdrawal.* Only meaningful weighted by local water stress, and the location data needed to do that is not obtainable in 24 hours. Including it unweighted would be worse than excluding it.
- *Hazardous waste and toxic releases.* US EPA data exists and is good, but it is facility-level and US-only, so it would silently penalise companies with more of their footprint inside the US.
- *Biodiversity and land use.* No comparable cross-company dataset exists. Any number here would be invented.
- *Renewable energy share.* Already captured inside Scope 2. Adding it double-counts.

Saying why something is out is worth as much as saying why something is in. The rubric explicitly rewards being honest about limitations.

## 6. Missing data is a finding, not an inconvenience

A large share of the S&P 500 does not report Scope 3 at all. There are three ways to handle that and two of them are lies.

- **Drop the company.** Lie by omission. The worst disclosers vanish from the ranking, so non-disclosure becomes a way to avoid being scored.
- **Treat missing as zero.** Lie outright. Rewards silence.
- **Estimate it, and flag it.** Honest. Estimate from sector-average intensity, mark the value as estimated, and publish the ranking twice: disclosed-only, and disclosed-plus-estimated.

We do the third.

**Disclosure coverage is itself a headline number.** "X% of the S&P 500 does not tell you the part of its footprint that is usually the largest" is a finding worth thirty seconds of a three-minute pitch.

## 7. Across sectors, or within them

Two different questions, and we must not blur them.

- **Across sectors.** Answers "where in this index does environmental damage actually happen". An oil company will lose to a software company and that is correct, not a bug. This is the primary view, because our definition is about damage caused, not about relative virtue.
- **Within sector.** Answers "who is the best operator in their industry". Useful to an allocator who has to hold energy exposure regardless.

We publish across-sector as the primary and within-sector as a secondary view. We never silently mix them.

## 8. What this score cannot tell you

Stated in the deck, out loud, before anyone asks.

1. **No trajectory.** A company halving its emissions and a company doubling them look identical if they pass each other today.
2. **No avoided emissions.** A wind turbine manufacturer has a real footprint. Its product displaces far more than it creates. Our score cannot see that, and it is the single biggest conceptual gap in a present-damage definition.
3. **Scope 3 double-counts across the index.** One company's downstream is another's upstream. Summing Scope 3 across all 500 counts the same molecule many times over. Our per-company numbers are valid; an index total would not be.
4. **Most of this data is self-reported and unaudited.** We inherit whatever the companies chose to tell us.
5. **No social or governance dimension.** By design, section 2.
6. **Estimated values carry real uncertainty.** Flagged, never hidden.

## 9. How the bonus question falls out

*Tomorrow the world commits to net zero as fast as possible. You run a $1 billion fund.*

Our framework does not answer this on its own, and we say so. A present-damage score plus one extra assumption does.

The bridge: **boundary sensitivity is a risk measure.** A company that looks clean at boundary A and collapses at boundary C is carrying environmental exposure that its own disclosure does not show. Under an abrupt net-zero commitment, that hidden exposure is exactly what gets repriced first.

So the allocation logic is:

1. Overweight the boundary-robust clean. Clean under every definition, so nothing surfaces when the boundary is redrawn by regulation.
2. Underweight or exclude the high-churn names. They look fine today only because of where the line currently sits.
3. Treat non-disclosure as risk, not as neutral.

And we name what we would need to do it properly: a carbon price path, a repricing horizon, and a sector-level demand model. We do not pretend a 24-hour project produced those.

## Open decisions

- [ ] Confirmed: does "damage" include Scope 3 (boundary C)? Everything above assumes yes.
- [ ] Revenue year and currency handling for non-USD reporters.
- [ ] Estimation method for missing Scope 3: sector-median intensity, or something better if the data allows.
- [ ] Exact GICS level for the within-sector view: sector, industry group, or industry.

## Related

- [[Efforts/Active/ETHack/challenge|challenge]] — the brief and the rubric this answers.
- [[Efforts/Active/ETHack/aggregate-confusion|aggregate-confusion]] — the divergence decomposition this method is built on.
- [[Efforts/Active/ETHack/idea|idea]] — scope, stack, risks.
