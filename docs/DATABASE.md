# CodePilot Relational Database Schema & Models

CodePilot uses SQLAlchemy ORM supporting SQLite for local zero-config execution and PostgreSQL for high-concurrency production deployments.

---

## Entity Relationship Architecture

```
+-------------+         +---------------+         +-------------------+
|    User     | 1 --- 1 |    Profile    | 1 --- * |    UserSkill      |
+-------------+         +---------------+         +-------------------+
       | 1
       + --- * +-------------------+
       |       |    UserSession    |
       |       +-------------------+
       + --- * +-------------------+
       |       |  ActivityHistory  |
       |       +-------------------+
       + --- * +-------------------+
               |    Submission     | * --- 1 +-------------------+
               +-------------------+         |      Problem      | 1 --- * +---------------+
                                             +-------------------+         |   TestCase    |
                                                       | *                 +---------------+
                                                       |
                                             +-------------------+
                                             |      Contest      |
                                             +-------------------+
```

---

## Core Models

1. **`users`**: Primary authentication entity (`id`, `username`, `email`, `password_hash`, `salt`, `role`, `is_active`, `is_verified`, `last_login_at`, `created_at`, `updated_at`).
2. **`profiles`**: Developer public profile (`display_name`, `avatar_url`, `bio`, `primary_language`, `xp`, `level`, `rank_title`, `streak_days`, `problems_solved`, `contest_rating`).
3. **`user_settings`**: User preferences (`theme`, `email_notifications`, `editor_font_size`, `editor_tab_size`, `editor_keymap`).
4. **`sessions`**: Active authentication sessions (`token`, `refresh_token`, `ip_address`, `user_agent`, `expires_at`, `is_revoked`).
5. **`login_attempts`**: Anti-brute-force audit log (`ip_address`, `username_or_email`, `attempted_at`, `success`, `failure_reason`).
6. **`password_resets`** & **`email_verifications`**: Cryptographic one-time token records.
7. **`problems`** & **`test_cases`**: Competitive challenge specifications and test fixtures.
8. **`submissions`**: Evaluation logs and multi-case verdict results.
9. **`contests`**: Scheduled competition arenas and leaderboard metadata.
10. **`courses`**, **`modules`**, **`lessons`**: Learning curriculum hierarchy.
11. **`activity_history`**: Chronological timeline records.
