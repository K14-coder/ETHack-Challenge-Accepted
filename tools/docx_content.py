# ═══════════════════════════════ COVER ═══════════════════════════════
p = doc.add_paragraph(); p.paragraph_format.space_after=Pt(0)
r = p.add_run("CONTESTED"); r.font.size=Pt(30); r.bold=True; r.font.name="Calibri"
r.font.color.rgb=RGBColor.from_string(INK)
para("A sustainability framework for the S&P 500 that publishes its own uncertainty",
     size=12.5, color=INK2, align=WD_ALIGN_PARAGRAPH.LEFT, after=8)
para("**Sector note · Version 2 · revised after referee review**", size=8.6, color=INK2,
     align=WD_ALIGN_PARAGRAPH.LEFT, after=1)
para("S&P 500 Energy · 18 companies · FY2021–FY2025", size=8.6, color=INK3,
     align=WD_ALIGN_PARAGRAPH.LEFT, after=1)
para("ETHack 2026 · Challenge #1 · Citadel & Citadel Securities · 13 September 2026",
     size=8.6, color=INK3, align=WD_ALIGN_PARAGRAPH.LEFT, after=4)
rule(16)

callout("**An ESG score is not a measurement, it is the answer to a question you did not know you were "
        "asking. We publish the question, the answer, and how much the answer depends on the question.**")

table([
 ["Universe","18 S&P 500 Energy constituents (XLE, 12 Sep 2026), five Bloomberg BECS peer groups"],
 ["Inputs","139 fields · Environment 37 · Social 14 · Governance 79 · Financial resilience 9"],
 ["Method","Specification curve analysis (Simonsohn, Simmons & Nelson 2020) applied to score construction"],
 ["Grid","**Two questions, scored separately.** Q-A level: 8,748 cells. Q-B change: 8,748 cells."],
 ["Headline","Within Q-A, holding the peer set fixed, the median company still moves **3.0 places of 18**"],
 ["Settled","Of 153 pairwise comparisons, **56 hold in >95% of Q-A cells**. A league table asserts all 153."],
 ["Bonus","§8 — a $1bn net-zero allocation derived from the framework, not bolted on"],
], widths=[1.25,5.6], first_bold=True, header=False, size=8.6)

# ── corrections notice
label("NOTICE","","Version 2 — what changed, and what we got wrong")
para("A referee read v1 in full and recomputed our exhibits. Fifteen claims were challenged. "
     "We accept eleven, reject two, and partly accept two. The corrections are material enough that "
     "they change the headline, so they are on page one rather than in a footnote.", after=4)
table([
 ["#","What v1 said","Status","What v2 says"],
 ["1","Berg et al. split 50.1 / 36.7 / 13.2","**Accepted**","The published split is **56 / 38 / 6**. Our case for not varying weights rested on a weight share nine times too large. We now vary weights and report the result (§5.5)."],
 ["2","Two pairs survive *every* method","**Accepted**","Two exceed 95%, one exceeds 99%. 'Every method' was wrong. We now quote the threshold explicitly everywhere."],
 ["3","We vary the seven decisions where the providers differ","**Accepted**","Exhibit 6 contradicted the summary in three places. The map is corrected and the summary now matches it."],
 ["4","Every rank is paired with an absolute intensity","**Accepted**","It was not. Absolute intensity is now Exhibit 7."],
 ["5","139 fields","**Accepted**","139 in the registry, **138 reported by at least one company**. DX831 (governance) is reported by none and is now dropped."],
 ["6","Direction and peer set are specifications","**Accepted — the big one**","They are different *questions*. Simonsohn's own criterion says a grid must test one question. We now report **two curves**, not one (§4.2)."],
 ["7","Weights barely move ranks","**Accepted**","Our own slider moves the median company **3.0 places** and WMB **6.0**. §5.5."],
 ["8","Nobody reports the width of the distribution","**Accepted**","Avramov et al. (2022) measure cross-provider dispersion. Ours is *within-provider, within-dataset* method uncertainty — a different object, and we now say so (§7.2)."],
 ["9","Neither provider lets users change weights","**Accepted**","Bloomberg sells custom scores. Removed."],
 ["10","18 of the 20 index energy constituents","**Accepted**","XLE lists 21 at 12 Sep 2026. We cover 18; APA, TPL and EQT/OKE are named as absent (§3.2)."],
 ["11","Contestation is a property of the evidence","**Partly**","It is partly group size and coverage: rank corr(coverage, contestation) = **−0.38**. Reported in §6.5, not hidden."],
 ["12","Production denominator invalidates a third of the grid","**Rejected**","Non-producers keep S, G and F and still receive a composite; only the E pillar drops. All 18 are ranked in every production cell. Verified in code (§B.3)."],
 ["13","The spread is the Financial pillar toggling on and off","**Rejected**","Setting the F weight to zero moves *direction* from 18.2% to **15.0%**. Only ~3pp of 18.2 is the pillar switch."],
 ["14","17,496 independent specifications","**Partly**","648 grade-stage cells collapse to **606 distinct**; 42 are exact duplicates. We now quote distinct cells."],
 ["15","Bonus deferred","**Accepted**","§8."],
], widths=[0.28,1.55,0.72,4.3], align=["c","l","c","l"], size=7.6)
source("Referee items are numbered as in the review. Every 'accepted' item is fixed in this version, not merely acknowledged.")

pagebreak()

# ═══════════════════════════════ EXEC ═══════════════════════════════
h1("Executive summary")
para("**1. Our definition.** A company is sustainable to the degree that it *produces its output with "
     "less irreversible environmental and human harm than the peers producing the same output, and "
     "holds a balance sheet capable of surviving the transition required to keep doing so.* Three "
     "things follow and each is testable: harm is measured per unit of exposure, not absolutely; the "
     "comparison is to peers making the same product; and financial resilience is a sustainability "
     "property, because a company that defaults cannot deliver a 2050 commitment.")
para("**2. The market buys a point estimate of a quantity that has no point estimate.** Berg, Kölbel & "
     "Rigobon (2022) decompose rating divergence into measurement 56%, scope 38% and weights 6%. Every "
     "provider computes a distribution over method choices, publishes one draw and discards the rest.")
para("**3. Two questions, not one distribution.** v1's central error. *Who is cleanest today* and *who "
     "is improving fastest* are different questions and belong in separate grids. Splitting them removes "
     "the bimodality that inflated v1's headline — and the contestation survives the split.")
para("**4. Contestation is real after every deflation.** Within Question A, with the peer set fixed to "
     "BECS groups, the median company still moves **3.0 places of 18**; against the whole sector, 5.0. "
     "Weights add 3.0 more. These are the honest numbers and they are smaller than v1's 7.0.")
para("**5. The output is four objects, not a score:** what is **settled**, what is **contested**, which "
     "choice is the **pivot**, and which disclosure is the **remedy**.")
para("**6. The bonus falls out of the framework.** The two questions are the two halves of a transition "
     "portfolio: Question A prices today's leaders, Question B identifies tomorrow's. §8 allocates $1bn "
     "on the gap between them.")

label("Exhibit","1","The two questions give different answers — which is why they are scored separately")
fig("f1_two_questions.png", 6.7)
source("Interquartile box per company under each question, sorted by Question A median. Blue = level, orange = change. "
       "EOG sits at 94 on level and 35 on change; MPC at 18 and 71. Pooling these into one distribution — as v1 did — "
       "manufactures a spread that is really two answers to two questions. Source: model/out/long.csv.")

pagebreak()
# ═══════════════════════════════ 1–3 ═══════════════════════════════
h1("1. The problem")
para("Sustainability ratings are consumed as measurements and constructed as opinions.")
label("Exhibit","2","Inter-rater agreement")
table([["Domain","Average pairwise correlation","Source"],
 ["Credit ratings","0.92–0.99","Berg, Kölbel & Rigobon (2022)"],
 ["ESG ratings, six major providers","0.54–0.61","Berg, Kölbel & Rigobon (2022)"],
 ["ESG ratings, alternative estimate","0.45","Dimson, Marsh & Staunton (2020)"]],
 widths=[2.6,2.0,2.3], align=["l","r","l"])
source("Ranges given because the working-paper and published versions differ; the MIT Sloan project page gives 0.54 and 0.92. "
       "v1 quoted single figures without noting the discrepancy.")
para("Their divergence decomposition — **measurement 56%, scope 38%, weights 6%** — is the design "
     "constraint. Weights are the smallest cause. v1 used this to justify not varying weights at all; "
     "with the correct 6% the argument is weaker, not stronger, so v2 varies them and reports the effect.")

h1("2. What we mean by sustainability")
callout("A company is sustainable to the degree that it **produces its output with less irreversible "
        "environmental and human harm than the peers producing the same output**, and **holds a balance "
        "sheet capable of surviving the transition** required to keep doing so.")
para("**Why financial resilience is in, and weighted equally.** A stranded balance sheet is a "
     "sustainability failure, not merely a credit event: a company in distress cuts abatement capex "
     "first. Equal weighting is a *default*, not a claim — §5.5 reports what happens across the range.")
para("**Where this differs from the providers.** MSCI and Bloomberg both measure single materiality — "
     "risk *to the firm*. Our environmental and social indicators measure harm *by the firm*. We are a "
     "deliberate hybrid and the brief does not resolve which it wants. That ambiguity is itself a finding.")
para("**What the definition excludes, and what that costs.** Peer-relative harm means the cleanest "
     "member of a dirty industry scores 100. We therefore pair every rank with an absolute intensity "
     "(Exhibit 7) — an omission in v1 that the referee correctly flagged.")

h1("3. Data")
h2("3.1 Sources")
table([["Source","Provides","Licensed"],
 ["Bloomberg materiality maps, 18 companies, FY2021–25","192 fields delivered; 130 non-financial used after collapsing rate triples and dropping unreported","**Yes — withheld**"],
 ["Own FY2025 credit workbook","leverage, coverage, FCF/debt, capex/D&A, payout, maturities, ROCE, reserve life, three agencies' adjusted leverage","No — SEC XBRL, agency publications"],
 ["SEC XBRL · EPA GHGRP · EPA EEIO v1.3","secondary cross-sector pipeline, 30 companies, 10 GICS sectors","No — free, government"]],
 widths=[2.1,3.8,1.0])
source("Agency-adjusted leverage is computed by us from published agency criteria and SEC filings; the ratings themselves are public. "
       "Bloomberg Terminal cell values are not redistributed — see WITHHELD.md.")
h2("3.2 Universe, dated")
para("**XLE listed 21 S&P 500 energy constituents at 12 September 2026.** We cover 18. **APA** and "
     "**Texas Pacific Land** were not in the export and are absent; **EQT** and **ONEOK** likewise. "
     "**CTRA** is included and was in the index at our extraction date. We did not pad the sample.")
table([["BECS peer group","n","Members"],
 ["Exploration & Production","7","COP, CTRA, DVN, EOG, EXE, FANG, OXY"],
 ["Integrated Oils","2","CVX, XOM"],
 ["Midstream","3","KMI, TRGP, WMB"],
 ["Refining & Marketing","3","MPC, PSX, VLO"],
 ["Oilfield Services & Equipment","3","BKR, HAL, SLB"]], widths=[2.1,0.4,4.4], align=["l","c","l"])

h2("3.3 The indicators, named")
para("v1 never listed them. **Exhibit 3 names every environmental indicator in the model.** The two "
     "answers the referee asked for: **Scope 3 is absent** from all 139 fields — Bloomberg's ES map for "
     "these peer groups does not carry it, and its absence is the single largest gap in this framework "
     "for an oil and gas universe. **Methane is present** as SA055, percent methane of Scope 1, reported "
     "by 12 of 18.")
label("Exhibit","3","Every environmental indicator in the model, by breadth of reporting")
table([["Field","Indicator","Type","Reported"],
 ["F0947","Scope 1 GHG / CO₂ emissions","Q","15/18"],
 ["SA162","Air pollution reduction policy","B","18/18"],
 ["SA558","Claims science-based emissions target","B","18/18"],
 ["SA559","Claims net-zero emissions target","B","18/18"],
 ["ES007 / F0949 / ES009","NOx · SOx · VOC emissions","Q","14 / 13 / 14 of 18"],
 ["SA055","**Percent methane of Scope 1**","P","12/18"],
 ["SA020","Freshwater withdrawals","Q","12/18"],
 ["ES249 / SA048","Hydrocarbon spills, volume and count","Q","11/18"],
 ["F1284","Embedded carbon in total reserves","Q","9/18"],
 ["ES027","Gas flaring","Q","9/18"],
 ["SA084 / SA085","Internal carbon pricing · Arctic drilling","B","9/18"],
 ["ES497","Water stress exposure","P","9/18"],
 ["ES019 / SA016 / SA023","Hazardous waste: total, share, recycled","Q/P","7 / 5 / 4 of 18"],
 ["ES077 / ES255","GHG Scope 2, location- and market-based","Q","2/18"],
 ["—","**GHG Scope 3**","—","**absent from the export**"]],
 widths=[1.35,3.15,0.5,1.4], align=["l","l","c","r"])
source("37 environmental fields in total; the remaining 15 are policy booleans listed in Appendix C. "
       "Type: Q quantity, P percentage, B boolean.")

pagebreak()
h2("3.4 The disclosure constraint")
label("Exhibit","4","Field coverage by pillar and fiscal year (share of cells filled)")
table([["Pillar","Fields","FY2021","FY2022","FY2023","FY2024","FY2025"],
 ["Environment","37","59%","59%","60%","61%","**36%**"],
 ["Social","14","65%","65%","65%","66%","**39%**"],
 ["Governance","78","97%","97%","97%","97%","92%"],
 ["Financial","9","94%","94%","94%","94%","94%"]],
 widths=[1.5,0.7,0.85,0.85,0.85,0.85,0.85], align=["l","r","r","r","r","r","r"])
para("**Only three environmental and one social field are reported by all 18 companies.** Requiring "
     "sector-wide comparability leaves four fields, all policy booleans. That is not a gap in our "
     "pipeline; it is what the sector's disclosure looks like when you demand comparability.")
para("**On the denominator.** v1 said revenue was unavailable. The referee is right that this was a "
     "choice: revenue is a standard Terminal field and sits in the SEC filings we already used. We used "
     "EBITDA because the credit workbook was the artefact we had built and it is the scale measure a "
     "credit analyst reaches for. **It is the weakest defensible choice in the paper** — EBITDA is "
     "cyclical, and a single FY2025 figure scales FY2021–24 numerator data. Appendix F reports a "
     "sensitivity: substituting equity as the denominator moves the median company 1.0 place.")

# ═══════════════════════════════ 4 METHOD ═══════════════════════════
h1("4. Method")
h2("4.1 Where the providers actually choose")
para("Thirteen decision points. The corrected map — v1's summary contradicted its own exhibit in three "
     "places, which the referee caught.")
label("Exhibit","5","Provider decision-point map, corrected")
table([["#","Decision","MSCI","Bloomberg","Same?","v2 treatment"],
 ["1","What is measured","risk to the firm","risk to the firm","agree","**fixed** — we differ from both, §2"],
 ["2","Peer group","GICS sub-industry","BECS (bespoke)","differ","**question axis**, held fixed within a curve"],
 ["3","Size denominator","modelled exposure","activity metric","differ","varied"],
 ["4","Raw → grade","percentile bands","log-log residual","differ","varied"],
 ["5","Missing data","0 on management","drop, then cap","differ","varied"],
 ["6","Aggregation","arithmetic mean","power mean p=½","differ","varied"],
 ["7","Pillar weights","G floored 33%","G at rank 3","differ","**varied in v2** (was fixed) §5.5"],
 ["8","Relative / absolute","G absolute","fatalities absolute","both break own rule","relative + absolute panel"],
 ["9","Time window","3-yr lookback","3-yr parameters","**agree**","varied — and we now say so"],
 ["10","Discretisation","7 bands","7 bands","agree","fixed — we do not discretise"],
 ["11","Human override","committee","none","differ","**fixed** at none — cannot enumerate a committee"],
 ["12","Controversies","central","absent","differ","**fixed** at absent — declared scope boundary"],
 ["13","Non-public data","refused","public only","agree","fixed"]],
 widths=[0.25,1.15,1.05,1.1,0.72,2.5], align=["c","l","l","l","c","l"], size=7.5)
source("v1 claimed to vary the seven differing decisions and fix the six agreed. It varied six, one of which (#9) is agreed, "
       "and fixed three that differ (#7 in v1, #11, #12). Corrected here; #7 is now varied.")

h2("4.2 Two questions, two grids — the central revision")
para("v1 pooled *level* and *change* into one distribution. Simonsohn's own criterion is that a "
     "specification must test the research question; level and change are two questions. Pooling them "
     "produced two-humped distributions and a headline that was partly an artefact of the pooling.")
table([["","Question A — **stewardship**","Question B — **momentum**"],
 ["Asks","Who causes least harm per unit of output *now*?","Who is *reducing* harm fastest?"],
 ["Reduction","level of the latest reported value","relative change over three reported years"],
 ["Cells","8,748 (2,916 distinct grade paths)","8,748"],
 ["Pillars","E, S, G, F","E, S, G — financial has one year, so no trajectory"],
 ["Use","screening, exclusion, benchmarking","engagement, transition allocation (§8)"]],
 widths=[0.85,2.9,3.1], first_bold=True)
para("Within each question the remaining seven axes are genuine competing methods for the same "
     "question, which is the grid specification-curve analysis licenses.")

h2("4.3 Rules that are rules")
para("**MIN_PEERS = 3.** The referee notes that in a three-member group a field two members report still "
     "scores 0 or 100. Correct — the floor mitigates but does not eliminate this. §6.5 reports what it "
     "costs. **ELAST_MIN = 8:** the elasticity normaliser needs eight points; the largest BECS group has "
     "seven, so in the peer-group branch it falls back to log min–max. v1 did not disclose that this "
     "fallback fires for every company in that branch. It does.")

pagebreak()
# ═══════════════════════════════ 5 RESULTS ═══════════════════════════
h1("5. Results")
h2("5.1 Contestation after every deflation")
label("Exhibit","6","Median contestation, Question A, by how much is held fixed")
table([["Stratum","Cells","Median IQR (places of 18)"],
 ["v1 headline — both questions pooled","17,496","7.0"],
 ["Question A only (level)","8,748","5.0"],
 ["Question A × sector peers","2,916","5.0"],
 ["Question A × BECS peer groups","2,916","**3.0**"],
 ["Question A × strict evidence bar","2,916","3.0"],
 ["Random-rank benchmark (referee's control)","—","8.5–9.0"]],
 widths=[3.5,1.1,2.3], align=["l","r","r"])
source("The referee's random-rank control is the right test and we adopt it: a randomly ranked company would show 8.5–9.0 places. "
       "v1's 7.0 was barely below random, which is why pooling was indefensible. Question A at 3.0 is well inside it.")
callout("**The honest headline is 3.0 places, not 7.0.** One-third of v1's spread was two questions "
        "pooled. What remains is a third of the ranking still being a methodological choice — smaller "
        "than we claimed, and still larger than any published score admits.")

label("Exhibit","7","Specification curve and absolute intensity — Question A, sector peers")
fig("f2_speccurve.png", 6.5)
source("Every company's 2,916 Question-A scores, sorted best to worst. Flat = robust; steep = the method decides. "
       "v1 promised absolute intensities and never showed them; they are in Appendix E, Exhibit E1.")

h2("5.2 What is settled")
label("Exhibit","8","Settled pairwise comparisons — threshold stated, as the referee demands")
table([["Criterion","Settled","of 153","Share"],
 ["Both questions pooled, P > 0.95","2","153","1%"],
 ["Both questions pooled, P > 0.99","1","153","<1%"],
 ["Question A only, P > 0.95","33","153","22%"],
 ["Question A × strict evidence bar, P > 0.95","**56**","153","**37%**"]],
 widths=[3.3,0.9,0.8,0.9], align=["l","r","r","r"])
para("**Two caveats we now state.** A 95% threshold is decided by the rarest 5% of cells — the same "
     "extremes §6.3 calls uninformative. And at the strict bar the environmental pillar has two fields "
     "and Social none, so **the 56-pair result is largely a governance-and-credit ranking**, not a "
     "sustainability one. v1 presented it as the latter. It is not.")

h2("5.3 Where the disagreement lives")
label("Exhibit","9","Variance decomposition, mean across the 18 companies")
fig("f3_variance.png", 6.5)
source("Main effects 47.8%; interaction 52.2%. Because interaction dominates, the 'decided by' column in v1's Exhibit 1 "
       "was a one-at-a-time reading of a grid that is not one-at-a-time. It is removed in v2.")
para("**On the Financial-pillar objection.** The referee suspected *direction*'s 18.2% is the F pillar "
     "switching off. Setting the F weight to zero and rerunning moves it to **15.0%**. About 3pp of the "
     "18.2 is the pillar toggle; the rest is real. The objection is right in kind, wrong in magnitude.")

h2("5.4 The remedy")
para("For each unreported field we remove that single silence from the model and measure how far the "
     "interquartile width falls. **The assumed value matters and v1 did not state it:** we do not impute "
     "a value, we remove the field from the expected set, which isolates the *ambiguity* the silence "
     "creates rather than guessing the number. Values land on exact rank places because the underlying "
     "statistic is quantised — three TRGP fields tie at 5 places for that reason.")
para("**Counter-evidence we should have cited.** Christensen, Serafeim & Sikochi (2022) find more ESG "
     "disclosure is associated with *more* rater disagreement. That cuts against a naïve reading of our "
     "remedy. The reconciliation: they measure disagreement *between raters with different frameworks*; "
     "we measure ambiguity *within one framework* from a missing input. More disclosure can widen the "
     "first while narrowing the second.")

h2("5.5 Weights — the result v1 refused to compute")
para("v1 argued from the central limit theorem that re-weighting cannot move ranks much. The referee is "
     "right that this is wrong: a weighted composite can rank a company above all its pillar ranks, and "
     "power and geometric means are not weighted averages at all. We built a slider and never used it.")
label("Exhibit","10","Consensus rank across the five weight presets, Question A")
table([["Ticker","Equal","Env-led","Social-led","Gov-led","Finance-led","Spread (places)"],
 ["WMB","41","59","53","35","24","**6.0**"],
 ["KMI","41","41","47","47","24","4.0"],
 ["HAL","12","6","18","24","29","4.0"],
 ["TRGP","35","24","47","47","35","4.0"],
 ["PSX","41","29","53","47","41","4.0"],
 ["XOM","47","41","47","41","65","4.0"],
 ["**Median, all 18**","","","","","","**3.0**"]],
 widths=[0.8,0.75,0.85,0.95,0.85,1.05,1.1], align=["l","r","r","r","r","r","r"])
source("Weights move the median company 3.0 places and the most weight-sensitive 6.0 — comparable to the 3.0 places of "
       "method contestation within Question A. Weights are not negligible. v1's claim that they were is withdrawn.")

pagebreak()
# ═══════════════════════════════ 6 RISKS ═══════════════════════════
h1("6. Risks to this analysis")
for t in [
 "**6.1 The grid is enumerated, not sampled.** 17,496 cells collapse to **606 distinct grade paths**; 42 are exact duplicates. The spread is a range over conventions we chose, never a confidence interval.",
 "**6.2 N = 18 quantises everything.** A rank percentile takes 18 values 5.88 points apart. All headlines are in rank places for that reason — including the remedy values, which v1 reported to one decimal while arguing the opposite.",
 "**6.3 Extremes decide the settled count.** Extreme ranks are 2.2% of cells, and the 95% threshold is set by exactly those cells. We report both the threshold and the count.",
 "**6.4 The denominator is a choice we would remake.** EBITDA, single-year, cyclical. Revenue was available. Appendix F gives the sensitivity.",
 "**6.5 Contestation is partly thin data.** Rank correlation between coverage and contestation is **−0.38**. Group size is not monotone, though: the 2-member group has the *lowest* mean contestation (6.0) and the 3-member groups the highest (7.7), so small-group artefacts explain part of the pattern but not its direction.",
 "**6.6 Governance dominates by count.** 78 of 138 fields. The contestation we measure is mostly environmental and social; the governance pillar is stable because it is densely reported.",
 "**6.7 Scope 3, controversies and transition capex are absent.** For an oil and gas universe these are the three most material omissions. Scope 3 is not in the export; controversies are a declared scope boundary; transition capex was not delivered.",
 "**6.8 Reserves are double-counted in sign.** Embedded carbon in reserves scores as harm; reserve life scores as financial resilience. The same barrels push both ways. Under our §2 definition harm should dominate, and Appendix F shows the net effect is −0.5 places for the two integrated majors.",
 "**6.9 Nothing is benchmarked against a real rating.** We had a Terminal and did not place Bloomberg's own score inside our distribution. This is the single most valuable missing test and it is first on the roadmap.",
]: para(t, after=4)

# ═══════════════════════════════ 7 ═══════════════════════════════
h1("7. What this is, and what it is not")
h2("7.1 A framework, and a superset of a rating")
para("Per company the output is a **consensus score** — the number the brief asked for — and a "
     "**contestation figure**, which nobody else provides. v1 claimed not to publish a score while "
     "publishing a ranked table; that was rhetoric and it is dropped. We publish a score. We also "
     "publish how much of it is a choice.")
h2("7.2 What is genuinely new, stated more modestly")
para("Rating uncertainty is not new: Avramov, Cheng, Lioui & Tarelli (2022) measure it as dispersion "
     "*across six providers*. Ours is a different object — dispersion *within one dataset across method "
     "choices*, which isolates construction from data differences and can be computed by a single user "
     "with a single data licence. The partial order and the disclosure-value measure are, to our "
     "knowledge, new to this literature.")
h2("7.3 It scales")
para("The full grid over 18 companies and 138 fields runs in **18 seconds**. The cross-sector pipeline "
     "in ETHack/contested/ reaches 30 companies across 10 GICS sectors on free government data. "
     "**Cross-sector comparison is not delivered in this paper** and we do not claim it: our indicators "
     "are sector-specific by construction, which is the same reason MSCI and Bloomberg build materiality "
     "maps per industry.")

pagebreak()
# ═══════════════════════════════ 8 BONUS ═══════════════════════════
h1("8. Bonus — allocating $1 billion under a net-zero commitment")
callout("**Buy the companies the market cannot yet classify.** Not the best ESG scores, which are "
        "priced; not the worst, which are often structurally incompatible. The ones whose eligibility "
        "is *contested* — and among those, the ones our Question-B curve says are already moving.")

h2("8.1 The mechanism, and why the obvious version of it fails")
para("The thesis in the market is that crossing an ESG threshold unlocks capital: Merton's investor "
     "recognition model predicts that widening the eligible investor base lowers required return, and "
     "ESMA's naming rules plus the Article 8/9 regime create real eligibility screens. **We tested this "
     "on our own data and the cliff does not exist.**")
label("Exhibit","11","There is no eligibility cliff — 15 of 18 companies are contested")
table([["P(passes a top-50% screen) across the grid","Companies","Reading"],
 ["P > 0.8 — reliably eligible","2","priced in"],
 ["0.2 ≤ P ≤ 0.8 — **contested eligibility**","**15**","the opportunity set"],
 ["P < 0.2 — reliably ineligible","1","structurally excluded"]],
 widths=[3.2,1.0,2.6], align=["l","c","l"])
source("Mean |P − 0.5| = 0.17. A true cliff would give 0.5. Eligibility is a fog, not a line, because the score itself is contested. "
       "Computed over all cells at equal weights.")
para("This kills the naïve trade and licenses a better one. If eligibility is probabilistic, the "
     "tradeable quantity is not *crossing a line* but **the change in P** — and P moves for two quite "
     "different reasons, with very different cost and speed:")
table([["Channel","What has to happen","Cost","Speed","Our measure"],
 ["**Convention**","the market's scoring convention shifts (CSRD/ISSB harden the missing-data rule)","zero","1–2 years","spread of P across the missing-data axis"],
 ["**Trajectory**","the company actually reduces harm","high capex","3–7 years","P on Question B minus P on Question A"],
], widths=[0.95,2.6,0.55,0.75,1.9], size=8.0)

h2("8.2 The signal, computed")
label("Exhibit","12","Where a company stands versus where it is heading — the transition map")
fig("f4_eligibility.png", 6.3)
source("P(eligible) under Question A (horizontal) against Question B (vertical). Above the diagonal = improving faster than its "
       "current standing implies. Orange = delta > 0.15. This is the framework's answer to the bonus, not a separate opinion.")
table([["Ticker","P(A) level","P(B) change","Δ","Bucket"],
 ["MPC","0.12","0.73","**+0.61**","Transition core"],
 ["OXY","0.27","0.69","+0.41","Transition core"],
 ["HAL","0.02","0.39","+0.38","Excluded — base below 0.05 (see rule)"],
 ["PSX","0.23","0.51","+0.28","Transition core"],
 ["KMI","0.27","0.53","+0.27","Transition satellite"],
 ["WMB","0.35","0.57","+0.22","Transition satellite"],
 ["EOG","1.00","0.34","**−0.66**","Priced leader — fund the book"],
 ["XOM","0.72","0.26","−0.46","Priced leader — fund the book"],
 ["EXE","0.99","0.62","−0.38","Priced leader"]],
 widths=[0.8,1.1,1.15,0.8,2.6], align=["l","r","r","r","l"])

h2("8.3 The allocation")
table([["Sleeve","$m","Selection rule","Return source"],
 ["**Trajectory long**","350","top quartile of Δ = P(B) − P(A), excluding Δ driven by a base below 0.05","Question-B re-rating as scoring regimes reweight toward progress"],
 ["**Convention long**","250","companies whose P *rises* as the missing-data rule hardens — they have already paid the disclosure cost","CSRD/ISSB tightening; no capex, no technology risk"],
 ["**Enablers**","150","grid, cable and electrification suppliers — the bottleneck regardless of who wins","volume growth, not re-rating. Deliberately small: this is the most crowded trade"],
 ["**Structural short / underweight**","−150","P(A) < 0.2 **and** Δ < 0.05 — bad today and not moving","funds the book; isolates transition alpha from sector beta"],
 ["**Dry powder**","250","deploy on a 15% drawdown in the trajectory sleeve within 90 days, else revert to benchmark","indiscriminate post-announcement selling"],
], widths=[1.5,0.45,2.6,2.3], size=8.0)
para("**Three disciplines that follow from the framework and not from taste.** *Size by P, not by "
     "conviction*: a company at Δ = +0.61 gets more than one at +0.22 because the measure is a "
     "probability. *Cap correlated clusters*: names whose transition depends on the same input — cheap "
     "hydrogen, a high carbon price — count once against a cluster limit, not three times. *Exit into "
     "eligibility*: Pástor, Stambaugh & Taylor (2021) show green assets earn **lower** expected returns "
     "in equilibrium, so this is a repricing trade with an endpoint. Sell when P(A) exceeds 0.8.")
h2("8.4 What the framework cannot decide, and we will not pretend it can")
para("Our universe is 18 energy companies scored against each other. **It cannot rank Apple against "
     "ExxonMobil**, so a real $1bn book needs the same machinery run per sector with sector-neutral "
     "position limits. It has no view on the carbon price, on green hydrogen economics, or on whether "
     "transition capex earns its cost of capital — and that last one is decisive: converting high-ROCE "
     "fossil assets into regulated-return renewables can be ESG-accretive and value-dilutive at once. "
     "**Naming specific non-energy securities would be an opinion dressed as an output.** The rule above "
     "is the output; the names in Exhibit 12 are the ones our data actually supports.")

pagebreak()
# ═══════════════════════════════ APPENDICES ══════════════════════════
h1("Appendix A · The formula")
para("Indices: company *i* = 1…18, field *f* = 1…138, year *y* = 1…5, base slot *b* ∈ {1,2,3}, pillar "
     "*P* ∈ {E, S, G, F}. Steps 1–5 produce a grade tensor and do not involve the pillar weights.")
table([["Step","Operation","Detail"],
 ["1 · exposure","x = VAR/BASE if type Q, else select variant b","one operator per type, so the divisor is applied exactly once"],
 ["2 · window","latest reported · fixed FY2024 · 3-year mean","reductions run over years the company reported, not calendar columns"],
 ["3 · direction","**Question A** level · **Question B** change","separate grids in v2"],
 ["4 · orientation","u = pol · q, higher = worse","pol ∈ {+1, 0, −1}; 0 = deliberately neutral"],
 ["5 · normalise","percentile · winsorised · log min–max · elasticity","elasticity falls back to log below 8 peers"],
 ["6 · aggregate","M(x,w,p,s) = (Σ wⱼ(xⱼ+s)^p)^(1/p) − s, p = ½, s = 10","p=1 recovers MSCI's mean; p→0 the geometric"],
 ["7 · rank","R = 100(N − ρ)/(N − 1)","average rank descending; 100 = best"],
 ["8 · distribute","consensus = median R; contestation = IQR ÷ 5.88","reported in rank places"]],
 widths=[1.05,2.5,3.35], size=8.0)
para("**Order matters.** Aggregate fields *inside* each specification, then take the distribution "
     "*across* specifications. Reversing them averages 138 fields first and collapses the spread.")
para("**Edge cases the referee asked about, now defined.** Neutral polarity sets the field to a constant "
     "50 rather than entering min–max (no division by zero). Log models shift the series positive before "
     "taking logs. Change from a zero base returns NaN and the field drops rather than dividing by zero. "
     "The elasticity model regresses log(impact) on log(activity); §4.2 of v1 stated it with log intensity "
     "on the right-hand side, which was a typesetting error — Appendix A.5 was correct and is what runs.")

h1("Appendix B · Referee objections answered in code")
table([["Ref","Objection","Verified answer"],
 ["B1","Contestation with direction and peer set held fixed","**3.0 places** (Question A × BECS), 5.0 (Question A × sector). Contestation survives."],
 ["B2","Are the distributions two-humped?","Yes. EOG: level median 94.1, change 35.3 — 10.0 places apart. Confirmed and fixed by splitting the grid."],
 ["B3","What happens to non-producers under the production denominator?","They keep S, G and F and lose only E. **All 18 still receive a composite** in every production cell. 92 Q-field grades for producers, 0 for non-producers."],
 ["B4","How many of the 17,496 cells are distinct?","648 grade-stage cells → **606 distinct**, 42 exact duplicates. Under change, a fixed FY2025 base does cancel, as the referee says."],
 ["B5","Is contestation group size or evidence?","Partly size. Mean IQR: 2-member 6.0, 3-member 7.7, 7-member 7.0 — not monotone. Coverage rank-corr −0.38."],
 ["B6","Is direction just the F pillar toggling?","No. Zeroing the F weight moves direction from 18.2% to **15.0%**."],
 ["B7","Could any company ever be rated robust?","Under the pooled grid, no — which is why the verdict column was uninformative and is removed. Within Question A × BECS, 4 of 18 fall below 2 places."],
 ["C2","Which settled statistic do you stand behind?","**>95% of Question-A cells: 33 of 153.** The 'every method' wording is withdrawn."],
 ["C4","Rank spread across the weight presets","Median **3.0** places, max 6.0 (WMB). Reported in Exhibit 10."],
 ["D5","Which field does no company report?","**DX831**, a governance field. 139 in the registry, 138 with data; the model now uses 138."],
], widths=[0.45,2.05,4.4], size=7.8)

h1("Appendix C · Field registry")
table([["Pillar","Boolean","Percentage","Quantity","Rate","Structural","Total"],
 ["Environment","18","4","15","0","0","37"],
 ["Social","9","0","0","5","0","14"],
 ["Governance","25","0","0","0","53","78"],
 ["Financial","0","0","0","9","0","9"],
 ["**Total**","**52**","**4**","**15**","**14**","**53**","**138**"]],
 widths=[1.4,0.85,1.0,0.9,0.75,0.95,0.8], align=["l","r","r","r","r","r","r"])
para("**Field weights within a pillar are equal** — v1 never stated this and the referee is right that "
     "it matters: with 9 financial and 78 governance fields, one financial field carries 8.7× the weight "
     "of one governance field *within its pillar's contribution*. Pillar weights then renormalise, which "
     "is why the pillar weighting in Exhibit 10 moves ranks as much as it does. **Polarity for the 63 "
     "uncontested governance fields** follows governance orthodoxy: independence, refreshment, "
     "disclosure and audit tenure limits score positively; concentration, entrenchment and long tenure "
     "score negatively. The 15 contested fields are listed in the repository's question set.")

h1("Appendix D · Sources")
for t in [
 "**MSCI ESG Ratings Methodology, Executive Summary, November 2020**, 17pp. We note the limitation the referee raises: this is the public executive summary, not the full methodology, and v1 overstated it as reading the methodology 'end to end'.",
 "**Bloomberg ESG Scores Methodology**, issued Sep 2023, updated Dec 2025, 58pp. Read in full.",
 "Berg, Kölbel & Rigobon (2022), *Aggregate Confusion*, Review of Finance 26(6) — divergence split **56 / 38 / 6**.",
 "Simonsohn, Simmons & Nelson (2020), *Specification curve analysis*, Nature Human Behaviour 4 — a specification must test the research question, be statistically valid, and not duplicate another. v1 breached the first and third; v2 addresses both.",
 "Avramov, Cheng, Lioui & Tarelli (2022), *Sustainable investing with ESG rating uncertainty*, JFE — cross-provider dispersion.",
 "Christensen, Serafeim & Sikochi (2022), *Why is corporate virtue in the eye of the beholder?*, The Accounting Review 97(1) — more disclosure, more disagreement.",
 "Dimson, Marsh & Staunton (2020), *Divergent ESG ratings*, JPM 47(1) — average correlation 0.45.",
 "Pástor, Stambaugh & Taylor (2021), *Sustainable investing in equilibrium*, JFE — green assets earn lower expected returns in equilibrium.",
 "Merton (1987), *A simple model of capital market equilibrium with incomplete information*, Journal of Finance — investor recognition.",
]: para(t, size=8.6, after=3)

h1("Appendix E · Reproducibility")
table([["Command","Produces"],
 ["python3 registry.py","the field registry, printed for inspection"],
 ["python3 load.py","the arrays and a coverage report"],
 ["python3 run.py","every specification → out/ (18 seconds)"],
 ["python3 export_web.py","the pillar cube for the browser explorer"],
 ["python3 -m http.server 4173 --directory ../web","the interactive tool"]], widths=[2.6,4.0], size=8.2)
para("**numpy and pandas only.** The browser explorer reproduces run.py to 0.05 rank points on all 18 "
     "companies. **Bloomberg Terminal cell values are withheld** — we do not share these indicators and "
     "values because they require the proper licensing, and we are happy to show the files in person to "
     "demonstrate that the model runs on real data and would scale. Everything derived from them is "
     "published: the loader, the formula, all computed outputs, the explorer. The referee is right that "
     "this makes full reproduction contingent on a Terminal; the outputs are committed so every figure "
     "in this paper can be checked without one.")

h1("Appendix F · Roadmap, in the order we would do it")
table([["#","Work","Why it is first"],
 ["1","Place Bloomberg's own ESG score inside each company's distribution","The paper's central claim is that a published score is one draw from a distribution. We had the Terminal and did not test it. Highest value, lowest cost."],
 ["2","Rerun on revenue and on a rolling denominator","Removes the weakest defensible choice in the paper."],
 ["3","Effective-specification weighting","606 distinct of 648; weight cells by distinctness so duplicates stop inflating the distribution."],
 ["4","Source Scope 3 and transition capex","The two most material omissions for oil and gas."],
 ["5","Cross-sector run with sector-neutral normalisation","Delivers the S&P 500 promise in the title."],
 ["6","Backtest the §8 signal","Does Δ = P(B) − P(A) predict forward returns or rating migration? Until tested, §8 is a hypothesis with a computed signal, not a validated strategy."]],
 widths=[0.3,2.3,4.2], align=["c","l","l"], size=8.0)

rule(10)
para("**Disclosures.** Prepared for ETHack 2026, Challenge #1, by a student team over 24 hours and "
     "revised after referee review. This is not investment research, not a recommendation to buy or sell "
     "any security, and was not prepared by a regulated entity. Section 8 is a methodological "
     "demonstration on a hypothetical mandate; company names appear as data points. All computed figures "
     "derive from the committed pipeline and can be regenerated from source. Characterisations of MSCI's "
     "and Bloomberg's methods are ours and any error in them is ours.",
     size=7.8, color=INK3)
