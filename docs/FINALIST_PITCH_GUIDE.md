# DATA TITANS — 10-minute finalist presentation plan

**Opening (0:00–0:40):** “If you have only 25 field reviews this week, which wells deserve them first?” Introduce WellGuard AI as an inspection prioritization study, not automated repairs.

**Problem + context (0:40–2:10):** What was provided; five million daily records; why early years' sparse failure logging prevents naive analysis. Equipment failures often coincide with maintenance records.

**Method (2:10–3:20):** Eligible producing-well Sundays, 14-day future recorded-failure labels, strictly past-only features, chronological train/validation/test, 18-week held-out period.

**Evidence (3:20–4:45):** LightGBM AP 0.164 versus continuous failure recency AP 0.103 (not accuracy). At 25 slots/week, 116 versus 75 eligible distinct recorded events out of 643. Explain both groups were subject to the same capacity and labels. No prevented failures implied.

**Live demo — SYNTHETIC only (4:45–7:00):** 25 to 50 alerts; 1-week cooldown; open as-of Well Investigator, highlight missingness and operational verification; change simulator success assumptions and reveal break-even. Clearly state that 142/643 cooldown count was observed post-hoc on the original test and requires new independent validation.

**Value and risks (7:00–8:40):** 25/week is an *illustrative* operating scenario, not validated company headcount. No real cost data or measured savings. Suggest a shadow pilot with business-as-usual comparison, field stratification, operator feedback, time to resolution, review hours and independently verified events.

**Close (8:40–10:00):** “The result is not a magic failure prediction. It's a reviewable, privacy-conscious process to choose investigations with a fixed workload.” Discuss model uncertainties and future operational pilot; invite questions.

## Prepared Q&A (3 minutes)

- **“Did you prevent 40 failures?”** No. We retrospectively flagged **41 additional recorded eligible events** over the stronger recency baseline; prevention was not measured.
- **“Why 25?”** It is an illustrative workload slider. A field pilot would derive capacity by staff, geography, skills and shift patterns.
- **“Does 0.164 mean 16.4% accurate?”** No. Average precision is a precision-recall summary. ROC-AUC 0.805 is also not accuracy.
- **“Did you tune the cooldown on test data?”** Yes, this was exploratory. We do not count the higher 142/643 as an independently proven improvement.
- **“How can an operator trust the AI?”** Every explanation points to observed inputs; the optional local language model is not a mechanical diagnosis, and a human operator authorizes action.
- **“Why no real ROI?”** The dataset lacks usable actual costs, intervention effectiveness, and causal production recovery outcomes.

**Rehearsal:** every registered member should present their own work and be able to explain how the two-week features and 14-day labels avoid future leakage.
