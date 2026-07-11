# SentimentIQ - Real-time Brand Intelligence

SentimentIQ is a real-time sentiment monitoring platform built for startups and companies that need fast, accurate brand intelligence and crisis alerts.

## 🚀 Problem Statement
Companies lose millions because they can't monitor brand sentiment in real-time. They often learn about PR crises too late.

## 💡 Our Solution
Real-time sentiment intelligence that monitors social media, classifies sentiment, and alerts teams before a crisis happens.

## 🎯 Target Users
- Marketing Teams: manual monitoring is slow → automated real-time alerts
- PR Agencies: crisis response is too late → instant negative sentiment detection
- Product Managers: no feedback loop → continuous product sentiment insights
- Startup Founders: enterprise tools are expensive → affordable self-hosted/freemium solution

## 📏 Success Metrics
- Response Time: < 5 seconds from tweet to dashboard
- Accuracy: > 90% sentiment classification
- User Engagement: 10+ daily active users
- Alert Accuracy: < 5% false positives
- Processing Speed: 1000+ tweets/second

## 🏗️ Architecture Overview
- `src/producer/` — data ingestion and tweet publishing
- `src/consumer/` — sentiment analysis and processing
- `src/storage/` — MongoDB storage for processed events
- `src/dashboard/` — Streamlit visualization
- `config/` — configuration and environment settings
- `docs/` — architecture and deployment documentation

## 📦 Quick Start
1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Copy environment settings:

```bash
copy .env.example .env
```

3. Start the full stack locally:

```bash
docker compose up --build
```

4. Run the dashboard:

```bash
streamlit run src/dashboard/app.py
```

## 🔧 Recommended VS Code Setup
This repository includes `.vscode/` workspace settings for Python, debugging, testing, and Docker.

### Run from VS Code
- `🐍 Consumer: Run All`
- `🐍 Producer: Run Mock`
- `📊 Dashboard: Streamlit`
- `🧪 Run All Tests`

## 📚 Project Documentation
- `docs/ARCHITECTURE.md` — architecture and design overview
- `docs/DEPLOYMENT.md` — Docker Compose and deployment instructions

## 🧪 Testing
Run all tests:

```bash
pytest tests/ -v --cov=src --cov-report=html
```

## 📁 Workspace File Structure
```text
sentiment-pipeline/
├── .vscode/                  # VS Code workspace settings
├── config/                   # YAML and runtime configuration
├── docs/                     # Architecture and deployment docs
├── src/                      # Main application code
│   ├── consumer/
│   ├── dashboard/
│   ├── producer/
│   └── storage/
├── docker-compose.yml        # Local stack orchestration
├── requirements.txt          # Python dependencies
├── README.md                 # Project overview
└── .env.example              # Environment sample
```

## ✅ What This Project Now Includes
- startup-friendly architecture
- investor-ready product description
- company-ready docs and deployment
- VS Code launch, test, and task configurations
- production-style Docker Compose setup

## 📌 Notes
This README is the central handbook for developers, founders, and reviewers. Keep it updated as features and architecture evolve.

## ▶ Run & Deploy
Below are convenient PowerShell commands to run the Streamlit dashboard, run the Next.js dashboard locally, deploy to Vercel, and check running status.

1) Run Streamlit Dashboard (PowerShell)

```powershell
# Navigate to your project
cd "C:\Users\rhim7\Downloads\project\PROJECT 3 SEDIMENT ANALYSIS OF REVIEWS\SENTIMENT ANALYSIS OF REVIEWS\sentiment-pipeline"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the dashboard
streamlit run simple_app.py
```

Open: http://localhost:8501

2) Run Next.js Dashboard (Local)

```powershell
# Navigate to Next.js dashboard
cd "C:\Users\rhim7\Downloads\project\PROJECT 3 SEDIMENT ANALYSIS OF REVIEWS\SENTIMENT ANALYSIS OF REVIEWS\sentiment-dashboard"

# Run development server
npm run dev
```

Open: http://localhost:3000

3) Deploy to Vercel

```powershell
# Navigate to Next.js dashboard
cd "C:\Users\rhim7\Downloads\project\PROJECT 3 SEDIMENT ANALYSIS OF REVIEWS\SENTIMENT ANALYSIS OF REVIEWS\sentiment-dashboard"

# Deploy to Vercel (production)
vercel --prod
```

4) Quick Status Checks

```powershell
# Check if streamlit is running
Get-Process python* | Where-Object { $_.MainWindowTitle -like "*streamlit*" }

# Check if Next.js is running
Get-Process node* | Where-Object { $_.MainWindowTitle -like "*next*" }
```

You can also use the workspace PowerShell scripts in `scripts/` and the VS Code tasks under the Run Task menu.
