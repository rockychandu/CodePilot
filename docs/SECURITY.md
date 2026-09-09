# CodePilot Platform Security Architecture

## 1. Cryptographic Standards

- **Password Hashing**: Salted `PBKDF2-HMAC-SHA256` utilizing 100,000 iterations with 32-byte cryptographic random salts.
- **Constant-Time Verification**: Verification operations use `hmac.compare_digest` to prevent side-channel timing attacks.
- **Session Tokens**: Tamper-proof HMAC-SHA256 signed JSON Web Tokens (JWT) incorporating unique `jti` nonces.
- **Refresh Tokens**: Cryptographically secure 48-byte URL-safe random nonces (`secrets.token_urlsafe(48)`).

---

## 2. Access Control & Authorization

- **Role-Based Access Control (RBAC)**:
  - `USER`: Access to IDE, problems, learning, contests, and personal history.
  - `INSTRUCTOR`: Content authoring capabilities for courses and problem sets.
  - `MODERATOR`: Community moderation, report management.
  - `ADMIN`: Full platform governance, tenant controls, system telemetry, and audit inspection.
- **Protected Endpoints**: Guaranteed 401 Unauthorized for unauthenticated requests and 403 Forbidden for insufficient roles.

---

## 3. Anti-Brute-Force & Rate Limiting

- **Sliding-Window Rate Limiting**: All authentication routes are gated with sliding-window attempt trackers.
- **Lockout Mechanism**: Multiple failed login attempts (default: 10 attempts in 15 minutes) trigger temporary account lockouts.
- **Audit Logging**: All authentication successes, failures, and password resets are recorded in immutable audit tables.

---

## 4. Multi-Tenant Data Isolation

- Activity history, code runs, project workspaces, and problem submissions strictly enforce tenant ownership filters (`user_id == current_user.id`).
- Direct object reference (IDOR) attacks are mitigated by requiring ownership validation on all query fetchers.
