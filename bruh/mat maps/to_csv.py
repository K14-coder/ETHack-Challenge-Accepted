#!/usr/bin/env python3
"""
to_csv.py — turn the Bloomberg materiality exports and the credit comps workbook
into CSVs a program can read.

    python3 to_csv.py            # writes ./csv/

Output
    csv/raw/<TICKER>_ES.csv          faithful dump of the ES Materiality sheet
    csv/raw/<TICKER>_G.csv           faithful dump of the G Materiality sheet
    csv/raw/credit_<sheet>.csv       one per sheet of the credit comps workbook
    csv/materiality_long.csv         tidy: one row per ticker x field x year
    csv/materiality_wide.csv         tidy: one row per ticker x field, years across
    csv/coverage.csv                 per ticker: fields, and how many have 3+ years
    csv/companies.csv               ticker -> peer group, from the exports themselves

Everything is UTF-8 with a BOM so Excel opens it without mangling, comma
separated, quoted where needed. Header names are flattened to single-line
snake_case. Blank Pillar / Issue / Sub-Issue cells are forward-filled, because
Bloomberg only prints them on the first row of each block.
"""

import csv
import glob
import os
import re
import unicodedata

import openpyxl

OUT = "csv"
RAW = os.path.join(OUT, "raw")
YEARS = [2021, 2022, 2023, 2024, 2025]


def slug(s):
    if s is None:
        return ""
    s = str(s).replace("\n", " ").replace("\r", " ")
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^0-9A-Za-z]+", "_", s).strip("_").lower()
    return s


def clean(v):
    """One cell -> a string fit for CSV. Bloomberg's blanks all become ''."""
    if v is None:
        return ""
    if isinstance(v, str):
        v = v.strip()
        if v in ("—", "-", "--", "n/a", "N/A", "#N/A", "#N/A N/A", ""):
            return ""
        return v
    return v


def numeric(v):
    """The same cell as a number, or '' when it is not one."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v
    if isinstance(v, str):
        t = v.strip().replace(",", "")
        if re.fullmatch(r"-?\d+(\.\d+)?([eE][-+]?\d+)?", t):
            return float(t)
    return ""


def writer(path, header):
    fh = open(path, "w", newline="", encoding="utf-8-sig")
    w = csv.writer(fh)
    w.writerow(header)
    return fh, w


def dump_sheet(ws, path):
    """Faithful dump: every cell, every row, newlines flattened."""
    fh = open(path, "w", newline="", encoding="utf-8-sig")
    w = csv.writer(fh)
    for row in ws.iter_rows(values_only=True):
        w.writerow(["" if c is None else str(c).replace("\n", " ") for c in row])
    fh.close()


def read_materiality(path):
    """One workbook -> (ticker, peer_group, [record, ...])."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ticker = peer = ""
    records = []

    for sheet, kind in (("ES Materiality", "ES"), ("G Materiality", "G")):
        if sheet not in wb.sheetnames:
            continue
        ws = wb[sheet]
        rows = list(ws.iter_rows(values_only=True))

        # row 2 carries: Ticker | XXX US Equity | | Peer Group | <group>
        if len(rows) > 1:
            if not ticker and rows[1][1]:
                ticker = str(rows[1][1]).split()[0]
            if not peer and len(rows[1]) > 4 and rows[1][4]:
                peer = str(rows[1][4]).strip()

        # header is row 5 (index 4); data starts after it
        hdr = [clean(c) for c in rows[4]] if len(rows) > 4 else []
        if kind == "ES":
            cols = dict(pillar=0, theme=None, issue=1, sub_issue=2,
                        field=3, field_id=4, units=5, y0=6)
        else:
            cols = dict(pillar=0, theme=1, issue=2, sub_issue=3,
                        field=4, field_id=5, units=None, y0=6)

        carry = {"pillar": "", "theme": "", "issue": "", "sub_issue": ""}
        for row in rows[5:]:
            if row is None or all(c is None for c in row):
                continue
            get = lambda k: clean(row[cols[k]]) if cols[k] is not None and cols[k] < len(row) else ""
            for k in carry:
                v = get(k)
                if v:
                    carry[k] = str(v)
            fid = str(get("field_id")).strip()
            field = str(get("field")).strip()
            if not fid or not field:
                continue                       # section headers and spacers
            rec = dict(ticker=ticker, peer_group=peer, sheet=kind,
                       pillar=carry["pillar"], theme=carry["theme"],
                       issue=carry["issue"], sub_issue=carry["sub_issue"],
                       field=field, field_id=fid,
                       units=str(get("units")).strip())
            for i, y in enumerate(YEARS):
                j = cols["y0"] + i
                rec[str(y)] = clean(row[j]) if j < len(row) else ""
            records.append(rec)
    wb.close()
    return ticker, peer, records


def main():
    os.makedirs(RAW, exist_ok=True)
    files = sorted(f for f in glob.glob("*.xlsx") if not f.startswith("~$"))
    credit = [f for f in files if "credit" in f.lower() or "comps" in f.lower()]
    maps = [f for f in files if f not in credit]

    long_fh, long_w = writer(os.path.join(OUT, "materiality_long.csv"),
        ["ticker", "peer_group", "sheet", "pillar", "theme", "issue", "sub_issue",
         "field", "field_id", "units", "year", "value_raw", "value"])
    wide_fh, wide_w = writer(os.path.join(OUT, "materiality_wide.csv"),
        ["ticker", "peer_group", "sheet", "pillar", "theme", "issue", "sub_issue",
         "field", "field_id", "units"] + [f"y{y}" for y in YEARS] + ["years_reported"])
    cov_fh, cov_w = writer(os.path.join(OUT, "coverage.csv"),
        ["ticker", "peer_group", "sheet", "fields", "fields_with_3plus_years",
         "coverage_pct", "cells_filled", "cells_total"])
    co_fh, co_w = writer(os.path.join(OUT, "companies.csv"),
        ["ticker", "peer_group", "source_file", "es_fields", "g_fields"])

    grand = 0
    for f in maps:
        ticker, peer, recs = read_materiality(f)
        if not ticker:
            print("  !! no ticker found in", f, "- skipped")
            continue

        wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
        for sheet, tag in (("ES Materiality", "ES"), ("G Materiality", "G")):
            if sheet in wb.sheetnames:
                dump_sheet(wb[sheet], os.path.join(RAW, f"{ticker}_{tag}.csv"))
        wb.close()

        per_sheet = {}
        for r in recs:
            filled = 0
            for y in YEARS:
                v = r[str(y)]
                long_w.writerow([r["ticker"], r["peer_group"], r["sheet"], r["pillar"],
                                 r["theme"], r["issue"], r["sub_issue"], r["field"],
                                 r["field_id"], r["units"], y, v, numeric(v)])
                if v != "":
                    filled += 1
            wide_w.writerow([r["ticker"], r["peer_group"], r["sheet"], r["pillar"],
                             r["theme"], r["issue"], r["sub_issue"], r["field"],
                             r["field_id"], r["units"]] +
                            [r[str(y)] for y in YEARS] + [filled])
            s = per_sheet.setdefault(r["sheet"], [0, 0, 0])
            s[0] += 1
            s[1] += 1 if filled >= 3 else 0
            s[2] += filled

        for tag in ("ES", "G"):
            if tag in per_sheet:
                n, n3, cells = per_sheet[tag]
                cov_w.writerow([ticker, peer, tag, n, n3,
                                round(100 * cells / (n * len(YEARS)), 1), cells, n * len(YEARS)])
        co_w.writerow([ticker, peer, f,
                       per_sheet.get("ES", [0])[0], per_sheet.get("G", [0])[0]])
        grand += len(recs)
        print(f"  {ticker:6} {peer:28} {len(recs):4} fields   <- {f}")

    for fh in (long_fh, wide_fh, cov_fh, co_fh):
        fh.close()

    for f in credit:
        wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
        for sn in wb.sheetnames:
            dump_sheet(wb[sn], os.path.join(RAW, f"credit_{slug(sn)}.csv"))
        wb.close()
        print(f"  credit workbook: {len(wb.sheetnames)} sheets <- {f}")

    print(f"\n{len(maps)} materiality exports, {grand} field rows, "
          f"{grand * len(YEARS)} long rows. Written to ./{OUT}/")


if __name__ == "__main__":
    main()
