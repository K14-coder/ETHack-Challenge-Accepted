/* Edge middleware — HTTP Basic Auth in front of the whole deployment.
 *
 * This runs at Vercel's edge BEFORE any static file is served, so a request
 * without the password never receives a single byte of the app: not the HTML,
 * not the JavaScript, and not the 6.6 MB pillar cube.
 *
 * It is access control, not encryption. Anyone you DO give the password to can
 * open developer tools and save the files, because a browser cannot render what
 * it has not downloaded. There is no configuration on any host that changes
 * that. What this does guarantee is that the set of people who can obtain the
 * files is exactly the set of people you hand the password to.
 *
 * Set SITE_USER and SITE_PASSWORD in the Vercel project's environment variables.
 */

export const config = {
  // everything except Vercel's own internal endpoints
  matcher: "/((?!_vercel/).*)",
};

function safeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

export default function middleware(request) {
  const user = process.env.SITE_USER;
  const pass = process.env.SITE_PASSWORD;

  // fail closed: an unconfigured deployment serves nothing
  if (!user || !pass) {
    return new Response(
      "This deployment has no SITE_USER / SITE_PASSWORD configured, so it is " +
      "serving nothing. Set both in the Vercel project settings and redeploy.",
      { status: 503, headers: { "content-type": "text/plain; charset=utf-8" } }
    );
  }

  const expected = "Basic " + btoa(`${user}:${pass}`);
  const given = request.headers.get("authorization") || "";

  if (!safeEqual(given, expected)) {
    return new Response("Authentication required.", {
      status: 401,
      headers: {
        "WWW-Authenticate": 'Basic realm="CONTESTED — ETHack 2026", charset="UTF-8"',
        "content-type": "text/plain; charset=utf-8",
        "x-robots-tag": "noindex, nofollow",
      },
    });
  }
}
