# Prospective validation and business pilot protocol (proposed, NOT executed)

**Objective.** Determine whether the previously frozen WellGuard ranking is useful for selecting **25 review candidates per week** relative to an equally resourced operating-data-only model and the continuous failure-recency baseline. No field deployment or realized savings is asserted.

## Phase A — label audit (requires authorized data-owner input)
1. Define independently adjudicated *equipment failure onset*, failure severity, work-order linkage, false-positive process and missing failure records. Specifically investigate why historical failure reporting is sparse before 2025 and why many recorded failures coincide with maintenance jobs.
2. Stratify by artificial-lift class, well type, sensor availability, field and recording completeness. The pilot's eligible population cannot be assumed to cover all 2,905 wells.
3. Evaluate the pump-efficiency unit ambiguity: the handbook describes a fractional measure but many non-missing values exceed 1.0. The private `scripts/09_source_quality_gate.py` records prevalence, quantiles and conflicts. Never silently treat values above 1 as valid fractions or percentages without owner confirmation.
4. Freeze input columns, as-of cutoffs, label rules, missing-data policy, scoring frequency and model version before assessing new outcomes.

## Phase B — 8–12-week prospective shadow evaluation
- Use **no operational changes** on the basis of research model output. Restrict display to authorized personnel.
- On the same weekly cut-off, freeze top-25 lists from (i) the full LightGBM, (ii) the operating-only variant and (iii) continuous failure-recency, each with deterministic ties; do not retrospectively alter lists.
- Store file hashes, cutoff timestamps, missing-sensor coverage, candidate list, model version and subsequent independently adjudicated event labels.
- Primary metric: *distinct failure-event recall at fixed 25-review/week capacity*, calculated with a documented eligible-event denominator and advance horizon of days 1–14.
- Secondary: positive well-week precision, precision/alert by cohort, avoidable repeat reviews, review time, false-alert burden, median warning lead time, operator acceptance and calibration only if separately tested.
- Report statistical uncertainty by week and, if possible, well/field. Distinguish events from alert-positive well-weeks; a single weekly selection can correspond to multiple events.
- Evaluate any repeat-review cooldown on a **future untouched period** or through an up-front selection policy. Prior 142/141-event observations were post-hoc and should not be promoted as verified gains.

## Phase C — controlled field pilot (only with owner authorization)
- Define interventions by qualified field staff, severity and risk constraints, baseline inspection policy and required safety approvals.
- Compare the same inspection-hours budget with an approved comparator; log all operator decisions, extra inspections, false alerts, reported work, direct costs, actual production recovery and missed-event reviews.
- Measure realized business value from **observed** intervention costs, verified outcomes and an appropriate counterfactual. An inspection alert does not by itself prevent a failure.

## Transparent economic example (fully hypothetical)

At **25 inspections/week**, **CAD 50 assumed cost/inspection**, **3 assumed candidate events/week**, **25% addressable**, **20 m³ assumed avoidable oil/event**, **CAD 400 assumed net value/m³**, and **30% assumed successful interventions**:

- Assumed inspection spend: `25 × CAD 50 = CAD 1,250/week`.
- Hypothetical gross value: `3 × 25% × 30% × 20 m³ × CAD 400 = CAD 1,800/week`.
- Hypothetical net: `CAD 550/week`; break-even success rate `1,250 / (3 × .25 × 20 × 400) = 20.8%`.

**None of these prices, volumes, intervention rates, or cost assumptions is observed for Strathcona.** The economic calculation is a sensitivity scenario, not an ROI prediction.

## Pre-registered decision rule
Prioritize whichever policy meets data-owner feasibility and the pre-specified fixed-capacity event-recall/alert-burden criteria on **new prospective data**. Do not choose a model solely because it has the highest global AP, nor switch models based on the 2026 holdout after inspecting its outcomes.
