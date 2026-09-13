---
edit: owned
last_edited: 2026-09-12T11:21:45 CET
changes: 0
type: reference
status: active
---
# Aggregate Confusion: the paper this project stands on

Everyone on the team reads this page before writing code. It is the intellectual spine of the submission and it is what makes our angle defensible in front of this specific jury.

## The paper

**Berg, Kölbel and Rigobon, *Aggregate Confusion: The Divergence of ESG Ratings*.** Review of Finance, 2022. Runs out of the [Aggregate Confusion Project](https://mitsloan.mit.edu/sustainability-initiative/aggregate-confusion-project) at the MIT Sloan Sustainability Initiative. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3438533)

## The finding

Five major ESG rating agencies (KLD, Sustainalytics, Vigeo-Eiris, Asset4, RobecoSAM) correlate with each other at an average of **0.61**.

Credit rating agencies correlate at **0.99**.

Moody's and S&P agree on whether a company will repay its debt. Nobody agrees on whether a company is sustainable.

## The decomposition

They split the disagreement into three causes and measure each.

| Cause | Share | What it means |
|---|---|---|
| **Measurement** | 50.1% | Same concept, different indicator. "Labour practices" as staff turnover for one agency, as lawsuit count for another. |
| **Scope** | 36.7% | Different lists of what even counts. One includes lobbying, another excludes it. |
| **Weight** | 13.2% | Same items, different importance assigned. |

**The thing everyone gets wrong:** they assume the argument is about weights. Weights are the smallest cause, 13%. Over half the disagreement is people measuring the same word differently, and another third is disagreeing about what belongs in the word at all.

This is why "we picked 40/30/30 weights" is the weakest possible hackathon answer. It is arguing about the 13%.

## Why this jury specifically

- **MIT judge.** This paper is MIT Sloan's flagship work on exactly this question. The Aggregate Confusion Project is a named MIT Sloan initiative.
- **Two ETH judges.** Julian Kölbel, second author, was a postdoc at [ETH Zurich's Group for Sustainability and Technology](https://sustec.ethz.ch/people/alumni/post-docs/dr--julian-koelbel.html) and is now a professor at St. Gallen. The ETH sustainable-finance world knows this paper cold.
- **Julius Bär judge.** Their published [sustainable investment framework](https://www.juliusbaer.com/fileadmin/legal/julius-baer-esg-investment-framework-en.pdf) buys ratings from **both MSCI and Sustainalytics**, stating in writing that this is to "minimise bias, mitigate tail risk and address issues arising from lack of market standards," and warns that provider data "may turn out to be incomplete or outdated" with no universally accepted framework. A bank paying twice for the same signal because it trusts neither source. That judge lives this problem daily.
- **Citadel.** A hedge fund and a market maker that sells no ESG product. They are not in the room to hear that sustainability matters. They are there to see whether a defensible estimate can be built out of messy data.

## What we take from it

We do not need to buy rating data to use this result. We reproduce the phenomenon ourselves: build our own score at several honestly-defined scope boundaries and show how violently the S&P 500 ranking moves between them.

Citation discipline: cite the paper once in the deck, correctly, and do not overclaim it. Attributing our own finding to them, or misstating the 0.61, is worse than not citing it.
