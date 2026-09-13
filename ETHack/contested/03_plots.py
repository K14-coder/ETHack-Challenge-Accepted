#!/usr/bin/env python3
"""
CONTESTED - step 3: the figures.

    python3 03_plots.py
    python3 03_plots.py --hero WMT      pick the company for Figure 1

Writes PNG at slide resolution into out/.
Palette is CVD-validated: blue #2a78d6, orange #eb6834, aqua #1baf7a.
"""
import csv, sys, math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path("out")
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, RULE     = "#13171a", "#59616a", "#dce1e6"
plt.rcParams.update({
    "figure.dpi": 160, "savefig.dpi": 160, "savefig.bbox": "tight",
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.edgecolor": RULE, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": "white", "axes.facecolor": "white",
})

def num(v):
    try: return float(v) if v not in (None, "", "None") else None
    except ValueError: return None

def load():
    long_ = list(csv.DictReader(open(OUT / "long.csv")))
    summ  = list(csv.DictReader(open(OUT / "summary.csv")))
    for r in long_:
        r["rank"] = num(r["rank"]); r["intensity"] = num(r["intensity"]); r["spec_id"] = int(r["spec_id"])
    for r in summ:
        for k in ("consensus_rank","contestation_iqr","rank_min","rank_max","rank_range",
                  "disclosed_t","modelled_t","revenue_usd","modelled_over_disclosed"):
            r[k] = num(r[k])
    return long_, summ

DIMS = [("boundary", ["A_disclosed","C_modelled"]),
        ("missing_rule", ["exclude","worst_case","modelled"]),
        ("margins", ["with","without"]),
        ("denominator", ["revenue","market_cap"])]

# --------------------------------------------------------------- Figure 1
def fig1(long_, summ, hero):
    pts = sorted([r for r in long_ if r["ticker"] == hero and r["rank"] is not None],
                 key=lambda r: r["rank"])
    if len(pts) < 2:
        print(f"  fig1 skipped: {hero} is ranked in only {len(pts)} specification(s)"); return
    name = next((s["company"] for s in summ if s["ticker"] == hero), hero)
    n = len(pts)
    rows = sum(len(v) for _, v in DIMS)

    fig, (ax, dash) = plt.subplots(2, 1, figsize=(11, 7),
                                   gridspec_kw={"height_ratios": [3, 1.5], "hspace": 0.18})
    x = range(n); y = [p["rank"] for p in pts]
    lo, hi = min(y), max(y)
    ax.fill_between([-0.5, n-0.5], lo, hi, color=BLUE, alpha=0.09, zorder=0)
    ax.plot(x, y, "-", color=BLUE, lw=2, zorder=2)
    ax.plot(x, y, "o", color=BLUE, ms=6, mec="white", mew=1.4, zorder=3)
    ax.invert_yaxis()
    ax.set_ylabel("Rank   (1 = cleanest)")
    ax.set_title(f"{name}: {n} defensible specifications, {int(hi-lo)} rank places apart",
                 loc="left", fontsize=13, fontweight="bold", pad=12)
    ax.annotate(f"rank {int(y[0])}", (0, y[0]), xytext=(10, 0), textcoords="offset points",
                va="center", fontsize=9, color=INK)
    ax.annotate(f"rank {int(y[-1])}", (n-1, y[-1]), xytext=(-10, 0), textcoords="offset points",
                va="center", ha="right", fontsize=9, color=INK)
    ax.set_xlim(-0.5, n-0.5); ax.set_xticks([])
    ax.grid(axis="y", color=RULE, lw=0.6)

    dash.set_xlim(-0.5, n-0.5); dash.set_ylim(rows, 0)
    dash.set_xticks([]); dash.set_yticks([]); [s.set_visible(False) for s in dash.spines.values()]
    ri = 0
    for dim, opts in DIMS:
        for opt in opts:
            for i, p in enumerate(pts):
                on = p[dim] == opt
                dash.add_patch(Rectangle((i-0.42, ri+0.15), 0.84, 0.7,
                                         facecolor=BLUE if on else "#e2e7eb", lw=0))
            dash.text(-0.7, ri+0.5, opt.replace("_", " "), ha="right", va="center",
                      fontsize=7.5, color=INK2)
            ri += 1
        dash.axhline(ri, color=RULE, lw=0.6)
    dash.text(-0.7, -0.55, "which choice produced each column", ha="right",
              fontsize=7.5, color=INK2, style="italic")
    fig.savefig(OUT / "fig1_specification_curve.png"); plt.close(fig)
    print(f"  fig1_specification_curve.png   {name}, {n} specs, range {int(hi-lo)}")

# --------------------------------------------------------------- Figure 2
def fig2(summ):
    d = [s for s in summ if s["consensus_rank"] is not None and s["rank_range"] is not None]
    if len(d) < 3:
        print("  fig2 skipped: too few ranked companies"); return
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.scatter([s["consensus_rank"] for s in d], [s["rank_range"] for s in d],
               s=70, color=BLUE, alpha=0.75, edgecolor="white", lw=1.2, zorder=3)
    for s in d:
        ax.annotate(s["ticker"], (s["consensus_rank"], s["rank_range"]),
                    xytext=(0, 9), textcoords="offset points", ha="center",
                    fontsize=7.5, color=INK)
    ax.set_xlabel("Consensus rank   (median across specifications, 1 = cleanest)")
    ax.set_ylabel("Contestation   (rank places travelled)")
    ax.set_title("Where the ranking is real, and where it is an artifact of method choice",
                 loc="left", fontsize=13, fontweight="bold", pad=12)
    ax.grid(color=RULE, lw=0.6)
    top = max(s["rank_range"] for s in d)
    ax.axhline(top*0.55, color=ORANGE, lw=1.2, ls="--", zorder=1)
    ax.text(ax.get_xlim()[1], top*0.55, " the number is a choice ", ha="right", va="bottom",
            fontsize=8, color=ORANGE)
    fig.savefig(OUT / "fig2_contestation_map.png"); plt.close(fig)
    print(f"  fig2_contestation_map.png      {len(d)} companies")

# --------------------------------------------------------------- Figure 3
def fig3(summ):
    d = [s for s in summ if s["disclosed_t"] and s["modelled_t"] and s["revenue_usd"]]
    nod = [s for s in summ if not s["disclosed_t"] and s["modelled_t"]]
    if not d:
        print("  fig3 skipped: no company has both a disclosed and a modelled figure"); return
    d.sort(key=lambda s: -s["modelled_over_disclosed"])
    fig, ax = plt.subplots(figsize=(11, max(3.2, 0.36*len(d)+1.6)))
    yy = range(len(d))
    for i, s in enumerate(d):
        ax.plot([s["disclosed_t"], s["modelled_t"]], [i, i], color=RULE, lw=2.5, zorder=1,
                solid_capstyle="round")
    ax.scatter([s["disclosed_t"] for s in d], yy, s=62, color=AQUA, zorder=3,
               edgecolor="white", lw=1.2, label="reported to EPA")
    ax.scatter([s["modelled_t"] for s in d], yy, s=62, color=ORANGE, zorder=3,
               edgecolor="white", lw=1.2, label="estimated, whole supply chain")
    for i, s in enumerate(d):
        ax.annotate(f"{s['modelled_over_disclosed']:.0f}x", (s["modelled_t"], i),
                    xytext=(9, 0), textcoords="offset points", va="center",
                    fontsize=8, color=INK, fontweight="bold")
    ax.set_yticks(list(yy)); ax.set_yticklabels([s["ticker"] for s in d])
    ax.set_xscale("log"); ax.set_xlabel("tonnes CO2e, log scale")
    ax.set_title("The gap between what must be disclosed and what is plausibly caused",
                 loc="left", fontsize=13, fontweight="bold", pad=12)
    ax.grid(axis="x", color=RULE, lw=0.6)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2)
    x0, x1 = ax.get_xlim(); ax.set_xlim(x0, x1 * 2.2)          # room for the ratio labels
    ax.set_ylim(-0.7, len(d) - 0.3)
    if nod:
        ax.text(0.0, 1.02, "no disclosed figure at all: " + ", ".join(s["ticker"] for s in nod),
                transform=ax.transAxes, fontsize=8.5, color=ORANGE, fontweight="bold")
    fig.savefig(OUT / "fig3_disclosure_gap.png"); plt.close(fig)
    print(f"  fig3_disclosure_gap.png        {len(d)} companies, {len(nod)} with no figure")

if __name__ == "__main__":
    long_, summ = load()
    hero = "WMT"
    if "--hero" in sys.argv: hero = sys.argv[sys.argv.index("--hero")+1].upper()
    else:
        ranked = [s for s in summ if s["rank_range"] is not None]
        if ranked: hero = max(ranked, key=lambda s: s["rank_range"])["ticker"]
    print("figures:")
    fig1(long_, summ, hero); fig2(summ); fig3(summ)
    print(f"\nall in {OUT.resolve()}")
