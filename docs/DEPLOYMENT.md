# CodePilot Production Deployment Guide

## Prerequisites
- Python 3.10+
- Node.js 20+
- PostgreSQL 15+ (optional; SQLite supported by default)
- GCC/G++, OpenJDK, Node, Python host runtimes

---

## 1. Environment Setup

Copy example environment configuration and specify production secrets:

```bash
export SECRET_KEY="enterprise-production-super-secret-key"
export JWT_SECRET="enterprise-jwt-signing-secret"
export DATABASE_URL="sqlite:///codepilot.db" # Or postgresql://user:pass@host:5432/codepilot
export FLASK_ENV="production"
```

---

## 2. Dependency Installation

```bash
# Python Backend
pip install -r backend/requirements.txt

# Node Frontend
npm ci
```

---

## 3. Production Build & Startup

```bash
# Build optimized frontend assets
npm run build

# Launch Python API Server with multi-worker WSGI (e.g. Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

---

## 4. Docker Deployment

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install -r backend/requirements.txt
EXPOSE 5000
CMD ["python", "-m", "backend.app"]
```
