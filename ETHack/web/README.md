# web — the CONTESTED explorer

The specification curve, made movable. Every control changes the ranking in
front of you, and the point of the thing is which controls move it and by how
much.

## Run

```bash
python3 -m http.server 4173 --directory web
```

Then <http://localhost:4173>. Opening `index.html` straight off the filesystem
also works — the data ships as `data/speccurve.js`, a plain script that assigns
`window.SPECCURVE`, precisely so no server and no `fetch` are needed. No build
step, no dependencies, no network.

## Where the numbers come from

`speccurve/spec.py` runs steps 1 to 5 of the formula — exposure, window,
direction, orientation, normalisation — and `speccurve/export_web.py` writes the
result as a grade tensor:

```
G[spec][company][field]   0..100, 100 = best, null = not reported
```

None of those five steps involves the pillar weights, which is what makes this
page possible. Steps 6, 7 and 8 (the weighted composite, the rank percentile,
the median and IQR across specifications) run in `assets/compute.js`, live, in
the browser. Nothing is precomputed for a particular answer, and the arithmetic
is the same arithmetic: the page reproduces `speccurve/out/summary.csv` to 0.05
rank points on all twenty companies under the four published weightings.

Regenerate after any change to the formula or the data:

```bash
cd speccurve && python3 export_web.py        # -> ../web/data/speccurve.{json,js}
```

## Swapping in real data

Replace `dummy.build()` with a loader returning the same keys (documented in
`speccurve/README.md`), rerun `export_web.py`, reload the page. Set
`meta.real = true` in the export and the synthetic badge and the warning in the
footer disappear on their own. Nothing in `web/` is specific to twenty
companies, thirty fields or seventy-two specifications; every count is read from
`meta`.

## The controls, and why they are not all sliders

| Control | Varies | Why it is there |
|---|---|---|
| Pillar weight sliders | E / S / F | What everyone asks for first. Weights explain ~13% of the divergence between commercial raters. |
| Specification axes | exposure base, window, direction, normaliser, peer set | Scope and measurement — the other ~87%. A segmented control, not a slider, because these are choices rather than dials. |
| Missing data | excluded vs graded zero | One line in `composite()`. It reorders the table harder than any weight does. |
| Vary the weighting too | sweeps all 231 weight vectors | Turns the sliders into a distribution so their influence can be measured against the axes rather than argued about. |

Leaving an axis on **vary** puts every one of its options into the distribution.
Pinning all five leaves exactly one specification — one number, no error bar —
and the page says so, because that is the thing the project argues against.

## Files

| File | What it is |
|---|---|
| `index.html` | structure and the copy |
| `assets/compute.js` | steps 6–8 of the formula. A direct port of `spec.py`. |
| `assets/charts.js` | the four marks, hand-drawn in SVG. No chart library. |
| `assets/app.js` | state, controls, rendering |
| `assets/styles.css` | the palette committed in `speccurve/run.py`, so the page and the figures in the deck match |
| `data/speccurve.js` | the grade tensor, written by `export_web.py` |

## Design notes

- **Light theme** because the demo is projected in a bright room.
- **Two colour jobs, kept apart.** Three categorical hues for the pillars, each
  always shown beside its own label; one sequential ramp from neutral to orange
  for contestation, always shown beside the word *robust* / *contested* /
  *opinion*. Colour is never the only channel.
- **One vertical scale everywhere**: rank percentile, 0 to 100, 100 = best of
  the twenty. The table bar, the curve and the scatter can be read against each
  other without translating.
- **Rows animate when the ranking changes** — via the Web Animations API, so a
  render landing mid-animation cannot corrupt the layout. It is the one place
  motion carries information: you see a company overtake another because of a
  choice you just made.
