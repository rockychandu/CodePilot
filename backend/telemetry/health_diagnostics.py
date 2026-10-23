"""
System Health Check & Runtime Diagnostics Telemetry
"""
import os
import sys
import time
import platform
from codepilot.db.connection import get_db_session

START_TIME = time.time()

class HealthDiagnostics:
    @staticmethod
    def get_system_status() -> dict:
        uptime = round(time.time() - START_TIME, 2)
        db_ok = False
        try:
            with get_db_session() as db:
                db.execute(__import__('sqlalchemy').text("SELECT 1"))
                db_ok = True
        except Exception:
            db_ok = False

        status = "HEALTHY" if db_ok else "DEGRADED"
        return {
            "status": status,
            "database": "CONNECTED" if db_ok else "DISCONNECTED",
            "uptimeSeconds": uptime,
            "platform": platform.platform(),
            "pythonVersion": platform.python_version(),
            "environment": os.environ.get("ENV", "production")
        }
