# CodePilot — Enterprise Developer Platform & Cloud Execution Engine

[![CI/CD Pipeline](https://github.com/codepilot/codepilot/actions/workflows/ci.yml/badge.svg)](.github/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](pyproject.toml)
[![Node Version](https://img.shields.io/badge/Node.js-20%2B-339933.svg?logo=node.js&logoColor=white)](package.json)
[![Build: Vite](https://img.shields.io/badge/Build-Vite%205-646CFF.svg?logo=vite&logoColor=white)](package.json)

**CodePilot** is an enterprise-grade cloud developer platform providing an authentic, restrained developer IDE, isolated multi-language code execution engine, competitive programming judge with hidden test verification, live contests, interactive learning academy, Pilot AI engineering assistant, and persistent activity history.

---

## 🏗 System Architecture

The platform is structured into decoupled, production-ready modules:

```
CodePilot/
├── backend/                  # Flask REST API v1 Architecture
│   ├── api/                  # Blueprint routers (/api/v1/auth, execution, problems, contests, etc.)
│   ├── auth/                 # Authentication service & token lifecycle
│   ├── execution/            # Isolated process execution engine & limit enforcement
│   ├── runtime/              # Multi-language host runtime registry & diagnostics
│   ├── problems/             # Problem catalog & metadata
│   ├── submissions/          # Multi-case competitive judge pipeline
│   ├── contests/             # Contest lifecycle & live leaderboards
│   ├── courses/              # Curriculum & course hierarchy
│   ├── projects/             # Workspace projects & file tree operations
│   ├── ai/                   # Pilot AI AST code reviewer & test synthesizer
│   ├── history/              # Chronological user activity audit trail
│   ├── search/               # Multi-entity global search engine
│   ├── analytics/            # Telemetry & system observability
│   ├── security/             # PBKDF2 hashing, JWT HMAC tokens, sliding-window rate limiter
│   ├── repositories/         # Clean ORM data access repositories
│   └── app.py                # Server entrypoint with auto-seeding & middleware
├── frontend/                 # High-Density Developer SPA UI
│   ├── main.js               # SPA entrypoint & hash-based router
│   ├── components/           # Reusable components (IDE, Navbar, Search, Modals, Terminal)
│   ├── pages/                # Views (Dashboard, IDE, Problems, Contests, History, Admin)
│   ├── services/             # Client API service adapters (Auth, Execution, Problem, etc.)
│   └── styles/               # Developer design system tokens, base, components, and pages
├── codepilot/                # Core Python Platform Library & CLI
│   ├── db/                   # SQLAlchemy ORM models, migrations, & database seeds
│   ├── engine/               # Execution sandbox & runtime detectors
│   └── cli.py                # Developer CLI utility
├── scripts/                  # Unified startup & maintenance automation
├── tests/                    # 500+ automated unit, integration, and API test cases
├── pyproject.toml            # Python package specification & dependencies
├── package.json              # Frontend manifest & npm build scripts
└── package-lock.json         # Pinned reproducible dependency lockfile
```

---

## ⚡ Quick Start & Development Setup

### System Prerequisites
- **Python**: `>= 3.10` (Python 3.11/3.12/3.14 verified)
- **Node.js**: `>= 20.0` (Node.js 20/22/25 verified)
- **npm**: `>= 10.0`

### 1. Installation

#### Backend Dependencies (Python)
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# Install locked production and test dependencies
pip install -r backend/requirements.txt
```

#### Frontend Dependencies (Node.js)
```bash
# Clean reproducible dependency install via package-lock.json
npm ci
```

---

### 2. Running Locally

#### Option A: Unified Dev Launcher (Recommended)
**On Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev.ps1
```

**On Linux / macOS (Bash):**
```bash
chmod +x scripts/dev.sh
./scripts/dev.sh
```

#### Option B: Individual Service Launchers
**Terminal 1 — Backend API:**
```bash
python -m backend.app
# Listening on http://127.0.0.1:5000
```

**Terminal 2 — Frontend Dev Server (Vite):**
```bash
npm run dev
# Accessible on http://127.0.0.1:5173
```

---

## 🧪 Automated Testing & Quality Verification

Run the full automated test suite spanning unit algorithms, integration endpoints, and frontend assertions:

```bash
# 1. Run Comprehensive 500+ Algorithmic & Security Test Suite
python tests/comprehensive_suite.py

# 2. Run Authentication & User Session Suite
python -m unittest tests/auth/test_auth_system.py

# 3. Run API v1 REST Endpoint Integration Tests
python tests/api/test_modular_api.py

# 4. Run Repository Data Access Tests
python tests/unit/test_repositories.py

# 5. Run Frontend Test Runner
npm test

# 6. Build Production Frontend Bundle
npm run build
```

---

## 🚀 Key Platform Capabilities

1. **Human-Made Developer UI**: Designed around information density, monospaced typography (`JetBrains Mono`, `Inter`), crisp 1px borders, and dark zinc themes without artificial glowing cards or neon glassmorphism.
2. **Dedicated Auth Lifecycle**: Real SQLite database persistence with PBKDF2-HMAC-SHA256 (100,000 rounds) password hashing, JWT access and refresh tokens, real-time password strength meter, email verification, password reset, and brute-force lockout protection.
3. **Route Guards & Session Isolation**: Frontend SPA navigation guards protecting private routes (`/dashboard`, `/ide`, `/problems`, `/contests`, `/history`, `/settings`, `/admin`) and strict user data isolation on executions and history.
4. **3-Column IDE Workspace**: File explorer tree, tabbed code editor with line numbers, Pilot AI analysis dock, and resizable bottom console for stdin input, stdout output, and terminal.
5. **Multi-Language Sandbox**: Process isolation with memory limits, execution timeouts, and native runtime detection (Python, C, C++, Java, JavaScript, Go, Rust).
6. **Competitive Problem Judge**: Multi-case submission pipeline evaluating public and hidden test cases, returning Accepted, Wrong Answer, Compilation Error, and Time Limit Exceeded verdicts.
7. **Real User History**: Fully persistent chronological activity log surviving page refreshes and server restarts with pagination and filter options.

---

## License

CodePilot is proprietary software.

Copyright © 2026 CodePilot. All rights reserved.

Unauthorized copying, modification, distribution, or commercial use is prohibited without written permission from the copyright owner.

For licensing inquiries, contact the project owner.

