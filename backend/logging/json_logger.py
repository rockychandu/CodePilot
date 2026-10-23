"""
Structured JSON Application Logger with Automated Redaction
"""
import json
import logging
import datetime

REDACTED_KEYS = {"password", "token", "secret", "authorization", "cookie", "apikey", "api_key"}

class JSONLogFormatter(logging.Formatter):
    def redact_data(self, data):
        if isinstance(data, dict):
            return {k: ("[REDACTED]" if k.lower() in REDACTED_KEYS else self.redact_data(v)) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.redact_data(x) for x in data]
        return data

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }
        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            log_obj["data"] = self.redact_data(record.extra_data)
        return json.dumps(log_obj)
