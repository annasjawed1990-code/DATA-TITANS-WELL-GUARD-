@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    py -3.12 -m venv .venv
    if errorlevel 1 py -3 -m venv .venv
)
call ".venv\Scripts\activate.bat"
python -m pip install -r requirements.txt
if errorlevel 1 (echo Setup failed. Check your internet/Python version.&pause&exit /b 1)
python -m streamlit run app.py
pause
