# One-click runner for the Tkinter desktop app (Windows PowerShell)
# Usage: .\run_desktop.ps1
# Optional: .\run_desktop.ps1 -ApiUrl http://localhost:8000/api

param(
    [string]$ApiUrl = "http://localhost:8000/api"
)

$ErrorActionPreference = "Stop"

Write-Host "Student Management System (Tkinter Desktop)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Ensure Python exists
python --version | Out-Null

# Create venv if missing
if (-not (Test-Path "./desktop_app/.venv")) {
    Write-Host "[INFO] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv ./desktop_app/.venv
}

# Activate venv
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
. .\desktop_app\.venv\Scripts\Activate.ps1

# Install deps
Write-Host "[INFO] Installing dependencies..." -ForegroundColor Yellow
pip install -r .\desktop_app\requirements.txt

Write-Host ""
Write-Host "[INFO] Running desktop app..." -ForegroundColor Yellow
python -m desktop_app.app --api $ApiUrl
