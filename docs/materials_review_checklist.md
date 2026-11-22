# DATA TITANS — Datathon 2026 Materials Review Checklist

**Audit date:** November 20–21, 2026  
**Source:** `DSMLC Datathon 2026 Materials-20261121T013108Z-1-001.zip`  
**Package integrity:** Passed ZIP CRC integrity check; nine files (no missing/corrupt archive entries).

## A. File-by-file review register

- [x] **Briefing Document.pdf** — 10 pages, read in full. Reviewed eligibility, registered team contributions, AI disclosure, original work, challenge statement, permitted solution forms, deliverables, submission route, deadline, finalist judging, prizes, and dataset restrictions.
- [x] **Dataset Handbook.pdf** — 11 pages, read in full. Reviewed data grain, heavy-oil/PCP domain definitions, all three schemas, UWI join key, units, sample values, and contextual external resources.
- [x] **Research Topic Guide.pdf** — 5 pages, read in full. Reviewed eight suggested research directions, how to construct a research question, and supplementary public data resources.
- [x] **Canary Setup Troubleshooting Guide.pdf** — 4 pages, read in full. Reviewed Windows-only setup, licensing, time-zone issue, C: install guidance, API token creation, and common errors.
- [x] **Canary Install Guide Windows x86.docx** — 61 paragraphs and 18 embedded screenshots, installation text reviewed. Reviewed Windows 10/11 prerequisites, installer customization, Identity/License choices, login, four-component activation, repair/uninstall.
- [x] **Canary Labs Intro & Setup Guide.mp4** — 2:49.5, H.264 1280×720 with audio. Sampled screen frames across the recording; visually identified Axiom examples, installation steps, Canary Admin sign-in and licensing. **Spoken narration was not transcribed; not a full audio audit.**
- [x] **daily_production.parquet** — verified Parquet integrity marker, schema (41 columns), footer row count (5,075,590), row-group structure (5 groups), field-level null counts, type metadata and min/max statistics. **Full row-wise EDA, unique-well verification, duplicate detection, and plots remain pending.**
- [x] **well_jobs.parquet** — verified Parquet marker, schema (19 columns), row count (15,610), event field metadata and null statistics. **Full row-wise exploration and cross-file joining remain pending.**
- [x] **production_failures.parquet** — verified Parquet marker, schema (18 columns), row count (2,873), field completeness and date ranges. **Full event coding and label-validation remain pending.**

**Review status:** Five written documents reviewed in full; video visually sampled; three Parquet files structurally profiled through embedded metadata. A complete row-by-row analytics audit has **not** yet been performed.

## B. What the official briefing requires

- [x] Challenge theme is **Optimization**; team defines its own specific measurable research question from the Strathcona production, failure, and maintenance data (Briefing, p. 6).
- [x] Solution may be an analytical dashboard, an AI/ML prototype, or a data-driven implementation/recommendation plan (Briefing, p. 4).
- [x] Required submissions are presentation/slides, **five-minute** summary video, and source code (Briefing, pp. 4–6).
- [x] Submit a **public GitHub repository URL** to the Discord **#submissions** channel by **Sunday, November 22, 2026, 12:00 PM**; late submissions disqualified (Briefing, p. 6).
- [x] Repository must contain title, team member names, research question, motivation, summary findings, appropriate code/files, video link, slides, methods, validation, external resources, and AI disclosure (Briefing, p. 6).
- [x] **All AI-generated work must be disclosed and credited**; team understands and verifies technical claims and code (Briefing, p. 3).
- [x] Original work during competition; **only registered team members may contribute**; teams are 2–4 people (Briefing, p. 3).
- [x] Competition dataset may be used **only for this datathon**, without permission for other distribution/use (Briefing, p. 10). **Do not commit raw Parquet data to a public repo.**
- [x] Sunday in-person attendance mandatory; finalists have **10 minutes presentation + 3 minutes Q&A** (Briefing, p. 5).
- [x] Finalist judging rubric: **25% research/domain**, **25% technical/correctness**, **20% business impact**, **15% communication**, **15% creativity** (Briefing, pp. 8–9). The document does not state an identical numerical rubric for the preliminary stage.
- [x] Canary and Databricks are **optional**; Canary enables eligibility for a separate **$250 CAD Best Use of Canary** award (Briefing, p. 7).

## C. Independently confirmed dataset facts (Parquet footers)

| File | Rows (verified) | Columns (verified) | Date range (verified from metadata) |
|---|---:|---:|---|
| daily_production.parquet | 5,075,590 | 41 | 2021-01-01 through 2026-10-27 |
| well_jobs.parquet | 15,610 | 19 | Start dates 2021-01-01 through 2026-10-27 |
| production_failures.parquet | 2,873 | 18 | Failure starts 2021-12-14 through 2026-10-26 |

The **2,905 distinct wells in production, 1,903 in jobs, and 825 in failures** are from the **Dataset Handbook**, not independently verified by scanning row values. The Parquet row counts and field counts match the handbook exactly.

## D. Important data-quality findings from file metadata

- **Failure log sparsity:** `failure_end_date`, `action_taken`, and `cause_comments` each have only **1 populated row** out of 2,873; `failure_system` has only **3 populated rows**, and `failure_description` has **21**.
- **Job costs:** `actual_final_job_cost` has only **1 populated row** out of 15,610. `field_est_total` is populated on all rows but includes negative values; treat as estimated, not actual expenditure. AFE cost fields each have **775 non-null rows**.
- **Pump sensor coverage:** in the 5,075,590 production records, `pcp_pump_rpm` is **52.5% null**, `pump_efficiency_pct` **66.8% null**, `pcp_pump_rod_torque_ftlb` **74.0% null**, and motor current **82.2% null**. Missingness can reflect well type or operational state; do not interpret all nulls as errors.
- **Other production fields:** `lost_oil_m3` is **67.5% null**; `oil_produced_m3` is **23.1% null**; `tubing_pressure_kpa` is **47.4% null**. The handbook explicitly warns of `999999` placeholder pressure readings.
- **Implausible/edge values in metadata:** `pump_efficiency_pct` runs from approximately **-17.5 to 91.43** even though handbook says the unit is a decimal proportion. `tubing_pressure_kpa` reaches **999999**. Oil production has negative entries (minimum approximately -163.92 m³). `job_duration_days` ranges from about **-111.54 to 473**, and `field_est_total` includes negative figures. Must clean and explain rather than discard indiscriminately.
- **Join grain:** production is **well × day**, whereas jobs and failures are **events**. Joining event logs to daily rows without event-aware aggregation or time windows can duplicate observations and leak future information.
- **Label availability:** failure record starts are available, but end dates and action outcomes are nearly absent. A time-to-failure/7–14 day prediction task is possible to investigate, **not yet proven feasible or reliable**.
- **Canary installation guidance conflict:** Word guide demonstrates selecting a D: installation, while the troubleshooting guide specifically recommends default C: paths based on actual failures. Prefer the corrected troubleshooting guidance, and ask organizers if using Canary.
- **Setup dependency gap:** troubleshooting instructions mention a 'Starter EDA' folder and `requirements.txt`, but neither exists inside this nine-file archive.

## E. Preliminary work strategy (not yet executed)

- [ ] Install/enable a Parquet reader in a suitable environment (e.g., local Python with `pyarrow`/DuckDB). This audit environment lacked those readers, so only metadata was queried.
- [ ] Verify well IDs, distinct well counts, well-day uniqueness, overlap of the three files, and repeated failure/job records.
- [ ] Create profiling tables by well type, status, operating area, and year; investigate sensor coverage conditional on actual production and PCP use.
- [ ] Investigate failure type/cause frequencies and timing, maintenance-date relationship, and days of observed production history before events.
- [ ] Evaluate several **candidate research questions** objectively; choose only after establishing measurable outcomes and label quality.
- [ ] Construct leakage-safe time-based validation and simple baselines before complex ML.
- [ ] Build a working solution with visible explanations, honest uncertainty, business prioritization, and realistic cost assumptions.
- [ ] Record five-minute demo, test the public repository without uploading restricted data, and prepare slides/documentation/AI disclosures.
- [ ] Rehearse ten-minute finalist presentation and three-minute technical Q&A.

## F. Additional reference material (separate from competition ZIP)

- `Enbridge-Case-Competition-main.zip` — source archive available (224 entries); previously reviewed as an example of a winning predictive maintenance / anomaly detection system.
- `cochrane-mobility-analysis-master.zip` — source archive available (40 entries); previously reviewed as an example of analytical storytelling, GIS, and operational recommendations.

**Decision gate:** Before committing to predictive maintenance or any specific model, complete the row-level profiling and test whether event labels support a valid prediction horizon and operationally useful precision/recall.
