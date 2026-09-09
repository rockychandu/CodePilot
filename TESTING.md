# CodePilot — Automated Testing & Verification Guide

CodePilot features a **500+ automated test suite** covering unit, security, integration, execution sandboxing, and REST API layers.

---

## 1. Running the Test Suite

```bash
# Run complete test suite (500+ tests)
python -m unittest discover tests -p "*.py"

# Run specific unit test module
python -m unittest tests/unit/test_security.py
python -m unittest tests/unit/test_auth_service.py
python -m unittest tests/unit/test_ai_engine.py

# Run REST API integration tests
python -m unittest tests/api/test_api_v1.py

# Run execution sandbox tests
python -m unittest tests/execution/test_sandbox.py
```

---

## 2. Test Architecture Breakdown
1. **Security & Auth (`tests/unit/test_security.py`, `tests/unit/test_auth_service.py`)**: Tests PBKDF2 salt hashing, JWT signatures, token tampering, and password strength policies.
2. **Execution Sandbox (`tests/execution/test_sandbox.py`, `tests/execution/test_judge.py`)**: Tests multi-language compilers, stdin/stdout piping, process memory estimation, and timeout watchdogs.
3. **Pilot AI Suite (`tests/unit/test_ai_engine.py`)**: Verifies AST static parsing, asymptotic complexity estimations ($O(1)$, $O(N)$, $O(N^2)$), and unit test synthesis.
4. **REST API v1 (`tests/api/test_api_v1.py`)**: Tests all versioned HTTP endpoints, RBAC permission barriers, and JSON responses.
5. **Algorithmic Suite (`tests/comprehensive_suite.py`)**: 460+ parameterized cases testing dynamic programming, string algorithms, sorting, and cryptographic invariants.
