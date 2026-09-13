---
edit: owned
last_edited: 2026-09-12T11:21:45 CET
changes: 2
type: project-note
status: direction-set
---
# Idea

Challenge is known, see [[Efforts/Active/ETHack/challenge|challenge]]. Lock the idea by T+1h after team forming. After that this file records decisions, it does not reopen them.

## One sentence

> We build ___ so that ___ can ___ .

If it does not fit in one sentence, it is not scoped yet.

## The judge's question

What does a judge see in the first 30 seconds that makes them lean forward?

## The trap

Every team in the room will build a weighted ESG score. Pick three indicators, normalize them, weight them 40/30/30, put them on a bar chart, rank the S&P 500. That lands at 2 or 3 on Innovation and invites the one question nobody can answer: **why those weights?** A Citadel judge asks that in the first ten seconds of Q&A.

The differentiator is not better weights. It is having something to say about the weights themselves.

## Candidate angles

My proposals, not decisions. Kill each one explicitly so it does not come back at hour 15.

| # | Angle | Why it could win | Risk |
|---|---|---|---|
| 1 | **Disagreement as the product.** Do not publish a 7th score. Measure how much existing ESG ratings disagree on the same company, decompose the disagreement into scope, measurement and weight components, and show which companies are genuinely ambiguous. Known result: major raters correlate only around 0.5 (Berg, Kölbel, Rigobon, *Aggregate Confusion*, Review of Finance 2022, MIT Sloan). A MIT judge is on the panel. | Needs at least two rating sources. If ratings data is paywalled this dies. Check feasibility in the first 30 minutes. |
| 2 | **Transition risk, not virtue.** Score each company by exposure to an abrupt net-zero shock: carbon intensity times a shadow carbon price, against margin and balance-sheet headroom. Output is expected earnings impairment, in dollars, not a letter grade. | Speaks Citadel's language. The bonus question then falls straight out of the framework instead of being a separate opinion. | Needs emissions data plus financials joined per ticker. Assumption-heavy, so the sensitivity analysis is mandatory. |
| 3 | **Uncertainty-first scoring.** Same as a normal score but every company carries an error bar derived from disclosure quality and data coverage. Rank with confidence intervals. Refuse to rank companies whose intervals overlap. | Directly targets "honest about limitations" in the rubric. Intellectually honest in a room full of point estimates. | Reads as modest unless the visual sells it. Needs one great chart. |
| 4 | **Say vs do.** Gap between what companies claim in sustainability report and 10-K language and what the hard numbers show. NLP on EDGAR filings against reported emissions and validated SBTi targets. | Demo-friendly, immediately legible, a named greenwashing gap is a headline. | Text pipeline in 24h is a time sink. Only if someone on the team has done EDGAR text work before. |

**Strongest combination for this panel:** 2 as the spine, 3 as the honesty layer, and the bonus answered as a direct output. 1 is the highest-ceiling play if and only if two independent rating sources turn out to be reachable inside the first hour.

## Direction set (Aram, 12 Sep, pre-team)

Angle 1 and 3 fused, driven by Aram's own definition of sustainability: **a company is sustainable if it does little environmental damage right now.** Background and jury reasoning in [[Efforts/Active/ETHack/aggregate-confusion|aggregate-confusion]].

The move: the weak point of a present-damage definition is the **boundary of "damage"**. Count only what a company burns itself and every software firm and bank looks spotless while financing the oil field. That boundary question is not a flaw in the definition, it is the most interesting thing about it, and it is 36.7% of why the world's rating agencies disagree with each other.

So we do not publish a better score. We publish the same honest score computed at several defensible boundaries, and show how violently the S&P 500 ranking moves between them.

**Key de-risking property:** this does NOT require buying MSCI or Sustainalytics data. We reproduce the divergence phenomenon ourselves from free emissions and financial data. Angle 1's paywall risk is removed.

**Still open before lock:**
- [ ] Does "damage" include suppliers and customers using the product (Scope 3)? Gates the data requirement.
- [ ] How many boundary definitions do we run? Three is probably the limit in 24h.
- [ ] Who is the named user of the output: allocator, regulator, or the company itself?

**What it does:**

**Who it is for:** name a specific allocator, regulator or company. Not "society".

**Why it fits the challenge:** map it onto the five criteria in [[Efforts/Active/ETHack/challenge|challenge]], one line each.

**Why it is not obvious:**

## Data sources to check first

Verify each in the first 30 minutes. Anything not returning rows in 45 minutes gets dropped, no negotiation.

| Source | Gives | Free? | Verify |
|---|---|---|---|
| Wikipedia S&P 500 constituents | ticker list, sector (GICS) | yes | trivial, do this first |
| `yfinance` | financials, market cap, sector, sometimes an ESG risk field | yes | the sustainability endpoint has been unreliable, test it immediately |
| SEC EDGAR XBRL company facts API | audited financials per CIK, no key needed | yes | ticker to CIK mapping file is published by SEC |
| EPA GHGRP | US facility-level reported GHG emissions | yes | facility to parent-company mapping is the hard part |
| Climate TRACE | asset-level emissions estimates, global | yes | coverage and company attribution vary by sector |
| SBTi target dashboard | which companies have validated near-term and net-zero targets | yes, CSV | good binary signal, cheap to join |
| CDP | self-reported scope 1/2/3 | mostly paywalled | do not build the spine on it |
| MSCI / Sustainalytics / LSEG | rating scores | paywalled | needed for angle 1, check early or kill angle 1 |
| Kaggle S&P 500 ESG datasets | prepackaged scores | yes | often scraped and stale, fine as a *comparison* input, never as ground truth |

Rule: **one canonical join key**, the ticker, normalized once, in one place. Most of the lost hours in this kind of hack come from three people joining on three different spellings of a company name.

## Scope: in and out

**In the demo path (must work):**
- 
- 
- 

**Faked or hardcoded (admitted in the pitch):**
- 
- 

**Explicitly out (do not build, even with time left):**
- 
- 

## Stack

Five people, 24 hours, one repo. Suggested split. Fill the names.

| Layer | Choice | Owner | Note |
|---|---|---|---|
| Data acquisition | python, requests, pandas | | owns the ticker key and the raw data folder |
| Scoring / methodology | python, numpy | | owns the defensibility of every indicator |
| Sensitivity / validation | python | | owns the error bars and the "what if the weights change" chart |
| Visual output | matplotlib or a small Streamlit app | | one hero chart beats a dashboard |
| Slides + pitch | PowerPoint, `.ppt` | | starts at hour 0, not hour 20 |

Repo rule: raw data committed or cached to disk, every number in the deck reproducible by one script. They said they will read the code.

## Risks

| Risk | Blast radius | Mitigation | Kill-by |
|---|---|---|---|
| Rating data paywalled, angle 1 impossible | loses the strongest innovation play | test access first thing | T+0:45 |
| Emissions data does not map cleanly to tickers | the whole spine | fall back to disclosed intensity from filings for a subset of the index, say so honestly | T+3h |
| Five people editing one notebook | lost hours, merge hell | one repo, modules not notebooks, one owner per file | continuous |
| Scope creep into a dashboard | eats the pitch prep | dashboard is explicitly optional, slides are compulsory | T+14h |
| `.pptx` rejected because `.ppt` was required | automatic disqualification from the final deck | ask the organizers now, export both | T+2h |

## Scope cuts made

Append with the time.

- 
