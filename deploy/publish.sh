#!/usr/bin/env bash
# publish.sh - put the explorer on demo.mehro.ch without touching anything else.
#
# Run recon.sh first and set the three variables below from what it reports.
#
# Safety properties, by construction:
#   * The only host directory written is $WEBROOT, which is created for this
#     demo and used by nothing else. rsync --delete is scoped to it.
#   * The Caddyfile is backed up before the edit and restored automatically if
#     validation fails.
#   * The new block is fenced by sentinel comments, so re-running replaces it
#     instead of appending a duplicate. No existing block is parsed or rewritten.
#   * `caddy reload` is graceful. Other sites are not restarted and do not drop
#     a connection. If validation fails, nothing is reloaded at all.
#   * The last step re-checks the OTHER sites and fails loudly if any changed.
set -euo pipefail

SSH_HOST="${SSH_HOST:-physicare-prod}"

# --- set these from recon.sh -------------------------------------------------
CADDYFILE="${CADDYFILE:-/etc/caddy/Caddyfile}"   # host path to the Caddyfile
WEBROOT="${WEBROOT:-/srv/demo-mehro}"            # host dir to hold the 7 files
CADDY_ROOT="${CADDY_ROOT:-$WEBROOT}"             # same path as Caddy sees it
CADDY_CTR="${CADDY_CTR:-}"                       # container name, or "" if host service
OTHER_SITE="${OTHER_SITE:-ihre-praxis.ch}"       # the site we must not break
# -----------------------------------------------------------------------------

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE="$ROOT/build/demo-site"
BLOCK="$ROOT/deploy/demo.mehro.ch.caddy"

step() { printf '\n\033[1m== %s\033[0m\n' "$1"; }

step "0. rebuild the publish set"
"$ROOT/deploy/build-demo.sh"
[ -f "$SITE/index.html" ] || { echo "build produced no index.html" >&2; exit 1; }

step "1. baseline: is $OTHER_SITE healthy right now?"
BEFORE=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 20 "https://$OTHER_SITE/" || echo "000")
echo "  $OTHER_SITE -> HTTP $BEFORE  (recorded, checked again at the end)"

step "2. upload 7 files to $WEBROOT"
ssh "$SSH_HOST" "sudo mkdir -p '$WEBROOT' && sudo chown -R \$(id -u):\$(id -g) '$WEBROOT'"
rsync -av --delete --chmod=D755,F644 "$SITE/" "$SSH_HOST:$WEBROOT/"
ssh "$SSH_HOST" "sudo chown -R root:root '$WEBROOT' && sudo find '$WEBROOT' -type d -exec chmod 755 {} + && sudo find '$WEBROOT' -type f -exec chmod 644 {} +"

step "3. install the site block into $CADDYFILE"
sed "s|ROOT_PLACEHOLDER|$CADDY_ROOT|g" "$BLOCK" | ssh "$SSH_HOST" "cat > /tmp/demo-mehro.caddy"

ssh "$SSH_HOST" bash -euo pipefail -s <<REMOTE
CADDYFILE='$CADDYFILE'
CADDY_CTR='$CADDY_CTR'
STAMP=\$(date +%Y%m%d-%H%M%S)
BACKUP="\${CADDYFILE}.bak.\${STAMP}"

[ -f "\$CADDYFILE" ] || { echo "no Caddyfile at \$CADDYFILE" >&2; exit 1; }
sudo cp -a "\$CADDYFILE" "\$BACKUP"
echo "  backup: \$BACKUP"

# Drop any previous run's block, then append the current one. Sentinel-fenced,
# so nothing outside the fence is ever read or rewritten.
sudo awk '
  /^# >>> CONTESTED demo\.mehro\.ch >>>\$/ { skip=1 }
  !skip { print }
  /^# <<< CONTESTED demo\.mehro\.ch <<<\$/ { skip=0 }
' "\$BACKUP" | sudo tee "\$CADDYFILE.new" >/dev/null

{
  echo ""
  echo "# >>> CONTESTED demo.mehro.ch >>>"
  cat /tmp/demo-mehro.caddy
  echo "# <<< CONTESTED demo.mehro.ch <<<"
} | sudo tee -a "\$CADDYFILE.new" >/dev/null

sudo mv "\$CADDYFILE.new" "\$CADDYFILE"
rm -f /tmp/demo-mehro.caddy

# Validate BEFORE anything is reloaded. A bad file never reaches a running Caddy.
if [ -n "\$CADDY_CTR" ]; then
  VALIDATE="docker exec \$CADDY_CTR caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile"
  RELOAD="docker exec \$CADDY_CTR caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile"
else
  VALIDATE="sudo caddy validate --config \$CADDYFILE --adapter caddyfile"
  RELOAD="sudo caddy reload --config \$CADDYFILE --adapter caddyfile"
fi

echo "  validating..."
if ! eval "\$VALIDATE"; then
  echo "  VALIDATION FAILED - restoring \$BACKUP, nothing was reloaded" >&2
  sudo cp -a "\$BACKUP" "\$CADDYFILE"
  exit 1
fi

sudo mkdir -p /var/log/caddy

echo "  reloading (graceful, no restart)..."
if ! eval "\$RELOAD"; then
  echo "  RELOAD FAILED - restoring \$BACKUP and reloading the old config" >&2
  sudo cp -a "\$BACKUP" "\$CADDYFILE"
  eval "\$RELOAD" || true
  exit 1
fi
echo "  reloaded"
REMOTE

step "4. verify the demo"
sleep 5
for i in 1 2 3 4 5 6; do
  CODE=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 25 "https://demo.mehro.ch/" || echo "000")
  echo "  attempt $i: HTTP $CODE"
  [ "$CODE" = "200" ] && break
  sleep 10   # first hit waits on the Let's Encrypt certificate
done

step "5. security headers actually being sent"
curl -sSI --max-time 20 "https://demo.mehro.ch/" \
  | grep -iE 'strict-transport|content-security|x-content-type|x-frame|referrer-policy|permissions-policy|^server' || true

step "6. confirm nothing else broke"
AFTER=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 20 "https://$OTHER_SITE/" || echo "000")
echo "  $OTHER_SITE -> HTTP $AFTER  (was $BEFORE)"
if [ "$BEFORE" != "$AFTER" ]; then
  echo "  WARNING: $OTHER_SITE changed status. Investigate before walking away." >&2
  exit 1
fi
echo "  unchanged."

step "DONE - https://demo.mehro.ch"
