# CodePilot Multi-Language Execution Engine & Sandbox

## Overview
The CodePilot Execution Engine provides secure, isolated, and deterministic process execution across multiple programming language runtimes without executing code in the main web server process.

---

## Architecture Lifecycle

```
User Code Submission
      │
      ▼
Execution Manager (/api/v1/execution/run)
      │
      ▼
Language Runtime Resolver (RuntimeConfig)
      │
      ▼
Temporary Sandbox Directory Isolation (/tmp/sandbox_*)
      │
      ▼
Compilation Step (gcc, g++, javac, go build, rustc, tsc)
      │
      ▼
Subprocess Spawner with Resource Watchdogs
      │
      ├── Timeout Guard (threading.Timer / subprocess.communicate timeout)
      ├── Memory Cap Monitor (psutil RSS tracker)
      └── Stdin Stream Pipe & Output Truncation
      │
      ▼
Result Evaluator & History Persistence
```

---

## Supported Runtimes

| Language | Compiler / Interpreter | Execution Command | Default Timeout | Memory Cap |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | Python 3.10+ | `python main.py` | 5.0s | 128 MB |
| **JavaScript**| Node.js 20+ | `node main.js` | 5.0s | 128 MB |
| **TypeScript**| TypeScript Compiler | `node main.js` | 5.0s | 128 MB |
| **C** | GCC 13+ (`-O2 -Wall`) | `./main` | 3.0s | 64 MB |
| **C++** | G++ 13+ (`-O3 -std=c++20`) | `./main` | 3.0s | 64 MB |
| **Java** | OpenJDK 21 | `java Main` | 5.0s | 256 MB |
| **Go** | Go 1.22+ (`go build`) | `./main` | 4.0s | 128 MB |
| **Rust** | Rustc (`-O 2021 Edition`)| `./main` | 4.0s | 128 MB |
| **C#** | .NET 8 SDK | `dotnet run` | 5.0s | 256 MB |
| **PHP** | PHP 8.3+ | `php main.php` | 5.0s | 128 MB |
| **Ruby** | Ruby 3.3+ | `ruby main.rb` | 5.0s | 128 MB |

---

## Security Safeguards
1. **Isolated Subprocess Trees**: Code execution is launched via decoupled subprocesses with restricted environment variables.
2. **Strict Timeouts**: Guaranteed termination of infinite loops or deadlocks.
3. **Memory Limits**: Automatic process kill if RSS usage exceeds configured threshold (`MEMORY_LIMIT_EXCEEDED`).
4. **Output Truncation**: Output streams capped to 1MB to prevent buffer exhaustion.
