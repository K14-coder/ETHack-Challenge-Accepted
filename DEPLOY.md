# Deploying the explorer, password-gated

## What can and cannot be protected

Be clear about this before promising it to anyone.

**Can be guaranteed.** Nothing but the explorer ever reaches the host. The Python
pipeline, the working notes, the credit workbook, the government-data pipeline
and the git history are excluded by `.vercelignore` — they are not uploaded, not
built, not served. And the edge middleware runs *before* any file is delivered,
so a request without the password receives a 401 and **zero bytes** of the app:
not the HTML, not the JavaScript, not the 6.6 MB pillar cube.

**Cannot be guaranteed.** Anyone you *do* give the password to can save the
files. A browser cannot render what it has not downloaded, so the moment the
page works for a juror, that juror's machine holds a copy of `model.js`. No
setting on Vercel, Netlify, Cloudflare or anywhere else changes this. Anybody who
tells you otherwise is selling obfuscation, not protection.

So the real guarantee is: **the set of people who can obtain the files is exactly
the set of people you hand the password to.** For a jury link, that is the right
guarantee and it is enough.

Note also that `model.js` contains our model's *output* — four pillar scores per
company per specification. It does not contain Bloomberg's indicators or their
cell values. Even in the worst case, no licensed Bloomberg content is exposed.

## Deploy

One command, from the repo root. It will ask you to log in on first run.

```bash
npx vercel@latest login
```

Then set the credentials and ship:

```bash
npx vercel@latest env add SITE_USER production
npx vercel@latest env add SITE_PASSWORD production
npx vercel@latest --prod
```

`env add` prompts for the value rather than taking it on the command line, so the
password never lands in your shell history. Pick something you are happy to put
in an email to a jury.

On the first `--prod` run Vercel asks a few setup questions. The answers:

| Prompt | Answer |
|---|---|
| Set up and deploy? | yes |
| Which scope? | your personal account |
| Link to existing project? | no |
| Project name | `ethack-challenge-accepted` |
| In which directory is your code located? | `./` |
| Want to modify the settings? | no — `vercel.json` already sets them |

## Check it worked

```bash
curl -sI https://<your-deployment>.vercel.app | head -1
# expect: HTTP/2 401

curl -sI -u '<user>:<password>' https://<your-deployment>.vercel.app | head -1
# expect: HTTP/2 200
```

If the first one returns 200, the middleware is not running — check that
`middleware.js` is at the repo root and that both environment variables exist in
the **production** environment.

If either returns 503, the deployment is live but has no credentials configured.
That is the fail-closed path working as intended: it serves nothing rather than
serving the app unprotected.

## What is actually deployed

Everything under `ETHack/web/`, which is:

| | |
|---|---|
| `index.html` | ~9 KB |
| `assets/*.css`, `assets/*.js` | ~70 KB |
| `data/model.js` | 6.6 MB — the pillar cube, 17,496 specifications |
| `data/speccurve.js` | 250 KB — the synthetic reference dataset |
| `robots.txt` | disallow all |

No build step, no dependencies, no server-side code beyond the auth middleware.

`data/model.json` and `data/speccurve.json` are also in the folder and will be
uploaded; they are byte-identical copies of the `.js` files for programmatic use.
Delete them from `ETHack/web/data/` before deploying if you would rather not ship
14 MB twice — the page only loads the `.js`.

## If you would rather not share one password

Cloudflare Pages plus **Cloudflare Access** is free for up to 50 users and lets
you add jurors by email address; each gets a one-time code instead of a shared
secret, and you can revoke one person without changing anything for the others.
It needs a Cloudflare account and a few more steps than the above. Worth it if
the link is going to a named panel rather than a room.
