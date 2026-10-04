@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo ========================================================
echo Starting Smart Job Description Analyzer and Resume Optimizer
echo ========================================================

if not exist ".venv\Scripts\python.exe" (
    echo Setting up Python virtual environment...
    python -m venv .venv
)

"%~dp0.venv\Scripts\python.exe" -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo Installing dependencies into the virtual environment...
    set "UV_CMD="
    if exist "%USERPROFILE%\.local\bin\uv.exe" set "UV_CMD=%USERPROFILE%\.local\bin\uv.exe"
    if not defined UV_CMD (
        where uv.exe >nul 2>&1 && set "UV_CMD=uv"
    )

    if defined UV_CMD (
        echo Using high-speed uv installer
        set UV_CONCURRENT_DOWNLOADS=1
        "!UV_CMD!" pip install -r requirements.txt --python "%~dp0.venv\Scripts\python.exe"
    ) else (
        echo Using standard pip installer
        "%~dp0.venv\Scripts\python.exe" -m pip install -r requirements.txt
    )
)

echo Launching Streamlit web application...
"%~dp0.venv\Scripts\python.exe" -m streamlit run "%~dp0app.py"
if %errorlevel% neq 0 (
    echo.
    echo Streamlit exited with code %errorlevel%.
)
pause
