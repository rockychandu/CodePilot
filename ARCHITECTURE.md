# CodePilot — Comprehensive Architecture Audit & Production Blueprint

## 1. Executive Overview
CodePilot is an integrated, commercial-grade developer platform that unifies:
- **Cloud IDE**: Multi-tab code editor, syntax highlighting, minimap, line numbers, and virtual file tree.
- **Multi-Language Execution Engine**: Native subprocess sandbox supporting Python, JavaScript/Node.js, C, C++, Java, Go, Rust, Ruby, PHP, and C#.
- **Competitive Programming Platform**: Problem catalog, test case evaluation (public + hidden), automated judging, penalty calculation, and real-time contest leaderboards.
- **Pilot AI Developer Suite**: AST-based static code review, time/space complexity analysis, automated unit test generation, refactoring recommendations, and algorithmic problem hints.
- **Developer Learning Center**: Video curriculum with chapter timestamps, interactive PDF documentation viewer, quizzes, and automated certificate generation.
- **Project Workspaces**: Multi-file workspace management with import/export, templates, and execution capabilities.
- **Skill Tree & 365-Day Activity Tracking**: Contribution heatmaps, skill progression trees, XP, leveling, and achievement badges.
- **Enterprise Administration & Analytics**: RBAC, audit logging, system metrics, DAU/MAU analytics, and execution telemetry.

---

## 2. Existing Architecture & Module Audit

### 2.1 Backend Architecture (`backend/` & `codepilot/`)
- **Web Framework**: Flask 3.0+ REST API with Flask-CORS for cross-origin client communication.
- **Engine Core (`codepilot/engine/`)**:
  - `sandbox.py`: AST validator restricting unsafe Python imports and executing code within isolated sub-processes.
  - `ai_assistant.py`: Static analysis-driven code reviewer and PEP8 compliance checker.
- **Data Models (`codepilot/models/`)**: Python dataclasses and SQLAlchemy declarative models for Users, Problems, Submissions, Contests, Courses, and Activity Logs.
- **Services (`codepilot/services/`)**: Business logic layer managing authentication, problem loading, contest timers, and execution dispatching.
- **CLI Interface (`codepilot/cli.py`)**: Terminal interface for listing problems, running local solutions, and triggering AI code reviews.

### 2.2 Frontend Architecture (`frontend/` & `index.html`)
- **Architecture**: Vanilla ES6+ Modular Single Page Application (SPA) with custom hash routing, reactive store state management, and reusable UI components.
- **Design System (`frontend/styles/` & `design-system/`)**:
  - `tokens.css`: Curated HSL color palette, typography scales, glassmorphism tokens, and elevation variables.
  - `base.css`: CSS reset, typography, and dark-theme foundation.
  - `components.css`: Button, modal, badge, dropdown, table, card, tab, and alert design tokens.
  - `ide.css`: Code editor layout, split-pane terminal, line numbers, minimap, and file explorer styling.
  - `landing.css` & `pages.css`: Responsive landing hero, dashboard metrics, leaderboards, course viewer, and settings styling.
- **Client Services (`frontend/services/`)**: REST integration layer with fallback offline persistence in `localStorage`/`sessionStorage`.

---

## 3. Data Flow Architecture

```
User (Browser / CLI)
        │
        ▼
   HTTP / REST API  ◄───────── Auth & Rate Limiting Middleware (JWT / RBAC)
        │
  ┌─────┴──────────────────────────────────────────────────────┐
  │                   Application Services                     │
  │  ┌──────────────┐ ┌──────────────┐ ┌────────────────────┐  │
  │  │ Auth & Users │ │ Problems/Judge│ │   Learning Center  │  │
  │  └──────┬───────┘ └──────┬───────┘ └────────┬───────────┘  │
  │  ┌──────┴───────┐ ┌──────┴───────┐ ┌────────┴───────────┐  │
  │  │  Pilot AI    │ │  Leaderboards│ │ Project Workspaces │  │
  │  └──────────────┘ └──────────────┘ └────────────────────┘  │
  └───────────────────────────┬────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
    Relational Database              Execution Sandbox Engine
 (Users, Submissions, Logs)          (Python, C++, Java, Node, etc.)
```

---

## 4. Execution Sandbox Engine Architecture

The execution engine provides multi-language compilation and execution isolation:
1. **Request Intake**: API receives `language`, `sourceCode`, `stdin`, `timeLimit`, and `memoryLimit`.
2. **Language Adapter Resolution**: Resolves compiler command, compilation flags, execution binary, and runtime dependencies.
3. **Temporary Isolation**: Creates an isolated per-request directory with unique execution tokens.
4. **Compilation Phase**: Runs compiler subprocess (`gcc`, `g++`, `javac`, `rustc`, `go build`). If compilation fails, returns `COMPILE_ERROR` with compiler diagnostics.
5. **Execution Phase**: Runs binary/script using `subprocess.Popen` with standard I/O redirection and timeout watchdog (default 5.0s).
6. **Telemetry & Metrics**: Collects wall-clock runtime, process peak memory usage, standard output, and standard error.
7. **Cleanup**: Guaranteed cleanup of temporary artifacts within `finally` blocks.

---

## 5. Security & Isolation Model
- **Password Security**: PBKDF2-HMAC-SHA256 with cryptographically random 32-byte salts; plaintext passwords are never logged or stored.
- **Authentication**: Stateless JSON Web Tokens (JWT) with configurable expiration, signature verification, and user session revocation.
- **Role-Based Access Control (RBAC)**: Strict role gates (`USER`, `MODERATOR`, `INSTRUCTOR`, `ADMIN`) across sensitive endpoints.
- **Data Isolation**: Strict user-level tenant querying preventing cross-account access to execution history or private project files.
- **Execution Sandboxing**: Timeouts, memory limits, banned syscall guards, AST inspection for dangerous modules, and isolated scratch directories.

---

## 6. Migration & Evolution Roadmap
1. **Database Persistence**: Transition in-memory stores to unified SQLAlchemy ORM supporting SQLite and PostgreSQL.
2. **REST API Versioning**: Implement `/api/v1/*` standardized REST routes with comprehensive request validation and structured error payloads.
3. **Automated Judging Engine**: Connect problem submissions with automated multi-case test runners (public + hidden test evaluation).
4. **Pilot AI Expansion**: Broaden AST rules and heuristics to provide automated test case synthesis, complexity estimation, and bug explanations.
5. **Automated Test Infrastructure**: Deliver 500+ automated unit, integration, API, and security tests.
6. **DevOps & Containerization**: Deliver production `Dockerfile`, `docker-compose.yml`, and GitHub Actions CI pipelines.
