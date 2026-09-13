#!/usr/bin/env python3
"""build_pdf.py - render the SAME content file as the Word note, but to PDF.

docx_content.py is imperative: para(), table(), fig(), h1() and so on. This
module implements the identical call surface as an HTML emitter and execs the
same file, so the Word and PDF versions cannot drift. Chrome then prints it.
"""
import html as _html, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(ROOT, "figs")
BUILD = os.path.join(ROOT, "build"); os.makedirs(BUILD, exist_ok=True)
HTML_OUT = os.path.join(BUILD, "CONTESTED.html")
PDF_OUT = os.path.join(ROOT, "CONTESTED.pdf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

OUT = []
INK="101010"; INK2="3D3C38"; INK3="6B6A63"; ACC="C04A12"; LINE="DEDCD6"; PANEL="F6F5F2"

class _Fmt:
    def __init__(self): self.space_after=None; self.space_before=None; self.left_indent=None
class _Colour:
    def __init__(self): self.rgb=None
class _Run:
    def __init__(self, p):
        object.__setattr__(self,"p",p); object.__setattr__(self,"font",self)
        object.__setattr__(self,"bold",False); object.__setattr__(self,"italic",False)
        object.__setattr__(self,"size",None); object.__setattr__(self,"name",None)
        object.__setattr__(self,"color",_Colour())
    def __setattr__(self, k, v):
        object.__setattr__(self, k, v)
        if k == "text": self.p.buf.append(("run", v, self))
    def add_picture(self, path, width=None):
        OUT.append(f'<figure><img src="file://{path}"></figure>')
class _Para:
    def __init__(self): self.buf=[]; self.paragraph_format=_Fmt(); self.alignment=None
    def add_run(self, t=""):
        r=_Run(self); r.size=None
        if t: r.text=t
        return r
class _Doc:
    def add_paragraph(self, *a, **k):
        p=_Para(); OUT.append(("PARA", p)); return p
doc = _Doc()

def _inline(t):
    import re
    t=_html.escape(str(t), quote=False)
    t=re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t=re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    return t

def para(text="", size=9.5, bold=False, italic=False, color=INK, align=None,
         before=0, after=5, indent=0):
    cls = "small" if size < 8.5 else ""
    sty = f"color:#{color};font-size:{size}pt;margin:{before}pt 0 {after}pt;"
    body = _inline(text)
    if bold: body=f"<strong>{body}</strong>"
    if italic: body=f"<em>{body}</em>"
    OUT.append(f'<p class="{cls}" style="{sty}">{body}</p>')

def h1(t): OUT.append(f"<h1>{_inline(t)}</h1>")
def h2(t): OUT.append(f"<h2>{_inline(t)}</h2>")
def label(kind, num, title):
    tag = f"{kind} {num}".strip()
    OUT.append(f'<div class="exhibit"><span class="exno">{_html.escape(tag)}</span>'
               f'<span class="extitle">{_inline(title)}</span></div>')
def source(t): OUT.append(f'<p class="source">{_inline(t)}</p>')
def rule(width=12, color=INK, space=4):
    OUT.append(f'<hr style="border:0;border-top:{max(1,width/8):.1f}pt solid #{color};margin:{space}pt 0">')
def pagebreak(): OUT.append('<div class="pb"></div>')
def callout(text, color=ACC):
    OUT.append(f'<div class="callout" style="border-left-color:#{color}">{_inline(text)}</div>')
def fig(name, width=6.6):
    OUT.append(f'<figure><img src="file://{os.path.join(FIGS,name)}" '
               f'style="width:{width/8.27*100*0.86:.1f}%"></figure>')
def table(rows, widths=None, align=None, header=True, size=8.2, first_bold=False):
    tot = sum(widths) if widths else None
    h=['<table>']
    if widths:
        h.append("<colgroup>"+"".join(f'<col style="width:{w/tot*100:.2f}%">' for w in widths)+"</colgroup>")
    for ri,row in enumerate(rows):
        hdr = header and ri==0
        h.append("<thead><tr>" if hdr else "<tr>")
        for ci,val in enumerate(row):
            a=(align[ci] if align and ci<len(align) else "l")
            cls={"l":"al","r":"ar","c":"ac"}[a]
            body=_inline(val)
            if first_bold and ci==0 and not hdr: body=f"<strong>{body}</strong>"
            tag="th" if hdr else "td"
            h.append(f'<{tag} class="{cls}" style="font-size:{size}pt">{body}</{tag}>')
        h.append("</tr></thead>" if hdr else "</tr>")
    h.append("</table>")
    OUT.append("".join(h))

# stubs the content file touches but the PDF path does not need
def shade(*a, **k): pass
def borders(*a, **k): pass
def add_runs(*a, **k): pass
def add_page_numbers(): pass
class Pt(float):
    def __new__(cls, v): return float.__new__(cls, v)
class Inches(float):
    def __new__(cls, v): return float.__new__(cls, v)
class RGBColor:
    @staticmethod
    def from_string(s): return s
class WD_ALIGN_PARAGRAPH:
    LEFT="left"; CENTER="center"; RIGHT="right"; JUSTIFY="justify"

exec(open(os.path.join(ROOT,"tools","docx_content.py")).read())

# flush the raw doc.add_paragraph() calls used only by the cover
body=[]
for item in OUT:
    if isinstance(item, tuple) and item[0]=="PARA":
        p=item[1]; frag=[]
        for kind,txt,run in p.buf:
            sz=getattr(run,"size",None) or 9.5
            col=getattr(run,"color",None)
            col=getattr(col,"rgb",None) if col is not None and not isinstance(col,str) else col
            b="font-weight:700;" if getattr(run,"bold",False) else ""
            frag.append(f'<span style="font-size:{float(sz)}pt;{b}">{_html.escape(txt)}</span>')
        if frag: body.append("<p>"+"".join(frag)+"</p>")
    else:
        body.append(item)

CSS = """
@page { size:A4; margin:16mm 14mm 14mm; }
html{font-size:10pt}
body{margin:0;font-family:Charter,Georgia,serif;color:#101010;line-height:1.42;
     -webkit-font-smoothing:antialiased}
p{margin:0 0 5pt;text-align:justify;hyphens:auto;orphans:3;widows:3}
p.small{font-size:8pt}
strong{font-weight:700}
h1{font-family:"Helvetica Neue",sans-serif;font-size:13.5pt;font-weight:700;margin:16pt 0 5pt;
   padding-bottom:3pt;border-bottom:1.2pt solid #101010;break-after:avoid}
h2{font-family:"Helvetica Neue",sans-serif;font-size:10.5pt;font-weight:700;color:#C04A12;
   margin:11pt 0 3pt;break-after:avoid}
.exhibit{display:flex;align-items:baseline;gap:7pt;margin:13pt 0 4pt;padding-bottom:3pt;
   border-bottom:1.3pt solid #101010;break-after:avoid;break-inside:avoid}
.exno{font-family:"Helvetica Neue",sans-serif;font-size:7.4pt;font-weight:700;letter-spacing:.1em;
   text-transform:uppercase;color:#fff;background:#C04A12;padding:1.5pt 5pt;border-radius:1.5pt;white-space:nowrap}
.extitle{font-family:"Helvetica Neue",sans-serif;font-size:10pt;font-weight:700}
p.source{font-size:7.5pt;color:#6B6A63;font-style:italic;margin:-1pt 0 10pt;text-align:left}
.callout{margin:10pt 0 12pt;padding:9pt 12pt;background:#F6F5F2;border-left:2.6pt solid #C04A12;
   font-size:10pt;line-height:1.36;break-inside:avoid}
table{width:100%;border-collapse:collapse;margin:3pt 0 11pt;
  font-family:"Helvetica Neue",sans-serif;line-height:1.28;table-layout:fixed}
thead{display:table-header-group}
tr{break-inside:avoid}
th{text-align:left;font-weight:700;letter-spacing:.02em;color:#3D3C38;padding:3.6pt 5pt;
   border-top:1pt solid #101010;border-bottom:.6pt solid #B9B7B0;background:#F6F5F2;vertical-align:bottom}
td{padding:3pt 5pt;border-bottom:.4pt solid #DEDCD6;vertical-align:top;word-wrap:break-word}
tbody tr:last-child td{border-bottom:1pt solid #101010}
.ar{text-align:right;font-variant-numeric:tabular-nums}
.ac{text-align:center}
figure{margin:4pt 0 6pt;text-align:center;break-inside:avoid}
figure img{max-width:100%;height:auto}
.pb{break-after:page}
hr{break-inside:avoid}
"""
doc_html=(f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
          f'<title>CONTESTED</title><style>{CSS}</style></head><body>'
          + "\n".join(body) + "</body></html>")
open(HTML_OUT,"w",encoding="utf-8").write(doc_html)

if os.path.exists(CHROME):
    subprocess.run([CHROME,"--headless","--disable-gpu","--no-pdf-header-footer",
                    "--run-all-compositor-stages-before-draw","--virtual-time-budget=20000",
                    f"--print-to-pdf={PDF_OUT}","file://"+HTML_OUT],
                   check=True, capture_output=True)
    print(f"wrote {PDF_OUT}  ({os.path.getsize(PDF_OUT)/1024:.0f} KB)")
else:
    print(f"wrote {HTML_OUT}; Chrome not found")
