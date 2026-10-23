import unittest
from backend.telemetry.health_diagnostics import HealthDiagnostics

class TestHealthDiagnostics(unittest.TestCase):
    def test_status_fields(self):
        diag = HealthDiagnostics.get_system_status()
        self.assertIn(diag["status"], ["HEALTHY", "DEGRADED"])
        self.assertIn("database", diag)
        self.assertIsInstance(diag["uptimeSeconds"], (int, float))

    def test_platform_reporting(self):
        diag = HealthDiagnostics.get_system_status()
        self.assertTrue(len(diag["platform"]) > 0)
        self.assertTrue(len(diag["pythonVersion"]) > 0)

    def test_db_ping(self):
        diag = HealthDiagnostics.get_system_status()
        self.assertEqual(diag["database"], "CONNECTED")

if __name__ == "__main__":
    unittest.main()
