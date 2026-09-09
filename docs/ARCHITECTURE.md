# CodePilot Platform Architecture

## Executive Overview
CodePilot is an enterprise-scale developer platform and multi-language code execution environment designed for high-density information architecture, sub-second execution sandboxing, competitive programming evaluation, and persistent user history.

```
+-------------------------------------------------------------------------------+
|                       CodePilot Frontend SPA (Vite)                           |
|  [Multi-File Editor] [3-Column IDE] [Problem Judge] [Contest Arena] [Pilot AI]|
+---------------------------------------+---------------------------------------+
                                        | HTTP / REST API v1
                                        v
+-------------------------------------------------------------------------------+
|                       CodePilot Backend (Python Flask)                        |
|  [Auth & RBAC] [Session Mgr] [Judge Engine] [Telemetry] [Recommendation Eng]  |
+---------------------------------------+---------------------------------------+
        |                               |                               |
        v                               v                               v
+--------------------+      +-----------------------+      +--------------------+
| SQLite / PostgreSQL|      | Isolated Sandbox PIDs |      | In-Memory Caches   |
| (SQLAlchemy ORM)   |      | (Process Watchdogs)   |      | (LRU / Sliding Win)|
+--------------------+      +-----------------------+      +--------------------+
```

---

## Core Subsystems

### 1. Authentication & Session Manager (`backend/auth/`)
- Password Hashing: Salted `PBKDF2-HMAC-SHA256` with 100,000 iterations.
- JWT Access Tokens: Stateless HMAC-SHA256 signed tokens with unique `jti` nonce.
- Refresh Tokens: Cryptographically secure 48-byte random tokens.
- Anti-Brute-Force: Sliding-window rate limiting tracking failed attempts per IP and identifier.
- RBAC Roles: `USER`, `MODERATOR`, `INSTRUCTOR`, `ADMIN`.

### 2. Multi-Language Execution & Sandboxing (`backend/execution/`, `backend/sandbox/`)
- Process isolation using separate subprocess instances with memory watchdogs.
- Configurable timeout traps (default: 5.0s) and memory caps (default: 128MB).
- Supported host runtimes: Python, C, C++, Java, JavaScript, TypeScript, Go, Rust, C#, PHP, Ruby, Kotlin.

### 3. Competitive Programming Judge (`backend/judge/`, `backend/submissions/`)
- Multi-test-case validation executing starter code against public and hidden test fixtures.
- Precise verdict classification: `ACCEPTED`, `WRONG_ANSWER`, `COMPILE_ERROR`, `RUNTIME_ERROR`, `TIME_LIMIT_EXCEEDED`, `MEMORY_LIMIT_EXCEEDED`.

### 4. Contest & Rating Platform (`backend/contests/`, `backend/ratings/`)
- Scheduled contest windows, registration gates, penalty calculators, and live scoreboard freezes.
- Elo and Glicko-2 skill rating recalculators.

### 5. Learning & Course Academy (`backend/learning/`, `backend/courses/`)
- Structured curriculum hierarchy: Courses -> Modules -> Lessons -> Coding Exercises.
- Interactive code challenges and automated grading verifiers.

### 6. Pilot AI Engineering Assistant (`backend/ai/`)
- AST-based static code analyzer, cyclomatic complexity evaluator, security vulnerability scanner, and unit test synthesizer.

### 7. Persistent User History & Audit Trail (`backend/history/`, `backend/audit/`)
- Chronological timeline capturing code runs, judge submissions, contest entries, and login activity.
- Strict multi-tenant isolation ensuring User A only accesses User A's activity logs.
