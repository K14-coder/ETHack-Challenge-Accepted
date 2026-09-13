# deploy

Publishes the explorer to <https://demo.mehro.ch> as static files served by the
Caddy already running on the VPS. Nothing else on that box is touched.

## What is live

`/srv/mehro-demo` on the VPS, seven files, 6.8 MB. Served by a site block
appended to `/etc/caddy/Caddyfile`.

## The scripts

| | |
|---|---|
| `build-demo.sh` | Assembles `build/demo-site/` from `ETHack/web`: only the six files `index.html` actually loads, plus `robots.txt`. Strips the internal working path out of `meta.source`, then verifies the payload still parses and still holds 17,496 specifications. Refuses to build if an internal reference survives. |
| `demo.mehro.ch.caddy` | The site block, in the house style of the existing Caddyfile. |
| `recon.sh` | Read only. Reports containers, Caddy layout, mounts, configured sites, DNS. Changes nothing. |
| `publish.sh` | Build, upload, back up the Caddyfile, append, validate, reload, verify. Restores the backup automatically if validation or reload fails. |

## Republishing after a change to the tool

```bash
rsync -a --delete build/demo-site/ physicare-prod:/srv/mehro-demo/
```

Run `deploy/build-demo.sh` first. No Caddy reload is needed for a content
change: the site block already points at that directory, and HTML is served
`no-cache` so a refresh picks it up.

## Why it cannot damage the other projects

* **Append only.** The Caddyfile edit was verified as a pure append,
  `440a441,487`, with zero existing lines removed or modified.
* **Validated before reload.** `caddy validate` runs first. A config that does
  not parse never reaches the running server.
* **Graceful reload, not a restart.** `systemctl reload caddy` swaps the config
  in place. No container is stopped, started or recreated. All 20 containers
  kept their original uptime.
* **Its own directory.** `/srv/mehro-demo` is new and used by nothing else, so
  `rsync --delete` cannot reach another project's files.
* **Checked afterwards.** All 12 existing sites were probed before and after and
  returned identical status codes.

## The attack surface, and why it is small

The site is static files. There is no backend, no database, no reverse proxy, no
form, no upload path, no cookie, no session, and no user input of any kind. The
page makes no network request after load.

| Control | Effect |
|---|---|
| `GET`/`HEAD` only | `POST`, `PUT`, `DELETE` and everything else get 405 without reaching the file server |
| Dotfile matcher | `/.env`, `/.git/config` and friends get 404 |
| No `browse` | Directory listing is off: `/assets/` and `/data/` return 404 |
| `request_body max_size 4KB` | No request can push a large body at the server |
| Automatic HTTPS | HTTP gets a 308 to HTTPS; certificate from Let's Encrypt via TLS-ALPN |
| HSTS, one year, includeSubDomains | Browsers refuse plaintext to this host after the first visit |
| CSP `default-src 'none'` | Scripts are `'self'` only. `'unsafe-inline'` is on **style** only, because `charts.js` writes `style="width:..."` into the bars it renders |
| `frame-ancestors 'none'`, `X-Frame-Options DENY` | Cannot be framed, so no clickjacking |
| `Referrer-Policy no-referrer` | The URL never leaks to a third party |
| `-Server` | Caddy stops announcing itself |
| `robots.txt: Disallow: /` | Kept off search engines |

**What is published.** Derived pillar grades on a 0 to 100 scale, Bloomberg field
mnemonics and their human-readable names, and per-field coverage counts. **No
raw Bloomberg values are in the payload**, which is why this is publishable while
`bruh/mat maps/` stays withheld.

## If it ever needs to come down

```bash
ssh physicare-prod
sudo cp /etc/caddy/Caddyfile.bak-demo-20260913-111940 /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
sudo systemctl reload caddy
sudo rm -rf /srv/mehro-demo
```
