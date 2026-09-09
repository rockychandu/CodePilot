# CodePilot — Security & Isolation Architecture

## 1. Authentication & Session Security
- **Password Hashing**: PBKDF2-HMAC-SHA256 with 100,000 iterations and cryptographically random 32-byte salt per user (`os.urandom(32)`). Plaintext passwords are never persisted.
- **JWT Architecture**: Signed HMAC-SHA256 tokens with dynamic unique JWT ID (`jti`) ensuring uniqueness across subsecond requests.
- **Session Revocation**: Tokens can be explicitly revoked upon logout (`is_revoked = True` in `sessions` table).

---

## 2. Authorization & RBAC
- **Role Hierarchy**:
  - `USER`: Submit code, create workspaces, participate in contests, view own history.
  - `MODERATOR`: Review community discussions, moderate user reports.
  - `INSTRUCTOR`: Create courses, curate problem sets, author test cases.
  - `ADMIN`: Full platform access, manage user roles, view system telemetry and audit logs.
- **Enforcement**: Decorators `@require_auth` and `@require_role('ADMIN')` guard sensitive REST routes.

---

## 3. Data Isolation & Tenant Boundaries
- **User History Isolation**: All history queries strictly require `user_id = current_user.id`. User A cannot read or modify User B's execution logs, private project files, or notifications.
- **Hidden Test Case Protection**: Hidden test case inputs and expected outputs are never returned to clients; only test verdict and pass/fail indicators are exposed.

---

## 4. Subprocess Execution Sandboxing
- **Timeout Watchdog**: Processes strictly terminate upon reaching configured timeout limits (`subprocess.TimeoutExpired`).
- **Standard I/O Redirection**: `stdin`, `stdout`, and `stderr` are encapsulated inside dedicated subprocess pipes.
- **Temporary Scratch Isolation**: Temporary directory isolation with guaranteed deletion in `finally` handlers.
