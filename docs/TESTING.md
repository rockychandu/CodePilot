# CodePilot Testing Strategy & Automated Quality Gates

CodePilot employs a multi-tiered automated testing hierarchy spanning algorithmic unit tests, API integration tests, security & cryptographic verification, and frontend component assertions.

---

## Running the Automated Test Suites

### 1. Comprehensive Algorithmic & Security Test Suite (466 tests)
Validates core platform algorithms, sandbox execution, problem judge verifiers, Elo calculators, and static code analyzers:
```bash
python tests/comprehensive_suite.py
```

### 2. Authentication & User Session Suite (7 test scenarios)
Validates salted PBKDF2 hashing, JWT access/refresh token rotation, rate limiting lockouts, password resets, email verification, and session revocation:
```bash
python -m unittest tests/auth/test_auth_system.py
```

### 3. Modular API v1 Integration Suite (9 test suites)
Validates all REST endpoints across `/api/v1/auth`, `/api/v1/execution`, `/api/v1/problems`, `/api/v1/contests`, `/api/v1/courses`, `/api/v1/history`, and `/api/v1/diagnostics`:
```bash
python -m unittest tests/api/test_modular_api.py
```

### 4. Frontend Component & Storage Suite (5 tests)
Validates client localStorage/sessionStorage persistence, language registries, password strength scoring, and judge verdict mapping:
```bash
npm test
```

### 5. Production Bundle Build Verification
Ensures all frontend JavaScript, CSS tokens, and templates compile without bundle errors:
```bash
npm run build
```
