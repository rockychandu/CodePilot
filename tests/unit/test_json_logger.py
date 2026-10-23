import unittest
import logging
import json
from backend.logging.json_logger import JSONLogFormatter

class TestJSONLogger(unittest.TestCase):
    def setUp(self):
        self.formatter = JSONLogFormatter()

    def test_redaction(self):
        clean = self.formatter.redact_data({
            "username": "alice",
            "password": "Password123!",
            "token": "jwt-token-val",
            "meta": {"api_key": "secret-123"}
        })
        self.assertEqual(clean["username"], "alice")
        self.assertEqual(clean["password"], "[REDACTED]")
        self.assertEqual(clean["token"], "[REDACTED]")
        self.assertEqual(clean["meta"]["api_key"], "[REDACTED]")

    def test_formatting_json(self):
        rec = logging.LogRecord("test", logging.INFO, "test.py", 10, "Test log message", (), None)
        out = self.formatter.format(rec)
        parsed = json.loads(out)
        self.assertEqual(parsed["level"], "INFO")
        self.assertEqual(parsed["message"], "Test log message")

    def test_empty_record(self):
        rec = logging.LogRecord("test", logging.WARNING, "test.py", 20, "Warning msg", (), None)
        out = self.formatter.format(rec)
        self.assertIn('"level": "WARNING"', out)

if __name__ == "__main__":
    unittest.main()
