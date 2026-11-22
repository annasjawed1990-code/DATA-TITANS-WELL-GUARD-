"""WellGuard AI: private retrospective replay + strictly synthetic public demo.

Start: streamlit run app.py
Private historical data are read ONLY from the local gitignored outputs/ directory.
The UI must never be deployed to a public host with private competition well-level data.
"""
from __future__ import annotations
import json,sys,urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from core.demo_data import generate_synthetic_demo
from core.decision import investigator_report,well_evidence,scenario_weekly_gross_exposure,available
from core.scheduling import schedule_inspections,break_even_success_rate

st.set_page_config(page_title='WellGuard AI | DATA TITANS',page_icon='◈',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>
.stApp {background:#091322;color:#E5EDF6}
h1,h2,h3 {letter-spacing:-.02em}
[data-testid="stSidebar"] {background:#102239}
[data-testid="stMetric"] {background:rgba(19,39,63,.85);border:1px solid #25445C;padding:14px 18px;border-radius:13px}
[data-testid="stTabs"] button {font-weight:600}
.block-container {padding-top:1.5rem}
.main .block-container {max-width:1600px}
</style>''',unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_data(private:bool):
    if private:
        context=ROOT/'outputs/private_test_with_context.csv'
        d=pd.read_csv(context if context.exists() else ROOT/'outputs/private_test_alerts.csv',parse_dates=['week_end'])
        m=json.loads((ROOT/'outputs/aggregate_model_metrics.json').read_text())
        return d,m
    return generate_synthetic_demo(),{}

@st.cache_data(show_spinner=False)
def load_aggregate():
    def read(filename):
        p=ROOT/'results'/filename
        return json.loads(p.read_text()) if p.exists() else {}
    return (read('model_feasibility.json'),read('robustness_summary.json'),
            read('events_summary.json'),read('production_summary.json'))

feas,rob,event,production=load_aggregate()
m=feas.get('metrics',{})
model_m=m.get('LightGBM preliminary',{})
base_m=m.get('Recent failure (90 days)',{})
adv_path=ROOT/'results'/'advanced_validation_public.json'
adv=json.loads(adv_path.read_text()) if adv_path.exists() else {}
recency_ap=adv.get('recency_baseline_ap',.1030)
prevalence=feas.get('data',{}).get('test_positive_rate',.045)
private_ready=(ROOT/'outputs/private_test_alerts.csv').exists() and (ROOT/'outputs/aggregate_model_metrics.json').exists()

with st.sidebar:
    st.markdown('## ◈ WellGuard AI')
    st.caption('DATA TITANS · DSMLC Datathon 2026')
    st.markdown('**Historical inspection-priority research**')
    # Never accidentally project a proprietary well on an initial screen-share launch.
    choices=['Synthetic demo','Private replay'] if private_ready else ['Synthetic demo']
    mode=st.radio('Display mode',options=choices,index=0,
                  help='Default is SYNTHETIC. Private replay uses local restricted well-level records and must never be screen-shared or hosted publicly.')
    requested_private=mode=='Private replay'
    approved=st.checkbox('I confirm private replay is on an authorized local machine, with no public screen share.',value=False) if requested_private else False
    if requested_private and not approved:
        st.warning('Private replay is locked until you acknowledge the data-sharing restriction. Showing synthetic data instead.')
    private=requested_private and approved
    st.info('🔒 PRIVATE HISTORICAL REPLAY — DO NOT SCREEN-SHARE' if private else '🧪 SYNTHETIC ILLUSTRATION — NOT REAL WELLS')
    st.divider()
    st.caption('2026 DSMLC challenge | Strathcona Resources dataset | historical 14-day label')
    st.caption('Do not publish raw Parquet files or private well-level scoring outputs.')
    st.caption('No autonomous decisions. Inspect with an authorized operator.')

df,metrics=load_data(private)
df['week_end']=pd.to_datetime(df['week_end'])
sensor_columns=['eff_avg_2w','rpm_avg_2w','torque_avg_2w','current_avg_2w']
df['sensor_channels']=df[sensor_columns].notna().sum(axis=1)
if len(df)==0:st.error('No replay observations available.');st.stop()

st.title('WellGuard AI')
st.markdown('**Predict. Prioritize. Explain.**  |  Evidence-based inspection scheduling for oil-well operations')
st.warning('Model output is an **uncalibrated relative ranking**, not a failure probability. Training and evaluation are retrospective; this tool has not demonstrated actual prevented failures.')
if not private:
    st.caption('DEMO RULE: Well IDs, time series, scores, and outcomes displayed below are **fully synthetic**. Model-quality statistics are aggregate results from a separate historical experiment; never interpret synthetic dashboard events as real predictions.')

st.markdown('#### Research evidence — June to October 2026 historical holdout')
display_metrics = metrics if private else {}
k1,k2,k3,k4=st.columns(4)
k1.metric('Model average precision',f"{display_metrics.get('model_ap',model_m.get('average_precision',0)):.3f}")
k2.metric('Failure-recency baseline AP',f"{display_metrics.get('recency_baseline_ap',recency_ap):.3f}")
k3.metric('Model ROC-AUC',f"{display_metrics.get('model_roc_auc',model_m.get('roc_auc',0)):.3f}")
k4.metric('Holdout base rate',f"{display_metrics.get('test_positive_rate',prevalence):.1%}")

tab_fleet,tab_queue,tab_investigate,tab_validation,tab_scenario,tab_method=st.tabs(
    ['◈ Fleet overview','▤ Inspection queue','⌕ Well investigator','▥ Validation','⌁ Decision simulator','ⓘ Methods & limitations'])

with tab_fleet:
    left,right=st.columns([1.35,1])
    with left:
        st.subheader('Historical failure-reporting shift')
        if event.get('failure_by_year'):
            years=event['failure_by_year']
            if isinstance(years,dict):
                dat=pd.DataFrame({'Year':list(years.keys()),'Failure events':list(years.values())})
            else:dat=pd.DataFrame(years)
        else:dat=pd.DataFrame({'Year':['2021','2022','2023','2024','2025','2026'],
                                  'Failure events':[1,1,0,0,1230,1641]})
        fig=px.bar(dat,x='Year',y='Failure events',text_auto=True,color_discrete_sequence=['#23C7C1'])
        fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=330)
        st.plotly_chart(fig,use_container_width=True)
        st.caption('Absence of failure logs in earlier years is NOT proof of failure-free operations. The change may reflect reporting coverage.')
    with right:
        st.subheader('Operational decision')
        st.markdown('**Proposed workflow**')
        st.markdown('''1. Review a fixed weekly alert capacity.  
2. Inspect the observed production and equipment evidence.  
3. Check the relevant field records.  
4. Decide on inspection with an authorized specialist.  
5. Record outcomes to improve prospective evaluation.''')
        st.info('Opportunity: identify a **small, reviewable queue** rather than assert automatic repair diagnosis.')
        st.metric('Eligible failure events in historical holdout',rob.get('event_coverage',{}).get('eligible_events_with_active_lookback',643))

    st.subheader('Historical estimated lost-oil exposure')
    downtimes=[('Long-term shut-in',162412),('Downhole equipment – rods',72080),('Rodstring failure',40015),('Facility capacity',29374),('Downhole equipment – pump',24205),('Tubing failure',24097)]
    chart=pd.DataFrame(downtimes,columns=['Downtime code','Estimated lost oil (m³)'])
    f=px.bar(chart.sort_values('Estimated lost oil (m³)'),x='Estimated lost oil (m³)',y='Downtime code',orientation='h',color_discrete_sequence=['#23C7C1'])
    f.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=340)
    st.plotly_chart(f,use_container_width=True)
    st.caption('Source-coded historical aggregate categories. These volumes are **not** recoverable volume estimates or attributable solely to equipment failures.')

with tab_queue:
    st.subheader('Historic weekly inspection queue')
    date_choices=sorted(df.week_end.dt.date.unique(),reverse=True)
    a,b,c=st.columns([2,1,1])
    week=a.selectbox('As-of date',date_choices,format_func=lambda d:d.strftime('%d %b %Y'))
    cap=b.select_slider('Wells to review',options=[10,25,50,100],value=25)
    cooldown=st.selectbox('Repeat-review cooldown (exploratory)',options=[0,1,2],index=0,help='Prevents repeat selection in the next N weekly snapshots; NOT independently validated.')
    outcomes=c.toggle('Reveal future outcomes (hindsight)',value=False,
                      help='Use OFF during a demo of the operator view; future labels were unavailable at the historical prediction date.')
    wk=df[df.week_end.dt.date==week].sort_values(['relative_risk_score','uwi'],ascending=[False,True]).copy()
    wk['rank']=np.arange(1,len(wk)+1)
    selected=schedule_inspections(df,capacity=cap,cooldown_weeks=cooldown,through_date=week)
    selected=selected[selected.week_end.dt.date==week].copy()
    # The scheduler writes review_rank; the displayed queue must use that rank,
    # not an unavailable 'rank' column from the unselected candidate frame.
    selected['rank']=selected['review_rank'].astype(int)
    if cooldown: st.caption('Cooldown queue is a retrospectively explored scheduling hypothesis. Previous selections are based only on earlier dates, not future labels.')
    j1,j2,j3=st.columns(3)
    j1.metric('Eligible wells in snapshot',f'{len(wk):,}')
    j2.metric('Selected for review',len(selected))
    j3.metric('Selected future-positive well-weeks' if outcomes else 'Score range (relative)',
              str(int(selected.target_14d.sum())) if outcomes else (f'{selected.relative_risk_score.min():.3f}–{selected.relative_risk_score.max():.3f}' if len(selected) else 'No eligible wells'))
    view=['rank','uwi','relative_risk_score','sensor_channels','oil_daily_avg_2w','down_fraction_2w','rpm_avg_2w']
    if outcomes:view+=['target_14d']
    rename={'rank':'Rank','uwi':'Well ID','relative_risk_score':'Relative score',
            'oil_daily_avg_2w':'Oil (m³/day)','down_fraction_2w':'Downtime fraction',
            'rpm_avg_2w':'Pump RPM','sensor_channels':'Pump channels / 4','target_14d':'Recorded failure 1–14d later'}
    st.dataframe(selected[view].rename(columns=rename),use_container_width=True,hide_index=True,height=400)
    fig=px.scatter(wk,x='oil_daily_avg_2w',y='relative_risk_score',color='down_fraction_2w',
                   hover_name='uwi',color_continuous_scale='Tealgrn',labels={'oil_daily_avg_2w':'Observed mean oil rate (m³/day)',
                                                                              'relative_risk_score':'Relative alert score','down_fraction_2w':'Downtime fraction'})
    fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=350)
    st.plotly_chart(fig,use_container_width=True)
    st.caption('Scores are ranked within the eligible wells; no absolute probability calibration or cost-optimal threshold is claimed.')

with tab_investigate:
    st.subheader('Evidence-first well investigation')
    x1,x2=st.columns([2,1])
    with x1:
        chosen_week=st.selectbox('Snapshot date',sorted(df.week_end.dt.date.unique(),reverse=True),key='investigate_week')
        candid=df[df.week_end.dt.date==chosen_week].sort_values('relative_risk_score',ascending=False)
        chosen_well=st.selectbox('Well to investigate',candid.uwi.tolist(),key='investigate_well')
    row=candid[candid.uwi==chosen_well].iloc[0]
    rank=int(candid.uwi.tolist().index(chosen_well)+1)
    with x2:
        st.metric('Relative alert score',f'{row.relative_risk_score:.3f}')
        st.caption(f'Rank {rank:,} of {len(candid):,} eligible wells')
    all_hist=df[(df.uwi==chosen_well)&(df.week_end.dt.date<=chosen_week)].sort_values('week_end').copy()
    st.caption('Charts are strictly cut off at the selected as-of date; no later history is shown.')
    chart1,chart2=st.columns(2)
    for tgt,col,ttl in [(chart1,'relative_risk_score','Historical relative alert score'),(chart2,'oil_daily_avg_2w','Observed oil production (m³/day)')]:
        fig=px.line(all_hist,x='week_end',y=col,markers=True,title=ttl)
        fig.update_traces(line_color='#23C7C1')
        fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=300)
        tgt.plotly_chart(fig,use_container_width=True)
    chart3,chart4=st.columns(2)
    for tgt,col,ttl in [(chart3,'down_fraction_2w','Two-week downtime fraction'),(chart4,'rpm_avg_2w','Pump RPM')]:
        fig=px.line(all_hist,x='week_end',y=col,markers=True,title=ttl)
        fig.update_traces(line_color='#F4AC53')
        fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=300)
        tgt.plotly_chart(fig,use_container_width=True)
    if int(row.get('sensor_channels',0))<2:
        st.warning('Instrumentation warning: fewer than 2 of 4 pump-related channels were observed in this snapshot. Missingness may reflect well type or telemetry coverage, and model performance may not transfer to this well without field validation.')
    st.markdown(investigator_report(row.to_dict(),rank))
    # Local TreeSHAP margin contributions are available only when a model produced them.
    # Signs describe changes in model log-odds, not root causes or calibrated risk.
    signed=[]
    for idx in (1,2,3):
        driver=row.get(f'driver_{idx}')
        margin=row.get(f'driver_{idx}_margin')
        if isinstance(driver,str) and available(margin):
            signed.append({'Model feature':driver.replace('_',' '),'Margin contribution':float(margin)})
    if signed:
        st.markdown('#### Signed model contributions (local explanation)')
        attribution=pd.DataFrame(signed)
        fig=px.bar(attribution,x='Margin contribution',y='Model feature',orientation='h',
            color='Margin contribution',color_continuous_scale=['#ed808c','#a9c4d7','#27d4c8'],
            color_continuous_midpoint=0)
        fig.add_vline(x=0,line_dash='dash',line_color='#a2b5c8')
        fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',height=240,showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
        st.caption('Signed TreeSHAP margin units: positive pushes the model score up, negative pushes it down. Three largest absolute features only. Not mechanical fault attribution.')
    else:
        st.caption('Signed feature contributions are unavailable in this synthetic example. The listed example drivers are not measured causal explanations.')
    if private and 'last_job_date' in row.index:
        st.markdown('#### As-of maintenance and failure-log context')
        st.caption('These records were not prediction inputs. The dates shown are on or before the selected historical snapshot.')
        a1,a2,a3=st.columns(3)
        a1.metric('Prior job dates in 90 days',int(row.get('prior_jobs_90d',0)) if available(row.get('prior_jobs_90d')) else 'Unknown')
        a2.metric('Last recorded job type',str(row.get('last_job_type','Not recorded')) if pd.notna(row.get('last_job_type')) else 'Not recorded')
        a3.metric('Earlier recorded failure type',str(row.get('last_recorded_failure_type','None recorded')) if pd.notna(row.get('last_recorded_failure_type')) else 'None recorded')
        st.caption('Last job field estimate is not an actual incurred cost; it is excluded from the predictive model. No subsequent work orders or failure records are provided as evidence for the selected date.')
    elif not private:
        st.caption('Maintenance and recorded failure histories are omitted from this public synthetic illustration.')
    with st.expander('Optional local AI narrative — Ollama (runs on your own machine)'):
        st.caption('Never send restricted well information to an external hosted AI API without organizer/data-owner permission. Local inference only.')
        model_name=st.text_input('Installed local model name',value='qwen2.5:3b')
        if st.button('Generate a local, evidence-bounded explanation'):
            facts='\n'.join(f'{k}: {v}' for k,v in well_evidence(row.to_dict(),rank))
            system=('You are an industrial data reporting assistant. Use ONLY the supplied observations. '
                    'Do not diagnose equipment failures, invent measurements, recommend unauthorized actions, '
                    'interpret the score as a probability, or claim savings. Respond with Observations, Missing data, Checks for operator.')
            try:
                req=urllib.request.Request('http://127.0.0.1:11434/api/generate',
                    data=json.dumps({'model':model_name,'prompt':system+'\nOBSERVATIONS:\n'+facts,'stream':False,
                                     'options':{'temperature':0}}).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req,timeout=70) as response:
                    answer=json.loads(response.read().decode()).get('response','')
                st.markdown(answer)
                st.warning('AI prose is unverified. Compare each claim with the evidence above before using.')
            except Exception as err:
                st.error('Local Ollama is not running or the model is unavailable. The verified deterministic evidence brief above remains usable. '+str(err))

with tab_validation:
    st.subheader('What does the model improve over?')
    st.caption('This tab summarizes the frozen release benchmark.')
    comparisons=pd.DataFrame([
        ('Random ranking / prevalence',prevalence),
        ('Recent downtime',m.get('14d downtime intensity',{}).get('average_precision',.046)),
        ('Previous-failure recency',recency_ap),
        ('Prior failure within 90 days (weak comparator)',base_m.get('average_precision',.077)),
        ('Production & sensor features only',rob.get('sensor_only',{}).get('AP',.149)),
        ('Full LightGBM',model_m.get('average_precision',.164)),
    ],columns=['Approach','Average precision'])
    fig=px.bar(comparisons,x='Average precision',y='Approach',orientation='h',text_auto='.3f',color_discrete_sequence=['#23C7C1'])
    fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=330)
    st.plotly_chart(fig,use_container_width=True)
    st.info('At 25 weekly reviews, the release benchmark surfaced **116 full-model, 111 operating-only, and 75 recency** events out of 643. With seven-day-old inputs, the refit full model surfaced **66** versus **75** for lagged recency. Confirm data availability before using a model queue.')
    st.caption('Failure-recency is a continuous score from the number of days since the last recorded failure. Missing earlier failures are conservatively represented as 365 days, so incomplete reporting remains a limitation.')
    event_cov=rob.get('event_coverage',{})
    caps=[25,50,100]
    recall=pd.DataFrame({'Weekly alerts':caps,
         'Full model':[100*event_cov.get(f'model_top{i}_event_recall_eligible',0) for i in caps],
         'Continuous failure recency':[100*adv.get('policies',{}).get(f'continuous_recency_top{i}',{}).get('event_recall',0) for i in caps],
         'Sensors + ops only':[100*event_cov.get(f'sensor_only_top{i}_event_recall_eligible',0) for i in caps]})
    fig=px.line(recall,x='Weekly alerts',y=['Full model','Continuous failure recency','Sensors + ops only'],markers=True,
                labels={'value':'Unique eligible events detected (%)','variable':'Ranking'})
    fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=360)
    st.plotly_chart(fig,use_container_width=True)
    st.caption('Event-level recall denominator: 643 distinct recorded failures with at least one eligible advance snapshot. Continuous failure-recency is used as the fairer comparator, with reproducible well-ID tie breaking. Catching ≠ preventing a failure.')
    months=rob.get('by_month',{})
    if months:
        mdf=pd.DataFrame([{'Month':k,**v} for k,v in months.items()])
        st.subheader('Stability across test months')
        fig=px.bar(mdf,x='Month',y='AP',text_auto='.3f',color_discrete_sequence=['#F4AC53'])
        fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=280)
        st.plotly_chart(fig,use_container_width=True)
    interval=adv.get('week_cluster_ap_difference_sensitivity',{}).get('percentile_95_interval')
    if interval: st.caption(f'18-week clustered AP-gap sensitivity interval versus continuous baseline: {interval[0]:.3f}–{interval[1]:.3f}. This is a descriptive resampling interval, not prospective certainty.')
    st.caption('Cohort audit found substantial differences in logged failure prevalence between low- and high-telemetry well-weeks. This can reflect equipment mix or reporting selection and requires field/well-type independent testing; do not compare raw AP across cohorts with different base rates.')
    st.warning('Temporal holdout evaluates previously observed wells, not new-well generalization. No probability calibration, prospective trial, or demonstrated maintenance benefit. Reporting practices may bias the labels.')

with tab_scenario:
    st.subheader('Business-impact sensitivity — hypothetical assumptions only')
    st.caption('Use this to discuss feasibility with judges; none of the default values are measured savings, actual market prices, or established intervention efficacy.')
    c1,c2,c3=st.columns(3)
    weekly_alerts=c1.slider('Inspections per week',5,100,25,5)
    actionable=c2.number_input('Assumed genuinely actionable events per week',min_value=0.0,max_value=30.0,value=3.0,step=0.5)
    oil_volume=c3.number_input('Assumed avoidable oil loss per event (m³)',min_value=0.0,max_value=500.0,value=20.0,step=5.0)
    d1,d2,d3=st.columns(3)
    addressable=d1.slider('Fraction of these events addressable',0,100,25,5)/100
    effectiveness=d2.slider('Assumed successful intervention rate',0,100,30,5)/100
    value=d3.number_input('Net realized oil value (CAD/m³), assumed',min_value=0.0,max_value=1500.0,value=400.0,step=25.0)
    cost=st.number_input('Assumed inspection cost (CAD/inspection)',min_value=0.0,max_value=10000.0,value=50.0,step=25.0)
    sim=scenario_weekly_gross_exposure(actionable,oil_volume,addressable,effectiveness,value,weekly_alerts,cost)
    a,b,c=st.columns(3)
    a.metric('Hypothetical protected volume/week',f"{sim['hypothetical_oil_m3']:.1f} m³")
    b.metric('Hypothetical gross value/week',f"CAD {sim['hypothetical_gross_value_cad']:,.0f}")
    c.metric('Hypothetical net/week',f"CAD {sim['hypothetical_net_cad']:,.0f}")
    required=break_even_success_rate(flagged_events_per_week=actionable,fraction_addressable=addressable,volume_per_event_m3=oil_volume,value_cad_per_m3=value,inspections_per_week=weekly_alerts,cost_cad_per_inspection=cost)
    if required is None: st.info('Break-even cannot be calculated with zero assumed benefit per successful action.')
    elif required>1: st.warning(f'Assumed intervention success needed to break even: {required:.1%}. Exceeds 100%; this scenario is not economically viable under its assumptions.')
    else: st.info(f'Assumed success rate needed to break even: {required:.1%}. This is a hypothetical threshold, not observed effectiveness.')
    st.caption('Formula: assumed actionable events × addressable fraction × success fraction × assumed oil volume/event × assumed realized CAD/m³ − inspections × assumed CAD/inspection. Does not include all operating costs or missed interventions.')
    rates=np.linspace(.0,1,21)
    sensitivity=pd.DataFrame({'Assumed intervention success rate':rates*100,
        'Hypothetical net CAD/week':[scenario_weekly_gross_exposure(actionable,oil_volume,addressable,r,value,weekly_alerts,cost)['hypothetical_net_cad'] for r in rates]})
    fig=px.line(sensitivity,x='Assumed intervention success rate',y='Hypothetical net CAD/week',markers=True)
    fig.add_hline(y=0,line_dash='dash',line_color='#F4AC53')
    fig.update_traces(line_color='#23C7C1')
    fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=330)
    st.plotly_chart(fig,use_container_width=True)
    st.info('To claim actual business benefits, Strathcona would need a prospective deployment with costs, control group/comparison, verified interventions and realized production measurements.')

with tab_method:
    st.subheader('Methodology & guardrails')
    st.markdown('''**Target.** Recorded well equipment failure starting 1–14 days after the end of the observed Sunday week.  
**Eligibility.** ≥6 observed days, ≥3 producing days, preceding consecutive observed week; excludes 14 days following a documented failure.  
**Features.** Two-week averages of production, water cut, downtime, losses and available pump readings; prior failure recency; calendar month.  
**Model.** Gradient-boosted tree (LightGBM) with early stopping and fixed hyperparameters.  
**Train.** 2025-06-01 through 2026-03-01.  
**Validation.** 2026-03-22 through 2026-05-17.  
**Test.** 2026-06-07 through 2026-10-04.  
**Holdout sample.** 22,580 eligible well-weeks; 1,015 positive well-week labels (4.50%).  
**Reporting.** Average precision, ROC-AUC, fixed-capacity precision and unique-event detection with eligibility denominator.''')
    st.error('**Data caveats:** (1) failure logs nearly absent until 2025, (2) recorded failures and maintenance entries closely coincide, (3) incomplete sensors and inconsistent values, (4) final repair costs and actions nearly unpopulated, (5) uncertain failure-logging consistency.')
    st.markdown('**Model drivers are mathematical contributions, not diagnosed mechanisms.** A field specialist must validate any suspected cause.')
    st.markdown('**Privacy:** restricted raw data and private individual-well results stay on the team computer. The public demo uses explicitly synthetic well records.')
    st.markdown('**Research references:** SPE PetroWiki on progressing cavity pump systems; SLB Defining Series on PCP equipment; the DSMLC official dataset handbook and briefing. See `docs/REFERENCES.md`.')
    st.markdown('**AI disclosure:** ChatGPT-assisted research, analysis, code drafting, app design, validation documentation and presentation/video materials. Registered team members must review, run, and verify the full project before submission.')

st.divider()
st.caption('DATA TITANS • Historical research prototype • Evidence over unsupported automation • 2026 DSMLC Datathon')
