# ═══════════════════ APPENDIX ═══════════════════
# Backup slides. One slide, one question, one number. Never presented in the
# three minutes; flipped to during Q&A.

# divider, so an accidental arrow-press during the pitch lands somewhere safe
s = slide(INK)
text(s,0.85,3.0,11.6,0.7,[[("APPENDIX",{"size":18,"bold":True,"color":ACC})]])
text(s,0.85,3.5,11.6,1.2,[[("Backup. Not presented.",{"size":44,"bold":True,"color":WHITE})]])
text(s,0.85,4.9,11.6,0.6,
     [[("A1 value proposition · A2 the nine specifications · A3 data · A4 indicators · A5 results · "
        "A6 variance · A7 deflation · A8 settled pairs · A9 risks · A10 formula · A11 bonus · A12 reproducibility",
        {"size":14,"color":DIM})]],ls=1.3)


def acard(s, x, y, w, h, head, body, big=None):
    box(s, x, y, w, h, PANEL)
    if big:
        text(s, x+0.28, y+0.16, w-0.55, 0.62, [[(big, {"size":30, "bold":True, "color":ACC})]])
        yy = y+0.82
    else:
        yy = y+0.2
    text(s, x+0.28, yy, w-0.55, 0.4, [[(head, {"size":14, "bold":True})]])
    text(s, x+0.28, yy+0.42, w-0.55, h-(yy-y)-0.55, [[(body, {"size":12, "color":INK2})]], ls=1.15)

def atitle(s, n, t):
    text(s,0.85,0.42,11.6,0.5,[[(f"APPENDIX {n}",{"size":12,"bold":True,"color":ACC}),
                                ("     "+t,{"size":19,"bold":True})]])
    rule(s,0.85,0.95,11.6,INK,2)

# ── A1 · VALUE PROPOSITION ──────────────────────────────────────────
s = slide(); atitle(s,"A1","Value proposition: who benefits, and what they do differently")
text(s,0.85,1.15,11.6,0.5,
     [[("We do not replace a rating. We tell you which parts of it you can act on.",
        {"size":20,"color":INK2})]])
rows=[("Asset allocator",
       "Gets the consensus rank, the number a provider already sells, plus the 33 of 153 comparisons that hold under every specification.",
       "Stops making 120 relative calls the evidence cannot support."),
      ("Engagement team",
       "The remedy column names the single missing disclosure that would most reduce a company's contestation.",
       "Walks into a meeting with one specific ask instead of a generic score complaint."),
      ("Regulator or standard setter",
       "Quantifies how much of a rating is convention rather than performance, per axis.",
       "Targets the disclosure rule at the convention that actually moves rankings."),
      ("Rating provider",
       "A quality-assurance lens on their own product: where is our published score fragile?",
       "Knows which issuers to re-review before publication."),
      ("The company being rated",
       "Sees which of its own silences costs it the most rank.",
       "Discloses the field that changes its classification, not the cheapest one.")]
y=1.85
for who,gets,does in rows:
    box(s,0.85,y,11.6,0.92,PANEL)
    text(s,1.1,y+0.13,2.5,0.6,[[(who,{"size":13,"bold":True,"color":ACC})]])
    text(s,3.75,y+0.1,4.6,0.75,[[(gets,{"size":10.5,"color":INK2})]],ls=1.1)
    text(s,8.55,y+0.1,3.7,0.75,[[(does,{"size":10.5,"bold":True})]],ls=1.1)
    y+=1.03
text(s,0.85,7.0,11.6,0.4,
     [[("Anyone who wants one number takes the consensus and ignores the rest. Nothing is lost by adding the error bar.",
        {"size":12,"color":INK3})]])

# ── A2 · THE NINE SPECIFICATIONS (THE DEMO CONTROLS) ────────────────
s = slide(); atitle(s,"A2","The nine specifications: every control in the demo")
text(s,0.85,1.1,11.6,0.4,
     [[("Each is a fork where MSCI and Bloomberg publish different choices, or one this data forces. "
        "3 × 3 × 2 × 3 × 4 × 3 × 3 × 3 × 3 = 17,496.",{"size":12,"color":INK2})]])
hdr=["Control","Options in the tool","Where it comes from"]
rows=[("Exposure base","EBITDA · equity · output","Bloomberg activity metrics. Output exists for the 9 producers only"),
      ("Window","latest · fiscal year · 3-year mean","Bloomberg ships Latest and Fiscal Year as separate products"),
      ("Direction","level · change","Curve A against Curve B. The two are scored separately"),
      ("Polarity","orthodox · neutral · stability","15 fields where the two governance conventions disagree"),
      ("Normaliser","percentile · winsorised · log min-max · elasticity","MSCI uses percentile bands. Bloomberg rejects them and fits a log-log residual"),
      ("Peer set","BECS group · producers · all 18","MSCI uses GICS sub-industry, Bloomberg built BECS"),
      ("Evidence bar","permissive · majority · strict","Forced by this data. At strict, Social has no fields left"),
      ("Missing data","excluded · worst case · capped","Bloomberg's sub-issue rule and its Issue Score cap"),
      ("Aggregation","arithmetic · power p=½ · geometric","MSCI's weighted mean against Bloomberg's power mean"),
      ("Pillar weights","4 sliders, 5 presets","Not a grid axis. Handed to the user, and worth 3.0 places")]
y=1.62; box(s,0.85,y,11.6,0.36,INK)
for i,h in enumerate(hdr):
    text(s,[1.1,3.6,7.15][i],y+0.06,[2.4,3.4,5.2][i],0.3,[[(h,{"size":11,"bold":True,"color":WHITE})]])
y+=0.4
for i,(a,b,c) in enumerate(rows):
    if i%2==0: box(s,0.85,y,11.6,0.5,PANEL)
    col = INK3 if a=="Pillar weights" else ACC
    text(s,1.1,y+0.1,2.4,0.35,[[(a,{"size":11.5,"bold":True,"color":col})]])
    text(s,3.6,y+0.1,3.4,0.35,[[(b,{"size":11,"color":INK})]])
    text(s,7.15,y+0.1,5.2,0.35,[[(c,{"size":10,"color":INK2})]])
    y+=0.5

# ── A3 · THE UNIVERSE AND THE DATA ──────────────────────────────────
s = slide(); atitle(s,"A3","Universe, data and coverage")
acard(s,0.85,1.2,3.7,1.5,"companies","18 of the 21 S&P 500 energy constituents at 12 Sep 2026. APA, TPL, EQT and ONEOK have no export.","18")
acard(s,4.8,1.2,3.7,1.5,"fields","E 37 · S 14 · G 78 · F 9. One registry field, DX831, is reported by nobody and excluded.","138")
acard(s,8.75,1.2,3.7,1.5,"specifications","606 distinct grade paths of 648. Kish effective N 574.","17,496")
label_rows=[["Pillar","Fields","FY21","FY22","FY23","FY24","FY25"],
 ["Environment","37","59%","59%","60%","61%","36%"],
 ["Social","14","65%","65%","65%","66%","39%"],
 ["Governance","78","97%","97%","97%","97%","92%"],
 ["Financial","9","94%","94%","94%","94%","94%"]]
y=3.05; text(s,0.85,y,11.6,0.35,[[("Share of cells filled, by pillar and fiscal year",{"size":13,"bold":True})]]); y+=0.42
for ri,row in enumerate(label_rows):
    if ri==0: box(s,0.85,y,11.6,0.36,INK)
    elif ri%2==0: box(s,0.85,y,11.6,0.36,PANEL)
    for ci,v in enumerate(row):
        c = WHITE if ri==0 else (ACC if (ri<3 and ci==6) else INK)
        text(s,1.1+ci*1.62,y+0.06,1.5,0.3,[[(v,{"size":11.5,"bold":ri==0 or (ri<3 and ci==6),"color":c})]])
    y+=0.38
text(s,0.85,5.35,11.6,0.9,
     [[("FY2025 is 36% complete for environmental data because sustainability reporting runs a year behind. "
        "That lag is why the window control has three settings and not two.",{"size":12,"color":INK2})]],ls=1.2)
box(s,0.85,6.05,11.6,0.95,None,ACC,2)
text(s,1.15,6.25,11.0,0.6,
     [[("Only 3 environmental and 1 social field are reported by all 18 companies. ",{"size":14,"bold":True}),
       ("Sector-wide comparability leaves four fields, all policy flags.",{"size":14})]])

# ── A4 · INDICATORS NAMED ───────────────────────────────────────────
s = slide(); atitle(s,"A4","The environmental indicators, named")
rows=[("F0947","Scope 1 GHG / CO2 emissions","15/18"),("SA162","Air pollution reduction policy","18/18"),
      ("SA558","Claims science-based target","18/18"),("SA559","Claims net-zero target","18/18"),
      ("ES007 / F0949 / ES009","NOx · SOx · VOC emissions","14 / 13 / 14"),
      ("SA055","Percent methane of Scope 1","12/18"),("SA020","Freshwater withdrawals","12/18"),
      ("ES249 / SA048","Hydrocarbon spills, volume and count","11/18"),
      ("F1284","Embedded carbon in reserves","9/18"),("ES027","Gas flaring","9/18"),
      ("SA084 / SA085","Internal carbon price · Arctic drilling","9/18"),
      ("ES019 / SA016 / SA023","Hazardous waste: total, share, recycled","7 / 5 / 4"),
      ("ES077 / ES255","Scope 2, location and market based","2/18")]
y=1.25
for i,(a,b,c) in enumerate(rows):
    if i%2==0: box(s,0.85,y,7.6,0.4,PANEL)
    text(s,1.05,y+0.07,2.1,0.3,[[(a,{"size":10.5,"bold":True,"color":ACC})]])
    text(s,3.25,y+0.07,4.0,0.3,[[(b,{"size":11,"color":INK})]])
    text(s,7.4,y+0.07,0.95,0.3,[[(c,{"size":10.5,"color":INK2})]])
    y+=0.42
box(s,8.9,1.25,3.55,2.4,None,ACC,2.5)
text(s,9.2,1.5,3.0,2.0,
     [[("Scope 3",{"size":26,"bold":True,"color":ACC})],
      [("is absent from all 138 fields.",{"size":14,"bold":True})],
      [("Bloomberg's ES map for these peer groups does not carry it. It is the largest gap in this framework for oil and gas, and we say so on page 5.",{"size":11,"color":INK2})]],space=6,ls=1.15)
acard(s,8.9,3.85,3.55,1.5,"Methane is present","SA055, percent of Scope 1, reported by 12 of 18.","SA055")
acard(s,8.9,5.5,3.55,1.35,"37 environmental fields","The 15 not listed here are policy booleans. Full registry in the repo.","37")

# ── A5 · FULL RESULTS ───────────────────────────────────────────────
s = slide(); atitle(s,"A5","All 18 companies, Curve A, equal weights")
res=[("BKR","Services",82,6.0,78),("EXE","E&P",82,6.0,91),("CTRA","E&P",76,7.0,81),
     ("VLO","Refining",71,5.0,77),("EOG","E&P",71,10.0,90),("SLB","Services",65,7.0,78),
     ("COP","E&P",53,6.0,93),("OXY","E&P",47,10.0,92),("XOM","Integrated",47,6.0,99),
     ("MPC","Refining",41,9.0,79),("PSX","Refining",41,8.0,77),("TRGP","Midstream",41,9.0,74),
     ("WMB","Midstream",41,11.0,75),("KMI","Midstream",41,7.0,76),("DVN","E&P",35,6.0,89),
     ("CVX","Integrated",35,6.0,97),("HAL","Services",18,7.0,78),("FANG","E&P",18,4.0,91)]
for col,xoff in [(res[:9],0.85),(res[9:],6.95)]:
    y=1.25; box(s,xoff,y,5.5,0.34,INK)
    for i,h in enumerate(["#","Ticker","Group","Cons.","Places","Cov."]):
        text(s,xoff+0.15+i*[0,0.45,1.5,3.0,3.9,4.8][min(i,5)]*0 + xoff*0 + [xoff+0.15,xoff+0.5,xoff+1.5,xoff+3.05,xoff+3.85,xoff+4.75][i],
             y+0.05,0.9,0.28,[[(h,{"size":10,"bold":True,"color":WHITE})]])
    y+=0.38
    start = 1 if xoff<3 else 10
    for k,(t,g,c,p,cv) in enumerate(col):
        if k%2==0: box(s,xoff,y,5.5,0.36,PANEL)
        for i,(v,b) in enumerate([(str(start+k),False),(t,True),(g,False),(f"{c}",True),(f"{p:.1f}",False),(f"{cv}%",False)]):
            text(s,[xoff+0.15,xoff+0.5,xoff+1.5,xoff+3.05,xoff+3.85,xoff+4.75][i],y+0.06,0.95,0.3,
                 [[(v,{"size":10.5,"bold":b,"color":ACC if i==4 and p>=9 else INK})]])
        y+=0.36
text(s,0.85,6.9,11.6,0.5,
     [[("Consensus is the median rank percentile. Places is the interquartile width in rank positions out of 18. "
        "Full audit trail, one row per company per specification, is in the repo.",{"size":11,"color":INK3})]])

# ── A6 · VARIANCE ───────────────────────────────────────────────────
s = slide(); atitle(s,"A6","Where the disagreement lives")
pic(s,"f3_variance.png",0.85,1.25,7.2)
box(s,8.4,1.25,4.05,4.6,PANEL)
text(s,8.7,1.5,3.5,4.1,
     [[("Main effects 47.8%",{"size":18,"bold":True,"color":ACC})],
      [("Interaction 52.2%",{"size":18,"bold":True,"color":INK})],
      [("More than half the variance is choices that only matter in combination. "
        "That is why we do not publish a single 'decided by' axis per company: "
        "it would be a one-at-a-time reading of a grid that is not one-at-a-time.",{"size":12,"color":INK2})],
      [("Two negative results, reported deliberately: the aggregation function is worth 0.3% and the polarity convention 0.5%. "
        "We implemented both so we could measure them rather than assume them.",{"size":12,"color":INK2})]],space=10,ls=1.15)
text(s,0.85,6.05,7.2,0.7,
     [[("The two that matter, direction and peer set, are scope choices: what you ask and who you ask it against. Neither is a weight.",
        {"size":13,"bold":True})]],ls=1.15)

# ── A7 · DEFLATION LADDER ───────────────────────────────────────────
s = slide(); atitle(s,"A7","Contestation survives every deflation")
rows=[["Stratum","Cells","Places of 18"],
 ["Both curves pooled (we do not report this)","17,496","7.0"],
 ["Curve A only (level)","8,748","5.0"],
 ["Curve A × majority evidence bar","2,916","6.0"],
 ["Curve A × majority × no worst-case","1,944","5.5"],
 ["Curve A × majority × sector peers","972","4.0"],
 ["Curve A × majority × no worst-case × sector","648","3.6"],
 ["Curve A × BECS peer groups","2,916","3.0"],
 ["Random-rank control","","8.5 to 9.0"]]
y=1.3
for ri,row in enumerate(rows):
    if ri==0: box(s,0.85,y,11.6,0.4,INK)
    elif ri==len(rows)-1: box(s,0.85,y,11.6,0.44,PANEL)
    elif ri%2==0: box(s,0.85,y,11.6,0.44,PANEL)
    for ci,v in enumerate(row):
        c=WHITE if ri==0 else (INK3 if ri==len(rows)-1 else (ACC if ci==2 and ri in (7,) else INK))
        text(s,[1.15,8.3,10.3][ci],y+(0.07 if ri==0 else 0.1),[6.9,1.7,2.0][ci],0.32,
             [[(v,{"size":12,"bold":ri==0 or (ci==2 and ri==7),"color":c})]],
             align=PP_ALIGN.RIGHT if ci>0 else PP_ALIGN.LEFT)
    y+=0.4 if ri==0 else 0.44
box(s,0.85,5.6,11.6,1.25,None,ACC,2.5)
text(s,1.2,5.85,11.0,0.8,
     [[("A randomly ordered company would show 8.5 to 9.0 places. ",{"size":15}),
       ("Pooled we would read 7.0, barely below noise, which is why we do not pool. Curve A at 3.0 is well inside the control.",
        {"size":15,"bold":True})]],ls=1.15)

# ── A8 · SETTLED PAIRS ──────────────────────────────────────────────
s = slide(); atitle(s,"A8","What is settled, and how it depends on the threshold")
rows=[["Threshold","Settled pairs","of 153","Share"],
 ["P > 0.999","7","153","5%"],["P > 0.99","12","153","8%"],
 ["P > 0.95  (our headline)","33","153","22%"],["P > 0.90","51","153","33%"],
 ["P > 0.85","68","153","44%"],["P > 0.80","79","153","52%"]]
y=1.3
for ri,row in enumerate(rows):
    if ri==0: box(s,0.85,y,7.4,0.4,INK)
    elif ri==3: box(s,0.85,y,7.4,0.46,PANEL)
    for ci,v in enumerate(row):
        c=WHITE if ri==0 else (ACC if ri==3 else INK)
        text(s,[1.15,4.2,5.9,7.1][ci],y+0.09,1.8,0.32,[[(v,{"size":12,"bold":ri in (0,3),"color":c})]])
    y+=0.4 if ri==0 else 0.46
box(s,8.6,1.3,3.85,3.1,PANEL)
text(s,8.9,1.55,3.3,2.6,
     [[("Monotone, no cliff",{"size":16,"bold":True,"color":ACC})],
      [("The count rises smoothly with the threshold, so our 95% cut-off is not sitting on a discontinuity.",{"size":12,"color":INK2})],
      [("Note that rank percentile assigns 0 and 100 in every specification by construction, so extreme ranks are structural, not a rare tail.",{"size":12,"color":INK2})]],space=8,ls=1.15)
box(s,0.85,4.85,11.6,1.0,None,ACC,2.5)
text(s,1.2,5.1,11.0,0.6,
     [[("At Curve A × strict evidence bar, 56 of 153 settle. ",{"size":15,"bold":True}),
       ("But at that setting Environment has 2 fields and Social none, so it is largely a governance and credit ranking. We label it as such.",{"size":15})]],ls=1.15)

# ── A9 · RISK REGISTER ──────────────────────────────────────────────
s = slide(); atitle(s,"A9","Risk register: four closed by rerunning the pipeline")
rows=[("CLOSED","Denominator is EBITDA, not revenue","Reran the full grid on SEC XBRL revenue, 16 of 18. Median shift 0.0 places, max 1.0."),
      ("CLOSED","17,496 cells are not independent","648 grade paths to 606 distinct. Kish effective N 574, a 6.5% inflation."),
      ("CLOSED","Reserves double-counted as harm and resilience","Dropped reserve life. Median shift 0.0 places, only OXY moves by 1.0."),
      ("CLOSED","Settled count depends on the 95% cut-off","7 pairs at 0.999 rising monotonically to 79 at 0.80. No cliff."),
      ("BOUNDED","Contestation is partly thin data","Coverage against contestation −0.38. Not monotone in group size."),
      ("BOUNDED","N = 18 quantises every statistic","5.88 points per rank place. All headlines quoted in places."),
      ("BOUNDED","Governance dominates by field count","78 of 138. The contestation we measure is mostly E and S."),
      ("OPEN","Not benchmarked against a published rating","Never placed Bloomberg's own score inside our distribution. First on the roadmap."),
      ("OPEN","Scope 3, controversies, transition capex absent","Scope 3 not in the export, controversies a declared boundary.")]
y=1.25
for st,risk,test in rows:
    col={"CLOSED":ACC,"BOUNDED":INK2,"OPEN":INK3}[st]
    box(s,0.85,y,11.6,0.6,PANEL if st=="CLOSED" else None)
    text(s,1.05,y+0.16,1.15,0.3,[[(st,{"size":10,"bold":True,"color":col})]])
    text(s,2.3,y+0.14,3.9,0.35,[[(risk,{"size":11.5,"bold":True})]])
    text(s,6.35,y+0.14,5.9,0.35,[[(test,{"size":10.5,"color":INK2})]])
    y+=0.63
text(s,0.85,7.0,11.6,0.4,
     [[("Every CLOSED row was tested by rerunning the pipeline, not settled by argument.",{"size":12,"color":INK3})]])

# ── A10 · FORMULA ───────────────────────────────────────────────────
s = slide(); atitle(s,"A10","The formula, eight steps")
steps=[("1","exposure","divide by the base for a quantity, select the published variant for a rate"),
 ("2","window","latest reported · fixed FY2024 · mean of the last three reported"),
 ("3","direction","level, or relative change between the last reported value and two reported steps earlier"),
 ("4","orientation","u = polarity × q, so higher u is always worse"),
 ("5","normalisation","raw value to a 0 to 100 grade inside the peer set, by one of four normalisers"),
 ("6","aggregation","fields to pillar to composite, under the missing-data rule and the chosen mean"),
 ("7","rank","R = 100 (N − rho) / (N − 1), so 100 is best of those with a score"),
 ("8","distribution","consensus = median R, contestation = interquartile width ÷ 5.88")]
y=1.3
for n,name,desc in steps:
    box(s,0.85,y,11.6,0.62,PANEL if int(n)%2 else None)
    text(s,1.1,y+0.14,0.5,0.35,[[(n,{"size":19,"bold":True,"color":ACC})]])
    text(s,1.75,y+0.16,2.1,0.35,[[(name,{"size":13,"bold":True})]])
    text(s,3.95,y+0.17,8.3,0.35,[[(desc,{"size":11.5,"color":INK2})]])
    y+=0.66
box(s,0.85,6.7,11.6,0.62,None,ACC,2)
text(s,1.2,6.86,11.0,0.4,
     [[("Order matters: aggregate fields inside each specification, then take the distribution across specifications. Reversing them collapses the spread.",
        {"size":13,"bold":True})]])

# ── A11 · BONUS DETAIL ──────────────────────────────────────────────
s = slide(); atitle(s,"A11","Bonus: the allocation rule and the signal behind it")
rows=[["Ticker","P(A) level","P(B) change","Delta","Bucket"],
 ["MPC","0.12","0.73","+0.61","Transition core"],["OXY","0.27","0.69","+0.41","Transition core"],
 ["HAL","0.02","0.39","+0.38","Excluded, base below 0.05"],["PSX","0.23","0.51","+0.28","Transition core"],
 ["KMI","0.27","0.53","+0.27","Transition satellite"],["WMB","0.35","0.57","+0.22","Transition satellite"],
 ["EXE","0.99","0.62","−0.38","Priced leader"],["XOM","0.72","0.26","−0.46","Priced leader"],
 ["EOG","1.00","0.34","−0.66","Priced leader, funds the book"]]
y=1.3
for ri,row in enumerate(rows):
    if ri==0: box(s,0.85,y,6.6,0.38,INK)
    elif ri%2==0: box(s,0.85,y,6.6,0.4,PANEL)
    for ci,v in enumerate(row):
        c=WHITE if ri==0 else (ACC if ci==3 and ri<7 else INK)
        text(s,[1.05,2.0,3.1,4.3,5.2][ci],y+0.07,1.3,0.3,[[(v,{"size":10.5,"bold":ri==0 or ci==3,"color":c})]])
    y+=0.38 if ri==0 else 0.4
alloc=[("350","Trajectory long","top quartile of delta, excluding a base below 0.05"),
 ("250","Convention long","P rises as the missing-data rule hardens under CSRD and ISSB"),
 ("150","Enablers","grid and electrification suppliers. Small, because it is the crowded trade"),
 ("−150","Structural short","P(A) < 0.2 and delta < 0.05. Funds the book, strips sector beta"),
 ("250","Dry powder","deploy on a 15% drawdown within 90 days, else revert to benchmark")]
y=1.3; text(s,7.75,y,4.7,0.35,[[("$m allocation",{"size":13,"bold":True})]]); y+=0.42
for amt,name,rule_ in alloc:
    box(s,7.75,y,4.7,0.76,PANEL)
    text(s,7.95,y+0.1,1.0,0.3,[[(amt,{"size":15,"bold":True,"color":ACC})]])
    text(s,9.0,y+0.08,3.3,0.3,[[(name,{"size":11.5,"bold":True})]])
    text(s,9.0,y+0.38,3.3,0.32,[[(rule_,{"size":9.5,"color":INK2})]])
    y+=0.82
text(s,0.85,5.5,6.6,1.5,
     [[("Three disciplines from the framework, not from taste.",{"size":13,"bold":True})],
      [("Size by probability, not conviction. Cap correlated clusters so three bets on cheap hydrogen count once. "
        "Exit when P(A) exceeds 0.8, because Pástor shows green assets earn lower expected returns once repriced.",{"size":11,"color":INK2})]],space=5,ls=1.15)
text(s,0.85,6.9,11.6,0.4,
     [[("It cannot rank Apple against ExxonMobil. A real book runs this per sector with sector-neutral limits.",{"size":11,"color":INK3})]])

# ── A12 · REPRODUCIBILITY ───────────────────────────────────────────
s = slide(); atitle(s,"A12","Reproducibility")
acard(s,0.85,1.25,3.7,1.6,"seconds","to run all 17,496 specifications on a laptop. numpy and pandas only.","18")
acard(s,4.8,1.25,3.7,1.6,"rank points","the browser tool reproduces the Python pipeline to this tolerance, on all 18 companies.","0.05")
acard(s,8.75,1.25,3.7,1.6,"dependencies","No build step, no network, no server. The explorer opens from a static folder.","0")
y=3.15; text(s,0.85,y,11.6,0.35,[[("The pipeline",{"size":14,"bold":True})]]); y+=0.45
for cmd,desc in [("python3 registry.py","the field registry, printed for inspection"),
                 ("python3 load.py","the arrays and a coverage report"),
                 ("python3 run.py","every specification into out/"),
                 ("python3 export_web.py","the pillar cube for the browser explorer"),
                 ("python3 -m http.server 4173 --directory ../web","the interactive tool")]:
    box(s,0.85,y,11.6,0.44,PANEL)
    text(s,1.1,y+0.09,5.2,0.32,[[(cmd,{"size":11.5,"bold":True,"color":ACC})]])
    text(s,6.5,y+0.09,5.8,0.32,[[(desc,{"size":11,"color":INK2})]])
    y+=0.48
box(s,0.85,5.95,11.6,1.05,None,ACC,2)
text(s,1.2,6.15,11.0,0.7,
     [[("Bloomberg cell values are withheld for licensing. ",{"size":13,"bold":True}),
       ("Everything derived from them is published: the loader, the formula, every computed output and the explorer. "
        "We are happy to show the files in person to demonstrate the model runs on real data.",{"size":13})]],ls=1.15)
