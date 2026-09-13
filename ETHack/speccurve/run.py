"""
run.py — build the dummy data, run all 288 scores, write the CSVs and the figures.

    python3 run.py                 # dummy data
    python3 run.py --seed 12       # a different dummy draw

Outputs, all in out/ :
    scores_long.csv   one row per company x specification x weighting  (20 * 288)
    summary.csv       one row per company: consensus, spread, quartiles, coverage
    fig1_curves.png   the 288 rank percentiles per company, sorted, highest left
    fig2_small_multiples.png   the same, one panel per company, shapes comparable
    fig3_scatter.png  consensus rank percentile against spread
"""

import argparse
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import dummy
import spec

OUT = "out"

# validated categorical palette, light mode (see dataviz reference palette)
SURFACE   = "#fcfcfb"
INK       = "#0b0b0b"
INK2      = "#52514e"
INK3      = "#8a8a85"
GRID      = "#e3e2de"
SERIES    = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
GHOST     = "#cfcec9"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "font.size": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "grid.color": GRID, "grid.linewidth": 0.6,
})



def titled(ax, title, subtitle):
    ax.set_title(title, fontsize=13, fontweight="bold", loc="left", pad=34)
    ax.text(0, 1.015, subtitle, transform=ax.transAxes, fontsize=9,
            color=INK2, va="bottom")


def declutter(ax, xs, ys, labels, color=INK2, fontsize=7.5):
    """Place point labels without overlaps. Greedy, in x order."""
    inv = ax.transData.transform
    placed = []
    cands = [(0, 11), (0, -16), (16, 4), (-16, 4), (0, 24), (0, -29),
             (26, 12), (-26, 12), (26, -12), (-26, -12)]
    w, h = 30.0, 11.0
    for i in np.argsort(xs):
        px, py = inv((xs[i], ys[i]))
        for dx, dy in cands:
            bx, by = px + dx, py + dy
            if all(abs(bx - qx) > w or abs(by - qy) > h for qx, qy in placed):
                placed.append((bx, by))
                ha = "center" if dx == 0 else ("left" if dx > 0 else "right")
                ax.annotate(labels[i], (xs[i], ys[i]), xytext=(dx, dy),
                            textcoords="offset points", ha=ha, va="center",
                            fontsize=fontsize, color=color)
                break


def main(seed):
    os.makedirs(OUT, exist_ok=True)
    d = dummy.build(seed)

    R, grid, wnames = spec.run_all(
        d["RAW"], d["BASE"], d["ftype"], d["pol"], d["pillar"], d["groups"])

    names, groups = d["names"], d["groups"]
    N, S, K = R.shape
    flat = R.reshape(N, S * K)                       # 288 numbers per company

    cons = np.nanmedian(flat, axis=1)
    p25  = np.nanpercentile(flat, 25, axis=1)
    p75  = np.nanpercentile(flat, 75, axis=1)
    iqr  = p75 - p25
    lo   = np.nanmin(flat, axis=1)
    hi   = np.nanmax(flat, axis=1)
    cov  = np.isfinite(d["RAW"][:, :, :, 0]).mean(axis=(1, 2)) * 100

    # ---------------------------------------------------------------- CSVs
    with open(f"{OUT}/scores_long.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["company", "subgroup", "spec_id", "base", "window", "direction",
                    "normalizer", "peerset", "weighting", "rank_pct"])
        for i in range(N):
            for s in grid:
                for k, wn in enumerate(wnames):
                    v = R[i, s["spec_id"], k]
                    w.writerow([names[i], groups[i], s["spec_id"], s["base"],
                                s["window"], s["direction"], s["normalizer"],
                                s["peerset"], wn,
                                "" if not np.isfinite(v) else round(float(v), 4)])

    order = np.argsort(-cons)
    with open(f"{OUT}/summary.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["company", "subgroup", "consensus_rank_pct", "spread_iqr",
                    "p25", "p75", "min", "max", "n_scores", "coverage_pct", "verdict"])
        for i in order:
            n_ok = int(np.isfinite(flat[i]).sum())
            verdict = ("robust" if iqr[i] < 12 else
                       "contested" if iqr[i] < 25 else "opinion")
            w.writerow([names[i], groups[i], round(cons[i], 1), round(iqr[i], 1),
                        round(p25[i], 1), round(p75[i], 1), round(lo[i], 1),
                        round(hi[i], 1), n_ok, round(cov[i], 1), verdict])

    # ------------------------------------------------------- fig 1, overlay
    curves = [np.sort(flat[i][np.isfinite(flat[i])])[::-1] for i in range(N)]

    # highlight the two tightest and the two widest spreads
    focus = [int(j) for j in np.argsort(iqr)[:2]] + [int(j) for j in np.argsort(-iqr)[:2]]
    fcol = {focus[0]: SERIES[0], focus[1]: SERIES[2],
            focus[2]: SERIES[1], focus[3]: SERIES[3]}

    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.axvspan(25, 75, color="#f0efe9", zorder=0)
    for i in range(N):
        if i in fcol:
            continue
        c = curves[i]
        ax.plot(np.linspace(0, 100, len(c)), c, color=GHOST, lw=1.0, zorder=1)

    ends = []
    for i in focus:
        c = curves[i]
        ax.plot(np.linspace(0, 100, len(c)), c, color=fcol[i], lw=2.0, zorder=3,
                label=f"{names[i]}   consensus {cons[i]:.0f},  spread {iqr[i]:.0f}")
        ends.append((c[-1], i))

    # vertical declutter of the end labels
    ends.sort()
    prev = -99.0
    for y, i in ends:
        y2 = max(y, prev + 5.0)
        ax.annotate(names[i], (100, y2), xytext=(8, 0), textcoords="offset points",
                    color=fcol[i], fontsize=8, va="center", fontweight="bold")
        prev = y2

    ax.set_xlim(-1, 108)
    ax.set_ylim(-3, 103)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["best\nspec", "25%", "50%", "75%", "worst\nspec"])
    ax.grid(axis="y", zorder=0)
    ax.set_xlabel("the 288 defensible ways to compute the score, sorted best to worst for that company")
    ax.set_ylabel("rank percentile  (100 = best of 20)")
    titled(ax, "Every company's score is a curve, not a number",
           "Shaded band = the middle half of the specifications. Its height is the spread. "
           "Flat = robust, steep = a methodological choice.")
    ax.legend(frameon=False, loc="lower left", fontsize=8, labelcolor=INK2)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig1_curves.png", dpi=180)
    plt.close(fig)

    # ----------------------------------------- fig 2, small multiples
    med_curve = np.nanmedian(np.array([
        np.pad(np.asarray(curves[i], float), (0, S * K - len(curves[i])),
               constant_values=np.nan) for i in range(N)]), axis=0)

    fig, axes = plt.subplots(4, 5, figsize=(13, 8.5), sharex=True, sharey=True)
    gcols = {g: SERIES[j] for j, g in enumerate(sorted(set(groups)))}
    for ax, i in zip(axes.ravel(), order):
        c = np.asarray(curves[i], float)
        ax.plot(np.arange(1, S * K + 1), med_curve, color=GHOST, lw=1.2, zorder=1)
        ax.plot(np.arange(1, len(c) + 1), c, color=gcols[groups[i]], lw=1.8, zorder=2)
        ax.set_title(f"{names[i]}   {cons[i]:.0f} ± {iqr[i]:.0f}",
                     fontsize=9, loc="left", color=INK)
        ax.set_ylim(-3, 103)
        ax.set_yticks([0, 50, 100])
        ax.set_xticks([])
        ax.grid(axis="y", zorder=0)
    handles = [plt.Line2D([], [], color=gcols[g], lw=2, label=g) for g in sorted(set(groups))]
    handles.append(plt.Line2D([], [], color=GHOST, lw=1.2, label="sector median curve"))
    fig.legend(handles=handles, frameon=False, ncol=6, loc="lower center",
               fontsize=9, labelcolor=INK2, bbox_to_anchor=(0.5, -0.005))
    fig.suptitle("Same axes for all 20, so the shapes are comparable",
                 fontsize=13, fontweight="bold", x=0.012, ha="left", y=0.985)
    fig.tight_layout(rect=[0, 0.035, 1, 0.955])
    fig.savefig(f"{OUT}/fig2_small_multiples.png", dpi=170)
    plt.close(fig)

    # ----------------------------------------------- fig 3, consensus vs spread
    fig, ax = plt.subplots(figsize=(9, 6.4))
    mx, my = float(np.nanmedian(cons)), float(np.nanmedian(iqr))
    ax.axvline(mx, color=GRID, lw=1.2, zorder=0)
    ax.axhline(my, color=GRID, lw=1.2, zorder=0)

    ax.scatter(cons, iqr, s=80, color=SERIES[0], edgecolor=SURFACE,
               linewidth=2, zorder=3)
    # companies landing on exactly the same (consensus, spread) share one label
    groups_xy = {}
    for i in range(N):
        groups_xy.setdefault((round(cons[i], 2), round(iqr[i], 2)), []).append(names[i])
    gx = np.array([k[0] for k in groups_xy])
    gy = np.array([k[1] for k in groups_xy])
    gl = [", ".join(v) for v in groups_xy.values()]
    declutter(ax, gx, gy, gl)

    pad_x = (np.nanmax(cons) - np.nanmin(cons)) * 0.12 + 2
    pad_y = (np.nanmax(iqr) - np.nanmin(iqr)) * 0.18 + 1
    x0, x1 = np.nanmin(cons) - pad_x, np.nanmax(cons) + pad_x
    y0, y1 = np.nanmin(iqr) - pad_y, np.nanmax(iqr) + pad_y
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)

    for tx, ty, txt, ha, va in [
        (x1, y0, "robustly strong\nbuy the story", "right", "bottom"),
        (x0, y0, "robustly weak\nno argument to be had", "left", "bottom"),
        (x1, y1, "looks strong, but only\nunder some methods", "right", "top"),
        (x0, y1, "looks weak, but only\nunder some methods", "left", "top")]:
        ax.text(tx, ty, txt, ha=ha, va=va, fontsize=8.5, color=INK3, style="italic")

    ax.grid(axis="y", zorder=0)
    ax.set_xlabel("consensus  =  median rank percentile over all 288 scores")
    ax.set_ylabel("spread  =  interquartile range of those 288 scores")
    titled(ax, "How good, and how much that depends on who is asking",
           "Right is better. Low is trustworthy. A company high on this axis has no single sustainability score.")
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig3_scatter.png", dpi=180)
    plt.close(fig)

    # ---------------------------------------------------------------- console
    print(f"specs {S}  x weightings {K}  =  {S*K} scores per company, {N} companies")
    print(f"{'company':9}{'grp':5}{'consensus':>10}{'spread':>8}{'min':>7}{'max':>7}"
          f"{'cov%':>7}  verdict")
    for i in order:
        v = ("robust" if iqr[i] < 12 else "contested" if iqr[i] < 25 else "opinion")
        print(f"{names[i]:9}{groups[i]:5}{cons[i]:10.1f}{iqr[i]:8.1f}"
              f"{lo[i]:7.1f}{hi[i]:7.1f}{cov[i]:7.1f}  {v}")

    # the headline robustness statistic: worst disagreement between two specs
    A = flat[:, :]
    keep = np.isfinite(A).all(axis=0)
    B = A[:, keep]
    print(f"\ncolumns usable for correlation: {B.shape[1]} of {S*K}")
    if B.shape[1] > 1:
        rk = np.apply_along_axis(spec.avg_rank, 0, -B)
        C = np.corrcoef(rk.T)
        iu = np.triu_indices(C.shape[0], 1)
        print(f"Spearman between two defensible specifications:"
              f"  min {C[iu].min():.3f}   median {np.median(C[iu]):.3f}   max {C[iu].max():.3f}")
        print("(published inter-provider benchmarks: 0.61 Berg et al., 0.45 Dimson et al.)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=7)
    main(ap.parse_args().seed)
