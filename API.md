# CodePilot — REST API Reference (v1)

Base URL: `http://localhost:5000/api/v1`

---

## 1. System & Observability

### `GET /health` or `GET /api/v1/health`
Check API service health and environment status.
- **Response `200 OK`**:
```json
{
  "status": "HEALTHY",
  "service": "CodePilot Production API",
  "version": "2.0.0",
  "environment": "production"
}
```

### `GET /ready`
Readiness probe for database connection and execution sandbox availability.
- **Response `200 OK`**:
```json
{
  "status": "READY",
  "database": "CONNECTED",
  "sandbox": "ONLINE"
}
```

---

## 2. Authentication & Authorization (`/api/v1/auth`)

### `POST /api/v1/auth/register`
Register a new developer account.
- **Request Body**:
```json
{
  "username": "alex_coder",
  "email": "alex@example.com",
  "password": "Password@123",
  "displayName": "Alex River"
}
```
- **Response `201 Created`**:
```json
{
  "token": "eyJhbGciOi...",
  "refreshToken": "rt_1_...",
  "user": {
    "id": 1,
    "username": "alex_coder",
    "email": "alex@example.com",
    "role": "USER",
    "profile": { "xp": 100, "level": 1 }
  }
}
```

### `POST /api/v1/auth/login`
Authenticate existing user via username or email.
- **Request Body**:
```json
{
  "loginIdentifier": "alex_coder",
  "password": "Password@123"
}
```
- **Response `200 OK`**: Returns access JWT token, refresh token, and user profile.

### `POST /api/v1/auth/logout`
Revoke active session token.
- **Headers**: `Authorization: Bearer <TOKEN>`
- **Response `200 OK`**: `{ "message": "Successfully logged out." }`

### `POST /api/v1/auth/forgot-password`
Request password reset token.
- **Request Body**: `{ "email": "alex@example.com" }`

### `POST /api/v1/auth/reset-password`
Reset password using reset token.
- **Request Body**: `{ "token": "uuid-token", "password": "NewPassword@123" }`

---

## 3. User Profiles & Isolated History

### `GET /api/v1/profile`
Retrieve authenticated user profile.
- **Headers**: `Authorization: Bearer <TOKEN>`

### `PUT /api/v1/profile`
Update display name, bio, primary language, or avatar.
- **Headers**: `Authorization: Bearer <TOKEN>`
- **Request Body**:
```json
{
  "displayName": "Alex River (Senior)",
  "bio": "Competitive programmer and distributed systems engineer.",
  "primaryLanguage": "Python"
}
```

### `GET /api/v1/history`
Retrieve paginated, filtered activity logs isolated to authenticated user.
- **Headers**: `Authorization: Bearer <TOKEN>`
- **Query Parameters**:
  - `page` (int, default: 1)
  - `pageSize` (int, default: 20)
  - `activityType` (string: `EXECUTION`, `SUBMISSION`, `AI_REVIEW`, `COURSE`, `LOGIN`)
  - `language` (string)
  - `status` (string)
  - `search` (string)

---

## 4. Multi-Language Execution & Diagnostics

### `POST /api/v1/execution/run` (and `POST /api/execute`)
Execute arbitrary source code inside sandboxed subprocess.
- **Request Body**:
```json
{
  "language": "python",
  "sourceCode": "print('Hello, CodePilot!')",
  "stdin": "",
  "timeout": 5.0,
  "memoryLimit": 128.0
}
```
- **Response `200 OK`**:
```json
{
  "status": "ACCEPTED",
  "stdout": "Hello, CodePilot!\n",
  "stderr": "",
  "output": "Hello, CodePilot!\n",
  "exitCode": 0,
  "runtime": "0.018s",
  "memory": "14.5 MB"
}
```

### `GET /api/v1/runtime/languages`
List supported compiler/interpreter engines with host installation status.

### `POST /api/v1/runtime-tests/run`
Run complete automated smoke test suite across all language adapters.

---

## 5. Competitive Programming & Problems

### `GET /api/v1/problems`
List catalog problems with difficulty, tags, and category filters.

### `GET /api/v1/problems/:identifier`
Retrieve problem details, constraints, hints, and public test cases by ID or slug.

### `POST /api/v1/submissions`
Submit solution code for automated evaluation against public + hidden test cases.
- **Headers**: `Authorization: Bearer <TOKEN>`
- **Request Body**:
```json
{
  "problemId": 1,
  "language": "python",
  "sourceCode": "..."
}
```
- **Response `200 OK`**: Returns verdict (`Accepted`, `Wrong Answer`, `Time Limit Exceeded`, etc.), passed test ratio, and per-test execution telemetry.

---

## 6. Pilot AI Assistant

### `POST /api/v1/ai/review`
Run AST-based static review, style compliance, and code quality scoring.

### `POST /api/v1/ai/complexity`
Calculate asymptotic time complexity ($O(1)$, $O(N)$, $O(N^2)$, etc.) and space complexity.

### `POST /api/v1/ai/generate-tests`
Synthesize automated unit tests for functions defined in source code.

### `POST /api/v1/ai/explain-bug`
Diagnose runtime exceptions and generate actionable fix recommendations.

---

## 7. Admin & Telemetry (Role: `ADMIN`)

### `GET /api/v1/admin/telemetry`
Fetch platform-wide stats (total users, submissions, acceptance rate, executions, AI reviews).

### `GET /api/v1/admin/users`
Paginated user administration list.

### `PUT /api/v1/admin/users/:id/role`
Update user permission role (`USER`, `MODERATOR`, `INSTRUCTOR`, `ADMIN`).
