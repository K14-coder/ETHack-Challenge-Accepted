#!/usr/bin/env python3
"""build_pptx.py - the 3 minute pitch deck. Five content slides plus a demo card."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(ROOT, "figs")
OUT  = os.path.join(ROOT, "CONTESTED_pitch.pptx")

INK  = RGBColor(0x10,0x10,0x10)
INK2 = RGBColor(0x3D,0x3C,0x38)
INK3 = RGBColor(0x6B,0x6A,0x63)
ACC  = RGBColor(0xC0,0x4A,0x12)
BG   = RGBColor(0xFC,0xFC,0xFB)
PANEL= RGBColor(0xF2,0xF1,0xED)
WHITE= RGBColor(0xFF,0xFF,0xFF)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = 13.333, 7.5

def slide(bg=BG):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    r = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    r.fill.solid(); r.fill.fore_color.rgb = bg; r.line.fill.background()
    r.shadow.inherit = False
    return s

def box(s, x, y, w, h, fill=None, line=None, lw=1.5):
    sh = s.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb = fill
    else: sh.fill.background()
    if line: sh.line.color.rgb = line; sh.line.width = Pt(lw)
    else: sh.line.fill.background()
    sh.shadow.inherit = False
    return sh

def text(s, x, y, w, h, runs, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT,
         space=6, anchor=MSO_ANCHOR.TOP, line_spacing=1.0):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    if isinstance(runs, str): runs = [runs]
    for i, item in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(space); p.line_spacing = line_spacing
        parts = item if isinstance(item, list) else [(item, {})]
        for t, o in parts:
            r = p.add_run(); r.text = t
            r.font.size = Pt(o.get("size", size)); r.font.bold = o.get("bold", bold)
            r.font.color.rgb = o.get("color", color); r.font.name = "Calibri"
    return tb

def rule(s, x, y, w, color=INK, pt=3):
    ln = s.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Pt(pt))
    ln.fill.solid(); ln.fill.fore_color.rgb = color; ln.line.fill.background()
    ln.shadow.inherit = False

def pic(s, name, x, y, w):
    s.shapes.add_picture(os.path.join(FIGS, name), Inches(x), Inches(y), width=Inches(w))

def kicker(s, txt):
    text(s, 0.85, 0.5, 11, 0.4, [[(txt, {"size":13, "bold":True, "color":ACC})]])

def foot(s, txt):
    text(s, 0.85, 6.85, 11.6, 0.4, [[(txt, {"size":11, "color":INK3})]])

# ───────────────────────────── 1 · TITLE ─────────────────────────────
s = slide()
rule(s, 0.85, 1.5, 11.6, INK, 4)
text(s, 0.85, 1.75, 11.6, 1.3, [[("CONTESTED", {"size":66, "bold":True})]])
text(s, 0.85, 3.05, 11.6, 0.8,
     [[("Every ESG score is one answer to a question nobody wrote down.", {"size":26, "color":INK2})]])
text(s, 0.85, 3.75, 11.6, 0.8,
     [[("We publish the question, the answer, and how much the answer depends on the question.",
        {"size":26, "color":ACC, "bold":True})]])
rule(s, 0.85, 4.9, 11.6, INK, 2)
text(s, 0.85, 5.15, 11.6, 0.9,
     [[("18 S&P 500 Energy companies  ·  138 indicators  ·  17,496 defensible scores each  ·  live tool",
        {"size":17, "color":INK3})]])
foot(s, "ETHack 2026 · Challenge #1 · Citadel & Citadel Securities")

# ───────────────────────────── 2 · PROBLEM ────────────────────────────
s = slide()
kicker(s, "THE PROBLEM")
text(s, 0.85, 1.0, 11.6, 1.0,
     [[("The market buys a point estimate of a quantity", {"size":38, "bold":True})],
      [("that has no point estimate.", {"size":38, "bold":True, "color":ACC})]], space=2)

for i,(num,lab,col) in enumerate([("0.99","credit ratings agree",INK2),
                                  ("0.61","ESG ratings agree",ACC),
                                  ("6%","of the gap is pillar weights",INK2)]):
    x = 0.85 + i*3.95
    box(s, x, 2.7, 3.55, 1.85, PANEL)
    text(s, x+0.3, 2.95, 3.0, 0.8, [[(num, {"size":52, "bold":True, "color":col})]])
    text(s, x+0.3, 3.85, 3.0, 0.6, [[(lab, {"size":15, "color":INK2})]])

text(s, 0.85, 4.95, 11.6, 1.4,
     [[("Providers compute a distribution over method choices, publish one draw, and throw the rest away. ",{"size":20,"color":INK2}),
       ("The thrown-away part is the part an allocator needs.",{"size":20,"bold":True})]], line_spacing=1.25)
foot(s, "Berg, Kölbel & Rigobon, Review of Finance 2022. Divergence: measurement 56%, scope 38%, weights 6%.")

# ───────────────────────────── 3 · METHOD ─────────────────────────────
s = slide()
kicker(s, "WHAT WE BUILT")
text(s, 0.85, 0.95, 11.6, 0.75,
     [[("We read MSCI's and Bloomberg's methodologies and found ", {"size":29}),
       ("13 places a rater must choose.", {"size":29, "bold":True})]])
text(s, 0.85, 1.65, 11.6, 0.55,
     [[("They differ at seven. We vary those, fix the rest, and declare every assumption.", {"size":19, "color":INK2})]])

for i,(t,b) in enumerate([("Exposure base","EBITDA · equity · output"),
                          ("Normaliser","percentile · winsorised · log · elasticity"),
                          ("Evidence bar","permissive · majority · strict"),
                          ("Missing data","excluded · worst case · capped"),
                          ("Aggregation","arithmetic · power · geometric"),
                          ("Pillar weights","user slider, five presets")]):
    x = 0.85 + (i%3)*3.95; y = 2.45 + (i//3)*1.12
    box(s, x, y, 3.55, 0.95, PANEL)
    text(s, x+0.22, y+0.13, 3.2, 0.35, [[(t, {"size":15, "bold":True})]])
    text(s, x+0.22, y+0.5, 3.2, 0.35, [[(b, {"size":12, "color":INK3})]])

box(s, 0.85, 4.9, 11.6, 1.0, None, ACC, 2.5)
text(s, 1.15, 5.1, 11.0, 0.7,
     [[("Then the correction that mattered: ", {"size":19}),
       ("“best today” and “improving fastest” are different questions.", {"size":19, "bold":True}),
       (" We score them separately.", {"size":19})]])
foot(s, "Specification curve analysis, Simonsohn, Simmons & Nelson, Nature Human Behaviour 2020.")

# ───────────────────────────── 4 · RESULT ─────────────────────────────
s = slide()
kicker(s, "THE RESULT")
text(s, 0.85, 0.95, 6.2, 2.6,
     [[("33", {"size":92, "bold":True, "color":ACC})],
      [("of 153 pairwise comparisons survive", {"size":22, "bold":True})],
      [("every defensible method.", {"size":22, "bold":True})],
      [("A published league table asserts all 153.", {"size":17, "color":INK2})]], space=3)
text(s, 0.85, 3.9, 6.2, 2.4,
     [[("The median company still moves ", {"size":19, "color":INK2}),
       ("3 places of 18", {"size":19, "bold":True, "color":ACC}),
       (" on method choice alone, after we hold the question and the peer group fixed.",
        {"size":19, "color":INK2})],
      [("Two axes decide it: what you ask, and who you ask it against. Neither is a weight.",
        {"size":17, "color":INK3})]], line_spacing=1.2, space=10)
pic(s, "f3_variance.png", 7.35, 1.15, 5.3)
text(s, 7.35, 5.35, 5.3, 0.4, [[("Share of a company's rank variance, by choice", {"size":12, "color":INK3})]])
foot(s, "Full grid runs in 18 seconds. Every figure regenerates from the committed pipeline.")

# ───────────────────────────── 5 · DEMO ───────────────────────────────
s = slide(INK)
text(s, 0.85, 2.4, 11.6, 1.2, [[("LIVE", {"size":22, "bold":True, "color":ACC})]])
text(s, 0.85, 2.9, 11.6, 1.6,
     [[("Move a slider. Watch the ranking change.", {"size":52, "bold":True, "color":WHITE})]])
text(s, 0.85, 4.5, 11.6, 1.0,
     [[("17,496 specifications, recomputed in the browser, in real time.",
        {"size":22, "color":RGBColor(0xB8,0xB7,0xB1)})]])

# ───────────────────────────── 6 · BONUS + CLOSE ──────────────────────
s = slide()
kicker(s, "BONUS · $1BN UNDER A NET-ZERO COMMITMENT")
text(s, 0.85, 0.95, 11.6, 0.8,
     [[("Buy the companies the market ", {"size":31}),
       ("cannot yet classify.", {"size":31, "bold":True, "color":ACC})]])
text(s, 0.85, 1.7, 11.6, 0.6,
     [[("We tested the “ESG threshold unlocks capital” thesis on our own data. There is no threshold.",
        {"size":18, "color":INK2})]])
pic(s, "f4_eligibility.png", 0.85, 2.3, 5.9)
box(s, 7.15, 2.3, 5.3, 3.5, PANEL)
text(s, 7.45, 2.55, 4.8, 3.1,
     [[("15 of 18", {"size":34, "bold":True, "color":ACC})],
      [("companies sit between 20% and 80% likely to pass a top-half screen.",
        {"size":15, "color":INK2})],
      [("So the tradeable number is not crossing a line. It is the gap between where a company ",
        {"size":15, "color":INK2}),
       ("stands", {"size":15, "bold":True}), (" and where it is ", {"size":15, "color":INK2}),
       ("heading", {"size":15, "bold":True}), (".", {"size":15, "color":INK2})],
      [("MPC +0.61   OXY +0.41   PSX +0.28", {"size":15, "bold":True, "color":ACC})],
      [("Long the gap, short the structurally stuck, exit into eligibility.",
        {"size":14, "color":INK3})]], space=9, line_spacing=1.12)
rule(s, 0.85, 6.15, 11.6, INK, 2)
text(s, 0.85, 6.4, 11.6, 0.6,
     [[("We deliver the ranking the brief asked for, and the honest error bar around it.",
        {"size":19, "bold":True})]])

prs.save(OUT)
print(f"wrote {OUT}  ({os.path.getsize(OUT)/1024:.0f} KB, {len(prs.slides.__iter__.__self__._sldIdLst)} slides)")
