---
edit: owned
last_edited: 2026-09-12T20:40:00 CET
changes: 22
type: project-note
status: active
---
# ETHack 2026

Hub for ETHack 2026, the student-run 24h hackathon at ETH Zürich. Theme: **Hack for Good**. 12-13 September 2026, ~100 students. Site: [ethack.ch](https://ethack.ch/)

I am participating as a hacker, not organizing. Separate from [[incube]], this is personal build work.

## Files

- **`speccurve/`** — **the formula, running.** 72 specifications x 4 weightings = 288 scores per company, dummy data, three figures. `FORMULA.md` is the whole method on one page. Open THIS folder in Claude Code.
- **`contested/`** — **the codebase.** Open this folder in Claude Code. `01_fetch.py` -> `02_score.py` -> `03_plots.py`. 30 companies, 24 specifications, tested end to end. `README.md` has the run instructions, `DEFENCE.md` the ten attacks answered.
- [[Efforts/Active/ETHack/sample-and-factors|sample-and-factors]] — **die Stichprobe und die 30 Faktoren.** S&P 500 Energy komplett (21-22 Firmen), Sub-Group-Split als intra/inter-Test, `factors30.csv` und `companies21.csv`.
- **`model/`** — **the model, rebuilt on the real export.** 18 energy companies, 139 fields, 9 axes, 17,496 specifications. `README.md` has the findings and the limitations. Replaces `speccurve/`, which stays as the synthetic-data reference.
- [[Efforts/Active/ETHack/methodology-next|methodology-next]] — **the four outputs.** Settled / contested / pivot / remedy. Locating MSCI and Bloomberg inside our own grid, variance decomposition over the axes, the partial order, and decision stability as the $1bn answer. All post-processing over the existing tensor.
- [[Efforts/Active/ETHack/provider-decision-points|provider-decision-points]] — **why our axes are the right axes.** Every fork where MSCI and Bloomberg choose differently, read out of the two methodology PDFs, with the branch we take at each and the citations. Also lists three cheap model additions and one claim of ours that needs correcting.
- [[Efforts/Active/ETHack/critique-weights|critique-weights]] — **Antwort auf die Gewichtungs-Kritik.** Warum ein Weight-Multiverse kollabiert (13.2%), warum unseres nicht (Scope + Measurement = 86.8%), und der Slider als zweite Ansicht.
- [[Efforts/Active/ETHack/divergence-sector|divergence-sector]] — **why Energy is the right sector.** Provider agreement is lowest in Energy (0.55). Equinor holds MSCI AAA. The named sign-flip cases and the pitch opener.
- [[Efforts/Active/ETHack/design-v4-fixes|design-v4-fixes]] — **current design.** Signed boolean tally, the exposure-base abstraction, 18 specs for every field type, and the export instructions.
- [[Efforts/Active/ETHack/design-v3-full-materiality|design-v3-full-materiality]] — **current design.** Type-aware dimensions across all 187 Bloomberg materiality fields, every choice justified from real XOM data, intra vs inter industry settled.
- [[Efforts/Active/ETHack/design-v2-utilities|design-v2-utilities]] — **the v2 design.** One industry (electric utilities), balanced 81-spec grid, three pillars, and the MSCI 37% finding.
- [[Efforts/Active/ETHack/execution-plan|execution-plan]] — **START HERE.** 6 companies, 4 people, 17 hours, checkpoints on the real clock.

- [[Efforts/Active/ETHack/challenge|challenge]] — the challenge brief, rules, judging criteria, deliverables. **Fill this first, everything downstream depends on it.**
- [[Efforts/Active/ETHack/idea|idea]] — what we are building, scope cuts, why it wins.
- [[Efforts/Active/ETHack/quantitative-claims|quantitative-claims]] — the six claims we will actually make, the answer to the provider-count objection, and measured scalability.
- [[Efforts/Active/ETHack/impact-and-innovation|impact-and-innovation]] — the Impact and Innovation answers, Q&A-proof. Named users, the $3.7tn number, and an honest novelty claim.
- [[Efforts/Active/ETHack/how-many-specs|how-many-specs]] — how many specifications and which spread statistic. Decided: 72 specs, contestation = IQR.
- [[Efforts/Active/ETHack/proof-nucor|proof-nucor]] — **feasibility proven.** All four data layers pulled live for Nucor FY2023, real tonnes and real dollars. Data in `data/`. Show this to anyone who doubts the plan.
- [[Efforts/Active/ETHack/finding-walmart|finding-walmart]] — **first real result.** Walmart has no emissions figure in the US mandatory dataset. Real data, pulled live. Probably the hero of the pitch.
- **[Output mockup](https://claude.ai/code/artifact/e8f19e05-25a3-4d73-bcf6-469496cef301)** — the three figures and the table, drawn with synthetic data. This is the build target. Nothing in it is a real figure.
- [[Efforts/Active/ETHack/data-plan|data-plan]] — **where every number comes from.** All free, all government-published. Includes the 45-minute smoke test and the paid-data roadmap.
- [[Efforts/Active/ETHack/team-pitch|team-pitch]] — how to sell the angle to the team in 90 seconds, with the objections pre-answered.
- [[Efforts/Active/ETHack/framework|framework]] — **the design.** Specification curve analysis applied to ESG: 36 defensible specs, consensus rank plus contestation. Read this and the definition, then build.
- [[Efforts/Active/ETHack/sustainability-definition|sustainability-definition]] — **the methodology spine.** What we mean by sustainable, the boundary ladder, indicators, limitations. Every number in the deck traces back here.
- [[Efforts/Active/ETHack/data-landscape|data-landscape]] — what companies are actually required to report (almost nothing), and how MSCI and Sustainalytics build their scores.
- [[Efforts/Active/ETHack/aggregate-confusion|aggregate-confusion]] — the MIT Sloan paper the angle stands on, and why it lands with this jury. **Whole team reads this.**
- [[Efforts/Active/ETHack/build-log|build-log]] — running timestamped log across the 24h.
- [[Efforts/Active/ETHack/demo-pitch|demo-pitch]] — pitch script, demo run sheet, what is real vs faked.
- [[Efforts/Active/ETHack/retro|retro]] — after. Written within 48h or not at all.

## Facts

| | |
|---|---|
| Event | ETHack 2026, "Hack for Good" |
| Dates | 12-13 September 2026, 24 hours |
| Location | ETH Zürich |
| Size | ~100 students |
| My role | Participant / building |
| Team | TBD, teams of 4-5, formed over lunch day 1 |
| Sponsor | Citadel / Citadel Securities |
| Challenge | #1, sustainability framework for the S&P 500, see [[Efforts/Active/ETHack/challenge\|challenge]] |
| Prizes | CHF 2,000 / 1,000 / 500 |
| Pitch | **3 minutes**, 13 Sep, slot TBD |
| Must submit | **PowerPoint in `.ppt`** (hard requirement) + GitHub link |
| Venue | CHN, hacking and lunch spaces |

## Operating rules for the 24h

Written before the adrenaline, so they hold when it hits.

1. **The demo is the product.** Build the exact path a judge will watch, end to end, before building anything wider. A working two-minute path beats a half-built platform.
2. **Ugly and running beats clean and broken.** Refactor after the demo works, or never.
3. **Cut scope at every checkpoint, never add.** Every checkpoint in the timeline asks one question: what comes out?
4. **Freeze the code with 2 hours left.** Last two hours are demo rehearsal, slides, and sleep. No new features after the freeze, no exceptions.
5. **Fake anything that is not the core claim,** and say so honestly in the pitch. Judges punish hidden fakes, not admitted ones.
6. **One person owns the pitch from hour 0,** not from hour 22. The pitch shapes what gets built.
7. **Eat, hydrate, and take 20 minutes horizontal around hour 14.** Non-negotiable. The last six hours are where the project is won and a wrecked brain loses them.

## Timeline

Anchor T0 to the actual start once known, then fill the wall-clock column.

| | Offset | Wall clock | Checkpoint |
|---|---|---|---|
| 1 | T+0 | 12 Sep ~10:00 | Kickoff done. Challenge captured in [[Efforts/Active/ETHack/challenge\|challenge]]. |
| 2 | T+1h | lunch | Team of 4-5 formed, "done" ticked in the team table. Data sources tested. Idea locked in one sentence in [[Efforts/Active/ETHack/idea\|idea]]. |
| 3 | T+2h | | Repo up, everyone runs it locally. Roles split. Ticker key normalized once. |
| 4 | T+5h | | Skeleton end to end: fake data, fake model, real flow. Something clickable. |
| 5 | T+9h | | Core mechanism works on real input. First scope cut. |
| 6 | T+14h | | Feature complete on the demo path. Rest. Second scope cut. |
| 7 | T+18h | | Demo path rehearsed once, start to finish, without touching the code. |
| 8 | T+21h | | Slides done and exported to `.ppt`. Pitch rehearsed twice out loud, **timed to 3:00**. |
| 9 | T+22h | | **Code freeze.** Deploy or package. Backup video of the demo recorded. |
| 10 | T+24h | | Submit. Present. |

## Status

Framework designed, see [[Efforts/Active/ETHack/framework|framework]]. We do not publish a score, we publish the distribution of every defensible score and report how wide it is. Method is specification curve analysis (Simonsohn et al. 2020) imported into ESG. Team not yet formed.

## Next actions

- [ ] Form the team over lunch, tick "done" in the team table.
- [ ] **Ask the organizers whether `.pptx` is accepted or `.ppt` is literal.** Mechanical disqualification risk.
- [ ] Test data source access in the first 30 minutes, see the table in [[Efforts/Active/ETHack/idea|idea]]. Kill any source not returning rows by T+0:45.
- [ ] Decide whether "damage" includes Scope 3. This gates every data decision.
- [ ] Lock the angle and write the one sentence in [[Efforts/Active/ETHack/idea|idea]].
- [ ] Get the judges' surnames from an organizer or the WhatsApp group.
- [ ] Read the five judging criteria out loud to the team before writing any code.
- [ ] Assign the pitch owner at hour 0.
- [ ] Anchor T0 and fill the wall-clock column above.

## Related

- [[ME]] — build mode applies for the duration.
- [[current-situation]] — this sits alongside HS26 semester start, see [[Efforts/Active/Exams/hs26-semester-plan|hs26-semester-plan]].
- [[Efforts/Active/LinkedIn/index|LinkedIn]] — post 3 already carries a hackathon photo brief. Shoot usable photos during the event.
