---
edit: owned
last_edited: 2026-09-12T10:50:00 CET
changes: 0
type: log
status: active
preserve: [append-only, newest at bottom, never rewrite past entries]
---
# Build log

Append-only. One line per meaningful event. Timestamp everything. This is what the [[Efforts/Active/ETHack/retro|retro]] and the LinkedIn post get written from, and it is what saves you when something that worked at hour 6 breaks at hour 20.

Format:

`### HH:MM | <what happened> | <decision or next step>`

Log these without being asked: idea locked, stack chosen, first thing running, every scope cut, every blocker and how long it ate, every checkpoint hit or missed, the freeze, the rehearsal.

---

### 10:50 | Effort scaffolded in the vault | Awaiting challenge announcement

### 11:21 | Direction set: present-damage score, boundary-sensitivity as the finding. Grounded in Aggregate Confusion (MIT Sloan). | Open gate: does damage include Scope 3?

### 11:28 | Wrote sustainability-definition.md: definition, E-only justification, A/B/C boundary ladder, dual denominator, indicator set with exclusions, missing-data policy, limitations, bonus-question bridge | Needs team sign-off before code

### 11:52 | Wrote data-landscape.md: current disclosure regulation status (SEC rescission proposed, CA SB253 due 10 Nov 2026, CSRD gutted, EPA GHGRP repeal proposed) and MSCI vs Sustainalytics methodology contrast | Key finding: emissions disclosure is still voluntary today

### 12:10 | Framework designed: specification curve analysis applied to ESG. 36 defensible specs, consensus rank + contestation per company. Bad data strengthens the finding. | Awaiting team sign-off

### 12:21 | Wrote team-pitch.md: 90-second spoken pitch for specification curve analysis, red-card study as the hook, six pre-loaded objections with answers | For selling the angle at team forming

### 12:53 | Wrote data-plan.md: SEC XBRL frames API for revenue in one call, EPA EEIO supply-chain factors for 100% emissions coverage, GHGRP parent rollup for disclosed Scope 1, six named traps, 45-min smoke test, four-phase paid-data roadmap | Endpoints NOT live-tested, egress blocked

### 12:59 | Published output mockup artifact (Contested): spec curve + contestation map + boundary slope + verdict table, synthetic data | Build target for the team, link in ethack.md

### 13:23 | REAL FINDING: Walmart has one GHGRP facility (HQ, Bentonville), registered only under supplier subparts OO/QQ (imports pre-charged F-gas equipment). co2e_emission null for all 24 rows 2012-2023. Working API is dmapservice not efservice. | Recommend Walmart as Figure 1 hero instead of a bank

### 13:30 | FEASIBILITY PROVEN end to end on Nucor FY2023: rev $34.71bn (SEC), 5.76 Mt disclosed Scope 1 across 26 GHGRP facilities, 27.32 Mt modelled via EEIO 0.787. Found 5th spec dimension (consolidation approach, 4.59% swing) and that EEIO alone kills within-sector variation. Data in data/ | Revenues tag trap confirmed real

### 13:36 | Decided spec count and spread statistic: floor is 7 for main effects, 36 for interactions, run 72 (adds consolidation); contestation = IQR P25-P75 primary + full range secondary; P10/P90 rejected at n=36 (falls between 4th and 5th value) | Variance decomposition by dimension flagged as highest-value optional output

### 13:56 | Wrote impact-and-innovation.md: triage-of-analyst-attention framing, $3.7tn sustainable fund AUM (Morningstar Q2 2026), four named users with the decision each changes, honest novelty separation, and the structural argument that incumbents cannot publish contestation because confidence is their product

### 14:11 | Answered the provider-count objection (we generate specs, we do not average providers; n is a design parameter), listed 6 falsifiable quantitative claims with the Spearman-vs-0.61 benchmark as headline, and measured scalability: 36k computations in 12ms, ~39 API calls via bulk-pull-then-local-join | Name matching is the only real risk

### 14:26 | Execution plan set: 6 companies as the core (intensity not rank) + 500 modelled as stretch; swapped GE out for a utility, kept Nucor (data already done); MSCI lookups reframed as a reference line not a divergence study; 4-person split with no blocking dependencies; checkpoints on real clock times to an 08:00 freeze

### 14:38 | 30-MIN SPRINT DELIVERED: real data for 4 companies (Walmart/Nucor/Ford/JPMorgan) from SEC frames + GHGRP + EEIO. HEADLINE: ranking fully inverts - Nucor worst by disclosed intensity, Walmart worst by modelled total (105.4 Mt vs 27.3 Mt). JPMorgan has ZERO GHGRP rows for 2023. Ford ratio 85x. Runnable run.py + DEFENCE.md (10 attacks answered) in contested/ | Existence claim not prevalence claim is the defence rule

### 14:54 | Built the contested/ project folder: companies.csv (30 companies, 10 GICS sectors x 3), 01_fetch.py (SEC frames + GHGRP dmapservice + EEIO + yfinance, cached), 02_score.py (24 specs = 2 boundary x 3 missing x 2 margins x 2 denominator, --peer for 48), 03_plots.py (3 figures). Tested end to end on the 4 verified companies: inversion confirmed True, median modelled/disclosed 44.9x. Ready for Claude Code.

### 15:20 | Built CONTESTED_raw_data_30_companies.xlsx: 6 sheets (README, Company inputs, EPA facilities 562 rows, EEIO factors, Data gaps 20 documented, Provenance). 128 formulas, recalc clean, SUMIF audit reconciles all 30 companies to zero, total 1,005,057,500 tCO2e. Found bug: XOM CIK resolved to ExxonMobil Holdings Corp (0002115436) not Exxon Mobil Corporation (0000034088), hence blank revenue.

### 16:35 | DESIGN V2: electric utilities (NAICS 2211), 10 companies, balanced 3x3x3 grid per pillar = 81 specs identical for every company. Balance fix: replaced missing-data rule with source-of-truth dimension (self/regulator/provider) so every company has every cell. S pillar = safety/reliability/affordability (all EIA-reported, no ideology). G replaced by financial resilience (leverage/transition funding/Moodys rating). Key external validation found: MSCI v5.0 March 2026 repriced 37% of issuers from its own model change; S&P dropped numerical ESG scores 2023; EU ESG Rating Regulation live 2 Jul 2026 under ESMA with authorisation due 2 Nov.

### 17:42 | DESIGN V3 from the Bloomberg XOM materiality export: 187 unique fields, 135 usable. Core fix = TYPE-AWARE dimensions (Q/R/P/B/S), 1272 spec-field combos per company. Key findings from the real data: coverage inversion (G 92% vs E 58%); Scope 1 -8.2% while embedded carbon in reserves +4.8%; spills volume -72% while spill count +154%; contractor TRIR 0.21 vs employee 0.10 and contractor fatality rate is the ONE unreported cell while workforce rate is 2x employee = the social Scope 3. Intra vs inter industry justified: Bloomberg supplies the peer group and the tree, we only choose the dimension set per type.

### 18:00 | DESIGN V4 fixes: booleans become a signed tally b(f) in {-1,0,+1} summed and divided by the peer expected-set size (missing=0 because coverage is reported separately, one fact one place); double-normalising solved by one abstract EXPOSURE BASE dimension that APPLIES a divisor for type Q and SELECTS a pre-divided variant for type R. Added reference(3) to P and polarity(2) to S so every type yields exactly 18 specs, which removes a hidden 3:1 weighting by measurement type in the roll-up. 135 fields x 18 = 2430 combos per company. Flagged the LCL currency bug (must be USD or non-US majors return GBP/EUR/NOK). Requested: Bloomberg peer list first, then Chevron as a single verification export, then revenue + boe production + headcount.

### 19:22 | Built CONTESTED_question_set_and_data_request.xlsx (7 sheets): all 135 usable questions with Bloomberg field IDs and type, the 18 specs enumerated per type, all 27 E/S boolean signs with per-field justification and tier (all 27 / substantive 23 / outcome-linked 5), governance polarity table (18 of 54 fields where the two conventions disagree, incl. auditor tenure 92 years), export instructions with the LCL->USD currency fix, and the 12-company priority list. Worked proof: Exxon boolean tally +0.259 (all) vs -0.600 (outcome-linked), a 0.86 swing on [-1,+1].
