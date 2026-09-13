---
edit: owned
last_edited: 2026-09-12T12:10:52 CET
changes: 0
type: project-note
status: proposed
---
# The framework

Aram's call: build something that **acknowledges the biases of ESG scoring instead of pretending to be free of them.**

This file turns that into a computable design. Read [[Efforts/Active/ETHack/sustainability-definition|sustainability-definition]] first for what we measure, and [[Efforts/Active/ETHack/aggregate-confusion|aggregate-confusion]] for why.

## The thesis, one sentence

> **There is no ESG score. There is a distribution of defensible scores, and the width of that distribution is the most useful number nobody reports.**

## The method has a name, and it is not ours

We are not inventing a technique. We are importing one.

**Specification curve analysis.** Simonsohn, Simmons and Nelson, *Nature Human Behaviour* 4, 2020. Built for a different crisis: in psychology and economics, a researcher faces dozens of defensible analytic choices, and by picking among them can reach almost any conclusion while every individual step stays justifiable. The published standard error hides that. Related work: multiverse analysis, Steegen, Tuerlinckx, Gelman and Vanpaemel, 2016.

Their fix, in three steps:

1. Enumerate every reasonable specification instead of choosing one.
2. Run all of them and plot the results, with a dashboard showing which choices produced which result.
3. Reason about the distribution, not about any single run.

**ESG rating has exactly the same disease and has never been given this treatment.** Berg, Kölbel and Rigobon proved the symptom, that raters disagree at 0.61. Specification curve analysis is the established cure for that class of problem. Nobody has connected the two on the S&P 500.

That connection is our submission.

## Step 1: Enumerate the choices

Each of these is a real decision a real rating agency makes, defensible, and invisible to whoever reads the final number.

| Dimension | Options | What it reproduces |
|---|---|---|
| **Emissions boundary** | Scope 1 · Scope 1+2 · Scope 1+2+3 | **scope divergence**, 36.7% of rater disagreement |
| **Denominator** | revenue · enterprise value including cash | **measurement divergence**, 50.1% |
| **Missing-data rule** | exclude · worst-case (what MSCI does) · sector-median estimate | the choice nobody discloses |
| **Peer group** | absolute · within GICS sector | MSCI is peer-relative, Sustainalytics claims absolute |

3 × 2 × 3 × 2 = **36 complete, defensible frameworks.**

Every one of them is in use by somebody real. None is objectively correct. That is the whole point.

## Step 2: Run all 36

Each specification produces a full ranking of the S&P 500. 36 × 500 = 18,000 company-scores. The compute is nothing. The data is the work.

## Step 3: Two numbers per company

Replace the single score with a pair.

| Metric | Definition | Reads as |
|---|---|---|
| **Consensus rank** | median rank across all 36 specifications | where the company sits when no single methodology gets to decide |
| **Contestation** | spread of that rank, P90 minus P10 | how much of its reputation is an artifact of methodology |

**Low contestation, good consensus rank** → robustly clean. Act on it.
**Low contestation, bad consensus rank** → robustly dirty. No hiding place.
**High contestation, anywhere** → the number is meaningless. Anyone quoting a single ESG score for this company is quoting a choice, not a fact.

## Step 4: The chart

Two visuals, and we only need the first to work.

**Primary, the specification curve.** Take one well-known company. Plot its rank across all 36 specifications, sorted. Below it, the dashboard panel: which boundary, which denominator, which missing-data rule produced each point. This is the exact published visual form of the method, so the academics on the panel will recognise it in under two seconds.

Pick a company whose curve is violent. A large bank or a consumer brand will swing hardest between boundary A and C.

**Secondary, the map.** All 500 as a scatter. Consensus rank on the x axis, contestation on the y. The high-contestation band across the top is where every ESG argument in the world actually takes place.

## Step 5: The bonus question falls straight out

*Tomorrow the world commits to net zero. You run a $1 billion fund.*

**Contestation is specification risk, and specification risk is priceable.** A company whose rank swings 300 places depending on an accounting convention is one regulatory definition away from being repriced. Under an abrupt net-zero commitment, conventions get rewritten fast, and that is exactly when the hidden half of a footprint surfaces.

So:

1. **Overweight low-contestation, high-consensus names.** Clean under every defensible definition, so no convention change can hurt them.
2. **Underweight high-contestation names regardless of consensus rank.** Their current standing depends on a choice someone else controls.
3. **Non-disclosure raises contestation mechanically**, because the missing-data rule then swings the result. Silence gets priced as risk instead of ignored.

And we name what we do not have: a carbon price path, a repricing horizon, a demand model. A 24-hour project did not produce those and we will not pretend otherwise.

## Why this scores on their rubric

| Criterion | The argument |
|---|---|
| **Impact** | Gives an allocator or a regulator a way to know *when an ESG number is safe to act on*. Named user, concrete decision. |
| **Innovation** | Imports an established metascience method into ESG for the first time. Not a new set of weights. Every other team will bring weights. |
| **Technical Execution** | 36 reproducible pipelines from one parameterised scorer, one command, free data. Reads well to someone opening the repo. |
| **Feasibility** | No paid data. Survives the weekend, and gets *stronger* on 10 Nov 2026 when California's first mandatory Scope 1+2 filings land. |
| **Presentation** | "Honest about limitations" is not a slide at the end. It is the product. |

## The property that makes this safe to build in 24 hours

**Bad data makes the finding stronger, not weaker.**

Most hackathon projects collapse when the dataset turns out to be patchy. Ours does the opposite. Poor Scope 3 coverage widens contestation, and wide contestation is the result we are reporting. There is no data outcome that kills the project. There is only a data outcome that changes the headline number.

Say this out loud in Q&A if anyone probes the data quality. It is the strongest answer available and it is true.

## Scope control

**Minimum viable, must exist by T+9h**
- Boundary A / B / C × revenue denominator × one missing-data rule = 3 specifications, full S&P 500, one chart.

**Target**
- Full 36. Both charts.

**Cuts, in the order we take them**
1. Drop EVIC if enterprise value is slow to source. 36 → 18. Framework unaffected.
2. Drop the within-sector peer group. 18 → 9.
3. Drop one missing-data rule. 9 → 6.
4. Floor is 3. Below that there is no distribution and no project.

**Do not build:** a dashboard, a web app, a login, anything interactive. Slides are compulsory, a web app is optional, and the chart is the product.

## Naming

Working handles, pick one and stop:
- **Contested** — the metric names the product
- **Specification Curve for the S&P 500** — plain, and signals the method to the academics
- **No Single Score** — the thesis as the name

Avoid anything cute. A quant judge discounts a pun.

## Open

- [ ] Confirm Scope 3 is in. Everything here assumes yes.
- [ ] Which company gets the hero specification curve.
- [ ] Contestation as P90 minus P10, or max minus min. P90-P10 is more robust to one weird spec.
- [ ] Name.

## Related

- [[Efforts/Active/ETHack/challenge|challenge]] · [[Efforts/Active/ETHack/sustainability-definition|sustainability-definition]] · [[Efforts/Active/ETHack/aggregate-confusion|aggregate-confusion]] · [[Efforts/Active/ETHack/data-landscape|data-landscape]] · [[Efforts/Active/ETHack/idea|idea]]

## Citations for the deck

- Berg, F., Kölbel, J. F., Rigobon, R. "Aggregate Confusion: The Divergence of ESG Ratings." *Review of Finance*, 2022.
- Simonsohn, U., Simmons, J. P., Nelson, L. D. "Specification Curve Analysis." *Nature Human Behaviour* 4, 2020.
- Steegen, S., Tuerlinckx, F., Gelman, A., Vanpaemel, W. "Increasing Transparency Through a Multiverse Analysis." *Perspectives on Psychological Science*, 2016.

Cite three papers, correctly, and no more. Verify every author list before it goes on a slide.
