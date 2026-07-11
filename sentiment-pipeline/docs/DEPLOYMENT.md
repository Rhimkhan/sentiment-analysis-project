# Deployment Guide

## Local Setup
1. Copy `.env.example` to `.env`.
2. Update any necessary environment variables.
3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Start the full stack:

```bash
docker compose up --build
```

5. Access the dashboard at `http://localhost:8501/`.

## Docker Compose Services
- `zookeeper` — Kafka coordination service.
- `kafka` — Kafka broker for event streaming.
- `mongo` — MongoDB storage for processed tweets.
- `redis` — optional cache or shared state.
- `producer` — data producer service.
- `processor` — sentiment consumer service.
- `dashboard` — Streamlit dashboard.

## VS Code Launch Configurations
Use the launch configs in `.vscode/launch.json`:
- `🐍 Consumer: Run All`
- `🐍 Producer: Run Mock`
- `📊 Dashboard: Streamlit`
- `🧪 Run All Tests`

## Production Notes
- Use `USE_MOCK=false` and set `TWITTER_BEARER_TOKEN` for real data.
- Set `SENTIMENT_MODEL=ensemble` for a combined model approach.
- Consider `prometheus` and `grafana` for monitoring in production.
- Secure MongoDB in production with authentication and network rules.
