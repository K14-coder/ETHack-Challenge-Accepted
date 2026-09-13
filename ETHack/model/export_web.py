"""
export_web.py — the pillar-score cube for the browser explorer.

The pillar weights enter only at the very last step, so everything a user can
move with a slider lives downstream of a cube that can be computed once:

    P[spec][company][pillar]     0..100, null where the company has no score

`spec` runs over the full 17,496-cell grid in a canonical nested-product order,
so the browser reconstructs the whole specification table from the axis lists
alone and no spec metadata has to be shipped:

    polarity x base x window x direction x normalizer x peerset
             x inclusion x missing x aggregator

The browser then does one weighted power mean over four numbers per company, the
rank percentile, and the distribution. That is a few hundred thousand operations
per frame, so pinning an axis or dragging a weight reorders the table live and
the arithmetic is identical to `run.py`.

    python3 export_web.py [--weighting equal] [--out ../web/data/model.json]
"""

import argparse
import json
import os
import warnings
from itertools import product

import numpy as np

import load
import spec

warnings.filterwarnings("ignore")

AXIS_ORDER = ["polarity", "base", "window", "direction", "normalizer",
              "peerset", "inclusion", "missing", "aggregator"]

AXIS_OPTIONS = {
    "polarity": spec.POLARITIES, "base": spec.BASES, "window": spec.WINDOWS,
    "direction": spec.DIRECTIONS, "normalizer": spec.NORMALIZERS,
    "peerset": spec.PEERSETS, "inclusion": spec.INCLUSIONS,
    "missing": spec.MISSINGS, "aggregator": spec.AGGREGATORS,
}


def build():
    d = load.build()
    f = d["fields"]
    pil = f.pillar.values
    tiers = f.tier.values
    names = d["names"]
    N = len(names)
    reported = np.isfinite(d["VAR"][:, :, :, 0]).any(axis=2)

    masks = {(p, lv): spec.inclusion_mask(reported, d["peers"][p], tiers, lv)
             for p in spec.PEERSETS for lv in spec.INCLUSIONS}

    grid = spec.spec_grid()
    tensors = {pol: spec.grade_tensor(d, pol)[0] for pol in spec.POLARITIES}

    # canonical nested product, matching AXIS_ORDER exactly
    cube = []
    for pol in spec.POLARITIES:
        G = tensors[pol]
        by_key = {(s["base"], s["window"], s["direction"], s["normalizer"],
                   s["peerset"]): s["spec_id"] for s in grid}
        for base, win, dirn, norm, peer in product(
                spec.BASES, spec.WINDOWS, spec.DIRECTIONS,
                spec.NORMALIZERS, spec.PEERSETS):
            S = G[by_key[(base, win, dirn, norm, peer)]]
            for lv, miss, agg in product(spec.INCLUSIONS, spec.MISSINGS,
                                         spec.AGGREGATORS):
                P, _ = spec.composite(S, pil, masks[(peer, lv)],
                                      spec.WEIGHTINGS["equal"], miss, agg)
                cube.append([[None if not np.isfinite(v) else round(float(v), 1)
                              for v in row] for row in P])

    # per-company, per-pillar field counts under each (peerset, inclusion),
    # so the detail panel can say how much evidence is behind a pillar score
    evidence = {}
    for (p, lv), m in masks.items():
        got = np.where(m & reported, 1, 0)
        evidence[f"{p}|{lv}"] = [
            [int(got[i][pil == q].sum()) for q in spec.PILLARS] for i in range(N)
        ]
    expected = {}
    for (p, lv), m in masks.items():
        expected[f"{p}|{lv}"] = [
            [int(m[i][pil == q].sum()) for q in spec.PILLARS] for i in range(N)
        ]

    peer_of = {s: [str(x) for x in d["peers"][s]] for s in spec.PEERSETS}

    return {
        "meta": {
            "source": "Bloomberg materiality maps + FY2025 credit workbook, bruh/mat maps/",
            "real": True,
            "n_companies": N,
            "n_fields": int(len(f)),
            "n_specs": len(cube),
            "years": d["years"],
            "pillars": spec.PILLARS,
            "axis_order": AXIS_ORDER,
            "axes": AXIS_OPTIONS,
            "presets": spec.WEIGHTINGS,
            "min_peers": spec.MIN_PEERS,
            "rank_step": round(100.0 / (N - 1), 2),
            "field_counts": {p: int((pil == p).sum()) for p in spec.PILLARS},
        },
        "companies": [
            {"ticker": t,
             "peers": {s: peer_of[s][i] for s in spec.PEERSETS},
             "coverage": round(100.0 * reported[i].mean(), 1)}
            for i, t in enumerate(names)
        ],
        "fields": [
            {"id": str(i), "name": r["name"], "pillar": r.pillar, "type": r.type,
             "issue": r.issue, "contested": bool(r.contested), "tier": r.tier,
             "reported": int(reported[:, k].sum())}
            for k, (i, r) in enumerate(f.iterrows())
        ],
        "evidence": evidence,
        "expected": expected,
        "P": cube,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="../web/data/model.json")
    a = ap.parse_args()

    payload = build()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as fh:
        json.dump(payload, fh, separators=(",", ":"))
    js = os.path.splitext(a.out)[0] + ".js"
    with open(js, "w") as fh:
        fh.write("window.MODEL=")
        json.dump(payload, fh, separators=(",", ":"))
        fh.write(";\n")

    mb = os.path.getsize(a.out) / 1e6
    m = payload["meta"]
    print(f"wrote {a.out} and {js}  ({mb:.1f} MB)")
    print(f"{m['n_specs']:,} specifications x {m['n_companies']} companies "
          f"x {len(m['pillars'])} pillars, from {m['n_fields']} fields")
