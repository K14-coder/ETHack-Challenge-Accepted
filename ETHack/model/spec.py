"""
spec.py — the formula, v2. Pure functions, no data, no plotting.

Nine axes. Each one is a fork where MSCI and Bloomberg made different published
choices, or where this data forces a choice that neither of them documents. See
`../provider-decision-points.md` for the citation behind each.

    axis         options                                        set at
    base         ebitda / equity / production                   step 1
    window       latest / fy_common / mean3                     step 2
    direction    level / change                                 step 3
    polarity     orthodox / neutral / stability                 step 4
    normalizer   percentile / winsor / log / elasticity         step 5
    peerset      subgroup / chain / sector                      step 5
    inclusion    permissive / majority / strict                 step 6
    missing      exclude / worst / cap                          step 6
    aggregator   arithmetic / pmean05 / geometric               step 6

    3 * 3 * 2 * 3 * 4 * 3 * 3 * 3 * 3 = 17,496 specifications.

Steps 1 to 5 produce a grade tensor and do not involve the pillar weights.
Steps 6 to 8 are cheap and run downstream of it, in `run.py` or in the browser.

THE EXPOSURE BASE has a type-dependent meaning, one operator per type:

    B(x, base) =  x / d(base)   if type is Q      APPLY the divisor
                  x[base]       if type is R      SELECT the published variant
                  x             otherwise         already unitless

so the divisor is applied exactly once on every branch. Slots: for Q, EBITDA /
equity / production; for a rate triple, employees / contractors / workforce; for
agency-adjusted leverage, Moody's / S&P / Fitch.

TWO RULES THAT ARE RULES, NOT SPECIFICATIONS. Neither is varied:

  MIN_PEERS = 3   a peer group below this is graded against the whole sector.
                  Three members give the coarsest ranking that is still a
                  ranking; two can only ever return 0 and 100.
  ELAST_MIN = 8   the elasticity normaliser needs enough points to fit a slope.
                  Below it, that cell falls back to log min-max.
"""

from itertools import product
import numpy as np

BASES       = ["ebitda", "equity", "production"]
WINDOWS     = ["latest", "fy_common", "mean3"]
DIRECTIONS  = ["level", "change"]
POLARITIES  = ["orthodox", "neutral", "stability"]
NORMALIZERS = ["percentile", "winsor", "log", "elasticity"]
PEERSETS    = ["subgroup", "chain", "sector"]
INCLUSIONS  = ["permissive", "majority", "strict"]
MISSINGS    = ["exclude", "worst", "cap"]
AGGREGATORS = ["arithmetic", "pmean05", "geometric"]

GRID_AXES = ("base", "window", "direction", "normalizer", "peerset")

PILLARS = ["E", "S", "G", "F"]

MIN_PEERS = 3
ELAST_MIN = 8

# How demanding the model is about what counts as evidence. One ladder, tightened
# at both ends together: a field must be reported by this share of the peer set,
# and a policy flag must clear this substantive tier.
#   0 all - any disclosed policy
#   1 substantive - the policy constrains an operating decision
#   2 outcome-linked - the policy carries a quantified, checkable commitment
INCLUSION_RULE = {
    "permissive": (0.50, 0),
    "majority":   (0.67, 1),
    "strict":     (1.00, 2),
}

TIER_RANK = {"": 3, "all only": 0, "all": 0, "substantive": 1, "outcome-linked": 2}

WEIGHTINGS = {
    "equal":       {"E": .25, "S": .25, "G": .25, "F": .25},
    "env_led":     {"E": .55, "S": .15, "G": .15, "F": .15},
    "social_led":  {"E": .15, "S": .55, "G": .15, "F": .15},
    "gov_led":     {"E": .15, "S": .15, "G": .55, "F": .15},
    "finance_led": {"E": .15, "S": .15, "G": .15, "F": .55},
}


def spec_grid():
    """The 144 grade specifications, in a fixed order."""
    grid = [dict(zip(GRID_AXES, c)) for c in
            product(BASES, WINDOWS, DIRECTIONS, NORMALIZERS, PEERSETS)]
    for k, s in enumerate(grid):
        s["spec_id"] = k
    return grid


# ---------------------------------------------------------------- helpers

def avg_rank(x):
    """Average ranks, ascending, 1-based. x must be finite."""
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

def exposure(VAR, BASE, ftype, base_name):
    """VAR (N,F,Y,3), BASE (N,3) -> x (N,F,Y)."""
    b = BASES.index(base_name)
    x = VAR[:, :, :, b].astype(float).copy()
    isQ = (ftype == "Q")
    denom = BASE[:, b][:, None, None]
    with np.errstate(divide="ignore", invalid="ignore"):
        x[:, isQ, :] = x[:, isQ, :] / denom
    return x


# ---------------------------------------------------------------- steps 2+3

def series_stats(x):
    """
    Collapse the year axis onto the years a company actually reported.

    Sustainability reporting runs a year or more behind. In this export FY2025
    is 36% complete for environmental fields against 60% for FY2024, so reading
    "the latest column" silently compares a company that has published against
    one that has not. Bloomberg splits exactly this into two products — Latest
    Scores, which take a company's most recent disclosure, and Fiscal Year
    Scores, which wait until a year is complete (B p.34). Both are offered here
    and the difference between them is a specification, not an accident.

    Returns, all (N,F):
        last     the most recent reported value
        prev     the value two reported steps earlier, for the change branch
        mean3    the mean of the last three reported values
        mean3p   the mean of the three before those
    """
    N, F, Y = x.shape
    last  = np.full((N, F), np.nan)
    prev  = np.full((N, F), np.nan)
    mean3 = np.full((N, F), np.nan)
    mean3p = np.full((N, F), np.nan)
    for i in range(N):
        for j in range(F):
            v = x[i, j]
            k = np.flatnonzero(np.isfinite(v))
            if not len(k):
                continue
            seq = v[k]
            last[i, j] = seq[-1]
            prev[i, j] = seq[-3] if len(seq) >= 3 else seq[0]
            mean3[i, j] = seq[-3:].mean()
            if len(seq) >= 4:
                mean3p[i, j] = seq[:-3][-3:].mean()
    return last, prev, mean3, mean3p


def reduce_series(x, window, direction, ftype, fy_index=None, single_year=None):
    """
    x (N,F,Y) -> q (N,F).

    window  latest     each company's most recent reported year
            fy_common  one fixed year for everybody, the last complete one
            mean3      the mean of its last three reported years
    Booleans take a plain difference under `change`, having no ratio.
    """
    last, prev, mean3, mean3p = series_stats(x)

    if direction == "level":
        if window == "latest":
            return last
        if window == "fy_common":
            return x[:, :, fy_index]
        return mean3

    if window == "mean3":
        end, start = mean3, mean3p
    elif window == "fy_common":
        end = x[:, :, fy_index]
        start = x[:, :, max(0, fy_index - 2)]
    else:
        end, start = last, prev

    diff = end - start
    with np.errstate(divide="ignore", invalid="ignore"):
        rel = np.where(np.abs(start) > 1e-12, diff / np.abs(start), np.nan)
    isB = (ftype == "B")[None, :]
    out = np.where(isB, diff, rel)
    if single_year is not None:
        # The credit workbook is one fiscal year. A single point has no
        # trajectory, so under `change` these fields drop out and the composite
        # renormalises over the pillars that do have one. Holding the value flat
        # and reporting a change of zero would be a fabricated time series.
        out = np.where(single_year[None, :], np.nan, out)
    return out


# ---------------------------------------------------------------- step 4

def orient(q, pol):
    """higher u = worse, always. pol 0 means the field is deliberately neutral
    under this convention: it enters the model and discriminates nothing."""
    return q * pol[None, :]


# ---------------------------------------------------------------- step 5

def grade(u_col, members, normalizer, act=None):
    """One field, one peer set. Returns 0..100, 100 = best, NaN outside the set."""
    out = np.full(u_col.shape, np.nan)
    ok = members & np.isfinite(u_col)
    m = int(ok.sum())
    if m == 0:
        return out
    if m == 1:
        out[ok] = 50.0
        return out

    U = u_col[ok]
    if np.allclose(U, U[0]):
        out[ok] = 50.0
        return out

    if normalizer == "percentile":
        r = avg_rank(U)
        out[ok] = 100.0 * (m - r) / (m - 1)

    elif normalizer == "winsor":
        lo, hi = np.percentile(U, [5, 95])
        if hi <= lo:
            out[ok] = 50.0
        else:
            out[ok] = 100.0 * (hi - np.clip(U, lo, hi)) / (hi - lo)

    elif normalizer == "log":
        umin, umax = U.min(), U.max()
        t = U if umin > 0 else U - umin + 0.01 * (umax - umin)
        L = np.log(t)
        if L.max() <= L.min():
            out[ok] = 50.0
        else:
            out[ok] = 100.0 * (L.max() - L) / (L.max() - L.min())

    elif normalizer == "elasticity":
        # Bloomberg's intensity model: log(impact) = log(intensity) + g*log(activity)
        # scored on the residual through the normal CDF. Falls back where the
        # activity metric is missing or the peer set is too small to fit a slope.
        A = None if act is None else act[ok]
        if A is None or m < ELAST_MIN or not np.all(np.isfinite(A)) \
                or np.any(A <= 0) or np.any(U <= 0):
            return grade(u_col, members, "log")
        lx, ly = np.log(A), np.log(U)
        g, c = np.polyfit(lx, ly, 1)
        eps = ly - (c + g * lx)
        sd = eps.std(ddof=1)
        if not np.isfinite(sd) or sd <= 0:
            return grade(u_col, members, "log")
        out[ok] = 100.0 * (1.0 - _phi(eps / sd))
    else:
        raise ValueError(normalizer)

    return out


def _phi(z):
    """Standard normal CDF, no scipy."""
    return 0.5 * (1.0 + _erf(z / np.sqrt(2.0)))


def _erf(x):
    """Abramowitz & Stegun 7.1.26, |error| < 1.5e-7."""
    s = np.sign(x)
    x = np.abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
                - 0.284496736) * t + 0.254829592) * t * np.exp(-x * x)
    return s * y


def peer_pairs(groups):
    """(compute-over, assign-to) pairs. A group below MIN_PEERS is graded against
    the whole sector, because it cannot support a ranking of its own."""
    N = len(groups)
    allm = np.ones(N, bool)
    pairs = []
    for g in np.unique(groups):
        m = (groups == g)
        pairs.append((m, m) if m.sum() >= MIN_PEERS else (allm, m))
    return pairs


def grade_all(u, groups, normalizer, act=None):
    """u (N,F) -> S (N,F) on 0..100."""
    N, F = u.shape
    S = np.full((N, F), np.nan)
    for peers, assign in peer_pairs(groups):
        for f in range(F):
            g = grade(u[:, f], peers, normalizer, act)
            S[assign, f] = g[assign]
    return S


# ---------------------------------------------------------------- step 6

def inclusion_mask(reported, groups, tiers, level):
    """
    Which fields are in the model, per company. (N,F) bool.

    `reported` (N,F) bool: the company has at least one year of this field.
    A field enters for company i when enough of i's peer group report it AND the
    field clears the substantive tier for this level.
    """
    share_req, tier_req = INCLUSION_RULE[level]
    N, F = reported.shape
    mask = np.zeros((N, F), bool)
    for g in np.unique(groups):
        m = (groups == g)
        share = reported[m].mean(axis=0)
        mask[m] = share >= share_req - 1e-9
    tier_ok = np.array([TIER_RANK.get(t, 3) >= tier_req for t in tiers])
    return mask & tier_ok[None, :]


def pmean(x, w, kind):
    """Weighted mean over the last axis, NaN-aware. Bloomberg's shifted power
    mean with p = 0.5 and, on this 0..100 scale, s = 10."""
    s = 10.0
    ok = np.isfinite(x)
    w = np.where(ok, w, 0.0)
    tot = w.sum(axis=-1)
    good = tot > 0
    w = np.where(good[..., None], w / np.where(tot[..., None] == 0, 1, tot[..., None]), 0.0)
    xf = np.where(ok, x, 0.0)

    if kind == "arithmetic":
        out = (w * xf).sum(axis=-1)
    elif kind == "pmean05":
        out = ((w * np.sqrt(np.maximum(xf + s, 0))).sum(axis=-1)) ** 2 - s
    elif kind == "geometric":
        out = np.exp((w * np.log(np.maximum(xf + s, 1e-9))).sum(axis=-1)) - s
    else:
        raise ValueError(kind)
    return np.where(good, out, np.nan)


def composite(S, pillar, mask, weights, missing, aggregator):
    """
    STEP 6. S (N,F) grades -> pillar scores (N,4) and the total (N,).

    missing:
      exclude  an unreported field drops out and the weights redistribute
               (Bloomberg's sub-issue rule)
      worst    it enters as 0, the strict reading of grading silence badly
      cap      it drops out, then the pillar is capped by its own disclosure:
               UT = 30 + sqrt(DF) * 70 on this scale (Bloomberg's Issue Score)
    """
    N, F = S.shape
    P = np.full((N, len(PILLARS)), np.nan)

    for k, pil in enumerate(PILLARS):
        cols = (pillar == pil)
        if not cols.any():
            continue
        sub = S[:, cols]
        sub_mask = mask[:, cols]
        vals = np.where(sub_mask, sub, np.nan)

        if missing == "worst":
            vals = np.where(sub_mask & ~np.isfinite(sub), 0.0, vals)

        w = np.ones_like(vals)
        score = pmean(vals, w, aggregator)

        if missing == "cap":
            got = (sub_mask & np.isfinite(sub)).sum(axis=1)
            exp = sub_mask.sum(axis=1)
            DF = np.where(exp > 0, got / np.maximum(exp, 1), 0.0)
            score = score * (30.0 + np.sqrt(DF) * 70.0) / 100.0

        P[:, k] = score

    wv = np.array([weights.get(p, 0.0) for p in PILLARS], float)
    T = pmean(P, np.tile(wv, (N, 1)), aggregator)
    return P, T


# ---------------------------------------------------------------- step 7

def rank_percentile(T):
    """100 = best of the N that have a score."""
    N = len(T)
    R = np.full(N, np.nan)
    ok = np.isfinite(T)
    m = int(ok.sum())
    if m < 2:
        return R
    rho = avg_rank(-T[ok])
    R[ok] = 100.0 * (m - rho) / (m - 1)
    return R


# ---------------------------------------------------------------- the run

def grade_tensor(data, polarity="orthodox"):
    """
    Steps 1 to 5 over the whole grid.
    Returns G (144, N, F) grades and the grid.
    """
    VAR, BASE = data["VAR"], data["BASE"]
    f = data["fields"]
    ftype = f["type"].values
    single = f["single_year"].values.astype(bool)
    pol = f[f"pol_{polarity}"].values.astype(float)
    grid = spec_grid()

    N, F = VAR.shape[0], VAR.shape[1]
    G = np.full((len(grid), N, F), np.nan)

    # the last fiscal year the sector as a whole actually reported
    filled = np.isfinite(VAR[:, :, :, 0]).mean(axis=(0, 1))
    fy = int(np.max(np.flatnonzero(filled >= 0.95 * filled.max())))

    for s in grid:
        x = exposure(VAR, BASE, ftype, s["base"])
        q = reduce_series(x, s["window"], s["direction"], ftype, fy, single)
        u = orient(q, pol)
        act = BASE[:, BASES.index(s["base"])]
        G[s["spec_id"]] = grade_all(u, data["peers"][s["peerset"]],
                                    s["normalizer"], act)
    return G, grid
