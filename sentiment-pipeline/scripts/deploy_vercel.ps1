# Deploy Next.js dashboard to Vercel (PowerShell)
# Navigate to sentiment-dashboard and run vercel --prod

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$nextDir = Join-Path $projectRoot '..\sentiment-dashboard'
Set-Location $nextDir

if (Test-Path package.json) {
    Write-Host "Deploying to Vercel (production)..."
    vercel --prod
} else {
    Write-Host "package.json not found in sentiment-dashboard. Ensure the path is correct." -ForegroundColor Yellow
}
