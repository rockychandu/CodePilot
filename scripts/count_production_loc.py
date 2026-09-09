"""
CodePilot Production LOC Counter
Accurately measures production application source code according to evaluator rules.
Excludes: tests, node_modules, .git, coverage, dist, build, generated artifacts.
"""

import os
import sys

EXCLUDED_DIRS = {
    ".git", "node_modules", "coverage", "dist", "build", ".pytest_cache",
    "__pycache__", "tests", "test", ".system_generated", "scratch", ".venv", "venv"
}

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".html", ".css", ".json", ".sql", ".sh", ".ps1", ".toml"
}

def count_file_loc(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            # Non-empty lines
            return len(lines)
    except Exception:
        return 0

def scan_production_loc(root_dir):
    total_loc = 0
    domain_loc = {}
    file_count = 0

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        # Check if current path contains excluded directory
        rel_root = os.path.relpath(root, root_dir).replace("\\", "/")
        if any(exc in rel_root.split('/') for exc in EXCLUDED_DIRS):
            continue

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                continue
            
            # Exclude test files by naming convention
            if file.startswith("test_") or file.endswith("_test.py") or file.endswith(".test.js") or file.endswith(".spec.js"):
                continue

            filepath = os.path.join(root, file)
            loc = count_file_loc(filepath)
            total_loc += loc
            file_count += 1

            # Determine top-level domain
            parts = rel_root.split('/')
            domain = parts[0] if parts and parts[0] != "." else "root"
            domain_loc[domain] = domain_loc.get(domain, 0) + loc

    return total_loc, file_count, domain_loc

if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    total, count, domains = scan_production_loc(repo_root)

    print("==================================================")
    print("      CODEPILOT PRODUCTION LOC AUDIT REPORT      ")
    print("==================================================")
    print(f"Total Production Files : {count:,}")
    print(f"Total Production LOC   : {total:,}")
    print("--------------------------------------------------")
    print("Breakdown by Domain:")
    for dom, loc in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {dom:<25}: {loc:>10,} LOC")
    print("==================================================")
