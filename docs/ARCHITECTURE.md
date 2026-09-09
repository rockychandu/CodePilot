# CodePilot System Architecture & Python Integration Guide

CodePilot is a commercial-grade developer platform ("Code. Learn. Build. Compete.") featuring a major Python architecture (`codepilot/` core package with AST sandbox engine, dataclass models, and CLI runner) paired with a high-performance modular frontend client.

## High-Level System Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        CodePilot Application                           │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Frontend Client Interface (HTML5, Modern CSS, ES Modules)           │
│    - SPA Router (Hash-based with deep link params)                     │
│    - VS Code-Grade IDE Editor (Multi-file tabs, Line numbers)         │
│    - Execution Simulator & Console (Preparing -> Compiling -> Output) │
│    - Integrated Test Runner (In-browser automated testing)            │
│                                                                        │
│ 2. Python Core Engine Package (`codepilot/`)                           │
│    - Engine: `sandbox.py` (AST Code Analyzer & Complexity Checker)    │
│    - AI Assistant: `ai_assistant.py` (PEP8 Linter & AI Code Review)    │
│    - Data Models: `user.py`, `problem.py`, `submission.py`             │
│    - CLI Runner: `cli.py` (`python -m codepilot`)                      │
│                                                                        │
│ 3. Python Backend Server (`backend/app.py`)                            │
│    - Flask/FastAPI REST APIs (/api/execute, /api/auth, /api/ai)        │
│    - Execution Subprocess Worker Sandbox                               │
└────────────────────────────────────────────────────────────────────────┘
```

## Python Backend Integration Contract

For your backend teammate connecting Python services to the frontend:

1. **Code Execution API**:
   - **Endpoint**: `POST /api/execute`
   - **Payload**:
     ```json
     {
       "language": "python",
       "sourceCode": "def two_sum(nums, target): return []",
       "stdin": ""
     }
     ```
   - **Response**:
     ```json
     {
       "status": "Accepted",
       "output": "[0, 1]",
       "runtime": "0.034s",
       "memory": "12.4 MB",
       "exitCode": 0
     }
     ```

2. **Authentication API**:
   - **Endpoint**: `POST /api/auth/login`
   - **Payload**: `{ "email": "alex@codepilot.io", "password": "••••••••" }`

3. **Pilot AI Assistance API**:
   - **Endpoint**: `POST /api/ai/explain`
   - **Payload**: `{ "code": "def solve(): pass", "prompt": "Explain time complexity" }`
