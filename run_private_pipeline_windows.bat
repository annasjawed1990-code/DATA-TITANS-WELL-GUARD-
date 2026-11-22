@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ===========================================================
echo DATA TITANS - PRIVATE WELLGUARD REPRODUCTION

echo ONLY RUN ON AUTHORIZED COMPUTER; DO NOT SHARE OUTPUTS
echo ===========================================================

for %%F in (daily_production.parquet well_jobs.parquet production_failures.parquet) do (
  if not exist "data\%%F" (
    echo MISSING: data\%%F
    echo Copy the original competition data to a local data folder.
    pause
    exit /b 2
  )
)
if not exist ".venv\Scripts\python.exe" (
  py -3.12 -m venv .venv
  if errorlevel 1 py -3 -m venv .venv
  if errorlevel 1 (echo ERROR: Python 3.11 or 3.12 required.&pause&exit /b 3)
)
call ".venv\Scripts\activate.bat"
python -m pip install -r requirements.txt
if errorlevel 1 (echo ERROR: Dependency installation failed.&pause&exit /b 4)
if not exist outputs mkdir outputs

echo [1/9] Inspecting source value and duplicate quality...
python scripts\09_source_quality_gate.py --data-dir data --out-dir outputs > outputs\private_run_log.txt 2>&1
if errorlevel 1 goto fail

echo [2/9] Auditing original Parquet data...
python scripts\01_data_audit.py --data-dir data --out-dir outputs >> outputs\private_run_log.txt 2>&1
if errorlevel 1 goto fail

echo [3/9] Training and evaluating model...
python scripts\02_failure_ranking.py --data-dir data --out-dir outputs >> outputs\private_run_log.txt 2>&1
if errorlevel 1 goto fail

echo [4/9] Adding strictly past-only maintenance context...
python scripts\03_private_history_context.py --data-dir data --out-dir outputs >> outputs\private_run_log.txt 2>&1
if errorlevel 1 goto fail

echo [5/9] Computing enhanced benchmark and scheduling sensitivity...
python scripts\05_advanced_validation.py --data-dir data --out-dir outputs >> outputs\private_run_log.txt 2>&1
if errorlevel 1 goto fail

echo [6/9] Checking expected historical results...
python scripts\06_verify_reproduction.py --out-dir outputs >> outputs\private_run_log.txt 2>&1
if errorlevel 1 goto fail

echo [7/9] Auditing sensor-coverage selection...
python scripts\07_cohort_robustness.py --out-dir outputs >> outputs\private_run_log.txt 2>&1
if errorlevel 1 goto fail

echo [8/9] Unit tests...
python -m unittest discover -s tests -v >> outputs\private_run_log.txt 2>&1
if errorlevel 1 goto fail

echo [9/9] Checking app logic using synthetic records...
python scripts\08_app_logic_smoke.py >> outputs\private_run_log.txt 2>&1
if errorlevel 1 goto fail

echo SUCCESS: Private source-to-score verification and app logic smoke passed.
echo Source and well-level outputs remain under gitignored data/ and outputs/.
echo Read outputs\private_run_log.txt and review the confidential app locally.
python -m streamlit run app.py
exit /b 0

:fail
echo FAILED. Check outputs\private_run_log.txt for error details.
echo Do not claim end-to-end verification or publish this output.
pause
exit /b 5
