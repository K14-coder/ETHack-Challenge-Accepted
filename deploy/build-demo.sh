#!/usr/bin/env bash
# build-demo.sh - assemble exactly what goes public. Nothing else.
#
# The publish set is derived from what index.html actually loads. Everything
# else in ETHack/web (the .json duplicates, the speccurve prototype data, the
# internal README) stays off the server.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/ETHack/web"
OUT="$ROOT/build/demo-site"

rm -rf "$OUT"
mkdir -p "$OUT/assets" "$OUT/data"

# The six files the page loads, plus robots.txt.
cp "$SRC/index.html"          "$OUT/index.html"
cp "$SRC/assets/styles.css"   "$OUT/assets/styles.css"
cp "$SRC/assets/app.js"       "$OUT/assets/app.js"
cp "$SRC/assets/charts.js"    "$OUT/assets/charts.js"
cp "$SRC/assets/compute.js"   "$OUT/assets/compute.js"
cp "$SRC/data/model.js"       "$OUT/data/model.js"
cp "$SRC/robots.txt"          "$OUT/robots.txt"

# meta.source carries an internal working path. No code reads it; strip it.
python3 - "$OUT/data/model.js" <<'PY'
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
before = s
s = s.replace(
    '"source":"Bloomberg materiality maps + FY2025 credit workbook, bruh/mat maps/"',
    '"source":"Bloomberg materiality maps + FY2025 credit workbook"')
assert s != before, "meta.source pattern not found - check the export format"
open(p, "w", encoding="utf-8").write(s)
PY

# The payload must still parse as the assignment the page expects.
python3 - "$OUT/data/model.js" <<'PY'
import json, sys
s = open(sys.argv[1], encoding="utf-8").read().strip()
assert s.startswith("window.MODEL="), "model.js no longer starts with the assignment"
d = json.loads(s[len("window.MODEL="):].rstrip(";"))
assert len(d["P"]) == 17496, f"expected 17496 specs, got {len(d['P'])}"
assert len(d["companies"]) == 18
assert "bruh" not in json.dumps(d["meta"])
print(f"  model.js verified: {len(d['P'])} specs x {len(d['companies'])} companies")
PY

# Refuse to ship anything that should never leave the repo.
if grep -rlI -e "bruh/mat maps" -e "BEGIN .*PRIVATE KEY" "$OUT" 2>/dev/null | grep -q .; then
  echo "REFUSING: internal reference found in the publish set" >&2
  exit 1
fi

echo "built $OUT"
find "$OUT" -type f | sed "s|$OUT|  .|" | sort
echo "  total: $(du -sh "$OUT" | cut -f1)"
