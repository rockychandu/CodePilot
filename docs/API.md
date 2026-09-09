# CodePilot REST API v1 Specification

Base URL: `/api/v1`

---

## 1. Authentication Endpoints (`/api/v1/auth`)

### `POST /auth/register`
Register a new developer account.
- **Request Body**:
  ```json
  {
    "username": "alex_dev",
    "email": "alex@codepilot.dev",
    "password": "StrongPassword#2026!",
    "confirmPassword": "StrongPassword#2026!",
    "displayName": "Alex Rivera"
  }
  ```
- **Response (201)**:
  ```json
  {
    "success": true,
    "token": "eyJhbGciOi...",
    "refreshToken": "48_char_token",
    "user": { "id": 1, "username": "alex_dev", "email": "alex@codepilot.dev", "role": "USER" }
  }
  ```

### `POST /auth/login`
Authenticate existing user credentials.
- **Request Body**:
  ```json
  {
    "identifier": "alex_dev",
    "password": "StrongPassword#2026!"
  }
  ```
- **Response (200)**: Token pair and user profile payload.

### `POST /auth/refresh`
Obtain a new JWT access token using a valid refresh token.

### `GET /auth/me`
Retrieve authenticated user profile and settings (`Authorization: Bearer <token>`).

### `POST /auth/logout`
Revoke current session token.

### `POST /auth/logout-all`
Revoke all active sessions for current user across all devices.

### `PUT /auth/change-password`
Update user password after verifying current password.

---

## 2. Execution & Sandbox Endpoints (`/api/v1/execution`)

### `POST /execution/run`
Execute code in an isolated subprocess sandbox.
- **Request Body**:
  ```json
  {
    "language": "python",
    "code": "print('Hello World')",
    "stdin": ""
  }
  ```
- **Response (200)**:
  ```json
  {
    "status": "SUCCESS",
    "stdout": "Hello World\n",
    "stderr": "",
    "exit_code": 0,
    "execution_time_ms": 42.5,
    "memory_mb": 14.2
  }
  ```

---

## 3. Problem & Judge Endpoints (`/api/v1/problems`, `/api/v1/submissions`)

### `GET /problems`
List catalog problems with difficulty and tag filters.

### `GET /problems/<id_or_slug>`
Retrieve problem specifications, starter templates, and public test cases.

### `POST /submissions`
Submit solution for multi-test-case judge evaluation against hidden tests.

---

## 4. Contest Endpoints (`/api/v1/contests`)

### `GET /contests`
List active, upcoming, and past competitive programming contests.

### `GET /contests/<id>/leaderboard`
Retrieve live contest ranking table with penalty metrics.

---

## 5. History & Audit Endpoints (`/api/v1/history`)

### `GET /history`
Retrieve paginated chronological activity history for the authenticated user.
