#!/usr/bin/env bash
# recon.sh - READ ONLY. Changes nothing. Run this before publish.sh.
#
# Answers the four questions that decide how the demo gets deployed without
# touching another project:
#   1. Is Caddy a container or a host service?
#   2. Where is the Caddyfile, on the host and inside the container?
#   3. Which host directories are already mounted into Caddy? (Putting the
#      demo inside one means no container has to be recreated.)
#   4. Which sites does the Caddyfile already serve?
set -uo pipefail
say() { printf '\n\033[1m== %s\033[0m\n' "$1"; }

say "host"
uname -srm; . /etc/os-release 2>/dev/null && echo "$PRETTY_NAME"; echo "uptime:$(uptime -p 2>/dev/null)"

say "containers (nothing here will be touched except Caddy's config reload)"
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' 2>&1 || echo "docker not available to this user"

say "who owns :80 and :443"
(ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null) | grep -E ':(80|443)\s' || echo "none found"

say "caddy as a host service?"
systemctl is-active caddy 2>/dev/null || echo "no active caddy systemd unit"
command -v caddy >/dev/null && caddy version || echo "no caddy binary on PATH"

say "caddy container detail"
CID=$(docker ps --filter 'ancestor=caddy' -q 2>/dev/null | head -1)
[ -z "${CID:-}" ] && CID=$(docker ps --format '{{.ID}} {{.Names}} {{.Image}}' 2>/dev/null | grep -i caddy | awk '{print $1}' | head -1)
if [ -n "${CID:-}" ]; then
  echo "container: $CID"
  echo "--- mounts (host -> container, rw/ro) ---"
  docker inspect "$CID" --format '{{range .Mounts}}{{.Source}} -> {{.Destination}} ({{if .RW}}rw{{else}}ro{{end}}){{"\n"}}{{end}}'
  echo "--- caddy version in container ---"
  docker exec "$CID" caddy version 2>&1 | head -2
else
  echo "no caddy container found"
fi

say "Caddyfile candidates on the host"
for p in /etc/caddy/Caddyfile /srv/Caddyfile /opt/caddy/Caddyfile /root/Caddyfile /home/ubuntu/Caddyfile; do
  [ -f "$p" ] && echo "FOUND $p  ($(wc -l < "$p") lines, modified $(date -r "$p" '+%Y-%m-%d %H:%M'))"
done
find /srv /opt /home /etc -maxdepth 4 -name 'Caddyfile*' -o -maxdepth 4 -name 'docker-compose*.y*ml' 2>/dev/null | grep -v -E '/(proc|sys)/' | head -20

say "site names already configured (names only, no config contents)"
for p in /etc/caddy/Caddyfile /srv/Caddyfile /opt/caddy/Caddyfile /root/Caddyfile /home/ubuntu/Caddyfile; do
  [ -f "$p" ] && { echo "--- $p ---"; grep -oE '^[a-z0-9*.-]+\.[a-z]{2,}[^{]*\{' "$p" | tr -d '{' ; }
done

say "is demo.mehro.ch already configured anywhere?"
grep -rl 'demo\.mehro\.ch' /etc/caddy /srv /opt /home 2>/dev/null | head || echo "no - clean slate"

say "DNS as this server sees it"
for h in demo.mehro.ch mehro.ch ihre-praxis.ch; do
  printf '%-18s A=%s AAAA=%s\n' "$h" "$(dig +short A "$h" | tr '\n' ',')" "$(dig +short AAAA "$h" | tr '\n' ',')"
done

say "disk headroom (the demo needs 7 MB)"
df -h / /srv 2>/dev/null | sort -u

say "RECON COMPLETE - nothing was modified"
