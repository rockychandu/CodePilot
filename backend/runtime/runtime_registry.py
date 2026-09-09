"""
Language Runtime Registry & Smoke Testing Engine
Detects installed compilers/interpreters on host OS, parses versions, and runs diagnostic smoke tests.
"""

import os
import shutil
import subprocess
import tempfile
import time
from typing import Dict, List, Any, Optional

class RuntimeRegistry:
    # Comprehensive Language Definitions
    LANGUAGES: Dict[str, Dict[str, Any]] = {
        "python": {
            "id": "python",
            "displayName": "Python 3",
            "extension": ".py",
            "binaries": ["python", "python3", "py"],
            "versionCmd": ["python", "--version"],
            "compileCmd": None,
            "execCmd": ["python", "{file}"],
            "timeout": 5.0,
            "memoryLimitMb": 128.0,
            "sampleCode": "import sys\nname = sys.stdin.read().strip() or 'World'\nprint(f'Hello, {name}!')\n",
            "sampleStdin": "CodePilot\n",
            "expectedStdout": "Hello, CodePilot!\n"
        },
        "javascript": {
            "id": "javascript",
            "displayName": "JavaScript (Node.js)",
            "extension": ".js",
            "binaries": ["node", "nodejs"],
            "versionCmd": ["node", "--version"],
            "compileCmd": None,
            "execCmd": ["node", "{file}"],
            "timeout": 5.0,
            "memoryLimitMb": 128.0,
            "sampleCode": "const fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim() || 'World';\nconsole.log(`Hello, ${input}!`);\n",
            "sampleStdin": "CodePilot\n",
            "expectedStdout": "Hello, CodePilot!\n"
        },
        "java": {
            "id": "java",
            "displayName": "Java (OpenJDK / Oracle)",
            "extension": ".java",
            "binaries": ["javac", "java"],
            "versionCmd": ["java", "-version"],
            "compileCmd": ["javac", "{file}"],
            "execCmd": ["java", "-cp", "{dir}", "Main"],
            "timeout": 6.0,
            "memoryLimitMb": 256.0,
            "sampleCode": "import java.util.Scanner;\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String name = sc.hasNext() ? sc.next() : \"World\";\n        System.out.println(\"Hello, \" + name + \"!\");\n    }\n}\n",
            "sampleStdin": "CodePilot\n",
            "expectedStdout": "Hello, CodePilot!\n"
        },
        "cpp": {
            "id": "cpp",
            "displayName": "C++ (GCC/Clang)",
            "extension": ".cpp",
            "binaries": ["g++", "clang++"],
            "versionCmd": ["g++", "--version"],
            "compileCmd": ["g++", "-O2", "{file}", "-o", "{out}"],
            "execCmd": ["{out}"],
            "timeout": 3.0,
            "memoryLimitMb": 128.0,
            "sampleCode": "#include <iostream>\n#include <string>\nusing namespace std;\nint main() {\n    string name;\n    if (!(cin >> name)) name = \"World\";\n    cout << \"Hello, \" << name << \"!\" << endl;\n    return 0;\n}\n",
            "sampleStdin": "CodePilot\n",
            "expectedStdout": "Hello, CodePilot!\n"
        },
        "c": {
            "id": "c",
            "displayName": "C (GCC/Clang)",
            "extension": ".c",
            "binaries": ["gcc", "clang"],
            "versionCmd": ["gcc", "--version"],
            "compileCmd": ["gcc", "-O2", "{file}", "-o", "{out}"],
            "execCmd": ["{out}"],
            "timeout": 3.0,
            "memoryLimitMb": 128.0,
            "sampleCode": "#include <stdio.h>\nint main() {\n    char name[100] = \"World\";\n    if (scanf(\"%99s\", name) == 1) {}\n    printf(\"Hello, %s!\\n\", name);\n    return 0;\n}\n",
            "sampleStdin": "CodePilot\n",
            "expectedStdout": "Hello, CodePilot!\n"
        },
        "go": {
            "id": "go",
            "displayName": "Go (Golang)",
            "extension": ".go",
            "binaries": ["go"],
            "versionCmd": ["go", "version"],
            "compileCmd": None,
            "execCmd": ["go", "run", "{file}"],
            "timeout": 5.0,
            "memoryLimitMb": 128.0,
            "sampleCode": "package main\nimport (\n    \"fmt\"\n    \"bufio\"\n    \"os\"\n    \"strings\"\n)\nfunc main() {\n    reader := bufio.NewReader(os.Stdin)\n    name, _ := reader.ReadString('\\n')\n    name = strings.TrimSpace(name)\n    if name == \"\" { name = \"World\" }\n    fmt.Printf(\"Hello, %s!\\n\", name)\n}\n",
            "sampleStdin": "CodePilot\n",
            "expectedStdout": "Hello, CodePilot!\n"
        },
        "rust": {
            "id": "rust",
            "displayName": "Rust (rustc)",
            "extension": ".rs",
            "binaries": ["rustc"],
            "versionCmd": ["rustc", "--version"],
            "compileCmd": ["rustc", "{file}", "-o", "{out}"],
            "execCmd": ["{out}"],
            "timeout": 5.0,
            "memoryLimitMb": 128.0,
            "sampleCode": "use std::io::{self, Read};\nfn main() {\n    let mut input = String::new();\n    io::stdin().read_to_string(&mut input).unwrap();\n    let name = input.trim();\n    let final_name = if name.is_empty() { \"World\" } else { name };\n    println!(\"Hello, {}!\", final_name);\n}\n",
            "sampleStdin": "CodePilot\n",
            "expectedStdout": "Hello, CodePilot!\n"
        },
        "typescript": {
            "id": "typescript",
            "displayName": "TypeScript (ts-node / node)",
            "extension": ".ts",
            "binaries": ["ts-node", "node"],
            "versionCmd": ["node", "--version"],
            "compileCmd": None,
            "execCmd": ["node", "{file}"],
            "timeout": 5.0,
            "memoryLimitMb": 128.0,
            "sampleCode": "const fs = require('fs');\nconst input: string = fs.readFileSync(0, 'utf-8').trim() || 'World';\nconsole.log(`Hello, ${input}!`);\n",
            "sampleStdin": "CodePilot\n",
            "expectedStdout": "Hello, CodePilot!\n"
        }
    }

    @classmethod
    def get_installed_languages(cls) -> List[Dict[str, Any]]:
        """Scan system for available language binaries and return catalog."""
        result = []
        for lang_id, defn in cls.LANGUAGES.items():
            installed = False
            bin_path = None
            for b in defn["binaries"]:
                p = shutil.which(b)
                if p:
                    installed = True
                    bin_path = p
                    break
            
            version = "Not Installed"
            if installed:
                try:
                    res = subprocess.run(defn["versionCmd"], capture_output=True, text=True, timeout=3)
                    version = (res.stdout or res.stderr).strip().split('\n')[0]
                except Exception:
                    version = "Detected"

            result.append({
                "id": lang_id,
                "displayName": defn["displayName"],
                "extension": defn["extension"],
                "installed": installed,
                "binaryPath": bin_path,
                "version": version,
                "defaultTimeout": defn["timeout"],
                "memoryLimit": defn["memoryLimitMb"]
            })
        return result

    @classmethod
    def run_diagnostics(cls) -> List[Dict[str, Any]]:
        """Run actual code compilation and execution smoke tests for each language."""
        from codepilot.engine.execution_sandbox import ExecutionSandbox

        reports = []
        for lang_id, defn in cls.LANGUAGES.items():
            # Check binary
            has_bin = any(shutil.which(b) for b in defn["binaries"])
            if not has_bin:
                reports.append({
                    "language": lang_id,
                    "displayName": defn["displayName"],
                    "installed": False,
                    "status": "NOT_INSTALLED",
                    "version": "None",
                    "testPassed": False,
                    "output": "Compiler/interpreter binary not found on system PATH."
                })
                continue

            # Run smoke test through Execution Sandbox
            start_t = time.time()
            res = ExecutionSandbox.execute_code(
                language=lang_id,
                source_code=defn["sampleCode"],
                stdin_data=defn["sampleStdin"],
                timeout=defn["timeout"],
                memory_limit_mb=defn["memoryLimitMb"]
            )
            elapsed = time.time() - start_t

            passed = (res["status"] == "ACCEPTED" and defn["expectedStdout"].strip() in res["stdout"].strip())
            reports.append({
                "language": lang_id,
                "displayName": defn["displayName"],
                "installed": True,
                "status": "PASS" if passed else "FAIL",
                "version": defn["displayName"],
                "testPassed": passed,
                "runtime": f"{elapsed:.3f}s",
                "output": res["stdout"] if passed else (res["stderr"] or res["stdout"])
            })

        return reports
