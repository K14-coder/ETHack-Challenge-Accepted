"""
spec.py — the formula. Pure functions, no data, no plotting.

THE FORMULA, top to bottom
==========================

Indices
    i   company          i = 1..N          (N = 20)
    f   field            f = 1..F          (F = 30, ten per pillar)
    y   year             y = 1..5          (2021..2025)
    b   exposure base    b in {revenue, volume, headcount}
    P   pillar           P in {E, S, F}

Per-field constants
    type[f]  in {Q, R, P, B}   quantity / rate / percentage / boolean
    pol[f]   in {+1, -1}       +1 if a LOWER raw value is better, -1 if HIGHER is better
    pil[f]   in {E, S, F}

Raw data
    RAW[i,f,y,b]   the reported number.
                   For type Q, P, B the three b-slices are identical (one number).
                   For type R the three b-slices are the three published variants
                   of the same rate (per employee-hours / per contractor-hours /
                   per total-workforce-hours).
    BASE[i,y,b]    the size denominator: revenue, volume, headcount.

A SPECIFICATION is one choice on each of five axes:
    sigma = (b, w, d, z, p)
        b in {revenue, volume, headcount}                       3
        w in {latest, mean3}                                    2
        d in {level, change}                                    2
        z in {percentile, winsor_minmax, log_minmax}            3
        p in {subgroup, sector}                                 2
    3 * 2 * 2 * 3 * 2 = 72 specifications.

A WEIGHTING is one of K = 4 pillar weight vectors.
    72 * 4 = 288 scores per company.

STEP 1  exposure   (units removed)
    x[i,f,y] = RAW[i,f,y,b] / BASE[i,y,b]      if type[f] = Q
             = RAW[i,f,y,b]                    otherwise (R uses b to pick the variant;
                                                P and B are already unitless)

STEP 2+3  window and direction   (one number per field)
    d = level,  w = latest :  q[i,f] = x[i,f,5]
    d = level,  w = mean3  :  q[i,f] = mean(x[i,f,3..5])
    d = change, w = latest :  q[i,f] = (x[i,f,5] - x[i,f,3]) / |x[i,f,3]|
    d = change, w = mean3  :  q[i,f] = (mean(x[i,f,3..5]) - mean(x[i,f,1..3]))
                                       / |mean(x[i,f,1..3])|
    For type B, "change" is the plain difference, not the ratio (0 in the denominator).

STEP 4  orientation   (higher = worse, always)
    u[i,f] = pol[f] * q[i,f]

STEP 5  normalisation   (units -> a 0..100 grade, 100 = best)
    Let G(i,p) be the peer set: i's sub-group if p = subgroup, all N if p = sector.
    Let U = { u[j,f] : j in G, u[j,f] not missing },  m = |U|.

    z = percentile
        r    = average rank of u[i,f] in U, ascending, 1 = lowest = best
        s    = 100 * (m - r) / (m - 1)

    z = winsor_minmax
        lo   = 5th percentile of U,  hi = 95th percentile of U
        uc   = clip(u[i,f], lo, hi)
        s    = 100 * (hi - uc) / (hi - lo)          (50 if hi = lo)

    z = log_minmax
        if min(U) > 0 :  t = u
        else          :  t = u - min(U) + 0.01 * (max(U) - min(U))   [1% floor]
        L    = log(t)
        s    = 100 * (max L - L[i]) / (max L - min L)                (50 if degenerate)

STEP 6  aggregation   (still 0..100, no rescaling needed)
    pillar score, averaged over the fields of P that company i actually reports:
        S_P[i] = mean{ s[i,f] : f in P, s[i,f] not missing }

    total, for weighting k, renormalised over the pillars i has at all:
        T_k[i] = ( sum_P W_k[P] * S_P[i] ) / ( sum_P W_k[P] * 1{S_P[i] exists} )

STEP 7  rank percentile of the total, across all N companies
    rho  = average rank of T_k[i] descending, 1 = highest total = best
    R    = 100 * (N - rho) / (N - 1)

STEP 8  the two outputs, per company, over all 288 (sigma, k)
    consensus  = median R
    spread     = IQR R = P75 - P25
"""

from itertools import product
import numpy as np

BASES       = ["revenue", "volume", "headcount"]
WINDOWS     = ["latest", "mean3"]
DIRECTIONS  = ["level", "change"]
NORMALIZERS = ["percentile", "winsor_minmax", "log_minmax"]
PEERSETS    = ["subgroup", "sector"]

AXES = ("base", "window", "direction", "normalizer", "peerset")

# A peer set smaller than this cannot support a percentile: with 2 members the
# only possible grades are 0 and 100. So a sub-group below the floor falls back
# to the sector. This is a rule, not a specification: it is not varied.
MIN_PEERS = 4

WEIGHTINGS = {
    "equal":       {"E": 1/3,  "S": 1/3,  "F": 1/3},
    "env_led":     {"E": 0.60, "S": 0.20, "F": 0.20},
    "social_led":  {"E": 0.20, "S": 0.60, "F": 0.20},
    "finance_led": {"E": 0.20, "S": 0.20, "F": 0.60},
}


def spec_grid():
    """The 72 specifications, in a fixed order."""
    grid = [dict(zip(AXES, c)) for c in
            product(BASES, WINDOWS, DIRECTIONS, NORMALIZERS, PEERSETS)]
    for k, s in enumerate(grid):
        s["spec_id"] = k
    return grid


# ---------------------------------------------------------------- helpers

def avg_rank(x):
    """Average ranks, ascending, 1-based. No scipy. x must be finite."""
    n = len(x)
    order = np.argsort(x, kind="mergesort")
    sx = x[order]
    r = np.empty(n, float)
    i = 0
    while i < n:
        j = i
        while j + 1 < n and sx[j + 1] == sx[i]:
            j += 1
        r[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return r


# ---------------------------------------------------------------- step 1

def exposure(RAW, BASE, ftype, base_name):
    """STEP 1. RAW (N,F,Y,3), BASE (N,Y,3) -> x (N,F,Y)."""
    b = BASES.index(base_name)
    x = RAW[:, :, :, b].astype(float).copy()
    isQ = (ftype == "Q")
    denom = BASE[:, :, b][:, None, :]                 # (N,1,Y)
    with np.errstate(divide="ignore", invalid="ignore"):
        x[:, isQ, :] = x[:, isQ, :] / denom
    return x


# ---------------------------------------------------------------- steps 2+3

def reduce_series(x, window, direction, ftype):
    """STEPS 2 and 3. x (N,F,Y) -> q (N,F)."""
    with np.errstate(invalid="ignore"), np.testing.suppress_warnings() as sup:
        sup.filter(RuntimeWarning)
        if direction == "level":
            return x[:, :, 4] if window == "latest" else np.nanmean(x[:, :, 2:5], axis=2)

        if window == "latest":
            end, start = x[:, :, 4], x[:, :, 2]
        else:
            end   = np.nanmean(x[:, :, 2:5], axis=2)
            start = np.nanmean(x[:, :, 0:3], axis=2)

    diff = end - start
    with np.errstate(divide="ignore", invalid="ignore"):
        rel = np.where(np.abs(start) > 1e-12, diff / np.abs(start), np.nan)
    isB = (ftype == "B")[None, :]
    return np.where(isB, diff, rel)


# ---------------------------------------------------------------- step 4

def orient(q, pol):
    """STEP 4. higher = worse, always."""
    return q * pol[None, :]


# ---------------------------------------------------------------- step 5

def grade(u_col, members, normalizer):
    """
    STEP 5. One field, one peer set.
    u_col   (N,) oriented values, nan = not reported
    members (N,) bool, the peer set
    returns (N,) grades 0..100 (100 = best), nan outside the peer set or where missing
    """
    out = np.full(u_col.shape, np.nan)
    ok = members & np.isfinite(u_col)
    m = int(ok.sum())
    if m == 0:
        return out
    if m == 1:
        out[ok] = 50.0
        return out

    U = u_col[ok]

    if normalizer == "percentile":
        r = avg_rank(U)                               # 1 = lowest u = best
        out[ok] = 100.0 * (m - r) / (m - 1)

    elif normalizer == "winsor_minmax":
        lo, hi = np.percentile(U, [5, 95])
        if hi <= lo:
            out[ok] = 50.0
        else:
            uc = np.clip(U, lo, hi)
            out[ok] = 100.0 * (hi - uc) / (hi - lo)

    elif normalizer == "log_minmax":
        umin, umax = U.min(), U.max()
        if umax <= umin:
            out[ok] = 50.0
        else:
            t = U if umin > 0 else U - umin + 0.01 * (umax - umin)
            L = np.log(t)
            out[ok] = 100.0 * (L.max() - L) / (L.max() - L.min())

    else:
        raise ValueError(normalizer)

    return out


def peer_pairs(groups, peerset):
    """
    (peer set, assignment set) pairs for one peerset choice.
    Grades are COMPUTED over the peer set and ASSIGNED to the assignment set.
    A sub-group below MIN_PEERS is graded against the whole sector instead,
    because a 2-member percentile can only ever return 0 or 100.
    """
    N = len(groups)
    allm = np.ones(N, bool)
    if peerset == "sector":
        return [(allm, allm)]
    pairs = []
    for g in np.unique(groups):
        m = (groups == g)
        pairs.append((m, m) if m.sum() >= MIN_PEERS else (allm, m))
    return pairs


def grade_all(u, groups, peerset, normalizer):
    """STEP 5 over every field. u (N,F) -> S (N,F) grades 0..100."""
    N, F = u.shape
    S = np.full((N, F), np.nan)
    pairs = peer_pairs(groups, peerset)
    for f in range(F):
        col = u[:, f]
        for peers, assign in pairs:
            g = grade(col, peers, normalizer)
            S[assign, f] = g[assign]
    return S


# ---------------------------------------------------------------- step 6

def composite(S, pillar, weights):
    """STEP 6. S (N,F) -> T (N,), still on 0..100."""
    N = S.shape[0]
    num = np.zeros(N)
    den = np.zeros(N)
    for P, w in weights.items():
        cols = (pillar == P)
        sub = S[:, cols]
        cnt = np.isfinite(sub).sum(axis=1)
        with np.errstate(invalid="ignore"):
            mean_P = np.where(cnt > 0, np.nansum(sub, axis=1) / np.maximum(cnt, 1), np.nan)
        has = cnt > 0
        num += np.where(has, w * np.nan_to_num(mean_P), 0.0)
        den += np.where(has, w, 0.0)
    return np.where(den > 0, num / np.maximum(den, 1e-12), np.nan)


# ---------------------------------------------------------------- step 7

def rank_percentile(T):
    """STEP 7. T (N,) totals -> R (N,) rank percentile, 100 = best of the N."""
    N = len(T)
    R = np.full(N, np.nan)
    ok = np.isfinite(T)
    m = int(ok.sum())
    if m < 2:
        return R
    rho = avg_rank(-T[ok])                            # 1 = highest total = best
    R[ok] = 100.0 * (m - rho) / (m - 1)
    return R


# ---------------------------------------------------------------- the whole run

def run_all(RAW, BASE, ftype, pol, pillar, groups, weightings=None):
    """
    Every specification x every weighting.
    returns R (N, 72, K) rank percentiles, the spec grid, and the weighting names.
    """
    weightings = weightings or WEIGHTINGS
    grid = spec_grid()
    wnames = list(weightings.keys())
    N = RAW.shape[0]
    R = np.full((N, len(grid), len(wnames)), np.nan)

    for s in grid:
        x = exposure(RAW, BASE, ftype, s["base"])
        q = reduce_series(x, s["window"], s["direction"], ftype)
        u = orient(q, pol)
        S = grade_all(u, groups, s["peerset"], s["normalizer"])
        for k, wn in enumerate(wnames):
            T = composite(S, pillar, weightings[wn])
            R[:, s["spec_id"], k] = rank_percentile(T)

    return R, grid, wnames
