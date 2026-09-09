"""
Anti-Brute-Force Rate Limiting & Failed Attempt Tracker
"""

import time
import threading
from datetime import datetime, timezone, timedelta
from typing import Optional
from codepilot.db.connection import get_db_session
from codepilot.db.models import LoginAttempt

class AuthRateLimiter:
    def __init__(self, max_attempts: int = 10, lockout_window_minutes: int = 15, lockout_seconds: Optional[int] = None):
        self.max_attempts = max_attempts
        if lockout_seconds is not None:
            self.lockout_window_seconds = lockout_seconds
        else:
            self.lockout_window_seconds = lockout_window_minutes * 60
        self._lock = threading.Lock()

    def record_attempt(self, ip_address: str, identifier: str, success: bool, failure_reason: str = ""):
        try:
            with get_db_session() as db:
                att = LoginAttempt(
                    ip_address=ip_address or "127.0.0.1",
                    username_or_email=identifier.lower().strip() if identifier else "unknown",
                    attempted_at=datetime.now(timezone.utc),
                    success=success,
                    failure_reason=failure_reason
                )
                db.add(att)
                db.commit()
        except Exception:
            pass

    def is_locked(self, ip_address: str, identifier: str) -> bool:
        """Check if IP or identifier has exceeded failed attempts threshold in recent window."""
        try:
            with get_db_session() as db:
                clean_ip = ip_address or "127.0.0.1"
                clean_id = (identifier or "").lower().strip()

                since = datetime.now(timezone.utc) - timedelta(seconds=self.lockout_window_seconds)

                # Check if there was a more recent successful login
                latest_success = db.query(LoginAttempt).filter(
                    ((LoginAttempt.ip_address == clean_ip) | (LoginAttempt.username_or_email == clean_id)),
                    LoginAttempt.success == True
                ).order_by(LoginAttempt.attempted_at.desc()).first()

                if latest_success and latest_success.attempted_at:
                    succ_at = latest_success.attempted_at
                    if succ_at.tzinfo is None:
                        succ_at = succ_at.replace(tzinfo=timezone.utc)
                    if succ_at > since:
                        since = succ_at

                failed_count = db.query(LoginAttempt).filter(
                    ((LoginAttempt.ip_address == clean_ip) | (LoginAttempt.username_or_email == clean_id)),
                    LoginAttempt.success == False,
                    LoginAttempt.attempted_at >= since
                ).count()

                return failed_count >= self.max_attempts
        except Exception:
            return False

auth_rate_limiter = AuthRateLimiter()
