---
edit: owned
last_edited: 2026-09-12T20:05:00 CET
changes: 0
type: project-note
status: active
---
# Die Stichprobe und die 30 Faktoren

## 1. Die Industrie: S&P 500 Energy, alle davon

**Harte Tatsache: Integrated Oil & Gas im S&P 500 sind genau zwei Firmen, XOM und CVX.** Die Bloomberg-Peer-Group "Integrated Oils" aus unserem Export ist global (Shell, TotalEnergies, BP, Eni, Equinor, Suncor, Petrobras). Man kann nicht gleichzeitig im S&P 500 bleiben und diese Peer Group behalten.

Der Challenge-Brief sagt S&P 500. Also: **GICS-Sektor Energy, komplett.** Der Sektor hat nur 21 bis 22 Mitglieder, also heißt "die 20 größten" praktisch "der ganze Sektor minus die zwei kleinsten". Kein Ranking nötig, nur zwei Streichungen: **TPL** (Royalty-Gesellschaft, kein Betreiber) und **APA**.

Liste in `contested/companies21.csv`. Aufteilung:

| Sub-Group | n | Firmen |
|---|---|---|
| INT Integrated | 2 | XOM, CVX |
| EP Exploration & Production | 10 | COP, EOG, OXY, FANG, EXE, EQT, DVN, CTRA, APA, TPL |
| MID Storage & Transportation | 4 | WMB, KMI, OKE, TRGP |
| REF Refining & Marketing | 3 | MPC, PSX, VLO |
| SVC Equipment & Services | 3 | SLB, BKR, HAL |

CTRA noch gegen die aktuelle Indexliste prüfen.

**Der Sub-Group-Split ist kein Problem, er ist der intra-vs-inter-Test, den wir sowieso begründen mussten.** Innerhalb REF sind es 3 Peers, über den Sektor 21. Beide Vergleiche sind vertretbar, sie geben verschiedene Ränge, also ist es eine Spec-Dimension und kostet uns keine zusätzliche Arbeit.

**Und es produziert ein Ergebnis:** `F1284 embedded carbon in total reserves`, unser wichtigstes Umweltfeld, existiert nur für INT und EP. Das sind **11 von 22 Firmen**. Für Refining, Midstream und Services gibt es das Feld gar nicht. Das heißt: die Hälfte des Energiesektors kann auf der wichtigsten Klimadimension nicht bewertet werden, und jeder Anbieter, der trotzdem einen Score für sie veröffentlicht, füllt die Lücke mit einer Annahme, die er nicht ausweist.

Die globale Integrated-Oils-Gruppe bleibt als **Validierungsset** für die Equinor-AAA-Folie (siehe [[Efforts/Active/ETHack/divergence-sector|divergence-sector]]), nicht als Hauptstichprobe.

## 2. Die 30 Faktoren

Datei: `contested/factors30.csv`. Drei Slider à 10 Faktoren, gezogen aus den 135 nutzbaren Feldern des Bloomberg-Exports.

**E, 10 Faktoren, 9 Ergebnisse und 1 Versprechen:**
Scope 1 (F0947), embedded carbon in reserves (F1284), Scope 2 location (ES077), Gas flaring (ES027), Methananteil an Scope 1 (SA055), Spill-Volumen (ES249), Abwasser (ES018), Frischwasserentnahme (SA020), Sonderabfall (ES019), Net-Zero-Ziel behauptet (SA559).

Das Paar F1284 + SA559 ist die Pointe: behauptet Net Zero, während der Kohlenstoff in den Reserven um 4.8% steigt.

**S, 10 Faktoren, gebaut als Paare:**
TRIR Mitarbeiter (ES121) vs Contractors (ES261), LTIR Mitarbeiter (ES092) vs Contractors (ES260), Todesfallrate Mitarbeiter (F1442) vs Workforce (RX389), Tier-1-Prozesssicherheit (SA052), Trainingsausgaben pro Kopf (RX312), Menschenrechtspolicy (ES059), Policy für indigene Rechte (SA029).

Die Paare sind der Punkt: XOM meldet 0.10 TRIR für Mitarbeiter und 0.21 für Contractors, und die Todesfallrate für Contractors (F1443) meldet es **gar nicht**. Wer nur "Mitarbeiter" zählt, halbiert das Risiko per Definitionswahl.

**F, Financial Sustainability statt Governance, 10 Faktoren:**
Net Debt/EBITDA, EBIT/Zinsaufwand, FCF/Gesamtschuld, Capex/Abschreibungen, (Dividende+Rückkäufe)/FCF, Fälligkeiten unter 24 Monaten, Moody's Issuer Rating und Outlook, Moody's adjusted Debt/EBITDA, ROCE, Reserve Life.

Diese zehn kommen **nicht** aus der Materiality Map, sondern aus Bloomberg-Fundamentals und Moody's. Muss im Data Request extra angefordert werden.

**Reserve Life ist absichtlich drin und absichtlich umstritten.** Reserven geteilt durch Jahresproduktion ist gleichzeitig eine Finanzkennzahl (wie lange trägt das Geschäft) und eine Umweltkennzahl (wie viel Kohlenstoff ist zur Förderung vorgesehen). Hohe Reserve Life ist finanziell gut und ökologisch schlecht. **Damit ist sogar die Zuordnung eines Feldes zu einer Säule eine Specification**, und das ist die beste Einzelillustration unserer ganzen These.

## 3. Zahlen

30 Faktoren x 18 Specs = **540 Specs pro Firma**, 22 Firmen. Von den 30 gelten 25 für alle Sub-Groups, 5 nur für INT und EP (F1284, ES027, SA055, FIN08 und teilweise ES249). Coverage wird separat berichtet, nie in den Score eingerechnet.

## 4. Moody's-Regel

Moody's Rating und ESG Credit Impact Score sind **Referenzlinien im Chart, nie Inputs.** Sie sind aus denselben Feldern gebaut, die wir verwenden. Als Input wären sie Doppelzählung. Vor der Jury sagen, bevor gefragt wird.

Moody's **adjusted** Debt/EBITDA gegen Bloombergs Debt/EBITDA ist dagegen ein legitimer Input, und zwar als Measurement-Spec: dieselbe Kennzahl, zwei Anbieter, verschiedene Bereinigungen, verschiedene Zahl. Das ist die 50.1%-Ursache aus Berg et al., live und an einer Zahl, die jeder Finanzmensch im Raum sofort versteht.
