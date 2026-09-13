---
edit: owned
last_edited: 2026-09-12T19:41:27 CET
changes: 0
type: project-note
status: active
---
# Which sector has the most provider disagreement

Question: we want an industry where the providers contradict each other hardest, ideally one company AAA at one and terrible at another, to prove the framework's point.

Answer: **Energy.** The sector we already chose. Do not switch.

## 1. The sector-level evidence

Lopez (2020), reported in Nasdaq's 2024 ESG ratings review: average inter-provider agreement is **lowest in Energy, 0.55**. Highest are Technology 0.77, Cyclical Consumer 0.74, Financials 0.74. Lopez's reading: the high-agreement sectors are ones where providers barely weight environment at all, so there is less to disagree about.

Zumente & Lace (2021), same review: most pronounced lack of convergence in **automobiles, media and entertainment, technology, utilities**. They hedge their own conclusion.

Gibson, Krueger & Schmidt (2021): highest E and S disagreement in consumer durables and telecoms; highest G disagreement in financials.

So: Energy wins on the cleanest measure, utilities and autos are the runners-up. Utilities was our v2 pick and is still defensible. Energy is better and is already built.

## 2. The named case inside our own sector

Integrated oil and gas, MSCI letter ratings, 2026:

| Company | MSCI | Source |
|---|---|---|
| Equinor | **AAA** | aggregator, verify |
| Shell | AA | aggregator, verify |
| TotalEnergies | **AA** | company-reported, March 2026 |
| BP | A | aggregator, verify |
| Eni | **A** | company-reported, March 2026 |
| Chevron | A | aggregator, verify |
| ExxonMobil | BBB | aggregator, verify |

**Equinor is AAA.** That is the top band of MSCI's scale. The same band MSCI awards to companies whose entire business is renewable generation. Equinor is an oil and gas producer.

Four bands of spread inside one industry, and the top of the range is the ceiling of the whole scale.

Cross-provider on the same companies:

- TotalEnergies: MSCI **AA** (top-two band) and Sustainalytics **24.5 = Medium risk**, ISS-ESG **B- (Prime)**. All March 2026, all from TotalEnergies' own disclosure page.
- Eni: MSCI **A**, Sustainalytics **Medium risk (20-30)**, ISS ESG **B-**, Moody's **1st in sector**, TPI carbon performance **aligned with 1.5C**. Eni did not respond to CDP in 2025.
- ExxonMobil: MSCI **BBB** and Sustainalytics **36.5 = High risk** (IEEFA 2022, older).

Eni's page is the single best slide in this whole pile. One oil major, five providers, and one of them says its carbon performance is **aligned with 1.5 degrees** while another declines to rate it because it stopped filling in the questionnaire.

## 3. Why the divergence is this large in Energy

Three mechanical reasons, all of which our framework makes visible instead of hiding:

1. **Industry-relative normalisation.** MSCI scores a company against its own sub-industry peers. An oil major only ever competes with other oil majors, so the best-managed oil major gets AAA. The rating is not "does little environmental damage", it is "manages sector risk better than other people in this sector". That is the exact gap between our definition and theirs.
2. **Governance floor.** MSCI gives governance a minimum 33% weight in every industry. A large, well-governed producer can offset environmental exposure with board and pay structure. We deliberately excluded governance-as-DEI from scoring; this is the reason.
3. **Scope choice.** Whether reserves and sold-product emissions count at all is a scope decision, not a measurement. Our Bloomberg export makes this concrete: XOM Scope 1 fell 8.2% while embedded carbon in reserves rose 4.8%, and the reserves figure is 83x larger. A provider that stops at Scope 1 sees improvement. One that counts reserves sees the opposite. Both are defensible. That is a specification, not an error.

## 4. The cross-sector shock slides, if we want them

Dimson, Marsh & Staunton, *Divergent ESG Ratings* (2020). Average inter-provider correlation **0.45**. By pillar: E 0.42-0.59, S 0.11-0.43, **G -0.02 to 0.30**. Governance, the thing everyone thinks is objective, is essentially uncorrelated across providers. This is a harder number than the 0.61 we already quote.

Their named 2019 cases, literally "top of one, bottom of another":

- **Facebook**: environment **1st percentile at Sustainalytics, 96th at MSCI**. Social reverses.
- **Wells Fargo**: **12th percentile at MSCI, 94th at FTSE**.
- **JP Morgan, Pfizer**: governance 4th-7th percentile at MSCI vs 87th-99th at Sustainalytics.
- **Tesla**: MSCI AA and 96th percentile on environment; FTSE very low; Sustainalytics middle. MSCI counted product emissions, FTSE counted factory emissions.

Pillar weights for the same industry (insurance): Sustainalytics ~33/33/33, MSCI **5% E, 74% S, 21% G**.

IEEFA (2022), utilities, the cleanest substantive sign-flip:

- **AC Energy, 87% renewable capacity**: Refinitiv C+ 47/100, MSCI BB, Sustainalytics 43.9 **severe risk**.
- **Origin Energy, 74% fossil**: Refinitiv B+ 67/100, MSCI A, Sustainalytics 34.0 high risk.

All three providers rate the renewable company worse than the fossil company. Also Solaria (100% renewable) Refinitiv B- 55 vs Endesa A 86, which IEEFA reads as size bias.

## 5. What this changes in the build

Nothing in the code. It changes the first 30 seconds of the pitch.

Open with Equinor AAA. "MSCI's top rating, the same grade as a pure renewables company, held by an oil and gas producer. Not a mistake. A defensible consequence of one scope choice and one normalisation choice. We show you every other defensible choice and what each one does to the ranking."

Then the Energy 0.55 number, then our own measured minimum Spearman of **-0.148** between two of our own defensible specs. Ours is worse than theirs because ours is honest about the range instead of publishing one number from it.

## 6. The trap

Provider scores stay **reference lines on the chart, never inputs**. They are built from the same underlying Bloomberg fields we use, so feeding them in double-counts. Say this before a judge asks.

And the question a judge will ask: "if the providers disagree, how do you know you are right?" Answer: we do not claim to be right. We claim the single number was never available, and we show the interval instead of picking a point inside it and calling it a rating.

## Sources

- [Nasdaq, ESG ratings: The mixed bag and its implications (2024)](https://www.nasdaq.com/docs/2024/02/09/ESG-ratings-report.pdf) - Energy 0.55, sector table
- [Dimson, Marsh & Staunton, Divergent ESG Ratings (2020)](https://www.repository.cam.ac.uk/items/11d32fd3-5967-4fd1-b70a-1d7d4836c871) - 0.45, pillar correlations, Facebook/Wells Fargo/Tesla
- [IEEFA, Greater ESG Rating Consistency Could Encourage Sustainable Investments (2022)](https://ieefa.org/sites/default/files/2022-10/Greater%20ESG%20Rating%20Consistency%20Could%20Encourage%20Sustainable%20Investments_final.pdf) - AC Energy vs Origin, Tesla vs Exxon
- [TotalEnergies, main ESG ratings](https://totalenergies.com/sustainability/reports-and-indicators/main-esg-ratings) - MSCI AA, Sustainalytics 24.5, March 2026
- [Eni, ESG indexes and ratings](https://www.eni.com/en-IT/investors/rating-esg.html) - five providers side by side, March 2026
- [Berg, Kolbel & Rigobon, Aggregate Confusion, Review of Finance 26(6)](https://academic.oup.com/rof/article/26/6/1315/6590670) - 0.61, the three-way decomposition
