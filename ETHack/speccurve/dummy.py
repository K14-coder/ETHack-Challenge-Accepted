"""
dummy.py — synthetic data with the exact shape the real Bloomberg export has.

Nothing here is real. The point is to exercise the formula and prove that the
five specification axes actually reshuffle the ranking. The generator is built
so that they do:

  base       revenue, volume and headcount are three independent denominators
             (margin and labour intensity vary by company), so dividing by one
             rather than another reorders the field.
  direction  the drift loads on weakness but carries large idiosyncratic noise,
             so "level" and "change" agree only partly. Level-only specs
             correlate about 0.9 with each other, change-only about 0.7, and
             across the two blocks about 0.35, which is the real pattern.
  normalizer one company carries a deliberate heavy outlier, which is exactly
             the case where percentile, winsorised min-max and log min-max part
             company.
  peerset    sub-groups have 2 to 8 members, so a company can be best in its
             sub-group and mid-table in the sector.
  missing    disclosure propensity is a company trait, so coverage varies and
             two companies are systematic non-disclosers.

Replace RAW and BASE with the real export and nothing else changes.
"""

import numpy as np

YEARS = [2021, 2022, 2023, 2024, 2025]

# (field name, pillar, type, polarity)  polarity +1 = lower is better
FIELDS = [
    ("F0947 Scope 1 GHG",                 "E", "Q", +1),
    ("F1284 Carbon in reserves",          "E", "Q", +1),
    ("ES077 Scope 2 location",            "E", "Q", +1),
    ("ES027 Gas flaring",                 "E", "Q", +1),
    ("ES249 Spill volume",                "E", "Q", +1),
    ("ES018 Emissions to water",          "E", "Q", +1),
    ("SA020 Freshwater withdrawal",       "E", "Q", +1),
    ("ES019 Hazardous waste",             "E", "Q", +1),
    ("SA055 Methane share of Scope 1",    "E", "P", +1),
    ("SA559 Net zero target claimed",     "E", "B", -1),

    ("ES121 TRIR employees",              "S", "R", +1),
    ("ES261 TRIR contractors",            "S", "R", +1),
    ("ES092 LTIR employees",              "S", "R", +1),
    ("ES260 LTIR contractors",            "S", "R", +1),
    ("F1442 Fatality rate employees",     "S", "R", +1),
    ("RX389 Fatality rate workforce",     "S", "R", +1),
    ("SA052 Tier 1 process safety",       "S", "R", +1),
    ("RX312 Training spend per head",     "S", "R", -1),
    ("ES059 Human rights policy",         "S", "B", -1),
    ("SA029 Indigenous rights policy",    "S", "B", -1),

    ("FIN01 Net debt / EBITDA",           "F", "R", +1),
    ("FIN02 EBIT / interest",             "F", "R", -1),
    ("FIN03 FCF / total debt",            "F", "R", -1),
    ("FIN04 Capex / depreciation",        "F", "R", -1),
    ("FIN05 Payout / FCF",                "F", "R", +1),
    ("FIN06 Debt due < 24 months",        "F", "P", +1),
    ("MDY01 Issuer rating (ordinal)",     "F", "R", -1),
    ("MDY02 Adj. debt / adj. EBITDA",     "F", "R", +1),
    ("FIN07 ROCE",                        "F", "R", -1),
    ("FIN08 Reserve life",                "F", "R", -1),
]

SUBGROUPS = ["G1"] * 4 + ["G2"] * 6 + ["G3"] * 4 + ["G4"] * 3 + ["G5"] * 3


def build(seed=7):
    rng = np.random.default_rng(seed)
    N = len(SUBGROUPS)
    F = len(FIELDS)
    Y = len(YEARS)

    names  = [f"CO-{i+1:02d}" for i in range(N)]
    groups = np.array(SUBGROUPS)
    ftype  = np.array([f[2] for f in FIELDS])
    pol    = np.array([f[3] for f in FIELDS], float)
    pillar = np.array([f[1] for f in FIELDS])

    # ---- company traits -------------------------------------------------
    qual   = rng.normal(0, 1, N)                    # >0 = dirtier / weaker
    volume = np.exp(rng.normal(4.0, 0.8, N))        # production or throughput
    margin = np.exp(rng.normal(0.0, 0.35, N))       # revenue per unit volume
    labour = np.exp(rng.normal(0.0, 0.40, N))       # volume per head
    drift  = 0.45 * qual + rng.normal(0, 0.18, N)  # deterioration loads on weakness
    disc   = np.clip(rng.beta(9, 1.6, N), 0.45, 1.0) # disclosure propensity
    disc[[4, 13]] = 0.55                             # two systematic non-disclosers
    cmult  = np.exp(rng.normal(0.7, 0.35, N))       # contractor vs employee ratio

    rev  = volume * margin
    head = volume / labour

    grow = np.linspace(1.0, 1.0, Y)[None, :] + drift[:, None] * np.linspace(0, 1, Y)[None, :]
    grow = np.clip(grow, 0.3, 3.0)                  # (N,Y) multiplicative path

    BASE = np.empty((N, Y, 3))
    BASE[:, :, 0] = rev[:, None]   * np.linspace(1.0, 1.25, Y)[None, :]
    BASE[:, :, 1] = volume[:, None] * np.linspace(1.0, 1.10, Y)[None, :]
    BASE[:, :, 2] = head[:, None]  * np.linspace(1.0, 1.05, Y)[None, :]

    RAW = np.full((N, F, Y, 3), np.nan)

    for f, (name, P, t, _) in enumerate(FIELDS):
        fe = rng.normal(0, 0.6)                     # field effect

        if t == "Q":
            inten = np.exp(0.85 * qual + fe + rng.normal(0, 0.28, N))
            lvl = (inten * volume)[:, None] * grow
            for b in range(3):
                RAW[:, f, :, b] = lvl

        elif t == "R":
            r0 = np.exp(0.75 * qual + fe + rng.normal(0, 0.24, N))
            emp = r0[:, None] * grow
            con = (r0 * cmult)[:, None] * grow * (1 + rng.normal(0, 0.05, (N, Y)))
            wf  = 0.6 * emp + 0.4 * con
            RAW[:, f, :, 0] = emp
            RAW[:, f, :, 1] = con
            RAW[:, f, :, 2] = wf

        elif t == "P":
            p = 100.0 / (1.0 + np.exp(-(1.0 * qual + fe)))
            lvl = np.clip(p[:, None] * grow, 0.1, 99.9)
            for b in range(3):
                RAW[:, f, :, b] = lvl

        else:  # B
            pr = 1.0 / (1.0 + np.exp(1.3 * qual - fe))
            bits = (rng.random((N, Y)) < pr[:, None]).astype(float)
            bits = np.maximum.accumulate(bits, axis=1)      # policies do not get revoked
            for b in range(3):
                RAW[:, f, :, b] = bits

    # deliberate heavy outlier on one quantity field, to separate the normalisers
    RAW[0, 1, :, :] *= 55.0

    # missing data, clustered by company
    miss = rng.random((N, F, Y)) > disc[:, None, None] * 0.94
    RAW[np.repeat(miss[:, :, :, None], 3, axis=3)] = np.nan

    return dict(names=names, groups=groups, ftype=ftype, pol=pol, pillar=pillar,
                RAW=RAW, BASE=BASE, fields=[f[0] for f in FIELDS], years=YEARS)
