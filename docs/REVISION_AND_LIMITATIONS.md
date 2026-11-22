# WellGuard AI — Revision and honest limitations ledger

| Judge concern | Revision | Status |
|---|---|---|
| Weak binary comparator, arbitrary ties | Continuous previous-failure recency; deterministic tie-break (well ID) | **Implemented and reproduced** |
| Historical well charts display future dates | Charts now apply selected snapshot date cutoff | **Fixed in source and tested in synthetic HTML**; Streamlit runtime still requires local test |
| Repeated inspections waste capacity | As-of no-repeat queue at 0/1/2-week cooldown | **Implemented; efficacy post-hoc only** |
| No event-lead-time interpretation | Earliest retrospectively flagged lead time included in aggregates | **Measured, not actionable guarantee** |
| Uncertainty in AP advantage | 750 week-cluster resamples of 18 test weeks | **Descriptive, not causal/prospective** |
| No true product interaction in video | Recorded actual synthetic UI clicks and inserted into new MP4 | **Implemented, team narrative review pending** |
| Mock interface in slide deck | Replaced with screenshot from tested app | **Done** |
| Financial benefit too speculative | Added explicit break-even, unrealistic scenario warning, prospective acceptance gates | **Implemented; ROI cannot be verified from source** |
| Default opening can expose restricted well IDs | Defaults to synthetic; explicit private acknowledgement gate | **Fixed in code** |
| Original-source PyArrow and live Streamlit run | Repeatable scripts plus Windows instructions and unit/browser QA | **OPEN: must run on approved team machine** |
| Sparse failure labels, selection bias | Model card and pilot plan; do not call old years failure-free | **Inherent dataset limitation, not resolvable without owner validation** |
| Missing actual costs/intervention outcomes | No claimed savings; hypothetical scenario only | **Inherent dataset limitation** |
| Missing telemetry / instrumentation-selection bias | Cohort audit by available pump channels; added channel count and low-coverage warning | **Observed, not resolved; requires field validation** |
| Missing field split and calibration | Acknowledge unverified generalization and uncalibrated scores | **Open research limitation** |
| Restricted data privacy | Public copy excludes raw files, well-level scores, weights; manual review required | **Automated check + human approval still required** |
| Final roster and video/GitHub link | Visible outstanding submission checklist | **OPEN: only registered team can confirm and publish** |

## Do not tell judges
- “We will prevent 40 extra failures” — **false**; we detected 41 additional *recorded* eligible events in retrospective test at the same weekly alert capacity.
- “The cooldown adds 27 proven detections” — **not independently validated**; policy explored on the same test period.
- “This is an 80.5% accurate model” — **false**; ROC-AUC is not accuracy.
- “Oil savings are $X” — **unproven**; scenario assumptions are not historical realized outcomes.
- “This is a live connected industrial platform” — **false**; this is a local, educational prototype.

## One-sentence defensible result
“On a chronological 18-week historical holdout, a fixed 25-review weekly queue flagged 116 of 643 eligible distinct *recorded* failure events, compared with 75 using continuous failure recency, before any prospective intervention or causal effect could be established.”

## Version 3 — judge-driven repairs

1. Fixed missing `rank` column in the Streamlit queue; the scheduler's `review_rank` is now used.
2. Fixed a chart-series name mismatch on the Streamlit validation tab.
3. Added signed TreeSHAP margin contributions in private replay where present, explicitly without causal diagnosis.
4. Added 19 passing automated tests including a full synthetic app-tab execution using an API stub (not a real Streamlit runtime).
5. Added a private original-source quality gate for pump-efficiency units, duplicate well-days and incomplete actual job costs. The gate awaits teammate execution with the authorized Parquet files.
The released operating-only model surfaces 111 events at 25 reviews/week versus 116 for the full model. With seven-day-old input features, the refitted model surfaces 66 versus 75 for lagged recency.
7. Reworked slide labels to describe a chronological holdout, updated the code bibliography and introduced a pre-registered prospective pilot plan.
8. Removed the white-flash artifact from the five-minute video and added extended screenshots of the synthetic interface while retaining a short actual click-through and AI narration as a team-review draft.

**Still unverified:** original Parquet run through standard PyArrow, actual Streamlit browser functionality, independent new data validation, prospective operational effectiveness, organizer-approved roster and publication. Do not score the project as fully production-ready.
