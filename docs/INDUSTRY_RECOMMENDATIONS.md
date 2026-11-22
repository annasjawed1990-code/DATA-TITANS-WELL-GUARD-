# Industry implementation and feasibility plan

## Research question
**Can two weeks of well operating measurements and previously observed failures help prioritize producing wells for inspection before a *recorded equipment failure* in the next 14 days?**

## What is currently demonstrated
A chronological retrospective test of 22,580 eligible well-weeks shows LightGBM AP 0.164 versus a stronger continuous failure-recency benchmark AP 0.103, with 116 versus 75 eligible events flagged at 25 weekly review slots. A weekly capacity of 25 is a **scenario**, not Strathcona's verified operational headcount. This scenario flagged 115 of the 643 recorded failure events with eligible prior snapshots. This is a ranking study; it is not proof of operating savings or of preventable failure events.

## Workflow proposal
1. **Data QA**: normalize timestamp zones and telemetry coverage; check device availability, downtime codes, duplicate well-days and event chronology.
2. **Weekly scoring**: produce scores at a Sunday snapshot using prior observations only; retain execution version and feature quality flags.
3. **Queue triage**: limit to 25, 50, or 100 wells per week, by available field-engineer capacity; compare field-specific alert workload with site needs.
4. **Evidence review**: show oil-rate, downtime, RPM, torque, electrical current, previous maintenance details, and missing-sensor indicators.
5. **Field adjudication**: engineers investigate the queue and decide whether or when to inspect; never let the prototype change pump settings.
6. **Feedback collection**: record actual inspection, observed fault, deferred intervention, safety issues, false alerts and realized production outcomes.
7. **Prospective shadow trial**: compare fixed-capacity operator response against documented business-as-usual, with independent outcome adjudication.

## Business case
The available `lost_oil_m3` is a **source-generated historical estimate**, not necessarily directly caused by equipment failures and **not** a measurement of preventable production. `field_est_total` records estimates of job costs and is not actual spending.

The app's simulator is a user-input thought experiment:

`hypothetical weekly net = (assumed actionable events/week × addressable fraction × successful intervention fraction × avoidable volume/event × assumed realized CAD/m³) − (weekly inspections × assumed CAD/inspection)`

Every input is labeled assumed. A pilot would require actual intervention records, well-specific oil netbacks, contractor/travel costs, operating constraints, and comparisons to normal maintenance operations. Do not use the simulator's default results as a projected savings forecast.

## Governance and deployment
- Keep the real dataset on approved team/company machines; restrict access; do not deploy raw data to public cloud.
- Perform field/well-type stratification to avoid bias toward instrumented wells.
- Track drift, false-alarm burden, missing inputs, and model sensitivity to maintenance-linked variables.
- Document an operator escalation policy, not an autonomous control action.
- Review maintenance recommendations for worker and process safety; establish authority boundaries.
- Export aggregated KPIs and privacy-preserving demo data only when disclosure is permitted.

## Optional platform integration
Canary is optional, not required for the overall award. If time permits, architecture could integrate a historian signal feed and Axiom review dashboard, but no live Canary connection has been built or verified. This is **not** a Canary award submission as delivered.

## Scheduling upgrade and workload reality
- The 18-week evaluation has **450 nominal review slots** at 25 per week. The standard model revisits some wells: 184 unique wells were selected across those slots.
- An optional 1-week no-repeat rule explores reducing duplicate reviews; event detection rose from 116 to 142 in the *same retrospective test*, but **this was selected after observing the holdout**. Treat it as an operational hypothesis only; validate prospectively.
- A valid field pilot must define real inspection capacity by geographic area, technician skills, travel time, site access, preventive maintenance windows, and emergency overrides. We did not optimize travel or verify field locations.
- Budget model break-even success fraction = `(weekly inspections × cost per inspection) / (assumed actionable events × addressable share × avoidable m³/event × realized CAD/m³)`. Values above 100% indicate that the hypothetical scenario cannot break even under its inputs. This formula excludes unmeasured implementation and opportunity costs; it is **not an ROI estimate**.

## Acceptance gates for a responsible pilot
1. Validate labels and reporting coverage directly with Strathcona; distinguish maintenance work orders from actual failure onset.
2. Audit prediction performance by well equipment type, field and telemetry availability; exclude cohorts for which the score is unreliable.
3. Independently reproduce all source-to-score steps and freeze the model, scheduler and alert thresholds before a fresh test.
4. Conduct a no-intervention *shadow trial* to measure alert workload, verified event recall and operator usefulness under real field constraints.
5. Only then evaluate a controlled intervention trial with actual findings, elapsed travel/work hours, real costs, and before/after production net of confounders.
