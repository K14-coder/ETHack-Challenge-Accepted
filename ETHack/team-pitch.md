---
edit: owned
last_edited: 2026-09-12T12:21:47 CET
changes: 0
type: project-note
status: active
---
# Pitching the idea to the team

How to explain specification curve analysis to four people who have never heard of it, in a noisy room, and get a yes. Design lives in [[Efforts/Active/ETHack/framework|framework]].

Rule: tell the story before the method. Nobody adopts a method they have not first felt the need for.

## The one-liner, for the group chat

> Every team here will build a weighted ESG score and get destroyed on "why those weights". We build the opposite: we run every defensible scoring method at once and report which companies' rankings survive and which ones are just an artifact of somebody's methodology. There is a Nature paper for this and nobody has ever done it to ESG.

## The 90 seconds, out loud

Say it roughly like this. Do not read it.

---

Here is the problem with what we are all about to build.

Every team in this room picks three or four metrics, weights them, ranks the S&P 500. Then a judge from Citadel asks "why 40% and not 25%", and nobody has an answer, because there isn't one.

So, a story. In 2018, twenty-nine teams of researchers, sixty-one analysts, were handed the identical dataset. Same 146,000 rows. Same question: do referees give more red cards to dark-skinned players? Twenty teams found yes. Nine found no. The effect sizes ran from 0.89 to 2.93.

Same data. Every team competent. Every team honest.

That is not a story about bad researchers. It is a story about the fact that analysis contains choices, and the choices moved the answer more than the data did.

The fix has a name. Specification curve analysis, Nature Human Behaviour, 2020. Instead of picking one way to analyse, you enumerate every defensible way, run all of them, and report the distribution instead of a number.

Now: ESG ratings have exactly this disease. MIT proved it. The major rating agencies correlate at 0.61 with each other. Credit rating agencies correlate at 0.99. And nobody has ever applied the specification curve fix to ESG.

So here is what I want us to build. Sustainability is environmental damage per unit of value produced. Four choices go into computing that: where you draw the emissions boundary, what you divide by, what you do with missing data, and whether you compare within an industry or across all of them. Thirty-six defensible combinations. We run all thirty-six, on all five hundred companies.

Every company gets two numbers. Where it lands on average, and how far it moves.

Companies that barely move are genuinely clean or genuinely dirty. Companies that swing three hundred places are companies where the ESG number is an artifact of somebody's choice, not a fact about the company.

That is the finding. Not a ranking. A map of where the ranking is real and where it is noise.

And the reason I want this one specifically: if our data turns out to be patchy, we still win. Bad data widens the spread, and the spread is the result. There is no version of tomorrow where we have nothing to show.

---

## The objections, and the answers

They will come in roughly this order.

**"Isn't this just sensitivity analysis?"**
Sensitivity analysis is an appendix where you check your answer did not move. This makes the movement the headline. And it has a name and a Nature paper, which matters when two academics are on the panel.

**"Thirty-six rankings is thirty-six times the work."**
No. It is one scoring function with four parameters, called in a loop. Identical code, plus a for-loop. The work is the data pipeline, and that is the same either way.

**"Are we dodging the challenge? They asked for a framework that scores companies."**
We score companies. We score them thirty-six times. It is a strict superset of what every other team delivers, plus the one thing none of them deliver.

**"Three minutes is too short for something this complex."**
One sentence and one chart. "There is no ESG score, there is a distribution, here is how wide it is." The chart carries the rest. Complexity in the method is fine, the *claim* is simple.

**"What if we cannot get Scope 3 data?"**
Then coverage is poor, contestation rises, and that is the finding. We can also drop to eighteen or nine specifications and nothing about the framework changes.

**"Won't they think we avoided the hard problem?"**
The choice *is* the hard problem. Everyone else will spend today arguing about weights, which is 13% of why ESG ratings disagree. We are attacking the other 87%.

## If someone wants a second, shorter analogy

Two doctors, same X-ray. One measures the tumour at its widest point, one measures the average across slices. Both are standard practice. They report different sizes. Nobody is lying. If all you see is the final number, you cannot tell which convention produced it, and you cannot tell how much the answer would have changed under the other one.

ESG ratings are that, at industrial scale, with money attached.

## What you are actually asking them to agree to

Be explicit, or they will nod and then relitigate at hour six.

1. We do not publish a single ranking. The distribution is the deliverable.
2. We restrict to environmental only, and we defend that choice rather than apologise for it.
3. We write one parameterised scorer, not four people's separate notebooks.
4. Slides start at hour zero, not hour twenty.

## Citations, verified

- Silberzahn, R. et al. "Many Analysts, One Data Set: Making Transparent How Variations in Analytic Choices Affect Results." *Advances in Methods and Practices in Psychological Science*, 2018. 29 teams, 61 analysts, 146,028 player-referee dyads, odds ratios 0.89 to 2.93, 20 of 29 found a significant effect.
- Simonsohn, U., Simmons, J. P., Nelson, L. D. "Specification Curve Analysis." *Nature Human Behaviour* 4, 2020.
- Berg, F., Kölbel, J. F., Rigobon, R. "Aggregate Confusion: The Divergence of ESG Ratings." *Review of Finance*, 2022. Average inter-rater correlation 0.61 across five agencies.
