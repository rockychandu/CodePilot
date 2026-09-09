# CodePilot — Production Deployment Guide

## 1. Local Development
```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Start the Backend API (Port 5000)
python backend/app.py

# 3. Start the Frontend Server (Port 8000)
python -m http.server 8000
```
Open `http://localhost:8000` in your web browser.

---

## 2. Docker & Containerized Deployment
```bash
# Build and run containers in background
docker compose up -d --build

# View container logs
docker compose logs -f
```

---

## 3. Production Environment Variables
| Variable | Description | Default |
|---|---|---|
| `PORT` | API listen port | `5000` |
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///codepilot.db` |
| `CODEPILOT_SECRET_KEY` | JWT HMAC signing secret | `codepilot-super-secret-jwt-key-2026-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifespan | `1440` (24h) |
| `ENV` | Environment name | `production` |
