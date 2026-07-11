Write-Host "👑 Starting Admin Dashboard..." -ForegroundColor Cyan
cd "C:\Users\rhim7\Downloads\project\PROJECT 3 SEDIMENT ANALYSIS OF REVIEWS\SENTIMENT ANALYSIS OF REVIEWS\sentiment-pipeline"
.\venv\Scripts\Activate.ps1
streamlit run admin_login.py --server.port 8503
