# Q&A prep

**One page. Read it twice before you go up.**

---

## The posture, which matters more than any single answer

**You are not defending a paper. You are reporting tests.** Most teams answer a
criticism with an argument. You answer with a rerun. That is the whole
difference, and it is why conceding fast makes you look stronger, not weaker.

Three rules:

1. **Lead with the number.** "We reran it. Zero places." Then explain. Never the
   reverse.
2. **Concede in one sentence, then pivot to what you did.** "You are right, and
   here is the rerun." A judge who lands a hit and watches you produce the fix
   has just learned you are rigorous. A judge who lands a hit and watches you
   argue has learned the opposite.
3. **When you do not know, name the test.** "We did not run that. It is first on
   the roadmap and it takes about an hour: place Bloomberg's own score inside our
   distribution." Naming the experiment proves you understand the gap. Waffling
   proves you do not.

**The thing that will sink you is hedging.** Not being wrong. Being vague.

---

## Say these three things before anyone asks

Volunteering a weakness costs you nothing and buys you the room.

1. **"The weighting slider is the part everyone argues about and it explains six
   percent of why raters disagree. We vary it anyway, and it moves the median
   company three places. We report that rather than assuming it away."**
2. **"Level and change are different questions. If you pool them the headline
   reads seven places, which is barely below a random ranking. We refuse to pool
   them, and the honest number is three."**
3. **"We had a Bloomberg Terminal and did not put Bloomberg's own score inside our
   distribution. That is the single most valuable test we did not run."**

---

## The eight most likely questions

### 1. "Why 18 energy companies when the brief says S&P 500?" *(near certain)*

> Because comparability is per sector and we would rather cover one sector
> honestly than 500 badly. Bloomberg builds its materiality map per peer group,
> which is why only three environmental fields are reported by all 18 of ours;
> across sectors that number goes to zero. The machinery is sector-agnostic and
> runs in 18 seconds, so scaling is an evening of parent-name matching, not a
> redesign. What we will not do is claim a cross-sector ranking we cannot
> support.

**Trap:** do not answer with runtime or API counts. That reads as dodging.

### 2. "Name your environmental indicators. Where is Scope 3?" *(near certain)*

> Thirty-seven environmental fields, all listed in Exhibit 3. Scope 1 is F0947,
> reported by 15 of 18. Methane is SA055, percent of Scope 1, reported by 12.
> **Scope 3 is absent from all 138 fields and that is the single largest gap in
> this framework for an oil and gas universe.** Bloomberg's ES map for these peer
> groups does not carry it. We say so on page 5 rather than hoping nobody checks.

**Trap:** never say "whatever Bloomberg's map contained." Own the selection.

### 3. "Isn't the spread just an artefact of your grid?" *(the kill shot)*

> We asked that first, which is why we do not pool. Level and change are
> different questions, not rival methods. Pooled, the median reads seven places.
> Scored separately it is **five against sector peers and three within BECS
> groups.** Against the random-rank control, a randomly ordered company would
> show 8.5 to 9. Three is well inside that. **The spread survives its own
> deflation, which is the only version of the claim worth making.**

### 4. "Where does Bloomberg's own score fall in your distribution?" *(we cannot answer)*

> We did not run it. It is the best test of our central claim and it needs one
> Terminal pull plus twenty lines of code. It is first on the roadmap in Appendix
> F. If it falls outside our interquartile range, our grid is missing a
> convention Bloomberg uses and we would want to know which.

**Trap:** do not invent a guess. Naming what a failure would teach you is the
strong move.

### 5. "What is your definition of sustainability?" *(brief requires it)*

> A company is sustainable to the degree that it **produces its output with less
> irreversible harm than the peers producing the same output, and holds a balance
> sheet capable of surviving the transition required to keep doing so.** Three
> consequences, all testable: harm is per unit of exposure, the comparison is to
> peers making the same product, and financial resilience counts because a
> company in distress cuts abatement capex first.

### 6. "Allocate the $1 billion." *(bonus, and they will ask)*

> We tested the premise first. The market thesis is that crossing an ESG
> threshold unlocks capital. **On our data there is no threshold: 15 of 18
> companies sit between 20% and 80% likely to pass a top-half screen.** So the
> tradeable number is not crossing a line, it is the gap between where a company
> stands and where it is heading. MPC is 0.12 on level and 0.73 on change.
> Long that gap, short the structurally stuck, exit when the gap closes because
> Pástor shows green assets earn lower expected returns once repriced.

### 7. "All 18 companies come out as 'opinion'. What did you actually tell me?" *(Julius Bär)*

> Under the full grid, yes, and that was itself the finding. Within one question
> it separates: **33 of 153 pairwise comparisons hold under essentially every
> method, and 56 once you raise the evidence bar.** That is the deliverable. Not
> a league table that asserts all 153 comparisons, but a map of which
> comparisons the evidence can carry. An allocator can act on 33 and knows to
> stop at the rest.

### 8. "Why would I use this instead of an MSCI rating?" *(the commercial question)*

> You would use it **with** one. We give you the consensus, which is the number
> MSCI gives you, plus how much of it is a choice, plus which choice decides it,
> plus which missing disclosure would settle it. Anyone who wants one number
> takes our median and ignores the rest. What nobody else ships is the error bar,
> and an engagement team can act on the remedy column tomorrow.

---

## Quick-fire, if they go technical

| They ask | You say |
|---|---|
| Production denominator invalidates a third of the grid? | No. Non-producers keep Social, Governance and Financial and lose only Environment. **All 18 are still ranked in every production cell.** Verified in code. |
| Is the spread just the Financial pillar switching off? | Zeroing the financial weight moves direction from **18.2% to 15.0%**. About 3 points of 18 is the pillar toggle. Right in kind, wrong in magnitude. |
| How many of the 17,496 are distinct? | 648 grade paths collapse to **606 distinct**, Kish effective N **574**. A 6.5% inflation, and we quote effective cells now. |
| Isn't contestation just thin data? | Partly. Coverage against contestation is **−0.38**. But it is not monotone in group size: the two-member group has the **lowest** contestation, 6.0, and the three-member groups the highest, 7.7. |
| Why EBITDA and not revenue? | It is our weakest input choice, so we tested it rather than defend it. Reran the whole grid on SEC XBRL revenue: **median shift 0.0 places, max 1.0.** The choice does not change the answer. |
| Do weights matter? | Yes. They move the median company **3.0 places** and WMB **6.0**. That is why we vary them instead of arguing from the central limit theorem that they cannot matter. |
| Your 95% cut-off is arbitrary. | Settled pairs by threshold: 7 at 0.999, 12 at 0.99, 33 at 0.95, 51 at 0.90, 79 at 0.80. Monotone, no cliff at our cut-off. |
| Why 138 fields and not the 139 in the registry? | **DX831**, a governance field that no company in the universe reports. It is in Bloomberg's map and carries no data, so it is excluded and the model runs on 138. |
| Isn't rating uncertainty already studied? | Avramov and co-authors measure dispersion **across six providers**. Ours is within one dataset across method choices, which isolates construction from data differences. Different object, and we say so. |
| Doesn't more disclosure increase disagreement? | Christensen, Serafeim and Sikochi find exactly that, **between raters with different frameworks**. We measure ambiguity within one framework from a missing input. Both can be true. |

---

## Three answers that will lose you points

- **"It's in the companion section."** Never. Answer, or say you did not run it.
- **"We acknowledge the cells aren't independent."** Acknowledging is not
  answering. Give 606 of 648.
- **"The brief was ambiguous."** True and irrelevant. Give your definition.

---

## If you are truly stuck

> "I do not have that number. Here is what I would run and what it would tell
> us."

Then say it in one sentence and stop talking. Silence after a clean concession
reads as confidence. Filling it reads as panic.
