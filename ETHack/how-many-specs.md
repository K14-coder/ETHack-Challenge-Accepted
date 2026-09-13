---
edit: owned
last_edited: 2026-09-12T13:36:41 CET
changes: 0
type: project-note
status: decided
---
# How many specifications, and how to measure the spread

## The framing that matters

This is **not a sampling problem.** A full factorial enumeration of the choice space *is* the population of that space. There is no sampling error on contestation. We compute it exactly.

What is a modelling choice is the choice space itself. So the real questions are narrower:

1. How many specifications to attribute the spread to each dimension?
2. Is our spread statistic well supported by that many order statistics?

## Answer 1: the floor is 7

Degrees of freedom for main effects across our four dimensions (3 boundary, 2 denominator, 3 missing-data, 2 peer group):

`1 + 2 + 1 + 2 + 1 = 7`

**Seven specifications is the mathematical floor** to say "this much of the spread comes from boundary choice, this much from the denominator". A fractional factorial at n=7 gets main effects and nothing else.

**36 is the full factorial**: every main effect plus every interaction. Interactions are not decorative here. "Widening the boundary matters more for a company that discloses nothing" *is* an interaction between boundary and missing-data rule, and it is exactly the Walmart story.

So: 7 to attribute, 36 to attribute honestly.

## Answer 2: P10/P90 is too thin at n=36

Where the percentiles actually land:

| n | P10 sits at | P25 sits at | mass per spec |
|---|---|---|---|
| 9 | value 1.8 | value 3.0 | 11.1% |
| 18 | value 2.7 | value 5.2 | 5.6% |
| **36** | **value 4.5** | **value 9.8** | **2.8%** |
| **72** | **value 8.1** | **value 18.8** | **1.4%** |
| 144 | value 15.3 | value 36.8 | 0.7% |

At n=36, P10 falls between the 4th and 5th value. One unusual specification moves it. At n=72 it falls between the 8th and 9th, which is stable.

## Decisions

1. **Run 72 specifications**, i.e. add consolidation approach as the fifth dimension. It is justified on content grounds anyway: the GHG Protocol defines operational-control and equity-share consolidation as distinct, EPA publishes the ownership percentages, and on Nucor alone it moves the total 4.59% (see [[Efforts/Active/ETHack/proof-nucor|proof-nucor]]). The statistics are a bonus.
2. **Report contestation as the interquartile range, P25 to P75.** Well supported at n=36 and comfortable at 72.
3. **Report the full range (min to max) as the secondary figure.** It is the headline-friendly number: "this company moved N places across every defensible method".
4. **Never quote P10/P90 at n=36.** If we end up cut back to 36, contestation is the IQR, full stop.

## The stronger move, if there is time

Because the design is a full factorial, the spread can be **decomposed by dimension**: what share of rank variance comes from boundary, from denominator, from missing-data rule, from peer group, from consolidation.

That produces our own version of the Berg/Kölbel/Rigobon table (scope 36.7%, measurement 50.1%, weight 13.2%), computed on the S&P 500 from free data. Not a citation of their result. A replication of their method on new data.

This is the single highest-value optional output. It requires the full factorial, which is the real argument for running all 72 rather than sampling.

## How many companies

The S&P 500 is a population, not a sample, so there is no sampling error on the ranking itself. The constraint is only on **sector-level** claims:

- ~45 companies per GICS sector on average
- the thin ones are real: Energy ~23, Materials ~28, Utilities ~31, Real Estate ~31

A within-sector median is worth quoting at roughly 20+ members. Below that, report it and state n.

## Related

[[Efforts/Active/ETHack/framework|framework]] · [[Efforts/Active/ETHack/proof-nucor|proof-nucor]]
