# Run Next.js Dashboard (PowerShell)
# Navigate to sentiment-dashboard and run dev server

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$nextDir = Join-Path $projectRoot '..\sentiment-dashboard'
Set-Location $nextDir

if (Test-Path package.json) {
    Write-Host "Starting Next.js dev server..."
    npm run dev
} else {
    Write-Host "package.json not found in sentiment-dashboard. Ensure the path is correct." -ForegroundColor Yellow
}
