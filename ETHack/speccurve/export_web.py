"""
export_web.py — dump the grade tensor for the web explorer.

The pillar weights enter the formula only at STEP 6. Steps 1-5 (exposure,
window, direction, orientation, normalisation) are weight-independent, so the
whole weighting question can be answered in the browser from one tensor:

    S[spec][company][field]   grade 0..100, 100 = best, null = not reported

The frontend then does STEP 6 (weighted pillar mean), STEP 7 (rank percentile)
and STEP 8 (median / IQR across the selected specs) live. Same arithmetic as
spec.py, no approximation.

    python3 export_web.py [--seed 7] [--out ../web/data/speccurve.json]

Writes the .json and, beside it, a .js that assigns the same payload to
window.SPECCURVE, so the explorer opens straight from the filesystem with no
server and no fetch.
"""

import argparse, json, os
import numpy as np
import dummy, spec


def build(seed):
    d = dummy.build(seed)
    RAW, BASE = d["RAW"], d["BASE"]
    ftype, pol, pillar, groups = d["ftype"], d["pol"], d["pillar"], d["groups"]
    grid = spec.spec_grid()

    N, F = RAW.shape[0], RAW.shape[1]
    tensor = []
    for s in grid:
        x = spec.exposure(RAW, BASE, ftype, s["base"])
        q = spec.reduce_series(x, s["window"], s["direction"], ftype)
        u = spec.orient(q, pol)
        S = spec.grade_all(u, groups, s["peerset"], s["normalizer"])
        tensor.append([[None if not np.isfinite(v) else round(float(v), 2)
                        for v in row] for row in S])

    # coverage: share of the 30 fields a company reports, in the reference spec
    ref = np.array(tensor[0], dtype=object)
    coverage = [round(100.0 * sum(v is not None for v in row) / F, 1) for row in ref]

    return {
        "meta": {
            "source": "speccurve/dummy.py",
            "real": False,
            "seed": seed,
            "n_companies": N,
            "n_fields": F,
            "n_specs": len(grid),
            "years": d["years"],
            "min_peers": spec.MIN_PEERS,
            "axes": {
                "base":       spec.BASES,
                "window":     spec.WINDOWS,
                "direction":  spec.DIRECTIONS,
                "normalizer": spec.NORMALIZERS,
                "peerset":    spec.PEERSETS,
            },
            "presets": spec.WEIGHTINGS,
        },
        "companies": [{"name": n, "group": str(g), "coverage": c}
                      for n, g, c in zip(d["names"], groups, coverage)],
        "fields": [{"name": n, "pillar": str(p), "type": str(t), "polarity": int(po)}
                   for n, p, t, po in zip(d["fields"], pillar, ftype, pol)],
        "specs": [{k: s[k] for k in ("spec_id",) + spec.AXES} for s in grid],
        "grades": tensor,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", default="../web/data/speccurve.json")
    a = ap.parse_args()

    payload = build(a.seed)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as fh:
        json.dump(payload, fh, separators=(",", ":"))
    js = os.path.splitext(a.out)[0] + ".js"
    with open(js, "w") as fh:
        fh.write("window.SPECCURVE=")
        json.dump(payload, fh, separators=(",", ":"))
        fh.write(";\n")

    kb = os.path.getsize(a.out) / 1024
    print(f"wrote {a.out} and {js}  ({kb:.0f} KB)  "
          f"{payload['meta']['n_specs']} specs x {payload['meta']['n_companies']} companies "
          f"x {payload['meta']['n_fields']} fields")
