---
edit: owned
last_edited: 2026-09-12T16:35:38 CET
changes: 0
type: project-note
status: proposed
---
# Design v2: one industry, balanced grid, three pillars

The v1 design had a real flaw Aram identified: a company that disclosed nothing got 12 cells and a company that disclosed got 4, so the two were ranked over different pools and the ranks were not comparable. This version fixes that structurally, narrows to one industry, and uses the Bloomberg/Moody's access properly.

## 1. Two findings that change the framing

Both verified 12 Sep 2026. Together they turn "ESG data is bad" into something much sharper.

### The providers are retreating from single scores

**S&P Global discontinued its numerical ESG credit indicators in August 2023**, citing investor confusion about their relevance, and reverted to narrative analysis.

### MSCI repriced 37% of the market by changing its own mind

**MSCI's ESG Ratings model v5.0 took effect March 2026.** Roughly **37% of rated issuers had their rating repriced: 26% from the model change itself**, 11% from routine data updates.

Read that again. Not a change in the companies. Not a change in the world. **One provider revised its own methodology and a quarter of the universe moved.**

That is contestation, measured and published by MSCI itself. It is the single best piece of external validation available to us and it cost nothing.

### And as of ten weeks ago, this is a regulated activity

**The EU ESG Rating Regulation entered into force on 2 July 2026.** ESMA is now the single supervisor for ESG rating providers across the EU. Providers must be authorised, and users are entitled to receive the rating methodologies. Existing providers must notify ESMA by **2 August 2026** and apply for authorisation by **2 November 2026**, which is seven weeks away.

So a regulator now has legal standing to ask providers how their ratings are built. The obvious follow-up question, which nobody yet answers, is **how much does the rating depend on those choices.** That is exactly what this framework measures.

## 2. The industry: Electric Utilities (NAICS 2211)

Seven reasons, and the first one is the decisive one.

1. **It is the only major industry where the correct denominator is physical and free.** tCO2e per **MWh generated** is the real industry metric, not a proxy for it. EIA Form 923 publishes net generation in MWh per plant, free and public, 2001 to present. This lets us prove that the denominator choice is *industry-specific* rather than arbitrary, which is the whole argument for doing this per sector.
2. **Enormous variation inside one NAICS code.** NextEra is the largest renewables operator in the country. Southern and AEP run large coal fleets. Exelon and ConEd barely generate at all. Same industry code, different physics.
3. **The best GHGRP coverage of any sector.** Power plants are the flagship reporters. Our own pull already returned 102 facilities for Southern, 54 for Duke, 30 for NextEra.
4. **The social pillar is physical here.** Safety, keeping the lights on, and whether people can afford the bill. All measured, all publicly reported, no ideology required.
5. **Highest exposure to a net-zero shock**, which makes the bonus question real rather than hypothetical.
6. **Maximum Moody's and Bloomberg coverage**, because utilities are the most leveraged sector in the index and therefore the most rated.
7. **Two companies will break the MWh denominator.** Exelon and ConEd distribute power without generating much of it. That is a genuine finding about denominator fragility that we discover from the data rather than assert.

## 3. The balance fix

**The problem.** "What do we do when a company disclosed nothing" is a dimension that only exists for *some* companies. That is an unbalanced design, and it means two companies get ranked over different pools.

**The fix.** Replace it with a dimension every company has a value for:

> **Source of truth** (3 options): self-reported · regulator-reported · provider-rated

All three exist for all ten companies. Where one is genuinely missing, the cell still exists and is filled by a substitution rule that is **identical for every company**, and the substitution is recorded as a coverage flag.

The critical property: **the substitution rule is a property of the design, not of the company.** So every company faces the same grid, the ranks are over the same pool, and the design is balanced.

**And non-disclosure does not disappear, it becomes measurable.** Instead of a structural hole, it shows up as the **gap between the self-reported and the regulator-reported cell.** A company whose own number sits far below the regulator's is telling you something, and now it is a quantity rather than an absence.

## 4. The grid: 3 × 3 × 3, three times

Every company gets **81 specifications**: 27 in each pillar. Identical grid, every company, no exceptions.

### Environmental — 27

| Dimension | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| **Boundary** | Scope 1, combustion at owned plants | Scope 1+2, adds purchased power | Scope 1+2+3, adds fuel supply chain and upstream methane |
| **Denominator** | per **MWh generated** (physical, industry-native) | per dollar of revenue | per dollar of enterprise value |
| **Source** | company self-reported | EPA GHGRP + EIA | provider-rated |

### Social — 27

The three components, all physical and all publicly reported for US utilities:

- **Safety.** OSHA recordable incident rate, or employee and contractor fatalities. Utility work kills people.
- **Reliability.** SAIDI, minutes of outage per customer per year, reported to **EIA Form 861**. Whether the power actually stays on.
- **Affordability.** Average residential retail rate in cents per kWh, from EIA. Whether people can pay the bill.

| Dimension | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| **Which component leads** | safety-led | reliability-led | affordability-led |
| **Window** | latest year | 3-year average | **worst year in 3** |
| **Source** | company self-reported | EIA + OSHA | provider-rated |

The **worst-year-in-3** option is not padding. For a utility with a wildfire or a winter-storm failure, the difference between its average and its worst year is the entire story. PG&E is in the sample precisely to make that visible.

### Financial resilience — 27, replacing governance

**Why we replace G, and the argument is not political.** A utility that cannot afford to decarbonise will not decarbonise, whatever its governance documents say. Capital capacity is a *sustainability* variable for a capital-intensive regulated business, and it is measurable. Governance, as scored today, is largely a policy-existence checklist, and policy existence is exactly what MSCI itself moved away from rewarding in its 2026 model update.

| Dimension | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| **Metric** | leverage, net debt / EBITDA | transition funding capacity, free cash flow after dividends ÷ capex | credit quality, **Moody's issuer rating** |
| **Window** | latest year | 3-year average | worst year in 3 |
| **Source** | reported financials (SEC XBRL) | **Moody's adjusted figures** | market-implied (credit spread or EV) |

This is where the Moody's access earns its place: adjusted debt and the issuer rating are things we cannot get for free and genuinely improve the pillar.

## 5. We do not publish a combined score

Combining E, S and F requires a weight, and weights are the 13.2% of rating divergence we deliberately refuse to argue about. So:

**Default output: three separate distributions per company. No total.**

Two optional aggregations are offered, clearly labelled, so a reader who wants one number can have one and see what it cost:

- **Equal thirds** — E 1/3, S 1/3, F 1/3
- **Environment-led** — E 1/2, S 1/4, F 1/4

Keep it to two. The point of showing them is to demonstrate that the weight changes the answer, not to recommend a weight.

## 6. The ten companies

Chosen so that each one breaks the framework in a different place.

| # | Company | Why it is in |
|---|---|---|
| 1 | **NextEra Energy** (NEE) | largest renewables operator. The E benchmark for "clean". |
| 2 | **Southern Company** (SO) | large coal and gas fleet plus new nuclear at Vogtle. 102 GHGRP facilities already confirmed. |
| 3 | **Duke Energy** (DUK) | big coal fleet mid-transition. 54 facilities confirmed. |
| 4 | **American Electric Power** (AEP) | coal-heavy generation plus the largest transmission network. |
| 5 | **Dominion Energy** (D) | offshore wind build-out funded with heavy leverage. E and F pull against each other. |
| 6 | **Xcel Energy** (XEL) | aggressive public decarbonisation pledge. Tests self-reported against regulator-reported. |
| 7 | **Exelon** (EXC) | wires only after the Constellation spin-off. **Barely generates, so the MWh denominator nearly breaks.** Deliberate. |
| 8 | **Consolidated Edison** (ED) | urban distribution, little generation. The second denominator breaker. |
| 9 | **PG&E** (PCG) | **the star of the sample.** Among the cleanest power in the country, and it caused fatal wildfires and went through bankruptcy. Wins on E, last on S and F. |
| 10 | **Vistra** (VST) | merchant generator, unregulated, coal plus nuclear. No rate base, so the financial pillar behaves completely differently. |

**PG&E is the slide.** One real company, cleanest on environment, worst on social and financial. If you ever needed proof that a single ESG letter destroys information, it is PG&E.

## 7. Scaling, honestly

**How it generalises.** The code does not change between industries. Only the **question definitions** change: which boundary options, which denominators, which components. One industry specialist defines a question set per sector once, and the framework runs unchanged. There are 99 three-digit NAICS sectors, or 69 GICS industries, so this is a finite, fundable exercise, not an open-ended research programme.

**What it costs.** Name the providers and the tiers, and do not invent prices. Bloomberg terminal and data licence, Moody's issuer ratings and adjusted financials, MSCI and Sustainalytics ratings, CDP disclosure data. **We did not obtain quotes and will not put a made-up number on a slide.** What we will say: the free regulator layer (EPA, EIA, SEC) runs at zero cost and already produces a complete framework, and each paid layer narrows the distribution rather than being required to produce it.

**Why the code scales.** 10 companies × 81 specifications is 810 computations. 500 companies × 81 is 40,500, which is milliseconds. The binding constraint was never compute or API volume, it is entity resolution: matching a parent company name to its facilities. For utilities that is unusually tractable, because EIA already publishes the plant-to-operator mapping.

## 8. The AI layer, specified so it cannot invent things

An LLM reads the **specification table**, not the internet, and writes the per-company explanation:

- **Robust case:** "This rating holds across all 27 environmental specifications. The spread is N units, driven almost entirely by boundary choice. You can act on this number."
- **Contested case:** "This rating moves N places depending on the denominator alone. Under MWh it is top quartile; under enterprise value it is bottom quartile. A single published score for this company is a methodology artifact."

The constraint that makes this defensible: **the model is given the numbers and the dimension names and asked to explain which dimension drove the spread.** It is grounded generation over a fixed table, so it cannot hallucinate a fact that is not in the grid. Say that explicitly, because "we plugged in an AI" is otherwise the weakest sentence in any hackathon pitch.

## 9. What this lets you say

> Funds today buy two or three ratings and still guess, because every provider hides its choices inside one letter. MSCI changed its own model in March and repriced 37% of the market. S&P gave up on numerical ESG scores altogether in 2023. And since 2 July this year ESMA regulates these providers and can demand their methodologies.
>
> We do not sell a better letter. For one industry, with a physical denominator that industry actually uses, we publish where a company lands across every defensible way of asking the question, and how far it travels. Then a fund knows which ratings it can act on and which are noise, and a regulator knows which conventions to standardise first.

## 10. Open decisions

- [ ] Confirm which 10 utilities the Bloomberg/Moody's download can actually cover. Ten is the cap.
- [ ] Confirm Moody's issuer rating and adjusted debt are in the downloadable fields.
- [ ] SAIDI: with or without major event days. EIA reports both, and it is itself a defensible choice worth considering as a fourth dimension.
- [ ] Fiscal year. Utilities are calendar-year, so FY2023 or FY2024 depending on Bloomberg coverage.
- [ ] Whether to show one aggregation or two.

## Sources

- [S&P Global discontinues numerical ESG credit indicators, Aug 2023](https://fintech.global/2023/08/09/sp-global-discontinues-esg-numerical-scores-amid-questions-of-their-relevance/)
- [MSCI ESG Ratings v5.0 2026 model update, 37% of issuers repriced](https://www.getsunhat.com/blog/msci-esg-rating-update-2026) · [MSCI's own deck](https://www.msci.com/downloads/web/msci-com/discover-msci/events/event-assets/2026/february/msci-esg-ratings-2026-model-update---transition-plan---model-enhancements---apac-session/MSCI%20ESG%20Ratings%202026%20Model%20Update%20APAC%20Webinar_February%2025,%202026.pdf)
- [EU ESG Rating Regulation, ESMA supervision from 2 July 2026](https://www.stibbe.com/publications-and-insights/esg-ratings-and-new-eu-supervision-as-of-2-july-2026)
- [EIA Form 923, net generation MWh by plant, free](https://eia.gov/electricity/data/eia923/) · [PUDL cleaned version with utility linkage](https://docs.catalyst.coop/pudl/en/latest/data_sources/eia923.html)
- [EIA Electric Power Annual, technical notes incl. reliability](https://www.eia.gov/electricity/annual/pdf/tech_notes.pdf)

## Related

[[Efforts/Active/ETHack/framework|framework]] · [[Efforts/Active/ETHack/how-many-specs|how-many-specs]] · [[Efforts/Active/ETHack/impact-and-innovation|impact-and-innovation]] · [[Efforts/Active/ETHack/data-landscape|data-landscape]]
