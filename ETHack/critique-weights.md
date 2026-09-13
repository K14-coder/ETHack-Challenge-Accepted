---
edit: owned
last_edited: 2026-09-12T20:05:00 CET
changes: 0
type: project-note
status: active
---
# Die Gewichtungs-Kritik, und warum sie unser Design nicht trifft

Kritik im Kern: wenn man alle möglichen Gewichte durchprobiert, bekommt man eine Verteilung um den Median, und der Median ist genau der ursprüngliche Score. Also kann man es auch gleich lassen. Und: "unterschiedliche Gewichte geben unterschiedliche Zahlen" ist keine Erkenntnis, das ist Arithmetik.

**Die Kritik ist richtig, aber sie beschreibt ein anderes Modell als unseres.**

## 1. Wo sie recht hat

Gewichte variieren heißt Konvexkombinationen derselben Indikatoren bilden. Jedes Ergebnis liegt in der konvexen Hülle der Indikatorränge. Viele Ziehungen konzentrieren sich um das gleichgewichtete Mittel. Das ist der zentrale Grenzwertsatz, und der Einwand ist mathematisch korrekt: **ein reines Weight-Multiverse ist wertlos.**

Zweiter Beleg, aus dem Paper auf dem wir stehen. Berg, Kölbel & Rigobon zerlegen die Divergenz zwischen Anbietern in drei Ursachen:

| Ursache | Anteil |
|---|---|
| Measurement (dieselbe Sache anders gemessen) | 50.1% |
| Scope (was überhaupt zählt) | 36.7% |
| **Weights (Gewichtung)** | **13.2%** |

Gewichte sind die **kleinste** der drei Ursachen. Wer nur Gewichte variiert, greift 13% des Problems an und lässt 87% liegen. Das ist genau das, was die Kritik meint, und sie liegt damit richtig.

## 2. Wo sie unser Design verfehlt

Unsere 18 Specs pro Feld enthalten **keine einzige Gewichtsdimension.** Variiert wird:

- **Boundary / Scope** — Scope 1 vs Scope 1+2 vs plus embedded carbon in reserves
- **Reference** — Absolutwert vs Veränderung über 5 Jahre vs Niveau im letzten Jahr
- **Exposure base** — pro Umsatz, pro boe Produktion, pro Mitarbeiter, pro Marktkapitalisierung
- **Source of truth** — Bloomberg-Feld vs behördlich gemeldeter Wert vs modellierter Wert
- **Polarity** — bei umstrittenen Feldern die Richtung selbst

Das sind Scope- und Measurement-Dimensionen. Also die 86.8%, nicht die 13.2%.

## 3. Warum sich das nicht wegmittelt

Drei Gründe, und der dritte ist der harte.

**Scope ändert die Indikatormenge, nicht die Mischung.** XOM: Scope 1 fällt um 8.2%, embedded carbon in reserves steigt um 4.8%, und die Reservenbasis ist 83x größer. Keine Konvexkombination von "nur Scope 1" kann das reserveninklusive Ergebnis erzeugen. Die Verteilungen sind nicht verschachtelt, also gibt es keinen gemeinsamen Median, um den sie konzentrieren könnten.

**Nenner sind nicht-monotone Transformationen.** Ein Wechsel von "pro Umsatz" auf "pro boe" kann eine Rangordnung umdrehen. Konvexe Gewichtung kann eine Ordnung nie umdrehen, sie kann sie nur stauchen.

**Empirisch, aus unserem eigenen Lauf:** die minimale Spearman-Korrelation zwischen zwei unserer eigenen Specs ist **−0.148.** Eine Normalverteilung um einen Median kann keine negative Rangkorrelation zwischen zwei Ziehungen erzeugen. Negativ heißt: die beiden Specs sind sich über die **Reihenfolge** uneinig, nicht nur über das Niveau. Damit ist der Einwand mit unseren eigenen Zahlen widerlegt, nicht mit einem Argument.

Zum Vergleich: die Anbieter untereinander liegen bei 0.61 (Berg et al.) bzw. 0.45 (Dimson, Marsh & Staunton). Wir sind schlechter als sie, weil wir ehrlich über die Bandbreite sind, statt einen Punkt daraus zu veröffentlichen.

## 4. Scores oder Ranks: beides, getrennt

Der Einwand "was wenn alle scheiße sind" ist berechtigt und Ränge verstecken das. Also zwei Zahlen pro Firma, nie eine:

- **Rangverteilung** über alle Specs — relativ, sagt "wer ist besser als wer"
- **Absolute Intensität** (z.B. tCO2e pro Mio. USD Umsatz) mit Peer-Median als Referenzlinie — sagt "ist überhaupt irgendwer gut"

Wenn die ganze Branche über jedem Benchmark liegt, steht das im zweiten Panel und nicht im Rang.

## 5. Der Slider: ja, aber als zweite Ansicht

Slider und Specification Curve sind dasselbe Objekt von zwei Seiten. **Die Curve ist die Menge aller Sliderpositionen. Der Slider ist ein Punkt darin.** Die Curve ist gebaut, der Slider ist danach ein Lookup über dasselbe Grid. Kein neues Modell, nur ein neues Frontend.

Zwei Regeln dafür:

1. **Der Slider darf nicht nur über Gewichte gehen.** Sonst ist es genau die 13%-Falle, die die Kritik beschreibt. Der mächtigste Regler ist kein Regler, sondern ein **Schalter**: "Reserven mitzählen: ja / nein". Der dreht die Rangliste, ein Gewichtsregler nicht.
2. **Reihenfolge im Pitch:** erst "bei diesen Firmen ist das Urteil robust über alle vertretbaren Methoden, bei diesen kippt es", dann "und hier ist dein eigener Regler". Nicht umgekehrt. Der Slider allein ist ein Spielzeug, die Robustheitsaussage ist das Produkt.

## 6. Die Antwort auf "was bringt es" in einem Satz

Es trennt die Firmen, bei denen jede vertretbare Methode dasselbe Urteil liefert, von denen, bei denen das Rating eine Meinung ist. Das Erste ist investierbare Information, das Zweite ist ein Warnschild. Kein Anbieter liefert diese Trennung, weil jeder genau einen Punkt aus der Verteilung veröffentlicht und den Rest wegwirft.

## 7. Was die Kritik uns tatsächlich gekostet hat

Nichts am Code. Eine Formulierung im Pitch: wir sagen nie wieder "wir variieren die Gewichtung". Wir sagen "wir variieren Scope und Messung, also die 87% der Divergenz, die die Gewichtung nicht erklärt". Wer "Gewichte" hört, denkt an den zentralen Grenzwertsatz und hat uns in zehn Sekunden erledigt.
