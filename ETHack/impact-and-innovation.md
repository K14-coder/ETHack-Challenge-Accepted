---
edit: owned
last_edited: 2026-09-12T13:56:49 CET
changes: 0
type: project-note
status: active
---
# Impact and Innovation

Direct answers to two of the five judging criteria. Written to survive Q&A, not to sound impressive.

## The one-liners, for the slide

**Impact.** $3.7 trillion sits in sustainable funds. Nobody can manually check 500 companies, but anyone can check 60. We say which 60.

**Innovation.** Every other approach tries to build a better score. We refuse to build one, and publish how much the score depends on its own conventions instead. The incumbents cannot do this, because confidence is the product they sell.

## Impact

### The number

**$3.7 trillion** in global sustainable fund assets at the end of Q2 2026. Europe $3.1tn (84%), US $398bn (11%). Source: Morningstar Q2 2026 global sustainable fund report.

That capital is allocated using scores that, as the MIT work showed, correlate at 0.61 between providers. Nobody currently publishes which companies those providers disagree about.

### The reframe: this is a triage tool

The scarce resource in this industry is not data. It is **analyst attention.** No allocator can do bottom-up diligence on 500 companies. Every one of them has to decide where to spend a limited number of analyst hours.

Contestation is exactly that allocation rule. Skip the robust names, where every defensible method agrees. Spend the hours on the contested ones, where the published number is a convention choice. **That is a cost decision, today, with a number attached.**

### Four named users and the decision each one changes

| User | Their problem today | What changes |
|---|---|---|
| **Asset allocator** | Julius Bär's published framework buys ratings from **both** MSCI and Sustainalytics, stating in writing that it is to "minimise bias, mitigate tail risk and address issues arising from lack of market standards". They already know the providers disagree. They have no list of **which companies** and **why**. | Contestation is that list, ranked, for the whole index. Diligence budget goes where the disagreement is. |
| **Regulator** | CARB receives the first mandatory US Scope 1+2 filings on **10 Nov 2026** and must then write rules on boundaries, consolidation and estimation. Which convention to standardise first is currently a judgement call. | The variance decomposition says which choices actually move rankings. Standardise the high-variance conventions first. Prioritised rulemaking instead of guesswork. |
| **The company itself** | A high-contestation company carries regulatory and reputational exposure it cannot see, because its own rating looks fine under the convention currently in use. | The output names the specific disclosure that would collapse its own spread. Actionable, and cheap relative to the exposure. |
| **Retail ESG fund buyer** | Owns a fund whose holdings were selected by one convention out of seventy-two, and has no way to know that. | Can see whether their fund's holdings are robust or contested. |

### The honest societal claim

We do not make any company cleaner. Overclaiming that is how this loses points.

What we do is make the measurement honest, and an honest measurement creates a **private incentive to disclose**. A narrow spread becomes commercially valuable, because risk-averse capital prefers it. A company can narrow its own spread only by disclosing more.

That is a mechanism, not a hope: **you do not need a mandate if transparency is priced.** State it at that level and it holds up.

## Innovation

### Say plainly what is not ours

Claiming too much here is the fastest way to lose the criterion in Q&A.

- **Not new:** that ESG ratings diverge. Berg, Kölbel and Rigobon established and quantified it (2022).
- **Not new:** specification curve analysis. Simonsohn, Simmons and Nelson (2020), built for metascience.
- **Not new:** input-output estimation of corporate footprints. Standard practice, and EPA publishes the factors.
- **Not new:** sensitivity analysis as a concept.

### What is ours

1. **The join.** Specification curve analysis has never been applied to ESG scoring. One field has the disease, another field has the cure, and nobody has connected them.
2. **Contestation as a shipped per-company output.** Not an appendix, not a robustness footnote. A second number published beside the score, for all 500, with a verdict attached.
3. **Replication from free data.** The MIT decomposition used proprietary rater data. We reproduce the same *kind* of decomposition on a live public index using only government sources, which means anyone can check us and anyone can rerun it.

### The strongest argument: nobody whose job it is can do this

This is the answer to "would a team have arrived here without thinking hard?"

**MSCI and Sustainalytics cannot publish contestation.** Their product is one authoritative number. Confidence *is* the thing being sold. Publishing "here is how much our rating depends on conventions we chose ourselves" destroys the product.

**Academics documented the problem but do not ship an index.** They produce papers on samples, not a maintained per-company output on live data.

So the gap is not intellectual difficulty. It is **incentive**. The people with the data cannot say it, and the people who can say it do not maintain a product. A student team with no revenue to protect is structurally the right party to do it.

That is also why the obvious move is a better score, and the non-obvious move is refusing to build one.

### Two design properties worth naming

**Bad data strengthens the result.** In almost every data project, patchy data weakens the finding. Here poor disclosure widens contestation, and contestation is the finding. There is no data outcome that kills it. That inversion is a property of the design, not luck.

**We refuse to argue about weights.** Weights are 13.2% of why ratings diverge. Scope is 36.7% and measurement is 50.1%. Every other team in the room will spend the day on the 13%. We attack the 87%.

## Sources

- [Morningstar Q2 2026 global sustainable fund report summary](https://www.todayesg.com/morningstar-2026-q2-global-sustainable-fund-report/)
- [Julius Baer Sustainable Investment Framework](https://www.juliusbaer.com/fileadmin/legal/julius-baer-esg-investment-framework-en.pdf)
- Divergence and decomposition: [[Efforts/Active/ETHack/aggregate-confusion|aggregate-confusion]]
- The 10 Nov 2026 date: [[Efforts/Active/ETHack/data-landscape|data-landscape]]
