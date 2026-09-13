#!/usr/bin/env python3
"""
CONTESTED - ETHack 2026, Challenge #1
Every number below was pulled from free public government APIs on 12 Sep 2026.
No paid data. No API key. Sources in SOURCES at the bottom.
"""
import csv, itertools, json

# ---------------------------------------------------------------- REAL DATA
# revenue        : SEC XBRL frames API, CY2023, form 10-K
# naics/factor   : EPA Supply Chain GHG Emission Factors v1.3 (kg CO2e / 2022 USD, with margins)
# disclosed_s1   : EPA GHGRP, facility emissions rolled up to parent, FY2023
COMPANIES = [
 # name,      cik,      revenue_usd,      naics,    eeio,  disc_s1_t,  n_fac, n_fac_with_data, note
 ("Walmart",  "104169", 642_637_000_000, "452311", 0.164,  None,        1,  0, "1 facility, HQ only, supplier subparts OO/QQ, co2e null every year 2012-2023"),
 ("Nucor",    "73309",   34_714_000_000, "331110", 0.787,  5_762_209.0,26, 26, "26 steel mills, all reporting, 2 jointly owned (51%)"),
 ("Ford",     "37996",  176_191_000_000, "336111", 0.240,    497_625.1,16, 10, "16 facilities in GHGRP, 10 with non-null emissions"),
 ("JPMorgan", "19617",  158_104_000_000,  None,    None,        0.0,    0,  0, "ZERO rows in GHGRP for 2023; only 2012-2014 as a petroleum products supplier (subpart MM)"),
]

MISSING_RULES = ["exclude", "worst_case", "modelled"]
BOUNDARIES    = ["A_disclosed_scope1", "C_modelled_full_chain"]

def intensity(c, boundary, missing_rule):
    """tonnes CO2e per million USD revenue. None = company drops out of this spec."""
    name, cik, rev, naics, eeio, disc, nf, nfd, note = c
    rev_m = rev / 1e6
    if boundary == "A_disclosed_scope1":
        if disc is None or disc == 0.0:
            if missing_rule == "exclude":    return None
            if missing_rule == "worst_case": return float("inf")
            if missing_rule == "modelled":
                return eeio * 1000 if eeio else None
        return disc / rev_m
    else:                                        # boundary C
        if eeio is None:
            if missing_rule == "exclude":    return None
            if missing_rule == "worst_case": return float("inf")
            if missing_rule == "modelled":   return None   # no factor, nothing to model from
        return eeio * 1000

def total_tonnes(c, boundary):
    name, cik, rev, naics, eeio, disc, nf, nfd, note = c
    if boundary == "A_disclosed_scope1": return disc
    return eeio * rev / 1000 if eeio else None

# ---------------------------------------------------------------- RUN
print("="*78); print("CONTESTED  ·  4 companies  ·  real data  ·  12 Sep 2026"); print("="*78)

print(f"\n{'company':<10}{'revenue $bn':>13}{'disclosed Sc1 t':>18}{'modelled t':>16}{'ratio':>9}")
print("-"*78)
rows=[]
for c in COMPANIES:
    name, cik, rev, naics, eeio, disc, nf, nfd, note = c
    mod = total_tonnes(c,"C_modelled_full_chain")
    ratio = (mod/disc) if (mod and disc) else None
    rows.append((name,rev,disc,mod,ratio))
    print(f"{name:<10}{rev/1e9:>13,.1f}"
          f"{('none' if disc is None else f'{disc:,.0f}'):>18}"
          f"{('n/a' if mod is None else f'{mod:,.0f}'):>16}"
          f"{('--' if ratio is None else f'{ratio:,.1f}x'):>9}")

print("\n" + "="*78)
print("THE RANKING INVERTS. Same data, same year, different defensible measure.")
print("="*78)
views = {
 "disclosed Scope 1 intensity (t/$M)": lambda c: (intensity(c,"A_disclosed_scope1","modelled") if c[5] in (None,0.0) else c[5]/(c[2]/1e6)),
 "modelled intensity (t/$M)":          lambda c: (c[4]*1000 if c[4] else None),
 "modelled TOTAL tonnes":              lambda c: total_tonnes(c,"C_modelled_full_chain"),
}
for label, fn in views.items():
    scored = [(c[0], fn(c)) for c in COMPANIES]
    scored = [(n,v) for n,v in scored if v is not None]
    scored.sort(key=lambda x:-x[1])
    print(f"\n  worst -> best by {label}")
    for i,(n,v) in enumerate(scored,1):
        print(f"    {i}. {n:<10}{v:>16,.1f}")

print("\n" + "="*78)
print("THE MISSING-DATA RULE, applied to boundary A. One choice, three worlds.")
print("="*78)
print(f"\n{'company':<10}" + "".join(f"{r:>16}" for r in MISSING_RULES))
print("-"*58)
for c in COMPANIES:
    cells=[]
    for r in MISSING_RULES:
        v = intensity(c,"A_disclosed_scope1",r)
        cells.append("dropped" if v is None else ("WORST" if v==float("inf") else f"{v:,.1f}"))
    print(f"{c[0]:<10}" + "".join(f"{x:>16}" for x in cells))

print("""
Read the Walmart row. Under 'exclude' it leaves the ranking entirely. Under
'worst_case' it is the dirtiest company in the sample. Under 'modelled' it sits
at 164 t/$M, mid-pack. Three defensible conventions, one company, three worlds.
Nobody publishing an ESG score tells you which one they used.
""")

with open("results.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["company","revenue_usd","disclosed_scope1_tco2e","modelled_tco2e","modelled_over_disclosed"])
    for r in rows: w.writerow(r)
print("wrote results.csv")

SOURCES = {
 "revenue":  "https://data.sec.gov/api/xbrl/frames/us-gaap/{TAG}/USD/CY2023.json  (TAG: RevenueFromContractWithCustomerExcludingAssessedTax, fallback Revenues)",
 "ghgrp_facilities": "https://data.epa.gov/dmapservice/ghg.pub_dim_facility/parent_company/contains/{NAME}/year/equals/2023/0:100/JSON",
 "ghgrp_emissions":  "https://data.epa.gov/dmapservice/ghg.pub_facts_sector_ghg_emission/facility_id/in/{IDS}/year/equals/2023/0:100/JSON",
 "eeio":     "https://pasteur.epa.gov/uploads/10.23719/1531143/SupplyChainGHGEmissionFactors_v1.3.0_NAICS_CO2e_USD2022.csv",
}
json.dump(SOURCES, open("sources.json","w"), indent=2)
