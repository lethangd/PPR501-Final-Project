# PowerShell script to run crawler via Docker
# Usage: .\run_crawler.ps1

Write-Host "Student Management System Crawler" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
docker info 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if the network exists
$network = docker network ls --format "{{.Name}}" | Where-Object { $_ -eq "ppr501-final-project_default" }
if (-not $network) {
    Write-Host "[ERROR] Docker network not found. Please run 'docker compose up -d' first." -ForegroundColor Red
    exit 1
}

# Create output directory if not exists
if (-not (Test-Path "./output")) {
    New-Item -ItemType Directory -Path "./output" | Out-Null
}

Write-Host "[INFO] Building crawler image..." -ForegroundColor Yellow
docker build -t student-crawler ./crawler

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to build crawler image." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[INFO] Running crawler..." -ForegroundColor Yellow
Write-Host ""

# Run crawler with volume mount for output
docker run --rm -v "${PWD}/output:/app/output" --network ppr501-final-project_default student-crawler

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] Crawler completed successfully!" -ForegroundColor Green
    Write-Host "[INFO] Output file: ./output/students.xlsx" -ForegroundColor Cyan
    Write-Host ""
    explorer.exe .\output
} else {
    Write-Host "[ERROR] Crawler failed." -ForegroundColor Red
    exit 1
}
