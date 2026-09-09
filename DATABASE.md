# CodePilot — Relational Database Architecture

CodePilot utilizes **SQLAlchemy 2.0 ORM** with native support for SQLite (zero-config local development) and PostgreSQL (high-concurrency production deployments).

---

## 1. Entity-Relationship Overview

```
 ┌───────────────┐        1:1        ┌───────────────┐
 │     User      ├───────────────────┤    Profile    │
 └───┬───┬───┬───┘                   └───────────────┘
     │   │   │
     │   │   │ 1:N
     │   │   └───────────────────────┐
     │   │ 1:N                       │
     │   └───────────────┐           ▼
     ▼                   ▼     ┌───────────────┐
┌──────────────┐   ┌─────────┐ │ActivityHistory│
│ CodeExecution│   │ Project │ └───────────────┘
└──────────────┘   └───┬─────┘
                       │ 1:N
                       ▼
                 ┌───────────┐
                 │ProjectFile│
                 └───────────┘

 ┌───────────────┐ 1:N ┌───────────────┐ 1:N ┌───────────────┐
 │    Problem    ├────►│   TestCase    │     │  Submission   │
 └───────┬───────┘     └───────────────┘     └───────┬───────┘
         │                                           │
         └───────────────────────────────────────────┘
```

---

## 2. Core Tables Schema

### `users`
- `id` (INTEGER, PK, Autoincrement)
- `username` (VARCHAR(64), UNIQUE, INDEX)
- `email` (VARCHAR(128), UNIQUE, INDEX)
- `password_hash` (VARCHAR(256), NOT NULL)
- `salt` (VARCHAR(64), NOT NULL)
- `role` (VARCHAR(32), Default: 'USER') — `USER`, `MODERATOR`, `INSTRUCTOR`, `ADMIN`
- `is_active` (BOOLEAN, Default: TRUE)
- `is_verified` (BOOLEAN, Default: FALSE)
- `created_at`, `updated_at` (TIMESTAMP)

### `profiles`
- `id` (INTEGER, PK)
- `user_id` (INTEGER, FK -> `users.id`, UNIQUE, INDEX)
- `display_name` (VARCHAR(128))
- `avatar_url` (VARCHAR(256))
- `bio` (TEXT)
- `primary_language` (VARCHAR(32))
- `preferred_languages` (TEXT, JSON list)
- `xp` (INTEGER, Default: 0)
- `level` (INTEGER, Default: 1)
- `rank_title` (VARCHAR(64))
- `streak_days` (INTEGER)
- `problems_solved` (INTEGER)
- `contest_rating` (INTEGER, Default: 1200)

### `activity_history`
- `id` (INTEGER, PK)
- `user_id` (INTEGER, FK -> `users.id`, INDEX)
- `activity_type` (VARCHAR(64), INDEX) — `EXECUTION`, `SUBMISSION`, `AI_REVIEW`, `COURSE`, `LOGIN`
- `title` (VARCHAR(256))
- `description` (TEXT)
- `language` (VARCHAR(32), INDEX)
- `status` (VARCHAR(32))
- `details_json` (TEXT)
- `created_at` (TIMESTAMP, INDEX)

### `problems`
- `id` (INTEGER, PK)
- `slug` (VARCHAR(128), UNIQUE, INDEX)
- `title` (VARCHAR(256))
- `difficulty` (VARCHAR(32), INDEX) — `Easy`, `Medium`, `Hard`
- `category` (VARCHAR(64), INDEX)
- `tags` (TEXT, JSON array)
- `description` (TEXT)
- `constraints` (TEXT)
- `hints` (TEXT, JSON array)
- `editorial` (TEXT)
- `starter_templates` (TEXT, JSON map)
- `time_limit_seconds` (FLOAT, Default: 2.0)
- `memory_limit_mb` (FLOAT, Default: 128.0)
- `total_submissions` (INTEGER)
- `accepted_submissions` (INTEGER)

### `test_cases`
- `id` (INTEGER, PK)
- `problem_id` (INTEGER, FK -> `problems.id`, INDEX)
- `input_data` (TEXT, NOT NULL)
- `expected_output` (TEXT, NOT NULL)
- `is_hidden` (BOOLEAN, Default: FALSE)
- `explanation` (TEXT)
- `order_index` (INTEGER)

### `submissions`
- `id` (INTEGER, PK)
- `user_id` (INTEGER, FK -> `users.id`, INDEX)
- `problem_id` (INTEGER, FK -> `problems.id`, INDEX)
- `contest_id` (INTEGER, FK -> `contests.id`, NULLABLE, INDEX)
- `language` (VARCHAR(32), INDEX)
- `source_code` (TEXT, NOT NULL)
- `status` (VARCHAR(32), INDEX)
- `passed_tests` (INTEGER)
- `total_tests` (INTEGER)
- `runtime_seconds` (FLOAT)
- `memory_mb` (FLOAT)
- `compiler_output` (TEXT)
- `test_results_json` (TEXT)
- `created_at` (TIMESTAMP, INDEX)

---

## 3. Indexing & Optimization Strategy
- **Authentication lookups**: Composite index on `username` and `email`.
- **Tenant activity isolation**: Strict filtering on `user_id` with descending `created_at` index.
- **Problem catalog search**: Indexes on `difficulty`, `category`, and `slug`.
