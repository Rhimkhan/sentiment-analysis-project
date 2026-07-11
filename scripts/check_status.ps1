Write-Host "📊 Checking Dashboard Status..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Streamlit Dashboard:" -ForegroundColor Yellow
$streamlit = Get-Process python* -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*streamlit*" }
if ($streamlit) {
    Write-Host "✅ Running on http://localhost:8501" -ForegroundColor Green
} else {
    Write-Host "❌ Not running" -ForegroundColor Red
}
Write-Host ""
Write-Host "Next.js Dashboard:" -ForegroundColor Yellow
$nextjs = Get-Process node* -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*next*" }
if ($nextjs) {
    Write-Host "✅ Running on http://localhost:3000" -ForegroundColor Green
} else {
    Write-Host "❌ Not running" -ForegroundColor Red
}
Write-Host ""
Write-Host "Vercel Deployment:" -ForegroundColor Yellow
Write-Host "🌐 https://sentiment-dashboard-ivory.vercel.app" -ForegroundColor Cyan
