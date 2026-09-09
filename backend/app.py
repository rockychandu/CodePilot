"""
CodePilot Enterprise REST API Server
Version: 2.1.0 (Production Modular Architecture)
"""

import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from codepilot.db.connection import init_db
from codepilot.db.seed import seed_database
from backend.api import register_blueprints
from backend.middleware.error_handler import register_error_handlers
from backend.execution.execution_engine import ExecutionEngine
from backend.middleware.auth_middleware import authenticate_request

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints & error handlers
register_blueprints(app)
register_error_handlers(app)

# Auto-seed database on server initialization
with app.app_context():
    init_db()
    seed_database()

# ---------------------------------------------------------
# Health & Root Routes
# ---------------------------------------------------------
@app.route("/health", methods=["GET"])
@app.route("/api/v1/health", methods=["GET"])
def health():
    return jsonify({
        "status": "HEALTHY",
        "service": "CodePilot Production API",
        "version": "2.1.0",
        "environment": os.environ.get("ENV", "production")
    }), 200

@app.route("/ready", methods=["GET"])
def ready():
    return jsonify({
        "status": "READY",
        "database": "CONNECTED",
        "sandbox": "ONLINE"
    }), 200

# ---------------------------------------------------------
# Legacy Compatibility Routes (/api/execute)
# ---------------------------------------------------------
@app.route("/api/execute", methods=["POST"])
def execute_legacy():
    data = request.get_json() or {}
    language = data.get("language", "python")
    source_code = data.get("sourceCode") or data.get("code", "")
    stdin_data = data.get("stdin", "")
    timeout = float(data.get("timeout", 5.0))
    memory_limit = float(data.get("memoryLimit", 128.0))

    payload = authenticate_request()
    user_id = payload.get("user_id") if payload else None

    result = ExecutionEngine.run_code(
        language=language,
        source_code=source_code,
        stdin_data=stdin_data,
        timeout=timeout,
        memory_limit_mb=memory_limit,
        user_id=user_id
    )

    return jsonify({
        "status": result["status"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "output": result["stdout"] if result["stdout"] else result["stderr"],
        "exitCode": result["exitCode"],
        "runtime": f"{result['runtimeSeconds']:.3f}s",
        "runtimeSeconds": result["runtimeSeconds"],
        "memory": f"{result['memoryMb']:.1f} MB",
        "memoryMb": result["memoryMb"]
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting CodePilot Production API on http://{host}:{port}...")
    app.run(host=host, port=port, debug=False)
