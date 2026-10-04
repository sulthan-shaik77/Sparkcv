@echo off
cd /d "%~dp0"
echo ========================================================
echo Starting Smart Job Description Analyzer and Resume Optimizer
echo (Instant Edition - Zero Downloads Required)
echo ========================================================

if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" standalone_app.py
) else (
    python standalone_app.py
)
pause
