# START HERE — DATA TITANS WellGuard AI

## 1. Demonstrate the project safely (no installation required)

Open `demo/WellGuard_AI_Interactive_Offline_Demo.html` in Chrome or Edge. Every displayed **well ID, trace and individual score is synthetic**. The statistical aggregates are separately reported results from the restricted competition study.

Show: **Inspection queue → set 25 then 50 slots → apply 1-week cooldown (exploratory) → click a well → Impact simulator → change success rate.** The as-of investigation must not display later observations. Do not imply that simulated profiles are real Strathcona wells.

## 2. Review the five-minute video

`media/DATA_TITANS_WellGuard_AI_5min.mp4` contains actual browser-recorded UI clicks, synthetic dashboard visuals, and AI-generated narration. This is a **team-review draft**, not proof of final submission. Confirm every figure and record team narration if possible.

## 3. Reproduce with private original files (Windows)

Use a **different, approved local folder** from the GitHub public copy. Put the provided files in `data/`:

- `data/daily_production.parquet`
- `data/well_jobs.parquet`
- `data/production_failures.parquet`

Double-click **`run_private_pipeline_windows.bat`**. It installs dependencies, audits data, trains and validates, enriches historical as-of context, runs tests and opens the private app. Everything under `data/` and `outputs/` is strictly private.

If Python is already installed, use a terminal from project root and follow the README commands. Do not upload real UWI screenshots, output CSVs, job histories or model weights to GitHub or a hosted AI service.

## 4. Before GitHub publishing

The default Streamlit mode is **Synthetic demo**. Do not publish the private working directory. Publish only the clean public ZIP created for the competition; run `python scripts/04_publication_preflight.py` and inspect all staged files manually.

Confirm: registered team members, AI credit, 5-minute video accessibility, slide claims and deadline. The model has not been prospectively validated and no operational savings have been measured.
