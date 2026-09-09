"""
CodePilot Multi-Language Runtime Manager
Maintains registry of compilers/interpreters, verifies host runtime availability,
and executes diagnostic smoke tests.
"""

import shutil
import subprocess
import time
import os
import sys


class RuntimeManager:
    # Language registry specifications
    LANGUAGE_REGISTRY = {
        "python": {
            "name": "Python",
            "extension": ".py",
            "type": "interpreted",
            "executable_candidates": [sys.executable, "python3", "python"],
            "version_flag": "--version",
            "test_hello": "print('Hello, CodePilot!')",
            "test_io": "x = input()\nprint(f'ECHO: {x}')",
            "expected_hello": "Hello, CodePilot!\n"
        },
        "javascript": {
            "name": "JavaScript (Node.js)",
            "extension": ".js",
            "type": "interpreted",
            "executable_candidates": ["node", "nodejs"],
            "version_flag": "-v",
            "test_hello": "console.log('Hello, CodePilot!');",
            "test_io": "const fs = require('fs'); const input = fs.readFileSync(0, 'utf-8').trim(); console.log('ECHO: ' + input);",
            "expected_hello": "Hello, CodePilot!\n"
        },
        "c": {
            "name": "C (GCC)",
            "extension": ".c",
            "type": "compiled",
            "compiler_candidates": ["gcc", "clang"],
            "compile_args": ["-O2", "-Wall"],
            "version_flag": "--version",
            "test_hello": '#include <stdio.h>\nint main() { printf("Hello, CodePilot!\\n"); return 0; }',
            "test_io": '#include <stdio.h>\nint main() { char buf[100]; if (scanf("%99s", buf) == 1) printf("ECHO: %s\\n", buf); return 0; }',
            "expected_hello": "Hello, CodePilot!\n"
        },
        "cpp": {
            "name": "C++ (G++)",
            "extension": ".cpp",
            "type": "compiled",
            "compiler_candidates": ["g++", "clang++"],
            "compile_args": ["-O3", "-std=c++20"],
            "version_flag": "--version",
            "test_hello": '#include <iostream>\nint main() { std::cout << "Hello, CodePilot!" << std::endl; return 0; }',
            "test_io": '#include <iostream>\n#include <string>\nint main() { std::string s; std::cin >> s; std::cout << "ECHO: " << s << std::endl; return 0; }',
            "expected_hello": "Hello, CodePilot!\n"
        },
        "java": {
            "name": "Java (OpenJDK)",
            "extension": ".java",
            "type": "compiled_jvm",
            "compiler_candidates": ["javac"],
            "runtime_candidates": ["java"],
            "version_flag": "-version",
            "test_hello": 'public class Main { public static void main(String[] args) { System.out.println("Hello, CodePilot!"); } }',
            "test_io": 'import java.util.Scanner; public class Main { public static void main(String[] args) { Scanner sc = new Scanner(System.in); if(sc.hasNext()) System.out.println("ECHO: " + sc.next()); } }',
            "expected_hello": "Hello, CodePilot!\n"
        },
        "go": {
            "name": "Go",
            "extension": ".go",
            "type": "compiled",
            "compiler_candidates": ["go"],
            "version_flag": "version",
            "test_hello": 'package main\nimport "fmt"\nfunc main() { fmt.Println("Hello, CodePilot!") }',
            "test_io": 'package main\nimport "fmt"\nfunc main() { var s string; fmt.Scan(&s); fmt.Println("ECHO:", s) }',
            "expected_hello": "Hello, CodePilot!\n"
        },
        "rust": {
            "name": "Rust",
            "extension": ".rs",
            "type": "compiled",
            "compiler_candidates": ["rustc"],
            "compile_args": ["-O"],
            "version_flag": "--version",
            "test_hello": 'fn main() { println!("Hello, CodePilot!"); }',
            "test_io": 'use std::io; fn main() { let mut s = String::new(); io::stdin().read_line(&mut s).unwrap(); print!("ECHO: {}", s); }',
            "expected_hello": "Hello, CodePilot!\n"
        },
        "ruby": {
            "name": "Ruby",
            "extension": ".rb",
            "type": "interpreted",
            "executable_candidates": ["ruby"],
            "version_flag": "-v",
            "test_hello": "puts 'Hello, CodePilot!'",
            "test_io": "s = gets&.strip; puts \"ECHO: #{s}\"",
            "expected_hello": "Hello, CodePilot!\n"
        },
        "php": {
            "name": "PHP",
            "extension": ".php",
            "type": "interpreted",
            "executable_candidates": ["php"],
            "version_flag": "-v",
            "test_hello": "<?php echo \"Hello, CodePilot!\\n\"; ?>",
            "test_io": "<?php $s = trim(fgets(STDIN)); echo \"ECHO: $s\\n\"; ?>",
            "expected_hello": "Hello, CodePilot!\n"
        }
    }

    @classmethod
    def get_available_runtimes(cls) -> list[dict]:
        """Detect and return runtime health matrix for all configured languages."""
        results = []
        for lang_id, spec in cls.LANGUAGE_REGISTRY.items():
            info = {
                "languageId": lang_id,
                "name": spec["name"],
                "type": spec["type"],
                "isInstalled": False,
                "version": "Not detected on host",
                "executable": None,
                "status": "UNAVAILABLE"
            }

            candidates = spec.get("compiler_candidates") or spec.get("executable_candidates") or []
            for cmd in candidates:
                path = shutil.which(cmd) if cmd != sys.executable else cmd
                if path:
                    info["isInstalled"] = True
                    info["executable"] = path
                    # Detect version
                    try:
                        v_arg = spec["version_flag"].split()
                        res = subprocess.run([path] + v_arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
                        ver_out = res.stdout if res.stdout else res.stderr
                        info["version"] = ver_out.strip().split("\n")[0][:60]
                        info["status"] = "AVAILABLE"
                    except Exception as e:
                        info["version"] = f"Detected ({e})"
                        info["status"] = "AVAILABLE"
                    break

            results.append(info)
        return results

    @classmethod
    def run_runtime_smoke_tests(cls) -> list[dict]:
        """Run smoke test suite across all languages."""
        from codepilot.engine.execution_sandbox import ExecutionSandbox
        report = []
        available = cls.get_available_runtimes()

        for rt in available:
            lang_id = rt["languageId"]
            spec = cls.LANGUAGE_REGISTRY.get(lang_id)
            if not spec:
                continue

            test_item = {
                "language": rt["name"],
                "languageId": lang_id,
                "version": rt["version"],
                "isInstalled": rt["isInstalled"],
                "helloWorld": "SKIPPED",
                "ioTest": "SKIPPED",
                "overallStatus": "PASS" if rt["isInstalled"] else "UNAVAILABLE"
            }

            if rt["isInstalled"]:
                # 1. Hello World
                res_hello = ExecutionSandbox.execute_code(lang_id, spec["test_hello"], stdin_data="", timeout=5.0)
                if res_hello["status"] == "ACCEPTED" and "Hello, CodePilot!" in res_hello["stdout"]:
                    test_item["helloWorld"] = "PASS"
                else:
                    test_item["helloWorld"] = "FAIL"
                    test_item["overallStatus"] = "FAIL"

                # 2. IO Test
                res_io = ExecutionSandbox.execute_code(lang_id, spec["test_io"], stdin_data="SmokeTestInput", timeout=5.0)
                if res_io["status"] == "ACCEPTED" and "SmokeTestInput" in res_io["stdout"]:
                    test_item["ioTest"] = "PASS"
                else:
                    test_item["ioTest"] = "FAIL"
                    test_item["overallStatus"] = "FAIL"

            report.append(test_item)

        return report
