import unittest
from backend.api.meta_routes import APIMetadataService

class TestMetaService(unittest.TestCase):
    def test_metadata_structure(self):
        meta = APIMetadataService.get_metadata()
        self.assertEqual(meta["version"], "2.1.0")
        self.assertEqual(meta["apiPrefix"], "/api/v1")
        self.assertEqual(meta["status"], "GA")

    def test_runtime_catalog(self):
        meta = APIMetadataService.get_metadata()
        self.assertEqual(meta["runtimeCount"], 7)
        langs = [r["language"] for r in meta["runtimes"]]
        self.assertIn("python", langs)
        self.assertIn("cpp", langs)
        self.assertIn("rust", langs)

    def test_runtime_metadata_fields(self):
        meta = APIMetadataService.get_metadata()
        for r in meta["runtimes"]:
            self.assertIn("version", r)
            self.assertIn("standard", r)

if __name__ == "__main__":
    unittest.main()
