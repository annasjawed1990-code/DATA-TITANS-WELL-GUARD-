# WellGuard AI — Model Card

## Intended use
Educational prototype for retrospective weekly **inspection queue ranking** of eligible producing wells, using a 14-day equipment-failure recording horizon. Not approved for automatic interventions, emergency alarms, or real-world maintenance authorization.

## Training target
Documented equipment failure with a start date **1 to 14 days after Sunday snapshot**. Failure labels are taken from `production_failures.parquet`; this is a **recorded failure** outcome, not guaranteed actual failure incidence.

## Features
Two-week production and operating summaries including downtime, oil rate, estimated historical losses, water cut, pump RPM, torque, current, efficiency, days producing, earlier failure history, and month. No *future* maintenance actions, future downtime, or future observations may be used as predictors. Certain features, including downtime and historical failure documentation, may correlate with the reporting process itself.

## Sampling criteria
At least 6 reported days in the current week, at least 3 days classified as producing; prior consecutive observed week; exclude 14 days after a documented failure. Wells not meeting these criteria are not scored. Missing pump sensors remain missing, allowing LightGBM to route missing values.

## Time partitions
Train: 2025-06-01–2026-03-01; validation: 2026-03-22–2026-05-17; test: 2026-06-07–2026-10-04. Weeks between partitions guard against labels overlapping a split boundary.

## Test metrics (from re-executed intermediate-data pipeline)

- Eligible test observations: 22,580 well-weeks, 1,015 positive labels (4.50%).
- LightGBM average precision: **0.1636889**; ROC-AUC: **0.8054624**.
- **Stronger continuous failure-recency comparator AP: 0.1029886**, ROC-AUC 0.7242529. A binary prior-90-day-failure flag achieved AP 0.0769253 but causes extensive tied queues and is not the headline comparator.
- Operating-conditions-only ablation AP: **0.1476328**.
- Top-25 alerts each week: **24.89%** positive well-weeks (do not confuse with independent events).
- Eligible distinct failure events: 643; model top-25 event coverage 116/643 (**18.04%**); continuous recency baseline 75/643 (**11.66%**), reproducibly tie-broken by stable well identifier.
- The holdout includes existing wells only; there has been no unseen-well, field-holdout, or prospective trial.

## Fixed-workload scheduling and reliability checks
- Ranking uses deterministic descending score, followed by ascending well identifier to resolve ties.
- 25 review slots/week × 18 retrospective weeks = 450 well-week review opportunities. Standard ranking touched **184 different wells**; the stronger recency baseline touched **323 wells**.
- At that workload, **116/643** events were retrospectively flagged by WellGuard versus **75/643** for continuous recency: **41 additional eligible recorded events**, not avoided failures.
- The **1-week and 2-week cooldown** variants yielded 142/643 and 141/643, respectively, but are **post-hoc sensitivity analyses on the same test data**. They are not independently validated policy gains. The default queue remains no cooldown.
- 750 week-cluster bootstrap resamples of the 18 holdout weeks gave a **descriptive 95% AP-difference interval of 0.044–0.077** against continuous recency (point difference 0.0609). These are not independent-well or prospective confidence intervals.
- The selected events had a median earliest lead-time of **5 days** at 25/week, evaluated retrospectively against recorded event dates; this is not guaranteed actionable notice.

## Not demonstrated
No calibration, counterfactual outcome, prospective forecast, production uplift, avoided failure, avoided downtime, or confirmed operational savings. The model score should **not** be presented as a probability of failure. Events may appear in multiple adjacent weekly labels.

## Main risks
1. Failure logs are nearly absent in 2021–2024; apparent rate shift in 2025 likely reflects reporting change or scope differences.
2. Failures and maintenance jobs are frequently co-dated; documentation patterns could contaminate the target.
3. Telemetry missingness is associated with well types and instrumentation configurations. A private cohort audit by available pump channels found dramatically different recorded-failure prevalence; a zero-channel cohort contained very few positive labels. **Do not apply fleet-wide without field/equipment-type evaluation and coverage-aware review.**
4. Data defects and outliers include negative values, placeholder pressures, and inconsistent pump-efficiency scale.
5. Actual final maintenance costs and actions taken are nearly absent.
6. Operating measurements are historic weekly aggregates, not continuously observed real-time sensor signals.

## Further validation priorities
Audit labeling by field and well type; perform separate field/well-cohort holdout, calibration and event-recall review; verify underlying operational log semantics; run prospective shadow deployment; log interventions and measure outcomes with proper comparisons.

## Privacy
No competition raw Parquet files, identifiable per-well predictions, private model files or trained weights should be published. Local individual-well outputs stay in `outputs/`, protected by `.gitignore` and the preflight script.

## Telemetry-coverage stress test (internal, not causal)
A new reproducible `scripts/07_cohort_robustness.py` script evaluates 0, 1–2 and 3–4 recorded pump channels per eligible well-week. The recorded positive rate differs sharply across cohorts, so aggregate discrimination may reflect instrumentation or reporting selection, not solely equipment deterioration. The zero-channel cohort has only a handful of recorded positives and must not be described as reliably evaluated. We keep the detailed cohort counts private pending data-rights review.

## Release audit: fixed-capacity model trade-off

- The operations/sensors-only model has **AP 0.1476** and flags **111/643** distinct eligible events at 25 review slots/week, versus **116/643** for the full LightGBM and **75/643** for continuous failure recency.
- The full model does **not** dominate all decision metrics; it has better overall AP and event coverage at 50 and 100 reviews/week. Choosing a policy because of its 25-slot performance on this same previously held-out period would be post-hoc.
- The private quality-gate script flags ambiguous pump-efficiency units and conflicting duplicate well-day observations for owner review. No assertion of correct unit conversion has been made.
- **Future validation requirement:** freeze the competing model versions and fixed-capacity policies before evaluating on new events.

## Input availability sensitivity

The seven-day delay ages production features and the failure-history cutoff. Calendar month, snapshots, eligibility, and targets are unchanged so the comparison isolates the effect of feature staleness. At 25 weekly slots the delayed model surfaced 66 distinct recorded events against 75 for delayed recency. The normal-input uplift over recency was 6.4 percentage points, with a descriptive paired event-date block interval of 4.1–8.3 points. A live deployment needs actual posting timestamps.
