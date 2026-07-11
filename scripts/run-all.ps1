Write-Host "🚀 Starting All Services..." -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Yellow

Write-Host "📊 Starting Streamlit Dashboard..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\rhim7\Downloads\project\PROJECT 3 SEDIMENT ANALYSIS OF REVIEWS\SENTIMENT ANALYSIS OF REVIEWS\sentiment-pipeline'; .\venv\Scripts\Activate.ps1; streamlit run simple_app.py"

Start-Sleep -Seconds 2

Write-Host "⚛️ Starting Next.js Dashboard..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\rhim7\Downloads\project\PROJECT 3 SEDIMENT ANALYSIS OF REVIEWS\SENTIMENT ANALYSIS OF REVIEWS\sentiment-dashboard'; npm run dev"

Write-Host ""
Write-Host "✅ All services started!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Streamlit: http://localhost:8501" -ForegroundColor Yellow
Write-Host "📍 Next.js:   http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop services." -ForegroundColor Red
