"""
registry.py — what every field is, and which way is better.

Built from the question set (`CONTESTED_question_set_and_data_request.xlsx`,
sheets Questions / Boolean signs / Governance polarity) joined to what the
Bloomberg materiality maps actually delivered. A field that was planned but not
delivered does not exist here; a field delivered but not planned is kept only if
we can type it and orient it.

Three attributes decide how a field is treated:

    type      Q quantity   needs an exposure base
              R rate       already divided; the base selects a variant if one exists
              P percentage unitless
              B boolean    Y/N
              S structural a governance count or level, unitless

    polarity  +1 if a LOWER raw value is better, -1 if HIGHER is better.
              Held under three conventions, because for a large part of the
              governance sheet the two defensible conventions disagree:
                orthodox   governance orthodoxy (short tenure, low pay, refreshment)
                neutral    the contested field is scored 50 and discriminates nothing
                stability  the continuity reading (experience, retained knowledge)

    tier      only for booleans. Which stringency level counts the field:
              all < substantive < outcome-linked.
"""

import os
import re

import numpy as np
import pandas as pd

# resolved against this file, not the working directory, so the pipeline runs
# from anywhere
HERE = os.path.dirname(os.path.abspath(__file__))
QSET = os.path.join(HERE, "..", "contested",
                    "CONTESTED_question_set_and_data_request.xlsx")

PILLAR_OF = {"ENVIRONMENTAL": "E", "SOCIAL": "S", "GOVERNANCE": "G"}

# Polarity for the E/S fields, which the question set leaves blank because the
# direction is not contested there. Keyword rules, then explicit overrides for
# everything the rules would get wrong. Printed by `python3 registry.py` so the
# whole table can be checked by eye.
HIGHER_IS_BETTER = re.compile(
    r"recycl|renewable|training|reduction target|diversity|independen|attendance|"
    r"women|female|minorit|efficiency|reuse|restored|rehabilitat",
    re.I)
LOWER_IS_BETTER = re.compile(
    r"emission|flar|spill|waste|withdraw|consumption|discharge|fine|penalt|"
    r"incident|fatalit|injur|lost time|accident|leak|methane|hazardous|"
    r"violation|complaint|breach|carbon",
    re.I)

POLARITY_OVERRIDE = {
    "SA023": -1.0,   # % hazardous waste RECYCLED, higher is better
    "SA016": +1.0,   # % of total waste that is hazardous, lower is better
    "SA055": +1.0,   # % methane of Scope 1, lower is better
    "ES199": -1.0,   # total employee training hours, higher is better
    "RX312": -1.0,   # training spend per employee, higher is better
    "F1284": +1.0,   # embedded carbon in reserves, lower is better
}


def _norm(s):
    return "" if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()


def build(delivered_ids=None):
    """Returns a DataFrame indexed by field_id. `delivered_ids` restricts it to
    what the materiality maps actually contain."""
    q = pd.read_excel(QSET, "Questions", header=1)
    q = q[q["Field ID"].notna()].copy()
    q["field_id"] = q["Field ID"].astype(str).str.strip()

    bs = pd.read_excel(QSET, "Boolean signs", header=1)
    bs = bs[bs["Field ID"].notna()].copy()
    bs["field_id"] = bs["Field ID"].astype(str).str.strip()
    bs = bs.set_index("field_id")

    gp = pd.read_excel(QSET, "Governance polarity", header=1)
    gp = gp[gp["Field ID"].notna()].copy()
    gp["field_id"] = gp["Field ID"].astype(str).str.strip()
    gp = gp.set_index("field_id")

    rows = []
    for _, r in q.iterrows():
        fid = r["field_id"]
        if delivered_ids is not None and fid not in delivered_ids:
            continue
        typ = _norm(r["Type"])[:1] or "S"
        pillar = PILLAR_OF.get(_norm(r["Pillar"]), "G")
        name = _norm(r["Bloomberg field"])

        # ---- polarity under the three conventions
        if fid in gp.index:
            orth = _dir_to_pol(gp.loc[fid, "Governance-orthodox"])
            stab = _dir_to_pol(gp.loc[fid, "Stability-orthodox"])
            contested = _norm(gp.loc[fid, "Do they disagree?"]).lower() == "yes"
        elif typ == "B":
            fav = _norm(r["Favourable state"])
            if fav.startswith("No"):
                orth = +1.0                      # presence is the bad state
            elif fav.startswith("CONTESTED"):
                orth = +1.0
            else:
                orth = -1.0                      # presence is the good state
            stab, contested = orth, False
            if fid in bs.index:
                contested = _norm(bs.loc[fid, "Favourable state"]).startswith("CONTESTED")
                if contested:
                    stab = -orth
        else:
            orth = POLARITY_OVERRIDE.get(fid)
            if orth is None:
                if HIGHER_IS_BETTER.search(name):
                    orth = -1.0
                elif LOWER_IS_BETTER.search(name):
                    orth = +1.0
                else:
                    orth = +1.0                  # default: less of it is better
            stab, contested = orth, False

        # ---- boolean stringency tier
        tier = _norm(r["Stringency tier"]) or ("all only" if typ == "B" else "")

        rows.append(dict(
            field_id=fid, name=name, pillar=pillar, type=typ,
            issue=_norm(r["Issue"]), sub_issue=_norm(r["Sub-issue"]),
            units=_norm(r["Unit"]), question=_norm(r["THE QUESTION"]),
            pol_orthodox=orth, pol_stability=stab, contested=bool(contested),
            tier=tier,
        ))

    reg = pd.DataFrame(rows).drop_duplicates("field_id").set_index("field_id")

    # A contested field scores 50 under the neutral convention: it is present in
    # the model and deliberately discriminates nothing. Encoded as polarity 0.
    reg["pol_neutral"] = np.where(reg.contested, 0.0, reg.pol_orthodox)
    return reg


def _dir_to_pol(v):
    v = _norm(v).lower()
    if v.startswith("lower"):
        return +1.0
    if v.startswith("higher"):
        return -1.0
    return 0.0            # neutral / both agree with no direction


TIER_RANK = {"all only": 0, "all": 0, "substantive": 1, "outcome-linked": 2}


def tier_ok(tier, level):
    """`level` 0 permissive, 1 majority, 2 strict."""
    return TIER_RANK.get(tier, 0) >= level


if __name__ == "__main__":
    reg = build()
    pd.set_option("display.width", 200)
    print(f"{len(reg)} fields\n")
    print(reg.groupby(["pillar", "type"]).size().unstack(fill_value=0), "\n")
    print(f"contested (the two conventions disagree): {int(reg.contested.sum())}")
    print(reg.tier.value_counts().to_dict(), "\n")
    print("--- E/S fields, derived polarity, check these by eye ---")
    es = reg[reg.pillar.isin(["E", "S"]) & (reg.type != "B")]
    for fid, r in es.iterrows():
        print(f"  {fid:6} {r.type} {'lower better' if r.pol_orthodox>0 else 'higher better':14} {r['name'][:56]}")
