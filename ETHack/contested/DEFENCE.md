# Defence brief — CONTESTED

Ten attacks, ranked by how much they hurt. For each: whether it is right, and the answer.

**The rule that governs every answer below:** we make an **existence** claim, not a **prevalence** claim.

> Existence: "the ranking *can* completely invert between two defensible conventions." Needs one example. We have three.
>
> Prevalence: "X% of the S&P 500 inverts." Needs the whole index. **We do not claim this.**

Most attacks on a 4-company sample are attacks on a prevalence claim. Do not make one and they miss.

---

## 1. "Revenue is the wrong denominator for an EEIO factor." — CORRECT

The EPA factor is kg CO2e per dollar of **purchaser price of the commodity**, not per dollar of company revenue.

**Answer:** Agreed, and we label it a **screening estimate**, which is what it is. Revenue-based screening is standard first-pass practice for Scope 3 before activity data exists. We never call it an accounting result. If you want the accounting result you need purchase-level spend data, which no public source provides.

## 2. "You compare cradle-to-gate EEIO against direct-only GHGRP. Apples and oranges." — CORRECT

**Answer:** They *are* different things. That is the finding, not a bug. The only **mandatory** number is the narrow one. So an investor relying on compulsory disclosure gets the narrow one and nothing tells them how narrow it is.

Critical framing discipline: the ratio is **"what must be disclosed versus what is plausibly caused."** It is **not** "underreporting" and we never say that word.

## 3. "GHGRP is US-only and above a 25,000 t threshold, so of course a global company looks small." — CORRECT

**Answer:** Yes. Every disclosed number we report is a **floor, not a measurement**, and we say so on the slide. But that floor is precisely what the mandatory US regime delivers today. Criticising us for it is criticising the regime, which is our point.

## 4. "Your modelled layer gives every company in a sector the same intensity, so it cannot differentiate." — CORRECT

**Answer:** Correct, and we found it ourselves: modelled intensity equals the factor by construction (revenue × factor ÷ revenue). The consequence is the interesting part. **Disclosed data is the only thing that creates within-sector variation.** So the missing-data rule does not merely shift the ranking, it decides whether within-sector comparison is possible at all.

## 5. "n=4 is far too small to conclude anything." — FAIR, AND THE MOST LIKELY ATTACK

**Answer:** Four is the hand-verified deep dive, not the sample for a population claim. Two things:

1. We make an **existence** claim. One counterexample is sufficient to show the ranking can invert. We have three companies doing it.
2. The method scales: **~39 API calls** for all 500 companies (bulk-pull then join locally, never per company) and **12 ms** of compute for 500 × 72 specifications, measured. The constraint is parent-name matching, not the method.

## 6. "Walmart obviously emits. Your data is wrong." — MISREADS THE CLAIM

**Answer:** We never claim Walmart emits nothing. We claim: **the mandatory US emissions dataset contains no emissions figure for Walmart.** One facility, its head office, registered under supplier subparts OO and QQ because it imports pre-charged refrigeration equipment, with `co2e_emission` null in every row from 2012 to 2023. That is a verifiable statement about the reporting regime, not about the company's physics.

## 7. "You cherry-picked companies to make the point." — CORRECT, AND WE SAY SO FIRST

**Answer:** Yes, deliberately. The six were selected to span the contestation axis, not sampled at random: a retailer with no disclosed number, a steelmaker whose emissions sit in its own furnaces, a bank with zero rows, an automaker whose footprint is customers driving. Selecting extreme cases is the right design for demonstrating a **mechanism**. It would be the wrong design for estimating **prevalence**, which is why we do not estimate prevalence.

## 8. "Ford's 497,625 t covers only 10 of its 16 GHGRP facilities." — CORRECT

**Answer:** Stated on the slide. Six Ford facilities return null. So Ford's disclosed figure is a floor even within the US regime, which strengthens rather than weakens the argument.

## 9. "You applied a 2022-dollar factor to 2023 revenue." — CORRECT

**Answer:** Not deflated. Roughly a 3% effect, disclosed in the caveats, and far smaller than the effects we are measuring (4.7× to 85×). One line of code to fix and we will state it rather than hide it.

## 10. "This is a critique of ESG, not a sustainability framework. You did not answer the challenge." — THE SHARPEST ATTACK

**Answer:** It is a framework, and a strict superset of what a single score provides. Per company it outputs:

- a **consensus score** (the median across defensible methods) — this is the score the challenge asked for
- a **contestation figure** (how far it moves) — this is the part nobody else provides

Anyone wanting one number can take our consensus and ignore the rest. We deliver the requested ranking **and** the honest error bar around it. Dropping the second number would not make it more of a framework; it would make it a less honest one.

---

## The three things to say first, before anyone attacks

1. **"Nucor is the dirtiest company in our sample. So is Walmart. Both statements come from the same government data, the same year, and two different defensible conventions."**
2. **"Every number on this slide came from free government APIs. Nothing is licensed, nothing is scraped, nothing is estimated by us beyond the EPA's own published factors."**
3. **"Our disclosed figures are floors, our modelled figures are screening estimates, and we will tell you which is which for every number."**

Volunteering the limitations is what the rubric rewards. Getting caught hiding one is what it punishes.
