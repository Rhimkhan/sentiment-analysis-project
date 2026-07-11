# Run Streamlit Dashboard (PowerShell)
# Navigate to project root and activate venv, then run simple_app.py

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

if (Test-Path .\venv\Scripts\Activate.ps1) {
    Write-Host "Activating virtual environment..."
    . .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment activation script not found. Ensure venv is created or activate manually." -ForegroundColor Yellow
}

Write-Host "Starting Streamlit dashboard (simple_app.py)..."
streamlit run simple_app.py
