#!/usr/bin/env python3
"""build_pptx.py - the 3 minute pitch. Four beats, 177 seconds, speaker notes."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(ROOT, "figs")
OUT  = os.path.join(ROOT, "CONTESTED_pitch.pptx")

INK  = RGBColor(0x10,0x10,0x10); INK2 = RGBColor(0x3D,0x3C,0x38)
INK3 = RGBColor(0x6B,0x6A,0x63); ACC  = RGBColor(0xC0,0x4A,0x12)
BG   = RGBColor(0xFC,0xFC,0xFB); PANEL= RGBColor(0xF2,0xF1,0xED)
WHITE= RGBColor(0xFF,0xFF,0xFF); DIM  = RGBColor(0xB8,0xB7,0xB1)
BLUE = RGBColor(0x2A,0x78,0xD6)

prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

def slide(bg=BG):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    r = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    r.fill.solid(); r.fill.fore_color.rgb = bg; r.line.fill.background(); r.shadow.inherit=False
    return s

def box(s,x,y,w,h,fill=None,line=None,lw=1.5):
    sh=s.shapes.add_shape(1,Inches(x),Inches(y),Inches(w),Inches(h))
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb=fill
    else: sh.fill.background()
    if line: sh.line.color.rgb=line; sh.line.width=Pt(lw)
    else: sh.line.fill.background()
    sh.shadow.inherit=False; return sh

def text(s,x,y,w,h,runs,size=18,color=INK,bold=False,align=PP_ALIGN.LEFT,
         space=6,anchor=MSO_ANCHOR.TOP,ls=1.0):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
    if isinstance(runs,str): runs=[runs]
    for i,item in enumerate(runs):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.space_after=Pt(space); p.line_spacing=ls
        for t,o in (item if isinstance(item,list) else [(item,{})]):
            r=p.add_run(); r.text=t
            r.font.size=Pt(o.get("size",size)); r.font.bold=o.get("bold",bold)
            r.font.color.rgb=o.get("color",color); r.font.name="Calibri"
    return tb

def rule(s,x,y,w,color=INK,pt=3):
    ln=s.shapes.add_shape(1,Inches(x),Inches(y),Inches(w),Pt(pt))
    ln.fill.solid(); ln.fill.fore_color.rgb=color; ln.line.fill.background(); ln.shadow.inherit=False

def pic(s,name,x,y,w): s.shapes.add_picture(os.path.join(FIGS,name),Inches(x),Inches(y),width=Inches(w))
def kicker(s,t,color=ACC): text(s,0.85,0.45,11.6,0.4,[[(t,{"size":13,"bold":True,"color":color})]])
def notes(s,t): s.notes_slide.notes_text_frame.text = t

# ══════════════════ 1 · HOOK · 30 to 35 seconds ══════════════════
s = slide()
kicker(s, "MARATHON PETROLEUM  ·  SAME DATA  ·  SAME YEAR")
text(s,0.85,1.15,11.6,0.9,[[("One company. Two defensible methods.",{"size":34,"color":INK2})]])

box(s,0.85,2.25,5.5,2.9,PANEL)
text(s,1.2,2.55,4.8,2.4,[[("15",{"size":128,"bold":True,"color":INK})],
    [("th of 18",{"size":28,"color":INK2})],
    [("on how clean it is today",{"size":17,"color":INK3})]],space=0,ls=0.85)
box(s,6.95,2.25,5.5,2.9,PANEL)
text(s,7.3,2.55,4.8,2.4,[[("6",{"size":128,"bold":True,"color":ACC})],
    [("th of 18",{"size":28,"color":ACC})],
    [("on how fast it is improving",{"size":17,"color":INK3})]],space=0,ls=0.85)

rule(s,0.85,5.5,11.6,INK,3)
text(s,0.85,5.75,11.6,1.1,
     [[("Nine places apart. Neither number is a mistake.",{"size":30,"bold":True})],
      [("An ESG score is one answer to a question nobody wrote down.",{"size":24,"color":ACC,"bold":True})]],space=4)
notes(s,"""HOOK  |  32 sec  |  78 spoken words  |  slow, this is the whole pitch

SAY:
"Marathon Petroleum. Fifteenth of eighteen energy companies on how clean it is
today. Sixth of eighteen on how fast it is improving.

Same company. Same data. Same year.

[PAUSE ONE BEAT]

Neither number is wrong. They answer two different questions, and the rating
industry publishes one of them without telling you which.

That is what an ESG score is. One answer to a question nobody wrote down.
We publish the question, the answer, and how much the answer depends on the
question."

DO NOT say methodology, specification or grid on this slide.""")

# ══════════════════ 2 · DEFINITION + STUDY + COMPANIES · 40s ══════════════════
s = slide()
kicker(s,"WHAT WE MEASURE, AND WHY THE INDUSTRY DISAGREES")
box(s,0.85,1.0,5.6,2.35,PANEL)
text(s,1.15,1.22,5.0,2.0,
     [[("Our definition",{"size":13,"bold":True,"color":ACC})],
      [("Less irreversible harm per unit of output than the peers making the same product, ",{"size":17,"color":INK}),
       ("and a balance sheet that survives the transition.",{"size":17,"bold":True})]],space=6,ls=1.1)

box(s,0.85,3.55,5.6,2.9,None,INK,1.5)
text(s,1.15,3.75,5.0,0.4,[[("Why ratings disagree",{"size":13,"bold":True,"color":ACC})]])
for i,(pct,lab,col) in enumerate([("56%","measurement  ·  same thing, measured differently",INK),
                                  ("38%","scope  ·  what counts at all",INK),
                                  ("6%","weights  ·  the slider everyone argues about",INK3)]):
    text(s,1.15,4.25+i*0.62,5.0,0.55,
         [[(pct,{"size":26,"bold":True,"color":ACC if i<2 else INK3}),("   "+lab,{"size":13,"color":col})]],space=0)
text(s,1.15,6.05,5.0,0.35,[[("Berg, Kolbel & Rigobon, Review of Finance 2022",{"size":10,"color":INK3})]])

pic(s,"f1_two_questions.png",6.75,1.05,6.0)
text(s,6.75,5.5,6.0,0.9,
     [[("All 18 companies, both specification curves.",{"size":15,"bold":True})],
      [("Blue is where they stand. Orange is where they are heading. "
        "The bars are how far the answer moves on method choice alone.",{"size":13,"color":INK3})]],space=3,ls=1.1)
notes(s,"""DEFINITION + STUDY + COMPANIES  |  40 sec  |  103 spoken words

SAY:
"Our definition: less irreversible harm per unit of output than the peers making
the same product, and a balance sheet that survives the transition. Financial
resilience is in there because a company in distress cuts abatement first.

Why do raters disagree? Berg and co-authors decomposed it. Fifty-six percent is
measurement. Thirty-eight percent is scope. Only six percent is the pillar
weighting, which is the only part anyone lets you touch.

So we attack the ninety-four percent. Nine choices where MSCI and Bloomberg
publish different specifications, every combination.

Right: all eighteen companies, both questions. Bar length is how far the answer
moves on method alone."

LAND 56 / 38 / 6 CLEARLY. Paraphrase the definition, do not read it.""")

# ══════════════════ 3 · WHY ENERGY + WHAT TO WATCH · bridge ══════════════════
s = slide()
kicker(s,"WHY THE ENERGY SECTOR")
text(s,0.85,1.0,11.6,0.8,
     [[("The hardest place to score, so the best place to test.",{"size":30,"bold":True})]])
for i,(t,b) in enumerate([
    ("Only 3 of 37","environmental fields are reported by all 18 companies"),
    ("Scope 3 absent","from every field Bloomberg delivers for these peer groups"),
    ("FY2025 is 36%","complete for environmental data. The lag is structural"),
    ("18 seconds","to run all 17,496 specifications on a laptop")]):
    x=0.85+(i%2)*5.95; y=2.15+(i//2)*1.5
    box(s,x,y,5.55,1.25,PANEL)
    text(s,x+0.3,y+0.18,5.0,0.45,[[(t,{"size":22,"bold":True,"color":ACC})]])
    text(s,x+0.3,y+0.72,5.0,0.45,[[(b,{"size":14,"color":INK2})]])
box(s,0.85,5.4,11.6,1.15,None,ACC,2.5)
text(s,1.2,5.65,11.0,0.7,
     [[("If the framework survives here, it survives anywhere. ",{"size":20,"bold":True}),
       ("Now watch what happens when I change one convention.",{"size":20})]])
notes(s,"""BRIDGE  |  12 sec  |  32 spoken words  |  fast

SAY:
"Why energy? Hardest sector to score. Only three of thirty-seven environmental
fields are reported by all eighteen companies. Scope Three is absent entirely,
and we say so. Let me show you."

THEN SWITCH TO THE BROWSER IMMEDIATELY.""")

# ══════════════════ 4 · DEMO CARD ══════════════════
s = slide(INK)
text(s,0.85,2.2,11.6,0.7,[[("LIVE",{"size":20,"bold":True,"color":ACC})]])
text(s,0.85,2.75,11.6,1.8,
     [[("Move one switch.",{"size":56,"bold":True,"color":WHITE})],
      [("Watch the ranking change.",{"size":56,"bold":True,"color":WHITE})]],space=2)
text(s,0.85,5.0,11.6,0.8,
     [[("17,496 specifications, recomputed in the browser, in real time.",{"size":22,"color":DIM})]])
notes(s,"""DEMO  |  68 sec  |  170 spoken words  |  DO EXACTLY THIS

1 (8s) "Eighteen companies ranked. Consensus here. This bar is how much of that
   rank is a choice."

2 (15s) DRAG THE ENVIRONMENT SLIDER.
   "This is what every provider gives you. Pillar weights. It moves the median
   company three places. That is the six percent."

3 (20s) PIN Direction to LEVEL, then Evidence bar to STRICT.
   "Here is what nobody gives you. This is the question I am asking. And this is
   how demanding I am about evidence."

4 (15s) POINT AT THE SETTLED COUNTER.
   "Thirty-three of a hundred and fifty-three comparisons survive every method.
   Raise the bar, fifty-six. A league table asserts all hundred and fifty-three."

5 (10s) HOVER A POINT ON THE CURVE.
   "Every point tells you which nine choices produced it. No black box."

IF IT BREAKS: skip to the last slide, say "numbers are in the paper, tool is in
the repo". Never debug on stage.""")

# ══════════════════ 5 · BONUS · 25 to 30s ══════════════════
s = slide()
kicker(s,"BONUS  ·  ONE BILLION DOLLARS UNDER A NET-ZERO COMMITMENT")
text(s,0.85,0.95,11.6,0.75,
     [[("Buy the companies the market ",{"size":32}),("cannot yet classify.",{"size":32,"bold":True,"color":ACC})]])
pic(s,"f4_eligibility.png",0.85,1.85,5.85)
box(s,7.15,1.85,5.3,3.75,PANEL)
text(s,7.5,2.1,4.7,3.3,
     [[("15 of 18",{"size":40,"bold":True,"color":ACC})],
      [("companies are between 20% and 80% likely to pass a sustainable-fund screen.",{"size":15,"color":INK2})],
      [("There is no threshold to cross. So the trade is not crossing a line, it is the gap between where a company ",{"size":15,"color":INK2}),
       ("stands",{"size":15,"bold":True}),(" and where it is ",{"size":15,"color":INK2}),("heading",{"size":15,"bold":True}),(".",{"size":15,"color":INK2})],
      [("MPC +0.61    OXY +0.41    PSX +0.28",{"size":16,"bold":True,"color":ACC})]],space=10,ls=1.12)
rule(s,0.85,5.95,11.6,INK,3)
text(s,0.85,6.2,11.6,0.8,
     [[("We give you the ranking the brief asked for, ",{"size":22}),
       ("and the honest error bar around it.",{"size":22,"bold":True,"color":ACC})]])
notes(s,"""BONUS + CLOSE  |  28 sec  |  70 spoken words

SAY:
"The bonus. The thesis is that crossing an ESG threshold unlocks a wall of
capital. We tested it. There is no threshold: fifteen of eighteen companies sit
between twenty and eighty percent likely to pass a screen.

So the trade is the gap between where a company stands and where it is heading.
We go long the gap, short the structurally stuck, and sell when the gap closes.

We give you the ranking the brief asked for, and the honest error bar around it.
Thank you."

STOP AT THANK YOU.""")

prs.save(OUT)
n = len(prs.slides._sldIdLst)
print(f"wrote {OUT}  ({os.path.getsize(OUT)/1024:.0f} KB, {n} slides)")
