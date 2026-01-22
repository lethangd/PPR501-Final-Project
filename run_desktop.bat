@echo off
REM One-click runner for the Tkinter desktop app (Windows CMD)
REM Usage: run_desktop.bat
REM Optional: set API_URL before running
REM   set API_URL=http://localhost:8000/api

setlocal

if "%API_URL%"=="" set API_URL=http://localhost:8000/api

echo Student Management System (Tkinter Desktop)
echo ============================================
echo.

REM Ensure venv exists
if not exist "desktop_app\.venv" (
  echo [INFO] Creating virtual environment...
  python -m venv desktop_app\.venv
  if errorlevel 1 (
    echo [ERROR] Failed to create venv. Is Python installed and on PATH?
    pause
    exit /b 1
  )
)

call desktop_app\.venv\Scripts\activate.bat

echo [INFO] Installing dependencies...
pip install -r desktop_app\requirements.txt
if errorlevel 1 (
  echo [ERROR] Failed to install dependencies.
  pause
  exit /b 1
)

echo.
echo [INFO] Running desktop app...
python -m desktop_app.app --api %API_URL%

endlocal
