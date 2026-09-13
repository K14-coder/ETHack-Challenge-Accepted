---
edit: owned
last_edited: 2026-09-12T14:26:21 CET
changes: 0
type: project-note
status: active
---
# Execution plan: 6 companies, 4 people, 17 hours

Written 12 Sep 14:25 CET. Freeze at 08:00 tomorrow, so **17.5 hours of build time.**

## Verdict on the plan: yes, with one correction

**Cutting from 500 companies to 6 is the best decision made today.** It removes the single biggest risk, parent-name matching across 500 firms, which was capped at two hours and could have eaten four. Six companies can be checked by hand, so every number on the slide is defensible. The rubric says *"how much actually works"*, and six companies fully worked beats 500 half-broken.

**The correction: with 6 companies, rank is meaningless.** "Walmart moved from 2nd to 5th" is not a headline. "Moved 350 places out of 500" is.

So the deep dive must report **intensity, not rank.** Intensity is absolute and needs no peers. Rank is relative and needs the index. Six companies gives us intensity ranges and ratios in physical units, which is actually *stronger* than a rank because it is in tonnes rather than positions.

### The resulting architecture

| Layer | Scope | What it gives | Risk |
|---|---|---|---|
| **Core, must land** | **6 companies**, all 72 specifications, disclosed + modelled | intensity ranges, ratios, the specification curve per company | low, data already proven |
| **Stretch, only if core is done** | **500 companies**, modelled layer only (revenue × EEIO factor) | real ranks, contestation in rank places, Figure 2 | medium, bulk pull + join |

The stretch layer needs only revenue and NAICS, both bulk-pullable in ~6 API calls. No name matching at all. So it is genuinely optional and genuinely cheap.

**The 6 companies are the project. The 500 is the upside.** That is the right way round.

## The company set

Reframe the selection criterion: **you are not picking 6 industries, you are picking 6 positions on the contestation axis.** Each one has to earn its place by being a different *kind* of case.

| Company | Sector | Why it is in | Expected position |
|---|---|---|---|
| **Walmart** | Retail | No emissions figure in the mandatory dataset at all. Registered only as an importer of pre-charged F-gas equipment. | maximum contestation |
| **Nucor** | Materials | 5.76 Mt disclosed across 26 facilities, all in its own electric-arc furnaces. **Data already pulled and verified.** | minimum contestation, high intensity |
| **JPMorgan** | Financials | Burns almost nothing, finances everything. The purest boundary case. | extreme contestation |
| **Ford** | Autos | Footprint is customers driving the cars. Scope 3 use-phase dominant. | high contestation |
| **Meta** | Tech | Data centre electricity. The Scope 2 case, where boundary B does the work. | medium |
| **a large utility** | Utilities | See below. | minimum contestation |

### Two changes to the proposed list

**Drop General Electric.** GE separated into GE Aerospace, GE Vernova and GE HealthCare across 2023-24. "Which GE" is a question you do not want in Q&A, and the parent-name matching is a mess. Not worth it.

**Add a utility instead of pharma** (Duke, Southern or NextEra). This is the pick that closes the story:

> The electricity powering every Walmart store and every Meta data centre is reported to EPA by **this** company, under **its** name. Not Walmart's, not Meta's.

That single sentence explains the whole boundary problem with two companies already on your slide. Eli Lilly is a fine company to study and adds nothing the other five do not already cover.

**Keep Nucor.** Its data is already pulled, verified and committed in `data/`. It is free coverage of the "robustly dirty" corner, which you need as the control case that makes Walmart's swing mean something.

## The MSCI task: keep it, but reframe it

Your colleague's instinct is good and the task is feasible. **MSCI publishes a free ESG Ratings & Climate Search Tool**, so six letter ratings can be looked up by hand in minutes.

But it is **not** a divergence study across providers. Six providers would be far too few for that, which is exactly why we dropped that angle this morning.

What it is instead: **a reference point on our chart.** One published letter, drawn as a single line across our 72-point spread.

> MSCI says AA. Our seventy-two defensible methods put this company anywhere from top decile to bottom quartile.

That is one of the strongest slides available, and it needs six manual lookups. Also grab the Sustainalytics risk band per company if it is publicly visible, remembering the two run in **opposite directions**: MSCI higher is better, Sustainalytics lower is better.

## Four-person split

Nobody blocks anybody. That is the whole design.

### Person A, Data
Owns every pull. Produces **one** tidy table and nothing else.
- GHGRP facilities + emissions for the 6 parents, year 2023, via `dmapservice` (working syntax in [[Efforts/Active/ETHack/proof-nucor|proof-nucor]])
- SEC revenue via the frames API, with the **4-tag fallback chain** (`Revenues` alone fails, see the Nucor proof)
- Market cap for the EVIC denominator
- EPA EEIO factor CSV, matched on NAICS
- Deliverable: `data/interim/companies.csv`, one row per company, columns agreed with B **in the first 30 minutes**

### Person B, Scorer
Owns one function and the loop over it.
- `score(boundary, denominator, missing_rule, peer_group, consolidation)`
- the 72-combination loop, plus consensus, IQR and full range
- the Spearman statistic benchmarked against 0.61
- **Starts on a fake 6-row table immediately.** Never waits for A.
- Deliverable: `results.csv`, 6 × 72

### Person C, Charts and reference ratings
- Figure 1, the specification curve, one company, 72 points plus the choice dashboard
- The MSCI and Sustainalytics manual lookups, overlaid as reference lines
- Figure 2 only if the 500-company stretch layer lands
- Deliverable: PNGs at slide resolution

### Person D, Pitch
**Starts now, not at hour 20.** The pitch shapes what gets built.
- Slides, in **`.ppt`** (ask the organisers whether `.pptx` is accepted, this is a mechanical disqualification risk)
- The 3-minute script, timed out loud
- Submission portal, backup demo recording
- Deliverable: submitted deck plus a rehearsed script

**Aram:** take the pitch, or integration. You are carrying all the context, so you are the wrong person to put on a data pull and the right person to own the story and make the scope cuts.

## Checkpoints, real clock times

| Time | Checkpoint | Cut if missed |
|---|---|---|
| **15:25** | Roles locked. Column names for `companies.csv` agreed. MSCI lookups started. | nothing, this is non-negotiable |
| **18:25** | End-to-end skeleton runs on fake data and produces a chart. | drop EVIC, 72 → 36 |
| **22:25** | All 6 companies have real disclosed and modelled numbers. | drop a company, keep Walmart and Nucor |
| **02:25** | Figure 1 drawn from real data. Spearman computed. | drop Figure 2 and the 500 layer |
| **05:25** | Slides done, exported to `.ppt`. | drop the variance decomposition |
| **06:25** | Rehearsed twice, timed to 3:00. | nothing |
| **08:00** | **FREEZE.** Submit. Sleep. | nothing |

## What we will not build

No dashboard. No web app. No login. No interactivity. Slides are compulsory, a web app is optional, and the chart is the product.

## Related

[[Efforts/Active/ETHack/framework|framework]] · [[Efforts/Active/ETHack/quantitative-claims|quantitative-claims]] · [[Efforts/Active/ETHack/proof-nucor|proof-nucor]] · [[Efforts/Active/ETHack/finding-walmart|finding-walmart]] · [[Efforts/Active/ETHack/data-plan|data-plan]]
