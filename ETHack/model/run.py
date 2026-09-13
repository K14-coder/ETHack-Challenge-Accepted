"""
run.py — every specification, and the four outputs.

    python3 run.py                 # the full 17,496
    python3 run.py --quick         # orthodox polarity only, 5,832

Writes into out/ :
    summary.csv      one row per company: consensus, contestation, verdict, coverage
    long.csv         one row per company per specification. The audit trail.
    pivot.csv        variance decomposition: which axis decides each company
    dominance.csv    P(i outranks j) for every pair
    remedy.csv       the missing disclosure that would remove the most contestation
    claims.json      the numbers that go on the slide, computed

The output is not a score and not only a distribution. It is four objects:

    settled     which comparisons hold under every defensible method
    contested   which do not
    pivot       which single choice decides the rest
    remedy      which missing disclosure would end the disagreement
"""

import argparse
import json
import os
import warnings
from itertools import product

import numpy as np
import pandas as pd

import load
import spec

warnings.filterwarnings("ignore", message="Mean of empty slice")
warnings.filterwarnings("ignore", category=RuntimeWarning)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

STEP6_AXES = ("inclusion", "missing", "aggregator")
ALL_AXES = spec.GRID_AXES + ("polarity",) + STEP6_AXES


def run_all(data, weights, polarities=None):
    """Every specification. Returns R (S, N) rank percentiles and the spec table."""
    polarities = polarities or spec.POLARITIES
    f = data["fields"]
    pil = f.pillar.values
    tiers = f.tier.values
    reported = np.isfinite(data["VAR"][:, :, :, 0]).any(axis=2)
    N = len(data["names"])

    # the inclusion mask depends on the peer scheme, so it is built per scheme
    masks = {(p, lv): spec.inclusion_mask(reported, data["peers"][p], tiers, lv)
             for p in spec.PEERSETS for lv in spec.INCLUSIONS}

    tensors = {}
    for pol in polarities:
        G, grid = spec.grade_tensor(data, pol)
        tensors[pol] = G

    rows, R = [], []
    for pol in polarities:
        G = tensors[pol]
        for s in grid:
            S = G[s["spec_id"]]
            for lv, miss, agg in product(spec.INCLUSIONS, spec.MISSINGS, spec.AGGREGATORS):
                P, T = spec.composite(S, pil, masks[(s["peerset"], lv)],
                                      weights, miss, agg)
                R.append(spec.rank_percentile(T))
                rows.append(dict(polarity=pol, inclusion=lv, missing=miss,
                                 aggregator=agg,
                                 **{a: s[a] for a in spec.GRID_AXES}))
    return np.array(R), pd.DataFrame(rows), tensors, masks


# ------------------------------------------------------------------ outputs

def summarise(R, names, groups, coverage):
    step = 100.0 / (len(names) - 1)          # one rank position, in points
    out = []
    for i, n in enumerate(names):
        v = R[:, i]
        v = v[np.isfinite(v)]
        if not len(v):
            out.append(dict(ticker=n, peer_group=groups[i], n_scores=0))
            continue
        p25, p50, p75 = np.percentile(v, [25, 50, 75])
        iqr = p75 - p25
        out.append(dict(
            ticker=n, peer_group=groups[i], n_scores=len(v),
            consensus=round(p50, 1), contestation=round(iqr, 1),
            p25=round(p25, 1), p75=round(p75, 1),
            rank_min=round(v.min(), 1), rank_max=round(v.max(), 1),
            range=round(v.max() - v.min(), 1),
            positions=round(iqr / (100 / (len(names) - 1)), 1),
            coverage_pct=round(coverage[i], 1),
            # thresholds in RANK POSITIONS, not percentile points. With N=18 a
            # percentile can only take 18 values 5.88 apart, so an IQR quoted in
            # points is a quantised quantity dressed up as a continuous one.
            verdict="robust" if iqr < 1.5 * step else
                    "contested" if iqr < 3.0 * step else "opinion",
        ))
    return pd.DataFrame(out).sort_values("consensus", ascending=False,
                                         na_position="last")


def pivot(R, specs, names):
    """
    Which axis decides this company's rating.

    The grid is a complete balanced factorial, so the variance of a company's
    rank percentile decomposes into main effects with no design correction.
    eta2 = SS(axis) / SS(total).
    """
    rows = []
    for i, n in enumerate(names):
        v = R[:, i]
        ok = np.isfinite(v)
        if ok.sum() < 2:
            continue
        y = v[ok]
        sub = specs[ok]
        gm = y.mean()
        sst = ((y - gm) ** 2).sum()
        r = dict(ticker=n, total_sd=round(y.std(), 2))
        if sst <= 0:
            rows.append(r)
            continue
        for a in ALL_AXES:
            ss = 0.0
            for lvl, idx in sub.groupby(a).indices.items():
                ss += len(idx) * (y[idx].mean() - gm) ** 2
            r[a] = round(100 * ss / sst, 1)
        top = max(ALL_AXES, key=lambda a: r.get(a, 0))
        r["pivot_axis"] = top
        r["pivot_pct"] = r.get(top, 0)
        rows.append(r)
    return pd.DataFrame(rows)


def dominance(R, names):
    """P(i outranks j) over every specification both companies score in."""
    N = len(names)
    D = np.full((N, N), np.nan)
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            ok = np.isfinite(R[:, i]) & np.isfinite(R[:, j])
            if ok.sum() == 0:
                continue
            D[i, j] = (R[ok, i] > R[ok, j]).mean()
    return pd.DataFrame(D, index=names, columns=names)


def remedy(data, R_base, weights, masks, tensors, names, top_n=3):
    """
    The disclosure that would end the disagreement.

    For each field a company does not report, ask what its contestation would be
    if that one silence were filled. We cannot know the value, so we do the
    honest thing and remove the *ambiguity* instead: hold the missing-data rule
    fixed at each of its three settings and see how much of the spread was
    attributable to not knowing. The field whose silence carries the most spread
    is the one worth demanding.
    """
    f = data["fields"]
    pil = f.pillar.values
    reported = np.isfinite(data["VAR"][:, :, :, 0]).any(axis=2)
    G = tensors["orthodox"]
    grid = spec.spec_grid()
    out = []

    for i, n in enumerate(names):
        base = R_base[:, i]
        base = base[np.isfinite(base)]
        if not len(base):
            continue
        base_iqr = np.subtract(*np.percentile(base, [75, 25]))
        cand = []
        for j in np.where(~reported[i])[0]:
            vals = []
            for s in grid[::6]:                      # every 6th cell, for speed
                S = G[s["spec_id"]].copy()
                for miss in spec.MISSINGS:
                    m = masks[(s["peerset"], "permissive")].copy()
                    m[i, j] = False                  # take this silence out of the model
                    _, T = spec.composite(S, pil, m, weights, miss, "arithmetic")
                    r = spec.rank_percentile(T)
                    if np.isfinite(r[i]):
                        vals.append(r[i])
            if len(vals) < 4:
                continue
            iqr = np.subtract(*np.percentile(vals, [75, 25]))
            cand.append((base_iqr - iqr, f.index[j], f.iloc[j]["name"]))
        cand.sort(reverse=True)
        for drop, fid, nm in cand[:top_n]:
            out.append(dict(ticker=n, field_id=fid, field=nm,
                            contestation_removed=round(float(drop), 1)))
    return pd.DataFrame(out)


# --------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true",
                    help="orthodox polarity only")
    ap.add_argument("--weighting", default="equal", choices=list(spec.WEIGHTINGS))
    a = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    d = load.build()
    names, f = d["names"], d["fields"]
    w = spec.WEIGHTINGS[a.weighting]
    pols = ["orthodox"] if a.quick else spec.POLARITIES

    print(f"{len(names)} companies x {len(f)} fields x {len(d['years'])} years")
    R, specs, tensors, masks = run_all(d, w, pols)
    print(f"{R.shape[0]:,} specifications, weighting = {a.weighting}")

    reported = np.isfinite(d["VAR"][:, :, :, 0]).any(axis=2)
    coverage = 100 * reported.mean(axis=1)

    s = summarise(R, names, d["peers"]["subgroup"], coverage)
    s.to_csv(f"{OUT}/summary.csv", index=False)

    p = pivot(R, specs, names)
    p.to_csv(f"{OUT}/pivot.csv", index=False)

    D = dominance(R, names)
    D.round(3).to_csv(f"{OUT}/dominance.csv")

    lo = specs.copy()
    for i, n in enumerate(names):
        lo[n] = np.round(R[:, i], 2)
    lo.to_csv(f"{OUT}/long.csv", index=False)

    rem = remedy(d, R, w, masks, tensors, names)
    rem.to_csv(f"{OUT}/remedy.csv", index=False)

    # ---- the claims, computed
    off = D.values[~np.eye(len(names), dtype=bool)]
    off = off[np.isfinite(off)]
    settled = int((off > 0.95).sum())
    pairs = len(off) // 2
    claims = dict(
        n_companies=len(names), n_fields=int(len(f)),
        n_specifications=int(R.shape[0]),
        axes={ax: (list(spec.POLARITIES) if ax == "polarity"
                   else list(getattr(spec, ax.upper() + "S", []))
                   or list(getattr(spec, ax.upper() + "ES", [])))
              for ax in ALL_AXES},
        median_contestation=round(float(s.contestation.median()), 1),
        median_contestation_positions=round(float(s.positions.median()), 1),
        widest=dict(ticker=str(s.iloc[s.range.values.argmax()].ticker),
                    range=float(s.range.max())),
        settled_pairs=settled, total_pairs=pairs,
        settled_share=round(settled / pairs, 3) if pairs else None,
        pivot_counts=p["pivot_axis"].value_counts().to_dict() if "pivot_axis" in p else {},
        rank_resolution=round(100 / (len(names) - 1), 2),
    )
    with open(f"{OUT}/claims.json", "w") as fh:
        json.dump(claims, fh, indent=2)

    # ---- console
    print(f"\n{'':5}{'cons':>6}{'IQR':>7}{'pos':>6}{'range':>7}  {'verdict':<10}{'pivot':<12}{'%':>5}")
    pv = p.set_index("ticker")
    for _, r in s.iterrows():
        q = pv.loc[r.ticker] if r.ticker in pv.index else None
        print(f"{r.ticker:5}{r.consensus:6.1f}{r.contestation:7.1f}{r.positions:6.1f}"
              f"{r.range:7.1f}  {r.verdict:<10}"
              f"{(q['pivot_axis'] if q is not None else ''):<12}"
              f"{(q['pivot_pct'] if q is not None else 0):5.0f}")

    print(f"\nsettled pairwise comparisons: {settled} of {pairs} "
          f"({100*settled/pairs:.0f}%). A published ranking asserts all {pairs}.")
    print(f"median contestation: {claims['median_contestation']} rank points "
          f"= {claims['median_contestation_positions']} positions of {len(names)}")
    print(f"rank resolution with N={len(names)}: {claims['rank_resolution']} points per position")
    print(f"\nwrote {OUT}/")


if __name__ == "__main__":
    main()
