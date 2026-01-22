@echo off
REM Batch script to run crawler via Docker
REM Usage: run_crawler.bat

echo.
echo  Student Management System Crawler
echo =====================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Create output directory if not exists
if not exist "output" mkdir output

echo [INFO] Building crawler image...
docker build -t student-crawler ./crawler

if errorlevel 1 (
    echo [ERROR] Failed to build crawler image.
    pause
    exit /b 1
)

echo.
echo [INFO] Running crawler...
echo.

REM Run crawler with volume mount for output
REM Crawler image defaults to http://backend:8000/api/students
docker run --rm -v "%cd%/output:/app/output" --network ppr501-final-project_default student-crawler

if errorlevel 0 (
    echo.
    echo [SUCCESS] Crawler completed!
    echo [INFO] Output file: .\output\students.xlsx
    echo.
    explorer.exe .\output
) else (
    echo [ERROR] Crawler failed.
)

pause
