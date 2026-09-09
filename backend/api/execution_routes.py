"""
Execution API Blueprint (/api/v1/execution & /api/v1/runtime)
"""

from flask import Blueprint, request, jsonify
from backend.execution.execution_engine import ExecutionEngine
from backend.runtime.runtime_registry import RuntimeRegistry
from backend.middleware.auth_middleware import authenticate_request
from backend.middleware.rate_limit_middleware import limit_requests

execution_bp = Blueprint("execution_bp", __name__, url_prefix="/api/v1")

@execution_bp.route("/execution/run", methods=["POST"])
@limit_requests(max_per_minute=120)
def run_code():
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

@execution_bp.route("/runtime/languages", methods=["GET"])
def list_runtimes():
    return jsonify(RuntimeRegistry.get_installed_languages()), 200

@execution_bp.route("/runtime-tests/run", methods=["POST"])
def run_diagnostics():
    report = RuntimeRegistry.run_diagnostics()
    return jsonify({"diagnostics": report}), 200
