# CodePilot — Multi-Language Execution Engine

The CodePilot Execution Engine coordinates process sandboxing, resource containment, and language adapters for high-concurrency developer code execution.

---

## 1. Supported Language Engines
- **Python**: Native Python 3.12+ with AST verification and standard library access.
- **JavaScript (Node.js)**: V8 engine execution with async I/O.
- **TypeScript**: `tsc` compiler checking with Node.js runtime.
- **C**: GCC 13+ with `-O2 -Wall` optimization flags.
- **C++**: G++ 13+ with `-O3 -std=c++20` modern standard compliance.
- **Java**: OpenJDK 21 `javac` / `java` virtual machine.
- **Go**: Golang 1.22+ compiled binaries.
- **Rust**: Rustc 2021 edition compiler with `-O` optimizations.
- **PHP**: PHP 8.3 CLI interpreter.
- **Ruby**: Ruby 3.3 YARV interpreter.

---

## 2. Resource & Safety Controls
- **Process Timeout**: Configurable hard execution limit (default 5.0s, problem-specific overrides).
- **Process Memory Cap**: Monitored peak memory allocation with cap enforcement (default 128 MB).
- **Subprocess Isolation**: Isolated scratch directories generated via `tempfile.mkdtemp` with cleanup on exit.
- **Dynamic Simulator Fallback**: Automatically provides simulated execution when native host compilers are unavailable in local development environments.
