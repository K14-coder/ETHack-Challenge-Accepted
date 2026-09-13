#!/usr/bin/env python3
"""
CONTESTED - step 1: pull every input from free public APIs.

Run this on a machine with internet. Caches everything to data/raw/ so a
second run costs nothing. Safe to interrupt and restart.

    python3 01_fetch.py

Sources, all free, no API key:
  SEC XBRL frames   revenue, audited, from 10-K filings
  SEC company_tickers.json   ticker -> CIK
  EPA GHGRP (dmapservice)    reported facility emissions, rolled up to parent
  EPA Supply Chain GHG Emission Factors v1.3   kg CO2e per 2022 USD by NAICS
  yfinance (optional)        market cap, for the second denominator
"""
import csv, json, os, sys, time, urllib.request, urllib.parse
from pathlib import Path

YEAR      = 2023
RAW       = Path("data/raw");     RAW.mkdir(parents=True, exist_ok=True)
INTERIM   = Path("data/interim"); INTERIM.mkdir(parents=True, exist_ok=True)
UA        = {"User-Agent": "ETHack 2026 student project - aram@vartanian.de"}

# SEC revenue tags, tried in order. 'Revenues' alone MISSES most modern filers:
# Nucor's only 10-K value under it is FY2018. This fallback chain is mandatory.
REV_TAGS = [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "RevenuesNetOfInterestExpense",
    "SalesRevenueNet",
]
EEIO_URL = ("https://pasteur.epa.gov/uploads/10.23719/1531143/"
            "SupplyChainGHGEmissionFactors_v1.3.0_NAICS_CO2e_USD2022.csv")
DMAP = "https://data.epa.gov/dmapservice"


def get(url, cache_name=None, pause=0.3):
    """Fetch with cache. Returns bytes, or None on failure."""
    if cache_name:
        p = RAW / cache_name
        if p.exists() and p.stat().st_size > 0:
            return p.read_bytes()
    try:
        time.sleep(pause)
        b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    except Exception as e:
        print(f"    ! {type(e).__name__}: {e}")
        return None
    if cache_name:
        (RAW / cache_name).write_bytes(b)
    return b


def load_companies():
    with open("companies.csv") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- 1. CIKs
def fetch_ciks(rows):
    print("[1/5] ticker -> CIK")
    b = get("https://www.sec.gov/files/company_tickers.json", "company_tickers.json")
    if not b:
        sys.exit("  cannot reach sec.gov - check your network")
    m = {v["ticker"].upper(): (str(v["cik_str"]).zfill(10), v["title"])
         for v in json.loads(b).values()}
    for r in rows:
        cik, title = m.get(r["ticker"].upper(), (None, None))
        r["cik"], r["sec_name"] = cik, title
        print(f"  {r['ticker']:<6} {cik or 'NOT FOUND':<12} {title or ''}")
    return rows


# ---------------------------------------------------------------- 2. revenue
def fetch_revenue(rows):
    print(f"\n[2/5] revenue, CY{YEAR}, frames API  (one call per tag, ALL filers each)")
    by_cik = {}
    for tag in REV_TAGS:
        b = get(f"https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/USD/CY{YEAR}.json",
                f"frames_{tag}_CY{YEAR}.json")
        if not b:
            continue
        d = json.loads(b)
        n = 0
        for item in d.get("data", []):
            cik = str(item["cik"]).zfill(10)
            if cik not in by_cik:
                by_cik[cik] = (item["val"], tag)
                n += 1
        print(f"  {tag:<52} {len(d.get('data',[])):>6} filers, {n:>5} new")
    for r in rows:
        val, tag = by_cik.get(r.get("cik") or "", (None, None))
        r["revenue_usd"], r["revenue_tag"] = val, tag
        flag = "" if val else "   <-- MISSING, check tags"
        print(f"  {r['ticker']:<6} {(f'{val:,}' if val else 'none'):>20}  {tag or ''}{flag}")
    return rows


# ---------------------------------------------------------------- 3. GHGRP
def ghgrp_facilities(search):
    q = urllib.parse.quote(search)
    b = get(f"{DMAP}/ghg.pub_dim_facility/parent_company/contains/{q}/year/equals/{YEAR}/0:200/JSON",
            f"ghgrp_fac_{search.replace(' ','_').replace('-','_')}_{YEAR}.json")
    return json.loads(b) if b else []


def ghgrp_emissions(ids):
    """Batched. URL length is the real limit - keep batches to 7 ids."""
    out = {}
    for i in range(0, len(ids), 7):
        chunk = ids[i:i+7]
        b = get(f"{DMAP}/ghg.pub_facts_sector_ghg_emission/facility_id/in/"
                f"{','.join(map(str,chunk))}/year/equals/{YEAR}/0:300/JSON",
                f"ghgrp_emis_{chunk[0]}_{len(chunk)}_{YEAR}.json")
        if not b:
            continue
        for row in json.loads(b):
            v = row.get("co2e_emission")
            if v is not None:
                out[row["facility_id"]] = out.get(row["facility_id"], 0.0) + float(v)
    return out


def parse_share(parent_str, search):
    """Ownership share of the matching parent, from strings like
       'NUCOR CORP (51%); YAMATO KOGYO (USA) CORP (49%)'. Defaults to 1.0."""
    import re
    if not parent_str:
        return 1.0
    for part in parent_str.split(";"):
        if search.upper().replace("-", "").replace(" ", "") in \
           part.upper().replace("-", "").replace(" ", ""):
            m = re.search(r"\(([\d.]+)\s*%\)", part)
            return float(m.group(1)) / 100 if m else 1.0
    return 1.0


def fetch_ghgrp(rows):
    print(f"\n[3/5] EPA GHGRP disclosed Scope 1, FY{YEAR}")
    detail = []
    for r in rows:
        facs = ghgrp_facilities(r["ghgrp_search"])
        used = r["ghgrp_search"]
        if not facs and r.get("ghgrp_alt"):
            facs = ghgrp_facilities(r["ghgrp_alt"])
            used = r["ghgrp_alt"]
        if not facs:
            r.update(disclosed_full=None, disclosed_equity=None,
                     n_facilities=0, n_with_data=0, ghgrp_matched=used)
            print(f"  {r['ticker']:<6} 0 facilities                      <-- NO GHGRP PRESENCE")
            continue
        ids = sorted({f["facility_id"] for f in facs})
        emis = ghgrp_emissions(ids)
        shares = {f["facility_id"]: parse_share(f.get("parent_company"), used) for f in facs}
        full   = sum(emis.values())
        equity = sum(v * shares.get(k, 1.0) for k, v in emis.items())
        r.update(disclosed_full=(full or None), disclosed_equity=(equity or None),
                 n_facilities=len(ids), n_with_data=len(emis), ghgrp_matched=used)
        for f in facs:
            detail.append({"ticker": r["ticker"], "facility_id": f["facility_id"],
                           "facility_name": f.get("facility_name"), "state": f.get("state"),
                           "naics": f.get("naics_code"), "share": shares[f["facility_id"]],
                           "co2e_t": emis.get(f["facility_id"]),
                           "parent_company": f.get("parent_company")})
        print(f"  {r['ticker']:<6} {len(ids):>3} fac, {len(emis):>3} with data, "
              f"{full:>14,.0f} t full / {equity:>14,.0f} t equity")
    with open(INTERIM / "facilities.csv", "w", newline="") as f:
        if detail:
            w = csv.DictWriter(f, fieldnames=list(detail[0].keys())); w.writeheader(); w.writerows(detail)
    return rows


# ---------------------------------------------------------------- 4. EEIO
def fetch_eeio(rows):
    print("\n[4/5] EPA supply-chain emission factors")
    b = get(EEIO_URL, "eeio_v1.3_naics_co2e.csv")
    if not b:
        print("  ! could not fetch. modelled boundary unavailable.")
        for r in rows:
            r["eeio_with"] = r["eeio_without"] = None
        return rows
    table = {}
    for row in csv.DictReader(b.decode("utf-8-sig").splitlines()):
        code = (row.get("2017 NAICS Code") or "").strip()
        if not code:
            continue
        try:
            table[code] = (float(row["Supply Chain Emission Factors with Margins"]),
                           float(row["Supply Chain Emission Factors without Margins"]),
                           row.get("2017 NAICS Title", ""))
        except (ValueError, KeyError):
            pass
    print(f"  {len(table)} NAICS codes loaded")
    for r in rows:
        naics, hit = r["naics"], None
        # progressively shorter prefixes: the table mixes aggregation levels
        for n in (naics, naics[:5], naics[:4], naics[:3]):
            for cand in (n, n.ljust(6, "0")):
                if cand in table:
                    hit = (cand, table[cand]); break
            if hit: break
        if hit:
            code, (w, wo, title) = hit
            r.update(eeio_with=w, eeio_without=wo, eeio_naics=code, eeio_title=title)
            print(f"  {r['ticker']:<6} {naics} -> {code}  {w:>6.3f} / {wo:>6.3f}  {title[:40]}")
        else:
            r.update(eeio_with=None, eeio_without=None, eeio_naics=None, eeio_title=None)
            print(f"  {r['ticker']:<6} {naics} -> NO FACTOR FOUND")
    return rows


# ---------------------------------------------------------------- 5. market cap
def fetch_mktcap(rows):
    print("\n[5/5] market cap, for the second denominator (optional)")
    try:
        import yfinance as yf
    except ImportError:
        print("  yfinance not installed -> denominator dimension drops, 24 specs becomes 12.")
        print("  pip install yfinance   to enable it")
        for r in rows:
            r["market_cap_usd"] = None
        return rows
    for r in rows:
        try:
            mc = yf.Ticker(r["ticker"]).info.get("marketCap")
        except Exception:
            mc = None
        r["market_cap_usd"] = mc
        print(f"  {r['ticker']:<6} {(f'{mc:,}' if mc else 'none'):>20}")
    return rows


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    rows = load_companies()
    rows = fetch_ciks(rows)
    rows = fetch_revenue(rows)
    rows = fetch_ghgrp(rows)
    rows = fetch_eeio(rows)
    rows = fetch_mktcap(rows)

    cols = ["ticker","company","gics_sector","cik","sec_name","naics","eeio_naics","eeio_title",
            "revenue_usd","revenue_tag","market_cap_usd","disclosed_full","disclosed_equity",
            "n_facilities","n_with_data","ghgrp_matched","eeio_with","eeio_without","note"]
    with open(INTERIM / "companies.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

    have = lambda k: sum(1 for r in rows if r.get(k) not in (None, "", 0))
    print(f"""
wrote data/interim/companies.csv   ({len(rows)} companies)
wrote data/interim/facilities.csv  (facility detail)

coverage
  revenue          {have('revenue_usd'):>3}/30
  disclosed Sc1    {have('disclosed_full'):>3}/30   <- the ones WITHOUT this are the story
  EEIO factor      {have('eeio_with'):>3}/30
  market cap       {have('market_cap_usd'):>3}/30   <- 0 means 12 specs instead of 24

next:  python3 02_score.py""")
