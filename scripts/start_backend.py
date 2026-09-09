#!/usr/bin/env python3
"""
CodePilot Backend Service Manager
Initializes database schema, verifies environment prerequisites, and runs Flask API server.
"""

import os
import sys
import subprocess

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, root_dir)

    print("=" * 60)
    print("  CodePilot Production Backend Service Launcher")
    print("=" * 60)

    # Check python version
    major, minor = sys.version_info[:2]
    print(f"[*] Python Runtime: {major}.{minor} ({sys.executable})")

    # Initialize DB & Seed
    try:
        from codepilot.db.connection import init_db
        from codepilot.db.seed import seed_database
        print("[*] Initializing Database Models & Tables...")
        init_db()
        print("[*] Seeding System Data & Initial Problems...")
        seed_database()
        print("[+] Database Ready.")
    except Exception as e:
        print(f"[!] Warning during DB bootstrap: {e}")

    # Start backend
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"[+] Starting API listener on http://{host}:{port}")
    
    from backend.app import app
    app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    main()
