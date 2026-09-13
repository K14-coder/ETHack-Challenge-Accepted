#!/usr/bin/env python3
"""
CONTESTED - step 2: run every defensible specification.

    python3 02_score.py            24 specifications
    python3 02_score.py --peer     48, adds the within-sector peer group

THE 24 SPECIFICATIONS = 2 x 3 x 2 x 2

  boundary      (2)  A_disclosed   only what the company reported to EPA
                     C_modelled    whole supply chain, estimated from its industry
  missing rule  (3)  exclude       no reported number -> drop from this ranking
                     worst_case    no reported number -> rank last (what MSCI does)
                     modelled      no reported number -> substitute the estimate
  eeio margins  (2)  with          factor includes transport and retail mark-up
                     without       factor excludes it
  denominator   (2)  revenue       tonnes per million dollars of sales
                     market_cap    tonnes per million dollars of company value

Every one is a real choice a real analyst makes. None is the correct one.
That is the point.
"""
import csv, itertools, json, math, sys
from pathlib import Path

INTERIM = Path("data/interim")
OUT     = Path("out"); OUT.mkdir(exist_ok=True)
INF     = float("inf")

BOUNDARY  = ["A_disclosed", "C_modelled"]
MISSING   = ["exclude", "worst_case", "modelled"]
MARGINS   = ["with", "without"]
DENOM     = ["revenue", "market_cap"]
PEER      = ["absolute", "within_sector"]


def f(v):
    try:
        return float(v) if v not in (None, "", "None") else None
    except ValueError:
        return None


def load():
    p = INTERIM / "companies.csv"
    if not p.exists():
        sys.exit("run 01_fetch.py first")
    rows = list(csv.DictReader(open(p)))
    for r in rows:
        for k in ("revenue_usd","market_cap_usd","disclosed_full","disclosed_equity",
                  "eeio_with","eeio_without"):
            r[k] = f(r.get(k))
    return rows


def intensity(r, boundary, missing, margins, denom):
    """tonnes CO2e per million USD of the chosen denominator.
       None  = this company is not ranked under this specification
       INF   = ranked last (worst-case rule)"""
    d = r["revenue_usd"] if denom == "revenue" else r["market_cap_usd"]
    if not d:
        return None
    d_m = d / 1e6
    eeio = r["eeio_with"] if margins == "with" else r["eeio_without"]

    if boundary == "A_disclosed":
        disc = r["disclosed_full"]
        if disc:
            return disc / d_m
        # no reported number - this is where the rule bites
        if missing == "exclude":    return None
        if missing == "worst_case": return INF
        if missing == "modelled":   return (eeio * r["revenue_usd"] / 1000) / d_m if eeio else None
    else:
        if not eeio:
            if missing == "worst_case": return INF
            return None
        return (eeio * r["revenue_usd"] / 1000) / d_m
    return None


def rank(vals, peer, sectors):
    """1 = cleanest. Companies scoring None are unranked (None)."""
    out = {}
    groups = {}
    for t, v in vals.items():
        key = sectors[t] if peer == "within_sector" else "_all"
        groups.setdefault(key, []).append((t, v))
    for key, items in groups.items():
        ranked = sorted([(t, v) for t, v in items if v is not None], key=lambda x: x[1])
        for i, (t, _) in enumerate(ranked, 1):
            out[t] = i
        for t, v in items:
            if v is None:
                out[t] = None
    return out


def main():
    use_peer = "--peer" in sys.argv
    rows = load()
    sectors = {r["ticker"]: r["gics_sector"] for r in rows}
    dims = [BOUNDARY, MISSING, MARGINS, DENOM] + ([PEER] if use_peer else [["absolute"]])
    specs = list(itertools.product(*dims))

    print(f"{len(specs)} specifications x {len(rows)} companies "
          f"= {len(specs)*len(rows):,} score computations")

    long_rows, rank_by_ticker = [], {r["ticker"]: [] for r in rows}
    for sid, (b, m, mg, dn, pr) in enumerate(specs):
        vals = {r["ticker"]: intensity(r, b, m, mg, dn) for r in rows}
        ranks = rank(vals, pr, sectors)
        n_ranked = sum(1 for v in ranks.values() if v is not None)
        for r in rows:
            t = r["ticker"]
            long_rows.append({"spec_id": sid, "boundary": b, "missing_rule": m,
                              "margins": mg, "denominator": dn, "peer_group": pr,
                              "ticker": t, "sector": r["gics_sector"],
                              "intensity": vals[t], "rank": ranks[t],
                              "n_ranked_in_spec": n_ranked})
            if ranks[t] is not None:
                rank_by_ticker[t].append(ranks[t])

    def pct(a, q):
        if not a: return None
        a = sorted(a); i = (len(a) - 1) * q
        lo, hi = math.floor(i), math.ceil(i)
        return a[lo] + (a[hi] - a[lo]) * (i - lo)

    summary = []
    for r in rows:
        t = r["ticker"]; rk = rank_by_ticker[t]
        summary.append({
            "ticker": t, "company": r["company"], "sector": r["gics_sector"],
            "specs_ranked": len(rk), "specs_total": len(specs),
            "consensus_rank": pct(rk, .5),
            "contestation_iqr": (pct(rk, .75) - pct(rk, .25)) if rk else None,
            "rank_min": min(rk) if rk else None, "rank_max": max(rk) if rk else None,
            "rank_range": (max(rk) - min(rk)) if rk else None,
            "disclosed_t": r["disclosed_full"],
            "modelled_t": (r["eeio_with"] * r["revenue_usd"] / 1000)
                          if (r["eeio_with"] and r["revenue_usd"]) else None,
            "revenue_usd": r["revenue_usd"],
        })
    for s in summary:
        s["modelled_over_disclosed"] = (s["modelled_t"] / s["disclosed_t"]
                                        if (s["modelled_t"] and s["disclosed_t"]) else None)

    with open(OUT / "long.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(long_rows[0].keys())); w.writeheader(); w.writerows(long_rows)
    with open(OUT / "summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary[0].keys())); w.writeheader(); w.writerows(summary)

    # ------------------------------------------------ the claims
    claims = {}
    ranked = [s for s in summary if s["rank_range"] is not None]
    claims["n_companies"] = len(rows)
    claims["n_specifications"] = len(specs)
    claims["no_disclosed_number"] = [s["ticker"] for s in summary if not s["disclosed_t"]]
    claims["median_modelled_over_disclosed"] = pct(
        [s["modelled_over_disclosed"] for s in summary if s["modelled_over_disclosed"]], .5)

    by_disc = sorted([s for s in summary if s["disclosed_t"] and s["revenue_usd"]],
                     key=lambda s: -s["disclosed_t"] / (s["revenue_usd"] / 1e6))
    by_mod  = sorted([s for s in summary if s["modelled_t"]], key=lambda s: -s["modelled_t"])
    claims["worst_by_disclosed_intensity"] = [s["ticker"] for s in by_disc[:5]]
    claims["worst_by_modelled_total"]      = [s["ticker"] for s in by_mod[:5]]
    claims["inversion_exists"] = bool(by_disc and by_mod and by_disc[0]["ticker"] != by_mod[0]["ticker"])

    try:  # Spearman between the two most extreme specs, benchmarked against 0.61
        from scipy.stats import spearmanr
        pairs = {}
        for lr in long_rows:
            pairs.setdefault(lr["spec_id"], {})[lr["ticker"]] = lr["rank"]
        ids = list(pairs)
        best = (2, None, None)
        for a, b in itertools.combinations(ids, 2):
            common = [t for t in pairs[a] if pairs[a][t] is not None and pairs[b][t] is not None]
            if len(common) < 8: continue
            rho = spearmanr([pairs[a][t] for t in common], [pairs[b][t] for t in common]).statistic
            if rho is not None and rho < best[0]: best = (rho, a, b)
        claims["min_spearman_between_specs"] = best[0] if best[1] is not None else None
        claims["berg_kolbel_rigobon_interrater_benchmark"] = 0.61
    except ImportError:
        claims["min_spearman_between_specs"] = "scipy not installed"

    json.dump(claims, open(OUT / "claims.json", "w"), indent=2, default=str)

    hdr = f"{'ticker':<8}{'sector':<26}{'consensus':>10}{'IQR':>7}{'range':>7}{'specs':>7}"
    print("\n" + hdr)
    print("-" * len(hdr))
    for s in sorted(summary, key=lambda x: -(x["rank_range"] if x["rank_range"] is not None else -1)):
        cons = f"{s['consensus_rank']:.0f}" if s["consensus_rank"] is not None else "-"
        iqr  = f"{s['contestation_iqr']:.1f}" if s["contestation_iqr"] is not None else "-"
        rng  = str(s["rank_range"]) if s["rank_range"] is not None else "-"
        print(f"{s['ticker']:<8}{s['sector'][:24]:<26}{cons:>10}{iqr:>7}{rng:>7}{s['specs_ranked']:>7}")

    nod = ", ".join(claims["no_disclosed_number"]) or "none"
    med = claims["median_modelled_over_disclosed"]
    print(f"\nno disclosed emissions figure at all: {nod}")
    print(f"median modelled/disclosed ratio: {med if med is None else round(med,2)}")
    print(f"ranking inverts between measures: {claims['inversion_exists']}")
    print(f"  worst by disclosed intensity: {claims['worst_by_disclosed_intensity']}")
    print(f"  worst by modelled total:      {claims['worst_by_modelled_total']}")
    print(f"lowest Spearman between two specs: {claims['min_spearman_between_specs']}  (benchmark 0.61)")

    print("\nwrote out/long.csv, out/summary.csv, out/claims.json\nnext: python3 03_plots.py")


if __name__ == "__main__":
    main()
