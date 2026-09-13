#!/usr/bin/env python3
"""
paper2pdf.py — typeset PAPER.md as a research note.

    python3 tools/paper2pdf.py

Writes build/PAPER.html and PAPER.pdf.

There is no pandoc or weasyprint on this machine, and installing a toolchain to
render one document is the wrong trade. Instead this is a small converter for
exactly the Markdown that PAPER.md uses, which buys something a general renderer
would not give us: semantic hooks. An `## Exhibit 7 · ...` heading and a bold
`**Exhibit 7 · ...**` paragraph are the same object and are styled as one; the
masthead becomes a tear sheet; italic paragraphs after a table become source
lines. Chrome then prints it, so the CSS is the whole design.
"""

import html
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "PAPER.md")
BUILD = os.path.join(ROOT, "build")
HTML_OUT = os.path.join(BUILD, "PAPER.html")
PDF_OUT = os.path.join(ROOT, "PAPER.pdf")

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


# ────────────────────────────────────────────────────────────────── inline

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


EXHIBIT = re.compile(r"^(?:\*\*)?Exhibit\s+(\d+)\s*·\s*(.+?)(?:\*\*)?$")


def exhibit_html(m):
    return (f'<div class="exhibit"><span class="exno">Exhibit {m.group(1)}</span>'
            f'<span class="extitle">{inline(m.group(2))}</span></div>')


# ────────────────────────────────────────────────────────────────── tables

def parse_table(lines, i):
    """A GFM pipe table starting at lines[i]. Returns (html, next_i) or None."""
    if i + 1 >= len(lines) or "|" not in lines[i]:
        return None
    sep = lines[i + 1].strip()
    if not re.fullmatch(r"\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?", sep):
        return None

    def cells(row):
        row = row.strip()
        if row.startswith("|"):
            row = row[1:]
        if row.endswith("|"):
            row = row[:-1]
        return [c.strip() for c in row.split("|")]

    align = []
    for c in cells(sep):
        if c.endswith(":") and c.startswith(":"):
            align.append("center")
        elif c.endswith(":"):
            align.append("right")
        else:
            align.append("left")

    head = cells(lines[i])
    body, j = [], i + 2
    while j < len(lines) and "|" in lines[j] and lines[j].strip():
        body.append(cells(lines[j]))
        j += 1

    # a two-column table with an empty header is a key/value block, not a grid
    keyval = len(head) == 2 and not any(h.strip() for h in head)

    out = ['<table class="%s">' % ("kv" if keyval else "grid")]
    if not keyval:
        out.append("<thead><tr>")
        for k, h in enumerate(head):
            a = align[k] if k < len(align) else "left"
            out.append(f'<th class="a-{a}">{inline(h)}</th>')
        out.append("</tr></thead>")
    out.append("<tbody>")
    for row in body:
        out.append("<tr>")
        for k, c in enumerate(row):
            a = align[k] if k < len(align) else "left"
            num = " num" if a == "right" else ""
            out.append(f'<td class="a-{a}{num}">{inline(c)}</td>')
        out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out), j


# ────────────────────────────────────────────────────────────────── blocks

def convert(md):
    lines = md.split("\n")
    out, i = [], 0
    in_masthead = True

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()

        if not s:
            i += 1
            continue

        # fenced code
        if s.startswith("```"):
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                buf.append(html.escape(lines[j]))
                j += 1
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>")
            i = j + 1
            continue

        # rules: the first closes the masthead
        if re.fullmatch(r"-{3,}", s):
            if in_masthead:
                out.append("</header>")
                in_masthead = False
            else:
                out.append('<hr class="sec">')
            i += 1
            continue

        # tables
        t = parse_table(lines, i)
        if t:
            out.append(t[0])
            i = t[1]
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            lvl, txt = len(m.group(1)), m.group(2)
            ex = EXHIBIT.match(txt)
            if ex:
                out.append(exhibit_html(ex))
            elif lvl == 1:
                out.append(f'<h1>{inline(txt)}</h1>')
            elif lvl == 2:
                cls = "appendix" if txt.startswith("Appendix") else "section"
                out.append(f'<h2 class="{cls}">{inline(txt)}</h2>')
            elif lvl == 3:
                cls = "subtitle" if in_masthead else ""
                out.append(f'<h3 class="{cls}">{inline(txt)}</h3>')
            else:
                out.append(f"<h{lvl}>{inline(txt)}</h{lvl}>")
            i += 1
            continue

        # blockquote
        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip("> ").rstrip())
                i += 1
            out.append(f'<blockquote>{inline(" ".join(buf))}</blockquote>')
            continue

        # lists
        if re.match(r"^[-*]\s+", s) or re.match(r"^\d+\.\s+", s):
            ordered = bool(re.match(r"^\d+\.\s+", s))
            tag = "ol" if ordered else "ul"
            items, pat = [], r"^\d+\.\s+" if ordered else r"^[-*]\s+"
            while i < len(lines):
                cur = lines[i].strip()
                if re.match(pat, cur):
                    items.append(re.sub(pat, "", cur))
                    i += 1
                elif cur and not re.match(r"^(#{1,6}\s|[-*]\s|\d+\.\s|>|```)", cur) \
                        and not parse_table(lines, i) and items:
                    items[-1] += " " + cur          # continuation line
                    i += 1
                else:
                    break
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items)
                       + f"</{tag}>")
            continue

        # paragraph — gather until a blank line or a block starter
        start = i
        buf = []
        while i < len(lines):
            cur = lines[i].strip()
            if not cur or re.match(r"^(#{1,6}\s|>|```|-{3,}$|[-*]\s|\d+\.\s)", cur) \
                    or parse_table(lines, i):
                break
            buf.append(cur)
            i += 1
        if i == start:                 # never leave the cursor where it was
            buf = [lines[i].strip()]
            i += 1
        para = " ".join(buf)

        ex = EXHIBIT.match(para)
        if ex:
            out.append(exhibit_html(ex))
            continue

        if in_masthead:
            for one in buf:                # each source line is its own line here
                out.append(f'<p class="meta">{inline(one)}</p>')
            continue

        # an all-italic paragraph directly after a table is a source line
        if para.startswith("*") and para.rstrip().endswith("*") \
                and not para.startswith("**") and out and "</table>" in out[-1]:
            out.append(f'<p class="source">{inline(para.strip("*"))}</p>')
            continue

        out.append(f"<p>{inline(para)}</p>")

    return "\n".join(out)


# ────────────────────────────────────────────────────────────────── shell

CSS = r"""
@page {
  size: A4;
  margin: 19mm 17mm 17mm;
  @bottom-center { content: counter(page); }
}

:root {
  --ink:    #101010;
  --ink-2:  #3d3c38;
  --ink-3:  #6b6a63;
  --line:   #dedcd6;
  --line-2: #b9b7b0;
  --rule:   #101010;
  --accent: #c04a12;
  --panel:  #f6f5f2;
}

* { box-sizing: border-box; }

html { font-size: 10.2pt; }

body {
  margin: 0;
  font-family: Charter, "Bitstream Charter", Georgia, "Times New Roman", serif;
  color: var(--ink);
  line-height: 1.46;
  font-kerning: normal;
  font-variant-ligatures: common-ligatures;
  text-rendering: optimizeLegibility;
  hanging-punctuation: first;
}

p { margin: 0 0 .62em; text-align: justify; hyphens: auto; }
p + p { text-indent: 0; }
strong { font-weight: 700; }
a { color: var(--ink); text-decoration: none; border-bottom: .4pt solid var(--line-2); }

code, pre {
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: .84em;
}
code { color: var(--ink-2); }
pre {
  margin: .7em 0 1em;
  padding: .68em .85em;
  background: var(--panel);
  border-left: 2pt solid var(--line-2);
  line-height: 1.42;
  white-space: pre-wrap;
  break-inside: avoid;
}

/* ───────────────────────────────────────────────────────── masthead */

header {
  border-bottom: 2.2pt solid var(--rule);
  padding-bottom: 9pt;
  margin-bottom: 13pt;
}
h1 {
  font-family: "Helvetica Neue", -apple-system, sans-serif;
  font-size: 30pt;
  font-weight: 700;
  letter-spacing: .10em;
  margin: 0 0 2pt;
  line-height: 1;
}
h3.subtitle {
  font-family: "Helvetica Neue", -apple-system, sans-serif;
  font-size: 12.2pt;
  font-weight: 400;
  color: var(--ink-2);
  margin: 0 0 11pt;
  letter-spacing: -.005em;
}
p.meta {
  font-family: "Helvetica Neue", -apple-system, sans-serif;
  font-size: 8.4pt;
  line-height: 1.5;
  color: var(--ink-3);
  margin: 0;
  text-align: left;
  letter-spacing: .015em;
}
p.meta strong { color: var(--ink); font-weight: 600; }

/* ───────────────────────────────────────────────────────── headings */

h2 {
  font-family: "Helvetica Neue", -apple-system, sans-serif;
  font-size: 13.2pt;
  font-weight: 700;
  letter-spacing: -.012em;
  margin: 20pt 0 7pt;
  padding-bottom: 3.5pt;
  border-bottom: .7pt solid var(--line-2);
  break-after: avoid;
}
h2.appendix {
  font-size: 11.6pt;
  text-transform: uppercase;
  letter-spacing: .085em;
  border-bottom-width: 1.4pt;
  border-bottom-color: var(--rule);
}
h3 {
  font-family: "Helvetica Neue", -apple-system, sans-serif;
  font-size: 10.4pt;
  font-weight: 700;
  margin: 13pt 0 4.5pt;
  break-after: avoid;
}
h4 {
  font-family: "Helvetica Neue", -apple-system, sans-serif;
  font-size: 9.6pt;
  margin: 11pt 0 3pt;
  break-after: avoid;
}

/* page discipline: results, risks and the appendix start fresh */
h2.appendix:first-of-type { break-before: page; }

blockquote {
  margin: 12pt 0 14pt;
  padding: 10pt 13pt;
  border-left: 2.6pt solid var(--accent);
  background: var(--panel);
  font-size: 11pt;
  line-height: 1.4;
  break-inside: avoid;
}
blockquote strong { font-weight: 700; }

/* ─────────────────────────────────────────────────────────── exhibits */

.exhibit {
  display: flex;
  align-items: baseline;
  gap: 7pt;
  margin: 15pt 0 5pt;
  padding-bottom: 3pt;
  border-bottom: 1.4pt solid var(--rule);
  break-after: avoid;
  break-inside: avoid;
}
.exno {
  font-family: "Helvetica Neue", -apple-system, sans-serif;
  font-size: 7.6pt;
  font-weight: 700;
  letter-spacing: .11em;
  text-transform: uppercase;
  color: #fff;
  background: var(--accent);
  padding: 1.6pt 5pt;
  border-radius: 1.5pt;
  white-space: nowrap;
}
.extitle {
  font-family: "Helvetica Neue", -apple-system, sans-serif;
  font-size: 10.2pt;
  font-weight: 700;
  letter-spacing: -.01em;
}

p.source {
  font-size: 7.8pt;
  color: var(--ink-3);
  font-style: italic;
  margin: -2pt 0 12pt;
  text-align: left;
}

/* ───────────────────────────────────────────────────────────── tables */

table {
  width: 100%;
  border-collapse: collapse;
  margin: 4pt 0 12pt;
  font-family: "Helvetica Neue", -apple-system, sans-serif;
  font-size: 8.5pt;
  line-height: 1.3;
  break-inside: auto;
}
thead { display: table-header-group; }
tr { break-inside: avoid; }
th {
  text-align: left;
  font-weight: 700;
  font-size: 7.9pt;
  letter-spacing: .028em;
  color: var(--ink-2);
  padding: 4pt 6pt;
  border-top: 1pt solid var(--rule);
  border-bottom: .6pt solid var(--line-2);
  background: var(--panel);
}
td {
  padding: 3.4pt 6pt;
  border-bottom: .4pt solid var(--line);
  vertical-align: top;
}
tbody tr:last-child td { border-bottom: 1pt solid var(--rule); }
.a-right  { text-align: right; }
.a-center { text-align: center; }
.num { font-variant-numeric: tabular-nums; white-space: nowrap; }

/* the tear-sheet: a two-column table with no header */
table.kv {
  margin: 11pt 0 14pt;
  border-top: 1.4pt solid var(--rule);
  border-bottom: 1.4pt solid var(--rule);
  font-size: 8.8pt;
}
table.kv td { padding: 4.4pt 7pt; border-bottom: .4pt solid var(--line); }
table.kv tr:last-child td { border-bottom: 0; }
table.kv td:first-child {
  width: 20%;
  font-weight: 700;
  color: var(--ink-2);
  white-space: nowrap;
}

ul, ol { margin: .3em 0 .8em; padding-left: 1.15em; }
li { margin-bottom: .24em; text-align: justify; hyphens: auto; }

hr.sec { border: 0; border-top: .6pt solid var(--line); margin: 15pt 0; }

/* widows and orphans throughout */
p, li, blockquote { orphans: 3; widows: 3; }
"""


def main():
    md = open(SRC, encoding="utf-8").read()
    body = convert(md)

    # start the body with an open <header>; convert() closes it at the first rule
    body = "<header>\n" + body

    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
           f'<title>CONTESTED — sector note</title><style>{CSS}</style>'
           f"</head><body>\n{body}\n</body></html>")

    os.makedirs(BUILD, exist_ok=True)
    with open(HTML_OUT, "w", encoding="utf-8") as fh:
        fh.write(doc)

    if not os.path.exists(CHROME):
        print(f"wrote {HTML_OUT}\nChrome not found at {CHROME}; open the HTML and "
              f"print to PDF manually.")
        return 0

    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw", "--virtual-time-budget=12000",
        f"--print-to-pdf={PDF_OUT}", "file://" + HTML_OUT,
    ], check=True, capture_output=True)

    kb = os.path.getsize(PDF_OUT) / 1024
    print(f"wrote {HTML_OUT}")
    print(f"wrote {PDF_OUT}  ({kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
