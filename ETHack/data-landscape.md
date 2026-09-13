---
edit: owned
last_edited: 2026-09-12T11:52:33 CET
changes: 0
type: reference
status: active
---
# What companies must report, and how the raters score them

Answers the challenge's "source the necessary data, justify your choice". Checked live on 12 Sep 2026, because this area moved hard in 2025 and 2026. Re-verify before quoting any date on stage.

## 1. The headline

**There is no mandatory greenhouse gas disclosure regime in force for US public companies today.** Emissions reporting by S&P 500 companies in September 2026 is, with narrow exceptions, voluntary and unaudited.

This is not a minor caveat. It is the foundation of our argument.

## 2. The regulations, current status

| Regime | Who | Status on 12 Sep 2026 |
|---|---|---|
| **SEC climate disclosure rule** | US listed companies | Adopted Mar 2024, stayed Apr 2024. SEC ended its legal defence Mar 2025. SEC **proposed full rescission**, published in the Federal Register 3 Jun 2026. On the books, not enforced. |
| **California SB 253** | ~4,160 entities, >$1bn revenue doing business in CA | Scope 1+2 first reports due **10 Nov 2026**, moved back from 10 Aug. No assurance required for the first report. Scope 3 from 2027 (5 of 15 categories), limited assurance 2027, reasonable assurance 2030. Penalties to $500k/yr. |
| **California SB 261** | >$500m revenue doing business in CA | Climate financial risk report, first deadline 1 Jan 2026, **currently under court injunction**. Published on company websites, URLs logged to a CARB docket. |
| **EU CSRD** | after the Omnibus, in force 18 Mar 2026 | Threshold raised to **€450m turnover AND 1,000+ employees**. Non-EU groups only if >€450m EU turnover with an EU subsidiary >€200m. Qualifying EU companies report from FY27. **Non-EU parents from FY28, filed 2029.** |
| **EPA GHGRP** | US facilities above the reporting threshold | Genuinely mandatory, facility-level, public, and the only hard US emissions dataset. EPA proposed **ending the programme** in Sep 2025. Historical filings remain published. |

**The date that matters for us: 10 Nov 2026.** California's first mandatory wave lands two months *after* this hackathon. We are working in the last window before US emissions data becomes mandatory. Worth saying on stage.

## 3. So where does the data actually come from

Since almost nothing is compelled, the raters assemble it:

1. **Voluntary sustainability reports.** Company-chosen scope, company-chosen boundary, usually unaudited.
2. **CDP questionnaire.** Voluntary, widely answered by large caps, mostly paywalled for bulk use.
3. **10-K and 20-F filings.** Mandatory and audited, but that mandate covers the *financials*, not the emissions.
4. **EPA GHGRP.** Mandatory, but US-only, facility-level, and needs facility-to-parent mapping.
5. **Estimation models.** Where nothing exists, raters model it from sector and revenue.

Contrast worth holding onto: **the denominator in our score is audited, the numerator is not.**

## 4. How MSCI computes a rating

- 35 ESG Key Issues in total. **Between two and seven** environmental and social issues are selected per company, chosen by GICS sub-industry. Governance applies to everyone.
- Each key issue gets a 0 to 10 score built from two parts: **exposure** (how much risk the business model and locations create) and **management** (how well policies and performance address it).
- Issue weights run **5% to 30%**. The **governance pillar carries a minimum 33% weight in every industry.**
- Weighted scores aggregate to a 0 to 10 company score, then get **normalised against global peers in the same GICS sub-industry**.
- Output: AAA down to CCC.
- Public data only. **Missing data is scored as worst case, not as average.**

Two consequences to state out loud:

**MSCI ratings are industry-relative.** An AAA-rated mining company is not cleaner than a BB-rated software company. It manages mining risk well, compared to other miners. Almost every press release quoting an MSCI rating ignores this.

**At least a third of the score is governance**, in every industry. So a rating people read as "how green is this company" is, by construction, mostly not about environmental damage.

## 5. How Sustainalytics computes a rating

A different object entirely.

1. Total **exposure** to each material issue at sub-industry level.
2. Split it into **manageable** and **unmanageable** risk. Carbon emissions for an oil producer are treated as partly unmanageable, inherent to the business.
3. **Managed risk**: what policies, programmes and performance actually address.
4. **Management gap**: manageable risk that is not being managed. Controversies count against here.
5. **Unmanaged risk** is the final score.

Five bands, negligible through severe. Positioned as an **absolute** measure, not peer-relative. **Lower is better.**

## 6. Why 0.61 was never going to be higher

Line the two up:

| | MSCI | Sustainalytics |
|---|---|---|
| What it measures | quality of ESG risk management | quantity of unmanaged ESG risk |
| Direction | higher is better | lower is better |
| Benchmark | relative to GICS sub-industry peers | absolute |
| Industry-inherent risk | normalised away | explicitly subtracted as "unmanageable" |
| Missing data | worst case | modelled |
| Governance share | minimum 33% everywhere | material-issue dependent |

These are not two attempts at the same measurement that happen to differ. They are **two different questions sharing one word.** Correlating at 0.61 is the expected result, not a scandal.

That is the paper's point made concrete, and it is exactly what [[Efforts/Active/ETHack/aggregate-confusion|aggregate-confusion]] decomposes into scope, measurement and weight.

## 7. What this licenses us to do

- **Our data choice is defensible by elimination.** We use physical emissions quantities and audited financials because they are the only inputs whose definitions two honest analysts would agree on. See [[Efforts/Active/ETHack/sustainability-definition|sustainability-definition]] section 2.
- **We can state a real coverage number.** In a voluntary regime, who discloses is itself a variable. That is a finding, not a data-quality complaint.
- **We are not competing with MSCI.** We are answering a different question from either of them: how much environmental damage, per unit of value, and how much does that answer depend on where you draw the line.

## Sources

SEC: [press release on proposed rescission](https://www.sec.gov/newsroom/press-releases/2026-49-sec-proposes-rescission-climate-related-disclosure-rules) · [Federal Register, 3 Jun 2026](https://www.federalregister.gov/documents/2026/06/03/2026-11091/rescission-of-climate-related-disclosure-rules)
California: [SB 253 / SB 261 overview](https://www.persefoni.com/blog/california-sb253-sb261)
EU: [KPMG on the Omnibus agreement](https://kpmg.com/xx/en/our-insights/ifrg/2025/esrs-eu-omnibus.html)
EPA: [GHGRP](https://www.epa.gov/ghgreporting) · [proposed repeal](https://www.epa.gov/newsreleases/epa-releases-proposal-end-burdensome-costly-greenhouse-gas-reporting-program-saving-24)
Raters: [MSCI ESG Ratings methodology](https://www.msci.com/documents/1296102/34424357/MSCI+ESG+Ratings+Methodology.pdf) · [Sustainalytics ESG Risk Ratings](https://www.sustainalytics.com/esg-data)
