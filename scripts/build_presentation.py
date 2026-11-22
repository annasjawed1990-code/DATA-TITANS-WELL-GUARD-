"""Build competition slide deck from documented aggregate metrics only.
No raw/private well data are used. Product screenshots are from the tested synthetic app.
"""
from pathlib import Path
import math
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN,MSO_ANCHOR

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'presentation'/'DATA_TITANS_WellGuard_AI_Competition_Deck.pptx'
prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
BG='091522';PANEL='11263B';PANEL2='172E44';LINE='2F4B60';WHITE='F0F7FD';MUTED='A1B7CA';TEAL='24D2C6';GOLD='FFC170';RED='F68E96';BLUE='639EEA'

def rgb(c):return RGBColor.from_string(c)
def rect(sl,x,y,w,h,fill,round=False,line=None,opacity=0):
    sh=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round else MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    sh.fill.solid();sh.fill.fore_color.rgb=rgb(fill)
    sh.line.fill.background() if not line else None
    if line:sh.line.color.rgb=rgb(line);sh.line.width=Pt(.7)
    if round:
        try:sh.adjustments[0]=.14
        except Exception:pass
    return sh

def txt(sl,t,x,y,w,h,size=18,color=WHITE,bold=False,align=None,margin=0,italic=False,para_space=None):
    sh=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=sh.text_frame;tf.word_wrap=True
    tf.margin_left=Inches(margin);tf.margin_right=Inches(margin);tf.margin_top=Inches(.04);tf.margin_bottom=Inches(.02)
    tf.clear();p=tf.paragraphs[0];p.text=t;p.font.name='Aptos';p.font.size=Pt(size);p.font.bold=bold;p.font.italic=italic;p.font.color.rgb=rgb(color)
    if align:p.alignment=align
    if para_space:p.space_after=Pt(para_space)
    return sh

def label(sl,text,x,y,w=7):txt(sl,text.upper(),x,y,w,.3,11,TEAL,True)
def title(sl,text,subtitle=None):
    txt(sl,text,.64,.83,12.1,.7,29,WHITE,True)
    if subtitle:txt(sl,subtitle,.66,1.58,11.8,.6,14,MUTED)

def new_slide(kicker='RESEARCH PROTOTYPE',page=1):
    sl=prs.slides.add_slide(prs.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=rgb(BG)
    rect(sl,0,0,.10,7.5,TEAL)
    txt(sl,'◈ WELLGUARD AI',.63,.29,3.0,.34,13,TEAL,True)
    txt(sl,'DATA TITANS  /  DSMLC DATATHON 2026',9.0,.29,3.7,.34,9,MUTED,True,PP_ALIGN.RIGHT)
    rect(sl,.65,6.95,11.95,.01,LINE)
    txt(sl,'STRATHCONA RESOURCES  •  HISTORICAL ANALYSIS',.66,7.03,7.3,.25,8,MUTED)
    txt(sl,f'{page:02d}',12.12,7.01,.35,.27,9,MUTED,False,PP_ALIGN.RIGHT)
    return sl

def card(sl,x,y,w,h,heading,body,accent=TEAL,hd=17,bd=13):
    rect(sl,x,y,w,h,PANEL,True,LINE)
    rect(sl,x+.18,y+.25,.06,.5,accent,True)
    txt(sl,heading,x+.38,y+.19,w-.55,.46,hd,WHITE,True)
    txt(sl,body,x+.38,y+.76,w-.55,h-.84,bd,MUTED)

def num_card(sl,x,y,w,h,number,desc,accent=TEAL):
    rect(sl,x,y,w,h,PANEL,True,LINE)
    txt(sl,number,x+.24,y+.23,w-.48,.63,30,accent,True)
    txt(sl,desc,x+.24,y+.98,w-.47,.65,12,MUTED)

def bar(sl,label_s,val,x,y,w,max_val=.2,height=.27,color=TEAL):
    txt(sl,label_s,x,y-.1,3.6,.45,13,WHITE)
    rect(sl,x+3.75,y,w,height,PANEL2,True)
    rect(sl,x+3.75,y,max(.04,w*val/max_val),height,color,True)
    txt(sl,f'{val:.3f}',x+3.83+w,y-.09,.7,.36,15,color,True)

# 1 cover
s=new_slide(page=1)
label(s,'WEEKLY INSPECTION PRIORITIZATION',.74,1.05,11)
txt(s,'WellGuard AI',.73,1.66,11,1.15,57,WHITE,True)
txt(s,'Predict. Prioritize. Explain.',.77,2.81,10.8,.72,31,TEAL,True)
txt(s,'An evidence-first, capacity-constrained inspection approach\nfor producing oil wells.',.78,3.73,10.8,1.04,21,MUTED)
rect(s,.78,5.5,11.64,.81,PANEL,True,LINE)
txt(s,'116 vs 75 recorded events surfaced at 25 reviews per week',1.13,5.67,10.9,.42,18,WHITE,True)

#2
s=new_slide(page=2);label(s,'01 / QUESTION',.67,.65);title(s,'Which wells deserve inspection first?','Objective: maximize the usefulness of a fixed maintenance-review capacity.')
card(s,.72,2.05,5.7,3.65,'Research question','Can the previous two weeks of recorded operations help identify wells at elevated risk of a documented equipment failure in the NEXT 14 DAYS?',TEAL,19,19)
card(s,6.68,2.05,5.92,1.55,'Operational framing','Prioritize well inspection—not autonomous controls.',GOLD,17,14)
card(s,6.68,3.82,5.92,1.87,'Decision metric','How many eligible distinct failures were ranked in the top 25 / 50 / 100 weekly slots?',TEAL,17,14)
txt(s,'RESEARCH, NOT AN IMPLEMENTED PREVENTION PROGRAM',.77,6.24,10,.35,12,GOLD,True)

#3
s=new_slide(page=3);label(s,'02 / DATA',.67,.65);title(s,'Three datasets. One well identifier.','The join key is UWI; event dates must be handled with strict as-of logic.')
num_card(s,.73,2.12,3.75,2.18,'5.08M','Daily production records\n41 columns',TEAL)
num_card(s,4.79,2.12,3.75,2.18,'15,610','Maintenance job records\n19 columns',GOLD)
num_card(s,8.85,2.12,3.75,2.18,'2,873','Documented failure events\n18 columns',BLUE)
card(s,.74,4.62,11.85,1.46,'Temporal integration','Aggregate production into observed well-weeks; attach only failures and measurements dated on or before each snapshot. Jobs support contextual review; future work orders are excluded from prediction.',TEAL,16,13)

#4
s=new_slide(page=4);label(s,'03 / DATA REALITY',.67,.65);title(s,'A major reporting shift changes interpretation','Observed recorded failures by calendar year—not ground-truth incident rates.')
vals=[1,1,0,0,1230,1641];yrs=['2021','2022','2023','2024','2025','2026 to Oct.']
for i,(yr,v) in enumerate(zip(yrs,vals)):
    x=.88+i*2.02
    h=max(.03,2.9*v/1700)
    rect(s,x,5.18-h,1.37,h,TEAL if i>=4 else LINE,True)
    txt(s,f'{v:,}',x,5.1-h,1.37,.37,16,WHITE,True,PP_ALIGN.CENTER)
    txt(s,yr,x,5.35,1.37,.35,13,MUTED,True,PP_ALIGN.CENTER)
rect(s,.83,5.95,11.67,.57,PANEL2,True)
txt(s,'No recorded failures in 2023–24 does NOT mean the wells were failure-free.',1.15,6.05,11,.37,16,GOLD,True)

#5
s=new_slide(page=5);label(s,'04 / EXPERIMENT',.67,.65);title(s,'Time-aware 14-day risk-ranking experiment','Sunday cutoff: at least six reported days and three producing days in the current week.')
for x,w,date,sub,col in [(.82,3.48,'TRAIN','Jun 2025 – Mar 1, 2026',TEAL),(4.85,3.25,'VALIDATE','Mar 22 – May 17, 2026',GOLD),(8.66,3.8,'CHRONOLOGICAL HOLDOUT','Jun 7 – Oct 4, 2026',BLUE)]:
    rect(s,x,2.2,w,1.76,PANEL,True,LINE);txt(s,date,x+.19,2.51,w-.3,.43,20,col,True);txt(s,sub,x+.19,3.21,w-.3,.4,14,MUTED)
txt(s,'21-day gap',4.31,4.13,1.4,.35,12,GOLD,True,PP_ALIGN.CENTER)
txt(s,'21-day gap',8.23,4.13,1.4,.35,12,GOLD,True,PP_ALIGN.CENTER)
card(s,.84,4.69,5.65,1.49,'Inputs available at snapshot','Two-week oil, water, downtime and pump signals; previous recorded failures.',TEAL,16,12)
card(s,6.74,4.69,5.66,1.49,'Target after snapshot','A documented failure begins during days 1–14 after the historical week end.',GOLD,16,12)

#6
s=new_slide(page=6);label(s,'05 / BASELINES',.67,.65);title(s,'A clear signal, with a transparent model trade-off','Average precision (AP) on a chronological holdout; 4.5% positive prevalence.')
for i,(name,v,col) in enumerate([('Random / prevalence',.045,LINE),('Recent downtime',.046,BLUE),('Failure recency',.103,GOLD),('Operating data only',.148,'66BFC9'),('Full LightGBM',.164,TEAL)]):
    bar(s,name,v,.98,2.08+i*.68,7.5,max_val=.18,height=.26,color=col)
rect(s,.93,5.75,11.62,.62,PANEL,True,LINE)
txt(s,'Seven-day-old inputs: refit model surfaces 66 events versus 75 for recency at 25 slots.',1.13,5.9,11.25,.32,15,WHITE,True)

#7
s=new_slide(page=7);label(s,'06 / ACTIONABLE METRIC',.67,.65);title(s,'How does review capacity change coverage?','Distinct-event recall: full model (teal) and continuous failure recency (gold).')
for i,(cap,model,base) in enumerate([(25,18.0,11.7),(50,28.0,17.7),(100,44.9,29.2)]):
    y=2.14+i*1.26
    txt(s,f'{cap} wells/week',.85,y,2.3,.37,18,WHITE,True)
    rect(s,3.11,y+.02,7.0,.3,PANEL2,True)
    rect(s,3.11,y+.02,7.0*model/50,.3,TEAL,True)
    rect(s,3.11,y+.45,7.0,.16,PANEL2,True)
    rect(s,3.11,y+.45,7.0*base/50,.16,GOLD,True)
    txt(s,f'{model:.1f}%',10.34,y-.02,1.1,.39,19,TEAL,True)
    txt(s,f'{base:.1f}% baseline',10.33,y+.38,1.6,.29,12,GOLD)
rect(s,.89,6.17,11.57,.38,PANEL2,True)
txt(s,'25/week × 18 weeks: 450 reviews per policy. 643 eligible events; +6.4 percentage points.',1.06,6.2,11.25,.26,12,MUTED)

#8 — real browser-tested synthetic dashboard screenshot; not a fabricated mock-up
s=new_slide(page=8);label(s,'07 / WORKING PRODUCT',.67,.65)
title(s,'A real, interactive inspection queue','Screenshot from our browser-tested synthetic HTML; no restricted individual-well observations are shown.')
image_path=ROOT/'presentation'/'synthetic_queue_screenshot_cropped.png'
s.shapes.add_picture(str(image_path),Inches(.83),Inches(2.05),width=Inches(11.63))
txt(s,'LIVE DEMO: select week  •  change 25 to 50 slots  •  apply a no-repeat policy  •  open well evidence',.94,6.48,11.4,.3,12,GOLD,True)

#9
s=new_slide(page=9);label(s,'08 / EXPLAINABILITY',.67,.65);title(s,'Well Investigator: evidence, not diagnoses','Optional local LLM can draft a report, but deterministic observations remain the source of truth.')
card(s,.83,2.1,3.64,2.69,'Observed signals','Recent oil production\nTwo-week downtime\nRPM, torque, current\nData completeness checks',TEAL,16,15)
card(s,4.84,2.1,3.65,2.69,'Model transparency','Top local feature drivers\nHistorical relative rank\nNo probability claim\nNo causal interpretation',GOLD,16,15)
card(s,8.85,2.1,3.64,2.69,'Operator review','Check source historian\nReview job/failure records\nConfirm field context\nHuman-authorized action',BLUE,16,15)
rect(s,.85,5.28,11.61,.86,PANEL2,True)
txt(s,'No autonomous pump control.  No fabricated root cause.  No sending private data to hosted AI.',1.12,5.52,11,.46,16,WHITE,True)

#10
s=new_slide(page=10);label(s,'09 / BUSINESS CASE',.67,.65);title(s,'Value must be modeled transparently','An assumption-based sensitivity simulator—not a promise of realized savings.')
rect(s,.9,2.03,11.54,1.2,PANEL,True,LINE)
txt(s,'Candidate events × Addressable % × Success % × Oil per event × CAD/m³',1.15,2.27,11.05,.34,18,TEAL,True,PP_ALIGN.CENTER)
txt(s,'minus  |  Inspection slots × Cost per inspection',1.15,2.73,11.05,.32,17,GOLD,True,PP_ALIGN.CENTER)
for i,(number,desc) in enumerate([('25','inspections per week'),('3','assumed candidate events/week'),('25%','assumed addressable'),('30%','assumed successful')]):
    num_card(s,.86+i*3.0,3.82,2.7,1.79,number,desc,TEAL if i%2==0 else GOLD)
txt(s,'Break-even success = inspection spending / assumed potential gross benefit; no measured ROI.',.93,6.16,11.4,.35,13,RED,True)

#11
s=new_slide(page=11);label(s,'10 / LIMITATIONS',.67,.65);title(s,'Three reasons to keep claims modest','Proactively identifying uncertainty is essential to safe and credible field use.')
card(s,.84,2.09,3.62,3.23,'Reporting process','Failure events nearly absent before 2025 and closely aligned with maintenance jobs.',RED,19,16)
card(s,4.84,2.09,3.62,3.23,'Signal quality','Different well types; pump telemetry often missing; placeholder and outlier values.',GOLD,19,16)
card(s,8.85,2.09,3.61,3.23,'Causal impact','No prospective trial, probability calibration or measured failure prevention / savings.',TEAL,19,16)
txt(s,'Our claim: a useful historical prioritization signal.  Not proof of operational benefit.',.96,5.82,11.3,.49,18,WHITE,True)

#12
s=new_slide(page=12);label(s,'11 / EXECUTION PLAN',.67,.65);title(s,'A realistic path from prototype to pilot','A controlled validation sequence before any operational integration.')
for i,(hd,body) in enumerate([('01  REPRODUCE','Run original Parquet pipeline and verify model metrics.'),('02  AUDIT','Field and well-type reporting consistency, missing sensors.'),('03  SHADOW TRIAL','Rank without changing operations; collect independent outcomes.'),('04  DECISION PILOT','Authorize limited inspections; compare workload and results.')]):
    x=.85+i*3.02
    card(s,x,2.20,2.75,3.27,hd,body,TEAL if i%2==0 else GOLD,15,15)
rect(s,.89,5.97,11.53,.52,PANEL2,True)
txt(s,'Success metrics:  event recall at fixed workload, false-alert burden, field acceptance, and verified value.',1.10,6.07,11.1,.34,13,WHITE,True)

#13 close
s=new_slide(page=13)
label(s,'DATA TITANS  /  FINAL MESSAGE',.78,1.0,11)
txt(s,'From noisy records\nto reviewable decisions.',.78,1.58,11.5,1.78,39,WHITE,True)
rect(s,.81,4.13,11.65,.05,TEAL)
txt(s,'We identified a measurable prioritization signal, tested it against simple baselines,\nand built a decision-support prototype that makes assumptions visible.',.88,4.52,11.5,1.21,20,MUTED)
txt(s,'25 reviews/week: full 116  •  operating-only 111  •  recency 75',.87,6.03,11.5,.38,17,TEAL,True)

#14 appendix disclosure
s=new_slide(page=14);label(s,'APPENDIX / SOURCES & DISCLOSURE',.67,.65);title(s,'Attribution, AI use and data stewardship')
card(s,.86,2.06,5.52,3.83,'Sources','DSMLC 2026 Briefing, Dataset Handbook, Research Guide; Strathcona competition Parquet files; SPE PetroWiki PCP overview; SLB PCP Defining Series; LightGBM and scikit-learn documentation. See REFERENCES.md.',TEAL,17,15)
card(s,6.66,2.06,5.8,3.83,'AI assistance','ChatGPT assisted research, code, model evaluation, application, slides and video production. All work requires registered team members to run and verify. Raw competition datasets and identifiable well-level results are excluded from the public submission.',GOLD,17,15)

OUT.parent.mkdir(parents=True,exist_ok=True)
prs.save(OUT)
print('Created',OUT,'slides',len(prs.slides), 'bytes',OUT.stat().st_size)
