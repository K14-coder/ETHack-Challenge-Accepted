"""
load.py — the Bloomberg materiality maps and the credit workbook, turned into
the arrays the formula runs on.

Nothing is fetched. Nothing is imputed. Every number here came out of an .xlsx
in `bruh/mat maps/`, and a cell that was empty there is NaN here.

    names   [18]                 tickers
    peers   {scheme: [18]}       three peer-set schemes, see PEER_SCHEMES
    fields  DataFrame            the registry, one row per field
    RAW     (18, F, 5)           the reported number, NaN where not reported
    VAR     (18, F, 5, 3)        the three published variants of a field, where
                                 they exist; otherwise the same number three times
    BASE    (18, 3)              the three exposure denominators, applied to Q only
    years   [2021 .. 2025]

The exposure base is one axis with a type-dependent meaning, as in design v4:

    slot 0        slot 1          slot 2
    Q  EBITDA     equity          production (MMboe/a)
    R  employees  contractors     total workforce
    F  Moody's    S&P             Fitch          (agency-adjusted leverage)

For Q the base is a divisor; for R and the agency figures it selects among
variants the reporter already published. The divisor is applied exactly once in
every branch.

Two facts about this data that the model has to live with, both declared rather
than engineered around:

  1. There is no revenue and no headcount anywhere in the export. EBITDA is the
     economic denominator we have. Bloomberg's own methodology calls revenue a
     fallback for when the physical activity metric is unavailable; we are one
     rung further down that ladder and say so.
  2. The credit workbook is a single fiscal year. So the F pillar has no time
     dimension: under `direction = change` it drops out entirely and the
     composite renormalises over E, S and G. That is the honest consequence of
     one year of financials, not a bug.
"""

import os
import numpy as np
import pandas as pd

import registry

HERE = os.path.dirname(os.path.abspath(__file__))
MM = os.path.join(HERE, "..", "..", "bruh", "mat maps", "csv")

YEARS = [2021, 2022, 2023, 2024, 2025]

# Bloomberg's five BECS peer groups collapse to two workable halves: the nine
# companies that own hydrocarbons and the nine that move, refine or service
# them. That split is not invented for convenience — it is exactly the set for
# which production and reserves are reported.
PRODUCERS = {"Exploration & Production", "Integrated Oils"}

PEER_SCHEMES = ["subgroup", "chain", "sector"]

# Rate fields that are three published views of one measurement. Collapsed into
# a single logical field so that safety is not counted three times, with the
# exposure base selecting the population — which is what design v4 specified and
# what Bloomberg does when it assigns no activity metric to an already-normalised
# field.
RATE_TRIPLES = {
    "TRIR": ("ES121", "ES261", "SA201"),   # employees, contractors, workforce
    "LTIR": ("ES092", "ES260", "SA202"),
    "FATAL": ("F1442", None, "RX389"),     # no contractor variant published
}

# The financial pillar, read straight out of credit_kennzahlen.csv. pol +1 means
# a lower raw value is better.
FIN_FIELDS = [
    ("FIN01", "Net debt / EBITDA",          ["Net Debt / EBITDA"],                   +1.0),
    ("FIN02", "EBIT / interest",            ["Zinsdeckung EBIT/Zins"],               -1.0),
    ("FIN03", "FCF / total debt",           ["FCF / Total Debt"],                    -1.0),
    ("FIN04", "Capex / D&A",                ["Capex / D&A"],                         -1.0),
    ("FIN05", "Payout / FCF",               ["Payout / FCF"],                        +1.0),
    ("FIN06", "Maturities < 24m / debt",    ["<24M / Total Debt"],                   +1.0),
    ("FIN07", "ROCE",                       ["ROCE"],                                -1.0),
    ("FIN08", "Reserve life",               ["Reserve Life (Jahre)"],                -1.0),
    # one logical field, three agencies' adjustments of the same leverage ratio
    ("FIN09", "Agency-adjusted debt / EBITDA",
     ["Moody's adj. Debt/EBITDA", "S&P adj. Debt/EBITDA", "Fitch adj. Debt/EBITDA"], +1.0),
]


def _credit(sheet, header):
    d = pd.read_csv(os.path.join(MM, "raw", f"credit_{sheet}.csv"), header=header)
    d = d.loc[:, ~d.columns.astype(str).str.startswith("Unnamed")]
    return d[d["Ticker"].notna()].set_index("Ticker")


MISSING_DATA_MSG = """
The Bloomberg materiality maps are not in this checkout.

They carry Bloomberg Terminal cell values and are not redistributed; see
    bruh/mat maps/WITHHELD.md
for the manifest and for how to regenerate them with a Terminal licence.

Everything downstream of this loader is committed and needs no licence:
    ETHack/model/out/          consensus, contestation, pivot, dominance, remedy
    ETHack/web/                the explorer, running on the committed pillar cube

    python3 -m http.server 4173 --directory ETHack/web
"""


def build():
    src = os.path.join(MM, "materiality_long.csv")
    if not os.path.exists(src):
        raise SystemExit(MISSING_DATA_MSG)
    long = pd.read_csv(src)
    long["field_id"] = long["field_id"].astype(str).str.strip()

    names = sorted(long.ticker.unique())
    N, Y = len(names), len(YEARS)
    ix = {t: i for i, t in enumerate(names)}
    yx = {y: k for k, y in enumerate(YEARS)}

    grp = long.drop_duplicates("ticker").set_index("ticker").peer_group
    peers = {
        "subgroup": np.array([grp[t] for t in names]),
        "chain":    np.array(["producers" if grp[t] in PRODUCERS else "downstream"
                              for t in names]),
        "sector":   np.array(["all"] * N),
    }

    reg = registry.build(delivered_ids=set(long.field_id))

    # ---------------------------------------------------------------- E/S/G
    collapsed = {v for tri in RATE_TRIPLES.values() for v in tri if v}
    keep = [f for f in reg.index if f not in collapsed]

    rows = []
    for f in keep:
        r = reg.loc[f]
        rows.append(dict(field_id=f, name=r["name"], pillar=r.pillar, type=r.type,
                         issue=r.issue, sub_issue=r.sub_issue, units=r.units,
                         pol_orthodox=r.pol_orthodox, pol_neutral=r.pol_neutral,
                         pol_stability=r.pol_stability, contested=r.contested,
                         tier=r.tier, variants=1, single_year=False))
    for key, tri in RATE_TRIPLES.items():
        base = reg.loc[tri[0]]
        rows.append(dict(field_id=key, name=base["name"].split(" - ")[0],
                         pillar=base.pillar, type="R", issue=base.issue,
                         sub_issue=base.sub_issue, units="Rate",
                         pol_orthodox=base.pol_orthodox, pol_neutral=base.pol_neutral,
                         pol_stability=base.pol_stability, contested=False,
                         tier=base.tier, variants=3, single_year=False))
    for fid, nm, cols, pol in FIN_FIELDS:
        rows.append(dict(field_id=fid, name=nm, pillar="F", type="R",
                         issue="Financial resilience", sub_issue=nm, units="Ratio",
                         pol_orthodox=pol, pol_neutral=pol, pol_stability=pol,
                         contested=False, tier="", variants=len(cols),
                         single_year=True))

    fields = pd.DataFrame(rows).set_index("field_id")
    F = len(fields)
    fidx = {f: j for j, f in enumerate(fields.index)}

    VAR = np.full((N, F, Y, 3), np.nan)

    # plain fields: the same number in all three slots
    sub = long[long.field_id.isin(keep) & long.value_raw.notna()]
    for t, f, y, v, raw in zip(sub.ticker, sub.field_id, sub.year, sub.value, sub.value_raw):
        val = _to_number(v, raw)
        if val is None:
            continue
        VAR[ix[t], fidx[f], yx[y], :] = val

    # rate triples: one slot per published population
    for key, tri in RATE_TRIPLES.items():
        j = fidx[key]
        for slot, src in enumerate(tri):
            if src is None:
                continue
            s = long[(long.field_id == src) & long.value.notna()]
            for t, y, v in zip(s.ticker, s.year, s.value):
                VAR[ix[t], j, yx[y], slot] = v
        # a company with no contractor figure falls back to the employee figure,
        # which is what a reader of the report would do
        miss = np.isnan(VAR[:, j, :, 1])
        VAR[:, j, :, 1] = np.where(miss, VAR[:, j, :, 0], VAR[:, j, :, 1])

    # ---------------------------------------------------------------- F pillar
    fin = _credit("kennzahlen", 4)
    for fid, _, cols, _ in FIN_FIELDS:
        j = fidx[fid]
        vals = [pd.to_numeric(fin[c], errors="coerce") if c in fin.columns else None
                for c in cols]
        for slot in range(3):
            v = vals[min(slot, len(vals) - 1)]
            if v is None:
                continue
            for t in names:
                if t in v.index and pd.notna(v[t]):
                    VAR[ix[t], j, :, slot] = float(v[t])   # one year, held flat

    # ---------------------------------------------------------------- BASE
    money = _credit("input_finanzen", 4)
    BASE = np.full((N, 3), np.nan)
    for t in names:
        if t not in money.index:
            continue
        BASE[ix[t], 0] = pd.to_numeric(money.loc[t, "EBITDA"], errors="coerce")
        BASE[ix[t], 1] = pd.to_numeric(money.loc[t, "Eigenkapital inkl. NCI"], errors="coerce")
        BASE[ix[t], 2] = pd.to_numeric(money.loc[t, "Produktion (MMboe/a)"], errors="coerce")
    BASE[BASE <= 0] = np.nan

    return dict(names=names, peers=peers, fields=fields, VAR=VAR, BASE=BASE,
                years=YEARS)


def _to_number(v, raw):
    if pd.notna(v):
        return float(v)
    s = str(raw).strip().upper()
    if s in ("Y", "YES", "TRUE"):
        return 1.0
    if s in ("N", "NO", "FALSE"):
        return 0.0
    return None


if __name__ == "__main__":
    d = build()
    f, VAR, BASE = d["fields"], d["VAR"], d["BASE"]
    print(f"{len(d['names'])} companies x {len(f)} fields x {len(d['years'])} years\n")
    print(f.groupby(["pillar", "type"]).size().unstack(fill_value=0), "\n")
    for s, p in d["peers"].items():
        u, c = np.unique(p, return_counts=True)
        print(f"  peers[{s:8}] {dict(zip(u, c.tolist()))}")
    print()
    rep = np.isfinite(VAR[:, :, :, 0]).any(axis=2)              # (N, F)
    print("companies reporting a field, by pillar:")
    for pil in ["E", "S", "G", "F"]:
        cols = (f.pillar == pil).values
        n = rep[:, cols].sum(axis=0)
        print(f"  {pil}: {cols.sum():3} fields | all 18: {(n == 18).sum():3}"
              f" | >=12: {(n >= 12).sum():3} | >=9: {(n >= 9).sum():3} | median {np.median(n):.0f}/18")
    print()
    print("exposure bases:", {n: int(np.isfinite(BASE[:, k]).sum())
                              for k, n in enumerate(["EBITDA", "equity", "production"])})
