Write-Host "🚀 Starting Next.js Dashboard..." -ForegroundColor Cyan
cd "C:\Users\rhim7\Downloads\project\PROJECT 3 SEDIMENT ANALYSIS OF REVIEWS\SENTIMENT ANALYSIS OF REVIEWS\sentiment-dashboard"

# Check if node_modules exists
if (!(Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
}

npm run dev
