---
edit: owned
last_edited: 2026-09-12T17:42:01 CET
changes: 0
type: project-note
status: proposed
---
# Design v3: every indicator, every pillar, type-aware dimensions

Aram's diagnosis of v1 was exactly right: **we designed four dimensions for one indicator (emissions) in one pillar (environmental), then pretended they generalised.** They do not. This document fixes that and justifies every choice from the Bloomberg materiality export.

Source file: `Exxon materiality map 2.xlsx`, Bloomberg "Financially Material Data", ticker XOM, **peer group "Integrated Oils"**, five fiscal years 2021-2025.

## 1. What is actually in the file

| | Fields | Usable (3+ years) | Coverage |
|---|---|---|---|
| **Environmental** | 64 | 37 | **58%** |
| **Social** | 35 | 19 | **54%** |
| **Governance** | 115 | 106 | **92%** |
| Unique field IDs | **187** | **135** | 72% |

Bloomberg reuses the same field under multiple sub-issues, so 214 rows collapse to 187 unique field IDs.

### The first finding, and it is free

**The pillar with the best data is the pillar with the least physical meaning.**

Governance is 92% covered because it is scraped from proxy statements, which are **mandatory SEC filings**. Environmental is 58% covered because it is **voluntary self-reporting**. So the thing we can measure most reliably is board tenure, and the thing we can measure worst is what the company emits.

That is a structural fact about ESG data, visible in a single export, and it explains a great deal about why ESG scores behave the way they do.

## 2. The core design problem, and the answer

**You cannot apply one dimension set to every indicator, because the legitimate dimensions are a property of the measurement type.**

- Dividing a **Boolean** by revenue is meaningless. "Has a water policy per million dollars" is not a quantity.
- Dividing a **Rate** by revenue is double-normalising. TRIR is already per 200,000 hours worked.
- A **physical quantity** is meaningless *without* a denominator. 90 million tonnes tells you nothing until you know per what.

So: **five measurement types, five dimension sets.** Every field is classified once, and its type determines its grid.

| Type | What it is | Fields | Usable | Dimensions | Specs/field |
|---|---|---|---|---|---|
| **Q** | physical quantity | 44 | 15 | denominator (3) × window (3) × direction (2) | **18** |
| **R** | already-normalised rate | 16 | 10 | population (3) × window (3) × direction (2) | **18** |
| **P** | percentage | 12 | 4 | window (3) × direction (2) | **6** |
| **B** | boolean / policy | 52 | 52 | stringency (3) × persistence (2) | **6** |
| **S** | structural count | 63 | 54 | reference (3) × window (3) | **9** |

**1,272 specification-field combinations per company. 20 companies = 25,440 computations.** Milliseconds.

## 3. Justifying each dimension, with real numbers from the file

### Denominator (Q only, 3 options)

`per revenue` · `per unit of physical output` · `per employee`

A physical quantity has no meaning alone, and the denominator you choose **embeds a theory of what the company is for.** Revenue says economic value. Physical output says physical product. Employees says human enterprise. None is wrong.

For Integrated Oils the physical denominator is **barrels of oil equivalent produced**, which every company in the peer group reports. This is the whole reason to work inside one industry: the physical denominator exists and is comparable.

### Window (Q, R, P, S — 3 options)

`latest year` · `3-year mean` · `worst of last 3`

**Justified by Exxon's own flaring data.** Gas flaring fell from 2,606,100 tonnes in 2021 to 1,180,410 in 2025, **down 54.7%**. On the latest year the company looks transformed. On a 3-year mean, much less so. On worst-of-3, barely changed.

The window choice is worth more than half the answer on this single field, from real reported data.

### Direction (Q, R, P — 2 options)

`level` · `3-year change`

Level answers "how dirty now". Change answers "which way is this going". They are different questions and they can disagree completely. **The file proves it twice over:**

| | 2021 | 2025 | change |
|---|---|---|---|
| **Scope 1 operational emissions** | 98,000,000 t | 90,000,000 t | **−8.2%** |
| **Embedded carbon in total reserves** | 7,789,274,004 t | 8,160,534,132 t | **+4.8%** |

Exxon's operational emissions are falling while **the carbon it owns in the ground is growing.** Since 2023 the reserves figure is up 14.6%. Same company, same five years, opposite directions, and the reserves number is **83 times larger**.

A second one, same pillar, same issue:

| | change 2021-2025 |
|---|---|
| Gas flaring | **−54.7%** |
| Scope 2, location-based | **+28.6%** |

And the cleanest demonstration of all, on one incident class:

| | 2021 | 2025 | change |
|---|---|---|---|
| **Hydrocarbon spills, volume** | 3,434 m³ | 954 m³ | **−72.2%** |
| **Hydrocarbon spills, count** | 158 | 402 | **+154.4%** |

More spills, each smaller. Whether Exxon's spill performance improved or collapsed depends entirely on whether you count litres or events. **Nobody publishing a single environmental score tells you which one they used.**

### Population (R only, 3 options) — this is the important one

`employees` · `contractors` · `total workforce`

**This is not our invention. Bloomberg reports all three separately**, and it is the social equivalent of the Scope 1 versus Scope 3 boundary game.

Exxon, 2025 reported:

| Metric | Employees | Contractors | Workforce |
|---|---|---|---|
| Total Recordable Incident Rate | **0.10** | **0.21** | 0.17 |
| Lost Time Incident Rate | 0.01 | 0.02 | 0.02 |
| **Fatality rate** | **0.017** | **not reported** | **0.034** |

Contractors are recorded at **2.1× the employee injury rate.** Employee TRIR improved 9.1% over the period while **contractor TRIR worsened 10.5%.**

And the fatality row is the finding. Employee fatality rate 0.017, workforce fatality rate 0.034 — twice as high. Workforce is employees plus contractors, so for the blended rate to be double the employee rate, **the contractor rate must be materially higher than either.** It is the one cell in the table that is not reported.

**A company can look safe on its own payroll while the danger sits with people it does not employ.** That is exactly the Scope 1 versus Scope 3 move, in the social pillar, and it proves the boundary problem is not about emissions. It is about every indicator where the company chooses the boundary of "us".

One more, because it cuts against the safety story: **Tier 1 process safety event rate rose 59.4%** over the period while employee TRIR fell. The most serious class of incident got worse while the headline safety number improved.

### Stringency (B only, 3 options)

`all booleans count equally` · `substantive only` · `outcome-linked only`

- **all** — any Y counts, including "Risks Discussed" and "Physical Risk Identified"
- **substantive** — a policy or a programme counts; merely *discussing* or *identifying* a risk does not
- **outcome-linked** — only a claimed science-based target or net-zero commitment counts

**Justified by MSCI's own behaviour, not by us.** MSCI's ESG Ratings model **v5.0 took effect March 2026** and shifted explicitly "from rewarding policies and disclosure to emphasizing measurable, financially material performance". It repriced roughly **37% of rated issuers, 26% from the model change alone.**

So the stringency choice is the precise change MSCI made, and making it moved a quarter of the market. We measure continuously what MSCI did once, in secret, retroactively.

Exxon's climate booleans make the point:

| Field | Value |
|---|---|
| Risks of Climate Change Discussed | **1** |
| Climate Scenario Analysis | **1** |
| Company Claims Net Zero Target | **1** |
| Climate Change Opportunities Discussed | **0** |
| Internal Carbon Pricing | **0** |
| Company Claims Science-Based Targets | **0** |

Under `all` it scores 3 of 6. Under `outcome-linked only` it scores 1 of 2, and the one it has is the unaudited self-declared kind.

### Persistence (B only, 2 options)

`true in the latest year` · `true in every one of the last 3 years`

A policy adopted last quarter and a policy held for five years are not the same commitment, and Booleans are the only field type where a company can change its score without changing anything physical.

### Reference (S only, 3 options)

`absolute` · `ratio to its own base` · `relative to peer-group median`

A board of 13 is meaningless alone. **12 independent directors out of 13** is meaningful. Both are meaningless without the Integrated Oils norm. Exxon: board size 13, independent directors 12, chairperson tenure 9 years, CEO duality Y, independent chairperson N.

## 4. Intra-industry versus inter-industry

Aram asked for this justified. The two are **not the same exercise**, and that is the point.

### Intra-industry is where the framework is valid

**Bloomberg already made the materiality judgment for us.** Row 2 of the export reads `Peer Group: Integrated Oils`, and row 3 states that "the fields selected are relevant for this peer group". The field set *is* the industry definition, and we did not choose it.

Four reasons it works:

1. **The field set is constant.** Every integrated oil has gas flaring, produced water, Arctic drilling exposure, embedded carbon in reserves. The same specification is computable for all 20.
2. **A physical denominator exists and is comparable.** Barrels of oil equivalent. Universally reported in this peer group.
3. **Disclosure norms are shared**, so a missing field carries information. When Exxon does not report contractor fatality rate, that is a *choice*, because its peers face the same expectation. Outside the industry it would merely be inapplicable.
4. **It matches the real decision.** An allocator who must hold energy exposure needs to know *which* integrated oil, not whether to prefer a software company.

### Inter-industry is where the framework exposes the rating agencies

1. **The field set changes, so the specification is not computable.** Bloomberg's materiality map for a bank contains no flaring, no produced water, no Arctic drilling. Cross-industry comparison therefore requires **reducing to a common core** — Scope 1, Scope 2, energy, revenue, employees, fines, board structure — and discarding everything industry-specific.
2. **That reduction destroys most of the information, and nobody discloses it.** For Exxon the common core retains roughly 8 of 37 usable environmental fields. The 29 discarded are precisely the ones that describe an oil company.
3. **MSCI's own answer is to normalise within sub-industry.** Which is why an AAA-rated miner is not cleaner than a BB-rated software firm. **The single cross-industry letter is already an intra-industry score wearing a cross-industry costume**, and almost nobody who quotes one knows this.

### So it becomes a dimension

**Comparison frame (2 options):** `intra-industry, full materiality map` · `inter-industry, common core only`

Reporting both *is* a finding: how far does a company's standing move when you strip away everything specific to its own industry? That number has never been published, and it is the honest measure of what a cross-industry ESG letter costs you.

## 5. Aggregation: we do not choose the tree either

Bloomberg's export is already hierarchical: **Pillar → Issue → Sub-Issue → Field.**

We use that hierarchy as the aggregation tree. Field-level distributions roll up to sub-issue, sub-issue to issue, issue to pillar.

This matters for defensibility. **The only thing we choose is the dimension set per measurement type. The field set, the materiality judgment, the peer group and the tree all come from Bloomberg.** That is a very small surface area to attack.

And as before: **no single ESG number.** Combining pillars requires a weight, and a weight is the one thing we refuse to invent. Three pillar distributions, published separately.

## 6. What we deliberately exclude, and why

- **52 fields with fewer than 3 years of data.** Reported, with the count, as a coverage statistic. Non-disclosure is a finding, not a gap to fill.
- **Fields identical across all five years and all peers** carry no information and are dropped, with the list published.
- **Duplicate field IDs.** Bloomberg lists e.g. CG003 under three sub-issues. Counted once. This alone cuts 214 rows to 187.
- **Gender and age diversity fields.** Available, and we exclude them. The honest reason: we are not equipped to defend a direction of effect. We do not claim they are immaterial; we claim we cannot justify a sign, and a dimension we cannot justify has no business in a framework whose entire argument is that every choice must be defensible. **Stated in the paper, not hidden.**

## 7. The 20 companies

**Do not let me guess the peer set.** Export Bloomberg's own `Integrated Oils` peer group membership, because three obvious names were acquired during the data window: **Pioneer Natural Resources** (by Exxon, 2024), **Hess** (by Chevron), **Marathon Oil** (by ConocoPhillips, 2024). A guessed list would contain companies that stopped existing mid-sample.

Using Bloomberg's own peer definition also removes one more thing for us to have chosen.

## 8. What to check before building

- [ ] Export Bloomberg's `Integrated Oils` peer group membership list.
- [ ] Confirm barrels of oil equivalent produced is in the downloadable fields. The physical denominator depends on it.
- [ ] Confirm the same field IDs are populated across peers, not just for Exxon. Coverage may be worse for smaller names.
- [ ] Decide whether to include the two non-US supermajors if Bloomberg's peer group has them, since jurisdiction then becomes a further dimension.

## 9. Sources

- Bloomberg Financially Material Data export, XOM, peer group Integrated Oils, FY2021-2025. The file itself.
- [MSCI ESG Ratings v5.0 2026 model update, 37% of issuers repriced](https://www.getsunhat.com/blog/msci-esg-rating-update-2026)
- [S&P Global discontinued numerical ESG credit indicators, 2023](https://fintech.global/2023/08/09/sp-global-discontinues-esg-numerical-scores-amid-questions-of-their-relevance/)
- [EU ESG Rating Regulation, ESMA supervision from 2 July 2026](https://www.stibbe.com/publications-and-insights/esg-ratings-and-new-eu-supervision-as-of-2-july-2026)
- Berg, Kölbel & Rigobon, *Aggregate Confusion*, Review of Finance 2022
- Simonsohn, Simmons & Nelson, *Specification Curve Analysis*, Nature Human Behaviour 2020

## Related

[[Efforts/Active/ETHack/design-v2-utilities|design-v2-utilities]] · [[Efforts/Active/ETHack/framework|framework]] · [[Efforts/Active/ETHack/how-many-specs|how-many-specs]] · [[Efforts/Active/ETHack/impact-and-innovation|impact-and-innovation]]
