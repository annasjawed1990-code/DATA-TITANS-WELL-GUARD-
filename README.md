# WellGuard AI · DATA TITANS

WellGuard ranks producing oil wells for a weekly maintenance review. We ask whether a 14-day recorded equipment-failure ranking surfaces more events than a rule based on time since the previous recorded failure, using the same number of review slots.

**Registered team members** · Add the confirmed organizer roster and contribution credits before submitting.

## Historical results

| Weekly reviews | Full LightGBM | Operating-only | Continuous failure recency |
|---:|---:|---:|---:|
| 25 | 116 | 111 | 75 |
| 50 | 180 | 172 | 114 |
| 100 | 289 | 267 | 188 |

Counts are distinct recorded events with at least one eligible preceding snapshot. The denominator is **643 eligible events** across 18 holdout weeks, including 22,580 well-weeks and 1,015 positive well-weeks. At 25 per week each policy spends 450 review slots. The full model's advantage over recency is **6.4 percentage points** of event recall. The descriptive paired 14-day event-date block interval is **4.1–8.3 percentage points**. The full model's AP is **0.164**, versus **0.103** for recency and **0.148** for operating-only. AP summarizes precision and recall across ranking thresholds.

**Data availability changes the decision.** With features aged seven days and a refitted model, the 25-slot model surfaced **66** events versus **75** for lagged recency. This sensitivity keeps the same cohort and future targets and changes the available feature history. It does not validate cohort eligibility itself under a delay. At 50 and 100 slots, the lagged model surfaced 133 and 223 events versus 114 and 188 for lagged recency. A shadow trial should establish actual data arrival times and test recency as a fallback at low capacity.

## Deliverables

- [Interactive offline demonstration](demo/WellGuard_AI_Interactive_Offline_Demo.html) · Download and open in a browser. Per-well records are synthetic.
- [Presentation PDF](presentation/DATA_TITANS_WellGuard_AI_Competition_Deck.pdf) and [editable slides](presentation/DATA_TITANS_WellGuard_AI_Competition_Deck.pptx).
- [Five-minute summary video](media/DATA_TITANS_WellGuard_AI_5min.mp4). Check the final published link while signed out.
- [Model card](docs/MODEL_CARD.md), [pilot protocol](docs/PROSPECTIVE_PILOT_PROTOCOL.md), [references](docs/REFERENCES.md), and [AI disclosure](AI_ASSISTANCE_DISCLOSURE.md).

## Run the app

Use Python 3.12. Set up an environment, then run:

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The default is the synthetic demonstration. The private replay becomes available after the restricted-data pipeline generates private outputs. Keep it on an authorized local machine.

## Reproduce the benchmark

Place the three official Parquet files in the gitignored `data/` directory in a separate authorized copy, or use an explicit private data path. Keep all outputs local. Windows users can use `run_private_pipeline_windows.bat`.

```sh
python scripts/09_source_quality_gate.py
python scripts/01_data_audit.py
python scripts/02_failure_ranking.py
python scripts/03_private_history_context.py
python scripts/05_advanced_validation.py
python scripts/06_verify_reproduction.py
python scripts/07_cohort_robustness.py
python -m unittest discover -s tests -v
```

The source benchmark verifies the delivered code, including the operating-only variant and seven-day input-delay test. Each comparator uses the same decision snapshots, target horizon, capacities, and deterministic tie-break. The [source benchmark](results/source_benchmark.json) and [advanced validation](results/advanced_validation_public.json) contain aggregate results only.

## Methods and limitations

Daily production becomes Sunday-ending well-weeks. Eligible snapshots have at least six observed current-week days, at least three producing days, a preceding calendar week, and no recorded failure in the previous 14 days. The model uses trailing operating measures and failure recency. The operating-only model drops month and both failure-history features. Jobs provide context in the app. Date-based cutoffs do not establish when a record first became available.

The first split trains through March 1, 2026. Validation runs March 22 through May 17. The holdout runs June 7 through October 4. Pre-2025 failure coverage is sparse, scores are uncalibrated, and the 14-day replay evaluates recorded events. The repeated-well sample does not establish new-field generalization. Cooldown is an exploratory policy. No intervention effect or realized savings was measured.

## Submission

Confirm registered members, provenance and disclosure. Review the final public commit history and release for restricted records, verified permissions, and access to the video and slides. Submit the public GitHub link in the datathon Discord `#submissions` channel before **Sunday, November 22 at noon Calgary time**.
