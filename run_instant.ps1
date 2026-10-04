Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Starting Smart Job Description Analyzer and Resume Optimizer" -ForegroundColor Green
Write-Host "(Instant Edition - Zero Downloads Required)" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

Set-Location -Path $PSScriptRoot

if (Test-Path "$PSScriptRoot\.venv\Scripts\python.exe") {
    & "$PSScriptRoot\.venv\Scripts\python.exe" standalone_app.py
} else {
    python standalone_app.py
}
